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

## 約束清單

> 僅列實體內部欄位／屬性約束。實體之間的關聯形狀與理由見 `DDL.md`「設計脈絡」（若本期有產出）。

{{CONSTRAINT_ITEMS}}

## 假設

{{ASSUMPTION_ITEMS}}

<!--
重複區塊與填寫指引：
1. `{{ADDITIONAL_ENTITY_SECTIONS}}`：其餘資料實體，結構同「## 實體」整段（含欄位表、衍生屬性、範例資料輸出；若有複合主鍵等補充句，放在欄位表與範例資料輸出之間）。
2. 欄位表列格式：`| \`欄位名\` | 型別 | 必填（是／否／系統產生） | 說明 | 驗證規則 | US-x, US-y |`
3. 驗證規則寫法：規則文字 + 括號內 FR／US 編號（只列編號、不寫 FR 全文）；多個編號用逗號分隔。例：`非空白 (FR-001, FR-014)`。無額外規則時可只寫 `(FR-006)`。
4. 無衍生屬性時，`{{ENTITY_N_DERIVED_ATTRIBUTES}}` 填「無」或刪除「### 衍生屬性」整節。
5. 約束清單每條格式：`- 因為{{原因}}（{{FR_OR_US_REFS}}），所以 {{設計}}。`；無對應 FR／US 時可省略括號引用；不可寫關聯拓撲（1:N／M:N／CASCADE 等）。
6. 本檔不含 `## ERD`／`## DDL`／SQL；有 DB 時另產 `DDL.md`。
7. `## 假設` 固定掛在檔案最下方（約束清單之後），只寫領域／模型假設；引擎／落表假設寫在 `DDL.md`。
-->
