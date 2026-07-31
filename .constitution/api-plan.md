---
name: api-plan
applies_to:
  - api-plan
---

# 開發規範（憲法）：api-plan

**建立日期**: 2026-07-31
**最後修訂**: 2026-07-31
**狀態**: 生效
**版本**: `1.2.0`

本檔為 `api-plan` 面向憲法。跨 skill 原則與堆疊見 `.constitution/core.md`。本檔約束 API 契約形狀；個別功能的 path、業務欄位由該功能之 `api-plan.md` 產物定之。

## 技術約束

- MUST：列表／查詢類 API 使用固定查詢 schema；分頁參數名稱固定為 `page` 與 `pageSize`（不可每支 API 自創同義參數）。
- MUST：每一個 API 的成功與錯誤 response 皆使用固定 envelope；不可有的 endpoint 直接回陣列、有的回物件、有的把錯誤寫在 200 body 卻無統一形狀。
- MUST：對外錯誤回應至少包含 `error.code` 與 `error.message`（形狀見下方例子）。
- MUST：對外資源識別為字串型穩定 UUID；MUST NOT 將可預測自增整數作為對外主鍵曝露。
- MUST：`api-plan` 產物描述查詢／列表 endpoint 時，MUST 寫出上述查詢參數與 response envelope（可引用本檔例子，不得省略形狀）。
- MUST NOT：把單一功能業務欄位表（例如某 POST body 必填欄）寫進本憲法；那些屬該功能 `api-plan` 產物。

查詢參數（固定）：

```http
GET /resources?page=1&pageSize=20
```

| 參數 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `page` | integer ≥ 1 | 是 | 頁碼；未傳時預設 `1`。 |
| `pageSize` | integer ≥ 1 | 是 | 每頁筆數；專案預設上限由各功能 `api-plan` 聲明，但參數名固定為 `pageSize`。 |

成功列表 response（固定 envelope）：

```json
{
  "data": [
    { "id": "550e8400-e29b-41d4-a716-446655440000" }
  ],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

成功單筆 response（固定 envelope）：

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

錯誤 response（固定 envelope）：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "pageSize must be a positive integer"
  }
}
```
