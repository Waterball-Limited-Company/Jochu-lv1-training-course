# Skill 工程編排提案

## 任務資訊

- 處理路徑: `optimize`
- 改動範圍: `skill rewrite`
- 目標 Skills: `design-experiment-scenario`

## 控制平面重建

- 維持 Phase 1～2；自 Phase 3 起分岔 **Artifact lane** 與 **Skill lane**。
- Phase 3：先判定有無 Artifact → 產出對應 Prompt 規範（改 Artifact vs 描述 `/skill-engineering` 改 Skill）。
- Phase 4：同一 Prompt 三跑驗證可行性（產物為 Artifact 檔或 skill 改動暫定檔）。
- Phase 5：Artifact lane 接定稿進 Skill Eng；Skill lane 以三跑為可行性本體，再寫驗證紀錄（可補正式 skill-engineering 閘門結果），不再假設必有定稿 Artifact。

## 步驟決策

- Phase 1～2：keep-inline。
- Phase 3 THINK：rewrite — 強制選 lane。
- Phase 3 WRITE：rewrite — template 支援雙路徑。
- Phase 4：rewrite — 依 lane 換「來源／產物／對齊」語意。
- Phase 5：rewrite — 依 lane 換驗證入口與定稿前提。
- 新增 `rules/實驗路徑分岔判準.md`：derive-rule。
- prompt／consistency／skill-eng templates + examples：rewrite。
- 進行中 `tdd-step-execution/prompt-writing-guide.md`：rewrite 為 Skill lane。

## 檔案動作

### 新增 / 更新

- Update `SKILL.md`（description + Phase 3～5）
- Create `rules/實驗路徑分岔判準.md`
- Update `templates/prompt-writing-guide.md` + `.example.md`
- Update `templates/consistency-report.md` + `.example.md`
- Update `templates/skill-eng-validation.md` + `.example.md`
- Update `rules/人工Review閘門判準.md`（若文案寫死 Artifact）
- Update `課程教材/客製化實驗/tdd-step-execution/prompt-writing-guide.md`

### 刪除

- 刪除 Phase 3～5「一律修改 Artifact」的單一敘事
- consistency／skill-eng 在 Skill lane 強制「來源／定稿 Artifact」的硬性前提措辭

## 驗證方式

- `uv run …/analyze_skill_references.py --skill .agents/skills/design-experiment-scenario`
- 重讀 SOP：TDD「改步驟執行方法」必走 Skill lane；抽換 OpenAPI 必走 Artifact lane

## 實作閘門

- 使用者已回 `go` → 依本 plan 直接落地。
