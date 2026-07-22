# 技術可行性研究：照片相簿整理應用程式

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-21
**狀態**: 草稿

## 決策 1: 採用極簡 Web 前後端分離架構

- **Decision**: 前端使用 `Vite + Vanilla HTML/CSS/JS`；後端使用 `Node.js + Express`
- **Rationale**:
  - 符合 spec 假設「桌面或平板等較適合拖放操作的介面」，本機 Web App 可快速驗證核心互動
  - 前後端分離讓 UI、HTTP API、持久化邊界清楚，後續 data／api／ui-plan 可直接對齊
  - 單機個人應用不需要 SSR 或大型 SPA 框架
- **Alternatives considered**:
  - 單體 SSR（例如 Next.js）：第一版不需要伺服端渲染，反而提高耦合與概念負擔
  - Electron 桌面原生：超出本期 Web 交付範圍，增加打包與維運成本
  - React／Vue SPA：超出目前需求，增加依賴與狀態管理成本

## 決策 2: 前端不引入 runtime framework，只以 Vite 作為開發／建置工具

- **Decision**: 使用 `Vite` 做開發伺服與建置；瀏覽器執行期不引入 React／Vue 等 framework，也不引入第三方狀態管理或 UI component library；狀態、資料請求、圖片顯示皆用瀏覽器原生能力
- **Rationale**:
  - 核心互動（日期分組列表、拖放、批次上傳、平鋪預覽）可用原生 ES modules 完成
  - 減少 bundle 與學習曲線，讓焦點留在「需求 → 合約 → 實作」
- **Alternatives considered**:
  - 狀態管理函式庫（Redux／Pinia 等）：單頁小應用價值低
  - UI component library：削弱對原生 DOM／CSS 基礎的聚焦

## 決策 3: 主頁相簿重排使用原生 Drag and Drop，且僅限同日期分組內

- **Decision**: 主頁先依相簿 `created_at`（建立日期）分組顯示；同分組內相簿排序使用原生 `HTML Drag and Drop API` 調整並持久化 `sort_order`；不引入第三方排序庫
- **Rationale**:
  - 對齊 spec 澄清決策「依相簿建立日期分組」（US2-FR2）
  - 組內重排可與日期分組共存，避免跨組拖放造成分組語意混亂
  - 原生 API 足以表達 DOM 事件與 `sort_order` 寫回，較易對應 api-plan／ui-plan
- **Alternatives considered**:
  - 全列表自由拖放、打散日期分組：與「主頁依日期分組」衝突
  - SortableJS：額外依賴，且隱藏核心排序邏輯
  - 自訂 Pointer Events 手勢：實作成本相對需求過高

## 決策 4: 後端使用最小必要套件處理上傳、格式驗證與縮圖

- **Decision**: 核心套件採用 `express`、`multer`、`better-sqlite3`、`sharp`；上傳時驗證 JPG／PNG／HEIC 格式；`sharp` 產生平鋪預覽縮圖；縮圖失敗時仍保留原圖可預覽路徑，`thumbnail_uri` 可為空並降級顯示
- **Rationale**:
  - `express`：成熟、最小的 HTTP API 框架，對齊後續 api-plan endpoint 契約
  - `multer`：簡化 `multipart/form-data` 批次照片上傳（對齊 US1-FR3）
  - `better-sqlite3`：本機關聯式儲存，無需獨立 DB 服務
  - `sharp`：產生縮圖並處理 HEIC 轉換（視平台能力）；支撐 US4 平鋪預覽效能
- **Alternatives considered**:
  - ORM（Prisma／TypeORM）：第一版表結構單純，抽象層收益低
  - `mysql2`／獨立 MySQL：與「單機本機資料」假設不符
  - 不產縮圖、直接載原圖：大量照片平鋪時效能與記憶體風險高

## 決策 5: 照片實體檔與中繼資料分離；一照片僅屬一相簿

- **Decision**:
  - 中繼資料（相簿、照片歸屬、排序、建立日期）存 SQLite
  - 匯入時將原始檔複製至 app-managed 目錄，並在該目錄產生縮圖
  - 每張照片以 `album_id` 外鍵指向單一相簿（1:N），對齊 spec 假設「每張照片同一時間只會屬於一個相簿」
- **Rationale**:
  - 二元大檔不適合塞進 DB blob；集中管理可支撐備份與平鋪預覽
  - 1:N 模型比 M:N 簡單，直接對齊 US1 驗收情境「照片只出現在指定相簿」
  - 複製原檔進 app 目錄，避免使用者移動本機檔案後預覽失效
- **Alternatives considered**:
  - 全部存 DB BLOB：備份／預覽／除錯成本高
  - 只記錄 `source_path` 不複製：使用者移動檔案後預覽可能失效
  - M:N 多相簿歸屬：與 spec 假設衝突，增加 API 與 UI 複雜度

## 假設

- 第一版為單機個人應用；技術選型以本機可跑、少依賴為優先
- 決策 3 的「僅組內重排」為低風險第一版假設（spec 未明確跨組拖放規則）
- HEIC 解析依 `sharp` 平台能力；若某環境不支援 HEIC，可在 API 回傳明確錯誤（對齊 US1 邊界情境）
- 第一版不做登入、雲端同步、跨裝置或多人共享
