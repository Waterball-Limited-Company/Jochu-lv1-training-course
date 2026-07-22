# API 計畫：照片相簿整理應用程式

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-22
**狀態**: 草稿

## API Schema 描述

| 欄位 | 內容 |
| --- | --- |
| 共通 Header | `Content-Type: application/json`（上傳 endpoint 使用 `multipart/form-data`）；本機個人應用，第一版不做登入 |
| 時間格式 | ISO-8601 with offset，例如 `2026-07-11T09:00:00+08:00` |
| 媒體 URL | 原圖與縮圖經 Express 同 origin 提供，路徑前綴 `/media/`；開發期可經 Vite proxy 轉發 |
| API 前綴 | REST 路徑以 `/api` 為前綴（例如 `POST /api/albums`）；本文 Endpoint 省略前綴以利閱讀 |

## 共通錯誤格式

全檔共用；各 Endpoint 仍須列出會回傳的 error status，並附上對應錯誤範例。

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "name is required",
    "details": []
  }
}
```

---

## 資料實體：Album

### 對應 User Story

| US | 描述 |
| --- | --- |
| US1 | 建立相簿並整理照片 |
| US2 | 在主頁面依日期瀏覽相簿 |
| US3 | 透過拖放重新排列相簿 |

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。

```json
{
  "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "name": "旅行",
  "sort_order": 0,
  "group_date": "2026-07-11",
  "photo_count": 5,
  "created_at": "2026-07-11T09:00:00+08:00",
  "updated_at": "2026-07-20T15:30:00+08:00"
}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
| `id` | 相簿識別 |
| `name` | 可辨識名稱 |
| `sort_order` | 同建立日期分組內的自訂排序 |
| `group_date` | 主頁日期分組鍵，由 `created_at` 日期部分衍生 |
| `photo_count` | 相簿內照片數（查詢衍生，不落庫） |
| `created_at` | 建立時間 |
| `updated_at` | 最後更新時間 |

### Endpoint：`POST /albums`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR1**：系統必須允許使用者建立相簿並命名<br>- **GR-001**：相簿不可嵌套 |
| 說明 | 建立單層相簿 |
| 設計備註 | `name` 必填且不可空白；不提供 `parent_album_id` 或任何巢狀欄位；新建相簿 `sort_order` 預設為同 `group_date` 分組內最大值 + 1（或 `0` 若為該日首筆） |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "name": "旅行"
}
```

#### Responses

##### 201 Created

```json
{
  "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "name": "旅行",
  "sort_order": 0,
  "group_date": "2026-07-11",
  "photo_count": 0,
  "created_at": "2026-07-11T09:00:00+08:00",
  "updated_at": "2026-07-11T09:00:00+08:00"
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "name is required",
    "details": [
      {
        "field": "name",
        "message": "must not be blank"
      }
    ]
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 建立成功 | 201 |
| 缺 name 或 name 空白 | 400 |

---

### Endpoint：`GET /albums`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US2-FR1**：主頁顯示所有相簿<br>- **US2-FR2**：依建立日期分組<br>- **US3-FR2**：持久化排序 |
| 說明 | 主頁列出所有相簿，依 `group_date` 分組，分組內依 `sort_order` 升冪排列 |
| 設計備註 | 無相簿時回空 `groups` 陣列；不顯示沒有相簿的空白日期分組；`group_date` 分組鍵由 `DATE(created_at)` 衍生，不另存可手動覆寫欄位 |

#### Parameters

無

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "groups": [
    {
      "group_date": "2026-07-11",
      "albums": [
        {
          "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
          "name": "旅行",
          "sort_order": 0,
          "group_date": "2026-07-11",
          "photo_count": 5,
          "created_at": "2026-07-11T09:00:00+08:00",
          "updated_at": "2026-07-20T15:30:00+08:00"
        },
        {
          "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2Y2",
          "name": "家庭",
          "sort_order": 1,
          "group_date": "2026-07-11",
          "photo_count": 0,
          "created_at": "2026-07-11T14:30:00+08:00",
          "updated_at": "2026-07-11T14:30:00+08:00"
        }
      ]
    },
    {
      "group_date": "2026-07-20",
      "albums": [
        {
          "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2Z3",
          "name": "工作",
          "sort_order": 0,
          "group_date": "2026-07-20",
          "photo_count": 12,
          "created_at": "2026-07-20T09:00:00+08:00",
          "updated_at": "2026-07-20T09:00:00+08:00"
        }
      ]
    }
  ]
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 有多個相簿，依建立日期分組回傳 | 200 |
| 尚無相簿，回空 groups | 200 |

---

### Endpoint：`PATCH /albums/reorder`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US3-FR1**：使用者必須能夠在主頁面透過拖放重新排列相簿順序<br>- **US3-FR2**：系統必須保存使用者重新排列後的相簿順序 |
| 說明 | 持久化同一 `group_date` 分組內的相簿 `sort_order` |
| 設計備註 | 僅允許同 `group_date` 分組內重排；`album_ids` 必須涵蓋該分組內全部相簿且順序即新 `sort_order`（0 起算）；跨分組拖放應在前端阻止，後端若偵測到跨組或遺漏 ID 回 400；不修改 `created_at` |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "group_date": "2026-07-11",
  "album_ids": [
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2Y2",
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1"
  ]
}
```

#### Responses

##### 200 OK

```json
{
  "group_date": "2026-07-11",
  "albums": [
    {
      "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2Y2",
      "name": "家庭",
      "sort_order": 0,
      "group_date": "2026-07-11",
      "photo_count": 0,
      "created_at": "2026-07-11T14:30:00+08:00",
      "updated_at": "2026-07-22T10:00:00+08:00"
    },
    {
      "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
      "name": "旅行",
      "sort_order": 1,
      "group_date": "2026-07-11",
      "photo_count": 5,
      "created_at": "2026-07-11T09:00:00+08:00",
      "updated_at": "2026-07-22T10:00:00+08:00"
    }
  ]
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "album_ids must include all albums in the same group_date",
    "details": [
      {
        "field": "album_ids",
        "message": "missing album alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 for group_date 2026-07-11"
      }
    ]
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "group_date has no albums",
    "details": [
      {
        "field": "group_date",
        "message": "2026-01-01"
      }
    ]
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 同 group_date 內重排成功 | 200 |
| album_ids 遺漏該分組內相簿 | 400 |
| group_date 不存在或無相簿 | 404 |
| 僅一個相簿時重排（順序不變） | 200 |

---

## 資料實體：Photo

### 對應 User Story

| US | 描述 |
| --- | --- |
| US1 | 建立相簿並整理照片 |
| US4 | 在相簿內以平鋪方式預覽照片 |

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。

```json
{
  "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "display_name": "IMG_20260711_090015.jpg",
  "original_url": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
  "thumbnail_url": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.webp",
  "mime_type": "image/jpeg",
  "created_at": "2026-07-20T14:00:00+08:00"
}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
| `id` | 照片識別 |
| `album_id` | 所屬相簿 |
| `display_name` | 列表／平鋪可辨識名稱 |
| `original_url` | 原圖 HTTP URL，對應 DB `file_path` 經 `/media/` 映射 |
| `thumbnail_url` | 縮圖 HTTP URL，對應 DB `thumbnail_path`；縮圖產生失敗時可為 `null`，前端降級顯示 `original_url` |
| `mime_type` | 影像 MIME，限 `image/jpeg`、`image/png`、`image/webp` |
| `created_at` | 加入相簿時間；平鋪預覽依此升冪排序 |

### Endpoint：`POST /albums/:albumId/photos`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR2**：系統必須允許使用者將照片加入指定相簿<br>- **US1-FR3**：系統必須支援一次選取多張 JPEG、PNG 或 WebP 照片匯入 |
| 說明 | 以 multipart 一次上傳多張照片至指定相簿 |
| 設計備註 | 僅接受 JPEG／PNG／WebP（不含 HEIC）；以檔案內容驗證 MIME；上傳後複製原檔至 app-managed 目錄並以 `sharp` 產生縮圖；縮圖失敗仍保留原圖，`thumbnail_url` 可為 `null`；部分檔案格式不符時整批拒絕或回傳 per-file 錯誤（第一版採整批拒絕並在 `details` 列出不支援檔名） |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | albumId | 是 | alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 |
| header | Content-Type | 是 | multipart/form-data |

#### Request body

`multipart/form-data`，欄位 `files` 可重複多次以承載多檔：

| 欄位 | 必填 | 說明 |
| --- | --- | --- |
| `files` | 是 | 一或多個影像檔（JPEG／PNG／WebP） |

#### Responses

##### 201 Created

```json
{
  "photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
      "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
      "display_name": "IMG_20260711_090015.jpg",
      "original_url": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "thumbnail_url": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.webp",
      "mime_type": "image/jpeg",
      "created_at": "2026-07-22T10:15:00+08:00"
    },
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K1",
      "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
      "display_name": "screenshot.png",
      "original_url": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K1.png",
      "thumbnail_url": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K1.webp",
      "mime_type": "image/png",
      "created_at": "2026-07-22T10:15:01+08:00"
    }
  ]
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "no files provided",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "album not found",
    "details": [
      {
        "field": "albumId",
        "message": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1"
      }
    ]
  }
}
```

##### 415 Unsupported Media Type

```json
{
  "error": {
    "code": "UNSUPPORTED_MEDIA_TYPE",
    "message": "only JPEG, PNG, and WebP are supported",
    "details": [
      {
        "field": "files",
        "message": "vacation.heic is not a supported image format"
      }
    ]
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 一次上傳多張 JPEG／PNG／WebP 成功 | 201 |
| 未附任何檔案 | 400 |
| 相簿不存在 | 404 |
| 含 HEIC 或其他不支援格式 | 415 |

---

### Endpoint：`PATCH /photos/:id`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR4**：將已屬於某相簿的照片加入另一相簿時，必須從原相簿移出<br>- **GR-002**：一張照片同一時間只屬於一個相簿 |
| 說明 | 變更照片所屬相簿（移動） |
| 設計備註 | 以 `UPDATE photos SET album_id = ?` 覆寫歸屬，不保留多重歸屬；目標相簿必須存在；不提供巢狀或相簿內子集合 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | id | 是 | pho_01HZX3A1B2C3D4E5F6G7H8J9K0 |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2Y2"
}
```

#### Responses

##### 200 OK

```json
{
  "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2Y2",
  "display_name": "IMG_20260711_090015.jpg",
  "original_url": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
  "thumbnail_url": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.webp",
  "mime_type": "image/jpeg",
  "created_at": "2026-07-20T14:00:00+08:00"
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "album_id is required",
    "details": [
      {
        "field": "album_id",
        "message": "must not be blank"
      }
    ]
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "photo or target album not found",
    "details": [
      {
        "field": "id",
        "message": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0"
      }
    ]
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 移動至另一相簿成功 | 200 |
| 缺 album_id | 400 |
| 照片或目標相簿不存在 | 404 |
| 移動至同一相簿（無實質變更） | 200 |

---

### Endpoint：`GET /albums/:albumId/photos`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US4-FR1**：允許使用者進入單一相簿查看內容<br>- **US4-FR2**：在相簿內以平鋪式介面預覽照片<br>- **US4-FR3**：相簿沒有照片時顯示可理解的空狀態 |
| 說明 | 取得指定相簿內照片平鋪列表，含 `thumbnail_url` |
| 設計備註 | 依 `created_at` 升冪排序；空相簿回空 `photos` 陣列（HTTP 200），由前端呈現空狀態；`thumbnail_url` 為 `null` 時前端以 `original_url` 降級顯示 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | albumId | 是 | alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 |

#### Request body

無

#### Responses

##### 200 OK

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
      "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
      "display_name": "IMG_20260711_090015.jpg",
      "original_url": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "thumbnail_url": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.webp",
      "mime_type": "image/jpeg",
      "created_at": "2026-07-20T14:00:00+08:00"
    },
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K1",
      "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
      "display_name": "screenshot.png",
      "original_url": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K1.png",
      "thumbnail_url": null,
      "mime_type": "image/png",
      "created_at": "2026-07-20T14:05:00+08:00"
    }
  ]
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "album not found",
    "details": [
      {
        "field": "albumId",
        "message": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1"
      }
    ]
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 相簿含多張照片，依 created_at 升冪回傳 | 200 |
| 空相簿回空 photos 陣列 | 200 |
| 相簿不存在 | 404 |

---

## 追溯總表（快速 Review）

| Endpoint | US | FR |
| --- | --- | --- |
| POST /albums | US1 | US1-FR1, GR-001 |
| GET /albums | US2, US3 | US2-FR1, US2-FR2, US3-FR2 |
| PATCH /albums/reorder | US3 | US3-FR1, US3-FR2 |
| POST /albums/:albumId/photos | US1 | US1-FR2, US1-FR3 |
| PATCH /photos/:id | US1 | US1-FR4, GR-002 |
| GET /albums/:albumId/photos | US4 | US4-FR1, US4-FR2, US4-FR3 |

## 假設

- 第一版為單機個人應用，不做登入與授權；所有 Endpoint 無需認證 Header
- 相簿為單層結構，絕不巢狀；不提供 `parent_album_id` 或相簿對相簿關聯
- 主頁先依 `DATE(created_at)` 分組為 `group_date`，組內依 `sort_order` 排列；拖放重排僅限同 `group_date` 分組內
- 一張照片同一時間只屬於一個相簿；移動以 `PATCH /photos/:id` 覆寫 `album_id` 表達
- 僅支援 JPEG、PNG、WebP；HEIC 與其他格式回 415（或等價 400）；以檔案內容驗證 MIME
- 上傳後原檔與縮圖寫入 app-managed 目錄；API 以 `/media/` URL 暴露，不直接回傳 DB 相對路徑欄位名
- 縮圖產生失敗時仍保留原圖，`thumbnail_url` 可為 `null`，前端降級顯示 `original_url`
- 平鋪預覽固定依 `photos.created_at` 升冪；第一版不提供相簿內拖放排序
- 空相簿仍保留相簿列；`GET /albums/:albumId/photos` 對空相簿回 200 與空陣列，空狀態由前端呈現
- 刪除相簿時 cascade 刪除所屬照片與實體檔（規格未另定刪除 API；低風險預設，本期不另開 DELETE Endpoint）
- REST 路徑實際掛載於 Express `/api` 前綴下；開發期 Vite proxy 轉發 `/api` 與 `/media`
