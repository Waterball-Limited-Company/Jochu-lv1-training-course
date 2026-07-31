---
name: implement
description: 依 specs/<plan-package>/task-plan/ 的 task 逐步實作：進場解析 package；若有 analyze-report.md 則讀取，嚴重項硬停確認後才進入範圍選單；§1／§2 親自執行；§3 的 /tdd-e2e-red 按 US 批次委派、green 按 Scenario、refactor 按 US；逐步勾選 checkbox；失敗即停並回報。Use when the user invokes /implement, asks to execute task-plan implementation, or continue from unchecked task items.
disable-model-invocation: true
---

# Implement

執行 `task-plan` 產物的逐步實作編排器：解析 `plan-package`；若有 `analyze-report.md` 則讀取，有嚴重發現則硬停確認；再確認本輪層別範圍與順序後，依對應 `task-*.md` 從第一個未勾項往下做。無 skill 引用的步驟親自落地；標有 `/tdd-e2e-red` 的 Scenario 格改為**同一 US 批次委派**（內部仍一支測一跑）；`/tdd-e2e-green` 為單一 Scenario；`/tdd-e2e-refactor` 為單一 US。成功則勾選進度；失敗則停止並回報，保留已勾項。

# SOP

## Phase 1 -- 解析 package、analyze 閘門並確認本輪範圍

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」，並依其讀取 `.constitution/core.md` 與本 skill 對應憲法（若存在）。
2. THINK 依本次已載入之憲法讀取規則處理缺檔或套用約束：缺檔則警告後繼續；有檔則萃取與本 skill 相關之規範，後續步驟／產出與憲法衝突時以憲法為準。
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

1. READ 讀取 `rules/步驟執行與委派判準.md`、`rules/進度勾選與失敗停止判準.md`，確認親自執行／委派邊界、參數組裝、勾選與失敗停止規則。
2. READ 讀取本輪下一層（或當前層）的 `specs/<plan-package>/task-plan/task-<layer>.md`，定位第一個未勾選項目。
3. THINK 依本次已載入規則判定該步驟為「親自執行」或「委派 tdd skill」，並收斂委派時必傳參數。
4. WRITE 若為親自執行步驟：依 task 指示完成該步（含其驗證指令）。
5. DELEGATE 若為 `/tdd-e2e-red`／`/tdd-e2e-green`／`/tdd-e2e-refactor`：依契約委派對應 skill，傳入必填欄位。
6. THINK 依本次已載入規則判定該步成功或失敗。失敗則停止並進入 Phase 4 回報；成功則繼續。
7. WRITE 成功時將該步在 `task-*.md` 的 checkbox 改為已勾選。
8. THINK 若本層尚有未勾項，回到本 Phase 讀取／執行下一步；若本層完成且還有下一層，切換下一層並重複；若本輪所有層完成，進入 Phase 3。

## Phase 3 -- 完成摘要

1. READ 讀取 `rules/回報與完成摘要判準.md`，確認成功摘要欄位。
2. THINK 依本次已載入規則整理本輪完成層別、已勾進度與後續建議。
3. WRITE 向使用者輸出完成摘要。

## Phase 4 -- 失敗或中止回報

1. READ 若尚未載入，讀取 `rules/回報與完成摘要判準.md`，確認失敗回報欄位。
2. WRITE 依本次已載入規則回報卡點、已完成進度、建議下一步。
