# Rule 1 - Green 必須承接同一代理的 Red 證據

- Level: `MUST`
- Scenario Agent 呼叫 `/tdd-e2e-green` 時必須提供：與 Red 相同的 `scenario-agent-id`、`layer`（僅 `backend`／`frontend`）、`plan-package`、`user-story`、本則 `S-n-m` ID／標題、Green 實作計畫、Red 測檔，以及「正確紅燈」或「既有綠燈且敏感度已驗證」證據。
- 缺有效 Red 階段證據、代理識別不同或 `layer=integration` 時停止；不可改傳整個 User Story 當工作範圍。
- 若是既有綠燈，Green 不再硬改產品程式碼；只確認本則與既有綠燈全套通過，將本階段回報為已由既有實作滿足。

## Good Example

```text
scenario-agent-id: frontend-US-1-S-1-1
layer: frontend
plan-package: 001-photo-albums
user-story: US-1
本則: S-1-1
Red: 主頁缺少「旅行」，value difference
```

## Bad Example

```text
新代理沒有 Red 輸出，直接開始做 US-1 全部功能
```

# Rule 2 - 一次只綠一個 Scenario

- Level: `MUST`
- 一次 `/tdd-e2e-green` 只對應一個後端或前端 Scenario。
- 不可把同 User Story 其他 Scenario 一併實作；本則變綠後回到同一 Scenario Agent 接續 Refactor。

## Good Example

```text
S-1-1 的 Red → 最少實作 → S-1-1 綠
```

## Bad Example

```text
順便把 S-1-2 與 S-1-3 一起做完
```

# Rule 3 - 本則 Red 測必須可定位

- Level: `MUST`
- 必須使用同一 Scenario Agent 在 Red 階段建立並驗證的測檔；找不到時停止，不得先寫功能再補測試。

## Good Example

```text
S-1-1 → frontend/tests/s-1-1-create-album.spec.ts
```

## Bad Example

```text
測檔不存在，先把建立相簿做完
```
