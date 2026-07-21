# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


RE_STORY_HEADING = re.compile(r"^### 使用者故事 (\d+) - .+（優先級：P(\d+)）$", re.MULTILINE)
RE_PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
RE_FR = re.compile(r"- \*\*US(\d+)-FR(\d+)\*\*：")
RE_SC = re.compile(r"- \*\*US(\d+)-SC(\d+)\*\*：")
RE_GR = re.compile(r"- \*\*GR-(\d+)\*\*：")
RE_PACKAGE_NAME = re.compile(r"^\d{3}-.+$")


@dataclass
class StoryBlock:
    number: int
    start: int
    end: int
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="檢查 my-specify 產出的 spec 結構是否有效。")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="要直接檢查的 spec Markdown 檔案路徑")
    group.add_argument("--package", help="要檢查的 NNN-plan-package；預設會對應到 specs/<package>/spec.md")
    parser.add_argument(
        "--workspace-root",
        default=".",
        help="workspace 根目錄；使用 --package 時會從此目錄推導 specs/<package>/spec.md",
    )
    return parser.parse_args()


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input not found: {path}")
    return path.read_text(encoding="utf-8")


def resolve_input_path(args: argparse.Namespace) -> Path:
    if args.input:
        return Path(args.input)

    assert args.package is not None
    if not RE_PACKAGE_NAME.match(args.package):
        raise ValueError(
            f"Invalid package name: {args.package}. Expected format like 001-photo-album-organizer"
        )

    workspace_root = Path(args.workspace_root)
    return workspace_root / "specs" / args.package / "spec.md"


def build_story_blocks(text: str) -> list[StoryBlock]:
    matches = list(RE_STORY_HEADING.finditer(text))
    blocks: list[StoryBlock] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append(
            StoryBlock(
                number=int(match.group(1)),
                start=start,
                end=end,
                text=text[start:end],
            )
        )
    return blocks


def ensure_contiguous(values: list[int], label: str, errors: list[str]) -> None:
    if not values:
        errors.append(f"{label} 不可為空。")
        return
    expected = list(range(1, len(values) + 1))
    if values != expected:
        errors.append(f"{label} 必須連續遞增，目前為 {values}，預期為 {expected}。")


def validate_story_structure(stories: list[StoryBlock], errors: list[str]) -> None:
    story_numbers = [story.number for story in stories]
    ensure_contiguous(story_numbers, "使用者故事編號", errors)

    required_headings = [
        "**為何列為此優先級**：",
        "**獨立驗證方式**：",
        "**功能需求**",
        "**成功標準**",
        "**驗收情境**",
        "**邊界情境**",
    ]

    for story in stories:
        for heading in required_headings:
            if heading not in story.text:
                errors.append(f"使用者故事 {story.number} 缺少區塊：{heading}")

        fr_matches = [(int(a), int(b)) for a, b in RE_FR.findall(story.text)]
        sc_matches = [(int(a), int(b)) for a, b in RE_SC.findall(story.text)]

        if not fr_matches:
            errors.append(f"使用者故事 {story.number} 至少需要一條 FR。")
        if not sc_matches:
            errors.append(f"使用者故事 {story.number} 至少需要一條 SC。")

        fr_story_numbers = sorted({a for a, _ in fr_matches})
        sc_story_numbers = sorted({a for a, _ in sc_matches})
        if fr_story_numbers and fr_story_numbers != [story.number]:
            errors.append(f"使用者故事 {story.number} 內的 FR 編號歸屬錯誤：{fr_story_numbers}")
        if sc_story_numbers and sc_story_numbers != [story.number]:
            errors.append(f"使用者故事 {story.number} 內的 SC 編號歸屬錯誤：{sc_story_numbers}")

        fr_numbers = [b for _, b in fr_matches]
        sc_numbers = [b for _, b in sc_matches]
        if fr_numbers:
            ensure_contiguous(fr_numbers, f"使用者故事 {story.number} 的 FR 編號", errors)
        if sc_numbers:
            ensure_contiguous(sc_numbers, f"使用者故事 {story.number} 的 SC 編號", errors)

        if "**假設**" not in story.text or "**當**" not in story.text or "**則**" not in story.text:
            errors.append(f"使用者故事 {story.number} 缺少完整的假設 / 當 / 則驗收情境。")


def validate_global_rules(text: str, errors: list[str]) -> None:
    if "## 共通規則與全域約束" in text:
        gr_numbers = [int(num) for num in RE_GR.findall(text)]
        if not gr_numbers:
            errors.append("存在全域約束章節，但沒有 GR 條目。")
        else:
            ensure_contiguous(gr_numbers, "GR 編號", errors)
        if "### 全域邊界情境" not in text:
            errors.append("存在全域約束章節時，應包含全域邊界情境。")


def validate_common_sections(text: str, errors: list[str]) -> None:
    if not text.startswith("# 功能規格："):
        errors.append("文件必須以 `# 功能規格：...` 開頭。")
    if "## 使用者故事與驗證 *(必填)*" not in text:
        errors.append("缺少 `## 使用者故事與驗證 *(必填)*` 章節。")

    placeholders = RE_PLACEHOLDER.findall(text)
    if placeholders:
        errors.append(f"文件仍殘留 placeholder：{', '.join(sorted(set(placeholders)))}")


def main() -> int:
    args = parse_args()
    try:
        input_path = resolve_input_path(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        text = load_text(input_path)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    errors: list[str] = []
    validate_common_sections(text, errors)
    stories = build_story_blocks(text)
    if not stories:
        errors.append("至少需要一個 `### 使用者故事 N - ...` 區塊。")
    else:
        validate_story_structure(stories, errors)
    validate_global_rules(text, errors)

    if errors:
        print("SPEC VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("SPEC VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
