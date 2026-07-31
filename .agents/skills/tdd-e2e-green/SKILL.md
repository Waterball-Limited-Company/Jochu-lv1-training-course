---
name: tdd-e2e-green
description: 由 implement 呼叫：依 layer、plan-package、單一 Scenario（對齊 Red 產出的 e2e 案例）與該格 Green 實作計畫，載入對應 Red 測與點名 SA／程式片段，只為該支仍紅 Scenario 做 just enough 程式碼實作；跑該層全套測試確認本支變綠且不弄紅既有綠燈後回報。Use when implement invokes /tdd-e2e-green, or when executing a task-plan Green checkbox for one Scenario.
disable-model-invocation: true
---

# TDD E2E Green

由 `/implement` 呼叫。一次針對**一個 Scenario**（對齊 task 一格、對齊 Red 的 e2e 案例）：依該格 Green 實作計畫做 just enough 程式碼實作；執行該層全部測試，確認本支變綠且不弄紅本層先前已綠的測。若附帶使其他仍紅測變綠，可回報註明，但不得當成推進策略或藉此超寫。不代勾 `task-*.md` checkbox。

# SOP

## Phase 1 -- 校驗呼叫輸入並定位 Scenario

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」，以及專案根目錄 `constitution.md`（若存在）。
2. THINK 依本次已載入之憲法讀取規則處理缺檔或套用約束：缺檔則警告後繼續；有檔則萃取與本 skill 相關之規範，後續步驟／產出與憲法衝突時以憲法為準。
3. READ 讀取 implement 帶入的 `layer`、`plan-package`、單一 Scenario ID／標題、該格 Green 實作計畫（可附所屬 US 識別供對照）。
4. READ 讀取 `rules/呼叫輸入與Scenario範圍契約.md`，確認必填欄位與單 Scenario 邊界。
5. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 5 回報。
6. READ 依本次已載入規則，確認該 Scenario 對應的既有 Red 測檔與 `e2e-test-plan.md` 中相關區塊可定位；無法收斂則進入 Phase 5 回報。

## Phase 2 -- 載入本 Scenario 的 context

1. READ 讀取 `rules/Context載入判準.md`，確認進場可載內容與迴圈補讀粒度。
2. READ 依本次已載入規則載入：本 Scenario 既有 Red 測、Green 實作計畫點名的 SA 片段、將改動的既有程式碼。
3. THINK 依本次已載入規則確認本支仍為紅（或判定已綠／必須停止）；若必須停止，進入 Phase 5 回報。

## Phase 3 -- 程式碼實作並以全套測試推進本支變綠

1. READ 讀取 `rules/Green完成條件與改動邊界.md`，確認單 Scenario 推進、全套跑測、回歸與附帶變綠界線。
2. THINK 依本次已載入規則與 Green 實作計畫，只為**本支** Scenario 收斂 just enough 程式碼實作。
3. WRITE 依本次已載入規則完成必要程式碼實作。
4. READ 讀取該層專案測試腳本定義（如 `package.json` 的 `scripts`）。
5. THINK 依本次已載入規則收斂全套測試指令；找不到則停止並進入 Phase 5 回報。
6. DELEGATE 執行該層全套測試。
7. THINK 依本次已載入規則判定本支是否已綠、有無附帶變綠、有無弄紅既有綠；通過則進入 Phase 4，否則回到本 Phase 修正或進入 Phase 5 回報失敗。

## Phase 4 -- 確認本支 Scenario 已綠

1. DELEGATE 若尚需終態確認，再執行一次該層全套測試。
2. THINK 依本次已載入規則判定本支是否可交付為綠；通過則進入 Phase 5，否則回到 Phase 3 或進入 Phase 5 回報失敗。

## Phase 5 -- 回報 implement

1. READ 讀取 `rules/回報與環境洞交接.md`，確認成功／失敗回報欄位。
2. WRITE 依本次已載入規則，向 implement 回報本次結果。
