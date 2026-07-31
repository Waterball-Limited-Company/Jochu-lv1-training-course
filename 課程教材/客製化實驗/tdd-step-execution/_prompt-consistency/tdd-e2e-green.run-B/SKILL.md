---
name: tdd-e2e-green
description: 由 implement 呼叫：依 layer、plan-package、單一 User Story 與 Green 實作計畫，載入本 US 既有 Red 測與點名 SA／程式片段，以仍紅 Scenario 為目標做 just enough 程式碼實作；每輪內部迴圈只鎖定一支仍紅 Scenario，每步跑該層全套測試推進變綠，直到本 US 全綠後回報。Use when implement invokes /tdd-e2e-green, or when executing a task-plan Green checkbox for one User Story.
disable-model-invocation: true
---

# TDD E2E Green

由 `/implement` 呼叫。一次針對**一個 User Story**：依 Green 實作計畫做 just enough 程式碼實作，內部以「仍紅的 Scenario」推進；**每一輪內部迴圈只鎖定一支仍紅 Scenario** 作為實作目標（對齊「一次只過一個失敗測試」；不是 triangulation／mini-step）。每步執行該層全部測試，確認鎖定目標變綠且不弄紅本層先前已綠的測；若附帶變綠其他測可計入已綠並回報，但不得當推進策略、不得藉此超寫，下一輪仍只挑一支仍紅者。本 US 相關測皆綠後回報 implement。不代勾 `task-*.md` checkbox。

# SOP

## Phase 1 -- 校驗呼叫輸入並收斂本 US 範圍

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」，以及專案根目錄 `constitution.md`（若存在）。
2. THINK 依本次已載入之憲法讀取規則處理缺檔或套用約束：缺檔則警告後繼續；有檔則萃取與本 skill 相關之規範，後續步驟／產出與憲法衝突時以憲法為準。
3. READ 讀取 implement 帶入的 `layer`、`plan-package`、User Story 識別（如 `US-1`）、Green 實作計畫，以及本 US 的 Scenario 清單（若未帶清單，從實作計畫／既有 Red 測與 e2e 對應推得）。
4. READ 讀取 `rules/呼叫輸入與US範圍契約.md`，確認必填欄位與單 US 邊界。
5. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 5 回報。
6. READ 依本次已載入規則，確認本 US 對應的既有 Red 測檔與 `e2e-test-plan.md` 中相關 Scenario 區塊可定位；無法收斂範圍則進入 Phase 5 回報。

## Phase 2 -- 載入本 US 的 context

1. READ 讀取 `rules/Context載入判準.md`，確認進場可載內容與迴圈補讀粒度。
2. READ 依本次已載入規則載入：本 US 既有 Red 測、Green 實作計畫點名的 SA 片段、將改動的既有程式碼。
3. THINK 依本次已載入規則整理「仍紅 Scenario」清單與本輪實作順序；若判定必須停止，進入 Phase 5 回報。

## Phase 3 -- 迴圈：程式碼實作並以全套測試推進變綠

1. READ 讀取 `rules/Green完成條件與改動邊界.md`，確認每輪只鎖定一支仍紅 Scenario、全套跑測、回歸與附帶變綠的界線。
2. THINK 依本次已載入規則與 Green 實作計畫，**選取下一支仍紅 Scenario** 作為本輪唯一實作目標，並收斂本次 just enough 程式碼實作。
3. WRITE 依本次已載入規則完成必要程式碼實作。
4. READ 讀取該層專案測試腳本定義（如 `package.json` 的 `scripts`）。
5. THINK 依本次已載入規則收斂全套測試指令；找不到則停止並進入 Phase 5 回報。
6. DELEGATE 執行該層全套測試。
7. THINK 依本次已載入規則更新仍紅／已綠清單（含附帶變綠者）、確認本輪鎖定目標是否變綠，並判定是否繼續迴圈、進入 Phase 4，或進入 Phase 5 回報。

## Phase 4 -- 確認本 US 全綠

1. DELEGATE 若尚需終態確認，再執行一次該層全套測試。
2. THINK 依本次已載入規則判定本 US 是否可交付全綠；通過則進入 Phase 5，否則回到 Phase 3 或進入 Phase 5 回報失敗。

## Phase 5 -- 回報 implement

1. READ 讀取 `rules/回報與環境洞交接.md`，確認成功／失敗回報欄位。
2. WRITE 依本次已載入規則，向 implement 回報本次結果。
