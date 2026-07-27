# Rule 1 - 完成條件只看本支新測是否為 Red

- Level: `MUST`
- 一次呼叫成功的必要條件：本支新測試已進入該層測試套件，且執行全套測試時本支呈現 Red（失敗）。
- 同 US 先前 Red 寫入、尚未經 Green 的其他失敗測試，可忽略，不構成本次失敗。
- 不可把「全套只剩本支紅」或「全套全綠」當成 Red 完成條件。

## Good Example

- 這個例子是好的，因為只證明 S-1-2 新測為紅，即使 S-1-1 仍紅。

```text
跑 npm test
S-1-1 FAIL（既有 Red）
S-1-2 FAIL（本支新測）→ 本次完成
```

## Bad Example

- 這個例子是壞的，因為要求先把其他測試弄綠才算 Red 完成。

```text
S-1-2 已紅，但因 S-1-1 也紅就判定本次失敗
```

# Rule 2 - 可寫測試基建，不可做程式碼實作

- Level: `MUST`
- 可新增／調整：E2E 測試檔、測試用 fixture（如假圖片）、測試 helper（清 DB、啟動測試 app、請求封裝）。
- 不可做讓 Scenario 通過的**程式碼實作**（例如真正處理建立相簿、上傳照片、拖放排序、寫入規則的 handler／UI 邏輯）；該工作留給 `/tdd-e2e-green`。
- 測檔應放在該層既有測試目錄並遵循既有命名慣例；無慣例時依環境 setup 已建立的測試基建位置新建，檔名宜可追溯 Scenario ID。

## Good Example

- 這個例子是好的，因為只動測試與 fixture。

```text
新增 backend/tests/s-1-1-create-album-import.test.js
新增 backend/tests/fixtures/sample.jpg
```

## Bad Example

- 這個例子是壞的，因為在 Red 階段做了 POST /albums 的程式碼實作。

```text
在 routes/albums.js 寫入建立相簿並存 DB 的完整邏輯
```

# Rule 3 - 最小空殼僅限無功能行為；更大環境洞交回 implement

- Level: `MUST`
- 若測試因缺少可 import／啟動的入口而跑不到斷言，僅可補「無功能行為」的最小空殼（例如可 import 的 app，未實作的 route 回 404 或空回應）。
- 環境／基建更大缺口（依賴未裝、測試腳本不存在、目錄未建立、服務無法啟動等）必須停止，回報 implement 補洞，不可由本 skill 擴大修環境。
- 不可為了讓測試變紅或變綠而做 Scenario 要求的程式碼實作。

## Good Example

- 這個例子是好的，因為空殼無功能行為，斷言仍紅。

```text
app 可 import；POST /api/albums 尚未實作 → 測試得到 404／失敗 → Red
```

## Bad Example

- 這個例子是壞的，因為自行補安裝依賴與改 package.json 測試腳本充當環境 setup。

```text
發現沒有 npm test，Red 自己改 package.json 並 npm install
```

# Rule 4 - 非預期綠不算完成；測試本身錯誤須先修好

- Level: `MUST`
- 若本支新測執行結果為綠，不得宣告 Red 完成；應強化斷言或對齊 Gherkin／契約後重跑，或回報「非預期綠」並停止。
- 禁止為製造失敗而刪改既有程式碼實作或故意破壞環境。
- 若失敗原因是測試語法錯、路徑錯、import 錯等「測試本身不可執行」，必須先修好並重跑，直到能證明是功能尚未程式碼實作導致的 Red（或改判為環境洞交回 implement）。

## Good Example

- 這個例子是好的，因為非預期綠時加嚴 Then 斷言，仍綠則回報停下。

```text
首次全綠 → 補上「不在相簿 A」斷言 → 變紅 → 完成
```

## Bad Example

- 這個例子是壞的，因為把產品 route 刪掉來製造紅燈。

```text
測試意外綠了 → 刪除已有的 albums 路由讓它變紅
```
