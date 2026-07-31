# 實作計畫（整合）：內部共享會議室預約系統

**功能分支**: `002-meeting-room-booking`  
**建立日期**: 2026-07-30  
**狀態**: 草稿  
**範圍**: 前後端真串接（僅 Then 必須兩端一起才有意義的 Scenario）

---

## 1. 規格閱讀

- [x] 已讀 `e2e-test-plan.md` 的 `## 整合`（本輪 S-1-1、S-1-6、S-3-2、S-4-3）
- [x] 已讀 `task-backend.md`／`task-frontend.md` 對應 US，確認單層 Red／Green 已完成
- [x] 已讀 `api-plan.md`、`ui-plan.md`，確認 REST API、錯誤回應與頁面互動契約一致
- [x] 確認四個整合 Scenario 均無 blocked 項

```bash
ls specs/002-meeting-room-booking/e2e-test-plan.md \
   specs/002-meeting-room-booking/task-plan/task-backend.md \
   specs/002-meeting-room-booking/task-plan/task-frontend.md \
   specs/002-meeting-room-booking/system-analyze/api-plan.md \
   specs/002-meeting-room-booking/system-analyze/ui-plan.md
```

---

## 2. 環境建立

### 2.1 既有專案與服務確認

- [x] 不重新初始化或重搭 `backend/`、`frontend/`；沿用兩端既有依賴、啟動腳本與測試基建
- [x] 確認 Node.js、後端 Express 與前端 Vite 的既有版本可正常執行
- [x] 確認 Docker PostgreSQL、backend、frontend 可同時啟動，且連線字串與機密皆由環境變數注入
- [x] 確認後端只以 PostgreSQL 作為應用資料真相來源，前端只經 REST API 存取資料

```bash
node -v
docker compose config
ls backend/package.json frontend/package.json
```

### 2.2 資料重置與種子

- [x] 確認可重置測試資料庫並套用既有 schema／migration，使每輪整合測試從可重現狀態開始
- [x] 確認 seed 可建立一般員工、設施管理員、啟用中會議室，以及各 Scenario 所需的空閒或既有預約資料
- [x] 確認重置／seed 不依賴前一次 Scenario 殘留資料，並以 `Asia/Taipei` 解讀業務日期與可預約時段

### 2.3 Proxy 與真串接 Smoke

- [x] 確認 frontend proxy 的 `/api` 指向同時執行中的 backend，瀏覽器端不直連 PostgreSQL
- [x] 從前端登入並呼叫一個受保護 API，確認 session／cookie、proxy 與專案一致的 `error.code`、`error.message` 回應可穿透
- [x] 確認整合測試可建立兩個彼此隔離的登入工作階段，以覆蓋雙員工與管理員／員工流程
- [x] 約定整合測試啟動與清場順序：PostgreSQL → reset／seed → backend → frontend → smoke／Scenario

---

## 3. User Story 實作計劃

### US-1 登入後瀏覽會議室並完成單次預約（優先級：P1）

#### AC / Edge

- AC-1-1 登入後合法預約應建立為已確認
- Edge-G-1 併發重疊時最多一筆成為已確認

#### Red

- [x] `/tdd-e2e-red` — S-1-1 登入後跨頁建立合法預約（真串接）:
  - 受測行為：
    - 員工以有效帳密登入，從首頁取得啟用中的空閒會議室，進入建立預約頁並送出合法時段
    - 建立成功後導向自己的預約頁，該筆預約顯示為已確認，且使用者、會議室與時段資料一致
    - 重新進入自己的預約頁後由後端重新讀取資料，仍可看到同一筆已確認預約
- [x] `/tdd-e2e-red` — S-1-6 併發重疊預約最多一筆確認（真串接）:
  - 受測行為：
    - 兩位已登入員工在隔離工作階段中，針對同一會議室送出彼此重疊的真實併發預約請求
    - 一位使用者看到預約已確認，另一位看到時段衝突，且錯誤回應維持專案一致形狀
    - 重新查詢該日預約後，系統中該重疊時段最多只有一筆已確認預約
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 串接 Login → Home → BookingCreate → MyBookings，確認前端皆使用真實 `POST /api/auth/login`、`GET /api/rooms`、`POST /api/bookings` 與 `GET /api/bookings/mine`
    - 對齊登入會話、UUID、日期時間與預約欄位契約；建立成功後導頁並由 API 重新載入，不以本地暫存冒充持久化結果
    - 讓兩個真實併發 `POST /api/bookings` 由 PostgreSQL 重疊排除約束收斂，將唯一成功與衝突錯誤映射為兩端一致的 UI 狀態
    - 以 `GET /api/bookings?date={date}` 驗證資料庫最終狀態，不新增旁路資料來源或平行契約

#### Refactor

- [x] `/tdd-e2e-refactor` — 行為不變下整理登入會話、預約提交、衝突錯誤映射與重載流程的重複接線

---

### US-3 查看並取消自己的預約（優先級：P3）

#### AC / Edge

- AC-3-2 取消後釋放時段且他人可成功預約

#### Red

- [x] `/tdd-e2e-red` — S-3-2 取消後另一位員工可預約同時段（真串接）:
  - 受測行為：
    - 員工 B 在員工 A 的已確認預約仍有效時送出同室同時段預約，看到時段衝突且未新增已確認預約
    - 員工 A 從自己的預約取消該筆預約後，畫面由後端資料更新為已取消
    - 員工 B 再次送出同室同時段預約後看到新預約已確認；重新讀取時，A 的歷史預約仍為已取消且 B 的預約維持已確認
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 串接 MyBookings 的取消操作至 `POST /api/bookings/{bookingId}/cancel`，成功後重新取得本人預約並顯示 `cancelled`
    - 保留原預約歷史資料但使其不再參與已確認時段互斥，讓另一登入工作階段可經 `POST /api/bookings` 建立同時段預約
    - 對齊取消、衝突與建立成功的 API 回應及 UI 狀態，確保兩位員工只能操作或查看各自權限內資料

#### Refactor

- [x] `/tdd-e2e-refactor` — 行為不變下整理跨工作階段的取消、重新預約與狀態重新載入流程

---

### US-4 管理員維護會議室與不可預約時段（優先級：P3）

#### AC / Edge

- AC-4-3 停用後阻擋新約但既有已確認預約仍有效
- Edge-4-2 停用時不強制取消既有預約
- Edge-G-3 對停用會議室新約失敗且不改既有狀態

#### Red

- [x] `/tdd-e2e-red` — S-4-3 停用後既有預約保留且新約失敗（真串接）:
  - 受測行為：
    - 設施管理員停用已有未來已確認預約的會議室後，員工從首頁與建立預約頁看到該室不可新約
    - 員工對停用會議室送出新預約時看到失敗，且錯誤回應維持專案一致形狀
    - 從預約檢視與自己的預約重新讀取資料後，停用前既有預約仍存在且維持已確認，系統未新增停用後的預約
- [x] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [x] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 串接 AdminRooms 至 `PATCH /api/rooms/{roomId}`，停用成功後讓 Home 與 BookingCreate 重新取得房間狀態並禁止新約
    - 在 `POST /api/bookings` 以後端房間狀態作最終檢查，拒絕停用會議室的新預約並回傳一致錯誤契約
    - 維持 Room 與 Booking 的既有關聯，不刪除或改寫既有預約；以 `GET /api/bookings?date={date}` 與 `GET /api/bookings/mine` 驗證其仍為已確認
    - 對齊管理員與員工兩個工作階段的權限、重載與錯誤顯示，不以只停用按鈕的前端限制取代後端規則

#### Refactor

- [x] `/tdd-e2e-refactor` — 行為不變下整理房間狀態重載、新約阻擋與既有預約顯示的共用接線

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor |
| --- | --- | --- | --- | --- |
| US-1 | S-1-1 | ✅ | ✅ | ✅ |
| US-1 | S-1-6 | ✅ | ✅ | ✅ |
| US-3 | S-3-2 | ✅ | ✅ | ✅ |
| US-4 | S-4-3 | ✅ | ✅ | ✅ |

---

## 5. 假設

- 本整合計畫恰好涵蓋 S-1-1、S-1-6、S-3-2、S-4-3；其他可由單一層證明的 Scenario 留在後端或前端 task
- `backend/`、`frontend/`、Docker PostgreSQL 與其啟動、reset、seed 腳本已由前置工作建立，本檔只補真串接與整合驗證，不重搭專案
- 若對應後端或前端 User Story 尚未 Green，先完成單層 task，再執行本檔的整合 Red
- 測試帳號、會議室、預約與維護資料皆可由既有 seed 穩定重建；每個 Scenario 執行前可重置至彼此隔離的基準狀態
- 所有業務日期與時段以 `Asia/Taipei` 解讀，持久化瞬間欄位遵循既有 `TIMESTAMPTZ` 契約
