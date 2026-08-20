# Rule 1 - 交接資料必須讓代理不用重猜範圍

- Level: `MUST`
- Scenario Agent 必須收到：`scenario-agent-id`、`layer`、`plan-package`、`user-story`、Scenario ID／標題、四個 task 步驟、e2e Scenario、已定位系統分析片段、契約案例、測試命令、允許修改路徑與禁止修改路徑。
- 缺任一範圍資料時停止委派，先由 `/implement` 補齊；不得讓代理自行把整個 User Story 當 Green 範圍。
- 正式 Red 前先跑同層、同 User Story 已完成 Scenario 的累積測試；基準已有紅燈時停止，不把既有失敗算成本則 Red。

## Good Example

```text
scenario-agent-id: frontend-US-1-S-1-1
layer: frontend
scenario: S-1-1
allowed paths: frontend/src, frontend/tests
contract ids: API-001-C1
```

## Bad Example

```text
請把 US-1 前端做完，自己找相關規格
```

# Rule 2 - 階段證據留在同一代理脈絡

- Level: `MUST`
- Red 成功證據至少含主斷言、實際失敗、失敗原因與測試命令；Green 含最少改動與本則通過結果；Refactor 含整理範圍與前後測試結果。
- 前一階段成功後由同一 Scenario Agent直接進下一階段，不回主控制面重開代理。
- Red、Green 或 Refactor 階段失敗時停止該 Scenario，回報已完成階段、工作樹變更、測試輸出與第一個未完成階段。Refactor 後的累積閘門若只是本則造成既有案例回歸，依 Rule 3 先由原代理修復；只有超出本則邊界、契約衝突、環境洞或仍無法修復時才停止回報。

## Good Example

```text
Red 證據保留在 Agent A → Agent A 接著做最少 Green → Agent A 重構
```

## Bad Example

```text
只回報「Red 完成」，Green 代理看不到實際失敗原因
```

# Rule 3 - Scenario 閘門與 User Story 閘門用途不同

- Level: `MUST`
- `User Story 層內全綠閘門 — S-n-m` 在每個 Scenario 重構後執行，範圍是同層、同 User Story 到目前為止的所有 Scenario，加上本 Scenario 必要契約證據；契約驗證命令必須以本則全部 `--contract-id` 限縮，不能提前要求故事中尚未執行的其他契約。
- `User Story 完成閘門 — US-n` 在該故事所有 Scenario 完成後，由 `/implement` 跑完整故事測試、該層全套回歸與該故事全部必要契約證據。
- 層內閘門失敗時，先找出變紅的 Scenario 與造成回歸的本則修改；能在本則邊界修復時，由目前 Scenario Agent 留在同一脈絡修復並重跑新舊案例，不因先前案例變紅就另開代理。若證據顯示是另一個尚未描述的獨立行為，才回控制面建立或定位對應 Scenario。

## Good Example

```text
S-1-2 完成後跑 US-1 的 S-1-1 與 S-1-2；故事結束再跑完整 US-1 與後端全套
```

## Bad Example

```text
每則只跑自己的測試，直到整合階段才第一次發現 S-1-1 被 S-1-2 改壞
```
