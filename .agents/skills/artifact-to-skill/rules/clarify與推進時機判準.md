# Rule 1 - 只有高影響結構缺口才應先進 clarify

- Level: `MUST`
- 若缺口會改變 artifact 的階層、歸屬、輸出契約、驗證單位、樣板骨架或 skill 控制平面，就必須先澄清。
- 若剩下的只是低風險預設、措辭偏好或可在 target artifact 階段安全調整的細節，應直接推進，不必為問而問。

## Good Example

- 這個例子是好的，因為它先問會改變結構的決策。

```md
- FR 要不要歸屬在 User Story 內？
- 成功標準要不要歸屬在 User Story 內？
- 跨故事限制要放在全域區還是故事內？
```

## Bad Example

- 這個例子是壞的，因為它先問低影響的 wording 細節。

```md
- 標題要不要用「功能規格」還是「需求規格」？
- 邊界情境要不要寫成條列還是短段落？
```

# Rule 2 - 一旦 target artifact 已足夠穩定，就應停止 clarify 並往下推進

- Level: `SHOULD`
- clarify 的目的在於收斂高風險不確定性，而不是把整個工程流程變成問卷。
- 當 target artifact 的主階層、歸屬與輸出方向已明確時，應停止澄清並進入改寫、template 萃取與工程化。

## Good Example

- 這個例子是好的，因為它在結構拍板後就開始改 artifact。

```md
已確認：
- 以 User Story 為主體
- FR / 成功標準都歸屬在故事內
- 共通限制另設全域區

下一步：直接改寫 target artifact
```

## Bad Example

- 這個例子是壞的，因為它在主要決策已明確後仍持續追問。

```md
已經拍板 artifact 主結構後，仍繼續追問：
- 破折號要不要改成數字編號？
- 每個章節間隔要留幾行？
```
