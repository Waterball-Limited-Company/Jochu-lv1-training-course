# API 計畫：照片相簿整理

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-20
**狀態**: 草稿

## API Schema 描述


| 欄位        | 內容                                                                                                                                           |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 共通 Header | `Content-Type: application/json`（本機個人應用；第一版不做登入，無 `Authorization`）                                                                           |
| 時間格式      | ISO-8601 with offset，例如 `2026-07-11T09:00:00+08:00`                                                                                          |


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


| US   | 描述                |
| ---- | ----------------- |
| US-1 | 手動建立相簿並在相簿內加入照片   |
| US-2 | 以平鋪介面預覽相簿內照片      |
| US-3 | 在主頁依日期分組查看並拖放重排相簿 |
| US-5 | 依日期自動產生相簿         |




### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。

```json
{
  "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "name": "旅行",
  "source": "manual",
  "group_date": "2026-07-11",
  "sort_order": 0,
  "photo_count": 12,
  "created_at": "2026-07-11T09:00:00+08:00",
  "updated_at": "2026-07-20T15:30:00+08:00"
}
```

欄位說明（非型別定義）：


| 欄位            | 說明                        |
| ------------- | ------------------------- |
| `id`          | 相簿識別                      |
| `name`        | 可辨識名稱；自動成冊時可為日期導向名稱       |
| `source`      | `manual` 或 `auto_date`    |
| `group_date`  | 主頁日期分組用的日期鍵（自動成冊通常等於成冊日期） |
| `sort_order`  | 主頁拖放後的自訂順序                |
| `photo_count` | 相簿內照片數（列表／空狀態判斷用）         |




### Endpoint：`POST /albums`


| 項目    | 內容                                                                                                                                                                         |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 對應 FR | - **FR-001**: 系統必須允許使用者建立新的相簿，並為相簿指定可辨識的名稱 - **FR-003**: 系統必須確保相簿只能以單層結構存在，不可把相簿放進另一個相簿                                                                                    |
| 說明    | 手動建立單層相簿                                                                                                                                                                   |
| 設計備註  | - `name` 必填且不可空白 - `group_date` 可選；省略時預設為本機當日（`YYYY-MM-DD`） - 若有傳入必須是有效日期，否則 `400` - FR-003 以「不提供 `parent_album_id` 等巢狀欄位／endpoint」結構性禁止巢狀，而非另開錯誤碼 - `source` 固定為 `manual` |




#### Parameters


| 位置     | 名稱           | 必填  | 範例               |
| ------ | ------------ | --- | ---------------- |
| header | Content-Type | 是   | application/json |




#### Request body

```json
{
  "name": "旅行",
  "group_date": "2026-07-11"
}
```



#### Responses



##### 201 Created

```json
{
  "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "name": "旅行",
  "source": "manual",
  "group_date": "2026-07-11",
  "sort_order": 0,
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

> 無效 `group_date`（非 `YYYY-MM-DD` 或無法解析）同樣回 `400`，`message` 為 `group_date must be a valid YYYY-MM-DD date`。



#### 測試規劃


| 情境                    | 預期 Status |
| --------------------- | --------- |
| 建立成功（含或不含 group_date） | 201       |
| 缺 name 或 name 空白      | 400       |
| group_date 格式無效       | 400       |


---



### Endpoint：`GET /albums`


| 項目    | 內容                                                                                       |
| ----- | ---------------------------------------------------------------------------------------- |
| 對應 FR | - **FR-008**: 系統必須在主頁列出所有相簿，並依日期進行分組顯示 - **FR-010**: 系統必須在使用者重新打開主頁後，維持其拖放後的排列結果         |
| 說明    | - 主頁列出所有相簿 - 回應依日期分組，分組內依 `sort_order` 排列                                                |
| 設計備註  | - 日期分組與拖放自訂順序的精確共存規則仍待 spec 澄清 - 第一版假設「先依 `group_date` 分組，組內依 `sort_order`」 - 無相簿時回空分組列表 |




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
          "source": "manual",
          "group_date": "2026-07-11",
          "sort_order": 0,
          "photo_count": 12,
          "created_at": "2026-07-11T09:00:00+08:00",
          "updated_at": "2026-07-20T15:30:00+08:00"
        },
        {
          "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X2",
          "name": "2026-07-11",
          "source": "auto_date",
          "group_date": "2026-07-11",
          "sort_order": 1,
          "photo_count": 2,
          "created_at": "2026-07-20T10:00:00+08:00",
          "updated_at": "2026-07-20T10:00:00+08:00"
        }
      ]
    },
    {
      "group_date": "2026-06-01",
      "albums": [
        {
          "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X3",
          "name": "畢業季",
          "source": "manual",
          "group_date": "2026-06-01",
          "sort_order": 0,
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


| 情境             | 預期 Status |
| -------------- | --------- |
| 有多個相簿，依日期分組回傳  | 200       |
| 尚無相簿，回空 groups | 200       |


---



### Endpoint：`GET /albums/{albumId}`


| 項目    | 內容                                       |
| ----- | ---------------------------------------- |
| 對應 FR | - **FR-005**: 使用者必須能打開任一已建立的相簿，查看其中的照片   |
| 說明    | 取得單一相簿摘要（進入相簿頁前的資源讀取）                    |
| 設計備註  | - 照片平鋪列表見 `GET /albums/{albumId}/photos` |




#### Parameters


| 位置   | 名稱      | 必填  | 範例                             |
| ---- | ------- | --- | ------------------------------ |
| path | albumId | 是   | alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 |




#### Request body

無

#### Responses



##### 200 OK

```json
{
  "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "name": "旅行",
  "source": "manual",
  "group_date": "2026-07-11",
  "sort_order": 0,
  "photo_count": 12,
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


| 情境          | 預期 Status |
| ----------- | --------- |
| 相簿存在        | 200       |
| albumId 不存在 | 404       |


---



### Endpoint：`PUT /albums/reorder`


| 項目    | 內容                                                                                                                                                               |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 對應 FR | - **FR-009**: 使用者必須能在主頁上透過拖放重新排列相簿順序 - **FR-010**: 系統必須在使用者重新打開主頁後，維持其拖放後的排列結果                                                                                   |
| 說明    | 主頁拖放後批次寫回相簿順序                                                                                                                                                    |
| 設計備註  | - `ordered_album_ids` 必須是**現有全部相簿 id 的完整排列**（集合相等、無缺漏、無多餘、無重複） - 與日期分組共存規則待澄清；此 API 只持久化 `sort_order`，分組鍵仍用 `group_date` - 缺漏／多餘／重複／空陣列 → `400` - 含未知 id → `404` |




#### Parameters


| 位置     | 名稱           | 必填  | 範例               |
| ------ | ------------ | --- | ---------------- |
| header | Content-Type | 是   | application/json |




#### Request body

```json
{
  "ordered_album_ids": [
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X2",
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X3"
  ]
}
```



#### Responses



##### 200 OK

```json
{
  "ordered_album_ids": [
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X2",
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
    "alb_01HZX2K9M3Q8R7N6P5T4V3W2X3"
  ]
}
```



##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "ordered_album_ids must be a non-empty unique permutation of all existing album ids",
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


| 情境                   | 預期 Status |
| -------------------- | --------- |
| 重排成功並可再次讀取維持順序       | 200       |
| 列表含未知 id             | 404       |
| 空陣列、重複 id、或缺漏／多餘既有相簿 | 400       |


---



### Endpoint：`POST /albums/auto-generate-by-date`


| 項目    | 內容                                                                                                                                                                                                                                           |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 對應 FR | - **FR-014**: 系統必須能依照片的日期資訊，自動產生對應的相簿 - **FR-015**: 自動產生的相簿必須與手動建立的相簿一樣，可在主頁被查看，且同樣不可巢狀 - **FR-016**: 當照片具備可用日期資訊時，系統必須把該照片歸入對應的自動日期相簿                                                                                                       |
| 說明    | - 依既有照片日期資訊自動產生／更新日期相簿 - 把照片歸入對應自動相簿                                                                                                                                                                                                         |
| 設計備註  | - 自動成冊粒度（日／月／年）仍待澄清；第一版假設以「日」為單位，`name` 與 `group_date` 使用該日 - 缺日期照片略過並回報 `skipped_without_date` - `photo_ids`：**省略**＝對照片庫中尚未歸入任何 `auto_date` 相簿的照片執行；**空陣列**＝`400`；**有值**＝只處理列出的 id（去重後執行） - 未知 id → `404`（與 assign 一致） - 與「一張照片可否屬多個相簿」決策連動 |




#### Parameters


| 位置     | 名稱           | 必填  | 範例               |
| ------ | ------------ | --- | ---------------- |
| header | Content-Type | 是   | application/json |




#### Request body

```json
{
  "photo_ids": [
    "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
    "pho_01HZX3A1B2C3D4E5F6G7H8J9K1"
  ]
}
```

> 省略 `photo_ids` 欄位時，對照片庫中尚未歸入任何 `auto_date` 相簿的照片執行成冊。不可傳空陣列。



#### Responses



##### 200 OK

```json
{
  "generated_albums": [
    {
      "id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X2",
      "name": "2026-07-11",
      "source": "auto_date",
      "group_date": "2026-07-11",
      "sort_order": 1,
      "photo_count": 2,
      "created_at": "2026-07-20T10:00:00+08:00",
      "updated_at": "2026-07-20T10:00:00+08:00"
    }
  ],
  "assigned_photo_count": 2,
  "skipped_without_date": 0
}
```



##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "photo_ids must not be an empty array; omit the field to process all eligible library photos",
    "details": []
  }
}
```



##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "one or more photos not found",
    "details": []
  }
}
```



#### 測試規劃


| 情境                   | 預期 Status |
| -------------------- | --------- |
| 具日期照片成功產生自動相簿並可在主頁看到 | 200       |
| 與既有手動相簿並存、皆為單層       | 200       |
| photo_ids 為空陣列       | 400       |
| photo_ids 含未知 id     | 404       |


---



## 資料實體：Photo



### 對應 User Story


| US   | 描述              |
| ---- | --------------- |
| US-1 | 手動建立相簿並在相簿內加入照片 |
| US-2 | 以平鋪介面預覽相簿內照片    |
| US-4 | 從照片庫將照片分配到相簿    |
| US-5 | 依日期自動產生相簿       |




### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。

```json
{
  "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
  "display_name": "IMG_20260711_090015.jpg",
  "source_path": "/Users/demo/Pictures/IMG_20260711_090015.jpg",
  "taken_at": "2026-07-11T09:00:15+08:00",
  "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
  "in_library": true,
  "created_at": "2026-07-20T14:00:00+08:00"
}
```

欄位說明（非型別定義）：


| 欄位              | 說明                        |
| --------------- | ------------------------- |
| `id`            | 照片識別                      |
| `display_name`  | 列表／平鋪可辨識名稱                |
| `source_path`   | 本機來源路徑                    |
| `taken_at`      | 照片日期；自動成冊依據；可能為 null（缺日期） |
| `thumbnail_uri` | 平鋪預覽用縮圖 URI               |
| `in_library`    | 是否仍出現在照片庫                 |




---



### Endpoint：`POST /albums/{albumId}/photos`


| 項目    | 內容                                                                                                                                                                                                                               |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 對應 FR | - **FR-002**: 系統必須允許使用者進入某個相簿後，從本機選擇照片加入該相簿 - **FR-003**: 系統必須確保相簿只能以單層結構存在，不可把相簿放進另一個相簿 - **FR-004**: 使用者完成加入後，系統必須讓使用者能確認照片已進入該相簿                                                                                              |
| 說明    | 進入相簿後，從本機選擇檔案加入該相簿（必要時一併進入照片庫）                                                                                                                                                                                                   |
| 設計備註  | - 從本機檔案加入相簿：若 `source_path` 尚不存在於照片庫，先建立 Photo 再建立關聯；若已存在於照片庫，**重用既有 Photo** 只建立關聯（不新建 id） - 同一相簿已含該 Photo 時回 `409` - 巢狀相簿以結構禁止（無 parent 欄位），本 endpoint 不另定義 `UNSUPPORTED_OPERATION` - 各 Endpoint 的 JSON 範例為**獨立情境**，不假設跨章節同一執行序 |




#### Parameters


| 位置     | 名稱           | 必填  | 範例                             |
| ------ | ------------ | --- | ------------------------------ |
| path   | albumId      | 是   | alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 |
| header | Content-Type | 是   | application/json               |




#### Request body

```json
{
  "local_files": [
    {
      "source_path": "/Users/demo/Pictures/IMG_20260711_090015.jpg",
      "display_name": "IMG_20260711_090015.jpg",
      "taken_at": "2026-07-11T09:00:15+08:00"
    }
  ]
}
```



#### Responses



##### 201 Created

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X1",
  "added_photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K0",
      "display_name": "IMG_20260711_090015.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260711_090015.jpg",
      "taken_at": "2026-07-11T09:00:15+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "in_library": true,
      "created_at": "2026-07-20T14:00:00+08:00"
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
    "details": []
  }
}
```



##### 409 Conflict

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "photo already exists in this album",
    "details": []
  }
}
```



##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "local_files must be a non-empty array",
    "details": []
  }
}
```



#### 測試規劃


| 情境              | 預期 Status |
| --------------- | --------- |
| 建立相簿後加入至少一張照片成功 | 201       |
| albumId 不存在     | 404       |
| 同一相簿重複加入同一本機照片  | 409       |
| local_files 為空  | 400       |


---



### Endpoint：`GET /albums/{albumId}/photos`


| 項目    | 內容                                                                                                                                        |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 對應 FR | - **FR-005**: 使用者必須能打開任一已建立的相簿，查看其中的照片 - **FR-006**: 系統必須以平鋪式介面呈現相簿內照片預覽，讓使用者能一次看到多張縮圖 - **FR-007**: 當相簿內沒有任何照片時，系統必須顯示空狀態，讓使用者知道可以開始加入照片 |
| 說明    | 相簿內平鋪預覽所需的照片列表（含縮圖）                                                                                                                       |
| 設計備註  | - 空相簿回 `photos: []`，由 UI 顯示空狀態 - 欄數／排序是否可調仍待澄清；第一版固定回傳順序（例如 `created_at` 升冪），不提供排序 query                                                  |




#### Parameters


| 位置   | 名稱      | 必填  | 範例                             |
| ---- | ------- | --- | ------------------------------ |
| path | albumId | 是   | alb_01HZX2K9M3Q8R7N6P5T4V3W2X1 |




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
      "display_name": "IMG_20260711_090015.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260711_090015.jpg",
      "taken_at": "2026-07-11T09:00:15+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K0.jpg",
      "in_library": true,
      "created_at": "2026-07-20T14:00:00+08:00"
    },
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K1",
      "display_name": "IMG_20260711_100000.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260711_100000.jpg",
      "taken_at": "2026-07-11T10:00:00+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K1.jpg",
      "in_library": true,
      "created_at": "2026-07-20T14:05:00+08:00"
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


| 情境               | 預期 Status |
| ---------------- | --------- |
| 有多張照片，回傳可平鋪預覽的列表 | 200       |
| 空相簿回空陣列          | 200       |
| albumId 不存在      | 404       |


---



### Endpoint：`POST /photos/library`


| 項目    | 內容                                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------------- |
| 對應 FR | - **FR-011**: 系統必須提供照片庫，讓使用者可匯入並查看尚未或不限於特定相簿的本機照片                                                                               |
| 說明    | 將本機照片匯入照片庫（不必然立刻屬於某個相簿）                                                                                                         |
| 設計備註  | - 照片庫為空時由 `GET /photos/library` 回空列表，UI 顯示匯入引導 - 若 `source_path` 已存在於照片庫回 `409` - 本範例使用尚未出現在其他 endpoint 成功回應中的路徑，避免與「相簿內加入」範例衝突 |




#### Parameters


| 位置     | 名稱           | 必填  | 範例               |
| ------ | ------------ | --- | ---------------- |
| header | Content-Type | 是   | application/json |




#### Request body

```json
{
  "local_files": [
    {
      "source_path": "/Users/demo/Pictures/IMG_20260601_120000.jpg",
      "display_name": "IMG_20260601_120000.jpg",
      "taken_at": "2026-06-01T12:00:00+08:00"
    },
    {
      "source_path": "/Users/demo/Pictures/IMG_20260615_180000.jpg",
      "display_name": "IMG_20260615_180000.jpg",
      "taken_at": "2026-06-15T18:00:00+08:00"
    }
  ]
}
```



#### Responses



##### 201 Created

```json
{
  "imported_photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K2",
      "display_name": "IMG_20260601_120000.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260601_120000.jpg",
      "taken_at": "2026-06-01T12:00:00+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K2.jpg",
      "in_library": true,
      "created_at": "2026-07-20T16:00:00+08:00"
    },
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K3",
      "display_name": "IMG_20260615_180000.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260615_180000.jpg",
      "taken_at": "2026-06-15T18:00:00+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K3.jpg",
      "in_library": true,
      "created_at": "2026-07-20T16:00:00+08:00"
    }
  ]
}
```



##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "local_files must be a non-empty array",
    "details": []
  }
}
```



##### 409 Conflict

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "photo with the same source_path already exists in library",
    "details": []
  }
}
```



#### 測試規劃


| 情境                 | 預期 Status |
| ------------------ | --------- |
| 匯入多張照片到照片庫成功       | 201       |
| local_files 為空     | 400       |
| 重複匯入相同 source_path | 409       |


---



### Endpoint：`GET /photos/library`


| 項目    | 內容                                                          |
| ----- | ----------------------------------------------------------- |
| 對應 FR | - **FR-011**: 系統必須提供照片庫，讓使用者可匯入並查看尚未或不限於特定相簿的本機照片           |
| 說明    | 查看照片庫中可選取／可分配的照片                                            |
| 設計備註  | - 「分配到相簿後是否仍留在庫中」待澄清 - 第一版假設仍留在庫中（`in_library: true`），可再次分配 |




#### Parameters

無

#### Request body

無

#### Responses



##### 200 OK（有照片）

```json
{
  "photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K2",
      "display_name": "IMG_20260601_120000.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260601_120000.jpg",
      "taken_at": "2026-06-01T12:00:00+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K2.jpg",
      "in_library": true,
      "created_at": "2026-07-20T16:00:00+08:00"
    },
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K3",
      "display_name": "IMG_20260615_180000.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260615_180000.jpg",
      "taken_at": "2026-06-15T18:00:00+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K3.jpg",
      "in_library": true,
      "created_at": "2026-07-20T16:00:00+08:00"
    }
  ]
}
```



##### 200 OK（空庫）

```json
{
  "photos": []
}
```



#### 測試規劃


| 情境          | 預期 Status |
| ----------- | --------- |
| 庫中有照片可查看與選取 | 200       |
| 空庫回空陣列      | 200       |


---



### Endpoint：`POST /photos/library/assign`


| 項目    | 內容                                                                                                                                   |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 對應 FR | - **FR-012**: 使用者必須能從照片庫選取照片，並將其分配到指定相簿 - **FR-013**: 分配完成後，系統必須讓使用者在目標相簿中看到這些照片                                                     |
| 說明    | 從照片庫選取照片，分配到指定相簿                                                                                                                     |
| 設計備註  | - 目標相簿已含相同照片時回 `409` - 多相簿歸屬規則待澄清；第一版允許同一 `photo_id` 被 assign 到**不同**相簿 - 本成功範例將庫中照片分配到「畢業季」相簿（`alb_...X3`），避免與「相簿內加入旅行相簿」成功範例使用同一目標 |




#### Parameters


| 位置     | 名稱           | 必填  | 範例               |
| ------ | ------------ | --- | ---------------- |
| header | Content-Type | 是   | application/json |




#### Request body

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X3",
  "photo_ids": [
    "pho_01HZX3A1B2C3D4E5F6G7H8J9K2",
    "pho_01HZX3A1B2C3D4E5F6G7H8J9K3"
  ]
}
```



#### Responses



##### 200 OK

```json
{
  "album_id": "alb_01HZX2K9M3Q8R7N6P5T4V3W2X3",
  "assigned_photos": [
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K2",
      "display_name": "IMG_20260601_120000.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260601_120000.jpg",
      "taken_at": "2026-06-01T12:00:00+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K2.jpg",
      "in_library": true,
      "created_at": "2026-07-20T16:00:00+08:00"
    },
    {
      "id": "pho_01HZX3A1B2C3D4E5F6G7H8J9K3",
      "display_name": "IMG_20260615_180000.jpg",
      "source_path": "/Users/demo/Pictures/IMG_20260615_180000.jpg",
      "taken_at": "2026-06-15T18:00:00+08:00",
      "thumbnail_uri": "local://thumbs/pho_01HZX3A1B2C3D4E5F6G7H8J9K3.jpg",
      "in_library": true,
      "created_at": "2026-07-20T16:00:00+08:00"
    }
  ]
}
```



##### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "album or photo not found",
    "details": []
  }
}
```



##### 409 Conflict

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "one or more photos already exist in the target album",
    "details": []
  }
}
```



##### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "photo_ids must be a non-empty array",
    "details": []
  }
}
```



#### 測試規劃


| 情境            | 預期 Status |
| ------------- | --------- |
| 從照片庫分配到既有相簿成功 | 200       |
| 目標相簿或照片不存在    | 404       |
| 目標相簿已含相同照片    | 409       |
| photo_ids 為空  | 400       |


---



## 追溯總表（快速 Review）


| Endpoint                             | US         | FR                     |
| ------------------------------------ | ---------- | ---------------------- |
| `POST /albums`                       | US-1       | FR-001, FR-003         |
| `GET /albums`                        | US-3, US-5 | FR-008, FR-010         |
| `GET /albums/{albumId}`              | US-2       | FR-005                 |
| `PUT /albums/reorder`                | US-3       | FR-009, FR-010         |
| `POST /albums/auto-generate-by-date` | US-5       | FR-014, FR-015, FR-016 |
| `POST /albums/{albumId}/photos`      | US-1       | FR-002, FR-003, FR-004 |
| `GET /albums/{albumId}/photos`       | US-2       | FR-005, FR-006, FR-007 |
| `POST /photos/library`               | US-4       | FR-011                 |
| `GET /photos/library`                | US-4       | FR-011                 |
| `POST /photos/library/assign`        | US-4       | FR-012, FR-013         |



## 假設

- 第一版為單機個人應用，資料保存在本機，不處理登入、雲端同步、跨裝置或多人共享
- 相簿為單層結構，絕不巢狀
- 「依日期分組」至少適用於主頁上的相簿呈現；自動成冊則是另外一條依日期產生相簿的能力
- 照片來源為使用者本機既有檔案；第一版不承諾相機即時拍攝或外部雲端相簿串接
- 主頁拖放重排與日期分組的精確共存規則、一張照片是否可屬多個相簿、自動成冊粒度，以及平鋪預覽是否可調欄數／排序，待後續澄清後回寫

