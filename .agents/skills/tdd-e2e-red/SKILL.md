---
name: tdd-e2e-red
description: 由 implement 在同一輪呼叫：依帶入的 layer、plan-package、單一 Scenario（整合可為 US-n）、受測行為與已定位片段，先寫入一支 E2E 測試並跑全套；若缺骨架再補最小實作骨架後重跑，直到本支為碰到主斷言的合格 Red（或交回環境洞／非預期綠），再回報給 implement。Use when implement invokes /tdd-e2e-red, or when executing a task-plan Red checkbox for one Scenario.
disable-model-invocation: true
---

# TDD E2E Red

由 `/implement` 在環境 setup 完成後、**同一輪**呼叫。針對**單一** Scenario（整合為單一 `US-n`）：優先使用已定位片段，以帶入的受測行為為準，先寫出完整 E2E 測試並執行該層全部測試；若結果顯示缺基礎骨架，再補最小骨架後重跑，直到本支為碰到主斷言的**合格 Red**（或判定環境洞／無法收斂的非預期綠）並交回 implement。不代勾 `task-*.md` checkbox，不做讓 Scenario 通過的系統行為實作（那是 `/tdd-e2e-green`）。

# SOP

## Phase 1 -- 校驗呼叫輸入並鎖定本則

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」（若存在），以及專案根目錄 `constitution.md`（若存在）；缺檔則略過，不報錯。
2. THINK 若已讀到憲法，萃取與本 skill 相關之 MUST，後續步驟／選型／產出與憲法衝突時改依憲法執行；若未讀到，依本 skill 預設規則繼續。
3. READ 讀取 implement 帶入的 `layer`、`plan-package`、本則 ID／標題、受測行為，以及已定位片段（若有）。
4. READ 讀取 `rules/呼叫輸入與層別契約.md`，確認必填欄位、單則邊界、已定位片段優先，以及缺欄時的停止條件。
5. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 6 回報。
6. READ 若尚未持有本則 e2e 區塊，依本次已載入規則在 `specs/<plan-package>/e2e-test-plan.md` 定位該區塊；已有片段則不得重開同檔定位。若依契約仍無法鎖定本則，停止並進入 Phase 6 回報。

## Phase 2 -- 依層載入本則 context

1. READ 讀取 `rules/Context載入與索引粒度.md`，確認觀測通道、禁測雛形，以及「已有片段不重載」的粒度。
2. READ 若已定位片段未覆蓋受測行為點名項目，才從對應 SA 產物補載所需片段。
3. THINK 依本次已載入規則收斂本支測試的行為準據、觀測通道與介面落點；若判定必須停止，進入 Phase 6 回報。

## Phase 3 -- 撰寫或修正 E2E 測試

1. READ 讀取 `rules/Red完成條件與改動邊界.md`，確認測檔可改範圍、合格 Red 形態（含主斷言），以及「本 phase 不可補實作骨架」。
2. READ 讀取 `rules/規格溯源註解判準.md`，確認測檔溯源註解的格式與落點。
3. THINK 依本次已載入規則，決定測檔路徑、是否需要 fixture／helper，以及如何對齊受測行為、觀測通道與契約形狀（`backend` 層斷言須含 API response status code）。
4. WRITE 一次寫出或修正完整 E2E 測試（必要時新增／調整測試用 fixture／helper），並依本次已載入規則在測檔寫入溯源註解。本 phase **不**寫產品行為，也**不**補實作骨架。
5. THINK 寫測完成後進入 Phase 4（必須先跑測，不可先去做骨架）。

## Phase 4 -- 執行全套測試

1. READ 讀取該層專案用以定義測試腳本的檔案（如 `package.json` 的 `scripts`）。
2. THINK 依本次已載入規則與已讀腳本，收斂全套測試指令；找不到可執行指令則進入 Phase 6 回報環境洞。
3. DELEGATE 執行該全套測試指令（含本支測試）。
4. THINK 依本次已載入規則的結果五類表，只判定下一動作（本 phase 不寫碼）：測試本身不可執行 → 回到 Phase 3；非預期綠且仍可加嚴斷言 → 回到 Phase 3；非預期綠且加嚴後仍綠 → 進入 Phase 6；缺骨架／compile／缺符號 → 進入 Phase 5；環境洞 → 進入 Phase 6；合格 Red → 進入 Phase 7。

## Phase 5 -- 補最小骨架實作

1. READ 若尚未持有骨架白名單與因果條文，讀取 `rules/Red完成條件與改動邊界.md` 中最小骨架相關規則。
2. THINK 依上次 Phase 4 的失敗訊息，收斂「只為讓本支測能跑到主斷言」所需的最小骨架項目；不可寫系統行為，不可自寫回 404 的 handler。
3. WRITE 僅補白名單內項目：資料定義、介面定義、函數簽章、函數體 `return null` 或 `return 0`。
4. THINK 補完後必須回到 Phase 4 重跑，不可直接宣告 Red 完成。

## Phase 6 -- 回報失敗或環境洞

1. READ 讀取 `rules/回報與環境洞交接.md`，確認失敗回報欄位與交接邊界。
2. WRITE 依本次已載入規則，向 implement 回報卡點類型（對齊結果五類或進場失敗，例如缺必填輸入、本則索引失敗、Gherkin 與受測行為矛盾）與缺口，結束本次呼叫。

## Phase 7 -- 回報合格 Red

1. READ 讀取 `rules/回報與環境洞交接.md`，確認成功回報欄位。
2. WRITE 依本次已載入規則，向 implement 回報合格 Red 結果（含主斷言與觀測通道），結束本次呼叫。
