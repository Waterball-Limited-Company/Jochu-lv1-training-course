---
name: data-plan
applies_to:
  - data-plan
---

# 開發規範（憲法）：data-plan

**建立日期**: 2026-07-31
**最後修訂**: 2026-07-31
**狀態**: 生效
**版本**: `1.2.0`

本檔為 `data-plan` 面向憲法。跨 skill 堆疊見 `.constitution/core.md`。本檔約束時區語意、稽核與軟刪欄位；個別功能實體與業務欄位由該功能之 `data-plan`／`DDL` 產物定之。

## 技術約束

- MUST：對外顯示與業務日曆語意以 `Asia/Taipei` 解讀；表示某一瞬間之持久化欄位統一使用 `TIMESTAMPTZ`（UTC 瞬間存入），應用層負責轉換。
- MUST：每一個應用資料表皆具備 `created_at`、`updated_at`、`deleted_at` 三欄（軟刪除以 `deleted_at` 為準；未刪除列之 `deleted_at` 為 NULL）。
- MUST：主鍵／對外對應之資源 id 欄位使用 UUID（或等價字串）；MUST NOT 以可預測自增整數作為對外曝露之主鍵。
- MUST：`data-plan` 與 `DDL` 產物描述實體／資料表時，MUST 寫出稽核三欄與時區語意；不得省略或改用同義但不同名之欄位（例如用 `modified` 取代 `updated_at`）。
- MUST：預設查詢應用列時 MUST 排除 `deleted_at IS NOT NULL` 之列，除非該功能規格明確要求包含已軟刪資料。
- MUST NOT：因「以後可能不用軟刪」而省略 `deleted_at`；本憲法之稽核／軟刪欄位優先於 skill 內「spec 未要求則不准預留」之類慣例。

例子（PostgreSQL）：

```sql
CREATE TABLE example_resources (
  id UUID PRIMARY KEY,
  -- …業務欄位…
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ NULL
);
```

`data-plan` 實體欄位列表示意：

| 欄位 | 型別 | 可空 | 說明 |
| --- | --- | --- | --- |
| `created_at` | `TIMESTAMPTZ` | 否 | 建立瞬間（UTC 存入） |
| `updated_at` | `TIMESTAMPTZ` | 否 | 最後更新瞬間（UTC 存入） |
| `deleted_at` | `TIMESTAMPTZ` | 是 | 軟刪瞬間；NULL 表示未刪除 |
