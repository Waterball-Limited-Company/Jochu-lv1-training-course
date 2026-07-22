# 系統分析：照片相簿整理應用程式

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-22
**狀態**: 草稿

## 摘要

### 規格功能概述

本功能是單機個人用的照片相簿整理應用：使用者可手動建立單層相簿並命名；可一次多選匯入 JPEG／PNG／WebP 照片加入指定相簿；同一張照片同一時間只屬於一個相簿，改歸屬時為移動；主頁依相簿建立日期分組瀏覽，並可在同一日期分組內以拖放重排順序且持久化；進入相簿後以平鋪介面預覽縮圖（含空狀態）；相簿不可巢狀；第一版不做登入、雲端同步與多人共享。

### 技術選型概述

技術選型採極簡 Web 前後端分離：前端以 `Vite + Vanilla HTML/CSS/JS`（執行期零 framework，原生 fetch／DOM／Drag and Drop）；後端以 `Node.js + Express` 提供 REST API；中繼資料以本機 `SQLite`（`better-sqlite3`）為單一真相來源，原檔複製至 app-managed 目錄、縮圖由 `sharp` 產生；上傳用 `multer`；不引入 EXIF 解析（分組依相簿建立日期）。細節決策見同 package 的 `system-analyze/technical-research.md`。

## 技術背景

### Language/Version

- Backend：Node.js 20 LTS（實作暫定；與 research 之 Node.js 選型對齊）
- Frontend：ES2022 vanilla JavaScript（實作暫定；對齊「原生 ES modules」決策）

### Primary Dependencies

- Backend：`express`、`multer`、`better-sqlite3`、`sharp`
- Backend（可選）：`cors`（僅在未使用 Vite proxy 的分 port 開發時需要；非 research 強制項）
- Frontend：`Vite`（僅開發／建置依賴）；執行期零 runtime 依賴

### Storage

- SQLite（本機檔，語意對齊後續 `system-analyze/DDL.md`）
- 照片原檔：複製至 app-managed 目錄，DB 存相對路徑
- 縮圖：寫入 app-managed 目錄，供平鋪預覽
- 相簿—照片：`photos.album_id` 一對多（1:N）

### Testing

- Backend：Node.js 內建 `node:test`（API 合約／整合測試；實作暫定）
- Frontend／端到端：以同 package 的 `e2e-test-plan.md` 與手動驗收為主
- 規格層：`e2e-test-plan.md` 作為端到端情境來源

### Target Platform

- 現代 evergreen 瀏覽器
- 主要場景：本機開發與單機使用（`localhost`）
- 互動假設：桌面或平板等較適合拖放的介面

### Project Type

- Web application
- Monorepo：`backend/` + `frontend/`

### Performance Goals

- 建立相簿、匯入照片、組內拖放重排、平鋪預覽等操作，目標在約 1 秒內反映於 UI（實作暫定體驗目標）
- 單使用者；不要求高併發

### Constraints

- 最小依賴：前端不引入 React／Vue 等 framework；後端不引入 ORM；不引入 EXIF 套件
- 前後端僅透過 REST API 溝通；前端不得直連資料庫
- 優先使用平台原生能力（含 HTML Drag and Drop）
- 相簿單層、不可巢狀；一張照片同一時間只屬於一個相簿
- 第一版不做登入、雲端同步、跨裝置或多人共享

### Scale/Scope

- 單使用者／個人情境
- 資料量：數十至數百本相簿、數百至數千張照片（教學／個人整理規模）
- 架構：前後端分離的單頁 Web App（SPA）

## 專案結構

### 文件（本功能）

```text
specs/001-photo-albums/
├── plan.md                          # 本檔（技術研究後總覽：Tech stack + 專案結構）
├── spec.md                          # 功能規格（/specify）
├── e2e-test-plan.md                 # E2E 測試計畫（後續）
├── spec-mapping-checklist.md        # specify 對齊檢查
├── system-analyze/
│   ├── technical-research.md        # 技術可行性研究（詳細 Decision／Rationale／Alternatives）
│   ├── data-plan.md                 # 資料實體合約（按需）
│   ├── DDL.md                       # ERD／設計脈絡／DDL（有 DB 時）
│   ├── api-plan.md                  # API 合約（按需）
│   └── ui-plan.md                   # UI 合約（按需）
└── task-plan/
    └── tdd-e2e-red.md               # 任務／TDD 計畫（後續）
```

### 原始碼（儲存庫根目錄）

```text
backend/
├── src/
│   ├── app.js                       # Express app 組裝（middleware、路由掛載）
│   ├── server.js                    # 啟動進入點（讀取環境變數、監聽埠）
│   ├── db/
│   │   └── sqlite.js                # better-sqlite3 連線與遷移／開檔
│   ├── models/
│   │   ├── album.js                 # 相簿資料存取（created_at／sort_order）
│   │   └── photo.js                 # 照片資料存取（album_id、路徑、sharp 縮圖）
│   └── routes/
│       ├── albums.js                # 相簿 CRUD、同建立日分組內重排
│       └── photos.js                # 多檔上傳、移動歸屬、相簿內列表（multer 掛在此）
├── db/
│   └── schema.sql                   # albums／photos 初始化
├── data/                            # 本機 runtime 資料（gitignore）
│   ├── app.sqlite
│   ├── uploads/
│   └── thumbs/
├── tests/
│   ├── albums.contract.test.js      # 端點合約測試（node:test）
│   └── photos.integration.test.js
├── .env.example
└── package.json

frontend/
├── index.html                       # 單頁 App 進入點
├── src/
│   ├── main.js                      # 進入點：載入、渲染、事件綁定
│   ├── api.js                       # 以原生 fetch 封裝的 REST 呼叫
│   ├── render.js                    # 主頁建立日分組、相簿平鋪預覽
│   ├── dnd.js                       # 原生 HTML Drag and Drop（同建立日分組內重排）
│   └── styles.css                   # 分組、平鋪預覽、拖放中樣式
├── vite.config.js                   # 開發期 proxy `/api`、`/media`
└── package.json                     # Vite 開發依賴
```

### 結構決策

- 採 monorepo 的 Web application 結構：根目錄分 `backend/`（Node.js + Express）與 `frontend/`（Vite + vanilla）
- 後端以 `models`（資料存取）／`routes`（HTTP 與驗證）分層，維持最小且清楚的職責分離
- 不引入 service 層或 ORM；上傳（`multer`）、縮圖（`sharp`）由對應 `models`／`routes` 直接呼叫
- 前端以功能檔案拆分（`api`／`render`／`main`，必要時加 `dnd`），全部使用原生 API
- 因採 1:N 歸屬，不另設 `album_photos` model／route
