# Skill 根因確認閘門報告

## 任務資訊

- 處理路徑: `optimize`
- 目標 Skills: `tdd-e2e-green`（主）、`task-plan`、`implement`（handoff）
- 使用者問題: Green 不可一次把 US 內全部 Red 做成 all green；每輪只鎖定一支仍紅 Scenario。task 做法須對齊 Red 產出的 e2e test case（按 Scenario 拆格）。

## 預期結果

- `/tdd-e2e-green` 一次呼叫只服務**一支** Scenario（對齊 Red 一格一呼叫），just enough 過該支；附帶變綠可回報但不得當策略。
- `task-*.md` 的 `#### Green` 改為與 Red 相同粒度：每個 `S-n-m` 一格 `/tdd-e2e-green`，不再「讓本 US 既有 Red 全綠」單格打包。
- `/implement` 委派 Green 時帶齊 Scenario ID（同 Red）。

## 現況重演

- Green Rule 1／SKILL 允許一次多支變綠；一次呼叫鎖整個 US。
- task-plan 範例與規則：Green 單格「讓本 US 既有 Red 全綠」；Red 則按 Scenario 多格。
- implement：Green 只傳 US，不強制 Scenario。

## 落差分析

| 預期 | 現況 |
|------|------|
| 一格／一呼叫／一支 Scenario | US 級一呼叫、可多支同綠 |
| task Green 對齊 Red 的 e2e 案例列 | task Green 打包整包 US |

## 根因

- 根因類型: `Contract Mismatch`（執行節奏與 task／Red 契約粒度不一致）
- 改動範圍: `chain rewrite`（`tdd-e2e-green` + `task-plan` + `implement` handoff）
- 失敗原因: Green 與 task 以 US 打包推進，與「一次只過一個失敗測試」及 Red 的 Scenario 粒度衝突。

## 影響範圍

- `.agents/skills/tdd-e2e-green/**`
- `.agents/skills/task-plan/rules/產物結構與章節判準.md`、templates／examples、必要時 validator
- `.agents/skills/implement/rules/步驟執行與委派判準.md`

## 候選刪除項

- 「允許一次多支變綠」條款與「讓本 US 既有 Red 全綠」單格 Green 形狀
- Green「選取下一批仍紅」語意

## 確認閘門

使用者已回「繼續」並交付修訂 Prompt → 依本根因進入編排與落地。
