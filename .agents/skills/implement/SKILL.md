---
name: implement
description: 依 specs/<plan-package>/task-plan/ 逐步實作：後端／前端每個 Scenario 只開一位 Scenario Agent，在同一脈絡跑完 Red、Green、Refactor 與層內全綠閘門；User Story 邊界再跑整層回歸與 API 契約證據；整合只跑停用 Mock 的完全端對端驗收。Use when the user invokes /implement, asks to execute task-plan implementation, or continue from unchecked task items.
disable-model-invocation: true
---

# Implement

執行 `task-plan` 產物的控制面：解析 `plan-package` 與本輪層別；後端／前端以完整 Scenario 區塊為一次委派單位，同一位 Scenario Agent 沿用同一脈絡完成 Red → Green → Refactor → User Story 層內全綠，不在階段間重開代理。`/implement` 親自執行環境步驟、User Story 完成閘門與整合完全端對端驗收，並以 `api-plan.md` 的可機械驗證契約檢查後端、前端 Mock 與整合證據。

# SOP

## Phase 1 -- 解析 package、analyze 閘門並確認本輪範圍

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」（若存在），以及專案根目錄 `constitution.md`（若存在）；缺檔則略過，不報錯。
2. THINK 若已讀到憲法，萃取與本 skill 相關之 MUST，後續步驟／選型／產出與憲法衝突時改依憲法執行；若未讀到，依本 skill 預設規則繼續。
3. READ 讀取使用者輸入與當前上下文，確認是否已帶 `plan-package` 或範圍選項。
4. READ 讀取 `rules/進場package與範圍契約.md`，確認 package 解析與範圍選單規則。
5. THINK 依本次已載入規則解析 `plan-package`；若零個可選 package，停止並進入 Phase 4 回報。
6. READ 若需使用者從多個 package 中選擇，讀取 `templates/implement-package-round.md` 與 `templates/implement-package-round.example.md`。
7. WRITE 若 package 尚未確定，依 package 骨架在對話中列出候選並等待回答；未回答前停止。
8. THINK 依回答或既有結果鎖定 `plan-package`。
9. READ 讀取 `rules/analyze報告進場閘門判準.md`；若存在 `specs/<plan-package>/analyze-report.md` 則 READ 該報告。
10. THINK 依已載入閘門規則判定是否有嚴重發現；無報告則依規則警告後繼續。
11. WRITE 若有嚴重發現：在對話硬停摘要嚴重項並詢問「先修」或「仍要繼續實作」；未獲明示繼續前停止，不進入範圍選單。
12. READ 讀取 `templates/implement-scope-round.md` 與 `templates/implement-scope-round.example.md`。
13. WRITE 若範圍／順序尚未拍板，依範圍骨架輸出進場選單並等待回答；未回答前停止。
14. THINK 依本次已載入規則與回答收斂本輪層別序列與對應 `task-*.md` 路徑；若不通過，停止並進入 Phase 4 回報。

## Phase 2 -- 依層執行 task 步驟

1. READ 讀取 `rules/步驟執行與委派判準.md`、`rules/Scenario代理與驗收閘門判準.md`、`rules/API契約證據閘門判準.md`、`rules/進度勾選與失敗停止判準.md`。
2. READ 讀取本輪下一層的 `task-<layer>.md`，定位第一個未勾選項或尚未完成的 Scenario 區塊。
3. WRITE 若為規格閱讀、環境建立或其他無 TDD 指令的前置步驟，由 `/implement` 依 task 親自執行與驗證；成功後勾選。
4. READ 若為後端／前端 Scenario，讀取 `templates/scenario-agent-handoff.md` 與 `templates/scenario-agent-handoff.example.md`，定位該 Scenario 的 task、e2e、系統分析與 API 契約片段。
5. DELEGATE 為該 Scenario 建立一位 Scenario Agent，傳入完整交接資料；該代理先確認同層、同 User Story 已完成 Scenario 的累積測試基準為綠，再在同一脈絡依序執行 `/tdd-e2e-red`、`/tdd-e2e-green`、`/tdd-e2e-refactor`，最後重跑加入本則後的累積測試與契約證據。不得為各階段另開代理。
6. THINK Scenario Agent 先在原脈絡修復本則造成的累積回歸；四步全部回報成功時，依實際證據勾選該 Scenario 的四個 checkbox。只有超出本則邊界、契約衝突、環境洞或仍無法修復時，才保留已證實進度並停止，不進入下一個 Scenario。
7. READ 到契約證據閘門時，讀取 `templates/api-contract-evidence.json` 與 `templates/api-contract-evidence.example.json`；證據必須由測試產生，不由 `/implement` 手填。
8. RUN 到 `User Story 完成閘門` 時，由 `/implement` 親自執行故事完整測試、該層全套回歸，再以 `--require-source backend-contract` 或 `--require-source frontend-mock` 執行 `scripts/validate_api_contract_evidence.py`，只驗證該故事在目前層必要的契約證據；全部通過才勾選。
9. RUN 若為整合層，先確認同一 User Story 的後端與前端完成閘門都已勾選，再停用 Mock、重設隔離資料、由真實瀏覽器跑完整系統端對端驗收，並以 `--require-source integration` 執行 `scripts/validate_api_contract_evidence.py` 驗證整合證據；失敗依 task 的路由分類，不呼叫 TDD 三階段 skill。
10. THINK 若本層尚有未勾項，回到本 Phase；若本層完成且還有下一層，切換後重複；全部完成則進入 Phase 3。

## Phase 3 -- 完成摘要

1. READ 讀取 `rules/回報與完成摘要判準.md`，確認成功摘要欄位。
2. THINK 依本次已載入規則整理本輪完成層別、已勾進度與後續建議。
3. WRITE 向使用者輸出完成摘要。

## Phase 4 -- 失敗或中止回報

1. READ 若尚未載入，讀取 `rules/回報與完成摘要判準.md`，確認失敗回報欄位。
2. WRITE 依本次已載入規則回報卡點、已完成進度、建議下一步。
