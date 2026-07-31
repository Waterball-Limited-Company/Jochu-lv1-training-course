---
name: e2e-test-plan
description: 依同 package 的 spec.md、api-plan.md、ui-plan.md，以及若存在的 data-plan.md／DDL.md，將各 User Story 的 AC／Edge 轉成領域語言 Gherkin Scenario，依落點寫入後端／前端／整合三區塊並對齊 API／UI／可測資料約束，產出 specs/<NNN-plan-package>/e2e-test-plan.md。Use when the user invokes /e2e-test-plan, asks for E2E test plan / 端對端測試計畫 after system-analyze（api-plan 與 ui-plan 已完成）, or needs to derive layered Gherkin scenarios from acceptance criteria.
disable-model-invocation: true
---

# E2E Test Plan

依同 package 的 `spec.md`、`system-analyze/api-plan.md`、`system-analyze/ui-plan.md`，以及若存在的 `data-plan.md`／`DDL.md`，將各 User Story 的驗收標準（AC）與邊界條件（Edge）轉成領域語言 Gherkin Scenario；依落點寫入 `## 後端`／`## 前端`／`## 整合`，對應欄位追溯 US／AC / Edge／FR 與 API、UI 或可測資料約束；檔末產出測試摘要總表。產出 `specs/<NNN-plan-package>/e2e-test-plan.md`。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」，並依其讀取 `.constitution/core.md` 與本 skill 對應憲法（若存在）。
2. THINK 依本次已載入之憲法讀取規則處理缺檔或套用約束：缺檔則警告後繼續；有檔則萃取與本 skill 相關之規範，後續步驟／產出與憲法衝突時以憲法為準。
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

1. READ 讀取 `rules/Scenario產生與AC-Edge對齊判準.md`、`rules/落點與證明區塊判準.md`、`rules/Gherkin領域語言與步驟結構判準.md`、`rules/對應欄位與測試摘要總表判準.md`、`rules/認證基線Scenario判準.md`，確認 Scenario 切分、落點、GWT 寫法、對應欄位、摘要總表格式，以及有認證時的 Auth 基線義務；若 Phase 1 已載入資料合約規則，一併套用。
2. THINK 依本次已載入規則，依 AC／Edge 決定後端／前端／整合落點，展開領域語言 Scenario、對齊 `api-plan`／`ui-plan` 以及（若有）`data-plan`／`DDL` 可測約束、補齊 Auth 基線（若適用）、對應欄位與測試摘要總表，並整理檔末假設。

## Phase 4 -- 寫出 e2e-test-plan

1. READ 讀取 `templates/e2e-test-plan.md` 與 `templates/e2e-test-plan.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/e2e-test-plan.md`。

## Phase 5 -- 驗證覆蓋與修正

1. DELEGATE 執行 `uv run .agents/skills/e2e-test-plan/scripts/validate_e2e_test_plan_output.py --input specs/<NNN-plan-package>/e2e-test-plan.md`，檢查必要結構、三區塊 Scenario、對應欄位、摘要總表與 Gherkin 家規。
2. READ 回頭檢查最終產物是否符合本次已載入規則；若不符合，立即修正。
