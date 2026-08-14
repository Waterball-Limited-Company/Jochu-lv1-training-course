# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
TITLE_RE = re.compile(r"^# 端對端測試計畫：.+$")
PROOF_BLOCK_RE = re.compile(r"^## (後端|前端|整合)\s*$")
US_HEADING_RE = re.compile(r"^### US-\d+\s+.+\（優先級：P\d+\）\s*$")
SCENARIO_HEADING_RE = re.compile(r"^#### Scenario:\s+(S-\d+-\d+|US-\d+)\s+.+$")
BLOCK_TAG_IN_SCENARIO_RE = re.compile(
    r"^#### Scenario:\s+(?:S-\d+-\d+|US-\d+)\s*（(?:後端|前端|整合)）"
)
GHERKIN_FENCE_RE = re.compile(r"^```gherkin\s*$")
API_PATH_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s+/|`/[a-zA-Z0-9_{}/-]+`")
MAPPING_LABEL_RE = re.compile(r"^\s*-\s*\*\*(.+?)\*\*\s*$")

REQUIRED_METADATA = [
    re.compile(r"^\*\*功能分支\*\*:\s*.+$"),
    re.compile(r"^\*\*建立日期\*\*:\s*.+$"),
    re.compile(r"^\*\*狀態\*\*:\s*.+$"),
]

REQUIRED_SECTIONS = [
    "## 後端",
    "## 前端",
    "## 整合",
    "## 未產出 Scenario 的邊界（blocked）",
    "## 測試摘要總表",
    "## 假設",
]

REQUIRED_MAPPING_BY_BLOCK = {
    "後端": (
        "US",
        "AC / Edge",
        "FR",
        "受測部位",
        "前置資料",
        "觀測通道",
        "必須維持不變",
        "本則不驗證",
        "預期 TDD Red",
        "API",
    ),
    "前端": (
        "US",
        "AC / Edge",
        "FR",
        "受測部位",
        "前置資料",
        "觀測通道",
        "狀態／畫面文案",
        "必須維持不變",
        "本則不驗證",
        "預期 TDD Red",
        "UI",
    ),
    "整合": (
        "US",
        "受測部位",
        "前置資料",
        "觀測通道",
        "必須維持不變",
        "本則不驗證",
        "前端",
        "後端",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structure of an e2e-test-plan Markdown artifact."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the e2e-test-plan.md file",
    )
    return parser.parse_args()


def extract_gherkin_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    idx = 0
    while idx < len(lines):
        if GHERKIN_FENCE_RE.match(lines[idx].strip()):
            idx += 1
            body: list[str] = []
            while idx < len(lines) and lines[idx].strip() != "```":
                body.append(lines[idx])
                idx += 1
            blocks.append(body)
        idx += 1
    return blocks


def validate_gherkin_block(body: list[str], label: str) -> list[str]:
    errors: list[str] = []
    steps = [line.rstrip() for line in body if line.strip()]
    when_indexes = [
        i for i, line in enumerate(steps) if re.match(r"^\s*When\b", line)
    ]
    if len(when_indexes) != 1:
        errors.append(f"{label}: gherkin must contain exactly one `When` step")
        return errors

    when_idx = when_indexes[0]
    then_indexes = [
        i for i, line in enumerate(steps) if re.match(r"^\s*Then\b", line)
    ]
    if not then_indexes:
        errors.append(f"{label}: gherkin missing `Then`")
        return errors

    first_then = then_indexes[0]
    for i in range(when_idx + 1, first_then):
        if re.match(r"^\s*(And|But)\b", steps[i]):
            errors.append(
                f"{label}: `And`/`But` must not appear between `When` and `Then`"
            )
            break

    for line in steps:
        if re.match(r"^\s*Or\b", line):
            errors.append(f"{label}: non-standard step keyword `Or` is not allowed")
        if API_PATH_RE.search(line):
            errors.append(f"{label}: gherkin must stay domain-language (no API path)")

    return errors


def current_proof_block(lines: list[str], index: int) -> str | None:
    for i in range(index, -1, -1):
        match = PROOF_BLOCK_RE.match(lines[i].strip())
        if match:
            return match.group(1)
        if lines[i].startswith("## ") and not PROOF_BLOCK_RE.match(lines[i].strip()):
            # left proof blocks (e.g. blocked / summary)
            if lines[i].strip() in {
                "## 未產出 Scenario 的邊界（blocked）",
                "## 測試摘要總表",
                "## 假設",
            }:
                return None
    return None


def validate_scenarios(lines: list[str]) -> list[str]:
    errors: list[str] = []
    scenario_indexes = [
        idx
        for idx, line in enumerate(lines)
        if SCENARIO_HEADING_RE.match(line.strip())
        or BLOCK_TAG_IN_SCENARIO_RE.match(line.strip())
    ]
    if not scenario_indexes:
        errors.append("missing at least one `#### Scenario: S-x-y …` or `US-n …` heading")
        return errors

    for position, start in enumerate(scenario_indexes):
        end = (
            scenario_indexes[position + 1]
            if position + 1 < len(scenario_indexes)
            else len(lines)
        )
        section = lines[start:end]
        heading = lines[start].strip()

        if BLOCK_TAG_IN_SCENARIO_RE.match(heading):
            errors.append(
                f"{heading}: scenario title must not include （後端／前端／整合）"
            )
        elif not SCENARIO_HEADING_RE.match(heading):
            errors.append(f"invalid scenario heading → `{heading}`")

        block = current_proof_block(lines, start)
        if block is None:
            errors.append(f"{heading}: scenario must sit under ## 後端／前端／整合")
            continue

        if block in {"後端", "前端"} and not heading.startswith("#### Scenario: S-"):
            errors.append(
                f"{heading}: under ## {block}, heading must use `S-x-y`"
            )
        if block == "整合" and not heading.startswith("#### Scenario: US-"):
            errors.append(
                f"{heading}: under ## 整合, heading must use `US-n`"
            )

        if not any(line.strip() == "**對應欄位**:" for line in section):
            errors.append(f"{heading}: missing `**對應欄位**:`")
            continue

        labels = [
            match.group(1)
            for line in section
            if (match := MAPPING_LABEL_RE.match(line))
        ]
        required = REQUIRED_MAPPING_BY_BLOCK[block]
        for label in required:
            if label not in labels:
                errors.append(
                    f"{heading}: under ## {block}, mapping missing `**{label}**`"
                )
        if block == "整合" and "預期 TDD Red" in labels:
            errors.append(
                f"{heading}: under ## 整合, mapping must not include `**預期 TDD Red**`"
            )

    return errors


def validate_us_headings(lines: list[str]) -> list[str]:
    errors: list[str] = []
    us_headings = [line for line in lines if line.startswith("### US-")]
    if not us_headings:
        errors.append("missing at least one `### US-…` heading under proof blocks")
        return errors
    for line in us_headings:
        if not US_HEADING_RE.match(line.strip()):
            errors.append(f"US heading must include 優先級：Pn → `{line.strip()}`")
    return errors


def validate_summary_table(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next(
        (idx for idx, line in enumerate(lines) if line.strip() == "## 測試摘要總表"),
        None,
    )
    if start is None:
        return errors

    if any(line.strip() == "## 元素覆蓋總表" for line in lines):
        errors.append("must not include obsolete `## 元素覆蓋總表`")

    header_idx = next(
        (
            idx
            for idx in range(start + 1, min(start + 30, len(lines)))
            if line_has_summary_header(lines[idx])
        ),
        None,
    )
    if header_idx is None:
        errors.append(
            "測試摘要總表: missing header "
            "`| User Story | AC / Edge | Scenario | 後端 | 前端 | 整合 |`"
        )
        return errors

    data_rows = 0
    for line in lines[header_idx + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if data_rows and stripped and not stripped.startswith("|"):
            break
        if (
            stripped.startswith("|")
            and not stripped.startswith("| ---")
            and "User Story" not in stripped
        ):
            data_rows += 1
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) != 6:
                errors.append(
                    f"測試摘要總表: row must have 6 columns → `{stripped}`"
                )
                continue
            for mark in cells[3:6]:
                if mark not in {"✓", "—"}:
                    errors.append(
                        f"測試摘要總表: 落點欄只能是 ✓ 或 — → `{stripped}`"
                    )
                    break
            if cells[5] != "—":
                errors.append(
                    f"測試摘要總表: 切片表整合欄必須是 — → `{stripped}`"
                )
    if data_rows < 1:
        errors.append("測試摘要總表: must contain at least one data row")

    acceptance_header_idx = next(
        (
            idx
            for idx in range(header_idx + 1, len(lines))
            if line_has_acceptance_header(lines[idx])
        ),
        None,
    )
    if acceptance_header_idx is None:
        errors.append(
            "測試摘要總表: missing 驗收表 header "
            "`| User Story | Scenario | 整合 |`"
        )
        return errors

    acceptance_rows = 0
    acceptance_us_ids: set[str] = set()
    for line in lines[acceptance_header_idx + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if acceptance_rows and stripped and not stripped.startswith("|"):
            break
        if (
            stripped.startswith("|")
            and not stripped.startswith("| ---")
            and "User Story" not in stripped
        ):
            acceptance_rows += 1
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) != 3:
                errors.append(f"驗收表: row must have 3 columns → `{stripped}`")
                continue
            us_match = re.match(r"^(US-\d+)\b", cells[0])
            scenario_match = re.match(r"^(US-\d+)\b", cells[1])
            if not us_match or not scenario_match:
                errors.append(
                    f"驗收表: User Story 與 Scenario 必須是 US-n → `{stripped}`"
                )
            else:
                acceptance_us_ids.add(us_match.group(1))
            if cells[2] not in {"✓", "—"}:
                errors.append(f"驗收表: 整合欄只能是 ✓ 或 — → `{stripped}`")
    if acceptance_rows < 1:
        errors.append("驗收表: must contain at least one data row")

    integration_ids = collect_integration_us_ids(lines)
    missing = [us_id for us_id in integration_ids if us_id not in acceptance_us_ids]
    if missing:
        errors.append(
            "驗收表: missing US-n rows for ## 整合 → " + ", ".join(missing)
        )
    return errors


def line_has_summary_header(line: str) -> bool:
    stripped = line.strip()
    return (
        stripped.startswith("|")
        and "User Story" in stripped
        and "AC / Edge" in stripped
        and "Scenario" in stripped
        and "後端" in stripped
        and "前端" in stripped
        and "整合" in stripped
    )


def line_has_acceptance_header(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    cells = [c.strip() for c in stripped.strip("|").split("|")]
    return cells == ["User Story", "Scenario", "整合"]


def collect_integration_us_ids(lines: list[str]) -> list[str]:
    ids: list[str] = []
    in_integration = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## 整合":
            in_integration = True
            continue
        if in_integration and stripped.startswith("## "):
            break
        match = re.match(r"^### (US-\d+)\s", stripped)
        if in_integration and match:
            ids.append(match.group(1))
    return ids


def validate_assumption_section(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next((idx for idx, line in enumerate(lines) if line.strip() == "## 假設"), None)
    if start is None:
        return ["missing `## 假設`"]

    top_level = [idx for idx, line in enumerate(lines) if line.startswith("## ")]
    if start != max(top_level):
        errors.append("## 假設 must be the last top-level section")

    bullet_count = sum(
        1 for line in lines[start + 1 :] if line.strip().startswith("- ")
    )
    if bullet_count < 1:
        errors.append("## 假設 must contain at least one `- ` bullet item")
    return errors


def validate_proof_block_order(lines: list[str]) -> list[str]:
    errors: list[str] = []
    positions = {
        name: next(
            (idx for idx, line in enumerate(lines) if line.strip() == f"## {name}"),
            None,
        )
        for name in ("後端", "前端", "整合")
    }
    if any(pos is None for pos in positions.values()):
        return errors
    if not (positions["後端"] < positions["前端"] < positions["整合"]):
        errors.append("proof blocks must appear in order: ## 後端 → ## 前端 → ## 整合")
    return errors


def validate(path: Path) -> list[str]:
    if not path.exists():
        return [f"Input not found: {path}"]

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors: list[str] = []

    if not lines or not TITLE_RE.match(lines[0].strip()):
        errors.append("missing top-level heading `# 端對端測試計畫：…`")

    for pattern in REQUIRED_METADATA:
        if not any(pattern.match(line.strip()) for line in lines[:12]):
            errors.append(f"missing metadata matching {pattern.pattern}")

    for section in REQUIRED_SECTIONS:
        if not any(line.strip() == section for line in lines):
            errors.append(f"missing `{section}`")

    if PLACEHOLDER_RE.search(content):
        errors.append("output still contains unreplaced {{PLACEHOLDER}} tokens")

    errors.extend(validate_proof_block_order(lines))
    errors.extend(validate_us_headings(lines))
    errors.extend(validate_scenarios(lines))
    errors.extend(validate_summary_table(lines))
    errors.extend(validate_assumption_section(lines))

    blocks = extract_gherkin_blocks(lines)
    if not blocks:
        errors.append("missing at least one ```gherkin fence")
    else:
        for i, body in enumerate(blocks, start=1):
            errors.extend(validate_gherkin_block(body, f"gherkin#{i}"))

    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    errors = validate(path)

    if errors:
        print(f"INVALID: {path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"VALID: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
