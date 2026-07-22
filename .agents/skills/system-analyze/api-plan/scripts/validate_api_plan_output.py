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
ENTITY_HEADING_RE = re.compile(r"^## 資料實體：.+$")
ENDPOINT_HEADING_RE = re.compile(r"^### Endpoint：`.+`$")
STATUS_HEADING_RE = re.compile(r"^##### .+$")
TITLE_RE = re.compile(r"^# API 計畫：.+$")
BRANCH_RE = re.compile(r"^\*\*功能分支\*\*:\s*`[^`]+`$")
CREATED_DATE_RE = re.compile(r"^\*\*建立日期\*\*:\s*\d{4}-\d{2}-\d{2}$")
STATUS_RE = re.compile(r"^\*\*狀態\*\*:\s*.+$")
JSON_FENCE_RE = re.compile(r"^```json\s*$")
BAD_ERROR_CODE_RE = re.compile(r'"code"\s*:\s*"Status Code"')

REQUIRED_TOP_LEVEL = [
    "## API Schema 描述",
    "## 共通錯誤格式",
    "## 追溯總表（快速 Review）",
    "## 假設",
]

ENDPOINT_REQUIRED_MARKERS = [
    "#### Parameters",
    "#### Request body",
    "#### Responses",
    "#### 測試規劃",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structure of an api-plan Markdown artifact."
    )
    parser.add_argument("--input", required=True, help="Path to the api-plan.md file")
    return parser.parse_args()


def find_ranges(lines: list[str], heading_re: re.Pattern[str]) -> list[tuple[int, int]]:
    headings = [idx for idx, line in enumerate(lines) if heading_re.match(line.strip())]
    if not headings:
        return []

    stop_markers = {
        "## 追溯總表（快速 Review）",
        "## 假設",
    }
    stop_index = next(
        (idx for idx, line in enumerate(lines) if line.strip() in stop_markers),
        len(lines),
    )

    ranges: list[tuple[int, int]] = []
    for position, start in enumerate(headings):
        if position + 1 < len(headings):
            end = headings[position + 1]
        else:
            end = stop_index
        ranges.append((start, end))
    return ranges


def section_has_marker(section_lines: list[str], marker: str) -> bool:
    return any(line.strip() == marker for line in section_lines)


def status_has_json_fence(section_lines: list[str], status_idx: int) -> bool:
    cursor = status_idx + 1
    while cursor < len(section_lines):
        stripped = section_lines[cursor].strip()
        if not stripped:
            cursor += 1
            continue
        if STATUS_HEADING_RE.match(stripped) or stripped.startswith("#### "):
            return False
        if JSON_FENCE_RE.match(stripped):
            return True
        cursor += 1
    return False


def validate_common_error_section(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next(
        (idx for idx, line in enumerate(lines) if line.strip() == "## 共通錯誤格式"),
        None,
    )
    if start is None:
        return errors

    end = next(
        (
            idx
            for idx, line in enumerate(lines[start + 1 :], start=start + 1)
            if line.startswith("## ")
        ),
        len(lines),
    )
    section = "\n".join(lines[start:end])
    if '"error"' not in section:
        errors.append("共通錯誤格式: missing `error` envelope example")
    if '"code"' not in section or '"message"' not in section or '"details"' not in section:
        errors.append("共通錯誤格式: envelope must include code / message / details")
    if BAD_ERROR_CODE_RE.search(section):
        errors.append("共通錯誤格式: `code` must not be the placeholder `Status Code`")
    if "```json" not in section:
        errors.append("共通錯誤格式: missing json code fence")
    return errors


def validate_assumption_section(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next((idx for idx, line in enumerate(lines) if line.strip() == "## 假設"), None)
    if start is None:
        return errors

    if start != max(idx for idx, line in enumerate(lines) if line.startswith("## ")):
        errors.append("## 假設 must be the last top-level section")

    bullet_count = 0
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("- "):
            bullet_count += 1

    if bullet_count < 1:
        errors.append("## 假設 must contain at least one `- ` bullet item")
    return errors


def validate_endpoint(section_lines: list[str], label: str) -> list[str]:
    errors: list[str] = []
    text = "\n".join(section_lines)

    for marker in ENDPOINT_REQUIRED_MARKERS:
        if not section_has_marker(section_lines, marker):
            errors.append(f"{label}: missing `{marker}`")

    if "| 對應 FR |" not in text and "對應 FR" not in text:
        errors.append(f"{label}: missing 對應 FR")

    status_indexes = [
        idx for idx, line in enumerate(section_lines) if STATUS_HEADING_RE.match(line.strip())
    ]
    if not status_indexes:
        errors.append(f"{label}: missing at least one `#####` response status heading")
    else:
        for idx in status_indexes:
            heading = section_lines[idx].strip()
            if not status_has_json_fence(section_lines, idx):
                errors.append(f"{label}: `{heading}` missing json code fence body")

    if "| 情境" not in text or "預期 Status" not in text:
        errors.append(f"{label}: 測試規劃 table must include 情境 and 預期 Status")

    return errors


def validate_entity(section_lines: list[str], label: str) -> list[str]:
    errors: list[str] = []
    text = "\n".join(section_lines)

    if "### 對應 User Story" not in text:
        errors.append(f"{label}: missing `### 對應 User Story`")
    if "### 實體形狀（欄位 + 範例資料）" not in text:
        errors.append(f"{label}: missing `### 實體形狀（欄位 + 範例資料）`")
    if "欄位說明（非型別定義）" not in text:
        errors.append(f"{label}: missing 欄位說明（非型別定義）")
    if "與資料實體 DDL Mapping" not in text:
        errors.append(f"{label}: missing DDL Mapping hint")

    endpoint_starts = [
        idx for idx, line in enumerate(section_lines) if ENDPOINT_HEADING_RE.match(line.strip())
    ]
    if not endpoint_starts:
        errors.append(f"{label}: missing at least one Endpoint")
        return errors

    for position, start in enumerate(endpoint_starts):
        end = (
            endpoint_starts[position + 1]
            if position + 1 < len(endpoint_starts)
            else len(section_lines)
        )
        endpoint_lines = section_lines[start:end]
        heading = section_lines[start].strip()
        errors.extend(validate_endpoint(endpoint_lines, f"{label} / {heading}"))

    return errors


def validate(path: Path) -> list[str]:
    if not path.exists():
        return [f"Input not found: {path}"]

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors: list[str] = []

    head = [line.strip() for line in lines[:10]]
    if not lines or not TITLE_RE.match(head[0] if head else ""):
        errors.append("missing top-level heading '# API 計畫：…'")
    if not any(BRANCH_RE.match(line) for line in head):
        errors.append("missing metadata line for 功能分支")
    if not any(CREATED_DATE_RE.match(line) for line in head):
        errors.append("missing metadata line for 建立日期")
    if not any(STATUS_RE.match(line) for line in head):
        errors.append("missing metadata line for 狀態")

    for header in REQUIRED_TOP_LEVEL:
        if not any(line.strip() == header for line in lines):
            errors.append(f"missing `{header}`")

    if PLACEHOLDER_RE.search(content):
        errors.append("output still contains unreplaced {{PLACEHOLDER}} tokens")

    errors.extend(validate_common_error_section(lines))
    errors.extend(validate_assumption_section(lines))

    entity_ranges = find_ranges(lines, ENTITY_HEADING_RE)
    if not entity_ranges:
        errors.append("missing at least one `## 資料實體：` section")
    else:
        for start, end in entity_ranges:
            label = lines[start].strip()
            errors.extend(validate_entity(lines[start:end], label))

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
