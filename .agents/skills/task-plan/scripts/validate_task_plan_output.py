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
RED_VERIFY_RE = re.compile(
    r"^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-red`?\s*—\s*"
    r"執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈\s*$",
    re.M,
)
SCENARIO_RED_ITEM_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-red`?\s*—\s*(S-\d+-\d+)\s+"
)
ANY_RED_ITEM_RE = re.compile(r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-red`?")
E2E_SCENARIO_RE = re.compile(r"^#### Scenario:\s+(S-\d+-\d+)\s+", re.M)
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")


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


def section_body(text: str, header: str) -> str:
    parts = re.split(r"(?m)^## ", text)
    for part in parts:
        if part.startswith(header.lstrip("#").strip() + "\n") or part.startswith(
            header.lstrip("#").strip() + "\r\n"
        ):
            return part
        # headers in REQUIRED are like "## 1. 規格閱讀" — after split marker removed
        title = header[3:] if header.startswith("## ") else header
        if part.startswith(title):
            return part
    return ""


def e2e_layer_scenarios(e2e_text: str, layer: str) -> list[str]:
    parts = re.split(r"(?m)^## ", e2e_text)
    body = ""
    for part in parts:
        if part.startswith(layer):
            body = part
            break
    return E2E_SCENARIO_RE.findall(body)


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

    # US blocks under section 3
    sec3 = ""
    if "## 3. User Story 實作計劃" in text:
        sec3 = text.split("## 3. User Story 實作計劃", 1)[1]
        if "## 4." in sec3:
            sec3 = sec3.split("## 4.", 1)[0]

    us_matches = list(US_RE.finditer(sec3))
    if not us_matches:
        errors.append(f"{path.name}: no User Story headings under section 3")

    for i, match in enumerate(us_matches):
        start = match.end()
        end = us_matches[i + 1].start() if i + 1 < len(us_matches) else len(sec3)
        block = sec3[start:end]
        for sub in ("#### AC / Edge", "#### Red", "#### Green", "#### Refactor"):
            if sub not in block:
                errors.append(f"{path.name}: {match.group(1)} missing {sub}")

        # Green nested plan
        if "#### Green" in block:
            green = block.split("#### Green", 1)[1]
            if "#### Refactor" in green:
                green = green.split("#### Refactor", 1)[0]
            if "/tdd-e2e-green" not in green:
                errors.append(f"{path.name}: {match.group(1)} Green missing /tdd-e2e-green")
            if "實作計畫：" not in green and "實作計畫:" not in green:
                errors.append(f"{path.name}: {match.group(1)} Green missing nested 實作計畫")

        # Red: Scenario items need nested plan; final item is fixed verify checkbox
        if "#### Red" in block:
            red = block.split("#### Red", 1)[1]
            if "#### Green" in red:
                red = red.split("#### Green", 1)[0]
            red_item_matches = list(ANY_RED_ITEM_RE.finditer(red))
            if not red_item_matches:
                errors.append(f"{path.name}: {match.group(1)} Red has no /tdd-e2e-red items")
            else:
                last = red_item_matches[-1]
                last_line = red[last.start() :].split("\n", 1)[0]
                if not RED_VERIFY_RE.match(last_line):
                    errors.append(
                        f"{path.name}: {match.group(1)} Red must end with fixed "
                        "US-level verify /tdd-e2e-red checkbox"
                    )
                else:
                    verify_body = red[last.end() :]
                    if (
                        "受測行為：" in verify_body
                        or "受測行為:" in verify_body
                        or "實作計畫：" in verify_body
                        or "實作計畫:" in verify_body
                    ):
                        errors.append(
                            f"{path.name}: {match.group(1)} Red verify item "
                            "must not nest 受測行為／實作計畫"
                        )
                for j, item in enumerate(red_item_matches[:-1]):
                    chunk_end = (
                        red_item_matches[j + 1].start()
                        if j + 1 < len(red_item_matches)
                        else len(red)
                    )
                    chunk = red[item.start() : chunk_end]
                    if not SCENARIO_RED_ITEM_RE.match(chunk):
                        errors.append(
                            f"{path.name}: {match.group(1)} non-final Red item "
                            "must be Scenario S-n-m"
                        )
                    if "受測行為：" not in chunk and "受測行為:" not in chunk:
                        errors.append(
                            f"{path.name}: {match.group(1)} a Scenario Red item "
                            "lacks nested 受測行為"
                        )

    actual_ids = SCENARIO_RED_ITEM_RE.findall(text)
    if actual_ids != expected_ids:
        errors.append(
            f"{path.name}: Red Scenario IDs {actual_ids} != e2e ## {layer} {expected_ids}"
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
