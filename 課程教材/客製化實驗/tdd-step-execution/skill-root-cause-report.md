# Skill 根因確認閘門報告

## 任務資訊

- 處理路徑: `optimize`
- 目標 Skills: `design-experiment-scenario`
- 使用者問題: Phase 2 應用「改版格式」（`Phase 2 (改版格式)｜主題` + 單行範圍 + 選項卡片）呈現「改 Skill」類實驗；實際卻產出舊的完整文件骨架（課程來源／建立日期／實驗目標長段），與已約定的改版呈現不一致。

## 預期結果

- Phase 2 對使用者的主呈現為改版格式：
  - 標題：`## Phase 2 (改版格式)｜{{TOPIC}}`
  - 單行：`**範圍**：…`（寫清客製化槓桿：改 Skill／rules，並與易混淆題目區隔）
  - 其後直接 5～10 張選項卡片（`### 選項 X｜…` + 怎麼實作／為何效益高／學員瞬間看懂的點／評分列）
  - 結尾請以字母勾選
- 「改 Skill」類課綱題（加強顆粒度、改 TDD 步驟執行方法等）標題語感應對齊參考例（如 `改／加深 {{skill或步驟}}：{{變更點}}`），而不是先堆完整實驗企劃文件再給選項。
- 後續仍可把同一內容落盤；但對話 Review 契約以改版格式為準。

## 現況重演

- 盤點 `design-experiment-scenario`：Phase 2 WRITE 強制讀取並依 `templates/experiment-goals-and-scenarios.md` 與 `.example.md` 產出。
- 該骨架必填：課程來源、建立日期、狀態、本次範圍、**實驗目標**長段、再才是「情境可能性」與選項。
- `rules/情境列舉與排序判準.md` Rule 1 要求先寫「實驗目標」再列情境；Good Example 也是 `## 實驗目標` + 文件式選項，**沒有**編碼 `Phase 2 (改版格式)` 標題與單行範圍呈現。
- 本次執行嚴格跟 template／rule → 產出舊文件式 Phase 2；使用者指出應與「加強系統分析顆粒度」那份改版格式一致。

## 落差分析

- 預期是「改版格式」的對話／Review 契約；現況是「實驗企劃文件」契約。
- 欄位內容（怎麼實作等）大致對，但**外殼與資訊層級**錯：多餘的日期／狀態／目標長段淹沒「範圍一句話 + 選項卡片」。
- 根因不在單次執行疏忽，而在 Phase 2 的 template／rule 仍把舊外殼當成 MUST；agent 越遵守 skill，越偏離已約定改版格式。

## 根因

- 根因類型: `Template/Rule Spec Gap`
- 改動範圍: `step rewrite`（Phase 2 WRITE 路徑：template + example + 情境列舉規則；必要時 SKILL Phase 2 對齊一句）
- 失敗原因: Phase 2 控制平面只規定「選項卡片欄位與排序」，沒有把「改版格式」定成主呈現契約，仍溯源到舊的 `experiment-goals-and-scenarios` 企劃骨架，導致「改 Skill」實驗無法穩定輸出與參考截圖一致的格式。

## 影響範圍

- `.agents/skills/design-experiment-scenario/SKILL.md`（Phase 2 WRITE 描述）
- `rules/情境列舉與排序判準.md`（呈現契約／目標如何收斂進「範圍」）
- `templates/experiment-goals-and-scenarios.md`
- `templates/experiment-goals-and-scenarios.example.md`
- 後續所有 `/design-experiment-scenario` Phase 2 產出（含本次 TDD 步驟執行方法實驗）

## 候選刪除項

- template 必填的「建立日期／狀態」作為 Phase 2 **對話主呈現**欄位（可刪或降為可選落盤 meta）
- 獨立長段 `## 實驗目標` 作為主呈現必填（改為收斂進 `**範圍**` 一句／短句；詳細目標若需保留可放落盤附註，不當 Review 主體）
- example 中「抽換 Artifact」舊企劃外殼若與改版格式衝突的章節標題（改寫為改版格式 example，避免雙重真相）

## 確認閘門

請確認以上根因與落差分析是否成立；未收到確認前，**停止**後續編排提案與對 `design-experiment-scenario` 的檔案修改。

確認後我再提 skill-engineering plan（重建 Phase 2 呈現契約 → 改 template／rule／example）。  
你確認 skill 根因後，再回答 TDD 情境勾選（`A` / `A, C` 等）即可。
