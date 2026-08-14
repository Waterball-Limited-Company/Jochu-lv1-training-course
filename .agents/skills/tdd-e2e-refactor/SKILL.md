---
name: tdd-e2e-refactor
description: 由 implement 在該則 Green 之後、同一輪呼叫：依 layer、plan-package、單一 Scenario（整合可為 US-n）與該格整理範圍，在行為與契約不變下只整理這一則剛綠的碼；過程可多次跑該層全套測試，結束必須本則仍綠並回報。Use when implement invokes /tdd-e2e-refactor, or when executing a task-plan Refactor checkbox for one Scenario.
disable-model-invocation: true
---

# TDD E2E Refactor

由 `/implement` 在**該則**已 Green 之後、同一輪呼叫。一次針對**一個 Scenario**（整合為一個 `US-n`）：依該格「整理範圍」整理程式碼與測試（去重、非功能品質、計畫點名的對齊風格／抽層），**不改行為與契約**，不准擴到本則不驗證／下一則。過程可多次執行該層全套測試；結束時本則必須仍綠、既有綠仍綠。不代勾 `task-*.md` checkbox。

# SOP

## Phase 1 -- 校驗呼叫輸入

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」（若存在），以及專案根目錄 `constitution.md`（若存在）；缺檔則略過，不報錯。
2. THINK 若已讀到憲法，萃取與本 skill 相關之 MUST，後續步驟／選型／產出與憲法衝突時改依憲法執行；若未讀到，依本 skill 預設規則繼續。
3. READ 讀取 implement 帶入的 `layer`、`plan-package`、本則 ID／標題、整理範圍，以及已定位片段（若有）。
4. READ 讀取 `rules/呼叫輸入與Scenario範圍契約.md`，確認必填欄位與單則邊界。
5. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 4 回報。

## Phase 2 -- 載入重構 context 並確認本則已綠

1. READ 讀取 `rules/Context與重構範圍判準.md`、`rules/Refactor完成條件與改動邊界.md`，確認可載內容、允許／禁止範圍，以及本則已綠／既有綠仍綠閘門。
2. READ 依本次已載入規則載入：整理範圍點名的程式／測試；必要時點名且尚未持有的 SA 片段。
3. READ 讀取該層測試腳本定義（如 `package.json` 的 `scripts`）。
4. THINK 依本次已載入規則收斂全套測試指令；找不到則進入 Phase 4 回報。
5. DELEGATE 執行該層全套測試。
6. THINK 依本次已載入規則判定起點是否可進入重構（本則已綠、既有綠仍綠；不要求尚未寫出的下一則也綠）；若不通過，進入 Phase 4 回報。

## Phase 3 -- 依整理範圍重構並保持綠

1. WRITE 依本次已載入規則與整理範圍進行重構。
2. DELEGATE 執行該層全套測試。
3. THINK 依本次已載入規則判定本則是否仍綠、既有綠是否仍綠、是否繼續重構，或進入 Phase 4（成功或失敗回報）。

## Phase 4 -- 回報 implement

1. READ 讀取 `rules/回報與環境洞交接.md`，確認回報欄位。
2. WRITE 依本次已載入規則，向 implement 回報本次結果。
