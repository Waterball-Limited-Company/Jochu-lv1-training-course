---
name: e2e-test-plan
description: 依同 package 的 spec.md，將各 User Story 的驗收標準（AC）與邊界條件（Edge）轉成領域語言 Gherkin Scenario，並以對應欄位追溯 US／AC／Edge／FR，輸出到 specs/<NNN-plan-package>/e2e-test-plan.md。Use when the user invokes /e2e-test-plan, asks for E2E test plan / 端對端測試計畫 after specify（或下游分析完成後）, or needs to derive Gherkin scenarios from acceptance criteria.
disable-model-invocation: true
---

# E2E Test Plan

依同 package 的 `spec.md`，將各 User Story 的驗收標準（AC）與邊界條件（Edge）轉成領域語言 Gherkin Scenario；FR 只做覆蓋追溯。產出 `specs/<NNN-plan-package>/e2e-test-plan.md`。不讀取 `system-analyze/`，不綁定 API／UI 步驟。

# SOP

## Phase 1 -- 收斂 package 與輸出契約

1. READ 讀取使用者需求、同 package 的 `spec.md` 與 `templates/e2e-test-plan.example.md`，確認功能主題、US／AC／Edge／FR 與既有約束。
2. READ 讀取 `rules/輸出檔案定位判準.md`，確認最終 `e2e-test-plan.md` 的目錄與檔名。
3. THINK 依本次已載入規則，整理 `plan-package`、目標路徑與標題 metadata（功能分支／建立日期／狀態）。

## Phase 2 -- 掃描 NEED CLARIFICATION 並決定是否先澄清

1. THINK 掃描 `spec.md` 各 US 邊界條件中的 `[NEED CLARIFICATION: ...]`（及依賴未澄清決策的邊界），列出將標為 blocked、本輪不產出 Scenario 的項目。
2. DELEGATE 若存在上述項目，先詢問使用者是否呼叫 `/clarify` 釐清；若使用者同意則委派 `/clarify`，並在澄清結果回寫 `spec.md` 後重新進入本 phase；若使用者選擇暫不澄清，則帶著 blocked 清單繼續，不自行腦補行為。

## Phase 3 -- 展開 Scenario 與對應欄位

1. READ 讀取 `rules/Scenario產生與AC-Edge對齊判準.md`、`rules/Gherkin領域語言與步驟結構判準.md`、`rules/對應欄位與覆蓋總表判準.md`，確認 Scenario 切分、GWT 寫法與追溯格式。
2. THINK 依本次已載入規則，依 US（含優先級）展開 Scenario、補齊對應欄位與元素覆蓋總表，並整理檔末假設。

## Phase 4 -- 寫出 e2e-test-plan

1. READ 讀取 `templates/e2e-test-plan.md` 與 `templates/e2e-test-plan.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/e2e-test-plan.md`。

## Phase 5 -- 驗證覆蓋與修正

1. DELEGATE 執行 `uv run .agents/skills/e2e-test-plan/scripts/validate_e2e_test_plan_output.py --input specs/<NNN-plan-package>/e2e-test-plan.md`，檢查必要結構、Scenario／覆蓋表與 Gherkin 家規。
2. READ 回頭檢查最終產物是否符合本次已載入規則；若不符合，立即修正。
