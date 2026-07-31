# Skill 工程編排提案｜取料先行 × 實驗 Prompt 即產物

## 任務資訊

- 處理路徑: `optimize`
- 改動範圍: `sop rebuild`（外層 SOP 重切 + rules 汰換 + templates 換骨架）
- 目標 Skills: `design-experiment-scenario`
- 依據: `260730 水球 review — skill TODO`（第一題通過答案、第二題打回原則）＋ 使用者本次流程設計

## 術語（先定名，全 skill 一致）

| 詞 | 指涉 | 備註 |
|---|---|---|
| **實驗 Prompt** | 本 skill 的主產物；交付給學員在課堂使用的那份 Prompt | 舊稱「第二步的 artifact」 |
| **目標 Artifact** | 實驗 Prompt 執行時要被修改的對象＝**目標 skill 的 `templates/*.example.md`** | 舊稱「來源 Artifact」；水球：「artifact 後面接的叫 example」 |
| **目標 Skill** | 目標 Artifact 所屬的 skill，其 `SKILL.md`／`rules/` 為行為規範 | **其 `SKILL.md`／`rules/`** 只能由 `/artifact-to-skill-engineering`、`/skill-engineering` 改；`templates/*.example.md` 不在此限（那就是目標 Artifact） |
| **Artifact First** | 只綁**目標 Artifact**：實驗 Prompt 內部的步驟順序必須「先改目標 Artifact，再反推目標 Skill」 | 不綁實驗 Prompt |

一詞兩義是本次最大的行為風險：不定名，`Artifact First` 會被 AI 解讀成「先寫 Prompt」。

### example 與 skill 行為規範的界線（本次關鍵判斷）

> ⚠️ **本節僅為提案理由，不落地。** 規範以 `實驗Prompt結構判準` Rule 3 為唯一來源；不得把本節寫進 `SKILL.md` 前言或另開一份 rule，否則同一條規範會出現在三個地方。（標題刻意不用「判準」二字——`*判準.md` 是本 repo 的 rule 檔命名詞。）

改 `templates/*.example.md` **不等於**改 skill 行為 —— example 是產物長相，`SKILL.md`／`rules/` 才是行為規範。Artifact First 的完整因果是：先改 example 的長相，再由 `/artifact-to-skill-engineering` 把長相變更**反推**成行為規範變更。所以：

- 實驗 Prompt（**學員在課堂執行時**）**可以**改目標 Artifact（＝目標 skill 的 `templates/*.example.md`）
- 實驗 Prompt **不可以**改目標 skill 的 `SKILL.md`／`rules/`
- **本 skill 及其 sub-agent 一律不得改目標 skill 的任何檔案，含 `templates/*.example.md`** —— 三跑止於「產出可視化規劃」，本來就碰不到 example；「可以改 example」只授權給課堂上的學員，不授權給執行者

## 控制平面重建

### 兩層模型（本次的核心改動）

**外層 — 本 skill 的 SOP（設計者側）**：收斂主題 → 取料設計 → 設計實驗 Prompt → 三跑驗穩定 → 交付。

**內層 — 實驗 Prompt 的內容（學員側，Prompt 內固定四步）**：
1. 用 Prompt 找資料，走過發散 → 收斂
2. 產出**可視化規劃** → 停等學員 review → **學員自行下 `/clarify`** 補齊細節
3. 規劃確認後改**目標 Artifact**（`templates/*.example.md`）
4. 改完呼叫 `/artifact-to-skill-engineering` 由 example 反推目標 Skill，必要時再接 `/skill-engineering`

舊版把內層四步誤置為外層 phase，導致執行者自己去改 skill；本次以兩層分離根治。

第四步保留 `/artifact-to-skill-engineering` 是水球第一題通過答案的原文（「再用 skill engineering 跟 artifact-to-skill 去反推 skill」），不可簡化成只呼叫 `/skill-engineering`。

### 三跑的邊界（承接舊 Phase 4，但範圍改寫）

三跑的目的改為驗**同一份實驗 Prompt 不管怎麼執行、品質是否相同**。因此三跑**只跑內層第一～二步**（找資料 → 發散收斂 → 產出可視化規劃），三個 sub-agent 各寫入獨立暫定產物，比對三份**可視化規劃**的一致性後即停。

不跑第三、四步，原因有二：第二步結尾本來就要停等學員 review（sub-agent 沒有學員可停等）；第三、四步會動到目標 Artifact 與目標 Skill，屬於課堂上學員的動作，執行者代跑等同代改。

現存殘留須一併清除：`課程教材/客製化實驗/tdd-step-execution/_prompt-consistency/tdd-e2e-green.run-A|B|C/`（各含 SKILL.md ＋ 4 rules 的 skill 複本）正是上次越過此邊界的產物。

### 實驗路徑分岔：廢除

舊版 Phase 3 起分岔 `Artifact` / `Skill` 兩條平行路徑。新模型中**不存在這個岔口** —— 每一份實驗 Prompt 都是「先目標 Artifact、後反推目標 Skill」的線性四步。分岔判準整條報廢，其中「禁止執行者直接改 skill」的防線移入實驗 Prompt 結構判準續存（但禁改範圍依上節界線收斂）。

### 勾選卡片：廢除

舊版 Phase 2 產 5～10 張選項卡片請使用者勾字母。使用者判定「不懂勾選要勾什麼」，整組拿掉。其中「先收斂目標成單行範圍句」的價值保留，下沉為 Phase 1 的收斂動作，**並在 Phase 1 補上 Review 閘門**（範圍句是 Phase 2 判型的唯一依據，無人確認會讓整條取料鏈連帶錯）。

## 步驟決策

| Phase | 決策 | 內容 |
|---|---|---|
| Phase 1 收斂實驗主題 | rewrite | 讀課程內容 → 收斂單行範圍句 → **停等 Review**；刪除「下一步產出排序選項卡片」的預告，但**必須保留** `SKILL.md:22` 後半「若使用者修正範圍，下游產物須依新範圍重做後再停等」（新模型下更關鍵：範圍一改，判型可能從機制型翻成內容型，整份原料清單作廢）。⚠️ 該句原文結尾是「再停等**勾選**」，保留時必須把「勾選」二字改掉，否則會踩到本 plan 自己的 grep 驗證條件 |
| Phase 2 取料設計 | **new** | 判定機制型／內容型 → 內容型列關鍵字／書名 → 收斂原料清單 → 停等 |
| Phase 3 設計實驗 Prompt | rewrite | 依原料清單寫出實驗 Prompt（內含固定四步）→ 停等使用者 review 並修改 → 定稿 |
| Phase 4 三跑一致性 | rewrite | 定稿 Prompt 三 sub-agent 實跑**至「產出可視化規劃」為止**（不含第二步結尾的停等學員 review 與 `/clarify`），比對三份可視化規劃 → 停等 |
| Phase 5 教材交付紀錄 | rewrite | 打包定稿 Prompt ＋ 原料清單 ＋ 三跑結論為可上課教材；**MUST 記錄三跑覆蓋率邊界**（內層第三、四步未經任何機制驗證即交付）＋ 其他已知債 |

### Rules

- `情境列舉與排序判準.md` — **DELETE**（勾選卡片廢除，整條失效）
- `實驗路徑分岔判準.md` — **DELETE**（岔口不存在）
- `人工Review閘門判準.md` — **rewrite（非薄修）**：全檔含舊模型死語意，逐條列於下方
- `取料來源判準.md` — **NEW**
- `實驗Prompt結構判準.md` — **NEW**

#### `人工Review閘門判準.md` 的 rewrite 清單（逐行）

| 行 | 死語意 | 處置 |
|---|---|---|
| `:4` | Phase 2 情境清單、Phase 4 依路徑分岔 | 改為 Phase 1 範圍句／Phase 2 原料清單／Phase 3 Prompt 定稿／Phase 4 三跑結論／Phase 5 交付 |
| `:10` | 「停點與確認方式依路徑清楚」 | 刪路徑語意 |
| `:13` | 「請勾選選項字母」 | 刪 |
| `:15` | 「標明 Artifact 或 Skill」 | 刪 |
| `:17` | Phase 4（Artifact）：請確認三跑一致性報告 | 改為單一 Phase 4 文案 |
| `:18` | Phase 4（Skill）路徑 | 刪 |
| `:23` | 「或 Skill 路徑擅自三跑改 skill」 | 改為「越過『產出可視化規劃』這個停點代跑第三、四步」 |
| `:26` | 「已列出情境，接著我先把 Prompt 規範與三跑都做完」 | Bad Example 改為範圍句／原料清單語境 |
| `:32` | 情境排序 | 刪 |
| `:40` | 「刪除選項 H 並重排序 → 請再次確認勾選字母」 | 整段 Good Example 重寫 |
| `:48` | 「用原選項 A 繼續寫規範」（Rule 2 **Bad** Example） | 整段重寫 |
| `:54` | 「使用者可決定本期只做到某一階段（例如 Artifact 只到三跑、Skill 只到交付 Prompt）」 | ⚠️ 與 `:55` 同型 —— 本行職責是**授權使用者縮範圍**，不是複述 SOP 停點（停點已在 `SKILL.md` Phase 4 與 Rule 3 layer 2，複述會變成同一句出現在三個檔）。只換掉分岔舉例：「使用者可決定本期只做到某一階段（例如只到 Phase 2 原料清單，或只到 Phase 4 三跑結論）；各 Phase 停點定義見 `SKILL.md`」 |
| `:55` | 「**執行者**不得…直接改目標 skill」 | ⚠️ 非死語意，主詞是**執行者**＝ Rule 3 **layer 2**。**不可**收斂成「只禁 `SKILL.md`／`rules/`」（那是 layer 1 的範圍，會變成明文對執行者開放 example）。但也**不可複述整份禁改清單** —— 本檔 Rule 3 的主題是「允許使用者縮範圍，禁止執行者擅自擴範圍」，不是禁改清單，複製過來會踩到「同一個規則重複提及」且日後必然漂移。正解是**改為引用**：「執行者不得在未要求下自動補做完整學員 SOP、下游全鏈接線，或代跑內層第三、四步；禁改範圍見 `實驗Prompt結構判準` Rule 3 layer 2。」 |
| `:63` | 「本期到交付 /skill-engineering Prompt 為止」 | 改為本期到教材交付紀錄為止 |

Rule 2、Rule 3 的 Good **與 Bad** Example 整段皆為舊模型措辭（含選項字母、路徑分岔），需整段重寫。全檔 72 行。

### 新 Rule 1：`取料來源判準.md`

- **Rule 1（MUST）先判型，再決定解法誰給**
  判型 MUST 以 **Phase 1 已確認的範圍句**為唯一依據；範圍句未經 Review 閘門確認前不得判型。範圍句事後被修正時，判型與原料清單 MUST 重做。
  - **機制型**：只示範「可以這樣改」，不宣稱「這樣比較對」→ 不需外部取料，設計者可直接給具體改法
  - **內容型**：要宣稱「這樣品質比較好／顆粒度比較夠／比較正確」→ 進入 Rule 2
  評估「為何適合當課堂教材」屬教學效益判斷，不算內容型宣稱。
  禁止一律套外部取料（水球明確踩煞車：「不是每一題都是電子書」）。

- **Rule 2（MUST）內容型的解法不得取自設計者的知識儲備**
  **僅適用內容型。** 情境的實質解法（方法論／品質標準／該有多細）不可由設計者直接給出，必須改寫為「指定 AI 取料的方式」。
  Bad Example 直用被打回的答案：`加強系統分析顆粒度 → 加 OOA 跟 C4 model`。
  理由寫進 rule：學員知識儲備不足，要教的是低儲備前提下能自己舉一反三的做法；給了 solution 就要負責。

- **Rule 3（MUST）取料形式：關鍵字優先，書只給書名**
  取料手段依序為：(a) 指定查詢關鍵字；(b) 指定書名。
  書**不得附檔案**（版權），只給書名，且書名必須是 AI 查得到的。

- **Rule 4（MUST）Phase 2 產物是原料清單，不是解法**
  原料清單只列「要提取哪些元素／原料」與取料方式，不得預先寫出結論。

### 新 Rule 2：`實驗Prompt結構判準.md`

- **Rule 1（MUST）實驗 Prompt 必須含固定四步且順序不可調**
  找資料+發散收斂 → 可視化規劃+停等學員 review+學員下 `/clarify` → 改目標 Artifact → 呼叫 `/artifact-to-skill-engineering`（必要時再接 `/skill-engineering`）。

- **Rule 2（MUST）Artifact First：目標 Artifact 先於目標 Skill**
  Prompt 中「改目標 Artifact（`templates/*.example.md`）」必須排在「反推目標 Skill」之前，且必須是 Prompt 的明列步驟。

- **Rule 3（MUST）禁改範圍依主詞分兩層**
  - **實驗 Prompt（學員課堂執行時）**：不得改目標 skill 的 `SKILL.md`／`rules/`／SOP 流程，**亦不得指示 AI 改目標 skill 的複本／副本中的 `SKILL.md`／`rules/` 以規避本條**。**明確排除** `templates/*.example.md` —— 那是目標 Artifact，是 Artifact First 要動的對象。Prompt 可指示 AI 讀目標 skill 以理解上下文，但改行為規範一律由第四步的 `/artifact-to-skill-engineering`／`/skill-engineering` 承接。
    Bad Example 沿用現況 `實驗路徑分岔判準.md:68–72`（本次 DELETE，此為唯一承接人）：「請參照本 run 目錄內的 tdd-e2e-green，直接改 SKILL.md 與 rules…」——字面上沒碰到目標 skill，但繞過了整條 Artifact First 因果。
  - **本 skill 及其 sub-agent（執行者）**：不得修改目標 skill 的**任何**檔案，**含 `templates/*.example.md`**；**亦不得用「複製到暫定目錄直接改」假裝完成**。三跑止於「產出可視化規劃」，本來就不該碰到 example；代跑第三、四步等同代改。
    ⚠️ 反造假條款（暫定目錄複本）**必須掛在這一層**：歷史違規 `_prompt-consistency/tdd-e2e-green.run-A|B|C/` 15 檔正是執行者幹的，而暫定目錄裡的複本**不是**「目標 skill 的檔案」，光靠上一句的「任何檔案」字面擋不住。三跑仍會寫入暫定產物（見「三跑的邊界」一節），這條路徑依然通。

  兩層不可混寫成一條 —— 混寫會出現「執行者被授權改 example」的授權外溢，那正是舊版三跑改 skill 複本的同型錯誤。兩層的複本條款也**禁止物件不同、不可合併**：layer 1 鎖「複本中的 `SKILL.md`／`rules/`」（防 Prompt 繞過 Artifact First 因果），layer 2 鎖「暫定目錄複本的任何檔案」（防執行者代跑造假）；落地寫 rule 時須把這個差異點破。
  （承接自舊 `實驗路徑分岔判準` Rule 2，禁改範圍已依 example 界線與主詞重切）

- **Rule 4（MUST）第二步必須可視化且停等學員，`/clarify` 由學員手動下**
  Prompt 必須規定 AI 以條列、易讀的方式呈現規劃，並明寫「等學員 review 後，**由學員自行輸入 `/clarify`**」。
  `.agents/skills/clarify/SKILL.md` 為 `disable-model-invocation: true`，AI 不得自行叫起；Prompt 不可寫成「AI 呼叫 /clarify」。

- **Rule 5（MUST）術語鎖定**
  一律用「目標 Artifact」指涉被修改的 example、「目標 Skill」指涉其所屬 skill、「實驗 Prompt」指涉本 skill 產物，禁止互串。

### Templates

| 檔案 | 動作 | 要點 |
|---|---|---|
| `experiment-goals-and-scenarios.md` / `.example.md` | **DELETE** | 勾選卡片骨架整份作廢 |
| `sourcing-design.md` / `.example.md` | **NEW** | 範圍句／判型（機制型 or 內容型）／關鍵字／書名／要提取的原料清單 |
| `experiment-prompt.md` / `.example.md` | **NEW** | 實驗 Prompt 骨架，四步固定段落；取代舊 `prompt-writing-guide` |
| `prompt-writing-guide.md` / `.example.md` | **DELETE** | 撰寫規範內化為 `實驗Prompt結構判準.md` |
| `consistency-report.md` / `.example.md` | rewrite | 見下方逐行清單 |
| `skill-eng-validation.md` / `.example.md` | rewrite | `.md` 換欄位；`.example.md` **整份 36 行重寫**（現為 api-plan → OpenAPI 的 Artifact 路徑實例，非薄修可救） |

#### `consistency-report` rewrite 逐行清單

| 行 | 內容 | 處置 |
|---|---|---|
| `.md:3` | blockquote「本樣板**僅用於 Artifact 路徑**…Skill 路徑不要使用本樣板」 | 整句刪，改為「本樣板用於驗實驗 Prompt 執行穩定度，比對範圍止於內層『產出可視化規劃』」（此為**逐字落到 template** 的取代文字，不可寫「第二步」——那包含 sub-agent 做不到的停等與 `/clarify`） |
| `.example.md:3` | 同上但**只有前半句**（無「Skill 路徑不要使用」） | 同上 |
| `.md:6` / `.example.md:6` | `**實驗路徑**: Artifact` | 刪欄位（兩檔皆有） |
| `.md:7` | `**Prompt 規範版本／來源**: {{PROMPT_GUIDE_REF}}` | **懸空引用**（全 repo 唯一一處，指向被 DELETE 的 `prompt-writing-guide`）→ 改指 `experiment-prompt` 定稿版本 |
| `.example.md:7` | 同欄位的實例值「抽換 API Artifact → OpenAPI 規範草稿」 | 同上 |
| `.md:8` / `.example.md:8` | 欄位名 `來源 Artifact` | 改為 `目標 Artifact` |
| `.md:17` / `.example.md:17` | 三跑產物路徑 `{{RUN_A_PATH}}`… | 保留，但語意改為「三份可視化規劃」而非三份改過的 Artifact |
| `.md:27` / `.example.md:32` | `## 與來源 Artifact 對齊` | **不是改名就好** —— 三跑止於「產出可視化規劃」時根本還沒碰目標 Artifact，此節無比對對象。整節改為「與原料清單／範圍句對齊」或刪除；只改名會留下永遠填不了的欄位 |
| `.md:34` / `.example.md:40` | `建議定稿檔：{{RECOMMENDED_RUN}}` | **刪** —— 新模型的交付物是實驗 Prompt，不是某一跑的產物，「選哪一跑當定稿」在新邊界下無意義 |
| `.md:35` / `.example.md:41` | 「是否可進 Phase 5 驗證紀錄」 | 改為「是否可進 Phase 5 教材交付紀錄」 |
| `.md:39` / `.example.md:45` | 「請確認三跑品質是否可接受；未確認前不進入 Phase 5。」 | 同一改名批次：Phase 5 稱呼須與 `:35`／`:41` 一致，否則同檔內出現新舊兩種叫法 |

#### `skill-eng-validation` rewrite 欄位處置

| 行 | 既有欄位 | 處置 |
|---|---|---|
| `:4` | `實驗路徑` | 刪 |
| `:5` | `定稿 Artifact（僅 Artifact 路徑）` | 改為 `定稿實驗 Prompt` |
| `:6` | `目標 Skill` | 保留（術語已與新定名一致） |
| `:7–9` | `驗證入口`（含 `/artifact-to-skill-engineering`） | 保留 `/artifact-to-skill-engineering`，刪路徑分岔語意 |
| `:1` | 標題「Skill Engineering 驗證紀錄」 | 改為「教材交付紀錄」，與 Phase 5 新名稱一致 |
| `:12` | `## 驗證目標` | 改為「交付內容」 |
| `:16–21` | `## 設計約束（本次）`：不要過度工程／先從最簡單 SOP 開始／rules 按需疊代且必須掛回主 SOP | **刪** —— 這三條是 skill-engineering 的設計約束，在教材交付紀錄語意下屬殘留 |
| 新增 | — | 原料清單／三跑結論／**三跑覆蓋率邊界**（第三、四步未驗證）／其他已知債 |

## 檔案動作

### 新增

- `rules/取料來源判準.md`
- `rules/實驗Prompt結構判準.md`
- `templates/sourcing-design.md` + `.example.md`
- `templates/experiment-prompt.md` + `.example.md`

### 更新

- `SKILL.md` — description 重寫（去分岔語意、加取料先行）；Phase 1～5 全部重切
- `rules/人工Review閘門判準.md` — 全檔 rewrite
- `templates/consistency-report.md` + `.example.md`
- `templates/skill-eng-validation.md` + `.example.md`

### 刪除

- `rules/情境列舉與排序判準.md`
- `rules/實驗路徑分岔判準.md`
- `templates/experiment-goals-and-scenarios.md` + `.example.md`
- `templates/prompt-writing-guide.md` + `.example.md`
- `課程教材/客製化實驗/tdd-step-execution/_prompt-consistency/tdd-e2e-green.run-A|B|C/`（越界的 skill 複本殘留）

## 憲法

本次**不掛**。理由：憲法正要分檔並加 front matter 宣告「哪些 skills 遵照此憲法」，適用關係應在憲法端宣告，不在每支 skill 各補讀取行。待 core 憲法 front matter 就緒後，再明確把本 skill 列入或排除。

註：現況全目錄唯一的「憲法」字樣在 `rules/情境列舉與排序判準.md:115`，是把憲法當客製化槓桿的舉例名詞，該檔本次 DELETE，不影響此決策。

## 動手前置

`.agents/skills/design-experiment-scenario/` 與 `課程教材/客製化實驗/` 目前皆為 untracked（`??`），尚未進 git。本次要 DELETE **6 個 skill 檔**（2 rules + 4 templates），另加 `_prompt-consistency/` 殘留目錄（15 檔）。**動手前先 commit 一版當基準**，否則無法還原。

## 驗證方式

- `uv run .agents/skills/skill-engineering/scripts/analyze_skill_references.py --skill .agents/skills/design-experiment-scenario`
  （分析發現**不影響 exit code**，須人工判讀 `missingArtifactRefs`／`unreferencedArtifacts` 是否皆為空；改動前基線已實測為空。註：路徑給錯時腳本會 exit 2）
- **整個 skill 目錄** grep：不得出現 `實驗路徑`／`Artifact 路徑`／`Skill 路徑`／`選項字母`／`勾選`／`PROMPT_GUIDE_REF`／`來源 Artifact`／**`內層第二步`**（最後這條防停點粒度漂移：三跑止於「產出可視化規劃」，寫成「第二步」會把 sub-agent 做不到的停等與 `/clarify` 包進來）。範圍不可只掃 `SKILL.md`，殘留主要在 `rules/` 與 `templates/`
- 重讀新 rules：`Artifact First` 僅綁「目標 Artifact」，無一處綁到實驗 Prompt；`/clarify` 無一處寫成 AI 自行呼叫
- 反例驗證：以「加強系統分析顆粒度」跑 Phase 2，須被 `取料來源判準` Rule 1 判為內容型、Rule 2 要求取料，不得直接產出方法論解法
- 正例驗證：以「改 Green 推進節奏」跑 Phase 2，須被判為機制型且**不**要求外部取料（防 Rule 2 過度擴張）

## 下游波及（不在本 plan 動手範圍，但需排期）

骨架作廢、需重產的既有產物共 **6 份**：

| 檔案 | 作廢原因 |
|---|---|
| `architecture-constraint/experiment-goals-and-scenarios.md` | 骨架 DELETE |
| `tdd-flow-db-design/experiment-goals-and-scenarios.md` | 骨架 DELETE |
| `tdd-step-execution/experiment-goals-and-scenarios.md` | 骨架 DELETE |
| `tdd-flow-db-design/prompt-writing-guide.md` | 骨架 DELETE |
| `tdd-step-execution/prompt-writing-guide.md` | 骨架 DELETE |
| `tdd-step-execution/skill-eng-validation.md` | 骨架語意改寫 |

三份 `experiment-goals-and-scenarios.md` **各有 8 個選項卡片，合計 24 個情境**（不只 tdd-step-execution 那 8 個）。新結構沒有容納並列情境的骨架，重產時是「擇一收斂成單行範圍句」，不是換骨架搬運。

判型須逐一重審，**不預設全部機制型**：`tdd-step-execution` 的選項 D（Refactor 固定三步 checklist）與選項 E（Red 須 status＋body 雙斷言）表面帶有「這樣品質比較好」的宣稱，依 `取料來源判準` Rule 1 可能落在內容型。

進度校正：`architecture-constraint` 已有完整 8 卡 Phase 2 產物但**未勾選**；`tdd-flow-db-design` 已勾選 `C`；`tdd-step-execution` 已勾選 `A`。其餘題目尚未開始，改完 skill 後方可續作。

**時序相依**：`architecture-constraint` 整題以「專案憲法」為主槓桿（選項 A 直接呼叫 `/constitution`）。本 plan 決定「本 skill 不掛憲法」對本 skill 成立，但該題**重產**時會與憲法分檔／front matter 的排程直接相依 —— 憲法分檔未定案前不宜重產該題。

## 實作閘門

- 使用者已對齊：兩層模型、術語定名、三題決議（三跑保留／勾選拿掉／`clarify` 為 repo skill）
- **本版新增、待使用者確認的三項判斷**：
  1. 三跑只跑到內層「產出可視化規劃」為止（不含第二步結尾的停等學員 review 與 `/clarify`），比對三份可視化規劃
  2. 目標 Artifact ＝ 目標 skill 的 `templates/*.example.md`；禁改範圍**依主詞分兩層**——實驗 Prompt（學員執行時）禁 `SKILL.md`＋`rules/`，可改 example；本 skill 及其 sub-agent（執行者）禁目標 skill 全部檔案含 example，且不得用暫定目錄複本假裝完成
  3. 內層第四步恢復 `/artifact-to-skill-engineering`
- 使用者回「繼續」→ 依本 plan 呼叫 `/skill-engineering` 落地
