# 實作計畫（{{LAYER_LABEL}}）：{{FEATURE_NAME}}

流程版本: 2
功能分支: `{{PLAN_PACKAGE}}`
建立日期: {{CREATED_DATE}}
狀態: 草稿

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

#### {{SCENARIO_ID}} {{SCENARIO_TITLE}}

- [ ] `/tdd-e2e-red` — {{SCENARIO_ID}} {{SCENARIO_TITLE}}:
  - 受測行為：
    - 前置：{{PRECONDITION}}
    - 打：{{HIT_SURFACE}}
    - 看：{{OBSERVATION_CHANNEL}}
    - 期望：{{EXPECTED_RESULT}}
    - 文案：{{COPY_TEXT}}
    - 還沒做時：{{RED_FAILURE}}
  - 契約案例：{{CONTRACT_IDS}}
- [ ] `/tdd-e2e-green` — {{SCENARIO_ID}}:
  - 實作計畫：
    - {{GREEN_PLAN_ITEM}}
    - 本則不驗證：{{OUT_OF_SCOPE}}
- [ ] `/tdd-e2e-refactor` — {{SCENARIO_ID}}:
  - 整理範圍：
    - {{REFACTOR_SCOPE}}
    - 不准擴到{{OUT_OF_SCOPE}}
- [ ] `User Story 層內全綠閘門` — {{SCENARIO_ID}}:
  - 累積測試：{{US_ACCUMULATED_TEST_COMMAND}}
  - 契約證據：{{API_CONTRACT_EVIDENCE_COMMAND}}
  - 完成：同層、同一 User Story 到目前 Scenario 的測試與契約證據全部通過

{{ADDITIONAL_SCENARIO_BLOCKS}}

- [ ] `User Story 完成閘門` — {{US_ID}}:
  - User Story 測試：{{US_COMPLETE_TEST_COMMAND}}
  - 全層回歸：{{FULL_LAYER_REGRESSION_COMMAND}}
  - 契約證據：{{US_API_CONTRACT_EVIDENCE_COMMAND}}

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor | 層內全綠 |
| --- | --- | --- | --- | --- | --- |
{{PROGRESS_TABLE_ROWS}}

| User Story | 完成閘門 |
| --- | --- |
{{US_GATE_TABLE_ROWS}}

---

## 5. 假設

{{ASSUMPTIONS}}
