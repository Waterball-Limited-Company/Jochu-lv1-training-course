# Rule 1 - 以仍紅 Scenario 推進，允許一次多支變綠

- Level: `MUST`
- 內部迴圈以「本 US 仍紅的 Scenario／對應測」為目標做程式碼實作。
- 若一次實作使多支仍紅測同時變綠，全部計入已綠，接著處理下一支仍紅者；不必假裝一次只准綠一支。
- 禁止用放寬斷言、刪測、或改 Gherkin 語意來製造綠燈。

## Good Example

- 這個例子是好的，因為落地 POST /albums 後 S-1-1 與 S-1-3 同綠，繼續打仍紅的 S-1-2。

```text
實作 POST /albums
→ S-1-1、S-1-3 PASS；S-1-2 仍 FAIL → 下一輪打 PATCH
```

## Bad Example

- 這個例子是壞的，因為把 S-1-3 斷言刪掉來讓套件看起來較綠。

```text
刪除空相簿相關 expect，只留 S-1-1
```

# Rule 2 - 每步與終態都跑該層全套；守護既有綠燈

- Level: `MUST`
- 每次程式碼實作後必須執行該層**全套**測試（非只跑單支）。
- 當下目標相關測應變綠（或同批變綠）；本層在進入本 US Green 前已綠的測試不得被弄紅。
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
