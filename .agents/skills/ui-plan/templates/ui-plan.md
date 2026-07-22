# UI 計畫：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: 草稿

## 業務邏輯 1：{{BUSINESS_LOGIC_1_TITLE}}

{{BUSINESS_LOGIC_1_INTRO}}

```mermaid
{{BUSINESS_LOGIC_1_SEQUENCE_MERMAID}}
```

對應：

{{BUSINESS_LOGIC_1_TRACEABILITY_LINES}}

---

{{ADDITIONAL_BUSINESS_LOGIC_SECTIONS}}

## 頁面：{{PAGE_1_NAME}}（{{PAGE_1_CODE}}）

### 職責

{{PAGE_1_RESPONSIBILITY_LINES}}

### 呈現內容

{{PAGE_1_PRESENTATION_LINES}}

### 操作 Flow

```mermaid
{{PAGE_1_FLOW_SEQUENCE_MERMAID}}
```

{{PAGE_1_FLOW_NOTES}}

### 導覽

| 操作 | 前往頁面 |
| --- | --- |
{{PAGE_1_NAVIGATION_ROWS}}

### API 對應

| 使用者操作 | API | 說明 |
| --- | --- | --- |
{{PAGE_1_API_MAPPING_ROWS}}

---

{{ADDITIONAL_PAGE_SECTIONS}}

## 頁面總覽（導覽關係）

```mermaid
{{PAGE_OVERVIEW_FLOWCHART_MERMAID}}
```

| 頁面 | 主要 US |
| --- | --- |
{{PAGE_OVERVIEW_US_ROWS}}

---

## 假設

{{ASSUMPTION_LINES}}

<!--
重複區塊填寫指引：
1. `{{ADDITIONAL_BUSINESS_LOGIC_SECTIONS}}`：其餘業務邏輯，結構同「## 業務邏輯 N：標題」整段（簡介 → Sequence → 對應條列）。編號從 2 起連續。
2. `{{ADDITIONAL_PAGE_SECTIONS}}`：其餘頁面，結構同「## 頁面：名稱（代號）」整段（職責、呈現內容、操作 Flow、導覽、API 對應）。
3. 對應／職責條列格式：`- **US-x** …`、`- **FR-xxx** …`、`- **AC-x-y** …`。
4. 導覽列：`| 操作 | 前往頁面 |`；API 列：`| 使用者操作 | API | 說明 |`；總覽列：`| 頁面 | 主要 US |`。
5. `{{PAGE_1_FLOW_NOTES}}`：操作 Flow 後的補充說明；無則留空。
6. 業務邏輯 Sequence 只畫跨頁業務路徑；頁內操作細節放在各頁「操作 Flow」。
7. 僅可獨立到達的全頁算「頁面」；Modal、檔案選取器等附屬寫入所屬頁操作 Flow，不另開頁。
8. 頁面狀態（空／錯／載入）不單獨立項，寫進「呈現內容」與「操作 Flow」。
9. `{{ASSUMPTION_LINES}}`：`- ` 條列，格式同 spec.md「## 假設」；無額外假設時填 `- 本期無額外假設`。高影響未決須在業務邏輯／頁面正文使用 `[NEEDS CLARIFICATION: …]`；低風險只寫本節（不可省略章節，也不可留下空的假設區）。
10. Mermaid 區塊只替換圖內容本體，保留外層 ```mermaid 圍欄。
-->
