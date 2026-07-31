# Rule 1 - 呼叫時必須帶齊 Scenario 級必填欄位

- Level: `MUST`
- implement 呼叫 `/tdd-e2e-green` 時必須顯式提供：`layer`（`backend`／`frontend`／`integration`）、`plan-package`（僅目錄名，如 `001-photo-albums`，不含 `specs/`）、單一 Scenario ID／標題、該格 Green 實作計畫。
- 可附所屬 User Story 識別供對照，但不可用「整包 US」取代 Scenario。
- 規格路徑一律 `specs/<plan-package>/...`。
- 缺少必填欄位時必須停止並回報，不可自行猜測 `layer`、package 或 Scenario。

## Good Example

- 這個例子是好的，因為 Scenario 級四項齊備。

```text
layer: backend
plan-package: 001-photo-albums
Scenario: S-1-1 建立「旅行」相簿並一次匯入多格式照片
Green 實作計畫:（巢狀條列，只服務本支）
```

## Bad Example

- 這個例子是壞的，因為未指定 Scenario，卻一次想綠化整包 US。

```text
layer: backend
US: US-1
請把本 US 所有紅燈都變綠
```

# Rule 2 - 一次呼叫只處理一個 Scenario

- Level: `MUST`
- 一次 `/tdd-e2e-green` 只對應一個 Scenario（對齊 task 一格、對齊 Red 一格一呼叫）。
- 不可在同一次呼叫中把多支仍紅 Scenario 當實作目標；本支變綠即結束（交回 implement 再呼下一格）。

## Good Example

- 這個例子是好的，因為範圍鎖在 S-1-1。

```text
僅 S-1-1 的既有 Red → 變綠
```

## Bad Example

- 這個例子是壞的，因為一次做完 S-1-1～S-1-5。

```text
順便把同 US 後面 Scenario 也綠掉
```

# Rule 3 - 本支 Scenario 的 Red 測必須可定位

- Level: `MUST`
- 必須能定位本支 Scenario 對應的既有 Red 測與 `e2e-test-plan.md` 區塊。
- 無法對到本支 Red 測時必須停止並回報（可能 Red 尚未完成）。

## Good Example

- 這個例子是好的，因為 S-1-2 對到既有測檔。

```text
S-1-2 → backend/tests/…s-1-2….test.js 仍紅可定位
```

## Bad Example

- 這個例子是壞的，因為尚未有對應 Red 測就要求 Green。

```text
Scenario 標題對不到任何測檔 → 仍繼續寫產品碼
```
