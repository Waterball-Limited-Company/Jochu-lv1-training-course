---
name: task-plan
description: 依 e2e-test-plan、plan.md 與 system-analyze 產出三份實作計畫：後端／前端以 Scenario 為 TDD 顆粒度，由同一代理跑完 Red、Green、Refactor 與 User Story 層內全綠；整合以 User Story 跑完全端對端驗收，不假造 TDD Red。Use when the user invokes /task-plan, asks for 實作計畫／Task plan after e2e-test-plan is ready, or needs layered TDD and integration acceptance plans from specs.
disable-model-invocation: true
---

# Task Plan

依同 package 的 `e2e-test-plan.md`、`plan.md` 與 `system-analyze/` 產物，保留三份 task 檔。後端／前端每則 `S-n-m` 各自一區塊 Red → Green → Refactor → User Story 層內全綠，並在故事邊界跑整層回歸；整合每則 `US-n` 只做停用 Mock 的完全端對端驗收與失敗路由。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」（若存在），以及專案根目錄 `constitution.md`（若存在）；缺檔則略過，不報錯。
2. THINK 若已讀到憲法，萃取與本 skill 相關之 MUST，後續步驟／選型／產出與憲法衝突時改依憲法執行；若未讀到，依本 skill 預設規則繼續。
3. READ 讀取使用者需求、同 package 的 `e2e-test-plan.md`、`plan.md`、依層需要的 `system-analyze/technical-research.md`／`DDL.md`／`api-plan.md`／`ui-plan.md`，以及 `templates/task-backend.example.md`、`templates/task-frontend.example.md`、`templates/task-integration.example.md`，確認功能主題與各層 Scenario。
4. THINK 若 `e2e-test-plan.md` 不存在，停止後續步驟，先請使用者完成 `/e2e-test-plan`。
5. READ 讀取 `rules/輸出檔案定位判準.md`，確認三份產物目錄與檔名。
6. THINK 依本次已載入規則，整理 `plan-package`、三檔目標路徑與標題 metadata。

## Phase 2 -- 依層展開實作計畫內容

1. READ 讀取 `rules/產物結構與章節判準.md`、`rules/實作意圖撰寫判準.md`，確認後端／前端 Scenario 代理區塊、故事閘門、整合驗收區塊與三層環境建立方式。
2. THINK 依本次已載入規則，分別收斂後端／前端的 Scenario Red、Green、Refactor、故事累積測試、契約證據與故事邊界回歸；前端環境必須使用 plan 已選的瀏覽器套件。整合則收斂每則 `US-n` 的真串接前置、完整路徑、觀測、契約證據與失敗回送，不產出 TDD 三階段。

## Phase 3 -- 寫出三份 task

1. READ 讀取 `templates/task-backend.md`、`templates/task-frontend.md`、`templates/task-integration.md` 與對應 `.example.md`，確認骨架槽位與完成態。
2. WRITE 若需要產出三層實作計畫，先讀取 `templates/task-backend.md` 與 `templates/task-backend.example.md`、`templates/task-frontend.md` 與 `templates/task-frontend.example.md`、`templates/task-integration.md` 與 `templates/task-integration.example.md`，再依骨架複製結構、參考範例改寫填位符號與具體內容，將結果寫入 `specs/<NNN-plan-package>/task-plan/task-backend.md`、`task-frontend.md`、`task-integration.md`（必要時建立 `task-plan/`）。

## Phase 4 -- 驗證與修正

1. DELEGATE 執行 `uv run .agents/skills/task-plan/scripts/validate_task_plan_output.py --package specs/<NNN-plan-package>`，確認三檔存在、後端／前端每則 Scenario 有連續三階段與層內全綠閘門、每個故事有整層回歸、整合只有完全端對端驗收且無 TDD 三階段，以及 ID 集合與 `e2e-test-plan.md` 各層對齊。
2. DELEGATE 無條件執行 `uv run .agents/skills/task-plan/scripts/validate_api_contract_references.py --package specs/<NNN-plan-package>`；腳本自行依 package 是否存在可機械驗證契約判斷新舊流程，確認版本不可降級、三份 task 逐 Scenario 引用的契約案例存在且必要證據來源都有落點。沒有 `api-plan.md` 的非 API package 由腳本安全略過契約檢查。
3. READ 回頭檢查最終產物是否符合本次已載入規則；若不符合，立即修正。

## Phase 5 -- 收尾

1. WRITE 回報三份 task 路徑、Scenario 代理區塊數、User Story 完成閘門數與整合驗收數；下一步固定指向 `/analyze`，不可直接跳到 `/implement`。
