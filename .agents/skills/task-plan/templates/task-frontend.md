# 實作計畫（{{LAYER_LABEL}}）：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`  
**建立日期**: {{CREATED_DATE}}  
**狀態**: 草稿

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
- [ ] `/tdd-e2e-green` — {{SCENARIO_ID}}:
  - 實作計畫：
    - {{GREEN_PLAN_ITEM}}
    - 本則不驗證：{{OUT_OF_SCOPE}}
- [ ] `/tdd-e2e-refactor` — {{SCENARIO_ID}}:
  - 整理範圍：
    - {{REFACTOR_SCOPE}}
    - 不准擴到{{OUT_OF_SCOPE}}

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor |
| --- | --- | --- | --- | --- |
{{PROGRESS_TABLE_ROWS}}

---

## 5. 假設

{{ASSUMPTIONS}}
