# 資料計畫：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: 草稿

## 實體：{{ENTITY_1_NAME}}（{{ENTITY_1_NAME_ZH}}）

{{ENTITY_1_INTRO}}

| 欄位 | 型別 | 必填 | 說明 | 驗證規則 | 對應 User Story |
| --- | --- | --- | --- | --- | --- |
{{ENTITY_1_FIELD_ROWS}}

### 衍生屬性

{{ENTITY_1_DERIVED_ATTRIBUTES}}

### 範例資料輸出

```json
{{ENTITY_1_EXAMPLE_JSON}}
```

---

{{ADDITIONAL_ENTITY_SECTIONS}}

## ERD

```mermaid
{{ERD_MERMAID}}
```

---

## 約束清單

{{CONSTRAINT_ITEMS}}

---

## DDL

> 單一腳本、多表並以註解區隔。建表順序：{{DDL_TABLE_ORDER}}。

```sql
{{DDL_SQL}}
```

## 假設

{{ASSUMPTION_ITEMS}}

<!--
重複區塊與填寫指引：
1. `{{ADDITIONAL_ENTITY_SECTIONS}}`：其餘資料實體，結構同「## 實體」整段（含欄位表、衍生屬性、範例資料輸出；若有複合主鍵等補充句，放在欄位表與範例資料輸出之間）。
2. 欄位表列格式：`| \`欄位名\` | 型別 | 必填（是／否／系統產生） | 說明 | 驗證規則 | US-x, US-y |`
3. 驗證規則寫法：規則文字 + 括號內 FR／US 編號（只列編號、不寫 FR 全文）；多個編號用逗號分隔。例：`非空白 (FR-001, FR-014)`。無額外規則時可只寫 `(FR-006)`。
4. 無衍生屬性時，`{{ENTITY_N_DERIVED_ATTRIBUTES}}` 填「無」或刪除「### 衍生屬性」整節。
5. 約束清單每條格式：`- 因為{{原因}}（{{FR_OR_US_REFS}}），所以 {{設計}}。`；無對應 FR／US 時可省略括號引用。
6. DDL 以 SQL comment 區隔各表，例如 `-- ========== table_name ==========`；多表寫在同一段 `{{DDL_SQL}}`，並依外鍵依賴排序（被引用表先建）。
7. `## 假設` 固定掛在檔案最下方（DDL 之後）；格式與 `spec.md` 相同，使用 `- ` 條列。高影響未決須在實體／約束等正文使用 `[NEEDS CLARIFICATION: …]`；低風險只寫本節。對上游 `spec.md` 標記與本檔暫定取捨，澄清後回寫。
-->
