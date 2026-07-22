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
TITLE_RE = re.compile(r"^# 技術可行性研究：.+$")
BRANCH_RE = re.compile(r"^\*\*功能分支\*\*:\s*`[^`]+`$")
CREATED_DATE_RE = re.compile(r"^\*\*建立日期\*\*:\s*\d{4}-\d{2}-\d{2}$")
STATUS_RE = re.compile(r"^\*\*狀態\*\*:\s*.+$")
DECISION_HEADING_RE = re.compile(r"^## 決策 (\d+):\s*.+$")

REQUIRED_MARKERS = (
    "- **Decision**:",
    "- **Rationale**:",
    "- **Alternatives considered**:",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structure of a technical-research Markdown artifact."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the technical-research.md file"
    )
    return parser.parse_args()


def find_decision_ranges(lines: list[str]) -> list[tuple[int, int, int]]:
    headings: list[tuple[int, int]] = []
    for idx, line in enumerate(lines):
        match = DECISION_HEADING_RE.match(line.strip())
        if match:
            headings.append((idx, int(match.group(1))))

    if not headings:
        return []

    stop_index = next(
        (idx for idx, line in enumerate(lines) if line.strip() == "## 假設"),
        len(lines),
    )

    ranges: list[tuple[int, int, int]] = []
    for position, (start, number) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else stop_index
        ranges.append((start, end, number))
    return ranges


def section_has_marker(section_lines: list[str], marker: str) -> bool:
    return any(line.strip().startswith(marker) for line in section_lines)


def has_child_bullets_after(section_lines: list[str], marker: str) -> bool:
    return bool(_child_bullets_after(section_lines, marker))


def _child_bullets_after(section_lines: list[str], marker: str) -> list[str]:
    for idx, line in enumerate(section_lines):
        if line.strip().startswith(marker):
            bullets: list[str] = []
            for following in section_lines[idx + 1 :]:
                stripped = following.strip()
                if not stripped:
                    continue
                if stripped.startswith("- **"):
                    break
                if stripped.startswith("- "):
                    bullets.append(stripped[2:].strip())
                    continue
                break
            return bullets
    return []


def _alternative_bullets(section_lines: list[str]) -> list[str]:
    return _child_bullets_after(section_lines, "- **Alternatives considered**:")


def _has_rejection_reason(bullet: str) -> bool:
    for separator in ("：", ":"):
        if separator not in bullet:
            continue
        left, right = bullet.split(separator, 1)
        if left.strip() and right.strip():
            return True
    return False


def validate_metadata(lines: list[str]) -> list[str]:
    errors: list[str] = []
    if not lines or not TITLE_RE.match(lines[0].strip()):
        errors.append("H1 must match `# 技術可行性研究：...`")

    head = [line.strip() for line in lines[:12]]
    if not any(BRANCH_RE.match(line) for line in head):
        errors.append("missing `**功能分支**: \\`...\\`` metadata line")
    if not any(CREATED_DATE_RE.match(line) for line in head):
        errors.append("missing `**建立日期**: YYYY-MM-DD` metadata line")
    if not any(STATUS_RE.match(line) for line in head):
        errors.append("missing `**狀態**: ...` metadata line")
    return errors


def validate_decisions(lines: list[str]) -> list[str]:
    errors: list[str] = []
    ranges = find_decision_ranges(lines)
    if not ranges:
        errors.append("must contain at least one `## 決策 N: ...` section")
        return errors

    expected = 1
    for start, end, number in ranges:
        label = f"決策 {number}"
        if number != expected:
            errors.append(
                f"{label}: decision numbers must be contiguous starting at 1 "
                f"(expected {expected})"
            )
        expected += 1

        section_lines = lines[start:end]
        for marker in REQUIRED_MARKERS:
            if not section_has_marker(section_lines, marker):
                errors.append(f"{label}: missing `{marker}`")

        if section_has_marker(section_lines, "- **Rationale**:"):
            if not has_child_bullets_after(section_lines, "- **Rationale**:"):
                # Allow inline rationale on the same line after the marker.
                rationale_line = next(
                    (
                        line.strip()
                        for line in section_lines
                        if line.strip().startswith("- **Rationale**:")
                    ),
                    "",
                )
                inline = rationale_line[len("- **Rationale**:") :].strip()
                if not inline:
                    errors.append(f"{label}: Rationale must include at least one bullet or inline text")

        if section_has_marker(section_lines, "- **Alternatives considered**:"):
            if not has_child_bullets_after(
                section_lines, "- **Alternatives considered**:"
            ):
                errors.append(
                    f"{label}: Alternatives considered must include at least one `- ` bullet"
                )
            else:
                for bullet in _alternative_bullets(section_lines):
                    if not _has_rejection_reason(bullet):
                        errors.append(
                            f"{label}: alternative `{bullet}` must use "
                            "`方案：不選原因` (non-empty reason after colon)"
                        )

        decision_line = next(
            (
                line.strip()
                for line in section_lines
                if line.strip().startswith("- **Decision**:")
            ),
            "",
        )
        inline_decision = decision_line[len("- **Decision**:") :].strip()
        if not inline_decision and not has_child_bullets_after(
            section_lines, "- **Decision**:"
        ):
            errors.append(f"{label}: Decision must include inline text or child bullets")

    return errors


def validate_assumption_section(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next(
        (idx for idx, line in enumerate(lines) if line.strip() == "## 假設"), None
    )
    if start is None:
        errors.append("missing `## 假設` section")
        return errors

    top_level = [idx for idx, line in enumerate(lines) if line.startswith("## ")]
    if start != max(top_level):
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


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    if PLACEHOLDER_RE.search(text):
        errors.append("output still contains unreplaced {{PLACEHOLDER}} tokens")

    errors.extend(validate_metadata(lines))
    errors.extend(validate_decisions(lines))
    errors.extend(validate_assumption_section(lines))
    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        print(f"Input not found: {path}", file=sys.stderr)
        return 2

    errors = validate(path)
    if errors:
        print(f"FAIL: {path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
