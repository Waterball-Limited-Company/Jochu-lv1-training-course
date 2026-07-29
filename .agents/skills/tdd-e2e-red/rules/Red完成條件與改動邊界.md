# Rule 1 - 完成條件是本支合格 Red，不是任意失敗

- Level: `MUST`
- 一次呼叫成功的必要條件：本支新測試已進入該層測試套件，且執行全套測試時本支為**合格 Red**。
- 合格 Red 必須同時滿足：
  1. 失敗**不是**因環境緣故；
  2. 失敗形態為下列三者之一：`value difference`（值不符預期）、`expected exception`（符合預期的例外）、`expected error code`（符合預期的錯誤碼／status）。
- `layer` 為 `backend` 時，本支斷言**必須**包含 API response status code；缺少 status 斷言不得宣告合格 Red。
- `frontend`／`integration`：只要落在上述三種形態之一即可（例如 UI 可見結果的 value difference）。
- 同 US 先前 Red 寫入、尚未經 Green 的其他失敗測試，可忽略，不構成本次失敗。
- 不可把「全套只剩本支紅」「全套全綠」或「compile／import 失敗」當成合格 Red。

## Good Example

- 這個例子是好的，因為本支紅在 status／值比對，且形態合法。

```text
跑 npm test
S-1-1 FAIL（既有 Red，可忽略）
S-1-2 期望 200，實得自然 404 → expected error code → 本次合格 Red
```

## Bad Example

- 這個例子是壞的，因為把 compile error 或任意紅燈當完成。

```text
Cannot find module './albums' → 直接回報 Red 完成
```

# Rule 2 - 可寫測試基建，不可做系統行為實作

- Level: `MUST`
- 可新增／調整：E2E 測試檔、測試用 fixture（如假圖片）、測試 helper（清 DB、啟動測試 app、請求封裝）。
- 不可做讓 Scenario 通過的**系統行為實作**（例如真正處理建立相簿、上傳照片、拖放排序、寫入規則的 handler／UI 邏輯）；該工作留給 `/tdd-e2e-green`。
- 測檔應放在該層既有測試目錄並遵循既有命名慣例；無慣例時依環境 setup 已建立的測試基建位置新建，檔名宜可追溯 Scenario ID。
- 撰寫／修正測試的 phase **只動測側**；實作骨架改動只允許出現在「補最小骨架」phase，且必須先有一次跑測結果顯示缺骨架。

## Good Example

- 這個例子是好的，因為只動測試與 fixture。

```text
新增 backend/tests/s-1-1-create-album-import.test.js
新增 backend/tests/fixtures/sample.jpg
```

## Bad Example

- 這個例子是壞的，因為在 Red 階段做了 POST /albums 的系統行為實作。

```text
在 routes/albums.js 寫入建立相簿並存 DB 的完整邏輯
```

# Rule 3 - 最小骨架僅限型態白名單；須先跑測再補；寫明因果

- Level: `MUST`
- 准許補骨架的**唯一原因**：不定骨架會讓本支死在 compile／import／缺符號，那樣的失敗**不是**合格 Red，會與 Rule 1 自相矛盾。
- 此處骨架是**實作程式碼的骨架**，不是測試程式碼的骨架。例如：測試會呼叫 repository → 可定 repository 介面／簽章；測試測 service → 可定 service 函數簽章，函數體可 `return null`。
- 可補項目（窮舉，除此之外沒有其他）：
  1. 資料的定義
  2. 介面的定義
  3. 函數簽章的定義
  4. 開出函數後，函數體 `return null` 或 `return 0` 這類 stub
- 不可補：任何系統行為實作。一句話：骨架可以、行為不行。
- 路由**尚未掛上**導致框架／運行時**自然**回 404（或等價「找不到」）：可視為已跑到斷言的合格失敗（通常歸 `expected error code`／value difference），**不必**再為此補 handler。
- **禁止**主動實作一個專門回 404／空回應的 handler 來「假裝未實作」。
- 環境／基建更大缺口（依賴未裝、測試腳本不存在、目錄未建立、服務無法啟動等）必須停止並交回 implement，不可由本 skill 擴大修環境，也不可假裝成缺骨架。

## Good Example

- 這個例子是好的，因為先跑測暴露缺符號，再只補簽章與 stub。

```text
跑測 → TypeError: createAlbum is not a function
→ 定 createAlbum 簽章，return null
→ 重跑 → 期望 201 實得 404（自然）→ 合格 Red
```

## Bad Example

- 這個例子是壞的，因為未跑測就預先鋪空殼，或自寫 404 handler。

```text
寫測前先實作 app.post('/api/albums', (req,res)=>res.status(404).end())
```

# Rule 4 - 跑測結果必須歸入五類之一，並只依類別回到對應步驟

- Level: `MUST`
- 每次跑完全套測試後，必須把**本支**結果歸入下列五類之一，並只依處置行動（不可在「跑測」步驟內順便寫碼）：

| 類別 | 典型現象 | 處置 |
| --- | --- | --- |
| 合格 Red | 形態為 value difference／expected exception／expected error code；非環境緣故；backend 含 status 斷言 | 進入成功回報 |
| 缺骨架 | compile error、缺模組、缺函數／簽章、import 不到實作符號 | 進入補最小骨架，再回到跑測 |
| 環境洞 | 無測試腳本、依賴未裝、目錄／服務無法啟動等基建缺口 | 停止並交回 implement |
| 測試本身不可執行 | 測檔語法錯、測檔路徑錯、測檔 import 錯等 | 回到撰寫／修正測試，再跑測 |
| 非預期綠 | 本支新測為綠 | 回到修正測試以加嚴斷言；若仍綠則停止回報非預期綠 |

- 禁止為製造失敗而刪改既有系統行為實作或故意破壞環境。
- 自然 404（路由未掛）且斷言已比對 status／值：歸「合格 Red」，不要歸「缺骨架」。

## Good Example

- 這個例子是好的，因為先分類再回到單一專責步驟。

```text
跑測 → 測檔 ReferenceError（測寫錯）→ 類別：測試本身不可執行 → 回修正測試 → 再跑測
```

## Bad Example

- 這個例子是壞的，因為在跑測步驟裡一邊分類一邊補骨架又改測檔。

```text
跑完發現缺函數 → 同一步寫完 stub、改斷言、再宣告完成
```
