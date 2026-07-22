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
SCENARIO_HEADING_RE = re.compile(r"^### Scenario:\s+(S-\d+-\d+)\s+.+$")
US_HEADING_RE = re.compile(r"^## US-\d+\s+.+\（優先級：P\d+\）\s*$")
GHERKIN_FENCE_RE = re.compile(r"^```gherkin\s*$")
API_PATH_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s+/|`/[a-zA-Z0-9_{}/-]+`")
MAPPING_CATEGORY_RE = re.compile(
    r"^\s*-\s*\*\*(User Story|驗收標準|邊界條件|FR)\*\*:"
)

REQUIRED_METADATA = [
    re.compile(r"^\*\*功能分支\*\*:\s*.+$"),
    re.compile(r"^\*\*建立日期\*\*:\s*.+$"),
    re.compile(r"^\*\*狀態\*\*:\s*.+$"),
]

REQUIRED_SECTIONS = [
    "## 元素覆蓋總表",
    "## 假設",
]


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


def validate_scenarios(lines: list[str]) -> list[str]:
    errors: list[str] = []
    scenario_indexes = [
        idx for idx, line in enumerate(lines) if SCENARIO_HEADING_RE.match(line.strip())
    ]
    if not scenario_indexes:
        errors.append("missing at least one `### Scenario: S-x-y …` heading")
        return errors

    for position, start in enumerate(scenario_indexes):
        end = (
            scenario_indexes[position + 1]
            if position + 1 < len(scenario_indexes)
            else len(lines)
        )
        section = lines[start:end]
        heading = lines[start].strip()
        if not any(line.strip() == "**對應欄位**:" for line in section):
            errors.append(f"{heading}: missing `**對應欄位**:`")
        for line in section:
            if MAPPING_CATEGORY_RE.match(line):
                errors.append(
                    f"{heading}: mapping must not use category labels "
                    "(User Story / 驗收標準 / 邊界條件 / FR)"
                )
                break

    return errors


def validate_coverage_table(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next(
        (idx for idx, line in enumerate(lines) if line.strip() == "## 元素覆蓋總表"),
        None,
    )
    if start is None:
        return errors

    header_idx = next(
        (
            idx
            for idx in range(start + 1, min(start + 20, len(lines)))
            if "| ID |" in lines[idx] and "描述" in lines[idx] and "Scenario" in lines[idx]
        ),
        None,
    )
    if header_idx is None:
        errors.append("元素覆蓋總表: missing `| ID | 描述 | Scenario |` header")
        return errors

    if "類型" in lines[header_idx]:
        errors.append("元素覆蓋總表: must not include `類型` column")

    data_rows = 0
    for line in lines[header_idx + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("|") and not stripped.startswith("| ---") and "ID" not in stripped:
            data_rows += 1
    if data_rows < 1:
        errors.append("元素覆蓋總表: must contain at least one data row")
    return errors


def validate_assumption_section(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next((idx for idx, line in enumerate(lines) if line.strip() == "## 假設"), None)
    if start is None:
        return ["missing `## 假設`"]

    if start != max(idx for idx, line in enumerate(lines) if line.startswith("## ")):
        errors.append("## 假設 must be the last top-level section")

    bullet_count = sum(
        1
        for line in lines[start + 1 :]
        if line.strip().startswith("- ")
    )
    if bullet_count < 1:
        errors.append("## 假設 must contain at least one `- ` bullet item")
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
        if not any(pattern.match(line.strip()) for line in lines[:8]):
            errors.append(f"missing metadata matching {pattern.pattern}")

    for section in REQUIRED_SECTIONS:
        if not any(line.strip() == section for line in lines):
            errors.append(f"missing `{section}`")

    if PLACEHOLDER_RE.search(content):
        errors.append("output still contains unreplaced {{PLACEHOLDER}} tokens")

    us_headings = [line for line in lines if line.startswith("## US-")]
    if not us_headings:
        errors.append("missing at least one `## US-…` section")
    else:
        for line in us_headings:
            if not US_HEADING_RE.match(line.strip()):
                errors.append(f"US heading must include 優先級：Pn → `{line.strip()}`")

    errors.extend(validate_scenarios(lines))
    errors.extend(validate_coverage_table(lines))
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
