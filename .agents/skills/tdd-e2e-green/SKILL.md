---
name: tdd-e2e-green
description: 由 implement 在同一輪呼叫：依 layer、plan-package、單一 Scenario（整合可為 US-n）與該格 Green 實作計畫，優先使用已定位片段，做 just enough 程式碼讓本則變綠；跑該層全套測試，不弄紅既有綠燈，遵守本則不驗證。Use when implement invokes /tdd-e2e-green, or when executing a task-plan Green checkbox for one Scenario.
disable-model-invocation: true
---

# TDD E2E Green

由 `/implement` 在同一輪呼叫。一次針對**一個 Scenario**（整合為一個 `US-n`）：依該格 Green 實作計畫做 just enough 程式碼實作，讓本則紅測變綠；執行該層全部測試，確認本則變綠且不弄紅本層先前已綠的測。禁止以「一次實作讓本 US 多支變綠」當策略；附帶變綠可回報。遵守該格「本則不驗證」。不代勾 `task-*.md` checkbox。

# SOP

## Phase 1 -- 校驗呼叫輸入並鎖定本則

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」（若存在），以及專案根目錄 `constitution.md`（若存在）；缺檔則略過，不報錯。
2. THINK 若已讀到憲法，萃取與本 skill 相關之 MUST，後續步驟／選型／產出與憲法衝突時改依憲法執行；若未讀到，依本 skill 預設規則繼續。
3. READ 讀取 implement 帶入的 `layer`、`plan-package`、本則 ID／標題、Green 實作計畫，以及已定位片段（若有）。
4. READ 讀取 `rules/呼叫輸入與Scenario範圍契約.md`，確認必填欄位與單則邊界。
5. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 4 回報。
6. READ 依本次已載入規則，確認本則對應的既有 Red 測檔可定位；無法鎖定本則則進入 Phase 4 回報。

## Phase 2 -- 載入本則 context

1. READ 讀取 `rules/Context載入判準.md`，確認進場可載內容與「已有片段不重載」。
2. READ 依本次已載入規則載入：本則既有 Red 測、Green 實作計畫點名且尚未持有的 SA 片段、將改動的既有程式碼。
3. THINK 依本次已載入規則整理本則實作邊界與「本則不驗證」；若判定必須停止，進入 Phase 4 回報。

## Phase 3 -- 程式碼實作並以全套測試讓本則變綠

1. READ 讀取 `rules/Green完成條件與改動邊界.md`，確認本則推進、全套跑測、回歸與禁止以多支同綠當策略的界線。
2. READ 讀取 `rules/規格溯源註解判準.md`，確認實作檔溯源註解的格式與落點。
3. THINK 依本次已載入規則與 Green 實作計畫，收斂讓本則變綠所需的 just enough 程式碼。
4. WRITE 依本次已載入規則完成必要程式碼實作，並在實作檔寫入溯源註解。
5. READ 讀取該層專案測試腳本定義（如 `package.json` 的 `scripts`）。
6. THINK 依本次已載入規則收斂全套測試指令；找不到則停止並進入 Phase 4 回報。
7. DELEGATE 執行該層全套測試。
8. THINK 依本次已載入規則判定本則是否已綠、既有綠是否仍綠；未過則回到本 Phase 繼續，或進入 Phase 4 回報失敗。本則已綠則進入 Phase 4 成功回報。

## Phase 4 -- 回報 implement

1. READ 讀取 `rules/回報與環境洞交接.md`，確認成功／失敗回報欄位。
2. WRITE 依本次已載入規則，向 implement 回報本次結果。
