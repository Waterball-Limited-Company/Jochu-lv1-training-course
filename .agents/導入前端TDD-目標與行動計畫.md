# 導入前端 TDD：目標、現況與行動計畫

**對照來源**：水球版 Speckit（魔改 TDD＋前後端）  
路徑：`/Users/pinyi/Downloads/水球版的Speckit魔改TDD+前後端`  
**Gold package**：`specs/001-photo-albums/`  
**姊妹檔**：`.agents/導入前端TDD-task-plan節奏與設計決策.md`（task-plan 節奏、D1–D9、下一刀 skill）  
**作法**：Artifact-first。ui-plan／e2e／task-plan gold 已落地。**task-plan skill 與 implement／TDD skill 已對齊 gold**。下一刀是 001 前端 S-1-1 真跑一圈 RGB。

---

## 目標

把這個專案導入**前端 TDD**。

做法是參照水球版 Speckit 魔改 TDD＋前後端，把值得要的設計萃取出來，接到這包既有的流程上。不是把這包整份換成水球骨架。

前端 TDD 要能做到：

- 一則測試只打一個畫面操作（public seam）
- 斷言看執行期畫面的正式入口（觀測通道），不是 Mock 呼叫次數、不是資料表、不是靜態雛形 HTML
- 假資料與畫面文案對齊 ui-plan／api-plan
- `/tdd-e2e-red` 寫前端測時不必再猜「打哪、看哪、先備什麼資料」
- Green 只讓當前這一則變綠；Refactor 只整理這一則剛綠的碼。兩者都不准順便做下一則

---

## 這包要留的（不要換成水球）

- 第一層仍是 **後端／前端／整合**。implement 與 TDD 吃 `layer`。
- 行為規格仍是 **領域 Gherkin**。不要用水球欄位取代 Gherkin。
- 憲法：Vite + Vanilla；前端不直連 DB。
- ui-plan 路徑維持 `specs/<NNN>/system-analyze/ui-plan.md`，並可點雛形在 `system-analyze/ui/`。
- 同一 AC 可在後端與前端各證一次。整合不再抄同一則薄 Scenario。

---

## 從水球萃取、已經接到這包的

### ui-plan（已落地 gold 與 skill）

- 雙層產出：`ui-plan.md` 加上可點的 `ui/*.html`
- 視覺方向、頁面編排、狀態表（狀態 ID、觸發時間、畫面文案）
- 畫面文案是前端 TDD Then 要比的字
- 雛形像產品；`index.html` 是主頁不是 sitemap
- 假資料對齊 api-plan（旅行／家庭／工作與日期分組）
- 保留 Mermaid 與 API 對應表（前端 Mock 的命脈）

不抄：用水球條列取代 Mermaid、放棄 API 對應、把雛形當受測物。

### e2e-test-plan（gold 已改；skill 規則已跟上，example 尚未同步）

後端／前端是薄切片（一則一個意圖、一個 seam）：

- Gherkin 講預期行為（不另加「預期行為」欄）
- **受測部位**：Act 打哪
- **前置資料**：白話 Arrange（資料庫尚無任何相簿、已有空的「旅行」）。不另開 FX 總表，不用「空庫」
- **觀測通道**：Assert 從哪條正式介面看
- **必須維持不變**、**本則不驗證**、**預期 TDD Red**
- US／AC／FR 寫編號加短標題，不用 `spec.md →` 箭頭鏈
- AC-1-1 拆成 S-1-1（建立）與 S-1-6（匯入）

整合是 User Story 驗收，對準 spec 的獨立驗證方式：

- 編號 `US-1`～`US-4`，真串接
- 要 Gherkin（When 可寫完整路徑，仍只一條 When）
- 不要預期 TDD Red
- 邊界（HEIC、只有一本不能拖、禁止巢狀）留在切片，不進整合

雛形不是受測物：寫在 skill 規則，不寫進產物正文。

刻意不搬：Journey／Slice 雙型當一等公民、Act 輸入／預期輸出／唯一測試意圖（與 Gherkin 重複）、FX-\* 代號。

### task-plan（gold 與 skill 都已對齊）

節奏契約見姊妹檔 D1–D9。gold 與 skill 都已是：

- 一則 Scenario 一個區塊；區塊內 Red → Green → Refactor
- 受測行為吃前置／打哪／觀測通道／期望／還沒做時
- Green 寫本則不驗證；Refactor 寫整理範圍（不准擴到下一則）
- 前端 US-1：S-1-1 只建立「旅行」，S-1-6 才匯入
- 整合掛 `US-1`～`US-4`，不抄 S-1-2、S-3-2
- 環境不准偷做「旅行」或平鋪；測試入口不是 `ui/*.html`

---

## 觀測通道（前端 TDD 的關鍵）

不是「只為前端發明」，但前端特別需要。

| 欄 | 意思 |
| --- | --- |
| 受測部位 | 打哪裡 |
| 觀測通道 | 從哪裡看結果 |

前端看執行期畫面哪一區。後端看 API 回應或再 GET。整合兩邊都看。

禁止：查資料表、數 Mock、打開 `system-analyze/ui/*.html`。

畫面文案（ui-plan）是要比的字；觀測通道是去哪一區看這句字。兩件事都要。

---

## 還沒接到目標的缺口

1. **task-plan skill**、**implement**、**tdd-e2e-red／green／refactor**：已對齊（姊妹檔 §11.1、§11.2）。
2. **e2e-test-plan example** 若仍舊切片，下次跑 skill 可能寫回舊樣（旁路）。
3. **analyze-report** 等下游若仍把薄切片寫進整合，會過期（旁路）。
4. 還沒用 001 **真的跑一輪前端 S-1-1 RGB**，證明鏈可執行。這是下一刀。

---

## 行動計畫

原則：gold 已齊，不要倒推。執行鏈 skill 已收完。不要並行一次改完旁路。

### 已完成

- 第 0 步：e2e gold 凍結（薄切片、觀測通道、US 驗收）
- 第 2 步：task-plan gold（一則 RGB、觀測通道、整合 `US-n`）
- 第 3 步：`task-plan` skill（規則、example、validator；001 validator OK）
- 第 4 步：`implement` + `tdd-e2e-red`／`green`／`refactor`（D8：一則一圈、同一輪、已定位片段、主斷言／觀測通道）

### 下一刀（與姊妹檔 §11.3 同一條）

用 001 前端 S-1-1 跑通：執行期主頁看不到「旅行」→ Green 主頁出現「旅行」→ 這一則 Refactor → 才寫 S-1-6。

S-1-1 的觀測通道是**執行期主頁**，不是詳情標題、不是 `ui/index.html`。

旁路另開：e2e example、analyze-report。

---

## 建議執行順序（下一刀起）

1. 跑 S-1-1 前端 RGB（證明鏈可執行）

不要並行大改。前端 TDD 的最短路徑剩下：真的紅燈。

---

## 對照檔案

- Gold ui-plan：`specs/001-photo-albums/system-analyze/ui-plan.md`  
  雛形：`specs/001-photo-albums/system-analyze/ui/`
- Gold e2e：`specs/001-photo-albums/e2e-test-plan.md`
- Gold task-plan：`specs/001-photo-albums/task-plan/task-frontend.md`、`task-backend.md`、`task-integration.md`
- 節奏決策：`.agents/導入前端TDD-task-plan節奏與設計決策.md`
- 水球 testplan skill：該專案 `.agents/skills/testplan/`（觀測通道、薄切片、Journey 不當單輪紅燈）
- 水球 overtime 產物：該專案 `specs/001-overtime-payroll/testplan.md`
