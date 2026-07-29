# 規格分析報告：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: 草稿

---

## 每階段產物盤點表

| 產物 | 路徑 | 狀態 |
| --- | --- | --- |
| 功能規格 | `{{SPEC_PATH}}` | {{SPEC_STATUS}} |
| 系統分析總覽 | `{{PLAN_PATH}}` | {{PLAN_STATUS}} |
| 技術研究 | `{{TECHNICAL_RESEARCH_PATH}}` | {{TECHNICAL_RESEARCH_STATUS}} |
| 資料計畫 | `{{DATA_PLAN_PATH}}` | {{DATA_PLAN_STATUS}} |
| DDL | `{{DDL_PATH}}` | {{DDL_STATUS}} |
| API 計畫 | `{{API_PLAN_PATH}}` | {{API_PLAN_STATUS}} |
| UI 計畫 | `{{UI_PLAN_PATH}}` | {{UI_PLAN_STATUS}} |
| 端對端測試計畫 | `{{E2E_TEST_PLAN_PATH}}` | {{E2E_TEST_PLAN_STATUS}} |
| 後端實作計畫 | `{{TASK_BACKEND_PATH}}` | {{TASK_BACKEND_STATUS}} |
| 前端實作計畫 | `{{TASK_FRONTEND_PATH}}` | {{TASK_FRONTEND_STATUS}} |
| 整合實作計畫 | `{{TASK_INTEGRATION_PATH}}` | {{TASK_INTEGRATION_STATUS}} |

> 狀態用語：`存在`／`缺失`／`不適用`（plan 未要求且合理跳過）。

---

## 問題總表

| 編號 | 比對依據 | 嚴重程度 | 位置 | 摘要 | 建議處理 |
| --- | --- | --- | --- | --- | --- |
| {{FINDING_1_ID}} | {{FINDING_1_AXIS}} | {{FINDING_1_SEVERITY}} | {{FINDING_1_LOCATION}} | {{FINDING_1_SUMMARY}} | {{FINDING_1_RECOMMENDATION}} |
{{ADDITIONAL_FINDING_ROWS}}

> 若無問題，保留表頭並於表下寫「本輪無問題」。

---

## 規格覆蓋矩陣

| 需求編號 | 摘要 | 介面落點 | Scenario | Task | 備註 |
| --- | --- | --- | --- | --- | --- |
| {{REQ_1_ID}} | {{REQ_1_SUMMARY}} | {{REQ_1_INTERFACE}} | {{REQ_1_SCENARIO}} | {{REQ_1_TASK}} | {{REQ_1_NOTE}} |
{{ADDITIONAL_REQ_COVERAGE_ROWS}}

---

## 驗收覆蓋矩陣

| AC／Edge | 摘要 | Scenario | 後端 | 前端 | 整合 | Task 落點 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{AC_1_ID}} | {{AC_1_SUMMARY}} | {{AC_1_SCENARIO}} | {{AC_1_BACKEND}} | {{AC_1_FRONTEND}} | {{AC_1_INTEGRATION}} | {{AC_1_TASK}} | {{AC_1_NOTE}} |
{{ADDITIONAL_AC_COVERAGE_ROWS}}

---

## 指標

| 指標 | 數值 |
| --- | --- |
| 需求總數（FR／GR 計入覆蓋者） | {{METRIC_REQ_TOTAL}} |
| 有介面落點的需求數 | {{METRIC_REQ_WITH_INTERFACE}} |
| 有 Scenario 的需求數 | {{METRIC_REQ_WITH_SCENARIO}} |
| AC／Edge 總數 | {{METRIC_AC_TOTAL}} |
| 有 Scenario 的 AC／Edge 數 | {{METRIC_AC_WITH_SCENARIO}} |
| 發現總數 | {{METRIC_FINDING_TOTAL}} |
| 嚴重 | {{METRIC_CRITICAL}} |
| 高 | {{METRIC_HIGH}} |
| 中 | {{METRIC_MEDIUM}} |
| 低 | {{METRIC_LOW}} |

---

## 其餘發現摘要

{{REMAINING_FINDINGS_SUMMARY}}

---

## 下一步建議

{{NEXT_ACTIONS_PROSE}}

---

## 假設

{{ASSUMPTIONS_SECTION}}
