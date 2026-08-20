# 實作計畫（{{LAYER_LABEL}}）：{{FEATURE_NAME}}

流程版本: 2
功能分支: `{{PLAN_PACKAGE}}`
建立日期: {{CREATED_DATE}}
狀態: 草稿
範圍: {{INTEGRATION_SCOPE}}

---

## 1. 規格閱讀

{{SPEC_READING_CHECKLIST}}

```bash
{{SPEC_READING_LS_COMMANDS}}
```

---

## 2. 環境建立

{{ENV_SETUP_SECTIONS}}

---

## 3. User Story 實作計劃

### {{US_ID}} {{US_TITLE}}（優先級：{{US_PRIORITY}}）

#### AC / Edge

{{AC_EDGE_ITEMS}}

#### {{US_ID}} {{SCENARIO_TITLE}}

- [ ] `User Story 完全端對端驗收` — {{US_ID}}:
  - 前置閘門：後端與前端的 {{US_ID}} 完成閘門皆已通過
  - Mock：停用
  - 前端：真實執行期頁面
  - API：正式 API
  - 後端：真實後端
  - 資料：{{RESETTABLE_TEST_DATA_COMMAND}}
  - 執行：{{FULL_E2E_COMMAND}}
  - 觀測：{{OBSERVATION_CHANNEL}}
  - 期望：{{EXPECTED_RESULT}}
  - 契約案例：{{CONTRACT_IDS}}
  - 契約證據：{{INTEGRATION_CONTRACT_EVIDENCE_COMMAND}}
  - 失敗路由：行為缺口回到對應層 Scenario；契約不一致依 api-plan.md 判定漂移方；接線或環境缺口留在整合驗收修復

{{ADDITIONAL_US_BLOCKS}}

---

## 4. 進度總覽

| User Story | 完全端對端驗收 |
| --- | --- |
{{PROGRESS_TABLE_ROWS}}

---

## 5. 假設

{{ASSUMPTIONS}}
