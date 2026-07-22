# 端對端測試計畫：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: {{STATUS}}

## {{US_1_HEADING}}

### Scenario: {{SCENARIO_1_1_ID}} {{SCENARIO_1_1_TITLE}}

```gherkin
Scenario: {{SCENARIO_1_1_TITLE}}
{{SCENARIO_1_1_GHERKIN_BODY}}
```

**對應欄位**:

{{SCENARIO_1_1_MAPPING_LINES}}

---

{{US_1_ADDITIONAL_SCENARIO_SECTIONS}}

{{ADDITIONAL_US_SECTIONS}}

## 未產出 Scenario 的邊界（blocked）

{{BLOCKED_EDGE_INTRO}}

| ID | 描述 | 阻塞原因 |
| --- | --- | --- |
{{BLOCKED_EDGE_ROWS}}

---

## 元素覆蓋總表

> 一列一個被追蹤元素。`Scenario` 欄為 `blocked` 表示尚未有可執行情境覆蓋。

| ID | 描述 | Scenario |
| --- | --- | --- |
{{COVERAGE_MATRIX_ROWS}}

---

## 假設

{{ASSUMPTION_LINES}}

<!--
重複區塊填寫指引：
1. `{{US_1_ADDITIONAL_SCENARIO_SECTIONS}}`：同一 US 的其餘 Scenario，結構同「### Scenario」整段（含 gherkin 與對應欄位）。
2. `{{ADDITIONAL_US_SECTIONS}}`：其餘 US，結構同「## US-…」整段（標題需含「優先級：Pn」）。
3. `{{SCENARIO_*_GHERKIN_BODY}}`：縮排步驟本體；Given／Then 可用 And，When 僅一條且其後不可接 And。
4. `{{SCENARIO_*_MAPPING_LINES}}`：`- ` 條列，只列有對到的 US／AC／Edge／FR，ID 後接 spec 說明；無分類小標。
5. 無 blocked 項時，`{{BLOCKED_EDGE_ROWS}}` 可寫 `| （無） | （無） | （無） |`，或刪除整段 blocked 章節並在假設說明本期無 NEED CLARIFICATION。
6. `{{COVERAGE_MATRIX_ROWS}}`：每個 US／AC／Edge／FR 一列；未產出 Scenario 的 Edge 填 `blocked`。
7. `{{ASSUMPTION_LINES}}`：`- ` 條列；無額外假設時填 `- 本期無額外假設`。
8. 主標題與 metadata 欄位名稱必須對齊 spec.md（功能分支／建立日期／狀態）。
-->
