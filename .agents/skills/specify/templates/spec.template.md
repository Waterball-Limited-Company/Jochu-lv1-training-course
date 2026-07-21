<!-- 先完成 `spec-mapping-checklist` 的語意映射，再回填此模板；不得直接從原始 prompt 跳寫最終 spec。 -->
<!-- 本模板對應的最終輸出檔固定為 `/specs/<NNN-plan-package>/spec.md`。 -->

# 功能規格：{{FEATURE_NAME}}

**功能分支**：`{{FEATURE_BRANCH}}`<br>**建立日期**：{{CREATED_DATE}}<br>**狀態**：{{STATUS}}<br>**輸入需求**：{{INPUT_REQUIREMENTS}}

## 使用者故事與驗證 *(必填)*

<!-- 依需求複製以下「使用者故事」區塊；故事編號請依序遞增（US1、US2…），並刪除未使用的區塊。每個故事只保留一個可獨立感知的使用者價值。 -->

### 使用者故事 {{USER_STORY_NUMBER}} - {{USER_STORY_TITLE}}（優先級：{{USER_STORY_PRIORITY}}）

{{USER_STORY_DESCRIPTION}}

**為何列為此優先級**：{{USER_STORY_PRIORITY_RATIONALE}}

**獨立驗證方式**：{{USER_STORY_INDEPENDENT_VERIFICATION}}

**功能需求**

<!-- 依需求增刪功能需求條目；編號請在故事內遞增（FR1、FR2…）。每條 FR 都必須歸屬到單一故事。需求若有待釐清，可使用 [NEEDS CLARIFICATION: {{CLARIFICATION_NOTE}}] 標記。 -->

- **US{{USER_STORY_NUMBER}}-FR1**：{{USER_STORY_FR_1}}
- **US{{USER_STORY_NUMBER}}-FR2**：{{USER_STORY_FR_2}}

**成功標準**

<!-- 依需求增刪成功標準條目；編號請在故事內遞增（SC1、SC2…）。成功標準必須對應此故事的主要使用者價值。 -->

- **US{{USER_STORY_NUMBER}}-SC1**：{{USER_STORY_SC_1}}
- **US{{USER_STORY_NUMBER}}-SC2**：{{USER_STORY_SC_2}}

**驗收情境**

<!-- 依需求增刪驗收情境；每則情境使用「假設 / 當 / 則」格式。 -->

1. **假設** {{ACCEPTANCE_SCENARIO_1_GIVEN}}，**當** {{ACCEPTANCE_SCENARIO_1_WHEN}}，**則** {{ACCEPTANCE_SCENARIO_1_THEN}}
2. **假設** {{ACCEPTANCE_SCENARIO_2_GIVEN}}，**當** {{ACCEPTANCE_SCENARIO_2_WHEN}}，**則** {{ACCEPTANCE_SCENARIO_2_THEN}}

**邊界情境**

<!-- 依需求增刪邊界情境；僅保留與此故事直接相關的項目。 -->

- {{USER_STORY_EDGE_CASE_1}}
- {{USER_STORY_EDGE_CASE_2}}

## 共通規則與全域約束

<!-- 只有跨故事且永遠成立的限制才可放在此章節；若無此類限制，可刪除此整段章節。 -->

- **GR-001**：{{GLOBAL_RULE_1}}

### 全域邊界情境

<!-- 依需求增刪全域邊界情境。 -->

- {{GLOBAL_EDGE_CASE_1}}

## 關鍵實體 *(僅在功能涉及資料時保留)*

<!-- 若功能不涉及資料模型，可刪除此整段章節。 -->

- **{{ENTITY_NAME_1}}**：{{ENTITY_DESCRIPTION_1}}
- **{{ENTITY_NAME_2}}**：{{ENTITY_DESCRIPTION_2}}

## 假設

- {{ASSUMPTION_1}}
- {{ASSUMPTION_2}}
- {{ASSUMPTION_3}}
- {{ASSUMPTION_4}}
