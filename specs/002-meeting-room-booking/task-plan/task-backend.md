# 實作計畫（後端）：內部共享會議室預約系統

**功能分支**: `002-meeting-room-booking`  
**建立日期**: 2026-07-30  
**狀態**: 草稿

---

## 1. 規格閱讀

- [x] 已讀 `plan.md`（Node.js + Express、`backend/` 結構、PostgreSQL、`node:test`）
- [x] 已讀 `system-analyze/technical-research.md`（`pg` 手寫 SQL、bcrypt、PostgreSQL session、交易與 exclusion）
- [x] 已讀 `system-analyze/DDL.md`（`users`、`rooms`、`holidays`、`bookings`、`maintenance_windows` 與約束）
- [x] 已讀 `system-analyze/api-plan.md`（REST endpoint、狀態碼、回應形狀與錯誤碼）
- [x] 已讀 `e2e-test-plan.md` 的 `## 後端` 全部 Scenario
- [x] 已讀專案根目錄 `constitution.md`（禁 ORM／query builder、PostgreSQL Docker、session、時間與 REST 約束）
- [x] 確認後端 Scenario ID 與本計畫逐一對齊，且沒有 blocked 項

```bash
ls specs/002-meeting-room-booking/plan.md \
   specs/002-meeting-room-booking/system-analyze/technical-research.md \
   specs/002-meeting-room-booking/system-analyze/DDL.md \
   specs/002-meeting-room-booking/system-analyze/api-plan.md \
   specs/002-meeting-room-booking/e2e-test-plan.md \
   constitution.md
```

---

## 2. 環境建立

### 2.1 工具與目錄

- [x] 確認本機 Node.js 為現行 LTS，Docker 與 Docker Compose 可執行；以 `package.json` 的 `engines.node`（可搭配 `.nvmrc`）鎖定本期 Node.js LTS 版本

```bash
node -v
docker --version
docker compose version
```

- [x] 建立 `backend/` 骨架（對齊 `plan.md`：`src/db`、`src/middleware`、`src/models`、`src/lib`、`src/routes`、`db`、`tests/helpers`；`app.js` 可被 import，暫不實作業務 handler）

```bash
mkdir -p backend/src/db backend/src/middleware backend/src/models \
  backend/src/lib backend/src/routes backend/db backend/tests/helpers
ls -ld backend backend/src backend/src/db backend/src/middleware \
  backend/src/models backend/src/lib backend/src/routes backend/db backend/tests
```

- [x] 在儲存庫根目錄準備 `docker-compose.yml` 的 PostgreSQL 服務，並確認 `.gitignore` 至少忽略 `node_modules/`、`.env` 與本機測試輸出

### 2.2 套件與腳本

- [x] 初始化 `backend` 為 ESM，安裝 runtime 依賴 `express`、`pg`、`bcrypt`、`dotenv`、`express-session`、`connect-pg-simple`
- [x] 不安裝 ORM 或 query builder；UUID 使用 Node.js 內建 `crypto.randomUUID()`
- [x] 設定 `package.json` 的 `type` 為 `module`、`engines.node` 為本期鎖定的 LTS 版本，並讓 `npm test` 執行 `node --test`

```bash
cd backend
npm pkg get type
npm pkg get engines.node
npm pkg get scripts.test
npm ls express pg bcrypt dotenv express-session connect-pg-simple
```

### 2.3 Schema 與環境變數

- [x] 將 `system-analyze/DDL.md` 的完整 SQL 落到 `backend/db/schema.sql`，包含 `btree_gist`、五張應用資料表、索引、外鍵、CHECK 與 `bookings_confirmed_no_overlap`
- [x] 建立 root `docker-compose.yml`，以 PostgreSQL 14+ 容器提供本機主庫；不得改用 SQLite 或 MySQL
- [x] 提供 `backend/.env.example`，列出伺服器埠、`DATABASE_URL`、session secret、cookie／環境設定；真實機密只由環境變數注入
- [x] 準備 schema 與可重現 seed／reset 腳本邊界；session 表交由 `connect-pg-simple` 在同一 PostgreSQL 建立

```bash
ls docker-compose.yml backend/db/schema.sql backend/.env.example
docker compose config
rg "CREATE EXTENSION IF NOT EXISTS btree_gist|CREATE TABLE (users|rooms|holidays|bookings|maintenance_windows)|bookings_confirmed_no_overlap" backend/db/schema.sql
```

### 2.4 測試基建

- [x] 準備 `node:test` 測試基建：可 import Express app、啟停測試伺服器、以內建 HTTP 能力送請求並保留 session cookie
- [x] 準備獨立測試資料庫與 helper：套用 `schema.sql`、依外鍵順序重置資料、灌入三角色使用者／會議室／假日等可重現資料
- [x] 準備測試時間控制邊界，讓 `Asia/Taipei` 的今日、已結束預約、平假日與營業窗案例可重現
- [x] 撰寫最小 smoke：證明 PostgreSQL 容器可連線、schema 可套用、app 可載入與健康檢查可回應；不實作或斷言任何業務 handler

```bash
docker compose up -d postgres
cd backend
npm test
```

---

## 3. User Story 實作計劃

### US-1 登入後瀏覽會議室並完成單次預約（優先級：P1）

#### AC / Edge

- AC-1-1 登入後合法預約應建立為已確認
- AC-1-2 同室重疊時段應被拒絕並提示衝突
- AC-1-3 未登入使用者不得建立預約
- Edge-1-1 清單中的停用會議室必須可被辨識
- Edge-1-2 缺必填欄位或時段無效時拒絕並提示
- Edge-G-1 併發重疊時最多一筆成為已確認
- Edge-G-2 跨日、假日、過短、過長或超出營業窗時拒絕

#### Red

- [x] `/tdd-e2e-red` — S-1-1 登入後建立合法預約並確認:
  - 受測行為：
    - `POST /api/auth/login` 使用有效帳密 → 預期 200 並建立可供後續請求使用的 session
    - `GET /api/rooms` 使用有效 session → 預期 200，回傳包含啟用中的目標會議室及其屬性
    - `POST /api/bookings` 送出用途、人數、設備需求與合法時段 → 預期 201，回傳屬於登入員工且 `status` 為 `confirmed` 的預約
- [x] `/tdd-e2e-red` — S-1-2 拒絕重疊時段並提示衝突:
  - 受測行為：
    - 同室已有 14:00–15:00 的 confirmed 預約時，`POST /api/bookings` 建立 14:30–15:30 預約 → 預期 409
    - 回應為 `BOOKING_CONFLICT` 且說明時段衝突；資料庫不新增第二筆預約
- [x] `/tdd-e2e-red` — S-1-3 未登入不得建立預約:
  - 受測行為：
    - 未帶有效 session 呼叫 `POST /api/bookings` → 預期 401 `UNAUTHENTICATED`
    - 拒絕後不建立任何預約
- [x] `/tdd-e2e-red` — S-1-4 清單可辨識停用會議室:
  - 受測行為：
    - `GET /api/rooms` 使用有效 session → 預期 200
    - 回傳清單同時保留啟用與停用會議室，且每筆以 `is_active` 明確表達是否接受新預約
- [x] `/tdd-e2e-red` — S-1-5 拒絕缺漏或無效預約資料:
  - 受測行為：
    - `POST /api/bookings` 缺少用途、人數、設備需求或起迄，或送出無效時間格式／起迄順序 → 預期 400
    - 回應固定包含 `error.code`、`error.message` 與可修正的欄位或時段原因；不建立預約
- [x] `/tdd-e2e-red` — S-1-6 併發重疊預約最多一筆確認:
  - 受測行為：
    - 兩位已登入員工幾乎同時對同室送出彼此重疊的 `POST /api/bookings`
    - 最多一個請求預期 201 且成為 confirmed；另一個預期 409 `BOOKING_CONFLICT`
    - 最終資料只存在一筆占用該重疊時段的 confirmed 預約
- [x] `/tdd-e2e-red` — S-1-7 拒絕超出可預約日與時段規則:
  - 受測行為：
    - `POST /api/bookings` 分別送出跨日、週末／假日、短於 30 分鐘、長於 4 小時或超出 Asia/Taipei 平日 09:00–21:00 的預約 → 預期 400
    - 回應為 `BOOKING_RULE_VIOLATION` 並指出違反的可預約日或時段規則；不建立預約
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 落地 `POST /api/auth/login` 與 session middleware：以 `pg` 手寫 SQL 查 `users`、bcrypt 驗證密碼、輪替 session ID，並以 `connect-pg-simple` 將 HttpOnly session 存入 PostgreSQL
    - 落地 `GET /api/rooms`：查詢並依樓層、名稱排序所有 rooms，保留停用資料與 `is_active`
    - 落地 `POST /api/bookings`：由 session 決定 `user_id`，集中驗證必填欄位、容量、啟用狀態、Asia/Taipei 平假日／同日／09:00–21:00／30 分鐘至 4 小時與維護重疊
    - 將預約建立集中於 booking model 的 PostgreSQL 交易，鎖定會議室、以半開區間檢查衝突並寫入 UUID／`confirmed`；由 `bookings_confirmed_no_overlap` 收斂併發競爭
    - 對齊 201／400／401／404／409 與 `error.code`、`error.message`；將 exclusion violation 映射為 `BOOKING_CONFLICT`

#### Refactor

- [x] `/tdd-e2e-refactor` — 全綠下整理認證、預約交易、台北時間規則與共通錯誤映射，維持既有契約

---

### US-2 以首頁、日曆與列表掌握會議室預約狀況（優先級：P2）

#### AC / Edge

- AC-2-1 首頁今日概況可區分各室忙碌程度
- AC-2-2 日曆視圖依時段顯示預約
- AC-2-3 列表視圖列出可辨識的預約資訊
- Edge-2-1 今日無預約時呈現可理解空狀態
- Edge-2-2 所選日無預約時日曆與列表顯示空狀態

#### Red

- [x] `/tdd-e2e-red` — S-2-1 今日概況可區分忙碌與空閒:
  - 受測行為：
    - `GET /api/overview/today` 使用有效 session → 預期 200，依 Asia/Taipei 今日回傳每間會議室摘要
    - 有 confirmed 預約的房間回傳非零 `booked_minutes`／`busy_ratio`／`confirmed_booking_count`；全日空閒房間回傳零值
- [x] `/tdd-e2e-red` — S-2-2 同批預約支援日曆與列表檢視:
  - 受測行為：
    - `GET /api/bookings?date={date}` 使用有效 session 查詢有多筆 confirmed 預約的台北日期 → 預期 200
    - 同一 `bookings` 集合依 `starts_at` 排序，包含會議室、時段、預約者與用途摘要，足以供日曆與列表共用
- [x] `/tdd-e2e-red` — S-2-3 今日無預約仍回傳可理解概況:
  - 受測行為：
    - 今日所有房間皆無 confirmed 預約時呼叫 `GET /api/overview/today` → 預期 200
    - `rooms` 仍包含每間會議室，且各室預約筆數、占用分鐘與忙碌比例皆為 0
- [x] `/tdd-e2e-red` — S-2-4 所選日期無預約時回傳空集合:
  - 受測行為：
    - `GET /api/bookings?date={date}` 查詢沒有 confirmed 預約的日期 → 預期 200
    - 回應保留 `date`、`timezone` 並回傳空 `bookings` 陣列，不將無資料視為錯誤
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 落地 `GET /api/overview/today`：以 Asia/Taipei 算今日 UTC 邊界，手寫 SQL 將 rooms 與 confirmed bookings 聚合，所有房間皆輸出，無預約與週末／假日安全回零值
    - 落地 `GET /api/bookings?date={date}`：驗證台北日曆日與可選 `roomId`，只查 confirmed，關聯 room／user 顯示欄位並依開始時間、會議室名稱排序
    - 維持日曆與列表共用單一查詢回應；無資料回 200 與空集合，不另建 Overview 資料表
    - 沿用 session 保護與共通 400／401／404 錯誤形狀

#### Refactor

- [x] `/tdd-e2e-refactor` — 全綠下整理台北日期邊界、查詢投影與零值聚合，避免日曆／列表資料邏輯分岔

---

### US-3 查看並取消自己的預約（優先級：P3）

#### AC / Edge

- AC-3-1 我的預約列出目前使用者自己的紀錄
- AC-3-2 取消後釋放時段且他人可成功預約
- AC-3-3 使用者不可取消他人的預約
- Edge-3-1 無自己的預約時顯示可理解空狀態
- Edge-3-2 已結束或已取消預約不可再取消成功

#### Red

- [x] `/tdd-e2e-red` — S-3-1 我的預約只列出本人紀錄:
  - 受測行為：
    - 員工 A 使用有效 session 呼叫 `GET /api/bookings/mine` → 預期 200
    - 回應只含 A 的 confirmed／cancelled 預約，不含其他使用者紀錄，並依 `starts_at` 降冪排列
- [x] `/tdd-e2e-red` — S-3-2 取消後釋放時段供他人預約:
  - 受測行為：
    - 員工 A 對自己的未結束 confirmed 預約呼叫 `POST /api/bookings/{bookingId}/cancel` → 預期 200 且狀態成為 `cancelled`
    - 員工 B 隨後以 `POST /api/bookings` 預約同室同時段 → 預期 201 且新預約為 `confirmed`
- [x] `/tdd-e2e-red` — S-3-3 不得取消他人預約:
  - 受測行為：
    - 員工 A 呼叫 `POST /api/bookings/{bookingId}/cancel` 取消員工 B 的預約 → 預期 403 `FORBIDDEN`
    - 原預約仍維持 `confirmed`，且 `updated_at` 不因拒絕而改變
- [x] `/tdd-e2e-red` — S-3-4 沒有自己的預約時回傳空集合:
  - 受測行為：
    - 無任何個人預約的已登入使用者呼叫 `GET /api/bookings/mine` → 預期 200
    - 回應為空 `bookings` 陣列，不將無資料視為失敗
- [x] `/tdd-e2e-red` — S-3-5 已結束或已取消預約不可再次取消:
  - 受測行為：
    - 對已結束或已取消的本人預約呼叫 `POST /api/bookings/{bookingId}/cancel` → 預期 409 `BOOKING_NOT_CANCELLABLE`
    - 拒絕後預約維持原狀態，不重複更新
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 落地 `GET /api/bookings/mine`：只以 session 的 user UUID 查詢本人 confirmed／cancelled 紀錄，關聯 room 顯示資料並衍生 `is_cancellable`
    - 落地 `POST /api/bookings/{bookingId}/cancel`：在交易內鎖定預約，驗證存在、所有權、`confirmed` 狀態與尚未結束，再更新為 `cancelled` 與 `updated_at`
    - 保留取消歷史而不刪列；利用 partial exclusion 僅限制 confirmed 的特性，使同時段可由他人重新預約
    - 對齊 200／401／403／404／409 與共通錯誤形狀，拒絕路徑不得修改資料

#### Refactor

- [x] `/tdd-e2e-refactor` — 全綠下整理本人查詢、可取消判斷與交易內狀態轉換，維持所有權及歷史保留語意

---

### US-4 管理員維護會議室與不可預約時段（優先級：P3）

#### AC / Edge

- AC-4-1 管理員新增會議室後員工可見且可預約
- AC-4-2 維護時段內的新預約應被拒絕
- AC-4-3 停用後阻擋新約但既有已確認預約仍有效
- Edge-4-2 停用時不強制取消既有預約
- Edge-G-3 對停用會議室新約失敗且不改既有狀態
- AC-4-4 員工不可新增會議室或維護設定
- Edge-4-1 維護時段起迄無效時拒絕儲存

#### Red

- [x] `/tdd-e2e-red` — S-4-1 新增會議室後員工可見可約:
  - 受測行為：
    - 設施管理員呼叫 `POST /api/rooms` 送出名稱、樓層、容量與設備標誌 → 預期 201，回傳 `is_active: true`
    - 員工呼叫 `GET /api/rooms` → 預期 200 且可見新會議室；對該室送出合法 `POST /api/bookings` → 預期 201
- [x] `/tdd-e2e-red` — S-4-2 維護時段內拒絕新預約:
  - 受測行為：
    - 設施管理員以 `POST /api/rooms/{roomId}/maintenance-windows` 建立有效維護時段 → 預期 201
    - 員工以 `POST /api/bookings` 建立與維護時段重疊的預約 → 預期 409 `MAINTENANCE_CONFLICT`，且不建立預約
- [x] `/tdd-e2e-red` — S-4-3 停用只擋新約並保留既有預約:
  - 受測行為：
    - 設施管理員對已有未來 confirmed 預約的房間呼叫 `PATCH /api/rooms/{roomId}` 設 `is_active: false` → 預期 200
    - 員工再對停用房間呼叫 `POST /api/bookings` → 預期 400 `BOOKING_RULE_VIOLATION`
    - `GET /api/bookings?date={date}` → 預期 200，停用前既有預約仍為 `confirmed`
- [x] `/tdd-e2e-red` — S-4-4 一般員工不得執行管理操作:
  - 受測行為：
    - 一般員工分別呼叫 `POST /api/rooms`、`PATCH /api/rooms/{roomId}`、`POST /api/rooms/{roomId}/maintenance-windows` → 皆預期 403 `FORBIDDEN`
    - 拒絕後 rooms 與 maintenance_windows 均無新增或更新
- [x] `/tdd-e2e-red` — S-4-5 拒絕無效維護起迄:
  - 受測行為：
    - 設施管理員呼叫 `POST /api/rooms/{roomId}/maintenance-windows`，送出結束時間不晚於開始時間的區間 → 預期 400 `VALIDATION_ERROR`
    - 回應指出 `ends_at` 必須晚於 `starts_at`，且不儲存維護時段
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 落地 `requireRole('facility_admin')` 並套用於管理 endpoint；一般員工與主管統一回 403，未登入仍回 401
    - 落地 `POST /api/rooms`：驗證名稱、樓層、正容量與設備布林欄位，以 UUID 寫入 rooms 並固定新房間啟用
    - 落地 `PATCH /api/rooms/{roomId}`：第一版只接受 `is_active: false`，更新房間但不刪除、不取消或更動既有 bookings
    - 落地 `POST /api/rooms/{roomId}/maintenance-windows`：由 session 寫入 `created_by`，驗證 ISO 起迄與順序後寫入 DDL 對應資料
    - 完善 booking model 的交易內維護重疊與停用檢查，分別映射 409 `MAINTENANCE_CONFLICT` 與 400 `BOOKING_RULE_VIOLATION`
    - 對齊 rooms／maintenance 的 DDL CHECK、外鍵、不級聯語意及 201／200／400／401／403／404 回應

#### Refactor

- [x] `/tdd-e2e-refactor` — 全綠下整理角色閘門、房間狀態與維護時段存取，維持停用不影響既有預約的契約

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor |
| --- | --- | --- | --- | --- |
| US-1 | S-1-1 | — | — | — |
| US-1 | S-1-2 | — | — | — |
| US-1 | S-1-3 | — | — | — |
| US-1 | S-1-4 | — | — | — |
| US-1 | S-1-5 | — | — | — |
| US-1 | S-1-6 | — | — | — |
| US-1 | S-1-7 | — | — | — |
| US-2 | S-2-1 | — | — | — |
| US-2 | S-2-2 | — | — | — |
| US-2 | S-2-3 | — | — | — |
| US-2 | S-2-4 | — | — | — |
| US-3 | S-3-1 | — | — | — |
| US-3 | S-3-2 | — | — | — |
| US-3 | S-3-3 | — | — | — |
| US-3 | S-3-4 | — | — | — |
| US-3 | S-3-5 | — | — | — |
| US-4 | S-4-1 | — | — | — |
| US-4 | S-4-2 | — | — | — |
| US-4 | S-4-3 | — | — | — |
| US-4 | S-4-4 | — | — | — |
| US-4 | S-4-5 | — | — | — |

---

## 5. 假設

- 後端 Scenario 共 21 個：US-1 7 個、US-2 4 個、US-3 5 個、US-4 5 個；本檔不增刪 `e2e-test-plan.md` 的後端 Scenario ID。
- 所有 `/api` endpoint 除 `POST /api/auth/login` 外皆要求有效 session；session 由 `express-session` + `connect-pg-simple` 存於同一 PostgreSQL。
- `employee` 與 `manager` 的預約權限相同；管理 endpoint 僅 `facility_admin` 可用。
- 時段採半開區間 `[starts_at, ends_at)`；顯示及業務日曆以 `Asia/Taipei` 解讀，瞬間以 `TIMESTAMPTZ` 保存。
- PostgreSQL partial exclusion 是併發重疊預約的最終防線；取消保留歷史且不再占用時段。
- 假日使用本機 `holidays` 表或等價種子，不依賴外部服務；第一版不引入 Redis、GraphQL、message queue、SSO 或通知服務。
