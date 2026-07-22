# API 計畫：照片相簿整理應用程式

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-21
**狀態**: 草稿

## API Schema 描述

| 欄位 | 內容 |
| --- | --- |
| 共通 Header | `Content-Type: application/json`（上傳 endpoint 使用 `multipart/form-data`）；本機個人應用，第一版不做登入，無 `Authorization` |
| 時間格式 | ISO-8601 with offset，例如 `2026-07-11T09:00:00+08:00` |

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
| `photo_count` | 相簿內照片數（查詢衍生） |

### Endpoint：`POST /albums`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR1**：系統必須允許使用者建立相簿並命名<br>- **GR-001**：相簿不可嵌套 |
| 說明 | 建立單層相簿 |
| 設計備註 | - `name` 必填且不可空白<br>- 不提供 `parent_album_id` 等巢狀欄位，結構性禁止巢狀<br>- `created_at` 由系統產生，作為日期分組依據 |

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
    "details": []
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
| 對應 FR | - **US2-FR1**：系統必須在主頁面顯示所有相簿<br>- **US2-FR2**：系統必須依相簿建立日期將相簿分組顯示<br>- **US3-FR2**：系統必須保存使用者重新排列後的相簿順序 |
| 說明 | 主頁列出所有相簿，依建立日期分組，分組內依 `sort_order` 排列 |
| 設計備註 | - 無相簿時回空 `groups` 陣列<br>- 無相簿的日期分組不出現（US2 邊界情境）<br>- 分組鍵 `group_date` 由 `created_at` 衍生 |

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
        }
      ]
    },
    {
      "group_date": "2026-06-01",
      "albums": [
        {
          "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X3",
          "name": "畢業季",
          "sort_order": 0,
          "group_date": "2026-06-01",
          "photo_count": 0,
          "created_at": "2026-06-01T12:00:00+08:00",
          "updated_at": "2026-06-01T12:00:00+08:00"
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

### Endpoint：`GET /albums/{albumId}`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US4-FR1**：系統必須允許使用者進入單一相簿查看內容 |
| 說明 | 取得單一相簿摘要 |
| 設計備註 | 照片平鋪列表見 `GET /albums/{albumId}/photos` |

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
  "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "name": "旅行",
  "sort_order": 0,
  "group_date": "2026-07-11",
  "photo_count": 5,
  "created_at": "2026-07-11T09:00:00+08:00",
  "updated_at": "2026-07-20T15:30:00+08:00"
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "album not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 相簿存在 | 200 |
| albumId 不存在 | 404 |

---

### Endpoint：`PUT /albums/reorder`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US3-FR1**：使用者必須能夠在主頁面透過拖放重新排列相簿順序<br>- **US3-FR2**：系統必須保存使用者重新排列後的相簿順序 |
| 說明 | 同建立日期分組內，拖放後批次寫回相簿順序 |
| 設計備註 | - `group_date` 必填，指定要重排的分組<br>- `ordered_album_ids` 必須是該分組內**全部相簿 id 的完整排列**（集合相等、無缺漏、無多餘、無重複）<br>- 含不屬於該分組的 id → `400`<br>- 含未知 id → `404` |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| header | Content-Type | 是 | application/json |

#### Request body

```json
{
  "group_date": "2026-07-11",
  "ordered_album_ids": [
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X2",
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1"
  ]
}
```

#### Responses

##### 200 OK

```json
{
  "group_date": "2026-07-11",
  "ordered_album_ids": [
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X2",
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1"
  ]
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "ordered_album_ids must be a non-empty unique permutation of all albums in the group",
    "details": []
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "one or more albums not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 組內重排成功並可再次讀取維持順序 | 200 |
| 列表含未知 id | 404 |
| 空陣列、重複 id、或缺漏／多餘該分組相簿 | 400 |
| 含不屬於指定 group_date 的相簿 id | 400 |

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
  "file_uri": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
  "thumbnail_uri": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
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
| `file_uri` | 原檔存取 URI（由後端提供靜態服務） |
| `thumbnail_uri` | 平鋪預覽用縮圖 URI；可為 null 時降級顯示原檔 |
| `mime_type` | 影像 MIME 類型 |

### Endpoint：`POST /albums/{albumId}/photos`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US1-FR2**：系統必須允許使用者將照片加入指定相簿<br>- **US1-FR3**：系統必須支援一次選取多張照片匯入，且支援 JPG、PNG、HEIC 等常見格式<br>- **GR-001**：相簿不可嵌套 |
| 說明 | 批次上傳照片至指定相簿 |
| 設計備註 | - 使用 `multipart/form-data`，欄位名 `files`（可多檔）<br>- 只接受 JPG／PNG／HEIC；不支援格式列入 `skipped_files`，不匯入該檔案（US1 邊界情境）<br>- 至少一張支援格式成功匯入時回 `201`（可同時含 `skipped_files`）<br>- 僅當 `files` 為空，或全部為不支援格式且無任何成功匯入時回 `400`<br>- 上傳後複製至 app-managed 目錄並產生縮圖<br>- 每張照片直接綁定 `album_id`（1:N，不重用至其他相簿） |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | albumId | 是 | alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 |
| header | Content-Type | 是 | multipart/form-data |

#### Request body

```
files: （二進位檔案，可多個）
```

#### Responses

##### 201 Created

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "added_photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
      "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
      "display_name": "IMG_20260711_090015.jpg",
      "file_uri": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "thumbnail_uri": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "mime_type": "image/jpeg",
      "created_at": "2026-07-20T14:00:00+08:00"
    }
  ],
  "skipped_files": [
    { "file": "document.pdf", "reason": "only JPG, PNG, HEIC are supported" }
  ]
}
```

##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "no supported files to import",
    "details": [
      { "file": "document.pdf", "reason": "only JPG, PNG, HEIC are supported" }
    ]
  }
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "album not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 批次上傳至少一張支援格式照片成功 | 201 |
| albumId 不存在 | 404 |
| 混合批次：部分支援格式成功、部分不支援 | 201（含 skipped_files） |
| 全部為不支援格式 | 400 |
| files 為空 | 400 |

---

### Endpoint：`GET /albums/{albumId}/photos`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | - **US4-FR1**：系統必須允許使用者進入單一相簿查看內容<br>- **US4-FR2**：系統必須在相簿內以平鋪式介面預覽照片<br>- **US4-FR3**：系統必須在相簿沒有照片時顯示可理解的空狀態 |
| 說明 | 相簿內平鋪預覽所需的照片列表 |
| 設計備註 | - 空相簿回 `photos: []`，由 UI 顯示空狀態<br>- 排序固定依 `created_at` 升冪 |

#### Parameters

| 位置 | 名稱 | 必填 | 範例 |
| --- | --- | --- | --- |
| path | albumId | 是 | alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 |

#### Request body

無

#### Responses

##### 200 OK（有照片）

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
      "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
      "display_name": "IMG_20260711_090015.jpg",
      "file_uri": "/media/uploads/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "thumbnail_uri": "/media/thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "mime_type": "image/jpeg",
      "created_at": "2026-07-20T14:00:00+08:00"
    }
  ]
}
```

##### 200 OK（空相簿）

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "photos": []
}
```

##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "album not found",
    "details": []
  }
}
```

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
| 有多張照片，回傳可平鋪預覽的列表 | 200 |
| 空相簿回空陣列 | 200 |
| albumId 不存在 | 404 |

---

## 追溯總表（快速 Review）

| Endpoint | US | FR |
| --- | --- | --- |
| `POST /albums` | US1 | US1-FR1, GR-001 |
| `GET /albums` | US2, US3 | US2-FR1, US2-FR2, US3-FR2 |
| `GET /albums/{albumId}` | US4 | US4-FR1 |
| `PUT /albums/reorder` | US3 | US3-FR1, US3-FR2 |
| `POST /albums/{albumId}/photos` | US1 | US1-FR2, US1-FR3, GR-001 |
| `GET /albums/{albumId}/photos` | US4 | US4-FR1, US4-FR2, US4-FR3 |

## 假設

- 第一版為單機個人應用，不處理登入、雲端同步、跨裝置或多人共享
- 相簿為單層結構，絕不巢狀
- 拖放重排僅限同一 `group_date` 分組內；跨組拖放不在第一版範圍
- 照片來源為使用者本機檔案上傳；不支援照片庫或自動成冊
- 每張照片只屬於一個相簿；上傳時直接綁定目標 `album_id`
- HEIC 解析依 `sharp` 平台能力；不支援時列入 `skipped_files`；若全部檔案皆無法匯入則回 `400`
- 後端以 `/media/` 靜態路由提供 `file_uri`／`thumbnail_uri` 存取
