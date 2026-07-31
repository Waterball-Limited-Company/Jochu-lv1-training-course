# Skill 路徑 Phase 4／5 筆記：改 Green 推進節奏

**實驗路徑**: `Skill`  
**日期**: 2026-07-30  
**狀態**: skill-engineering 已由使用者下指令並落地（見下）

## Phase 4

- 使用者修訂 Prompt 後呼叫 `/skill-engineering`，目標 `.agents/skills/tdd-e2e-green/`，並要求 task 對齊 Red 的 e2e Scenario 粒度。
- 本筆記不代替直接改 skill；改動經 skill-engineering 鏈完成。

## Phase 5 — 驗證紀錄摘要

**驗證目標**: Green 一次一格一支 Scenario；禁止整包 US all-green；task／implement handoff 對齊；validator 強制 Green＝Red Scenario 集合。

**結論**: 通過（鏈上已改）

**已證明可修改**:
- `tdd-e2e-green`：Scenario 級契約；移除多支同綠策略
- `task-plan`：Green 按 `S-n-m` 一格（rules／examples）；`validate_task_plan_output.py` 拒絕「全綠」單格並要求與 Red／e2e 對齊
- `implement`：Green 委派帶 Scenario

**已知債**: 既有 `specs/*/task-plan/` 產物若仍為舊「全綠」單格，`validate_task_plan_output.py` 會 FAIL，需另行重跑 `/task-plan` 才會換成新形狀。
