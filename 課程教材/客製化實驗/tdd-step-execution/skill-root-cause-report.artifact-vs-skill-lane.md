# Skill 根因確認閘門報告

## 任務資訊

- 處理路徑: `optimize`
- 目標 Skills: `design-experiment-scenario`
- 使用者問題: Phase 3／4 被寫死成「用 Prompt 修改 Artifact」；但像「修改 TDD 每一步執行方法」這類實驗**沒有 Artifact**，下一步應設計的是「描述如何用 `/skill-engineering` 改 Skill」的 Prompt，再用該 Prompt 做三跑可行性實驗。Skill 把兩條客製化路徑混成一條 Artifact 路徑，理解錯了。

## 預期結果

客製化實驗在勾選情境後，必須依槓桿分岔：

1. **有 Artifact（抽換／改產物形狀）**  
   - Phase 3：設計「修改 Artifact」的 Prompt 規範與草稿  
   - Phase 4：同一 Prompt × 同一來源 Artifact → 三 sub-agent 實跑 → 一致性報告  
   - Phase 5：再把定稿接進 Skill Eng（`/artifact-to-skill-engineering` 或 `/skill-engineering`）驗證可落地

2. **無 Artifact（直接改 Skill 執行方法／流程／約束）**  
   - Phase 3：設計的是「呼叫 `/skill-engineering`（含後續要交給它的修改描述／Prompt）」的撰寫規範與草稿——**不是**假裝在改某個 md／yaml Artifact  
   - Phase 4：用這份 Prompt 做實驗（三跑）確認**改 Skill 這條路可行、跨 model 大品質同檔**  
   - Phase 5：依實驗結果收斂 Skill Eng 驗證紀錄（通過／阻塞／已知債）；不可再假設「一定有定稿 Artifact 要抽換進 skill」

兩條路都是：先設計 Prompt → 再用 Prompt 實驗可行性；差在 Prompt 的**改造對象**是 Artifact 還是 Skill（經 skill-engineering）。

## 現況重演

- `SKILL.md` Phase 3 THINK 原文：「收斂『用 Prompt **修改 Artifact**』所需的撰寫規範」——無分岔。  
- Phase 4 WRITE／DELEGATE：「產出正式『**修改 Artifact**』Prompt」「相同來源 **Artifact**」「比對與**來源**對齊」。  
- Phase 5 THINK：「依已確認的定稿 **Artifact**／實驗意圖」呼叫 artifact-to-skill-engineering 或 skill-engineering。  
- `templates/prompt-writing-guide.example.md`、`consistency-report.md` 欄位皆以來源 Artifact／產物對齊為預設。  
- 本次 TDD 選項 A 實驗：目標是改 `tdd-e2e-green` 的執行政策，**沒有**系統分析 Artifact；執行者仍被 SOP 導向 Artifact 語意（或自行把 skill 檔硬套成「Artifact」），與使用者預期的「Prompt → `/skill-engineering` → 改 skill → 三跑驗證」不符。

## 落差分析

| 預期 | 現況 |
|------|------|
| Phase 3 依有無 Artifact 選 Prompt 類型 | 一律「改 Artifact」 |
| 無 Artifact 時 Prompt 描述 `/skill-engineering` 改 skill | 未編碼；example／consistency 也不支援 |
| Phase 4 實驗「這條客製化 Prompt 是否可行」 | 寫死為 Artifact 三跑比對 |
| Phase 5 在 Skill 路徑上可能已是實驗本體的延伸 | 仍假設先有定稿 Artifact 再做 Skill Eng |

根因不在單次執行疏忽，而在控制平面把「抽換 Artifact」當成唯一實驗骨架。

## 根因

- 根因類型: `Control-Plane Gap`
- 改動範圍: `skill rewrite`（至少重寫 Phase 3～5 分岔；template／rule／description 一併對齊）
- 失敗原因: SOP 與樣板只建模「Artifact 修改實驗」一條 lane，沒有「Skill 修改實驗（Prompt → skill-engineering）」lane，導致無 Artifact 的課綱題（改 TDD 步驟執行方法、改 TDD 流程、改架構約束等）被錯誤導流。

## 影響範圍

- `.agents/skills/design-experiment-scenario/SKILL.md`（Phase 3～5、front matter description）
- `templates/prompt-writing-guide.md`／`.example.md`（需能表達兩種 Prompt 類型，或分 example）
- `templates/consistency-report.md`／`.example.md`（Skill 路徑改為比對三份 skill 改動結果，而非來源 Artifact）
- `templates/skill-eng-validation.md`／`.example.md`（Skill 路徑下的驗證語意）
- `rules/人工Review閘門判準.md`（停等文案若寫死 Artifact）
- 進行中實驗：`課程教材/客製化實驗/tdd-step-execution/prompt-writing-guide.md`（確認後應依新契約重寫為 skill-engineering 取向）

## 候選刪除項

- Phase 3／4／5 中「一律修改 Artifact」的單一敘事（改為分岔，刪掉強制 Artifact 前提）
- consistency-report 必填「來源 Artifact」在 Skill lane 的硬性欄位（改為來源 Skill／改造對象，或兩欄互斥）
- Phase 5 在「Skill lane 三跑已是 skill-engineering 實驗」時，重複、空轉的「再假設有 Artifact 定稿」步驟措辭（收斂成驗證紀錄，避免雙重誤會）

## 確認閘門

請確認以上根因與落差分析是否成立；未收到確認前，**停止**後續編排提案與對 `design-experiment-scenario` 的檔案修改。

確認後下一步：提出 Phase 3～5 雙 lane（Artifact／Skill）的 skill-engineering plan，再落地改 SOP／templates。
