---
name: e2e-test-plan
description: 依同 package 的 spec.md、api-plan.md、ui-plan.md，以及若存在的 data-plan.md／DDL.md，將各 User Story 的 AC／Edge 轉成領域語言薄切片 Gherkin（後端／前端），整合對準各 US 獨立驗證；對應欄位含受測部位、前置資料、觀測通道，產出 specs/<NNN-plan-package>/e2e-test-plan.md。Use when the user invokes /e2e-test-plan, asks for E2E test plan / 端對端測試計畫 after system-analyze（api-plan 與 ui-plan 已完成）, or needs to derive layered Gherkin scenarios from acceptance criteria.
disable-model-invocation: true
---

# E2E Test Plan

依同 package 的 `spec.md`、`system-analyze/api-plan.md`、`system-analyze/ui-plan.md`，以及若存在的 `data-plan.md`／`DDL.md`，將各 User Story 的 AC／Edge 轉成領域語言薄切片 Gherkin，寫入 `## 後端`／`## 前端`；`## 整合` 對準各 US 獨立驗證（`US-n`）。對應欄位含受測部位、前置資料、觀測通道；檔末產出切片表與驗收表。產出 `specs/<NNN-plan-package>/e2e-test-plan.md`。完成態見 `templates/e2e-test-plan.example.md`。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」（若存在），以及專案根目錄 `constitution.md`（若存在）；缺檔則略過，不報錯。
2. THINK 若已讀到憲法，萃取與本 skill 相關之 MUST，後續步驟／選型／產出與憲法衝突時改依憲法執行；若未讀到，依本 skill 預設規則繼續。
3. READ 讀取使用者需求、同 package 的 `spec.md`、`system-analyze/api-plan.md`、`system-analyze/ui-plan.md` 與 `templates/e2e-test-plan.example.md`，確認功能主題、US／AC／Edge／FR、API／UI 合約與既有約束。
4. THINK 若 `api-plan.md` 或 `ui-plan.md` 不存在，停止後續步驟，先請使用者完成對應計畫（或經 `/system-analyze` 主鏈產出）。
5. READ 讀取 `rules/資料合約讀取與對齊判準.md`；若同 package 存在 `system-analyze/data-plan.md` 則 READ 之；若存在 `system-analyze/DDL.md` 則 READ 之。
6. THINK 依資料合約規則處理缺檔（不硬停）或收斂與本期相關的可測持久化約束。
7. READ 讀取 `rules/輸出檔案定位判準.md`，確認最終 `e2e-test-plan.md` 的目錄與檔名。
8. THINK 依本次已載入規則，整理 `plan-package`、目標路徑與標題 metadata（功能分支／建立日期／狀態）。

## Phase 2 -- 掃描 NEED CLARIFICATION 並決定是否先澄清

1. READ 讀取 `rules/Scenario產生與AC-Edge對齊判準.md` 中關於 blocked 的規則，確認未澄清邊界如何標示與是否可產出 Scenario。
2. THINK 掃描 `spec.md` 各 US 邊界條件中的 `[NEED CLARIFICATION: ...]`（及依賴未澄清決策的邊界），列出將標為 blocked、本輪不產出 Scenario 的項目。
3. DELEGATE 若存在上述項目，先詢問使用者是否呼叫 `/clarify` 釐清；若使用者同意則委派 `/clarify`，並在澄清結果回寫 `spec.md` 後重新進入本 phase；若使用者選擇暫不澄清，則帶著 blocked 清單繼續，不自行腦補行為。

## Phase 3 -- 展開 Scenario、落點與對應欄位

1. READ 讀取 `rules/Scenario產生與AC-Edge對齊判準.md`、`rules/落點與證明區塊判準.md`、`rules/Gherkin領域語言與步驟結構判準.md`、`rules/對應欄位與測試摘要總表判準.md`、`rules/產物可讀性與雛形非受測判準.md`，確認 Scenario 切分、落點、GWT 寫法、對應欄位與切片表／驗收表格式；若 Phase 1 已載入資料合約規則，一併套用。產物用白話，不把雛形 HTML 當受測物，也不把 skill 備註寫進 e2e-test-plan。
2. THINK 依本次已載入規則，將 AC／Edge 展開為後端／前端薄切片（一則一個 seam）；整合各 US 一則驗收（`US-n`），不抄薄 Scenario。對齊 `api-plan`／`ui-plan` 以及（若有）`data-plan`／`DDL`，補齊對應欄位（含觀測通道）與切片表／驗收表，並整理檔末假設。

## Phase 4 -- 寫出 e2e-test-plan

1. READ 讀取 `templates/e2e-test-plan.md` 與 `templates/e2e-test-plan.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/e2e-test-plan.md`。

## Phase 5 -- 驗證覆蓋與修正

1. DELEGATE 執行 `uv run .agents/skills/e2e-test-plan/scripts/validate_e2e_test_plan_output.py --input specs/<NNN-plan-package>/e2e-test-plan.md`，檢查必要結構、三區塊 Scenario、對應欄位、切片表／驗收表與 Gherkin 家規。
2. READ 回頭檢查最終產物是否符合本次已載入規則；若不符合，立即修正。
