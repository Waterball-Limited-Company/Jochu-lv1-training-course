# Rule 1 - GWT 必須使用領域語言，不可綁定 API 或 UI 實作細節

- Level: `MUST`
- Scenario 的 Given／When／Then 只能使用規格領域用語（例如相簿、照片庫、主頁、拖放）。
- 不可出現 endpoint path、HTTP method／status、資料表名、元件 selector 或內部模組名。
- 本 skill 只凍結行為意圖；可觀測合約對齊留給下游 TDD／實作計畫。

## Good Example

- 這個例子是好的，因為步驟停留在使用者可理解的領域行為。

```gherkin
When 使用者建立一個名為「旅行」的相簿並從本機將該照片加入「旅行」相簿
Then 「旅行」相簿存在
```

## Bad Example

- 這個例子是壞的，因為把 API 合約寫進 Gherkin。

```gherkin
When 使用者呼叫 POST /albums
Then 回應 201 且 body 含 id
```

# Rule 2 - When 只能有一條；And 只允許接在 Given 或 Then 之後

- Level: `MUST`
- 每個 Scenario 的 Gherkin 區塊內，`When` 關鍵字只能出現一次，且 When 之後、Then 之前不可再出現 `And`／`But`。
- `Given` 與 `Then` 可以用 `And` 延續多個前置或斷言。
- 若 AC 含多個連續動作，應合併進同一條 When，或把驗證性動作寫進 Then，不可拆成 When + And。

## Good Example

- 這個例子是好的，因為單一 When，And 只出現在 Given／Then。

```gherkin
Given 使用者尚未建立任何相簿
And 本機有至少一張可選的照片
When 使用者建立一個名為「旅行」的相簿並從本機將該照片加入「旅行」相簿
Then 「旅行」相簿存在
And 該相簿內含剛加入的那張照片
```

## Bad Example

- 這個例子是壞的，因為 When 後又用 And 接第二個操作。

```gherkin
When 使用者建立相簿
And 從本機加入照片
Then 相簿內含該照片
```

# Rule 3 - 不可使用非標準步驟關鍵字冒充分支

- Level: `MUST`
- Gherkin 步驟關鍵字僅限 `Given`／`When`／`Then`／`And`／`But`（且 And／But 受 Rule 2 約束）。
- 不可使用 `Or`、`Also` 等非標準關鍵字另起一行；若需表達「或」語意，應寫進同一條步驟文字內。

## Good Example

- 這個例子是好的，因為「或」寫在同一條 When／Then 裡。

```gherkin
When 使用者嘗試在目前相簿下建立子相簿，或把另一個相簿放進目前相簿
Then 系統避免造成難以辨識的重複項目，或提供清楚回應讓使用者知道結果
```

## Bad Example

- 這個例子是壞的，因為使用了非法的 `Or` 關鍵字行。

```gherkin
When 使用者嘗試建立子相簿
Or 把另一個相簿放進目前相簿
```
