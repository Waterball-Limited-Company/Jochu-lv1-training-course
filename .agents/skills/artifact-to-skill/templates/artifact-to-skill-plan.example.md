# Artifact to Skill 工程提案

## 任務資訊

- benchmark artifact: `/.agents/skills/my-specify/templates/spec.example.md`
- target artifact: `改寫後、以 User Story 為主體的 spec 成品`
- 目標 skill: `my-specify`
- 改動範圍: `skill rewrite`

## 控制平面

- 先把 benchmark spec 改成使用者滿意的 target artifact。
- 再從 target artifact 抽出 `spec.template.md`。
- 接著反推要穩定重現這份 spec 所需的推理流程、rules、templates 與 validator。
- 最後把整套方法落地成 `my-specify/SKILL.md`、`rules/`、`templates/` 與 `scripts/`。

## 模組決策

- `artifact 改寫`：keep inline，保留在主 SOP。
- `高影響結構決策`：keep inline，必要時 handoff 到 `/clarify`。
- `語意切分、故事切分、成功標準生成`：derive rule。
- `mapping checklist`：derive template。
- `spec 骨架與 example`：derive template。
- `靜態結構檢查`：derive script。

## 檔案動作

### 新增 / 更新

- Update `my-specify/SKILL.md`
- Create `my-specify/rules/輸入正規化與語意切分判準.md`
- Create `my-specify/rules/使用者故事切分與合併判準.md`
- Create `my-specify/rules/成功標準生成判準.md`
- Create `my-specify/templates/spec-mapping-checklist.template.md`
- Create `my-specify/templates/spec-mapping-checklist.example.md`
- Update `my-specify/templates/spec.template.md`
- Create `my-specify/scripts/validate_spec_output.py`

### 刪除

- 刪除舊版把 FR 與成功標準散落在全域區的 artifact 結構

## 驗證方式

- 重新閱讀 `my-specify/SKILL.md`，確認先有 target artifact，後有 template，再有 skill engineering。
- 重新檢查每個新增 module 是否都能回掛到主 SOP 的讀取或執行時機。
- 用 benchmark prompt 重跑一次生成流程，確認最終輸出穩定落在 target artifact 結構。

## 實作閘門

- 若使用者只要求提案，停在此處。
- 若使用者已確認 plan 並要求落地，依本 plan 實作與清理。
