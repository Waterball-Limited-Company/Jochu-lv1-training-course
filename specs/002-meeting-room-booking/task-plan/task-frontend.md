# 實作計畫（前端）：內部共享會議室預約系統

**功能分支**: `002-meeting-room-booking`  
**建立日期**: 2026-07-30  
**狀態**: 草稿

---

## 1. 規格閱讀

- [x] 已讀 `plan.md`（monorepo、`frontend/` 結構、Vite + TypeScript 原生 DOM）
- [x] 已讀 `technical-research.md`（History API、自製日曆、Vite proxy `/api`）
- [x] 已讀 `ui-plan.md`（Login、Home、BookingsBrowse、BookingCreate、MyBookings、AdminRooms）
- [x] 已讀 `api-plan.md`（REST 請求／回應、session cookie、錯誤形狀；本層可用 Mock）
- [x] 已讀 `e2e-test-plan.md` 的 `## 前端`
- [x] 確認前端 Scenario 無 blocked 項，且 US-1 不含僅屬後端／整合的 S-1-6
- [x] 已讀專案根目錄 `constitution.md`，確認執行期不使用 React、Vue、Angular，且前端只透過 REST 存取資料

```bash
ls specs/002-meeting-room-booking/plan.md \
   specs/002-meeting-room-booking/system-analyze/technical-research.md \
   specs/002-meeting-room-booking/system-analyze/ui-plan.md \
   specs/002-meeting-room-booking/system-analyze/api-plan.md \
   specs/002-meeting-room-booking/e2e-test-plan.md \
   constitution.md
```

---

## 2. 環境建立

### 2.1 Vite + TypeScript 專案骨架

- [x] 確認本機 Node.js 為現行 LTS，於 `frontend/` 初始化 Vite + TypeScript 專案
- [x] 執行期僅使用 TypeScript 編譯後的原生 DOM、History API、CSS 與 `fetch`，不安裝 React、Vue、Angular、重量級 router 或日曆套件
- [x] 建立 `index.html`、`src/main.ts`、`src/router.ts`、`src/api/client.ts`、`src/auth/session.ts`、`src/lib/datetime-taipei.ts`、`src/components/`、`src/styles/`

```bash
node -v
npm create vite@latest frontend -- --template vanilla-ts
cd frontend
npm install
```

### 2.2 頁面與路由底座

- [x] 建立 `src/pages/login.ts`、`home.ts`、`bookings-browse.ts`、`booking-create.ts`、`my-bookings.ts`、`admin-rooms.ts`
- [x] 在 `router.ts` 以 History API 定義 Login、Home、BookingsBrowse、BookingCreate、MyBookings、AdminRooms 六個可獨立到達頁面
- [x] 讓 BookingsBrowse 的 `date`、`roomId`、`view=calendar|list` 與 BookingCreate 的 `roomId` 可由 URL 還原
- [x] 建立共用導覽、載入中、空狀態、錯誤提示與重試區塊的最小呈現底座

### 2.3 API client、Mock 與 proxy

- [x] 在 `src/api/client.ts` 封裝 JSON `fetch`、一致錯誤形狀與 401 導回 Login；session cookie 由瀏覽器處理，不在前端儲存 token
- [x] 建立可切換的 Mock API，回應形狀對齊 `api-plan.md`，涵蓋 auth、rooms、overview、bookings、mine、cancel、maintenance endpoints
- [x] 在 `vite.config.ts` 設定 `/api` proxy 指向本機 Express `http://localhost:3000`
- [x] Mock 與真 API 使用相同頁面呼叫介面，避免頁面內分岔兩套資料契約

```bash
cd frontend
npm pkg get scripts
npm run dev
```

### 2.4 測試與 smoke 基建

- [x] 建立前端 Scenario 的瀏覽器驗收入口；本層以 Mock API 固定成功、錯誤、空資料與角色狀態
- [x] 確認六個頁面皆可由路由載入，重新整理與瀏覽器返回可維持對應頁面狀態
- [x] 確認 `/api` Mock 可切換案例，且未登入、一般使用者、設施管理員三種身分可重現
- [x] 確認 `npm run build` 可完成 TypeScript 型別檢查與 Vite 建置

---

## 3. User Story 實作計劃

### US-1 登入後瀏覽會議室並完成單次預約（優先級：P1）

#### AC / Edge

- AC-1-1 登入後合法預約應建立為已確認
- AC-1-2 同室重疊時段應被拒絕並提示衝突
- AC-1-3 未登入使用者不得建立預約
- Edge-1-1 清單中的停用會議室必須可被辨識
- Edge-1-2 缺必填欄位或時段無效時拒絕並提示
- Edge-G-2 跨日、假日、過短、過長或超出營業窗時拒絕

#### Red

- [x] `/tdd-e2e-red` — S-1-1 登入後建立合法預約並確認:
  - 受測行為：
    - Login 以有效帳密登入後導向 Home，Home 可見啟用中會議室及其屬性
    - 從 Home 選室進入 BookingCreate，送出完整且合法的單次預約後顯示已確認結果
    - 成功後導向 MyBookings，畫面可見該筆會議室、時段、用途與已確認狀態
- [x] `/tdd-e2e-red` — S-1-2 拒絕重疊時段並提示衝突:
  - 受測行為：
    - BookingCreate 送出與既有已確認預約重疊的同室時段後，畫面顯示可理解的時段衝突
    - 頁面停留在 BookingCreate，原有會議室、用途、人數、設備需求與起迄輸入均保留供修正
- [x] `/tdd-e2e-red` — S-1-3 未登入不得建立預約:
  - 受測行為：
    - 未登入使用者進入 BookingCreate 時被導向 Login 或顯示必須先登入
    - 畫面不提供可完成預約的受保護操作；受保護 API 回 401 時亦回到 Login
- [x] `/tdd-e2e-red` — S-1-4 清單可辨識停用會議室:
  - 受測行為：
    - Home 同時顯示啟用中與已停用會議室，且停用項目有清楚的不可新約狀態
    - 停用會議室不提供有效的建立預約流程；BookingCreate 遇停用會議室時不可送出
- [x] `/tdd-e2e-red` — S-1-5 拒絕缺漏或無效預約資料:
  - 受測行為：
    - BookingCreate 缺少用途、人數、起迄或設備需求等必填資訊時，畫面阻止完成預約
    - 起迄格式或順序無效時，在對應位置顯示可修正原因並保留其他輸入
- [x] `/tdd-e2e-red` — S-1-7 拒絕超出可預約日與時段規則:
  - 受測行為：
    - BookingCreate 對跨日、假日、少於 30 分鐘、超過 4 小時或超出平日 09:00–21:00 的時段顯示規則原因
    - 規則拒絕後留在原頁，保留原有輸入供使用者修改
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - Login 串接 Mock `GET /api/auth/me`、`POST /api/auth/login`，建立登入中／失敗狀態與成功後 Home 路由
    - Home 串接 Mock `GET /api/rooms`，呈現樓層、容量、設備與啟用狀態，僅讓啟用項目導向 BookingCreate
    - BookingCreate 以 URL `roomId` 還原選室，串接 Mock rooms、maintenance 與 `POST /api/bookings`，實作欄位及 Asia/Taipei 時段輔助預檢
    - 將 `BOOKING_CONFLICT`、`BOOKING_RULE_VIOLATION`、`MAINTENANCE_CONFLICT` 與欄位錯誤映射為可理解訊息，錯誤時保留表單
    - 建立受保護路由與 API 401 共用處理；成功建立後導向 MyBookings，Mock 回傳該筆 confirmed 預約

#### Refactor

- [x] `/tdd-e2e-refactor` — 行為不變下整理登入守衛、預約表單狀態、錯誤映射與頁面導覽

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
    - Home 呈現每間會議室的今日預約筆數、占用分鐘與忙碌比例
    - 畫面可明確區分有已確認預約的相對忙碌會議室與全日空閒會議室
- [x] `/tdd-e2e-red` — S-2-2 同批預約支援日曆與列表檢視:
  - 受測行為：
    - BookingsBrowse 的日曆模式依 09:00–21:00 時段與會議室呈現所選日期預約
    - 切換列表模式後顯示同一批預約的會議室、時段、用途與預約者摘要，不因切換而取得另一資料來源
    - 重新整理後依 URL 還原日期、會議室篩選與目前檢視模式
- [x] `/tdd-e2e-red` — S-2-3 今日無預約顯示皆空閒狀態:
  - 受測行為：
    - 今日所有會議室都無已確認預約時，Home 仍列出各會議室
    - 每間會議室顯示皆空閒或無預約的可理解狀態，不呈現空白頁
- [x] `/tdd-e2e-red` — S-2-4 所選日期無預約時兩種視圖顯示空狀態:
  - 受測行為：
    - BookingsBrowse 在所選日期無預約時，日曆模式顯示可理解空狀態
    - 切換列表模式後亦顯示空狀態而非載入失敗，日期與篩選仍維持
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - Home 串接 Mock `GET /api/overview/today`，以 Asia/Taipei 日期呈現各室忙碌摘要、全空閒與載入失敗狀態
    - BookingsBrowse 串接 Mock `GET /api/rooms` 與 `GET /api/bookings?date={date}&roomId={roomId}`，保存單一 `bookings[]` 頁面狀態
    - 以原生 CSS Grid／DOM 完成日曆模式，以清單／表格完成列表模式；兩模式只重繪同一份資料
    - 在 History URL 同步 `date`、`roomId`、`view`，處理返回、重新整理、日期變更、篩選與兩種空狀態

#### Refactor

- [x] `/tdd-e2e-refactor` — 行為不變下整理今日摘要、預約投影、模式切換與 URL 狀態同步

---

### US-3 查看並取消自己的預約（優先級：P3）

#### AC / Edge

- AC-3-1 我的預約列出目前使用者自己的紀錄
- AC-3-2 取消後釋放時段且他人可成功預約
- AC-3-3 使用者不可取消他人的預約
- Edge-3-1 無自己的預約時顯示可理解空狀態
- Edge-3-2 已結束或已取消預約不可再取消成功

#### Red

- [x] `/tdd-e2e-red` — S-3-1 我的預約列出本人紀錄:
  - 受測行為：
    - MyBookings 列出目前登入使用者自己的已確認與已取消預約
    - 每筆紀錄顯示會議室、樓層、起迄、用途、設備需求與狀態
- [x] `/tdd-e2e-red` — S-3-2 取消後釋放時段供他人預約:
  - 受測行為：
    - MyBookings 取消可取消的已確認預約後，就地顯示為已取消且不再提供有效取消操作
    - 前往 BookingCreate 選擇同一會議室與原時段時，畫面允許繼續填寫送出；跨使用者成功閉環留待整合層證明
- [x] `/tdd-e2e-red` — S-3-3 不得取消他人預約:
  - 受測行為：
    - 員工 A 的 MyBookings 不顯示員工 B 的預約
    - 畫面不提供取消他人預約的操作，清單內容只反映目前登入者
- [x] `/tdd-e2e-red` — S-3-4 沒有自己的預約時顯示空狀態:
  - 受測行為：
    - MyBookings 收到空清單時顯示可理解的無預約狀態
    - 空狀態提供前往 BookingCreate 的操作，且可正常完成頁面導覽
- [x] `/tdd-e2e-red` — S-3-5 已結束或已取消預約不可再次取消:
  - 受測行為：
    - MyBookings 對已結束或已取消預約不提供有效取消操作，並顯示不可取消狀態
    - 若取消結果回報已不可取消，畫面不顯示成功，改呈現原因並維持正確狀態
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - MyBookings 串接 Mock `GET /api/bookings/mine`，依 API 順序呈現本人 confirmed／cancelled 紀錄與空狀態
    - 只對 `is_cancellable=true` 的項目提供附屬確認流程，串接 Mock `POST /api/bookings/{bookingId}/cancel`
    - 取消成功後就地更新為 cancelled 並停用操作；403／404／409 時呈現一致錯誤並依需要重新載入
    - 空狀態與取消後的導覽連至 BookingCreate；Mock 狀態同步釋放時段，讓建立頁可繼續填寫

#### Refactor

- [x] `/tdd-e2e-refactor` — 行為不變下整理本人預約渲染、可取消判定、確認流程與狀態更新

---

### US-4 管理員維護會議室與不可預約時段（優先級：P3）

#### AC / Edge

- AC-4-1 管理員新增會議室後員工可見且可預約
- AC-4-2 維護時段內的新預約應被拒絕
- AC-4-3 停用後阻擋新約但既有已確認預約仍有效
- AC-4-4 員工不可新增會議室或維護設定
- Edge-4-1 維護時段起迄無效時拒絕儲存
- Edge-4-2 停用時不強制取消既有預約
- Edge-G-3 對停用會議室新約失敗且不改既有狀態

#### Red

- [x] `/tdd-e2e-red` — S-4-1 新增會議室後員工可見可約:
  - 受測行為：
    - facility_admin 在 AdminRooms 填妥名稱、樓層、容量與設備標誌後，新增的會議室顯示為啟用中
    - 切換為員工視角後，Home 可見該室且可由該室前往 BookingCreate
- [x] `/tdd-e2e-red` — S-4-2 維護時段內拒絕新預約:
  - 受測行為：
    - AdminRooms 建立有效維護時段後，維護清單可見該會議室、起迄與說明
    - BookingCreate 對與維護時段重疊的新預約顯示維護不可用原因，並保留可修正輸入
- [x] `/tdd-e2e-red` — S-4-3 停用只擋新約並保留既有預約:
  - 受測行為：
    - AdminRooms 停用會議室前顯示「只阻擋新預約、不取消既有預約」說明，完成後狀態更新為停用
    - Home 與 BookingCreate 清楚標示該室不可新約，且不提供可成功完成的新預約操作
    - BookingsBrowse 與 MyBookings 仍顯示停用前既有預約為已確認
- [x] `/tdd-e2e-red` — S-4-4 一般員工不得執行管理操作:
  - 受測行為：
    - employee 或 manager 在 Home 不會看到會議室管理入口
    - 非 facility_admin 直接進入 AdminRooms 時顯示無權存取與返回 Home 的方式，不呈現可操作管理表單
- [x] `/tdd-e2e-red` — S-4-5 拒絕無效維護起迄:
  - 受測行為：
    - AdminRooms 的維護表單在結束時間不晚於開始時間時拒絕完成儲存
    - 畫面提示結束時間必須晚於開始時間，並保留其他可修正輸入
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - Home 與 AdminRooms 依 Mock `GET /api/auth/me` 的 `facility_admin` 角色控制管理入口與頁面權限狀態
    - AdminRooms 串接 Mock `GET /api/rooms`、`POST /api/rooms` 與 `PATCH /api/rooms/{roomId}`，完成新增 Modal、停用確認與就地清單更新
    - AdminRooms 串接 Mock maintenance GET／POST，完成查詢區間、維護清單、附屬表單與起迄預檢
    - Mock rooms、bookings 與 maintenance 使用共享狀態，使新增室反映至 Home／BookingCreate，停用只改 Room 且保留既有 Booking
    - BookingCreate 將 maintenance 提示及 `MAINTENANCE_CONFLICT` 映射為可理解原因；AdminRooms 將 403 呈現為無權存取

#### Refactor

- [x] `/tdd-e2e-refactor` — 行為不變下整理角色閘門、管理表單、Mock 共享狀態與跨頁房間投影

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor |
| --- | --- | --- | --- | --- |
| US-1 | S-1-1 | ✅ | ✅ | ✅ |
| US-1 | S-1-2 | ✅ | ✅ | ✅ |
| US-1 | S-1-3 | ✅ | ✅ | ✅ |
| US-1 | S-1-4 | ✅ | ✅ | ✅ |
| US-1 | S-1-5 | ✅ | ✅ | ✅ |
| US-1 | S-1-7 | ✅ | ✅ | ✅ |
| US-2 | S-2-1 | ✅ | ✅ | ✅ |
| US-2 | S-2-2 | ✅ | ✅ | ✅ |
| US-2 | S-2-3 | ✅ | ✅ | ✅ |
| US-2 | S-2-4 | ✅ | ✅ | ✅ |
| US-3 | S-3-1 | ✅ | ✅ | ✅ |
| US-3 | S-3-2 | ✅ | ✅ | ✅ |
| US-3 | S-3-3 | ✅ | ✅ | ✅ |
| US-3 | S-3-4 | ✅ | ✅ | ✅ |
| US-3 | S-3-5 | ✅ | ✅ | ✅ |
| US-4 | S-4-1 | ✅ | ✅ | ✅ |
| US-4 | S-4-2 | ✅ | ✅ | ✅ |
| US-4 | S-4-3 | ✅ | ✅ | ✅ |
| US-4 | S-4-4 | ✅ | ✅ | ✅ |
| US-4 | S-4-5 | ✅ | ✅ | ✅ |

---

## 5. 假設

- 本層可使用 Mock API 證明畫面、路由與互動；真實 session、持久化、併發與跨使用者一致性由後端及整合層證明
- 前端採 Vite + TypeScript 編譯後的原生 DOM／fetch，不使用 React、Vue、Angular、重量級 router 或日曆套件
- 六個全頁固定為 Login、Home、BookingsBrowse、BookingCreate、MyBookings、AdminRooms；Modal、確認框與維護表單附屬所屬頁面
- 開發期 `/api` 由 Vite proxy 轉送至 Express；前端不直連 PostgreSQL，也不儲存 session token
- 所有受保護頁面與 API 401 都導向 Login；管理入口只對 `facility_admin` 顯示，`employee` 與 `manager` 的預約能力相同
- 所有日期、今日與營業時段顯示以 `Asia/Taipei` 解讀；前端預檢僅提供提示，REST API 回應仍是規則最終真相
