# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## 1. 規格閱讀",
    "## 2. 環境建立",
    "## 3. User Story 實作計劃",
    "## 4. 進度總覽",
    "## 5. 假設",
]

LAYER_FILES = {
    "後端": "task-backend.md",
    "前端": "task-frontend.md",
    "整合": "task-integration.md",
}

US_RE = re.compile(r"^### (US-\d+)\s+.+\（優先級：P\d+\）\s*$", re.M)
US_LEVEL_RGB_HEADING_RE = re.compile(r"(?m)^#### (Red|Green|Refactor)\s*$")
SCENARIO_HEADING_RE = re.compile(r"(?m)^#### ((?:S-\d+-\d+)|(?:US-\d+))\s+.+$")
E2E_SCENARIO_RE = re.compile(r"^#### Scenario:\s+((?:S-\d+-\d+)|(?:US-\d+))\s+", re.M)
RED_ITEM_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-red`?\s*—\s*((?:S-\d+-\d+)|(?:US-\d+))\s+"
)
GREEN_ITEM_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-green`?\s*—\s*((?:S-\d+-\d+)|(?:US-\d+))"
)
REFACTOR_ITEM_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-refactor`?\s*—\s*((?:S-\d+-\d+)|(?:US-\d+))"
)
CHECKBOX_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/(tdd-e2e-(?:red|green|refactor))`?"
)
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
FORBIDDEN_VERIFY_RE = re.compile(
    r"確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈"
)
FORBIDDEN_US_GREEN_RE = re.compile(r"讓本 US 既有 Red 全綠")

RED_FIELDS = ("前置", "打", "看", "期望")
SLICE_RED_FIELDS = RED_FIELDS + ("還沒做時",)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate task-plan artifacts for a specs package."
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Path to specs/<NNN-plan-package> directory",
    )
    return parser.parse_args()


def e2e_layer_scenarios(e2e_text: str, layer: str) -> list[str]:
    parts = re.split(r"(?m)^## ", e2e_text)
    body = ""
    for part in parts:
        if part.startswith(layer):
            body = part
            break
    return E2E_SCENARIO_RE.findall(body)


def section_three(text: str) -> str:
    if "## 3. User Story 實作計劃" not in text:
        return ""
    sec3 = text.split("## 3. User Story 實作計劃", 1)[1]
    if "## 4." in sec3:
        sec3 = sec3.split("## 4.", 1)[0]
    return sec3


def has_label(chunk: str, label: str) -> bool:
    return f"{label}：" in chunk or f"{label}:" in chunk


def validate_scenario_block(
    path_name: str,
    us_id: str,
    heading_id: str,
    block: str,
    layer: str,
) -> list[str]:
    errors: list[str] = []
    prefix = f"{path_name}: {us_id} {heading_id}"

    red_ids = RED_ITEM_RE.findall(block)
    green_ids = GREEN_ITEM_RE.findall(block)
    refactor_ids = REFACTOR_ITEM_RE.findall(block)

    if red_ids != [heading_id]:
        errors.append(f"{prefix} Red ID {red_ids} != heading {heading_id}")
    if green_ids != [heading_id]:
        errors.append(f"{prefix} Green ID {green_ids} != heading {heading_id}")
    if refactor_ids != [heading_id]:
        errors.append(f"{prefix} Refactor ID {refactor_ids} != heading {heading_id}")

    commands = CHECKBOX_RE.findall(block)
    if commands != ["tdd-e2e-red", "tdd-e2e-green", "tdd-e2e-refactor"]:
        errors.append(
            f"{prefix} checkbox order {commands} != red → green → refactor"
        )

    if not has_label(block, "受測行為"):
        errors.append(f"{prefix} missing nested 受測行為")
    if not has_label(block, "實作計畫"):
        errors.append(f"{prefix} missing nested 實作計畫")
    if not has_label(block, "整理範圍"):
        errors.append(f"{prefix} missing nested 整理範圍")

    required_fields = SLICE_RED_FIELDS if layer in {"後端", "前端"} else RED_FIELDS
    for field in required_fields:
        if not has_label(block, field):
            errors.append(f"{prefix} 受測行為 missing {field}")

    if "本則不驗證" not in block:
        errors.append(f"{prefix} Green missing 本則不驗證")

    return errors


def validate_task_file(path: Path, layer: str, expected_ids: list[str]) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing file: {path}"]

    text = path.read_text(encoding="utf-8")
    if PLACEHOLDER_RE.search(text):
        errors.append(f"{path.name}: unresolved placeholders remain")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: missing section {section}")

    if "## 2. Setup" in text or re.search(r"(?m)^## 2\.\s*Setup\b", text):
        errors.append(f"{path.name}: section 2 must be 環境建立, not Setup")

    if "完成定義" in text:
        errors.append(f"{path.name}: must not contain 完成定義")

    if FORBIDDEN_VERIFY_RE.search(text):
        errors.append(f"{path.name}: must not contain US-level Red verify item")

    if FORBIDDEN_US_GREEN_RE.search(text):
        errors.append(f"{path.name}: must not contain US-level Green 讓本 US 既有 Red 全綠")

    sec3 = section_three(text)
    us_matches = list(US_RE.finditer(sec3))
    if not us_matches:
        errors.append(f"{path.name}: no User Story headings under section 3")

    actual_ids: list[str] = []
    for i, match in enumerate(us_matches):
        start = match.end()
        end = us_matches[i + 1].start() if i + 1 < len(us_matches) else len(sec3)
        block = sec3[start:end]
        us_id = match.group(1)

        if "#### AC / Edge" not in block:
            errors.append(f"{path.name}: {us_id} missing #### AC / Edge")

        rgb_headings = US_LEVEL_RGB_HEADING_RE.findall(block)
        if rgb_headings:
            errors.append(
                f"{path.name}: {us_id} must not use US-level #### {', '.join(rgb_headings)}"
            )

        scenario_matches = list(SCENARIO_HEADING_RE.finditer(block))
        if not scenario_matches:
            errors.append(f"{path.name}: {us_id} has no Scenario heading")

        for j, scenario in enumerate(scenario_matches):
            heading_id = scenario.group(1)
            if layer == "整合":
                if not re.fullmatch(r"US-\d+", heading_id):
                    errors.append(
                        f"{path.name}: {us_id} integration heading {heading_id} must be US-n"
                    )
            elif not re.fullmatch(r"S-\d+-\d+", heading_id):
                errors.append(
                    f"{path.name}: {us_id} {layer} heading {heading_id} must be S-n-m"
                )

            chunk_end = (
                scenario_matches[j + 1].start()
                if j + 1 < len(scenario_matches)
                else len(block)
            )
            chunk = block[scenario.start() : chunk_end]
            actual_ids.append(heading_id)
            errors.extend(
                validate_scenario_block(path.name, us_id, heading_id, chunk, layer)
            )

    if actual_ids != expected_ids:
        errors.append(
            f"{path.name}: Scenario IDs {actual_ids} != e2e ## {layer} {expected_ids}"
        )

    return errors


def main() -> int:
    args = parse_args()
    package = Path(args.package)
    if not package.is_dir():
        print(f"ERROR: package directory not found: {package}", file=sys.stderr)
        return 2

    e2e_path = package / "e2e-test-plan.md"
    if not e2e_path.is_file():
        print(f"ERROR: missing {e2e_path}", file=sys.stderr)
        return 2

    e2e_text = e2e_path.read_text(encoding="utf-8")
    task_dir = package / "task-plan"
    errors: list[str] = []

    for layer, filename in LAYER_FILES.items():
        expected = e2e_layer_scenarios(e2e_text, layer)
        errors.extend(validate_task_file(task_dir / filename, layer, expected))

    if errors:
        print("INVALID")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
