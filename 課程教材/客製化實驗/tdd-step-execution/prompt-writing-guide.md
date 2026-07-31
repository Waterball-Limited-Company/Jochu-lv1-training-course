# Prompt 撰寫規範：改 Green 推進節奏（一次只綠一支）

**實驗路徑**: `Skill`
**對應課堂實驗**: A（允許一次多支變綠 → 每輪只鎖定一支仍紅 Scenario）
**建立日期**: 2026-07-30
**狀態**: 已確認（使用者修訂 Prompt 後已下 `/skill-engineering`）

## 規範目的

Skill 路徑只設計「給使用者呼叫 `/skill-engineering`」的條列 Prompt。執行者**不能**直接改 skill 流程／檔案；改 skill 一定走 skill-engineering，由使用者下指令。

## 適用範圍

- 主目標 skill：`.agents/skills/tdd-e2e-green/`
- 連動：`task-plan`（Green 列對齊 Red 的 e2e Scenario）、必要時 `implement` 委派參數
- Prompt 入口：使用者呼叫 `/skill-engineering` 並貼上正式 Prompt
- **禁止**：把 skill 當 Artifact 直接改；禁止 sub-agent 改正式 skill 或暫定複本冒充完成

## 撰寫原則

1. 開頭：「請呼叫 `/skill-engineering`，目標 skill 為…，本次是優化既有 skill，符合以下規範：」
2. 其後條列大顆粒度要求（風格對齊 Artifact 路徑的條列 Prompt，但入口不是改 Artifact）。
3. 鎖政策與必碰鏈（green＋task），少寫逐行替換；閘門交 skill-engineering。
4. 規範與正式 Prompt 分開；正式 Prompt 以使用者修訂版為準。

## 必須鎖住的範圍

- 入口是 `/skill-engineering`，使用者下指令
- Green：每輪只鎖定一支仍紅 Scenario；不得以一次綠完全部 Red 為策略
- Task：Green 做法對齊 Red 產出的 e2e test case（按 `S-n-m`）
- 不改 Red／Refactor 本體、全套跑測、just enough（除非鏈上必要薄改）

## 避免寫法

- 「請參照本 run 目錄…直接改 SKILL.md」
- 「將此 Artifact 修改…」套在 skill 上
- 執行者代改 `.agents/skills/tdd-e2e-green/`

## 本輪正式 Prompt（使用者修訂版）

請呼叫 `/skill-engineering`，目標 skill 為 `.agents/skills/tdd-e2e-green/`。本次是優化既有 skill，符合以下規範：

1. 把 Green 做法改成：從一次實作全部 Red 測試案例變 all green，改為每一輪內部迴圈只鎖定**一支**仍紅 Scenario 作為實作目標，不得超過（對齊「一次只過一個失敗測試」）。
2. 連 task 的做法也需要改成對齊 Red 產出的 e2e test case（Green 按 Scenario 一格，禁止整包 US「全綠」單格）。

## Review 停等

本 Prompt 已由使用者下達並完成 skill-engineering 落地；見 `skill-eng-validation.md`。
