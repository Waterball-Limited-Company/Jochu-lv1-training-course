# Rule 1 - 每輪只鎖定一支仍紅 Scenario 推進

- Level: `MUST`
- 內部迴圈每輪只鎖定**一支**本 US 仍紅的 Scenario／對應測，作為當輪 just enough 程式碼實作目標（對齊「一次只過一個失敗測試」；不是 triangulation／mini-step）。
- 若一次實作後其他仍紅測**附帶**變綠，可計入已綠並回報；但不得當成推進策略，也不得藉此超寫。下一輪仍只挑一支仍紅者。
- 本條管**推進範圍**（每輪只鎖一支）；「寫多少」以 Rule 4（just enough）為準，不可拿「附帶變綠」當超寫藉口。
- 禁止用放寬斷言、刪測、或改 Gherkin 語意來製造綠燈。

## Good Example

- 這個例子是好的，因為本輪只鎖 S-1-1 實作 POST /albums；S-1-3 附帶變綠可回報，下一輪仍只挑仍紅的 S-1-2。

```text
本輪目標: S-1-1
實作 POST /albums
→ S-1-1 PASS；S-1-3 附帶 PASS（回報）；S-1-2 仍 FAIL
→ 下一輪目標: S-1-2
```

## Bad Example

- 這個例子是壞的，因為刻意一次實作多支仍紅 Scenario，或拿附帶變綠當推進策略／超寫藉口。

```text
仍紅: S-1-1、S-1-2、S-1-3
→ 一次實作 POST + PATCH + 空相簿邏輯，讓三支同綠（違反每輪只鎖一支）
```

## Bad Example

- 這個例子是壞的，因為把 S-1-3 斷言刪掉來讓套件看起來較綠。

```text
刪除空相簿相關 expect，只留 S-1-1
```

# Rule 2 - 每步與終態都跑該層全套；守護既有綠燈

- Level: `MUST`
- 每次程式碼實作後必須執行該層**全套**測試（非只跑單支）。
- 當輪鎖定的目標 Scenario 應變綠；本層在進入本 US Green 前已綠的測試不得被弄紅。
- 本 US 結束前必須能證明本 US 相關測皆綠；可將終態確認併入最後一次全套結果。

## Good Example

- 這個例子是好的，因為全套跑完：本 US 全 PASS，且先前 US 測仍 PASS。

```text
npm test（backend 全套）
US-1 測全 PASS；US-2 既有綠仍 PASS
```

## Bad Example

- 這個例子是壞的，因為只跑單一檔就宣告該 Scenario 完成。

```text
node --test tests/s-1-1.test.js → PASS → 當作一步完成（未跑全套）
```

# Rule 3 - Green 的改動是程式碼實作

- Level: `MUST`
- 本 skill 的主產出是讓紅測變綠所需的**程式碼實作**（handler、服務、UI 行為、資料存取等）。
- 可一併修正明顯阻礙執行的測試基建問題（路徑、helper）；但不可把「改測以遷就錯誤實作」當成完成手段。
- 環境／依賴／測試腳本缺失等基建洞交回 implement，不在本次擴大做環境 setup。

## Good Example

- 這個例子是好的，因為實作了契約要求的上傳與 MIME 檢查。

```text
落地 POST .../photos + 415 錯誤形狀 → 對應測變綠
```

## Bad Example

- 這個例子是壞的，因為把預期從 415 改成 500 來配合半成品。

```text
測期望改成 500，實作回 500 → 假綠
```

# Rule 4 - 只寫剛好通過測試的量（just enough）；設計留給 Refactor

- Level: `MUST`
- 每次實作必須是 `just enough code to pass test`：只寫讓**當輪鎖定之仍紅測**通過所需的最小程式碼，不多寫。
- 禁止超寫，至少包含：
  1. 實作時尚**沒有**對應紅測覆蓋的功能或分支（含刻意一次實作多支仍紅 Scenario）；
  2. 非過測所需的整理、抽共用、優化命名／目錄、預先抽象——這些留給 `/tdd-e2e-refactor`。
- Green 不負責「把設計做對」；通過測即可進入後續 Refactor。不可在 Green 以重構／優化為由擴大改動面。

## Good Example

- 這個例子是好的，因為本輪只鎖 S-1-1，只落地讓該測過的最小行為；S-1-3 若附帶變綠可回報，未順便做 PATCH 或抽層。

```text
本輪目標: S-1-1
→ 實作 POST /albums（just enough 讓 S-1-1 PASS）
→ S-1-1 PASS；不做 PATCH、不抽 AlbumService
```

## Bad Example

- 這個例子是壞的，因為順手做了還沒紅測的功能，或綠了還做設計優化。

```text
為過 S-1-1，順便實作尚未 Red 的排序 API，並抽完整 repository 層「以後比較好維護」
```
