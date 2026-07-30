# 系統分析：內部共享會議室預約系統

**功能分支**: `002-meeting-room-booking`
**建立日期**: 2026-07-30
**狀態**: 草稿

## 摘要

### 規格功能概述

本功能是公司內部共享會議室預約的本機 Web 應用：員工以帳密登入後可瀏覽會議室（名稱、樓層、容納、投影機／視訊、啟用狀態），送出單次預約（用途、預期人數、設備需求）；同一會議室不可有兩筆已確認時段重疊，衝突直接拒絕；可於首頁查看今日各室忙碌，並以日曆與列表檢視預約；可於「我的預約」取消自己的未結束預約。設施管理員可新增／停用會議室並設定維護黑名單時段（停用只擋新約）。第一版不做候補、主管審核、重複預約、與會者邀請、SSO、email 通知與使用率報表；時區與營業語意以 Asia/Taipei 為準。

### 技術選型概述

技術選型對齊專案憲法：monorepo 之 `backend/` + `frontend/`；前端 `Vite + TypeScript` 原生 DOM（無 React／Vue／Angular），日曆原生實作；後端 `Node.js + Express`，`pg` 手寫 SQL，`express-session` + `connect-pg-simple`，`bcrypt` 雜湊；主庫 PostgreSQL（Docker），`TIMESTAMPTZ` + UUID，預約以交易與 partial exclusion 防超賣；開發期 Vite proxy `/api`，無 GraphQL／MQ／Redis／第三方通知。細節決策見同 package 的 `system-analyze/technical-research.md`。

## 技術背景

### 使用語言／版本

- Backend：Node.js LTS（實作時鎖定於 `package.json`）
- Frontend：TypeScript（Vite 建置）+ 原生 DOM API

### 主要依賴

- Backend：`express`、`pg`、`bcrypt`、`dotenv`、`express-session`、`connect-pg-simple`
- Backend（可選）：`cors`（僅在未使用 Vite proxy、分 origin 時）
- Frontend：`vite`、`typescript`（開發／建置）；執行期不依賴 UI framework

### 資料儲存

- PostgreSQL（本機 Docker Compose 為準；單一應用主庫）
- 瞬間欄位：`TIMESTAMPTZ`（UTC 存）
- Session 表由 `connect-pg-simple` 使用同一 PostgreSQL
- 假日：本機假日表（或等價種子資料），不接外部 API

### 測試環境

- Backend：Node.js 內建 `node:test`（合約／整合；實作暫定）
- 端到端：同 package `e2e-test-plan.md` + 可重現 seed／重置
- 資料庫：可獨立測試庫或測試前 `TRUNCATE` 後重灌

### 開發平台

- 現代 evergreen 瀏覽器
- 本機開發：`localhost`（Vite + Express + Docker PostgreSQL）

### 專案類型

- Web application（前後端分離）
- Monorepo：`backend/` + `frontend/`

### 效能目標

- 登入、查會議室、建立／取消預約、首頁／日曆／列表切換，目標在一般本機環境約 1 秒內反映於 UI（體驗目標，非硬性 SLA）
- 併發重點：同室重疊時段不得出現兩筆已確認（正確性優先於吞吐）

### 技術約束

- 遵守專案根目錄 `constitution.md`：禁 ORM／query builder、禁 UI framework、禁 GraphQL／MQ、禁 SQLite／MySQL 主庫、機密僅環境變數
- 前後端僅 REST；錯誤回應固定含 `error.code` 與 `error.message`；對外 ID 為 UUID 字串
- 業務日曆與可預約窗以 `Asia/Taipei` 解讀
- 第一版不做 Redis 鎖、email、SSO

### 實作規模／範圍

- 內部多使用者（種子三角色）；主管暫無額外權限
- 資料量：數十間會議室、日常數百筆預約量級（訓練／本機驗證規模）
- 交付：可本機啟動之前後端與關鍵路徑可驗證行為

## 專案結構

### 文件（本功能）

```text
specs/002-meeting-room-booking/
├── plan.md                          # 本檔（技術研究後總覽）
├── spec.md                          # 功能規格（/specify）
├── e2e-test-plan.md                 # E2E 測試計畫（後續）
├── spec-mapping-checklist.md        # specify 語意映射
├── system-analyze/
│   ├── technical-research.md        # 技術可行性研究
│   ├── data-plan.md                 # 資料實體合約
│   ├── DDL.md                       # DDL
│   ├── api-plan.md                  # API 合約
│   └── ui-plan.md                   # UI 合約
└── task-plan/
    ├── task-backend.md
    ├── task-frontend.md
    └── task-integration.md
```

### 原始碼（儲存庫根目錄）

```text
backend/
├── src/
│   ├── app.js                       # Express 組裝（middleware、路由）
│   ├── server.js                    # 啟動進入點
│   ├── db/
│   │   └── pool.js                  # pg Pool 與連線
│   ├── middleware/
│   │   ├── auth.js                  # session 登入檢查
│   │   └── requireRole.js           # 角色閘門
│   ├── models/
│   │   ├── user.js
│   │   ├── room.js
│   │   ├── booking.js               # 含交易內衝突檢查
│   │   ├── maintenance.js
│   │   └── holiday.js
│   ├── lib/
│   │   ├── time.js                  # Asia/Taipei 解讀／轉換
│   │   └── errors.js                # error.code + message
│   └── routes/
│       ├── auth.js
│       ├── rooms.js
│       ├── bookings.js
│       ├── maintenance.js
│       └── overview.js              # 今日忙碌等
├── db/
│   ├── schema.sql                   # DDL 對齊 system-analyze/DDL.md
│   └── seed.sql
├── tests/
├── .env.example
└── package.json

frontend/
├── index.html
├── src/
│   ├── main.ts
│   ├── router.ts
│   ├── api/
│   │   └── client.ts                # fetch + credentials
│   ├── auth/
│   │   └── session.ts
│   ├── lib/
│   │   └── datetime-taipei.ts
│   ├── pages/
│   │   ├── login.ts                 # 登入頁 Login
│   │   ├── home.ts                  # 首頁今日忙碌 Home
│   │   ├── bookings-browse.ts       # 預約瀏覽（日曆／列表切換）BookingsBrowse
│   │   ├── booking-create.ts        # 建立預約 BookingCreate
│   │   ├── my-bookings.ts           # 我的預約 MyBookings
│   │   └── admin-rooms.ts           # 會議室管理 AdminRooms
│   ├── components/
│   └── styles/
├── vite.config.ts                   # /api proxy → Express
└── package.json

docker-compose.yml                   # PostgreSQL 服務
```

### 結構決策

- 採 monorepo 前後端分割；不以其他根結構替代 `backend/`／`frontend/`
- 後端以 `routes` + `models`（手寫 SQL 資料存取）分層；不引入 service 層或 ORM 作為必要架構
- 預約寫入路徑集中在 booking model／交易，避免路由層散落衝突邏輯
- 前端以 pages／components／api 模組拆分；狀態以模組級記憶體 + `/me` 還原，不引入框架狀態庫
- 開發期以 Vite proxy 整合 REST，維持前端不直連 DB
