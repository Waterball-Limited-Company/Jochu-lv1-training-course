# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


STORY_HEADING_RE = re.compile(r"^### 使用者故事 \d+ - .+ \(優先級：P\d+\)$")
FR_RE = re.compile(r"^- \*\*FR-\d{3}\*\*:")
NUMBERED_ITEM_RE = re.compile(r"^\d+\. ")
BULLET_ITEM_RE = re.compile(r"^- ")

TOP_LEVEL_HEADERS = [
    "# 功能規格：",
    "# 原始需求",
    "## 使用者情境與測試 *(必填)*",
    "## 假設",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structure of a my-specify spec.md file."
    )
    parser.add_argument("--input", required=True, help="Path to the spec.md file")
    return parser.parse_args()


def find_story_ranges(lines: list[str]) -> list[tuple[int, int]]:
    headings = [idx for idx, line in enumerate(lines) if STORY_HEADING_RE.match(line.strip())]
    if not headings:
        return []

    assumption_index = next(
        (idx for idx, line in enumerate(lines) if line.strip() == "## 假設"),
        len(lines),
    )

    ranges: list[tuple[int, int]] = []
    for position, start in enumerate(headings):
        end = headings[position + 1] if position + 1 < len(headings) else assumption_index
        ranges.append((start, end))
    return ranges


def has_item_after_label(section_lines: list[str], label: str, item_regex: re.Pattern[str]) -> bool:
    for idx, line in enumerate(section_lines):
        if line.strip() != label:
            continue
        cursor = idx + 1
        while cursor < len(section_lines):
            stripped = section_lines[cursor].strip()
            if not stripped:
                cursor += 1
                continue
            if item_regex.match(stripped):
                return True
            if stripped.startswith("**") or stripped.startswith("### ") or stripped == "---":
                return False
            cursor += 1
    return False


def validate_story(section_lines: list[str], story_number: int) -> list[str]:
    errors: list[str] = []
    section_text = "\n".join(section_lines)

    required_markers = [
        "**為何是這個優先序**:",
        "**如何獨立驗證此使用者故事**:",
        "**邊界條件**:",
        "**驗收標準**:",
    ]
    for marker in required_markers:
        if marker not in section_text:
            errors.append(f"使用者故事 {story_number} 缺少區塊：{marker}")

    if not any(FR_RE.match(line.strip()) for line in section_lines):
        errors.append(f"使用者故事 {story_number} 缺少 FR 條目")

    if "**邊界條件**:" in section_text and not has_item_after_label(
        section_lines, "**邊界條件**:", BULLET_ITEM_RE
    ):
        errors.append(f"使用者故事 {story_number} 的邊界條件底下缺少條列項目")

    if "**驗收標準**:" in section_text and not has_item_after_label(
        section_lines, "**驗收標準**:", NUMBERED_ITEM_RE
    ):
        errors.append(f"使用者故事 {story_number} 的驗收標準底下缺少編號條目")

    return errors


def validate_spec(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.exists():
        return [f"Input not found: {path}"]

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    for header in TOP_LEVEL_HEADERS:
        if header not in content:
            errors.append(f"缺少必要章節：{header}")

    story_ranges = find_story_ranges(lines)
    if not story_ranges:
        errors.append("至少需要一個 `### 使用者故事 N - ...` 區塊")
        return errors

    fr_line_indexes = [idx for idx, line in enumerate(lines) if FR_RE.match(line.strip())]
    for fr_index in fr_line_indexes:
        if not any(start <= fr_index < end for start, end in story_ranges):
            errors.append(f"第 {fr_index + 1} 行的 FR 不在任何使用者故事區塊內")

    for story_number, (start, end) in enumerate(story_ranges, start=1):
        errors.extend(validate_story(lines[start:end], story_number))

    return errors


def main() -> int:
    args = parse_args()
    spec_path = Path(args.input)
    errors = validate_spec(spec_path)

    if errors:
        print("Spec validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    story_count = len(find_story_ranges(spec_path.read_text(encoding="utf-8").splitlines()))
    print(f"OK: validated {story_count} user story section(s) in {spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
