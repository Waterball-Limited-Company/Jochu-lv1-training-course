# DDL：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: 草稿
**對齊**: `system-analyze/data-plan.md`

## ERD

```mermaid
{{ERD_MERMAID}}
```

### 設計脈絡

{{DESIGN_CONTEXT_ITEMS}}

---

## DDL

> 單一腳本、多表並以註解區隔。建表順序：{{DDL_TABLE_ORDER}}。

```sql
{{DDL_SQL}}
```

## 假設

{{ASSUMPTION_ITEMS}}

<!--
填寫指引：
1. `{{ERD_MERMAID}}`：完整 Mermaid erDiagram 本體（不含外層 fence）。
2. `{{DESIGN_CONTEXT_ITEMS}}`：`- 因為…，所以…` 條列；只談實體間關聯形狀。無關聯時寫「本期無跨實體關聯」。
3. `{{DDL_TABLE_ORDER}}`：如 `albums` → `photos`。
4. `{{DDL_SQL}}`：單一腳本；表以 `-- ========== table_name ==========` 區隔。
5. `## 假設` 只寫引擎／落表前提，不重複 `data-plan.md` 領域假設。
-->
