# 一致性驗證報告：{{TOPIC_NAME}}

> 本樣板**僅用於 Artifact 路徑**的三 sub-agent 實跑。Skill 路徑不要使用本樣板去記錄「改 skill 三跑」。

**建立日期**: {{CREATED_DATE}}
**實驗路徑**: `Artifact`
**Prompt 規範版本／來源**: {{PROMPT_GUIDE_REF}}
**來源 Artifact**: {{SOURCE_ARTIFACT_PATH}}
**狀態**: 待 Review

## 實跑設定

| 項 | 內容 |
| --- | --- |
| Sub-agent 數量 | 3 |
| 模型（若固定） | {{MODEL_NAME}} |
| 產物路徑 | {{RUN_A_PATH}}／{{RUN_B_PATH}}／{{RUN_C_PATH}} |

## 穩定項（三跑相同或等價）

{{STABLE_FINDINGS}}

## 漂移項（不影響大品質者可接受）

{{DRIFT_FINDINGS}}

## 與來源 Artifact 對齊

{{ALIGNMENT_FINDINGS}}

## 結論

- 大品質是否同檔：{{QUALITY_VERDICT}}
- 建議定稿檔：{{RECOMMENDED_RUN}}
- 是否可進 Phase 5 驗證紀錄：{{READY_FOR_SKILL_ENG}}

## Review 停等

請確認三跑品質是否可接受；未確認前不進入 Phase 5。
