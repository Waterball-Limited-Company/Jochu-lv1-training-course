# Rule 1 - Context 以將整理的程式／測試與實作計畫為主

- Level: `MUST`
- 進場載入：Refactor 實作計畫、將整理的程式碼與測試檔、本 US 相關測（用於確認行為不變）。
- SA（`specs/<plan-package>/system-analyze/`）僅在計畫要求「對齊錯誤形狀／契約風格」等時點名讀取相關片段；不整檔通讀，不讀 `technical-research.md`／`spec.md`／`plan.md`／整份 `task-*.md`。

## Good Example

- 這個例子是好的，因為只開計畫點名的模組與對齊用的錯誤形狀片段。

```text
讀 routes/albums.js、routes/photos.js、共用 error helper
必要時讀 api-plan 共通錯誤格式片段
```

## Bad Example

- 這個例子是壞的，因為重構卻整份重讀 ui-plan 與 spec。

```text
先讀完整 ui-plan.md + spec.md
```

# Rule 2 - 允許的重構類型

- Level: `MUST`
- 允許：實作與測試的去重；非功能品質（設計、可維護性、可讀性）；實作計畫點名的對齊風格／抽層（例如錯誤形狀一致、路徑組裝抽清）。
- 以上皆必須在行為與對外契約不變的前提下進行。

## Good Example

- 這個例子是好的，因為去重並對齊錯誤形狀，契約不變。

```text
抽出 mapError()；各 route 回傳同一 error envelope
```

## Bad Example

- 這個例子是壞的，因為「重構」時改了狀態碼語意。

```text
把 415 改成 400 並同步改測試
```

# Rule 3 - 禁止的改動

- Level: `MUST`
- 禁止：新功能、改驗收／契約語意、放寬或刪除斷言來維持綠燈、與本 US 實作計畫無關的大範圍重寫。

## Good Example

- 這個例子是好的，因為計畫外的新 endpoint 不做。

```text
計畫只寫去重 → 不新增 reorder API
```

## Bad Example

- 這個例子是壞的，因為邊重構邊加功能。

```text
重構時順便做缩圖快取新行為
```
