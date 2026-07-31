# Rule 1 - 呼叫時必須帶齊 US 級必填欄位

- Level: `MUST`
- implement 呼叫 `/tdd-e2e-green` 時必須顯式提供：`layer`（`backend`／`frontend`／`integration`）、`plan-package`（僅目錄名，如 `001-photo-albums`，不含 `specs/`）、單一 User Story 識別（如 `US-1`）、該格 Green 實作計畫。
- 規格路徑一律 `specs/<plan-package>/...`。
- 缺少必填欄位時必須停止並回報，不可自行猜測 `layer`、package 或 US。

## Good Example

- 這個例子是好的，因為 US 級四項齊備。

```text
layer: backend
plan-package: 001-photo-albums
US: US-1
Green 實作計畫:（巢狀條列落地 endpoints）
```

## Bad Example

- 這個例子是壞的，因為未指定 US，卻一次想綠化整層所有故事。

```text
layer: backend
請把所有紅燈都變綠
```

# Rule 2 - 一次呼叫只處理一個 User Story

- Level: `MUST`
- 一次 `/tdd-e2e-green` 只對應一個 US（對齊 task 一格 Green）。
- 不可在同一次呼叫中跨 US 做程式碼實作；本 US 全綠即結束（交回 implement 再呼下一格）。

## Good Example

- 這個例子是好的，因為範圍鎖在 US-1。

```text
僅 US-1 的既有 Red → 全綠
```

## Bad Example

- 這個例子是壞的，因為一次做完 US-1 到 US-4。

```text
順便把後面 US 也綠掉
```

# Rule 3 - 本 US Scenario 範圍必須可收斂

- Level: `MUST`
- 必須能收斂「本 US 要變綠的 Scenario／對應 Red 測」集合：來自 implement 帶入清單，或由該 US 在 `e2e-test-plan.md`／既有測檔與 Green 實作計畫對齊得出。
- 無法對到任何本 US Red 測時必須停止並回報（可能 Red 尚未完成）。

## Good Example

- 這個例子是好的，因為 US-1 對到 S-1-1～S-1-5 的既有測。

```text
US-1 → tests: s-1-1…s-1-5
```

## Bad Example

- 這個例子是壞的，因為找不到本 US 測檔卻開始寫功能。

```text
測檔都還沒有，先把 API 做完再說
```
