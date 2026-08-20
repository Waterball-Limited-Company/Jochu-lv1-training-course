# Rule 1 - Refactor 必須承接同一代理的 Green 證據

- Level: `MUST`
- Scenario Agent 呼叫 `/tdd-e2e-refactor` 時必須提供：與 Red、Green 相同的 `scenario-agent-id`、`layer`（僅 `backend`／`frontend`）、`plan-package`、`user-story`、本則 `S-n-m` ID／標題、Green 全綠證據與整理範圍。
- 缺 Green 證據、代理識別不同或 `layer=integration` 時停止。

## Good Example

```text
scenario-agent-id: frontend-US-1-S-1-1
本則: S-1-1
Green: 本則與既有綠燈通過
整理範圍: 去重建立表單的 request 組裝
```

## Bad Example

```text
另開一位代理，沒有 Green 證據就重寫整個前端
```

# Rule 2 - 一次只重構一個 Scenario

- Level: `MUST`
- 只整理本則點名的程式與測試；不可借機做同 User Story 下一則、跨故事重寫或擴充需求。
- 完成後回同一 Scenario Agent 執行 User Story 層內全綠閘門。

## Good Example

```text
S-1-1 剛綠 → 只整理 S-1-1 新增路徑 → 接著跑層內全綠
```

## Bad Example

```text
重構時順便完成尚未 Red 的批次匯入
```
