---
name: tdd-e2e-red
description: 由 implement 在環境就緒後呼叫：依帶入的 layer、plan-package、單一 Scenario 與實作計畫，按需載入該 Scenario 的 e2e／SA 介面片段，寫入一支 E2E 測試（可含測試用 fixture／helper，不寫產品業務碼），跑全套測試並確認該新測為 Red，再回報給 implement。Use when implement invokes /tdd-e2e-red, or when executing a task-plan Red checkbox for one Scenario.
disable-model-invocation: true
---

# TDD E2E Red

由 `/implement` 在環境 setup 完成後呼叫。針對**單一** Scenario：以帶入的實作計畫為索引載入必要 context，寫出完整 E2E 測試，執行該層全部測試，確認**本支新測**為 Red，並將結果交回 implement。不代勾 `task-*.md` checkbox，不實作產品業務行為（那是 `/tdd-e2e-green`）。

# SOP

## Phase 1 -- 校驗呼叫輸入並定位 Scenario

1. READ 讀取 implement 帶入的 `layer`、`plan-package`、Scenario ID／標題與實作計畫。
2. READ 讀取 `rules/呼叫輸入與層別契約.md`，確認必填欄位、單 Scenario 邊界、定位與缺欄時的停止條件。
3. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 5 回報。
4. READ 依本次已載入規則，在 `specs/<plan-package>/e2e-test-plan.md` 定位該 Scenario 區塊；若依契約仍無法定位，停止並進入 Phase 5 回報。

## Phase 2 -- 依層載入本 Scenario 的 context

1. READ 讀取 `rules/Context載入與索引粒度.md`，確認各層必讀檔、路徑與「只讀點名元素」的粒度。
2. READ 依本次已載入規則與實作計畫點名項目，從對應 SA 產物載入所需片段。
3. THINK 依本次已載入規則收斂本支測試的行為準據與介面落點；若判定必須停止，進入 Phase 5 回報。

## Phase 3 -- 寫入 E2E 測試（可含測試基建）

1. READ 讀取 `rules/Red完成條件與改動邊界.md`，確認可改動範圍、測檔落點與空殼／環境洞界線。
2. THINK 依本次已載入規則，決定測檔路徑、是否需要 fixture／helper，以及如何對齊契約形狀。
3. WRITE 一次寫出完整 E2E 測試（必要時新增／調整測試用 fixture／helper）。若判定為環境／基建缺口而無法繼續，停止並進入 Phase 5 回報。

## Phase 4 -- 跑全套測試並證明本支為 Red

1. READ 讀取該層專案用以定義測試腳本的檔案（如 `package.json` 的 `scripts`）。
2. THINK 依本次已載入規則與已讀腳本，收斂全套測試指令；找不到可執行指令則停止並進入 Phase 5 回報。
3. DELEGATE 執行該全套測試指令（含剛寫入的測試）。
4. THINK 依本次已載入規則判定本支是否為合格業務 Red；若測試本身錯誤可先修正後重跑。通過則進入 Phase 5；無法證明 Red（含非預期綠或環境洞）則進入 Phase 5 回報。

## Phase 5 -- 回報 implement

1. READ 讀取 `rules/回報與環境洞交接.md`，確認成功／失敗回報欄位與交接邊界。
2. WRITE 依本次已載入規則，向 implement 回報本次結果。
