# 端對端測試計畫：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: 草稿

---

## 後端

### {{BACKEND_US_1_ID}} {{BACKEND_US_1_TITLE}}（優先級：{{BACKEND_US_1_PRIORITY}}）

#### Scenario: {{BACKEND_SCENARIO_1_ID}} {{BACKEND_SCENARIO_1_TITLE}}

```gherkin
{{BACKEND_SCENARIO_1_GHERKIN}}
```

**對應欄位**:

- **US**
  - {{BACKEND_SCENARIO_1_US_LINE}}
- **AC / Edge**
{{BACKEND_SCENARIO_1_AC_EDGE_LINES}}
- **FR**
{{BACKEND_SCENARIO_1_FR_LINES}}
- **API**
{{BACKEND_SCENARIO_1_API_LINES}}

---

{{BACKEND_US_1_ADDITIONAL_SCENARIOS}}

{{ADDITIONAL_BACKEND_US_SECTIONS}}

## 前端

### {{FRONTEND_US_1_ID}} {{FRONTEND_US_1_TITLE}}（優先級：{{FRONTEND_US_1_PRIORITY}}）

#### Scenario: {{FRONTEND_SCENARIO_1_ID}} {{FRONTEND_SCENARIO_1_TITLE}}

```gherkin
{{FRONTEND_SCENARIO_1_GHERKIN}}
```

**對應欄位**:

- **US**
  - {{FRONTEND_SCENARIO_1_US_LINE}}
- **AC / Edge**
{{FRONTEND_SCENARIO_1_AC_EDGE_LINES}}
- **FR**
{{FRONTEND_SCENARIO_1_FR_LINES}}
- **UI**
{{FRONTEND_SCENARIO_1_UI_LINES}}

---

{{FRONTEND_US_1_ADDITIONAL_SCENARIOS}}

{{ADDITIONAL_FRONTEND_US_SECTIONS}}

## 整合

> {{INTEGRATION_INTRO}}

### {{INTEGRATION_US_1_ID}} {{INTEGRATION_US_1_TITLE}}（優先級：{{INTEGRATION_US_1_PRIORITY}}）

#### Scenario: {{INTEGRATION_SCENARIO_1_ID}} {{INTEGRATION_SCENARIO_1_TITLE}}

```gherkin
{{INTEGRATION_SCENARIO_1_GHERKIN}}
```

**對應欄位**:

- **US**
  - {{INTEGRATION_SCENARIO_1_US_LINE}}
- **AC / Edge**
{{INTEGRATION_SCENARIO_1_AC_EDGE_LINES}}
- **FR**
{{INTEGRATION_SCENARIO_1_FR_LINES}}
- **前端**
{{INTEGRATION_SCENARIO_1_FRONTEND_LINES}}
- **後端**
{{INTEGRATION_SCENARIO_1_BACKEND_LINES}}

---

{{INTEGRATION_US_1_ADDITIONAL_SCENARIOS}}

{{ADDITIONAL_INTEGRATION_US_SECTIONS}}

## 未產出 Scenario 的邊界（blocked）

{{BLOCKED_INTRO}}

| ID  | 描述  | 阻塞原因 |
| --- | --- | ---- |
{{BLOCKED_ROWS}}

---

## 測試摘要總表

> {{SUMMARY_TABLE_NOTE}}

| User Story | AC / Edge | Scenario | 後端 | 前端 | 整合 |
| --- | --- | --- | --- | --- | --- |
{{SUMMARY_TABLE_ROWS}}

---

## 假設

{{ASSUMPTION_LINES}}

<!--
重複區塊填寫指引：
1. Scenario 標題寫成 `#### Scenario: S-x-y 業務標題`，標題內**不要**加「（後端／前端／整合）」括號；證明方式由所在 `## 後端`／`## 前端`／`## 整合` 區塊區分。
2. `{{*_SCENARIO_*_GHERKIN}}`：只替換 gherkin 區塊本體（含 `Scenario:` 與 Given／When／Then／And），保留外層 ```gherkin 圍欄。Gherkin 用領域語言；`When` 僅一條操作步驟。
3. `{{*_US_1_ADDITIONAL_SCENARIOS}}`：同一 US 下其餘 Scenario，結構同「#### Scenario」整段（含 Gherkin 與「**對應欄位**:」）。
4. `{{ADDITIONAL_*_US_SECTIONS}}`：該證明區塊其餘 US，結構同「### US-* 標題（優先級：Px）」整段（含其下全部 Scenario）。
5. 對應欄位分類（依證明區塊固定，不可混用）：
   - 後端：US／AC / Edge／FR／API
   - 前端：US／AC / Edge／FR／UI
   - 整合：US／AC / Edge／FR／前端／後端
6. `{{*_AC_EDGE_LINES}}`／`{{*_FR_LINES}}`／`{{*_API_LINES}}`／`{{*_UI_LINES}}`／`{{*_FRONTEND_LINES}}`／`{{*_BACKEND_LINES}}`：各填 `  - ` 開頭的條列（可多行）；無對應 FR 時可寫「（無獨立 FR 編號；…）」。
7. `{{INTEGRATION_INTRO}}`：整合區說明（僅收 Then 必須前後端真串接才有意義的 Scenario）。若本期無整合 Scenario，可刪除整合區內 US／Scenario 槽位，但保留 `## 整合` 與說明，或於說明註明本期無整合項。
8. `{{BLOCKED_INTRO}}`：blocked 章節開場說明；無 blocked 時表列填 `| （無） | （無） | （無） |`。
9. `{{SUMMARY_TABLE_NOTE}}`：總表說明（一列一條 AC 或 Edge；`✓`／`—` 標示落點；FR 不列入本表）。
10. `{{SUMMARY_TABLE_ROWS}}`：表列格式 `| US-x | AC-x-y 或 Edge-… | S-x-y | ✓ 或 — | ✓ 或 — | ✓ 或 — |`。
11. `{{ASSUMPTION_LINES}}`：`- ` 條列，掛在檔案最下方；交代證明區塊落點規則、Gherkin 慣例、與上游 spec／api-plan／ui-plan 對齊方式等。
-->
