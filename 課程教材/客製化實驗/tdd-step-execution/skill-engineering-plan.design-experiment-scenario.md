# Skill 工程編排提案

## 任務資訊

- 處理路徑: `optimize`
- 改動範圍: `step rewrite`
- 目標 Skills: `design-experiment-scenario`

## 控制平面重建

- 維持五 phase；Phase 4 拆成可執行 steps，Artifact／Skill 驗證方式分岔寫死。
- Skill 路徑：只交付「請使用者呼叫 `/skill-engineering`」Prompt，禁止三跑直接改 skill。
- Artifact 路徑：三跑 + consistency（含 example 雙檔掛回）。

## 步驟決策

- Phase 1～3：keep-inline（已大致正確）。
- Phase 4：rewrite — 拆步；Artifact READ consistency 雙檔；Skill 停等使用者下指令。
- Phase 5：rewrite 對齊句（Skill 不假設定稿 Artifact／不代改 skill）。
- `實驗路徑分岔判準`：keep（已正確）+ 必要薄修。
- `人工Review閘門判準`：rewrite Phase 4 停等文案。
- `consistency-report`：rewrite 為 **僅 Artifact 路徑**；刪 Skill 三跑語意。
- `prompt-writing-guide`：rewrite Review 停等依路徑分岔。
- `skill-eng-validation`：薄修 Skill 路徑說明。

## 檔案動作

### 新增 / 更新

- Update `SKILL.md` Phase 4～5
- Update `rules/人工Review閘門判準.md`
- Update `templates/consistency-report.md` + `.example.md`
- Update `templates/prompt-writing-guide.md` + `.example.md`（Review 句）
- Update `templates/skill-eng-validation.md`（若需）

### 刪除

- consistency 中 Skill 路徑當三跑必填的欄位語意

## 驗證方式

- `uv run …/analyze_skill_references.py --skill .agents/skills/design-experiment-scenario`（無 missing／無 orphan）
- 重讀：Skill 路徑不得指示直接改 skill

## 實作閘門

- 使用者已回「繼續」→ 依本 plan 落地。
