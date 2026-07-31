---
name: design-experiment-scenario
description: 依課程內容設計客製化實驗場景：收斂目標並產出排序情境供勾選；確認後分岔——Artifact 路徑用條列 Prompt 直接改產物並三跑比對；Skill 路徑只設計「請使用者呼叫 /skill-engineering」的條列 Prompt，禁止直接改 skill 流程／檔案。每階段停等人工 Review。Use when the user invokes /design-experiment-scenario, asks to design course experiment scenarios / 設計實驗場景, or needs goals→ranked scenarios→prompt norms→consistency runs→skill-eng validation from curriculum content.
disable-model-invocation: true
---

# 設計實驗場景

以「課程內容」為主要輸入，為客製化訓練設計可執行的實驗場景。控制平面採人工 Review 閘門：每一階段產出後必須停等使用者確認或修改，未確認不得進入下一階段。本期完成至 Skill Engineering 驗證可修改即可，不要求一次產出完整學員教材包。

自 Phase 3 起必須分岔：

- **Artifact 路徑**：條列式 Prompt **直接**改產物 → Phase 4 三 sub-agent 實跑比對。
- **Skill 路徑**：條列式 Prompt 描述呼叫 **`/skill-engineering`** → **禁止**直接改 skill 流程／檔案 → Prompt 交給**使用者**下 `/skill-engineering`；執行者不得代改正式 skill，也不得用暫定目錄複本直接改來假裝完成。

# SOP

## Phase 1 -- 收斂課程內容範圍

1. READ 讀取使用者提供的課程內容與既有上下文，確認本次要設計實驗的範圍（例如課綱某一條實戰訓練、某個客製化目標）。
2. THINK 若範圍仍含糊到無法設計實驗，先向使用者提出最小必要確認並停止；範圍清楚後收斂一句話的本次設計主題。
3. WRITE 向使用者覆述本次範圍（一句話主題），並說明下一步將以改版格式產出單行範圍句與 5～10 個排序選項卡片；可先進入 Phase 2 草擬，但若使用者修正範圍，Phase 2 產物必須依新範圍重做後再停等勾選。

## Phase 2 -- 定義目標並產出排序情境

1. READ 先讀取 `rules/情境列舉與排序判準.md`。
2. THINK 依本次已載入規則與課程內容，收斂實驗目標與客製化槓桿，壓成單行「範圍」句；並列出 5 至 10 個可能性，依優先順序排序（教學效益、可觀測性、課堂可完成性、與客製化槓桿對齊）。
3. WRITE 先讀取 `templates/experiment-goals-and-scenarios.md` 與 `templates/experiment-goals-and-scenarios.example.md`，再依**改版格式**骨架產出：標題 `Phase 2 (改版格式)｜主題`、單行 `**範圍**`、以及 **5～10 張已排序選項卡片**（`### 選項 X｜…`；欄位含怎麼實作／為何效益高／學員瞬間看懂的點／評分列；優先序以選項 A 為最高），請使用者以字母勾選。不可改回舊企劃外殼（課程來源／建立日期／獨立長段實驗目標）作為 Review 主呈現。
4. READ 讀取 `rules/人工Review閘門判準.md`，依閘門停等使用者 Review 或修改；未確認課堂實驗選項前，不進入 Phase 3。

## Phase 3 -- 設計 Prompt 撰寫規範

1. READ 讀取 `rules/人工Review閘門判準.md`（若本 session 尚未載入）。
2. READ 讀取 `rules/實驗路徑分岔判準.md`。
3. THINK 依已確認課堂實驗與本次已載入分岔規則，判定實驗路徑為 `Artifact` 或 `Skill`；再收斂對應 Prompt 撰寫規範：跨 model 仍能維持相近品質，大顆粒度、可重複、條列式、少實作細節堆砌但仍鎖住必改範圍。Artifact 路徑＝「請參照…，將此 Artifact 修改…」。Skill 路徑＝「請呼叫 `/skill-engineering`，目標 skill 為…，符合以下規範…」（給**使用者**下指令；**禁止**設計成直接改 skill 檔）。
4. WRITE 先讀取 `templates/prompt-writing-guide.md` 與 `templates/prompt-writing-guide.example.md`，再依骨架產出 Prompt 撰寫規範（抬頭必須標明實驗路徑）；必要時附上該次實驗可用的 Prompt 草稿，但規範本身須與單次草稿分離可複用。
5. READ 依已載入之人工 Review 閘門停等使用者 Review 或修改規範；未確認前，不進入 Phase 4。

## Phase 4 -- 驗證可行性（依路徑分岔）

1. READ 讀取 `rules/人工Review閘門判準.md`（若本 session 尚未載入）；若尚未持有分岔結論，讀取 `rules/實驗路徑分岔判準.md` 與 Phase 3 產物抬頭。
2. WRITE 依已確認規範，產出該次實驗的正式 Prompt（優先在對話列出；使用者要求落盤再寫檔）。Artifact 路徑：正式「修改 Artifact」條列 Prompt。Skill 路徑：正式「請呼叫 `/skill-engineering`」條列 Prompt；並明確告知：請**使用者**自行下 `/skill-engineering` 並貼上此 Prompt——執行者不會直接改目標 skill，也不會對 skill 複本做三跑改檔。
3. THINK 依實驗路徑決定下一步：Artifact → 三跑；Skill → 停等使用者下 `/skill-engineering`（本 skill 與 sub-agent **不得**直接改 skill 或 skill 複本）。
4. DELEGATE 僅 **Artifact** 路徑：以相同 Prompt、相同來源 Artifact，並行啟動三個 sub-agent 各寫入獨立暫定產物，避免互相覆蓋。Skill 路徑：跳過本步。
5. THINK 僅 Artifact 路徑：比對三份產物的結構完整性、與來源對齊、彼此一致性。Skill 路徑：若使用者已回傳 skill-engineering 結果則整理摘要；尚未下指令則保持停等。
6. WRITE 僅 Artifact 路徑：先讀取 `templates/consistency-report.md` 與 `templates/consistency-report.example.md`，再依骨架產出一致性驗證報告（實驗路徑標 `Artifact`）。Skill 路徑：不產三跑 consistency；可寫短註「已交付 Prompt／等待或已完成使用者 skill-engineering」。
7. READ 依已載入之人工 Review 閘門停等；Artifact 確認三跑品質；Skill 確認使用者已完成（或授權下一步）skill-engineering。未確認前不進入 Phase 5。

## Phase 5 -- Skill Engineering 驗證紀錄

1. READ 讀取 `rules/人工Review閘門判準.md`（若本 session 尚未載入）。
2. THINK 依實驗路徑與已確認結果收斂驗證目標，並明示設計約束：不要過度工程、先從最簡單 SOP 開始、rules 按需疊代且必須掛回主 SOP。Artifact 路徑：定稿產物能否抽換進既有 skill（常經 `/artifact-to-skill-engineering` 或再經 `/skill-engineering`，且仍由使用者確認閘門）。Skill 路徑：記錄使用者以 Phase 4 Prompt 走 `/skill-engineering` 是否通過；**不可**假設有定稿 Artifact，也**不可**由本 skill 回頭直接改目標 skill。
3. DELEGATE 僅在使用者要求且路徑需要時，協助整理交付內容或依其指示呼叫相關 skill；不得跳過確認閘門，**不得代為直接改目標 skill 檔**。
4. WRITE 先讀取 `templates/skill-eng-validation.md` 與 `templates/skill-eng-validation.example.md`，再依骨架記錄驗證過程要點與結論（通過／阻塞／已知債）；抬頭標明實驗路徑。
5. READ 依已載入之人工 Review 閘門停等使用者確認本期是否結束；若需回到某一階段重做，回到對應 phase，勿默默擴大範圍。
