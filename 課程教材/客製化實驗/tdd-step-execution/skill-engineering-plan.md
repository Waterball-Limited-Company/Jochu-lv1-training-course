# Skill 工程編排提案

## 任務資訊

- 處理路徑: `optimize`
- 改動範圍: `step rewrite`
- 目標 Skills: `design-experiment-scenario`

## 控制平面重建

- 維持五 phase 主幹不變；只重寫 Phase 2 WRITE 的呈現契約為「改版格式」。
- Phase 2 THINK 仍要收斂實驗目標，但產出時把目標壓進單行 `**範圍**`，不再以獨立長段當 Review 主體。
- 選項卡片欄位與 5～10／字母排序不變；外殼改為 `Phase 2 (改版格式)｜主題` + 選項。

## 步驟決策

- Phase 1 各 step：keep-inline。
- Phase 2 READ 規則／閘門：keep-inline。
- Phase 2 THINK（收斂目標與排序）：keep-inline；語意改為「目標收斂進範圍句」。
- Phase 2 WRITE（依 template 產出）：rewrite — 改版格式為唯一主呈現。
- `rules/情境列舉與排序判準.md`：rewrite — Rule 1／3／Good Example 對齊改版格式。
- `templates/experiment-goals-and-scenarios.md` + `.example.md`：rewrite — 刪舊企劃外殼，改改版格式骨架／範例。
- Phase 3～5：keep-inline。
- 不新增 script；不新增第二套 template（避免雙重真相）。

## 檔案動作

### 新增 / 更新

- Update `design-experiment-scenario/SKILL.md`（Phase 2 WRITE／THINK 對齊句）
- Update `rules/情境列舉與排序判準.md`
- Update `templates/experiment-goals-and-scenarios.md`
- Update `templates/experiment-goals-and-scenarios.example.md`
- 落盤本 plan 於 `課程教材/客製化實驗/tdd-step-execution/skill-engineering-plan.md`

### 刪除

- 刪除 template／example 中作為 **Phase 2 主呈現必填** 的：課程來源、建立日期、狀態、`## 實驗目標`、`## 情境可能性` 舊章節標題（內容語意併入範圍句與選項卡片，不另留平行骨架）

## 驗證方式

- 重讀 Phase 2 SOP：WRITE 只指向改版格式 template。
- 執行 `uv run .agents/skills/skill-engineering/scripts/analyze_skill_references.py --skill .agents/skills/design-experiment-scenario`
- 對照 example 與使用者截圖結構：標題／範圍／選項欄位一致

## 實作閘門

- 使用者已確認根因並表示「可以產了」→ 依本 plan 直接落地。
