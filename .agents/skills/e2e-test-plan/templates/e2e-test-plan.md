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
- **受測部位**
{{BACKEND_SCENARIO_1_SEAM_LINES}}
- **前置資料**
{{BACKEND_SCENARIO_1_ARRANGE_LINES}}
- **觀測通道**
{{BACKEND_SCENARIO_1_OBSERVE_LINES}}
- **必須維持不變**
{{BACKEND_SCENARIO_1_INVARIANT_LINES}}
- **本則不驗證**
{{BACKEND_SCENARIO_1_OUT_OF_SCOPE_LINES}}
- **預期 TDD Red**
{{BACKEND_SCENARIO_1_EXPECTED_RED_LINES}}
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
- **受測部位**
{{FRONTEND_SCENARIO_1_SEAM_LINES}}
- **前置資料**
{{FRONTEND_SCENARIO_1_ARRANGE_LINES}}
- **觀測通道**
{{FRONTEND_SCENARIO_1_OBSERVE_LINES}}
- **狀態／畫面文案**
{{FRONTEND_SCENARIO_1_COPY_LINES}}
- **必須維持不變**
{{FRONTEND_SCENARIO_1_INVARIANT_LINES}}
- **本則不驗證**
{{FRONTEND_SCENARIO_1_OUT_OF_SCOPE_LINES}}
- **預期 TDD Red**
{{FRONTEND_SCENARIO_1_EXPECTED_RED_LINES}}
- **UI**
{{FRONTEND_SCENARIO_1_UI_LINES}}

---

{{FRONTEND_US_1_ADDITIONAL_SCENARIOS}}

{{ADDITIONAL_FRONTEND_US_SECTIONS}}

## 整合

{{INTEGRATION_INTRO}}

### {{INTEGRATION_US_1_ID}} {{INTEGRATION_US_1_TITLE}}（優先級：{{INTEGRATION_US_1_PRIORITY}}）

#### Scenario: {{INTEGRATION_SCENARIO_1_ID}} {{INTEGRATION_SCENARIO_1_TITLE}}

```gherkin
{{INTEGRATION_SCENARIO_1_GHERKIN}}
```

**對應欄位**:

- **US**
  - {{INTEGRATION_SCENARIO_1_US_LINE}}
- **受測部位**
{{INTEGRATION_SCENARIO_1_SEAM_LINES}}
- **前置資料**
{{INTEGRATION_SCENARIO_1_ARRANGE_LINES}}
- **觀測通道**
{{INTEGRATION_SCENARIO_1_OBSERVE_LINES}}
- **必須維持不變**
{{INTEGRATION_SCENARIO_1_INVARIANT_LINES}}
- **本則不驗證**
{{INTEGRATION_SCENARIO_1_OUT_OF_SCOPE_LINES}}
- **前端**
{{INTEGRATION_SCENARIO_1_FRONTEND_LINES}}
- **後端**
{{INTEGRATION_SCENARIO_1_BACKEND_LINES}}

---

{{INTEGRATION_US_1_ADDITIONAL_SCENARIOS}}

{{ADDITIONAL_INTEGRATION_US_SECTIONS}}

## 未產出 Scenario 的邊界（blocked）

{{BLOCKED_INTRO}}

| ID | 描述 | 阻塞原因 |
| --- | --- | --- |
{{BLOCKED_ROWS}}

---

## 測試摘要總表

{{SLICE_SUMMARY_NOTE}}

| User Story | AC / Edge | Scenario | 後端 | 前端 | 整合 |
| --- | --- | --- | --- | --- | --- |
{{SLICE_SUMMARY_ROWS}}

{{ACCEPTANCE_SUMMARY_NOTE}}

| User Story | Scenario | 整合 |
| --- | --- | --- |
{{ACCEPTANCE_SUMMARY_ROWS}}

---

## 假設

{{ASSUMPTION_LINES}}

<!--
重複區塊填寫指引：
1. 後端／前端 Scenario 標題寫成 `#### Scenario: S-x-y 業務標題`。整合寫成 `#### Scenario: US-n 驗收標題`。標題內不要加「（後端／前端／整合）」；證明方式由所在 `##` 區塊區分。
2. `{{*_SCENARIO_*_GHERKIN}}`：只替換 gherkin 本體（含 `Scenario:` 與 Given／When／Then／And），保留外層圍欄。Gherkin 用領域語言；`When` 僅一條。整合的 When 可寫獨立驗證整段路徑。
3. `{{*_US_1_ADDITIONAL_SCENARIOS}}`：同一 US 下其餘 Scenario，結構同「#### Scenario」整段。
4. `{{ADDITIONAL_*_US_SECTIONS}}`：該區塊其餘 US，結構同「### US-* 標題（優先級：Px）」整段。
5. US／AC／FR 寫編號加短標題，例如 `US-1 建立相簿並整理照片`。不可只留裸編號，不可寫檔案路徑箭頭鏈。
6. 後端／前端（薄切片）對應欄位：US、AC / Edge、FR、受測部位、前置資料、觀測通道、必須維持不變、本則不驗證、預期 TDD Red；後端另加 API；前端另加狀態／畫面文案與 UI。涉及持久化時後端可另加 Data。
7. 整合（US 驗收）對應欄位：US、受測部位、前置資料、觀測通道、必須維持不變、本則不驗證、前端、後端。不要預期 TDD Red，不必掛 AC／FR。
8. 受測部位是 Act 打哪；觀測通道是 Assert 從哪條正式介面看。前置資料用白話。條列各填 `  - ` 開頭（可多行）。
9. `{{INTEGRATION_INTRO}}`：說明整合對準各 US 獨立驗證、真串接、不抄薄切片。用正文，不要用引用區塊；不要把「雛形不是受測物」寫進產物。
10. 切片表整合欄一律 `—`。驗收表列出各 `US-n`。無 blocked 時表列 `| （無） | （無） | （無） |`。
11. `{{ASSUMPTION_LINES}}`：`- ` 條列，掛在檔案最下方。
-->
