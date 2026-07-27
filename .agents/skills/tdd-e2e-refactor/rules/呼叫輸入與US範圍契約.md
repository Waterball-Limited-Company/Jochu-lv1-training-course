# Rule 1 - 呼叫時必須帶齊 US 級必填欄位

- Level: `MUST`
- implement 呼叫 `/tdd-e2e-refactor` 時必須顯式提供：`layer`、`plan-package`（僅目錄名，不含 `specs/`）、單一 User Story 識別、該格 Refactor 實作計畫。
- 缺少必填欄位時必須停止並回報。

## Good Example

- 這個例子是好的，因為四項齊備。

```text
layer: backend
plan-package: 001-photo-albums
US: US-1
Refactor 實作計畫: 去重 albums／photos 資料存取、對齊錯誤形狀
```

## Bad Example

- 這個例子是壞的，因為未指定 US 與計畫就開始大範圍重構。

```text
把 backend 全部重構一遍
```

# Rule 2 - 一次呼叫只處理一個 User Story

- Level: `MUST`
- 一次呼叫只整理一個 US 範圍內、實作計畫點名的程式與測試；不可借機做跨 US 大重構。

## Good Example

- 這個例子是好的，因為鎖在 US-1 相關模組。

```text
只整理 US-1 用到的 albums／photos 路徑
```

## Bad Example

- 這個例子是壞的，因為順便重寫整層架構。

```text
US-1 refactor 順便換目錄結構與全部 US 模組
```
