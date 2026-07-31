---
name: tdd-e2e-red
description: 由 implement 在環境就緒後呼叫：依帶入的 layer、plan-package、單一 User Story 與其 Scenario 清單（含各格受測行為），按依賴順序一次一支寫入 E2E 測並跑全套至合格 Red，再進下一支；整 US 皆合格紅（或中途環境洞／非預期綠）後回報。Use when implement invokes /tdd-e2e-red for a User Story Red batch, or when executing task-plan Red checkboxes for one US.
disable-model-invocation: true
---

# TDD E2E Red

由 `/implement` 在環境 setup 完成後呼叫。針對**單一 User Story 的 Red 批次**：帶入該 US 的 Scenario 清單與各格受測行為；內部仍**一次只實作一支**測檔，寫完必須跑該層全套測試並取得**合格 Red**（須碰到本 Scenario 主斷言）後，才進入清單下一支。不做讓 Scenario 通過的系統行為實作（那是 `/tdd-e2e-green`）；不代勾 `task-*.md`。

# SOP

## Phase 1 -- 校驗 US 批次輸入並收斂順序

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」，並依其讀取 `.constitution/core.md` 與本 skill 對應憲法（若存在）。
2. THINK 依本次已載入之憲法讀取規則處理缺檔或套用約束：缺檔則警告後繼續；有檔則萃取與本 skill 相關之規範，後續步驟／產出與憲法衝突時以憲法為準。
3. READ 讀取 implement 帶入的 `layer`、`plan-package`、User Story 識別、Scenario 清單（各含 ID／標題與受測行為）。
4. READ 讀取 `rules/呼叫輸入與層別契約.md`，確認必填欄位、US 批次邊界、排序與缺欄時的停止條件。
5. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 6 回報。
6. READ 依本次已載入規則，在 `specs/<plan-package>/e2e-test-plan.md` 逐一定位清單內各 Scenario；任一無法定位則停止並進入 Phase 6 回報。
7. THINK 依契約對清單排序（認證／session 基線與被依賴項在前）；收斂「待做佇列」後進入 Phase 2。

## Phase 2 -- 取出下一 Scenario 並載入 context

1. THINK 若待做佇列已空，進入 Phase 7 回報本 US 批次成功。
2. THINK 取出佇列第一個 Scenario 作為「本支」。
3. READ 讀取 `rules/Context載入與索引粒度.md`，確認各層必讀檔、路徑與「只讀點名元素」的粒度。
4. READ 依本次已載入規則與本支受測行為點名項目，從對應 SA 產物載入所需片段。
5. THINK 依本次已載入規則收斂本支測試的行為準據、介面落點與**主斷言**；若判定必須停止，進入 Phase 6 回報。

## Phase 3 -- 撰寫或修正本支 E2E 測試

1. READ 讀取 `rules/Red完成條件與改動邊界.md`，確認測檔可改範圍、合格 Red 形態（含主斷言）、以及「本 phase 不可補實作骨架」。
2. THINK 依本次已載入規則，決定測檔路徑、是否需要 fixture／helper，以及如何對齊受測行為與契約形狀（`backend` 層斷言須含 API response status code）。
3. WRITE 一次寫出或修正**本支**完整 E2E 測試（必要時新增／調整測試用 fixture／helper）。本 phase **不**寫產品行為，也**不**補實作骨架；**不可**一次寫入佇列中多支 Scenario 的測檔。
4. THINK 寫測完成後進入 Phase 4（必須先跑測，不可先去做骨架）。

## Phase 4 -- 執行全套測試

1. READ 讀取該層專案用以定義測試腳本的檔案（如 `package.json` 的 `scripts`）。
2. THINK 依本次已載入規則與已讀腳本，收斂全套測試指令；找不到可執行指令則進入 Phase 6 回報環境洞。
3. DELEGATE 執行該全套測試指令（含本支測試）。
4. THINK 依本次已載入規則的結果分類表，只判定下一動作（本 phase 不寫碼）：測試本身不可執行 → 回到 Phase 3；非預期綠且仍可加嚴斷言 → 回到 Phase 3；非預期綠且加嚴後仍綠 → 進入 Phase 6；缺骨架／compile／缺符號／走不到主斷言 → 進入 Phase 5；主斷言未達（死在前置）→ 依規則重排／補依賴骨架或 Phase 6；環境洞 → 進入 Phase 6；合格 Red → 將本支標為完成並回到 Phase 2 取下一支。

## Phase 5 -- 補最小骨架實作

1. READ 若尚未持有骨架白名單與因果條文，讀取 `rules/Red完成條件與改動邊界.md` 中最小骨架相關規則。
2. THINK 依上次 Phase 4 的失敗訊息，收斂「只為讓本支測能跑到**主斷言**」所需的最小骨架項目；不可寫系統行為，不可自寫回 404 的 handler。
3. WRITE 僅補白名單內項目：資料定義、介面定義、函數簽章、函數體 `return null` 或 `return 0`。
4. THINK 補完後必須回到 Phase 4 重跑，不可直接宣告本支 Red 完成，也不可跳進下一 Scenario。

## Phase 6 -- 回報失敗或環境洞

1. READ 讀取 `rules/回報與環境洞交接.md`，確認失敗回報欄位與交接邊界。
2. WRITE 依本次已載入規則，向 implement 回報：本 US、已完成合格紅的 Scenario 清單、卡在哪一支、卡點類型與缺口；結束本次呼叫（佇列後續未做項不繼續）。

## Phase 7 -- 回報本 US 批次合格 Red

1. READ 讀取 `rules/回報與環境洞交接.md`，確認成功回報欄位。
2. WRITE 依本次已載入規則，向 implement 回報本 US 全部清單 Scenario 的合格 Red 結果（含各支測檔與形態摘要），結束本次呼叫。
