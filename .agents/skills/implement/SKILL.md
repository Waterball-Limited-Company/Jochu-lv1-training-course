---
name: implement
description: 依 specs/<plan-package>/task-plan/ 的 task 逐步實作：進場解析 package 並以選單確認範圍／順序；§1／§2 等無 skill 引用步驟親自執行；§3 的 /tdd-e2e-red|green|refactor 委派並組裝參數；逐步勾選 checkbox；失敗即停並回報。Use when the user invokes /implement, asks to execute task-plan implementation, or continue from unchecked task items.
disable-model-invocation: true
---

# Implement

執行 `task-plan` 產物的逐步實作編排器：解析 `plan-package`、確認本輪層別範圍與順序後，依對應 `task-*.md` 從第一個未勾項往下做。無 skill 引用的步驟親自落地；標有 `/tdd-e2e-red`／`/tdd-e2e-green`／`/tdd-e2e-refactor` 的步驟委派並傳入契約參數。成功則勾選進度；失敗則停止並回報，保留已勾項。

# SOP

## Phase 1 -- 解析 package 並確認本輪範圍

1. READ 讀取使用者輸入與當前上下文，確認是否已帶 `plan-package` 或範圍選項。
2. READ 讀取 `rules/進場package與範圍契約.md`，確認 package 解析與範圍選單規則。
3. THINK 依本次已載入規則解析 `plan-package`；若零個可選 package，停止並進入 Phase 4 回報。
4. READ 若需使用者從多個 package 中選擇，讀取 `templates/implement-package-round.md` 與 `templates/implement-package-round.example.md`。
5. WRITE 若 package 尚未確定，依 package 骨架在對話中列出候選並等待回答；未回答前停止。
6. THINK 依回答或既有結果鎖定 `plan-package`。
7. READ 讀取 `templates/implement-scope-round.md` 與 `templates/implement-scope-round.example.md`。
8. WRITE 若範圍／順序尚未拍板，依範圍骨架輸出進場選單並等待回答；未回答前停止。
9. THINK 依本次已載入規則與回答收斂本輪層別序列與對應 `task-*.md` 路徑；若不通過，停止並進入 Phase 4 回報。

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
