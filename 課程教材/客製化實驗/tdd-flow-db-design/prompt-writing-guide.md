# Prompt 撰寫規範：後端掛上「資料庫設計」流程節點

**實驗路徑**: `Skill`
**對應課堂實驗**: C（獨立「資料庫設計」章；全後端一次；US 仍 R→G→R）
**建立日期**: 2026-07-30
**狀態**: 待 Review

## 規範目的

Skill 路徑只設計「給使用者呼叫 `/skill-engineering`」的條列 Prompt。執行者**不能**直接改 skill 流程／檔案；改 skill 一定走 skill-engineering，由使用者下指令。

## 適用範圍

- 主目標 skill：`.agents/skills/task-plan/`
- Prompt 入口：使用者呼叫 `/skill-engineering` 並貼上正式 Prompt
- **禁止**：把 skill 當 Artifact 直接改；禁止執行者代改正式 skill

## 撰寫原則

1. 開頭：「請呼叫 `/skill-engineering`，目標 skill 為…，本次是優化既有 skill，符合以下規範：」
2. 條列只寫**意圖與目的**；不寫「要改哪些檔／實際改哪些東西」。
3. 規範與正式 Prompt 分開；正式 Prompt 以對話確認版為準。

## 必須鎖住的範圍

- 入口是 `/skill-engineering`，使用者下指令
- 意圖：後端多一個獨立的資料庫設計流程章節（進 Red 前、全後端一次）
- 目的：產出可落地的資料表／物理設計，不是環境雜項裡的複製檔儀式
- 不改各 US 的 R→G→R 節奏

## 避免寫法

- 羅列必改 `rules/`／`templates/`／`validator`／逐檔對齊清單
- 「直接改 SKILL.md」或「將此 Artifact 修改…」
- 做成每 US Schema、新建 `/tdd-db-design`、只改 Green／Red 執行方法

## 本輪正式 Prompt（請使用者下）

請呼叫 `/skill-engineering`，目標 skill 為 `.agents/skills/task-plan/`。本次是優化既有 skill，符合以下規範：

1. 後端實作計畫要有一個**獨立的「資料庫設計」章節**（不要塞在環境建立雜項裡），放在進 User Story／Red 之前；目的是產出可落地的資料表設計（物理模型），而不是只複製既有檔案過關。
2. 該章以系統分析的**邏輯資料模型**為輸入意圖；完成條件要看得出設計意圖與關鍵取捨，並足以支撐後續落地與驗證——不是「檔案存在即可」。
3. 各 User Story 仍維持 Red → Green → Refactor；不要做成每個 US 重做一輪資料庫設計。

## Review 停等

請確認或修改本規範與上方正式 Prompt。確認後請**使用者**自行下 `/skill-engineering`；本實驗執行者不會直接改 `task-plan`。
