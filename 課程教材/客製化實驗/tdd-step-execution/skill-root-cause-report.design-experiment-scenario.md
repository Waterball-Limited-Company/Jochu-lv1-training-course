# Skill 根因確認閘門報告

## 任務資訊

- 處理路徑: `optimize`
- 目標 Skills: `design-experiment-scenario`
- 使用者問題: 實驗流程 skill 把 Artifact／Skill 搞混——有 Artifact 才用條列 Prompt 直接改產物並三跑；無 Artifact（改 skill）時不可直接改 skill 流程，必須設計「請使用者呼叫 `/skill-engineering`」的 Prompt，由使用者下指令。先前還錯誤地對 skill 複本做三跑直接改檔。

## 預期結果

- Phase 3 起強制分岔 `Artifact`／`Skill`。
- Artifact：條列「請參照…將此 Artifact 修改…」→ Phase 4 三 sub-agent 實跑 → consistency。
- Skill：條列「請呼叫 `/skill-engineering`…符合以下規範…」→ **禁止**直接改 skill／複本 → 交付使用者下指令 → Phase 5 記錄結果。
- templates／Review 閘門語意與上述一致，無「Skill 三跑改檔」殘留。

## 現況重演

- `SKILL.md` 與 `rules/實驗路徑分岔判準.md` 已寫入雙路徑與「禁止直接改 skill」。
- 仍有殘留：`consistency-report.md` 仍含 Skill 路徑欄位與「三跑產物」預設，易誘使 Skill 也走三跑；Phase 4 Artifact 未明確 READ `consistency-report.example.md`（盤點顯示 example 未引用）；Phase 4 有合併動詞 step；`人工Review`／prompt 骨架對 Skill「只交使用者下指令」強調不足。

## 落差分析

| 預期 | 現況 |
|------|------|
| Skill 路徑無三跑改 skill | SOP 已禁，但 consistency template 仍像通用三跑 |
| Artifact 完整讀 template 雙檔 | example 未掛回 SOP → unreferenced |
| Review 文案依路徑分岔 | 部分仍暗示一律三跑 |

## 根因

- 根因類型: `Control-Plane Gap`（殘留 Spec／Template 不一致）
- 改動範圍: `step rewrite`
- 失敗原因: 控制平面已轉向雙路徑，但 consistency／Review／SOP 掛接未清乾淨，執行者仍可能把 Skill 實驗做成 Artifact 式三跑改檔。

## 影響範圍

- `SKILL.md` Phase 4～5
- `rules/實驗路徑分岔判準.md`、`rules/人工Review閘門判準.md`
- `templates/consistency-report.md`／`.example.md`
- `templates/prompt-writing-guide.md`／`.example.md`
- `templates/skill-eng-validation.md`（Skill 路徑語意）

## 候選刪除項

- consistency 中「Skill 路徑也當三跑改 skill 產物」的必填語意
- Phase 4 合併動詞 `THINK／DELEGATE` 單步（拆成可執行 steps）

## 確認閘門

使用者已指示「先修改實驗流程設計的 skill」→ 視為授權依本根因落地；下列為同步編排與實作。
