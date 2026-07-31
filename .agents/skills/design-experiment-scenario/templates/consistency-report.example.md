# 一致性驗證報告：api-plan → OpenAPI

> 本樣板**僅用於 Artifact 路徑**的三 sub-agent 實跑。

**建立日期**: 2026-07-30
**實驗路徑**: `Artifact`
**Prompt 規範版本／來源**: 抽換 API Artifact → OpenAPI 規範草稿
**來源 Artifact**: `specs/002-meeting-room-booking/system-analyze/api-plan.md`
**狀態**: 待 Review

## 實跑設定

| 項 | 內容 |
| --- | --- |
| Sub-agent 數量 | 3 |
| 模型（若固定） | composer-2.5-fast |
| 產物路徑 | `_prompt-consistency/openapi.run-A.yaml`／`…-B.yaml`／`…-C.yaml` |

## 穩定項（三跑相同或等價）

- `openapi: 3.0.3`，YAML 可 parse
- 13 個 endpoint 與來源 api-plan 一致
- 各 endpoint status 集合對齊
- 有共用 `ErrorResponse`；login 為公開端點

## 漂移項（不影響大品質者可接受）

- schema／tag 命名不同
- `info.version` 寫法不同
- security 掛全域或掛 operation 的差異

## 與來源 Artifact 對齊

- path／method 無增刪
- FR／US 有進 description（三跑皆有）

## 結論

- 大品質是否同檔：是（位元級不同，課程品質同檔）
- 建議定稿檔：A
- 是否可進 Phase 5 驗證紀錄：是

## Review 停等

請確認三跑品質是否可接受；未確認前不進入 Phase 5。
