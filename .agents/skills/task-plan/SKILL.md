---
name: task-plan
description: 依同 package 的 e2e-test-plan、plan.md 與 system-analyze（technical-research／DDL／api-plan／ui-plan 依層），產出從零到完的 step-by-step 實作計畫（環境建立＋各 US 的 AC／Edge＋Red 巢狀受測行為／Green 巢狀實作計畫／Refactor，且每個 US 的 Red 末尾含固定驗紅項），寫入 specs/<NNN-plan-package>/task-plan/ 的 task-backend.md、task-frontend.md、task-integration.md。Use when the user invokes /task-plan, asks for 實作計畫／Task plan after e2e-test-plan is ready, or needs layered TDD R-G-R implementation plans from specs.
disable-model-invocation: true
---

# Task Plan

依同 package 的 `e2e-test-plan.md`、`plan.md`、`system-analyze/technical-research.md`、`system-analyze/DDL.md`、`system-analyze/api-plan.md`、`system-analyze/ui-plan.md`（依層取用），產出可給 implement 從零執行的實作計畫：規格閱讀、環境建立、各 User Story 的 AC／Edge 與 Red → Green → Refactor（Red 巢狀受測行為、Green 巢狀實作計畫）。寫入 `specs/<NNN-plan-package>/task-plan/task-backend.md`、`task-frontend.md`、`task-integration.md`。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取使用者需求、同 package 的 `e2e-test-plan.md`、`plan.md`、依層需要的 `system-analyze/technical-research.md`／`DDL.md`／`api-plan.md`／`ui-plan.md`，以及 `templates/task-backend.example.md`、`templates/task-frontend.example.md`、`templates/task-integration.example.md`，確認功能主題與各層 Scenario。
2. THINK 若 `e2e-test-plan.md` 不存在，停止後續步驟，先請使用者完成 `/e2e-test-plan`。
3. READ 讀取 `rules/輸出檔案定位判準.md`，確認三份產物目錄與檔名。
4. THINK 依本次已載入規則，整理 `plan-package`、三檔目標路徑與標題 metadata。

## Phase 2 -- 依層展開實作計畫內容

1. READ 讀取 `rules/產物結構與章節判準.md`、`rules/實作意圖撰寫判準.md`，確認章節階層、US 節奏，以及 Red「受測行為」／Green「實作計畫」寫法。
2. THINK 依本次已載入規則，分別收斂後端／前端／整合：規格閱讀清單、環境建立步驟、各 US 的 AC／Edge、Red（巢狀受測行為）／Green（巢狀實作計畫）／Refactor（每個 US 的 Red 區塊末尾含固定驗紅項）、進度總覽與假設；Scenario 集合對齊 `e2e-test-plan.md` 對應 `##` 區塊。

## Phase 3 -- 寫出三份 task

1. READ 讀取 `templates/task-backend.md`、`templates/task-frontend.md`、`templates/task-integration.md` 與對應 `.example.md`，確認骨架槽位與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/task-plan/task-backend.md`、`task-frontend.md`、`task-integration.md`（必要時建立 `task-plan/`）。

## Phase 4 -- 驗證與修正

1. DELEGATE 執行 `uv run .agents/skills/task-plan/scripts/validate_task_plan_output.py --package specs/<NNN-plan-package>`，檢查三檔存在、必要章節、US／Red／Green／Refactor 結構、Scenario 巢狀受測行為、Green 巢狀實作計畫、每個 US Red 末尾固定驗紅項，以及 Red Scenario 與 `e2e-test-plan.md` 各層對齊。
2. READ 回頭檢查最終產物是否符合本次已載入規則；若不符合，立即修正。
