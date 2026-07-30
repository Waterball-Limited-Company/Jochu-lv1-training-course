# 開發規範（憲法）：Jochu Lv1 訓練專案

**建立日期**: 2026-07-30
**最後修訂**: 2026-07-30
**狀態**: 生效
**版本**: `1.0.0`

本檔為專案根目錄之專案級開發規範（憲法）：約束實際開發與交付產物如何分析、如何實作。不含單一功能需求，亦不含具體 API path、畫面欄位或單一 User Story。

## 核心原則

- MUST：實作可回溯至已核可之功能規格（`spec.md`）；規格未涵蓋之行為不得擅自加入實作。
- MUST：發現規格缺漏或矛盾時，先修訂規格或經 `/clarify` 拍板再繼續，不得僅在程式碼中即興決定。
- MUST：依賴與架構抽象維持達成需求所必需之最小範圍；引入新依賴或額外抽象層 MUST 有正當理由。
- MUST：前後端（若皆存在）以明確契約整合；前端不得以旁路方式存取資料儲存（例如直連資料庫）。
- MUST：功能需求與關鍵路徑 MUST 可客觀驗證（自動化測試、可重現手動步驟或其他約定驗證方式）。

## 技術約束

- **專案結構**：採 monorepo；應用原始碼以 `backend/`、`frontend/` 分置（若本期範圍僅單一端，未列範圍之端可不建立，但不得改用未約定之其他根結構）。
- **後端基線**（本期若含後端）：Node.js + Express。
- **資料存取**（本期若含後端與持久化）：
  - MUST：以官方 PostgreSQL driver（`pg` 或同等官方 driver）+ 手寫 SQL 存取資料。
  - MUST NOT：使用完整 ORM（含 Prisma、TypeORM、Sequelize 等）。
  - MUST NOT：引入第三方 SQL query builder（含 Knex、Kysely 等）；參數綁定與 SQL 組裝由應用碼自行完成。
- **前端基線**（本期若含前端）：Vite 作為開發／建置工具；執行期 MUST NOT 引入 React、Vue、Angular 等 UI framework（原生 JS／TS 與必要之輕量工具可接受）。
- **資料儲存**（本期若含持久化）：
  - MUST：應用資料以單一資料庫為真相來源。
  - MUST：應用主庫引擎為 PostgreSQL；本機開發以 Docker 執行 PostgreSQL 為準（亦允許本機安裝，但不得改用其他引擎）。
  - MUST NOT：以 SQLite、MySQL 或其他引擎作為應用主庫。
- **時間與時區**：
  - MUST：對外顯示與「營業日／可預約時段」等業務日曆語意，以 `Asia/Taipei` 解讀。
  - MUST：表示「某一瞬間」之持久化欄位統一使用 `TIMESTAMPTZ`，以 UTC 瞬間存入；應用層負責進出時轉換為 `Asia/Taipei` 顯示或業務規則解讀。
- **整合方式**（若本期含前後端）：
  - MUST：前後端僅以 REST API 為唯一整合介面。
  - MUST NOT：使用 GraphQL；前端 MUST NOT 直連資料庫。
  - MUST NOT：第一版引入 message queue。
- **API 錯誤回應**：對外錯誤回應 MUST 具備專案級一致形狀，至少固定包含 `error.code` 與 `error.message`；個別 endpoint 欄位細節由該功能之 `api-plan` 定之，不在本檔展開。
- **資源 ID**：對外 API 之資源識別 MUST 為字串型穩定 ID，且一律為 UUID；MUST NOT 將可預測之自增整數作為對外主鍵曝露。DB 可用 `UUID` 型別或等價字串欄位，對外契約以字串呈現。
- **設定與機密**：連線字串與機密資訊 MUST 經環境變數或同等機制注入；MUST NOT 將機密寫入原始碼或提交至版本控制。
- **目標環境**：以本機開發與現代 evergreen 瀏覽器為預設場景，除非本檔或功能規格另有約定。

## 流程與品質規範

- MUST：功能依 Artifact-First 流程推進：規格 → 系統分析產物 → `e2e-test-plan` → `task-plan` → 實作；不得跳過已約定之必要產物，直接交付無追溯之實作。
- MUST：涉及 API 或資料模型之變更，MUST 先更新對應系統分析產物（如 `api-plan`／`data-plan`／`DDL`），再改動實作。
- MUST：若採 TDD 實作路徑，遵守 Red → Green → Refactor；Red 僅允許符合預期之失敗，不得以環境錯誤充數。
- MUST：進入實作與交付前，產出與實作 MUST 可對齊本開發規範；已知違規不得默默忽略（應修訂產物／實作，或依程序修訂本檔）。
- SHOULD：規格一致性分析（`analyze`）將違反本規範 MUST 條文者視為高嚴重項目。

## 憲法規範效力

- 本規範優先於各 skill 之預設慣例；衝突時以本規範為準。
- 本檔由人工編輯或 `/constitution` 建立／修訂；修訂時 MUST 更新「最後修訂」，語意變更時 MUST 升「版本」（錯字／措辭澄清可僅更新日期）。
- V1 不要求修訂本檔時同步修改其他 skill 或 templates；相依流程之日後掛接另行為之。
- 交付向 skill 若約定讀取本檔：有本檔則 MUST 遵守；若專案根目錄不存在本檔，依專案約定為警告後繼續（不因缺檔而強制中止）。
