# API 計畫：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: 草稿

## API Schema 描述

| 欄位 | 內容 |
| --- | --- |
| 共通 Header | {{COMMON_HEADERS}} |
| 時間格式 | {{DATETIME_FORMAT}} |

## 共通錯誤格式

全檔共用；各 Endpoint 仍須列出會回傳的 error status，並附上對應錯誤範例。

```json
{{COMMON_ERROR_JSON}}
```

---

## 資料實體：{{ENTITY_1_NAME}}

### 對應 User Story

| US | 描述 |
| --- | --- |
{{ENTITY_1_USER_STORY_ROWS}}

### 實體形狀（欄位 + 範例資料）

> 與資料實體 DDL Mapping。

```json
{{ENTITY_1_SHAPE_JSON}}
```

欄位說明（非型別定義）：

| 欄位 | 說明 |
| --- | --- |
{{ENTITY_1_FIELD_DESCRIPTION_ROWS}}

### Endpoint：`{{ENTITY_1_ENDPOINT_1_METHOD_PATH}}`

| 項目 | 內容 |
| --- | --- |
| 對應 FR | {{ENTITY_1_ENDPOINT_1_FR_LINES}} |
| 說明 | {{ENTITY_1_ENDPOINT_1_DESCRIPTION}} |
| 設計備註 | {{ENTITY_1_ENDPOINT_1_DESIGN_NOTES}} |

#### Parameters

{{ENTITY_1_ENDPOINT_1_PARAMETERS}}

#### Request body

{{ENTITY_1_ENDPOINT_1_REQUEST_BODY}}

#### Responses

{{ENTITY_1_ENDPOINT_1_RESPONSE_SECTIONS}}

#### 測試規劃

| 情境 | 預期 Status |
| --- | --- |
{{ENTITY_1_ENDPOINT_1_TEST_ROWS}}

---

{{ENTITY_1_ADDITIONAL_ENDPOINT_SECTIONS}}

{{ADDITIONAL_ENTITY_SECTIONS}}

## 追溯總表（快速 Review）

| Endpoint | US | FR |
| --- | --- |
{{TRACEABILITY_ROWS}}

## 假設

{{ASSUMPTION_LINES}}

<!--
重複區塊填寫指引：
1. ENTITY_1_ADDITIONAL_ENDPOINT_SECTIONS：同一實體的其餘 Endpoint，結構同「### Endpoint」整段（含 Parameters / Request body / Responses / 測試規劃）。
2. ADDITIONAL_ENTITY_SECTIONS：其餘資料實體，結構同「## 資料實體」整段（含 DDL Mapping 提示句與「欄位說明（非型別定義）」）。
3. Parameters 無參數時填「無」；有參數時用表格：位置 / 名稱 / 必填 / 範例。
4. Request body 無 body 時填「無」；有 body 時用 json code fence 完整貼上。
5. Responses 每個 status 使用「##### {status}」標題，並用 json code fence 完整貼上範例（成功與錯誤皆然）。
6. 測試規劃只列「情境名 + 預期 Status」，不寫步驟或断言。
7. 「## 假設」格式與 spec.md 相同：檔案最下方、以 `- ` 條列。高影響未決須在 Endpoint／設計備註等正文使用 `[NEEDS CLARIFICATION: …]`；低風險只寫本節。可對齊上游 spec，並交代本檔暫定取捨。
-->
