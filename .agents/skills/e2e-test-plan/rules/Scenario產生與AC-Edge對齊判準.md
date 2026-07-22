# Rule 1 - Scenario 的切分單位是 AC 或 Edge，不是 FR 或整個 US

- Level: `MUST`
- 每個可產出的 Scenario 必須對齊一條驗收標準（AC）或一條可測邊界條件（Edge）。
- User Story 只負責分章與優先級排序（標題需含「優先級：Pn」），不可把整包 US 壓成單一 Scenario。
- FR 不可單獨長出 Scenario；FR 只出現在對應欄位與覆蓋總表。

## Good Example

- 這個例子是好的，因為 US 下有多則 Scenario，各自對準 AC 或 Edge。

```md
## US-1 …（優先級：P1）

### Scenario: S-1-1 …
### Scenario: S-1-2 …
### Scenario: S-1-3 …
```

## Bad Example

- 這個例子是壞的，因為以 FR 為單位開 Scenario。

```md
### Scenario: S-FR-001 建立相簿能力
```

# Rule 2 - 預設 1 AC→1 Scenario、1 可測 Edge→1 Scenario；語意重複則合併

- Level: `MUST`
- 每條 AC 預設產出一則 Scenario；每條不含 `[NEED CLARIFICATION]` 的 Edge 預設產出一則 Scenario。
- 若某條 AC 與某條 Edge 的 When／Then 語意實質相同，必須合併為單一 Scenario，並在對應欄位同時列出該 AC 與 Edge。
- Scenario 編號建議採 `S-<US序>-<該US內序>`，全檔唯一。

## Good Example

- 這個例子是好的，因為巢狀拒絕的 AC 與 Edge 合併為一則。

```md
### Scenario: S-1-2 拒絕相簿巢狀並維持單層

**對應欄位**:

- US-1 …
- AC-1-2 …
- Edge-1-1 …
```

## Bad Example

- 這個例子是壞的，因為同一行為被拆成幾乎相同的兩則 Scenario。

```md
### Scenario: S-1-2 拒絕巢狀（AC）
### Scenario: S-1-3 拒絕巢狀（Edge）
```

# Rule 3 - NEED CLARIFICATION 與依賴未澄清決策的 Edge 不產出 Scenario

- Level: `MUST`
- 邊界條件若含 `[NEED CLARIFICATION: ...]`，本輪不可產出 Scenario，只能在 blocked 清單與覆蓋總表標 `blocked`。
- 若某邊界雖無標記，但明確依賴另一條未澄清決策，同樣標 `blocked`，不自行腦補行為。
- 使用者若先完成 `/clarify` 並回寫 `spec.md`，再依更新後的 AC／Edge 產出或更新 Scenario。

## Good Example

- 這個例子是好的，因為未澄清邊界只列在 blocked，不寫假 GWT。

```md
| Edge-1-3 | 同一張照片可否同時存在於多個相簿 | blocked |
```

## Bad Example

- 這個例子是壞的，因為在未澄清時自行發明行為並寫成 Scenario。

```gherkin
Scenario: 一張照片可同時屬於多個相簿
  When 使用者把同一張照片加入兩個相簿
  Then 兩個相簿都看得到該照片
```
