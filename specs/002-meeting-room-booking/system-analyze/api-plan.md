# API 計畫：內部共享會議室預約系統

**功能分支**: `002-meeting-room-booking`
**建立日期**: 2026-07-30
**狀態**: 草稿

## API Schema 描述

| 欄位 | 內容 |
| --- | --- |
| 共通 Header | JSON request 使用 `Content-Type: application/json`；登入後由瀏覽器自動帶入 HttpOnly session cookie；所有受保護 Endpoint 以該 session 辨識使用者 |
| 時間格式 | 瞬間使用 ISO-8601 with offset（例如 `2026-07-31T14:00:00+08:00`）或 UTC `Z`；日期 query 使用 `YYYY-MM-DD`，所有「今日／平日／營業時段」以 `Asia/Taipei` 解讀 |

## 共通錯誤格式

全檔共用；各 Endpoint 仍逐一列出可能的 error status 與完整錯誤範例。`details` 可用於提供欄位或規則細節。

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "starts_at",
        "reason": "must be a valid ISO-8601 datetime"
      }
    ]
  }
}
```

---

## 資料實體：Session/Auth

### 對應 User Story

| US | 描述 |
| --- | --- |
| US1 | 使用帳號密碼登入，並依角色取得可執行操作 |
| US4 | 以登入使用者角色限制設施管理操作 |

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。Session 由 `connect-pg-simple` 管理；下列為 API 可見的登入使用者形狀，不含密碼雜湊與 session token。

```json
{
  "authenticated": true,
  "user": {
    "id": "11111111-1111-4111-8111-111111111111",
    "username": "alice",
    "display_name": "Alice",
    "role": "employee",
    "created_at": "2026-07-30T01:00:00.000Z"
  }
}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
| `authenticated` | 目前 request 是否具有效 session |
| `user.id` | 登入使用者 UUID |
| `user.username` | 登入帳號 |
| `user.display_name` | UI 顯示名稱 |
| `user.role` | `employee`、`manager` 或 `facility_admin` |
| `user.created_at` | 帳號建立時間 |

### Endpoint：`POST /api/auth/login`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR1**：支援帳號密碼登入並區分三種角色 |
| 說明 | 驗證帳密、建立伺服端 session，並以 `Set-Cookie` 回傳 HttpOnly session cookie |
| 設計備註 | 帳號或密碼錯誤統一回 `INVALID_CREDENTIALS`，避免揭露帳號是否存在；成功後輪替 session ID |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "username": "alice",
  "password": "training-password"
}
```

#### Responses

##### 200 OK

```json
{
  "authenticated": true,
  "user": {
    "id": "11111111-1111-4111-8111-111111111111",
    "username": "alice",
    "display_name": "Alice",
    "role": "employee",
    "created_at": "2026-07-30T01:00:00.000Z"
  }
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "username and password are required",
    "details": []
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid username or password",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 有效帳密登入成功 | 200 |
| 缺少帳號或密碼 | 400 |
| 帳號或密碼錯誤 | 401 |

---

### Endpoint：`POST /api/auth/logout`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR1**：登入會話可結束並撤銷 |
| 說明 | 銷毀目前伺服端 session 並清除 cookie |
| 設計備註 | 僅接受有效 session；成功回傳 JSON，不使用空 body |

#### Parameters

無

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "authenticated": false
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 已登入使用者登出成功 | 200 |
| 未登入時要求登出 | 401 |

---

### Endpoint：`GET /api/auth/me`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR1**：辨識登入使用者與角色 |
| 說明 | 取得目前 session 對應的使用者資料 |
| 設計備註 | 不回傳 `password_hash`、session ID 或 cookie 值 |

#### Parameters

無

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "authenticated": true,
  "user": {
    "id": "11111111-1111-4111-8111-111111111111",
    "username": "alice",
    "display_name": "Alice",
    "role": "employee",
    "created_at": "2026-07-30T01:00:00.000Z"
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 有效 session 取得本人資料 | 200 |
| session 不存在或已失效 | 401 |

---

## 資料實體：Room

### 對應 User Story

| US | 描述 |
| --- | --- |
| US1 | 瀏覽會議室屬性與啟用狀態 |
| US2 | 依會議室呈現今日忙碌與預約 |
| US4 | 設施管理員新增及停用會議室 |

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。

```json
{
  "id": "22222222-2222-4222-8222-222222222222",
  "name": "大會議A",
  "floor": "3F",
  "capacity": 12,
  "has_projector": true,
  "has_video_conference": true,
  "is_active": true,
  "created_at": "2026-07-30T01:00:00.000Z",
  "updated_at": "2026-07-30T01:00:00.000Z"
}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
| `id` | 會議室 UUID |
| `name` | 會議室名稱 |
| `floor` | 樓層標示 |
| `capacity` | 最大容納人數 |
| `has_projector` | 是否具備投影機 |
| `has_video_conference` | 是否具備視訊設備 |
| `is_active` | 是否接受新預約；停用會議室仍保留並可辨識 |
| `created_at` | 建立時間 |
| `updated_at` | 最後更新時間 |

### Endpoint：`GET /api/rooms`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR2**：顯示會議室名稱、樓層、容量、設備及啟用狀態 |
| 說明 | 列出所有會議室，包含啟用與停用項目 |
| 設計備註 | 不預設排除停用會議室；前端以 `is_active` 明確呈現不可新約狀態；預設依 `floor`、`name` 排序 |

#### Parameters

無

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "rooms": [
    {
      "id": "22222222-2222-4222-8222-222222222222",
      "name": "大會議A",
      "floor": "3F",
      "capacity": 12,
      "has_projector": true,
      "has_video_conference": true,
      "is_active": true,
      "created_at": "2026-07-30T01:00:00.000Z",
      "updated_at": "2026-07-30T01:00:00.000Z"
    },
    {
      "id": "66666666-6666-4666-8666-666666666666",
      "name": "小會議B",
      "floor": "4F",
      "capacity": 6,
      "has_projector": false,
      "has_video_conference": true,
      "is_active": false,
      "created_at": "2026-07-30T01:10:00.000Z",
      "updated_at": "2026-07-30T04:00:00.000Z"
    }
  ]
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 清單同時含啟用與停用會議室 | 200 |
| 尚無會議室時回空陣列 | 200 |
| 未登入查詢 | 401 |

---

### Endpoint：`POST /api/rooms`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US4-FR1**：設施管理員可新增會議室<br>- **US4-FR4**：拒絕非設施管理員執行管理操作 |
| 說明 | 建立一間預設啟用的會議室 |
| 設計備註 | 僅 `facility_admin`；`name`、`floor` 不可空白，`capacity` 至少為 1；`has_projector` 與 `has_video_conference` 必填且須為布林值；建立時 `is_active` 固定為 `true` |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "name": "研討室C",
  "floor": "5F",
  "capacity": 8,
  "has_projector": true,
  "has_video_conference": false
}
```

#### Responses

##### 201 Created

```json
{
  "id": "77777777-7777-4777-8777-777777777777",
  "name": "研討室C",
  "floor": "5F",
  "capacity": 8,
  "has_projector": true,
  "has_video_conference": false,
  "is_active": true,
  "created_at": "2026-07-30T05:00:00.000Z",
  "updated_at": "2026-07-30T05:00:00.000Z"
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "capacity must be at least 1",
    "details": [
      {
        "field": "capacity",
        "reason": "must be at least 1"
      }
    ]
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

##### 403 Forbidden

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Facility administrator role is required",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 設施管理員建立會議室 | 201 |
| 欄位缺漏或容量無效 | 400 |
| 未登入建立 | 401 |
| 員工或主管建立 | 403 |

---

### Endpoint：`PATCH /api/rooms/{roomId}`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US4-FR2**：設施管理員可將會議室停用<br>- **US4-FR4**：拒絕非設施管理員執行停用操作<br>- **GR-003**：停用只禁止新預約，不取消既有已確認預約 |
| 說明 | 更新指定會議室的啟用狀態 |
| 設計備註 | 僅 `facility_admin`；第一版 request 僅接受 `is_active: false`，不開放重新啟用；停用只擋新預約，不取消或改動既有預約 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | roomId | 是 | 22222222-2222-4222-8222-222222222222 |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "is_active": false
}
```

#### Responses

##### 200 OK

```json
{
  "id": "22222222-2222-4222-8222-222222222222",
  "name": "大會議A",
  "floor": "3F",
  "capacity": 12,
  "has_projector": true,
  "has_video_conference": true,
  "is_active": false,
  "created_at": "2026-07-30T01:00:00.000Z",
  "updated_at": "2026-07-30T05:30:00.000Z"
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "is_active must be false",
    "details": [
      {
        "field": "is_active",
        "reason": "only deactivation is supported"
      }
    ]
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

##### 403 Forbidden

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Facility administrator role is required",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "ROOM_NOT_FOUND",
    "message": "Room was not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 設施管理員停用會議室 | 200 |
| is_active 缺漏、格式錯誤或傳入 true | 400 |
| 未登入更新 | 401 |
| 員工或主管更新 | 403 |
| roomId 不存在 | 404 |

---

## 資料實體：Booking

### 對應 User Story

| US | 描述 |
| --- | --- |
| US1 | 建立符合規則且不衝突的單次預約 |
| US2 | 以日曆與列表檢視同一批預約 |
| US3 | 查看並取消自己的預約 |
| US4 | 停用與維護時段限制新的預約 |

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。查詢回應可加入 `room`、`booked_by` 與 `is_cancellable` 等顯示／衍生資料，持久化欄位名仍對齊 data-plan。

```json
{
  "id": "33333333-3333-4333-8333-333333333333",
  "room_id": "22222222-2222-4222-8222-222222222222",
  "user_id": "11111111-1111-4111-8111-111111111111",
  "purpose": "產品週會",
  "attendee_count": 6,
  "needs_projector": true,
  "needs_video_conference": false,
  "starts_at": "2026-07-31T14:00:00+08:00",
  "ends_at": "2026-07-31T15:00:00+08:00",
  "status": "confirmed",
  "created_at": "2026-07-30T02:00:00.000Z",
  "updated_at": "2026-07-30T02:00:00.000Z"
}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
| `id` | 預約 UUID |
| `room_id` | 被預約的會議室 UUID |
| `user_id` | 預約者 UUID，由 session 決定 |
| `purpose` | 會議用途 |
| `attendee_count` | 預期人數 |
| `needs_projector` | 是否需要投影機 |
| `needs_video_conference` | 是否需要視訊設備 |
| `starts_at` | 預約開始瞬間 |
| `ends_at` | 預約結束瞬間 |
| `status` | `confirmed` 或 `cancelled` |
| `created_at` | 建立時間 |
| `updated_at` | 最後更新時間 |
| `is_cancellable` | 查詢衍生的可取消狀態，不落庫 |

### Endpoint：`POST /api/bookings`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR3**：必填用途、人數、起迄與設備需求<br>- **US1-FR4**：規則通過後建立 `confirmed` 紀錄<br>- **US1-FR5**：拒絕預約或維護時段重疊<br>- **US1-FR6**：拒絕人數超過容量<br>- **GR-001**：同室已確認預約不得重疊<br>- **GR-002**：台北同一平日 09:00–21:00、30 分鐘至 4 小時且非假日<br>- **GR-003**：停用會議室只拒絕新預約，不改動既有預約 |
| 說明 | 在交易內校驗並建立單次已確認預約 |
| 設計備註 | `user_id` 取自 session，不接受 client 指定；時段採半開區間 `[starts_at, ends_at)`；預約衝突回 `409 BOOKING_CONFLICT`；維護重疊回 `409 MAINTENANCE_CONFLICT`；停用、假日、營業時段、時長、跨日或容量超限回 400；設備需求僅記錄不因「會議室缺該設備」而拒絕；DB exclusion 為併發最終防線 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "room_id": "22222222-2222-4222-8222-222222222222",
  "purpose": "產品週會",
  "attendee_count": 6,
  "needs_projector": true,
  "needs_video_conference": false,
  "starts_at": "2026-07-31T14:00:00+08:00",
  "ends_at": "2026-07-31T15:00:00+08:00"
}
```

#### Responses

##### 201 Created

```json
{
  "id": "33333333-3333-4333-8333-333333333333",
  "room_id": "22222222-2222-4222-8222-222222222222",
  "user_id": "11111111-1111-4111-8111-111111111111",
  "purpose": "產品週會",
  "attendee_count": 6,
  "needs_projector": true,
  "needs_video_conference": false,
  "starts_at": "2026-07-31T14:00:00+08:00",
  "ends_at": "2026-07-31T15:00:00+08:00",
  "status": "confirmed",
  "created_at": "2026-07-30T02:00:00.000Z",
  "updated_at": "2026-07-30T02:00:00.000Z"
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "BOOKING_RULE_VIOLATION",
    "message": "Booking must be within 09:00–21:00 on one business day in Asia/Taipei",
    "details": [
      {
        "rule": "GR-002",
        "reason": "outside_business_hours"
      }
    ]
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "ROOM_NOT_FOUND",
    "message": "Room was not found",
    "details": []
  }
}
```

##### 409 Conflict — Booking overlap

```json
{
  "error": {
    "code": "BOOKING_CONFLICT",
    "message": "The room already has a confirmed booking in this time range",
    "details": [
      {
        "room_id": "22222222-2222-4222-8222-222222222222",
        "starts_at": "2026-07-31T14:00:00+08:00",
        "ends_at": "2026-07-31T15:00:00+08:00"
      }
    ]
  }
}
```

##### 409 Conflict — Maintenance overlap

```json
{
  "error": {
    "code": "MAINTENANCE_CONFLICT",
    "message": "The room is unavailable during a maintenance window",
    "details": [
      {
        "room_id": "22222222-2222-4222-8222-222222222222",
        "starts_at": "2026-07-31T14:00:00+08:00",
        "ends_at": "2026-07-31T15:00:00+08:00"
      }
    ]
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 合法且無衝突時建立已確認預約 | 201 |
| 欄位缺漏、格式錯誤或人數超過容量 | 400 |
| 停用會議室、跨日、假日、非平日或違反營業時段與時長 | 400 |
| 未登入建立 | 401 |
| room_id 不存在 | 404 |
| 與已確認預約重疊（含併發競爭） | 409 |
| 與維護時段重疊 | 409 |

---

### Endpoint：`GET /api/bookings`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US2-FR2**：提供日曆視圖資料<br>- **US2-FR3**：提供列表視圖資料<br>- **US2-FR4**：呈現已確認預約的會議室、時段及辨識摘要 |
| 說明 | 依台北日曆日取得已確認預約，供日曆與列表共用 |
| 設計備註 | `date` 必填並以 `Asia/Taipei` 日界查詢；`roomId` 可選；只回 `confirmed`，依 `starts_at`、會議室名稱排序；兩種視圖不得各自呼叫不同資料源 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| query | date | 是 | 2026-07-31 |
| query | roomId | 否 | 22222222-2222-4222-8222-222222222222 |

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "date": "2026-07-31",
  "timezone": "Asia/Taipei",
  "bookings": [
    {
      "id": "33333333-3333-4333-8333-333333333333",
      "room_id": "22222222-2222-4222-8222-222222222222",
      "room": {
        "name": "大會議A",
        "floor": "3F"
      },
      "user_id": "11111111-1111-4111-8111-111111111111",
      "booked_by": {
        "display_name": "Alice"
      },
      "purpose": "產品週會",
      "attendee_count": 6,
      "needs_projector": true,
      "needs_video_conference": false,
      "starts_at": "2026-07-31T14:00:00+08:00",
      "ends_at": "2026-07-31T15:00:00+08:00",
      "status": "confirmed",
      "created_at": "2026-07-30T02:00:00.000Z",
      "updated_at": "2026-07-30T02:00:00.000Z"
    }
  ]
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "date must use YYYY-MM-DD",
    "details": [
      {
        "field": "date",
        "reason": "invalid_date"
      }
    ]
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "ROOM_NOT_FOUND",
    "message": "Room was not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 查詢台北日全部已確認預約 | 200 |
| 依 roomId 篩選 | 200 |
| 該日無預約時回空陣列 | 200 |
| date 缺漏或格式錯誤 | 400 |
| 未登入查詢 | 401 |
| roomId 不存在 | 404 |

---

### Endpoint：`GET /api/bookings/mine`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US3-FR1**：列出目前使用者自己的已確認與已取消預約 |
| 說明 | 取得目前登入使用者的預約歷史 |
| 設計備註 | 不接受 `userId`；依 `starts_at` 降冪排序；`is_cancellable` 由狀態與目前時間衍生 |

#### Parameters

無

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "bookings": [
    {
      "id": "33333333-3333-4333-8333-333333333333",
      "room_id": "22222222-2222-4222-8222-222222222222",
      "room": {
        "name": "大會議A",
        "floor": "3F"
      },
      "user_id": "11111111-1111-4111-8111-111111111111",
      "purpose": "產品週會",
      "attendee_count": 6,
      "needs_projector": true,
      "needs_video_conference": false,
      "starts_at": "2026-07-31T14:00:00+08:00",
      "ends_at": "2026-07-31T15:00:00+08:00",
      "status": "confirmed",
      "is_cancellable": true,
      "created_at": "2026-07-30T02:00:00.000Z",
      "updated_at": "2026-07-30T02:00:00.000Z"
    }
  ]
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 回傳本人的已確認與已取消預約 | 200 |
| 本人無預約時回空陣列 | 200 |
| 未登入查詢 | 401 |

---

### Endpoint：`POST /api/bookings/{bookingId}/cancel`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US3-FR2**：可取消自己的未結束已確認預約<br>- **US3-FR3**：取消後改為 `cancelled` 並釋放時段<br>- **US3-FR4**：不得取消他人的預約 |
| 說明 | 取消目前登入使用者擁有且尚可取消的預約 |
| 設計備註 | 所有權不符回 403；已取消或已結束回 409；成功以交易更新狀態與 `updated_at`，保留歷史資料 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | bookingId | 是 | 33333333-3333-4333-8333-333333333333 |

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "id": "33333333-3333-4333-8333-333333333333",
  "room_id": "22222222-2222-4222-8222-222222222222",
  "user_id": "11111111-1111-4111-8111-111111111111",
  "purpose": "產品週會",
  "attendee_count": 6,
  "needs_projector": true,
  "needs_video_conference": false,
  "starts_at": "2026-07-31T14:00:00+08:00",
  "ends_at": "2026-07-31T15:00:00+08:00",
  "status": "cancelled",
  "created_at": "2026-07-30T02:00:00.000Z",
  "updated_at": "2026-07-30T06:00:00.000Z"
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

##### 403 Forbidden

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You cannot cancel another user's booking",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "BOOKING_NOT_FOUND",
    "message": "Booking was not found",
    "details": []
  }
}
```

##### 409 Conflict

```json
{
  "error": {
    "code": "BOOKING_NOT_CANCELLABLE",
    "message": "Booking is already cancelled or has ended",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 取消自己的未結束已確認預約 | 200 |
| 未登入取消 | 401 |
| 取消他人的預約 | 403 |
| bookingId 不存在 | 404 |
| 重複取消或取消已結束預約 | 409 |

---

## 資料實體：Overview

### 對應 User Story

| US | 描述 |
| --- | --- |
| US2 | 在首頁掌握今天各會議室的相對忙碌程度 |

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。Overview 為 Room 與當日 confirmed Booking 的查詢衍生投影，不另建資料表。

```json
{
  "date": "2026-07-30",
  "timezone": "Asia/Taipei",
  "rooms": [
    {
      "room_id": "22222222-2222-4222-8222-222222222222",
      "room_name": "大會議A",
      "is_active": true,
      "booked_minutes": 180,
      "business_minutes": 720,
      "busy_ratio": 0.25,
      "confirmed_booking_count": 3
    }
  ]
}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
| `date` | `Asia/Taipei` 的今日日期 |
| `timezone` | 業務日曆時區 |
| `rooms` | 每間會議室的今日摘要，包含停用會議室 |
| `room_id` | 會議室 UUID |
| `room_name` | 會議室名稱 |
| `is_active` | 是否接受新預約 |
| `booked_minutes` | 今日營業時段內已確認預約占用分鐘數 |
| `business_minutes` | 今日可計算的營業分鐘數；平日為 720，週末或假日為 0 |
| `busy_ratio` | `business_minutes` 大於 0 時的占用比例；否則為 0 |
| `confirmed_booking_count` | 今日已確認預約筆數 |

### Endpoint：`GET /api/overview/today`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US2-FR1**：呈現 Asia/Taipei 今日各會議室的忙碌概況 |
| 說明 | 回傳今日每間會議室的預約筆數與忙碌比例 |
| 設計備註 | 「今日」由伺服器依 `Asia/Taipei` 計算；只計 confirmed 預約；無預約仍回傳房間且數值為 0；週末／假日不以除以零計算 |

#### Parameters

無

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "date": "2026-07-30",
  "timezone": "Asia/Taipei",
  "rooms": [
    {
      "room_id": "22222222-2222-4222-8222-222222222222",
      "room_name": "大會議A",
      "is_active": true,
      "booked_minutes": 180,
      "business_minutes": 720,
      "busy_ratio": 0.25,
      "confirmed_booking_count": 3
    },
    {
      "room_id": "66666666-6666-4666-8666-666666666666",
      "room_name": "小會議B",
      "is_active": false,
      "booked_minutes": 0,
      "business_minutes": 720,
      "busy_ratio": 0,
      "confirmed_booking_count": 0
    }
  ]
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 今日含忙碌與空閒會議室 | 200 |
| 今日無任何已確認預約 | 200 |
| 今日為週末或假日 | 200 |
| 未登入查詢 | 401 |

---

## 資料實體：MaintenanceWindow

### 對應 User Story

| US | 描述 |
| --- | --- |
| US1 | 預約前辨識會議室不可用時段 |
| US4 | 設施管理員設定與查閱維護黑名單時段 |

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。

```json
{
  "id": "44444444-4444-4444-8444-444444444444",
  "room_id": "22222222-2222-4222-8222-222222222222",
  "starts_at": "2026-08-01T09:00:00+08:00",
  "ends_at": "2026-08-01T12:00:00+08:00",
  "note": "空調維修",
  "created_by": "55555555-5555-4555-8555-555555555555",
  "created_at": "2026-07-30T03:00:00.000Z"
}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
| `id` | 維護時段 UUID |
| `room_id` | 所屬會議室 UUID |
| `starts_at` | 維護開始瞬間 |
| `ends_at` | 維護結束瞬間 |
| `note` | 可選的維護說明 |
| `created_by` | 建立此維護時段的設施管理員 UUID |
| `created_at` | 建立時間 |

### Endpoint：`POST /api/rooms/{roomId}/maintenance-windows`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US4-FR3**：設施管理員可設定會議室維護黑名單時段<br>- **US4-FR4**：拒絕非設施管理員設定維護時段 |
| 說明 | 為指定會議室新增不可建立預約的維護區間 |
| 設計備註 | 僅 `facility_admin`；`created_by` 取自 session；`ends_at` 必須晚於 `starts_at`；維護區間採半開區間 `[starts_at, ends_at)`；不自動取消既有 confirmed 預約 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | roomId | 是 | 22222222-2222-4222-8222-222222222222 |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "starts_at": "2026-08-01T09:00:00+08:00",
  "ends_at": "2026-08-01T12:00:00+08:00",
  "note": "空調維修"
}
```

#### Responses

##### 201 Created

```json
{
  "id": "44444444-4444-4444-8444-444444444444",
  "room_id": "22222222-2222-4222-8222-222222222222",
  "starts_at": "2026-08-01T09:00:00+08:00",
  "ends_at": "2026-08-01T12:00:00+08:00",
  "note": "空調維修",
  "created_by": "55555555-5555-4555-8555-555555555555",
  "created_at": "2026-07-30T03:00:00.000Z"
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "ends_at must be later than starts_at",
    "details": [
      {
        "field": "ends_at",
        "reason": "must_be_after_starts_at"
      }
    ]
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

##### 403 Forbidden

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Facility administrator role is required",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "ROOM_NOT_FOUND",
    "message": "Room was not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 設施管理員新增有效維護時段 | 201 |
| 時間格式錯誤或結束不晚於開始 | 400 |
| 未登入新增 | 401 |
| 員工或主管新增 | 403 |
| roomId 不存在 | 404 |

---

### Endpoint：`GET /api/rooms/{roomId}/maintenance-windows`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR5**：支援預約前辨識維護不可用時段<br>- **US4-FR3**：支援管理員查閱指定會議室維護時段 |
| 說明 | 查詢指定會議室在時間區間內相交的維護時段 |
| 設計備註 | 已登入三角色皆可查詢，支援預約 UI 預檢與管理畫面；`from`、`to` 皆必填且 `to` 晚於 `from`；結果依 `starts_at` 排序 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | roomId | 是 | 22222222-2222-4222-8222-222222222222 |
| query | from | 是 | 2026-08-01T00:00:00+08:00 |
| query | to | 是 | 2026-08-02T00:00:00+08:00 |

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "room_id": "22222222-2222-4222-8222-222222222222",
  "maintenance_windows": [
    {
      "id": "44444444-4444-4444-8444-444444444444",
      "room_id": "22222222-2222-4222-8222-222222222222",
      "starts_at": "2026-08-01T09:00:00+08:00",
      "ends_at": "2026-08-01T12:00:00+08:00",
      "note": "空調維修",
      "created_by": "55555555-5555-4555-8555-555555555555",
      "created_at": "2026-07-30T03:00:00.000Z"
    }
  ]
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "from and to must be valid ISO-8601 datetimes and to must be later than from",
    "details": []
  }
}
```

##### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "ROOM_NOT_FOUND",
    "message": "Room was not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 查詢區間內有維護時段 | 200 |
| 查詢區間內無維護時段時回空陣列 | 200 |
| from／to 缺漏、格式錯誤或順序無效 | 400 |
| 未登入查詢 | 401 |
| roomId 不存在 | 404 |

---

## 追溯總表（快速 Review）

| Endpoint | US | FR |
| --- | --- | --- |
| `POST /api/auth/login` | US1 | US1-FR1 |
| `POST /api/auth/logout` | US1 | US1-FR1 |
| `GET /api/auth/me` | US1 | US1-FR1 |
| `GET /api/rooms` | US1 | US1-FR2 |
| `POST /api/rooms` | US4 | US4-FR1, US4-FR4 |
| `PATCH /api/rooms/{roomId}` | US4 | US4-FR2, US4-FR4, GR-003 |
| `POST /api/bookings` | US1, US4 | US1-FR3, US1-FR4, US1-FR5, US1-FR6, GR-001, GR-002, GR-003 |
| `GET /api/bookings` | US2 | US2-FR2, US2-FR3, US2-FR4 |
| `GET /api/bookings/mine` | US3 | US3-FR1 |
| `POST /api/bookings/{bookingId}/cancel` | US3 | US3-FR2, US3-FR3, US3-FR4 |
| `GET /api/overview/today` | US2 | US2-FR1 |
| `POST /api/rooms/{roomId}/maintenance-windows` | US4 | US4-FR3, US4-FR4 |
| `GET /api/rooms/{roomId}/maintenance-windows` | US1, US4 | US1-FR5, US4-FR3 |

## 假設

- 所有 `/api` Endpoint 除 `POST /api/auth/login` 外皆要求有效 session cookie；未登入固定回 `401 UNAUTHENTICATED`
- 管理操作只允許 `facility_admin`；`employee` 與 `manager` 權限相同，越權固定回 `403 FORBIDDEN`
- 時段採半開區間 `[starts_at, ends_at)`；相鄰但不重疊的預約或維護時段可成立
- `POST /api/bookings` 的停用、容量、跨日、週末／假日、營業時段與時長違規使用 `400 BOOKING_RULE_VIOLATION`；設備需求欄位僅記錄；預約或維護時段重疊使用 409
- 日曆與列表直接共用 `GET /api/bookings` 回應；第一版不另設 view 參數
- `GET /api/bookings/mine` 第一版回傳全部歷史，不做分頁；預設依開始時間降冪排序
- `GET /api/overview/today` 的 `busy_ratio` 以平日營業窗 09:00–21:00 共 720 分鐘計算；週末或假日的 `business_minutes` 與 `busy_ratio` 皆為 0
- 維護時段查詢對所有已登入角色開放，讓預約畫面可先提示不可用；建立維護時段仍限設施管理員
