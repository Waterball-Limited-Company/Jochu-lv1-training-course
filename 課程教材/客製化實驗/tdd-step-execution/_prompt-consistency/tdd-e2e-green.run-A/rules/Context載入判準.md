# Rule 1 - 進場可載本 US 完整工作 context

- Level: `MUST`
- 因一次呼叫須做完整個 US，進場可載入：本 US 全部相關 Red 測檔、Green 實作計畫、依計畫點名的 SA 片段（路徑在 `specs/<plan-package>/system-analyze/`，層別集合對齊 `/tdd-e2e-red` 的各層必讀）、以及將改動的既有程式碼。
- 不得整份通讀 `technical-research.md`、`spec.md`、`plan.md`、整份無關 `task-*.md`。

## Good Example

- 這個例子是好的，因為一次備齊本 US 測與點名契約，而不讀整包 specs。

```text
US-1 Green
→ 讀 s-1-1…s-1-5 測檔
→ 讀實作計畫點名的 api-plan／DDL／data-plan 片段
→ 讀將改的 routes／db 模組
```

## Bad Example

- 這個例子是壞的，因為順便讀完整個 package 所有規格。

```text
先把 spec + plan + 全部 SA 整檔讀完再開始
```

# Rule 2 - 迴圈中按仍紅 Scenario 補讀，SA 仍只讀點名元素

- Level: `SHOULD`
- 內部迴圈可再補讀當前仍紅 Scenario 的 e2e 區塊與相關契約片段；SA 仍禁止無關章節通讀。
- 行為準據以各 Scenario Gherkin／既有測試斷言為準；Green 實作計畫導航要落地的程式邊界。

## Good Example

- 這個例子是好的，因為補讀當下仍紅的 S-1-4 契約後再實作。

```text
仍紅: S-1-4
→ 補 e2e S-1-4 與 415 錯誤形狀片段
```

## Bad Example

- 這個例子是壞的，因為每一輪都把整份 api-plan 重讀一次。

```text
每個 Scenario 迴圈都 cat 整份 api-plan.md
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
