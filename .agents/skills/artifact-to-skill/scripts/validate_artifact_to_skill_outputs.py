# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "rules/benchmark與目標artifact收斂判準.md",
    "rules/clarify與推進時機判準.md",
    "rules/artifact改寫與結構重組判準.md",
    "rules/template萃取與placeholder邊界判準.md",
    "rules/meta工程化與模組抽取判準.md",
    "templates/artifact-transformation-checklist.template.md",
    "templates/artifact-transformation-checklist.example.md",
    "templates/artifact-to-skill-plan.template.md",
    "templates/artifact-to-skill-plan.example.md",
    "scripts/validate_artifact_to_skill_outputs.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="檢查 artifact-to-skill 類型 skill 的必要檔案是否齊備。")
    parser.add_argument("--skill-dir", required=True, help="要檢查的 skill 目錄路徑")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir)

    if not skill_dir.exists():
        print(f"Skill directory not found: {skill_dir}", file=sys.stderr)
        return 2

    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        target = skill_dir / relative_path
        if not target.exists():
            errors.append(f"缺少必要檔案：{relative_path}")

    skill_path = skill_dir / "SKILL.md"
    if skill_path.exists():
        skill_text = skill_path.read_text(encoding="utf-8")
        expected_phrases = [
            "# Artifact to Skill",
            "benchmark",
            "target artifact",
            "template",
            "## Phase 1 -- 收斂 benchmark 與目標邊界",
            "## Phase 2 -- 先把 artifact 改到目標成品",
            "## Phase 3 -- 從 target artifact 萃取樣板",
            "## Phase 4 -- 反推高可靠生成方法",
            "## Phase 5 -- 落地並驗證新 skill",
        ]
        for phrase in expected_phrases:
            if phrase not in skill_text:
                errors.append(f"SKILL.md 缺少必要內容：{phrase}")

    if errors:
        print("ARTIFACT-TO-SKILL VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ARTIFACT-TO-SKILL VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
