---
name: core
applies_to:
  - analyze
  - api-plan
  - data-plan
  - e2e-test-plan
  - implement
  - ooa-plan
  - specify
  - system-analyze
  - task-plan
  - technical-research
  - tdd-e2e-green
  - tdd-e2e-red
  - tdd-e2e-refactor
  - ui-plan
---

# 開發規範（憲法）：Jochu Lv1 訓練專案

**建立日期**: 2026-07-31
**最後修訂**: 2026-07-31
**狀態**: 生效
**版本**: `2.3.0`

## 核心原則

（本版無額外核心原則；架構與堆疊邊界見「技術約束」。）

## 技術約束

- MUST：應用採 monorepo；原始碼以 `backend/`、`frontend/` 分置（本期若僅單一端，未列範圍之端可不建立，但不得改用未約定之其他根結構）。
- MUST：後端（若本期含後端）為 Node.js + Express。
- MUST：資料存取（若本期含後端與持久化）使用官方 PostgreSQL driver（`pg` 或同等）+ 手寫 SQL；MUST NOT 使用完整 ORM；MUST NOT 引入第三方 SQL query builder。
- MUST：前端（若本期含前端）以 Vite 為開發／建置工具；執行期 MUST NOT 引入 React、Vue、Angular 等 UI framework。
- MUST：應用資料以單一 PostgreSQL 為真相來源；MUST NOT 以其他引擎作為應用主庫。
- MUST：前後端（若皆存在）僅以 REST API 為唯一整合介面；前端 MUST NOT 直連資料庫；MUST NOT 使用 GraphQL；MUST NOT 於第一版引入 message queue。
- MUST：連線字串與機密經環境變數或同等機制注入；MUST NOT 將機密寫入原始碼或提交至版本控制。

## 憲法規範效力

- 本規範與同目錄各 skill 憲法，優先於各 skill 之預設慣例；衝突時以憲法為準。`core` 與 skill 憲法衝突時以 `core` 為準。
- 本檔由人工編輯或 `/constitution` 建立／修訂；修訂時 MUST 更新「最後修訂」，語意變更時 MUST 升「版本」。
- 交付 skill 若約定讀取本檔：有則 MUST 遵守；若 `.constitution/core.md` 不存在，依專案約定警告後繼續。
