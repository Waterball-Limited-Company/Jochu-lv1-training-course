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

本檔為 `api-plan` 面向憲法。跨 skill 堆疊見 `.constitution/core.md`。本檔約束 API 契約形狀；個別功能的 path、業務欄位由該功能之 `api-plan.md` 產物定之。

## 技術約束

- MUST：列表／查詢類 API 使用固定查詢 schema；分頁參數名稱固定為 `page` 與 `pageSize`。
- MUST：每一個 API 的成功與錯誤 response 皆使用固定 envelope。
- MUST：對外錯誤回應至少包含 `error.code` 與 `error.message`。
- MUST：對外資源識別為字串型穩定 UUID。

查詢參數（固定）：

```http
GET /resources?page=1&pageSize=20
```

成功列表 response（固定 envelope）：

```json
{
  "data": [{ "id": "550e8400-e29b-41d4-a716-446655440000" }],
  "meta": { "page": 1, "pageSize": 20, "total": 1 }
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
