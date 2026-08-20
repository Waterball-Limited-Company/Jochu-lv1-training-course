# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FLOW_V2_RE = re.compile(r"(?mi)^流程版本\s*[:：]\s*2\s*$")
JSON_BLOCK_RE = re.compile(
    r"## 可機械驗證契約\s+.*?```json\s*(\{.*?\})\s*```",
    re.S,
)
CONTRACT_LABEL_RE = re.compile(
    r"^\s*-\s*(?:\*\*)?(?:API\s+)?契約案例(?:\*\*)?[：:]?\s*(.*)$"
)
CONTRACT_ID_RE = re.compile(r"\bAPI-\d{3}-C\d+\b")
API_USAGE_RE = re.compile(r"\b(?:GET|POST|PUT|PATCH|DELETE)\s+/|API Mock")

SOURCE_TO_LAYER = {
    "backend-contract": ("後端", "task-backend.md"),
    "frontend-mock": ("前端", "task-frontend.md"),
    "integration": ("整合", "task-integration.md"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate api-plan contract references across e2e and task plans."
    )
    parser.add_argument(
        "--package", required=True, help="Path to specs/<NNN-plan-package> directory"
    )
    return parser.parse_args()


def read(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def e2e_blocks_by_layer(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    matches = list(re.finditer(r"(?m)^## (後端|前端|整合)\s*$", text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.end() : end]
    return result


def parse_contracts(text: str) -> list[dict[str, Any]]:
    match = JSON_BLOCK_RE.search(text)
    if not match:
        raise ValueError("api-plan.md 缺少可機械驗證契約 JSON")
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError(f"api-plan.md 契約 JSON 無法解析: {exc}") from exc
    contracts = payload.get("contracts")
    if not isinstance(contracts, list):
        raise ValueError("api-plan.md 契約 JSON 的 contracts 必須是陣列")
    return [item for item in contracts if isinstance(item, dict)]


def referenced_contract_ids(text: str) -> set[str]:
    ids: set[str] = set()
    active = False
    for line in text.splitlines():
        match = CONTRACT_LABEL_RE.match(line)
        if match:
            inline = match.group(1)
            ids.update(CONTRACT_ID_RE.findall(inline))
            active = not inline.strip()
            continue
        if active and re.match(r"^\s{2,}-\s+", line):
            ids.update(CONTRACT_ID_RE.findall(line))
            continue
        if line.strip():
            active = False
    return ids


def frontend_declares_api_usage(text: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^\s*-\s*(?:\*\*)?API(?:\*\*)?\s*$", line):
            continue
        values: list[str] = []
        for following in lines[index + 1 :]:
            match = re.match(r"^\s{2,}-\s+(.+)$", following)
            if match:
                values.append(match.group(1).strip())
                continue
            if following.strip():
                break
        return values != ["不適用"]
    return False


def scenario_blocks(
    text: str, *, e2e: bool
) -> dict[tuple[str | None, str], str]:
    heading = (
        re.compile(r"(?m)^#### Scenario:\s+((?:S-\d+-\d+)|(?:US-\d+))\b")
        if e2e
        else re.compile(r"(?m)^#### ((?:S-\d+-\d+)|(?:US-\d+))\s+")
    )
    matches = list(heading.finditer(text))
    outer_headings = list(re.finditer(r"(?m)^### (US-\d+)\s+", text))
    result: dict[tuple[str | None, str], str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        preceding = [item for item in outer_headings if item.start() < match.start()]
        outer_story = preceding[-1].group(1) if preceding else None
        if preceding and re.search(r"(?m)^## ", text[preceding[-1].end() : match.start()]):
            outer_story = None
        result[(outer_story, match.group(1))] = text[match.end() : end]
    return result


def scenario_contract_refs(
    blocks: dict[tuple[str | None, str], str]
) -> dict[tuple[str | None, str], set[str]]:
    return {
        context: referenced_contract_ids(block) for context, block in blocks.items()
    }


def story_for_scenario(scenario_id: str) -> str:
    if scenario_id.startswith("US-"):
        return scenario_id
    return f"US-{scenario_id.split('-')[1]}"


def refs_for_story(
    refs: dict[tuple[str | None, str], set[str]], user_story: str
) -> set[str]:
    result: set[str] = set()
    for (outer_story, scenario_id), contract_ids in refs.items():
        if outer_story == user_story and story_for_scenario(scenario_id) == user_story:
            result.update(contract_ids)
    return result


def validate(package: Path) -> list[str]:
    errors: list[str] = []
    api_path = package / "system-analyze" / "api-plan.md"
    if not api_path.is_file():
        return errors

    api_text = read(api_path)
    e2e_text = read(package / "e2e-test-plan.md")
    task_dir = package / "task-plan"
    task_texts = {
        source: read(task_dir / filename)
        for source, (_, filename) in SOURCE_TO_LAYER.items()
    }
    has_machine_contract = "## 可機械驗證契約" in api_text
    v2_detected = has_machine_contract or any(
        FLOW_V2_RE.search(text)
        for text in [api_text, e2e_text, *task_texts.values()]
    )
    if not v2_detected:
        return errors

    if not FLOW_V2_RE.search(api_text):
        errors.append("api-plan.md: 流程版本 2 package 缺少 `流程版本: 2`")
    if not has_machine_contract:
        return errors + ["api-plan.md: 流程版本 2 package 缺少可機械驗證契約"]
    if not FLOW_V2_RE.search(e2e_text):
        errors.append("e2e-test-plan.md: 流程版本 2 package 缺少 `流程版本: 2`")
    for source, text in task_texts.items():
        if not FLOW_V2_RE.search(text):
            _, filename = SOURCE_TO_LAYER[source]
            errors.append(f"{filename}: 流程版本 2 package 缺少 `流程版本: 2`")

    contracts = parse_contracts(api_text)
    contract_ids = {
        item.get("contract_id")
        for item in contracts
        if isinstance(item.get("contract_id"), str)
    }
    contract_story_by_id = {
        item["contract_id"]: item.get("user_story")
        for item in contracts
        if isinstance(item.get("contract_id"), str)
    }

    e2e_blocks = e2e_blocks_by_layer(e2e_text)
    e2e_scenario_blocks = {
        source: scenario_blocks(e2e_blocks.get(layer, ""), e2e=True)
        for source, (layer, _) in SOURCE_TO_LAYER.items()
    }
    e2e_scenario_refs = {
        source: scenario_contract_refs(blocks)
        for source, blocks in e2e_scenario_blocks.items()
    }
    task_scenario_refs = {
        source: scenario_contract_refs(scenario_blocks(text, e2e=False))
        for source, text in task_texts.items()
    }

    for source, refs in e2e_scenario_refs.items():
        layer, filename = SOURCE_TO_LAYER[source]
        task_refs = task_scenario_refs[source]
        contexts = set(refs) | set(task_refs)
        for context in contexts:
            outer_story, scenario_id = context
            e2e_ids = refs.get(context, set())
            task_ids = task_refs.get(context, set())
            if e2e_ids != task_ids:
                errors.append(
                    f"{filename}: {outer_story or '缺少外層 US'} {scenario_id} 契約案例 {sorted(task_ids)} "
                    f"不等於 e2e ## {layer} {sorted(e2e_ids)}"
                )
            block = e2e_scenario_blocks[source].get(context, "")
            uses_api = (
                source in {"backend-contract", "integration"}
                or (source == "frontend-mock" and frontend_declares_api_usage(block))
                or bool(API_USAGE_RE.search(block))
            )
            if uses_api and not e2e_ids:
                errors.append(
                    f"e2e ## {layer}: {outer_story or '缺少外層 US'} {scenario_id} 使用 API 但缺少契約案例"
                )

    for contract in contracts:
        contract_id = contract.get("contract_id")
        user_story = contract.get("user_story")
        sources = contract.get("required_evidence", [])
        if not isinstance(contract_id, str):
            continue

        if (
            isinstance(user_story, str)
            and not any(
                outer_story == user_story and scenario_id == user_story
                for outer_story, scenario_id in e2e_scenario_refs["integration"]
            )
        ):
            errors.append(f"{contract_id}: user_story {user_story} 未落到 e2e 整合區")

        if isinstance(sources, list):
            for source in sources:
                if not isinstance(user_story, str):
                    continue
                e2e_story_refs = refs_for_story(
                    e2e_scenario_refs.get(source, {}), user_story
                )
                task_story_refs = refs_for_story(
                    task_scenario_refs.get(source, {}), user_story
                )
                if source in e2e_scenario_refs and contract_id not in e2e_story_refs:
                    layer, _ = SOURCE_TO_LAYER[source]
                    errors.append(
                        f"{contract_id}: required_evidence {source} 未被 e2e ## {layer} 的 {user_story} 引用"
                    )
                if source in task_scenario_refs and contract_id not in task_story_refs:
                    _, filename = SOURCE_TO_LAYER[source]
                    errors.append(
                        f"{contract_id}: required_evidence {source} 未被 {filename} 的 {user_story} 引用"
                    )

    for source, scenario_refs in e2e_scenario_refs.items():
        layer, _ = SOURCE_TO_LAYER[source]
        for (outer_story, scenario_id), ids in scenario_refs.items():
            expected_story = story_for_scenario(scenario_id)
            if outer_story != expected_story:
                errors.append(
                    f"e2e ## {layer}: {scenario_id} 位於 {outer_story or '缺少外層 US'}，預期 {expected_story}"
                )
            for contract_id in sorted(ids & contract_ids):
                contract_story = contract_story_by_id.get(contract_id)
                if outer_story != contract_story:
                    errors.append(
                        f"e2e ## {layer}: {contract_id} 位於 {outer_story or '缺少外層 US'}，契約屬於 {contract_story}"
                    )

    for source, scenario_refs in task_scenario_refs.items():
        _, filename = SOURCE_TO_LAYER[source]
        for (outer_story, scenario_id), ids in scenario_refs.items():
            expected_story = story_for_scenario(scenario_id)
            if outer_story != expected_story:
                errors.append(
                    f"{filename}: {scenario_id} 位於 {outer_story or '缺少外層 US'}，預期 {expected_story}"
                )
            for contract_id in sorted(ids & contract_ids):
                contract_story = contract_story_by_id.get(contract_id)
                if outer_story != contract_story:
                    errors.append(
                        f"{filename}: {contract_id} 位於 {outer_story or '缺少外層 US'}，契約屬於 {contract_story}"
                    )

    for source, scenario_refs in e2e_scenario_refs.items():
        layer, _ = SOURCE_TO_LAYER[source]
        ids = set().union(*scenario_refs.values()) if scenario_refs else set()
        for contract_id in sorted(ids - contract_ids):
            errors.append(f"e2e ## {layer}: 引用不存在的契約案例 {contract_id}")

    for source, scenario_refs in task_scenario_refs.items():
        _, filename = SOURCE_TO_LAYER[source]
        ids = set().union(*scenario_refs.values()) if scenario_refs else set()
        for contract_id in sorted(ids - contract_ids):
            errors.append(f"{filename}: 引用不存在的契約案例 {contract_id}")

    return errors


def main() -> int:
    args = parse_args()
    package = Path(args.package)
    if not package.is_dir():
        print(f"ERROR: package directory not found: {package}", file=sys.stderr)
        return 2
    try:
        errors = validate(package)
    except (FileNotFoundError, ValueError) as exc:
        print(f"INVALID\n- {exc}")
        return 1

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
