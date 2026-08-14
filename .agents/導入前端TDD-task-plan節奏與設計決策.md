# 導入前端 TDD：task-plan 節奏與設計決策

**寫作日期**：2026-08-14  
**對照來源**：水球版 Speckit（魔改 TDD＋前後端）  
路徑：`/Users/pinyi/Downloads/水球版的Speckit魔改TDD+前後端`  
**Gold package**：`specs/001-photo-albums/`  
**姊妹檔**：`.agents/導入前端TDD-目標與行動計畫.md`（目標、進度、下一刀證明圈）  
**作法**：Artifact-first。**task-plan gold 與執行鏈 skill 已對齊**（一則一區塊 RGB、觀測通道、整合 `US-n`）。下一刀是 001 前端 S-1-1 真跑一圈，不要倒推。

這份檔只回答一件事：**task-plan 的節奏要怎麼改，才能接到前端 TDD，又不會重演 002 實作時規格載入與資源爆炸。**

---

## 1. 目標（不變）

把這個專案導入**前端 TDD**。

做法是從水球版萃取值得要的設計，接到這包既有的「後端／前端／整合 + 領域 Gherkin」。不是整包換成水球骨架。

前端 TDD 要能做到：

- 一則測試只打一個畫面操作（public seam）
- 斷言看執行期畫面的正式入口（觀測通道），不是 Mock 呼叫次數、不是資料表、不是靜態雛形 HTML
- 假資料與畫面文案對齊 ui-plan／api-plan
- `/tdd-e2e-red` 寫前端測時不必再猜「打哪、看哪、先備什麼資料」
- Green 只讓**當前這一則**變綠，不准順便做本則不驗證的項目
- Refactor 只整理**當前這一則**剛綠的碼，不准擴到下一則

---

## 2. 這份決策從哪來

| 來源 | 內容 |
| --- | --- |
| 導入前端 TDD 主線 | 先改 ui-plan，再改 e2e（薄切片、觀測通道、US 驗收），再輪到 task-plan |
| 水球 `tasks.md`／`.agents/skills/tasks/` | 每則 Slice 固定 RED／GREEN／REFACTOR 三格；Green 寫死不得順便做下一則 |
| 這包 `task-plan` gold | **已改**：一則區塊 RGB；受測行為吃觀測通道；整合 `US-1`～`US-4` |
| 002 實作 scale | `002-meeting-room-booking` 後端 21 則、前端 20 則；一則一呼 `/tdd-e2e-red` 讓規格反覆載入、回合爆掉 |

相關對話：

- 導入前端 TDD（ui-plan → e2e → 行動計畫）：見當日主線
- 002 從規格到可跑、T1／T7／T11 紀錄：implement 實作那次（2026-07-30～07-31）
- 002 當日拍板：Red **進場**改成一個 US 一次；**內部**仍一次只寫一支測、跑到合格紅才下一支。當時 skill 根因報告寫了，但現行 `tdd-e2e-red` Rule 2 仍是「一次呼叫只處理一個 Scenario」——決策與程式尚未對齊。

---

## 3. 已經定案、這份不再重開

來自 ui-plan／e2e 那兩刀，task 必須遵守：

- 第一層仍是 **後端／前端／整合**。implement 與 TDD 吃 `layer`。不改成一份 `tasks.md`。
- 行為規格仍是 **領域 Gherkin**。不另加「預期行為」欄。
- 一則 Scenario = 一個 public seam。搬 Slice 的**切法**，不搬 Journey／Slice 雙型、不搬 `FX-*`、不搬 `spec.md →` 箭頭鏈。
- AC-1-1 拆成 S-1-1（建立）與 S-1-6（匯入）。
- 整合對準 spec 的 US 獨立驗證（`US-1`～`US-4`），不再抄 S-1-2、S-3-2。
- **受測部位**＝打哪；**觀測通道**＝從哪條正式介面看。畫面文案是要比的字。
- 「雛形不是受測物」只寫在 skill 規則，不進產物正文。
- 產物白話：前置資料用「尚未有任何相簿」，不用「空庫」。

---

## 4. 兩邊 task 差在哪

| 面向 | 這包 `task-plan` | 水球 `tasks` |
| --- | --- | --- |
| 檔案 | 三份：`task-backend`／`task-frontend`／`task-integration` | 一份 `tasks.md`（PHP 單體，畫面就是 HTTP View） |
| 切分來源 | `e2e-test-plan` 的 `## 後端`／`## 前端`／`## 整合` | `testplan.md` 的 Slice／Journey |
| 一格任務 | 改前：Green／Refactor 整個 US 一格。**改後 gold：每則區塊 RGB 三格** | **每個 Slice 固定 RED／GREEN／REFACTOR 三格** |
| 給執行者的資訊 | 巢狀「受測行為」「實作計畫」；Refactor 用「整理範圍」 | `Must Read`／`Optional`／`Why`，精確到檔案章節 |
| 環境 | `## 2. 環境建立` | Setup + Foundational；明文禁止偷做故事功能 |
| 驗收 | 改前掛 S-1-2、S-3-2。**改後 gold：US-1～US-4** | Journey 只出 `[ACCEPTANCE-GATE]`，不拆成薄紅燈 |
| 編號 | `/tdd-e2e-red` — `S-1-1` | `T005 [US1] [SLICE CALC-001] [TDD-RED]` |

這包強在：**層別清楚**，implement 可以「只做前端」。  
水球強在：**一則切片走完紅→綠→整理才進下一則**，Green／Refactor 都寫死範圍。

改前最痛：`task-frontend.md` 的 US-1 先開五則 Red（S-1-1 還把建立＋匯入綁在一起），再一格 Green 一次做建立、上傳、移動、415、禁巢狀。**gold 已改成一則 RGB**；`/tdd-e2e-green` 現行 skill 仍一次吃整個 US，那是第 5 步缺口。

---

## 5. 002 實作證明：規格載入會爆

002 當日壁鐘：`/implement` 後端→前端→整合約 1.5～2 小時才跑完；嚴格照 skill 字面會更長，因為根本跑不完。

最痛的 skill 問題：

| 編號 | 現象 | 影響 |
| --- | --- | --- |
| T1 | 一則 Scenario 一呼 `/tdd-e2e-red`；後端約 21 則 | 每一呼都是新進場：重讀憲法與 skill、重新定位 e2e 該則、再載入同一批 SA 片段、再跑該層全套。對話回合與 token 爆炸 |
| T7 | Red 碎、Green 一塊 | 教學與執行不對稱；Green 一次吃整包，just enough 名存實亡 |
| T11／T12 | 為了 scale，同回合批次寫測甚至直接 Green | 偏離 skill 字面；代表流程與真實壓力不合 |
| T4 | 多數 Red 卡在 login 404 就算合格紅 | 後面的主斷言沒跑到 |

當日拍板（尚未完全落到現行 skill）：

- 不要廢掉「一則 Scenario 一支測檔」
- Red **進場**不要一則新開一次讀規格的呼叫
- 合格紅必須碰到本則主斷言，卡在前置 404 不算完

002 當日把內圈收成「一個 US 先寫完所有測再 Green」，那只解 T1、不解 T7。**本檔覆寫內圈**：規格仍只讀一次，但寫測、做綠、整理按則交錯（見 D3／D8／D9）。

現行 `tdd-e2e-red` 契約**已經禁止** SA 整檔通讀（只讀該 Scenario 區塊與點名片段）。T1 不是「現在還會把 api-plan 從頭讀到尾」；是「每則仍新開呼叫，同一批片段被重新定位／載入，憲法與 skill 也每呼重讀」。後續改 skill 時不要把這兩件事寫成同一件事。

---

## 6. 比較之後，怎麼做比較好

水球的 cycle 是對的，但不能理解成「每一則再開三次會重讀規格的 Agent」。

要把兩個粒度拆開：

| | 產物粒度（測檔／區塊／just enough 碼） | 進場粒度（讀規格） |
| --- | --- | --- |
| 守住什麼 | 一則 Scenario 一支測、task 上一則一區塊、可追溯 | **implement 對一個 US 只讀一次規格** |
| 內部怎麼跑 | S-1-1 寫測 → 做綠 → 整理 → 才寫 S-1-6 | 不要每則、更不要每則 ×3 次新開對話去重新定位／載入同一批片段 |

協調者是 **`/implement` 這一輪 US**，不是每個 checkbox 新開一個 TDD Agent。T1 爆的是「每呼 tdd skill 都當新進場、重新定位並載入相同相關片段」；不是「一則 Scenario 只能有一個 checkbox」，也不是現行契約還在整檔通讀 api-plan。

三個候選，只採第三個：

1. **維持現況**：US 內先堆完所有 Red，再一次 Green。  
   否決。Green 會一次鋪整頁，不是前端 TDD；002 的 T7。

2. **照抄水球**：每則三個獨立任務，implement 每格各開一次讀規格的呼叫。  
   否決。T1 會比 002 更糟（回合數 ×3）。這包前端 US-1 拆完約 6 則，看起來不多，但每則新開呼叫、重新定位同一批片段一樣會炸。

3. **implement 當 US 協調者；內圈一則一圈 RGB（採納）**  
   - task：**一則一區塊**，區塊內三個 checkbox（Red、Green、Refactor），不是「一則只准一格」  
   - 受測行為吃 e2e 的觀測通道／前置資料／畫面文案／預期 TDD Red  
   - Green 的實作計畫對準**這一則**，寫死本則不驗證  
   - Refactor 對準**這一則**剛綠的碼；寫死不准擴到下一則（與 Green 的本則不驗證同一類約束）  
   - implement 進這個 US 時讀一次規格，然後依區塊順序走內圈：S-1-1 Red → Green → Refactor → S-1-6 Red → …  
   - 可仍呼叫 `/tdd-e2e-red`／`green`／`refactor`，但那是**同一輪 implement 裡的步驟**；子 skill 只吃該則已定位的片段，不得再當新進場去重新定位 e2e 或重載同一批 SA 片段

Canon TDD／Uncle Bob 第三法要的是「一次只過當前這一支」，那是**內圈**。規格載入成本由 **implement 的 US 進場**付一次。

---

## 7. 設計決策

### D1. 不換成水球的 `tasks.md`

這包是 Vite 前端 + API 後端，implement 吃 `layer`。水球的 HTTP slice 本身就是畫面。三檔保留。

### D2. 不搬 Slice／Journey 標題、T001、Must Read 箭頭鏈、Why

e2e 已否決雙型、`FX-*`、`檔案 → 章節`。索引在 e2e 對應欄位。Why 會跟 Gherkin、預期 TDD Red、本則不驗證重複。

### D3. 產物：一則 Scenario 一個區塊；區塊內 Red → Green → Refactor

「一則一格」容易被理解成「一則只准一個 checkbox」。正確說法是**一則一區塊**：

- 區塊標題用 Scenario ID（S-1-1）
- 區塊內三個 checkbox：先 Red、立刻 Green、立刻 Refactor
- 不要先列完該 US 所有 Red，再一個「讓本 US 既有 Red 全綠」
- 不要把 Refactor 收到 US 末尾一格

US 底下順序：

```text
### US-1
#### S-1-1
  Red checkbox
  Green checkbox      ← 只做建立「旅行」；不接上傳
  Refactor checkbox   ← 只整理這一則剛綠的碼
#### S-1-6
  Red checkbox
  Green checkbox      ← 只做平鋪匯入
  Refactor checkbox
…
```

進度總覽列 Scenario，不要只列 US。每則都有 Red／Green／Refactor 欄。

Gold 已是這個長相。收 skill 時：同一 US 內改成「每則一個區塊，區塊內 Red 緊接 Green 緊接 Refactor」。刪掉 US 級驗紅項與 US 末尾單一 Refactor。

### D4. 受測行為從 e2e 推，仍不寫測試手段

每則 Red 寫：

| 寫什麼 | 從哪來 |
| --- | --- |
| 要驗證什麼 | Gherkin Then |
| 打哪 | 受測部位 |
| 先備什麼 | 前置資料（白話） |
| 從哪裡看 | 觀測通道 |
| 要比哪句字 | ui-plan 畫面文案 |
| 還沒做會長怎樣 | 預期 TDD Red |

不寫 Playwright、selector、Mock 框架名。不寫可執行產品程式碼。

### D5. Green 寫「本則不准順便做」

不必新欄位。把 e2e 的 **本則不驗證** 寫進該則實作計畫。例如 S-1-1 Green：主頁建立表單 → `POST /albums` → 畫面出現「旅行」；不接批次匯入、日期分組、拖放。

### D6. 環境建立不准偷故事功能

§2 只建 Vite／測試入口／Mock 對齊 api-plan 形狀。不可在環境章節做出「旅行」或平鋪。`system-analyze/ui/*.html` 不是測試入口。

### D7. 整合改掛 US-1～US-4 驗收

不是薄切片的再一輪 Red。不要預期 TDD Red。對準 spec 獨立驗證。邊界（HEIC、只有一本不能拖、禁止巢狀）留在切片。

task-integration 的區塊 ID 用 `US-n`（與 e2e `## 整合` 一致），不是 `S-x-y`。現行 task-plan 規則若寫死 Red ID 必須 `S-n-m`，收 skill 時要開整合例外；`tdd-e2e-red`／implement 也要能吃 `US-n`。每一則 US 驗收仍是一區塊（Red 寫測 + Green 修接線 + Refactor 整理接線），不是六則薄切片再抄一遍。

### D8. implement 對一個 US 讀一次規格；內圈按區塊走完紅→綠→整理

這是 002 的 T1 解法，用來同時保住 D3 的交錯，而不是「Red 一次寫完全 US 所有測」。

執行模型：

1. implement 進入該 US：讀 e2e 該層該 US、ui-plan／api-plan 相關片段、task 本 US 區塊。**這是唯一一次定位與載入。**
2. 依 task 區塊順序：
   - 跑 S-1-1 Red（只寫該則測、跑到合格紅；斷言只走觀測通道；禁止測雛形 HTML）
   - 立刻跑 S-1-1 Green（只讓該則觀測通道變綠；遵守本則不驗證）
   - 立刻跑 S-1-1 Refactor（只整理這一則剛綠的碼；不准擴到下一則）
   - 再跑 S-1-6 Red → Green → Refactor
3. 沒有 US 末尾再一格 Refactor。

`/tdd-e2e-red`、`/tdd-e2e-green` 與 `/tdd-e2e-refactor` 仍可當步驟存在，但契約改成：

- 由**已在場的 implement** 帶入「這一則」的已定位片段（Gherkin、受測部位、前置資料、觀測通道、畫面文案、本則不驗證）
- **禁止**子呼叫再去 e2e／api-plan／ui-plan **重新定位或重載同一批片段**（現行契約已禁 SA 整檔通讀；還不夠，連「合法的點名重載」也不要每則再做一次）
- Green **禁止**以「一次實作讓本 US 多支變綠」當策略；附帶變綠可回報
- Refactor **禁止**夾帶下一則行為；整理後仍綠
- 現行 Rule「Red 一次只處理一個 Scenario」對**內圈一則**仍成立；要廢的是「每一則／每一步 = 一次新的規格進場」

若做不到「子 skill 不重新定位／重載片段」，就不要為每個 checkbox 開新 Agent：implement 在同一輪親自依 red／green／refactor 規則執行內圈。寧可少開 Agent，也不要為了 SOP 外形再炸 T1。

### D9. Refactor 跟 Scenario 同粒度，不跟 US 同粒度

覆寫先前「每 US 一次」。經典 TDD 與水球都是一個 Slice／一則測走完 RGB。

- 產物：每則區塊第三個 checkbox，巢狀「整理範圍」
- 範圍：只動這一則剛綠的碼（命名、去重、小幅抽取）；不准擴到本則不驗證／下一則
- 進場：仍由同一輪 implement 做完，**不是**每則再開一個會重讀規格的 Agent

US 一次會讓 S-1-1 的髒變成 S-1-6 的地基，末尾那格還容易膨脹成整頁重構。那不是 TDD 的 Refactor。

---

## 8. 目標樣貌（前端 US-1 最薄一則）

觀測通道跟 e2e 金標對齊：執行期主頁上看不看得到「旅行」。建立成功後畫面可能停在主頁或進詳情，**斷言入口仍是執行期主頁是否出現「旅行」**；詳情標題只是可能的伴隨結果，不是第二條要自己猜的通道。

```markdown
#### S-1-1 建立名為「旅行」的相簿

- [ ] `/tdd-e2e-red` — S-1-1 建立名為「旅行」的相簿:
  - 受測行為：
    - 前置：尚未有任何相簿
    - 打：主頁建立相簿表單
    - 看：執行期主頁（不是 `ui/index.html`）
    - 期望：主頁看得到「旅行」
    - 還沒做時：送出後仍顯示還沒有相簿，或看不到「旅行」
- [ ] `/tdd-e2e-green` — S-1-1:
  - 實作計畫：
    - 主頁建立表單 → `POST /albums` → 主頁出現「旅行」
    - 本則不驗證：批次匯入、日期分組、拖放
- [ ] `/tdd-e2e-refactor` — S-1-1:
  - 整理範圍：
    - 在綠燈下整理剛寫的建立表單／`POST /albums` 命名與去重
    - 不准擴到批次匯入、日期分組、拖放
```

然後才輪到 S-1-6（觀測通道＝平鋪區）。

前端 US-1 應對齊 e2e `## 前端`：S-1-1、S-1-6、S-1-2、S-1-3、S-1-4、S-1-5。不可再把 S-1-1 寫成建立＋匯入。

---

## 9. 刻意不搬

- 單一 `tasks.md`、`T001`、`[US#] [SLICE …]`、`[ACCEPTANCE-GATE]` 這個名字
- 每格 Must Read／Optional／Why，以及 `檔案 → 章節`
- `FX-*`、Foundational 偷塞業務
- Global NFR phase、Parallel Execution、MVP First（implement 已規定跟文件順序走）
- 把 TDD 家規（3A、Mock 邊界）寫進 task；那些屬 `tdd-e2e-red`／`green`
- 把 `ui/*.html` 當實作答案或測試入口

---

## 10. 現況：gold 與執行鏈 skill 已對齊

| 檔 | 狀態 |
| --- | --- |
| `task-plan` 規則／example／validator | 已對齊：一則一區塊 RGB；整合 `US-n`；001 validator OK |
| `tdd-e2e-red` | 已對齊：一次一則（含 `US-n`）；已定位片段不重載；走觀測通道；禁測雛形；合格紅碰主斷言 |
| `tdd-e2e-green` | 已對齊：一次一則；禁止以多支同綠當策略；遵守本則不驗證 |
| `tdd-e2e-refactor` | 已對齊：緊接該則 Green；只吃整理範圍 |
| `implement` | 已對齊：一個 US 只定位一次；同一輪按則 RGB；傳本則不傳整個 US |

Gold 路徑（對齊樣本，不要改回舊節奏）：

- `specs/001-photo-albums/task-plan/task-frontend.md`
- `specs/001-photo-albums/task-plan/task-backend.md`
- `specs/001-photo-albums/task-plan/task-integration.md`

---

## 11. 刀序與進度（不要並行一次全改）

11.1、11.2 已落地。剩下 11.3 證明圈。旁路（e2e example、analyze-report）另開。

### 11.1 `task-plan` skill（第一刀，已完成）

對齊 gold，不要發明第四種節奏。

| 檔 | 改什麼 |
| --- | --- |
| `SKILL.md` | description／SOP：一則一區塊 RGB；刪「每個 US 的 Red 末尾含固定驗紅項」 |
| `rules/產物結構與章節判準.md` | Rule 2／3／4：US 下是 `#### AC / Edge` 再 `#### S-n-m`（整合 `#### US-n`）；區塊內 Red→Green→Refactor；Refactor 巢狀「整理範圍」；刪 US 級驗紅項 |
| `rules/實作意圖撰寫判準.md` | Red 受測行為含前置／打／看／期望／還沒做時（前端加文案）；Green 寫本則不驗證；環境不准偷做故事功能；整合 ID 例外 `US-n` |
| `templates/` 與三份 `.example.md` | 骨架與完成態跟 001 gold 同形 |
| `scripts/validate_task_plan_output.py` | 驗：每則都有 R／G／Rf、無 US 級 `#### Red` 與驗紅項、前端／後端 ID=`S-n-m` 對齊 e2e、整合 ID=`US-n` 對齊 e2e `## 整合` |

通過條件：對 `specs/001-photo-albums` 跑 validator 要 OK。

### 11.2 TDD skill + `implement`（第二刀，已完成）

這是 D8。只改 TDD、不改 implement，checkbox 仍會每格新進場。

**`tdd-e2e-red`**

- 內圈一次仍只一則（含整合 `US-n`）
- 必讀並只走觀測通道；禁止測 `system-analyze/ui/*.html`
- 由已在場 implement 帶入已定位片段；禁止當新進場重載同一批 e2e／SA 片段
- 合格紅必須碰到本則主斷言

**`tdd-e2e-green`**

- 一次一則 Scenario（或整合一則 `US-n`），不是一個 US
- 只綠當前這則；禁止以「一次實作讓本 US 多支變綠」當策略；附帶變綠可回報
- 遵守該格「本則不驗證」

**`tdd-e2e-refactor`**

- 一次一則，緊接該則 Green，不是「本 US 全綠後」
- 只吃「整理範圍」；不准擴到本則不驗證／下一則
- 整理後仍綠

**`implement`**

- 進一個 US：讀一次該層該 US 的 e2e／相關 SA／task 區塊（唯一一次定位）
- 內圈按 checkbox：S-1-1 Red → Green → Refactor → S-1-6 …
- 委派時帶**這一則**已定位片段，Green／Refactor 傳 Scenario（整合傳 `US-n`），不傳整個 US
- 若子 skill 做不到「不重載片段」：同一輪親自跑內圈，不為每個 checkbox 新開 Agent

### 11.3 證明（第三刀，下一刀）

001 前端 S-1-1：執行期主頁看不到「旅行」為合格紅 → Green 主頁出現「旅行」→ 這一則 Refactor → 才寫 S-1-6。這步成功才算前端 TDD 鏈可執行。

旁路（不擋 11.3）：e2e-test-plan 的 example 若仍舊切片，下次 `/e2e-test-plan` 可能寫回舊樣；analyze-report 若仍把 S-1-1 寫進整合會過期。另開，不要跟證明圈混成一包。

---

## 12. 一句話

**內圈**學水球：一則一圈 RGB，Green／Refactor 都不准順便做下一則。  
**外圈**守 002 的教訓：implement 對一個 US 只定位／載入一次規格，不要每個 checkbox 新開 Agent 去重新定位並重載同一批片段。
