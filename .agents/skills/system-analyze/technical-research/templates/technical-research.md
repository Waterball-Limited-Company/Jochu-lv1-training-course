# 技術可行性研究：{{FEATURE_NAME}}

**功能分支**: `{{PLAN_PACKAGE}}`
**建立日期**: {{CREATED_DATE}}
**狀態**: 草稿

## 決策 1: {{DECISION_1_TITLE}}

- **Decision**: {{DECISION_1_DECISION}}
- **Rationale**:
  - {{DECISION_1_RATIONALE_ITEM}}
- **Alternatives considered**:
  - {{DECISION_1_ALTERNATIVE_ITEM}}

## 決策 2: {{DECISION_2_TITLE}}

- **Decision**: {{DECISION_2_DECISION}}
- **Rationale**:
  - {{DECISION_2_RATIONALE_ITEM}}
- **Alternatives considered**:
  - {{DECISION_2_ALTERNATIVE_ITEM}}

{{ADDITIONAL_DECISION_SECTIONS}}

## 假設

{{ASSUMPTION_ITEMS}}

<!--
重複區塊與填寫指引：
1. `{{ADDITIONAL_DECISION_SECTIONS}}`：其餘決策，結構同「## 決策 N」整段（含 Decision／Rationale／Alternatives considered）。
2. 決策編號從 1 連續遞增；標題寫簡短決策軸，不要把整段 Decision 塞進標題。
3. `**Decision**` 寫出所選技術或做法；可用 inline code 標關鍵字。
4. `**Rationale**` 與 `**Alternatives considered**` 底下至少各有一條 `- ` 子項；Alternatives 每條固定寫成 `方案：不選原因`（冒號兩側皆不可空白）。
5. `## 假設` 固定掛在檔案最下方；格式與 `spec.md` 相同，使用 `- ` 條列。高影響未決須在決策正文使用 `[NEEDS CLARIFICATION: …]`；低風險只寫本節。對上游 `spec.md` 標記與本檔暫定取捨，澄清後回寫。
-->
