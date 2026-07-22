# 技術可行性研究：照片相簿整理應用程式

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-22
**狀態**: 草稿

## 決策 1: 採用極簡 Web 前後端分離架構

- **Decision**: 前端使用 `Vite + Vanilla HTML/CSS/JS`；後端使用 `Node.js + Express`
- **Rationale**:
  - 符合單機個人、教學友善、套件少、責任清楚的約束
  - 前後端分離讓 UI、HTTP API、持久化邊界清楚，後續 data／api／ui-plan 可直接對齊
  - 規格假設以桌面／平板拖放為主，本機 Web（`localhost`）即可覆蓋，無需桌面殼
- **Alternatives considered**:
  - 單體 SSR（例如 Next.js／Nuxt）：第一版不需要伺服端渲染，反而提高耦合與概念負擔
  - React／Vue SPA：超出目前需求與教學目標，增加依賴與狀態管理成本
  - Electron／Tauri：規格未要求安裝型桌面 App，會擴大整合與打包範圍

## 決策 2: 前端不引入 runtime framework，只以 Vite 作為開發／建置工具

- **Decision**: 使用 `Vite` 做開發伺服與建置；瀏覽器執行期不引入 React／Vue 等 framework，也不引入第三方狀態管理或 UI component library；狀態、資料請求、圖片顯示皆用瀏覽器原生能力
- **Rationale**:
  - 核心互動（日期分組列表、拖放、多檔上傳、平鋪預覽）可用原生 ES modules 完成
  - 減少 bundle 與學習曲線，讓焦點留在「需求 → 合約 → 實作」
- **Alternatives considered**:
  - 狀態管理函式庫（Redux／Pinia 等）：單頁小應用價值低
  - UI component library：削弱對原生 DOM／CSS 基礎的聚焦

## 決策 3: 主頁相簿重排使用原生 Drag and Drop，且僅限同建立日分組內

- **Decision**: 主頁先依相簿 `created_at`（建立日期）分組顯示；同分組內使用原生 `HTML Drag and Drop API` 調整並持久化 `sort_order`；不引入第三方排序庫；不允許跨日期分組拖放改變分組
- **Rationale**:
  - 對齊已澄清規格：分組依據是相簿建立日期，不是拍攝日；拖放不應改寫 `created_at`
  - 「組內排序」讓日期分組與自訂順序可共存，避免與 US2 衝突
  - 原生 API 足以表達 DOM 事件與 `sort_order` 寫回，較易對應 api-plan／ui-plan
- **Alternatives considered**:
  - 全列表自由拖放、打散日期分組：與「主頁依建立日期分組」衝突
  - SortableJS：額外依賴，且隱藏核心排序邏輯
  - 自訂 Pointer Events 手勢：實作成本相對需求過高

## 決策 4: 後端使用最小必要套件處理上傳與縮圖（不引入 EXIF）

- **Decision**: 核心套件採用 `express`、`multer`、`better-sqlite3`、`sharp`；不引入 `exifr`；上傳後以檔案內容驗證僅接受 JPEG／PNG／WebP；縮圖失敗時仍保留原圖路徑，`thumbnail_path` 可為空並降級顯示
- **Rationale**:
  - `express`：成熟、最小的 HTTP API 框架，對齊後續 api-plan
  - `multer`：簡化 `multipart/form-data` 多檔上傳（US1-FR3）
  - `better-sqlite3`：本機關聯式儲存，無需獨立 DB 服務
  - `sharp`：產生平鋪預覽縮圖，並可輔助驗證影像格式
  - 主頁分組依相簿建立日期，規格無自動成冊／拍攝日需求，故 `exifr` 非必要
- **Alternatives considered**:
  - ORM（Prisma／TypeORM）：第一版表結構單純，抽象層收益低
  - `mysql2`／獨立 MySQL：與單機本機資料假設不符
  - `exifr`：本期分組與歸屬都不依賴拍攝日，屬多餘依賴
  - 缺縮圖就拒絕匯入：過嚴，阻礙「先整理進相簿」核心路徑

## 決策 5: 照片實體檔與中繼資料分離；匯入複製進 app 目錄；相簿—照片採 1:N

- **Decision**:
  - 中繼資料（相簿、歸屬、排序、建立日期）存 SQLite
  - 匯入時將原檔複製至 app-managed 目錄，並另產縮圖檔；DB 存相對路徑
  - `photos.album_id` 外鍵落實「一張照片同一時間只屬於一個相簿」；改歸屬以 `UPDATE` 移動，不採 M:N
  - 相簿表不設 `parent_id`，結構上禁止巢狀（GR-001）
- **Rationale**:
  - 二元大檔不適合塞進 DB blob；縮圖集中管理可支撐平鋪預覽
  - 複製進 app 目錄避免外部來源檔移動／刪除導致預覽失效
  - 單外鍵模型直接對齊已澄清的 GR-002，移動語意清楚
- **Alternatives considered**:
  - 全部存 DB BLOB：備份／預覽／除錯成本高
  - 只記錄外部 `source_path` 不複製：來源檔失效風險高
  - M:N `album_photos`：與已澄清「單相簿歸屬」衝突
  - 純檔案＋JSON：難以穩定表達外鍵與排序約束

## 決策 6: 本期零外部整合；本機以同 origin／proxy 串接 API 與媒體

- **Decision**: 不整合雲端相簿、OAuth 或裝置 Photos SDK；匯入僅用瀏覽器檔案選擇器；開發期以 Vite proxy 轉發 `/api` 與 `/media`；本機執行時由 Express 同 origin 提供靜態前端、REST API 與媒體檔
- **Rationale**:
  - 規格為單機個人、無登入／雲端同步，外部整合無本期價值
  - 同 origin／proxy 可避免 CORS 與 `<img>` 跨域問題，縮圖與原圖一律經 HTTP URL 取得
- **Alternatives considered**:
  - 分 port + `cors` 作為預設正式模式：可行但增加設定與除錯成本
  - 前端直接讀 `file://` 或本機絕對路徑：瀏覽器安全模型不允許，且無法穩定預覽

## 假設

- 第一版為單機個人應用；技術選型以本機可跑、少依賴為優先
- 決策 3 的「僅同建立日分組內重排」為低風險第一版假設（規格未要求跨組規則）
- 開發期可選用 `cors` 作為備援，但預設以 Vite proxy 為準
- 刪除相簿時採 cascade 刪除所屬照片與實體檔（規格未另定；低風險預設）
- 平板觸控對原生 HTML5 DnD 支援有限；第一版仍以原生 DnD 為準，必要時再評估排序庫
