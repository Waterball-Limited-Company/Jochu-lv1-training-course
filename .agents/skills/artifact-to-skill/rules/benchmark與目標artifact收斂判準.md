# Rule 1 - benchmark artifact 與 target artifact 必須先分開定義

- Level: `MUST`
- `benchmark artifact` 是拿來借鑑格式、結構或表達方式的參考成品；`target artifact` 是依使用者需求改寫後、真正要達成的成品。
- 在進入 template 萃取或 skill 工程化之前，必須先清楚區分兩者，不可把 benchmark 直接當成最終樣板。
- 若使用者其實對 benchmark 的結構不滿意，應先改出 target artifact，再進入下一層。

## Good Example

- 這個例子是好的，因為它先把 benchmark 改成使用者要的 target artifact。

```md
- benchmark artifact：`spec.example.md`
- target artifact：改成「FR 與成功標準都歸屬在 User Story 內」的新 spec 成品
- 下一步：再從 target artifact 抽出 `spec.template.md`
```

## Bad Example

- 這個例子是壞的，因為它直接把 benchmark 當成最終樣板來源，忽略使用者其實要改結構。

```md
- benchmark artifact：`spec.example.md`
- 下一步：直接抽 `spec.template.md`
```

# Rule 2 - benchmark 可借鑑的範圍必須顯式化

- Level: `SHOULD`
- 在開始改寫前，應先說清楚 benchmark 借鑑的是章節結構、命名風格、驗證粒度、表達語氣，還是其他部分。
- 不應籠統說「參考這份 artifact」，卻不指出真正可沿用的元素。

## Good Example

- 這個例子是好的，因為它明確指出借鑑與重寫邊界。

```md
- 借鑑：整體 spec 格式、使用者故事式展開、驗收情境寫法
- 重寫：FR 歸屬、成功標準歸屬、全域約束位置
```

## Bad Example

- 這個例子是壞的，因為它沒有說明到底參考哪一層。

```md
- 請參考這份 artifact，然後改成我想要的版本
```

# Rule 3 - target artifact 要先滿足使用者滿意度，才可進入後設工程化

- Level: `MUST`
- 若使用者明確表示要「先改到滿意的格式為止」，就必須先把 target artifact 修到可接受，再進入 template 萃取與 skill engineering。
- 不可在 target artifact 尚未穩定時，就提前抽 template 或寫 rules。

## Good Example

- 這個例子是好的，因為它先完成成品，再工程化流程。

```md
1. 先用 clarify 收斂高影響結構決策
2. 反覆改寫 artifact，直到使用者滿意
3. 再抽 template 與工程化 skill
```

## Bad Example

- 這個例子是壞的，因為它在成品還沒定稿前就先產品化。

```md
1. 看一眼 benchmark
2. 直接先寫 rules 與 templates
3. 之後再看看 artifact 長什麼樣
```
