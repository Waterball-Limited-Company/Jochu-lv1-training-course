# Rule 1 - 改寫 target artifact 時，應優先調整資訊架構而不是表面 wording

- Level: `MUST`
- 若使用者指出的是歸屬、階層、驗證單位、章節邊界或全域限制位置等問題，改寫時應優先重組 artifact 的資訊架構。
- 不可只微調文案、標題或詞句，卻保留原本錯誤的結構。

## Good Example

- 這個例子是好的，因為它先移動 FR 與成功標準的歸屬位置。

```md
原本：
- FR 在全域需求區
- 成功標準在故事外

改寫後：
- 每個 User Story 底下都有自己的 FR 與成功標準
```

## Bad Example

- 這個例子是壞的，因為它只改名稱，沒有改結構。

```md
把「需求」改名成「故事需求」，但 FR 仍然全部放在故事外
```

# Rule 2 - target artifact 應先成為可直接評估的 benchmark 成品

- Level: `MUST`
- 改寫完成後的 target artifact 應能單獨被閱讀、比較與驗證，不依賴後續 template 或 rules 補完。
- 它必須足夠完整，才能作為後續樣板萃取與 skill 工程化的 benchmark。

## Good Example

- 這個例子是好的，因為改寫後的成品本身已經可直接評估。

```md
target artifact：
- 章節已定稿
- 故事歸屬已定稿
- 驗收與成功標準已放到正確位置
```

## Bad Example

- 這個例子是壞的，因為 target artifact 仍然只是半成品。

```md
target artifact：
- 先留幾個 TODO
- 規則等之後寫 skill 再補
```

# Rule 3 - 改寫時應明確保留、重組、上提、下放、合併或刪除

- Level: `SHOULD`
- 在 benchmark 到 target artifact 的轉換過程中，應顯式判斷每個關鍵結構元素是要保留、重組、上提、下放、合併還是刪除。
- 這能避免改寫過程只靠模糊直覺，導致後續 template 與 skill 難以回推。

## Good Example

- 這個例子是好的，因為它把轉換動作說清楚。

```md
- 保留：整體 spec 章節語氣
- 下放：FR 到各自 User Story
- 下放：成功標準到各自 User Story
- 上提：跨故事限制到全域約束區
```

## Bad Example

- 這個例子是壞的，因為它只有結論，沒有結構轉換紀錄。

```md
- 直接改成我覺得比較好的樣子
```
