---
name: tdd-e2e-green
description: 由完成合格 Red 的同一位後端或前端 Scenario Agent 呼叫：沿用 Red 的實際失敗與已定位片段，只做讓單一 Scenario 通過的最少 Green，並守住既有綠燈；成功後在同一代理脈絡接續 Refactor。整合驗收不得使用本 skill。
disable-model-invocation: true
---

# TDD E2E Green

由剛完成 Red 的同一 Scenario Agent 呼叫，只接受 `backend` 或 `frontend` 的單一 `S-n-m`。沿用 Red 證據做 just enough 程式碼，讓本則變綠並守住既有綠燈；成功後在同一代理脈絡接續 `/tdd-e2e-refactor`。禁止以一次做完整 User Story 為策略，整合驗收不得使用本 skill。

# SOP

## Phase 1 -- 校驗呼叫輸入並鎖定本則

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」（若存在），以及專案根目錄 `constitution.md`（若存在）；缺檔則略過，不報錯。
2. THINK 若已讀到憲法，萃取與本 skill 相關之 MUST，後續步驟／選型／產出與憲法衝突時改依憲法執行；若未讀到，依本 skill 預設規則繼續。
3. READ 讀取 Scenario Agent 帶入的 `scenario-agent-id`、`layer`、`plan-package`、`user-story`、本則 ID／標題、Green 實作計畫、Red 證據與已定位片段。
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

## Phase 4 -- 回報 Scenario Agent

1. READ 讀取 `rules/回報與環境洞交接.md`，確認成功／失敗回報欄位。
2. WRITE 依本次已載入規則，向同一 Scenario Agent 回報本次結果；成功則接續 Refactor，失敗則停止該 Scenario。
