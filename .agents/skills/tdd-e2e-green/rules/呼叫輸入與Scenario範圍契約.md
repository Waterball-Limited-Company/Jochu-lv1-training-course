# Rule 1 - 呼叫時必須帶齊本則必填欄位

- Level: `MUST`
- implement 呼叫 `/tdd-e2e-green` 時必須顯式提供：`layer`（`backend`／`frontend`／`integration`）、`plan-package`（僅目錄名，不含 `specs/`）、本則 ID／標題、該格 Green 實作計畫。
- 本則 ID：後端／前端為 `S-n-m`；整合為 `US-n`。不可改傳整個 User Story 當工作範圍。
- 規格路徑一律 `specs/<plan-package>/...`。
- 缺少必填欄位時必須停止並回報，不可自行猜測 `layer`、package 或本則。

## Good Example

- 這個例子是好的，因為本則四項齊備。

```text
layer: frontend
plan-package: 001-photo-albums
本則: S-1-1
Green 實作計畫: 主頁建立表單 → POST /albums；本則不驗證：批次匯入
```

## Bad Example

- 這個例子是壞的，因為傳整個 US，一次想綠化多則。

```text
layer: frontend
US: US-1
請把本 US 既有 Red 全綠
```

# Rule 2 - 一次呼叫只處理一個 Scenario

- Level: `MUST`
- 一次 `/tdd-e2e-green` 只對應一個 Scenario（整合一個 `US-n` 區塊）。
- 不可在同一次呼叫中把同 US 其他則一併實作；本則變綠即結束（交回 implement 再跑本則 Refactor 或下一則 Red）。

## Good Example

- 這個例子是好的，因為範圍鎖在 S-1-1。

```text
僅 S-1-1 的既有 Red → 本則綠
```

## Bad Example

- 這個例子是壞的，因為一次做完 US-1 全部 Scenario。

```text
順便把 S-1-6、S-1-2 也綠掉
```

# Rule 3 - 本則 Red 測必須可收斂

- Level: `MUST`
- 必須能對到本則既有 Red 測檔（implement 帶入路徑，或由本則 ID 與既有測檔對齊得出）。
- 找不到本則 Red 測時必須停止並回報（可能 Red 尚未完成）。

## Good Example

- 這個例子是好的，因為 S-1-1 對到對應測檔。

```text
S-1-1 → tests/s-1-1-create-album.test.js
```

## Bad Example

- 這個例子是壞的，因為找不到本則測檔卻開始寫功能。

```text
測檔都還沒有，先把建立相簿做完再說
```
