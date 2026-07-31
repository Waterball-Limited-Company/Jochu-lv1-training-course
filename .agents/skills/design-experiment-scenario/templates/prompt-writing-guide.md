# Prompt 撰寫規範：{{TOPIC_NAME}}

**實驗路徑**: {{EXPERIMENT_LANE}}（`Artifact` 或 `Skill`）
**對應課堂實驗**: {{SELECTED_SCENARIOS}}
**建立日期**: {{CREATED_DATE}}
**狀態**: 待 Review

## 規範目的

{{GUIDE_PURPOSE}}

## 適用範圍

{{GUIDE_SCOPE}}

## 撰寫原則

{{WRITING_PRINCIPLES}}

## 建議結構（大顆粒度）

{{PROMPT_STRUCTURE_OUTLINE}}

## 必須鎖住的範圍（不寫就容易偏）

{{MUST_LOCK_ITEMS}}

## 避免寫法

{{ANTI_PATTERNS}}

## 品質穩定檢查（跨 model）

{{STABILITY_CHECKS}}

## 本輪 Prompt 草稿（可選）

{{OPTIONAL_PROMPT_DRAFT}}

## Review 停等

請確認或修改本規範。  
- **Artifact** 路徑：確認後進入三 sub-agent 實跑。  
- **Skill** 路徑：確認後將正式 Prompt 交給**使用者**下 `/skill-engineering`；**禁止**直接改 skill。
