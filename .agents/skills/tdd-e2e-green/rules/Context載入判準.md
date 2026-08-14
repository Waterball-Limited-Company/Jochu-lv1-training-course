# Rule 1 - 只載本則工作 context；已有片段不重載

- Level: `MUST`
- 進場載入：本則 Red 測檔、該格 Green 實作計畫、依計畫點名且尚未持有的 SA 片段（路徑在 `specs/<plan-package>/system-analyze/`，層別集合對齊 `/tdd-e2e-red` 的各層必讀）、以及將改動的既有程式碼。
- implement 已帶入的 e2e／SA／task 片段必須沿用，禁止再當新進場重開同一批檔。
- 不得整份通讀 `technical-research.md`、`spec.md`、`plan.md`、整份無關 `task-*.md`。
- 不得為「順便了解下一則」載入本則不驗證列出的能力。

## Good Example

- 這個例子是好的，因為只備齊 S-1-1 測與點名契約。

```text
S-1-1 Green
→ 讀 s-1-1 測檔
→ 使用已定位的 ui-plan 主頁建立表單、api-plan POST /albums
→ 讀將改的主頁模組
```

## Bad Example

- 這個例子是壞的，因為進場就載本 US 全部測與整包 specs。

```text
US-1 Green → 讀 s-1-1…s-1-6 測檔 + spec + 全部 SA
```

# Rule 2 - 缺契約時手術式補讀，SA 仍只讀點名元素

- Level: `SHOULD`
- 若斷言或落地仍缺形狀／欄位，可再補讀本則相關契約片段；SA 仍禁止無關章節通讀。
- 行為準據以本則 Gherkin／既有測試斷言為準；Green 實作計畫導航要落地的程式邊界，並遵守本則不驗證。

## Good Example

- 這個例子是好的，因為只補本則缺的 POST /albums 回應形狀。

```text
本則: S-1-1
→ 補 api-plan POST /albums 的 201 形狀
```

## Bad Example

- 這個例子是壞的，因為把整份 api-plan 重讀一次。

```text
cat 整份 api-plan.md
```

# Rule 3 - 各層 SA 路徑與 Red 對齊

- Level: `MUST`
- SA 根路徑為 `specs/<plan-package>/system-analyze/`。
- `backend`：`api-plan.md`、`DDL.md`、`data-plan.md`；`frontend`：`ui-plan.md`、`data-plan.md`（Mock 時加 `api-plan.md`）；`integration`：`ui-plan.md`、`api-plan.md`、`data-plan.md`。

## Good Example

- 這個例子是好的，因為前端 Mock 時點名讀 api 形狀。

```text
layer=frontend → ui-plan + data-plan + 點名 api-plan 片段
```

## Bad Example

- 這個例子是壞的，因為後端 Green 去讀 ui-plan 整檔。

```text
layer=backend → 讀完整 ui-plan.md
```
