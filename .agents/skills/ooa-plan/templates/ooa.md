# OOA 計畫：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: {{STATUS}}

**敘述階層（定稿）**

```text
## User Story（單位）
  ### Use Case（該故事底下的用例描述）
```

---

## 1. Use Case Diagram

> 正式 UML（Actor／橢圓／系統邊界）。Preview 不渲染 PlantUML 原始碼時，嵌入已匯出圖；來源見同目錄 PlantUML 檔。

![Use Case Diagram：{{FEATURE_NAME}}](./{{USE_CASE_DIAGRAM_PNG}})

**設計備註**

{{USE_CASE_DIAGRAM_NOTES}}

---

## 2. Use Case 敘述

### {{US1_ID}} - {{US1_TITLE}}

{{US1_USE_CASE_SECTIONS}}

### {{US2_ID}} - {{US2_TITLE}}

{{US2_USE_CASE_SECTIONS}}

{{ADDITIONAL_US_USE_CASE_SECTIONS}}

---

## 3. 領域 Class Diagram

```mermaid
{{DOMAIN_CLASS_DIAGRAM}}
```

**設計備註**

{{DOMAIN_CLASS_DIAGRAM_NOTES}}

---

## 4. 業務 Sequence Diagram

### 4.1 {{SEQUENCE_1_TITLE}}

```mermaid
{{SEQUENCE_1_DIAGRAM}}
```

### 4.2 {{SEQUENCE_2_TITLE}}

```mermaid
{{SEQUENCE_2_DIAGRAM}}
```

{{ADDITIONAL_SEQUENCE_SECTIONS}}

---

## 6. 假設

{{ASSUMPTION_ITEMS}}
