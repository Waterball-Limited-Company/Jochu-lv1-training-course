# Rule 1 - Context 以將整理的程式／測試與整理範圍為主

- Level: `MUST`
- 進場載入：該格整理範圍、將整理的程式碼與測試檔、本則測（用於確認行為不變）。
- implement 已帶入的片段必須沿用，禁止再當新進場重開同一批 e2e／SA。
- SA（`specs/<plan-package>/system-analyze/`）僅在整理範圍要求「對齊錯誤形狀／契約風格」等時點名讀取相關片段；不整檔通讀，不讀 `technical-research.md`／`spec.md`／`plan.md`／整份 `task-*.md`。

## Good Example

- 這個例子是好的，因為只開整理範圍點名的模組。

```text
讀剛寫的建立表單與 POST /albums 呼叫
必要時讀 api-plan POST /albums 錯誤形狀片段
```

## Bad Example

- 這個例子是壞的，因為重構卻整份重讀 ui-plan 與 spec。

```text
先讀完整 ui-plan.md + spec.md
```

# Rule 2 - 允許的重構類型

- Level: `MUST`
- 允許：實作與測試的去重；非功能品質（設計、可維護性、可讀性）；整理範圍點名的對齊風格／抽層（例如錯誤形狀一致、路徑組裝抽清）。
- 以上皆必須在行為與對外契約不變的前提下進行。

## Good Example

- 這個例子是好的，因為去重並對齊命名，契約不變。

```text
整理建立表單欄位命名；抽出重複的 POST /albums 錯誤處理
```

## Bad Example

- 這個例子是壞的，因為「重構」時改了狀態碼語意。

```text
把 415 改成 400 並同步改測試
```

# Rule 3 - 禁止的改動

- Level: `MUST`
- 禁止：新功能、改驗收／契約語意、放寬或刪除斷言來維持綠燈、整理範圍寫明「不准擴到」的下一則能力、與本則無關的大範圍重寫。

## Good Example

- 這個例子是好的，因為計畫外的匯入不做。

```text
整理範圍只寫建立表單 → 不新增加入照片
```

## Bad Example

- 這個例子是壞的，因為邊重構邊加功能。

```text
重構時順便做批次匯入
```
