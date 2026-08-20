# 前端 TDD 與分層驗證流程設計

狀態：已實作；交付閘門結果以本輪最終回報為準
建立日期：2026-08-20
適用範圍：州巧 Speckit 從系統分析、端對端測試計畫、實作計畫到實作與驗證的流程

## 1. 設計目標

1. 前端與後端都以 Scenario 為最小 TDD 粒度，各自在自己的執行邊界完成端對端驗證。
2. 一個 Scenario 由同一個代理、同一份 context 跑完 Red → Green → Refactor，不在三個階段間重開代理。
3. 每個 Scenario 完成後，以該層 User Story 的累積測試確認局部修改沒有破壞先前行為。
4. 前後端各自完成後，再以 User Story 為單位執行真前端、真後端與真資料的完全端對端驗收。
5. 前端測試套件在系統分析階段確定，後續測試計畫與實作計畫只能消費同一項決策，不可各自發明工具。
6. `api-plan.md` 是前端 Mock、後端 API 與完全端對端整合共同遵守的契約，不是只供閱讀的參考文件。

## 2. 不採用的設計

- 不建立 `TDD Slice`、`Acceptance Journey` 或 `Environment Gate` 等新的正式案例類型。
- 不把 Red、Green、Refactor 拆給三個不同代理。
- 不把整個 User Story 當成一輪 Red → Green → Refactor。
- 不在 User Story 全綠閘門內直接實作修正。
- 不在前端自行發明一份與 `api-plan.md` 不同的 Mock response。
- 不把靜態 UI 雛形當成執行期前端測試入口。
- 不修改既有 `specs/001-photo-albums/` 示範產物。

## 3. 名詞與責任邊界

### 3.1 User Story、AC 與 Scenario

- User Story 定義一段可獨立交付與驗收的使用者價值。
- AC 與 Edge 定義該 User Story 必須成立的條件與邊界。
- Scenario 把一條 AC 或 Edge 轉成可執行的具體例子，是前端與後端各層 TDD 的最小工作單位。

### 3.2 Public seam

Public seam 只是測試進入系統與觀測結果的技術位置，不是新的需求或案例類型。

目前 `e2e-test-plan.md` 已透過「打、看、期望、觀測通道、API、UI」表達這件事，因此不新增 `public seam` artifact 或分類欄位。需要的只是確保每則 Scenario 都能回答：

- 從哪個公開入口操作。
- 從哪個公開結果判定成功。
- 預期紅燈應在哪個主斷言發生。

### 3.3 三種端對端範圍

| 驗證層級 | 執行邊界 | 主要替身 | 證明內容 |
|---|---|---|---|
| 後端 Scenario 端對端 | 公開 API → 後端應用 → 測試資料庫／檔案 | 只替換不可控外部服務 | 後端對外行為、資料與契約成立 |
| 前端 Scenario 端對端 | 真瀏覽器 → 執行期前端 → API 邊界 | API 依 `api-plan.md` Mock | 前端畫面、狀態與互動成立 |
| User Story 完全端對端 | 真瀏覽器 → 真前端 → 真 API → 真後端 → 真資料 | 不使用前後端之間的 Mock | 完整使用者價值與接線成立 |

## 4. 整體產物流程

```text
specify
→ spec.md
→ system-analyze / technical-research
   → 若前端測試套件尚未確定，先 clarify
   → technical-research.md / plan.md 記錄採用結果
   → data-plan.md / DDL.md / api-plan.md / ui-plan.md
→ e2e-test-plan
   → 後端 Scenario
   → 前端 Scenario
   → User Story 完全端對端驗收路徑
→ task-plan
   → task-backend.md
   → task-frontend.md
   → task-integration.md
→ analyze
→ implement
   → Scenario RGB
   → User Story 層內全綠閘門
   → User Story 完全端對端驗收
```

## 5. 前端測試套件決策

### 5.1 決策時機

前端測試套件屬於技術堆疊決策，必須在 `system-analyze` 的 technical research／plan 階段確定，不能延後到 `task-plan` 或第一次 Red 才臨時選擇。

執行順序：

1. 先讀既有 `package.json`、測試設定與現有測試，判斷專案是否已有可用套件。
2. 已有單一且能覆蓋需求的套件時，沿用並寫入 `technical-research.md` 與 `plan.md`，不重複詢問。
3. 新建專案尚未選定、既有套件無法覆蓋本期關鍵互動，或同時存在多套可行框架而沒有明確主框架時，呼叫 `clarify` 請使用者選擇。
4. 使用者未指定偏好時，Web 專案的瀏覽器端對端測試推薦預設為 Playwright。

### 5.2 推薦預設

Playwright 是州巧這類 Web 前端的推薦預設，因為需要驗證：

- 執行期頁面與真實 DOM。
- 檔案選擇與多檔上傳。
- 拖放互動。
- 非同步畫面更新。
- 頁面重新整理後的狀態。
- API 攔截與依契約建立 Mock。
- 失敗時的 trace、截圖與瀏覽器紀錄。

Vitest、Jest 或 Testing Library 可以作為純函式、元件或狀態邏輯的輔助測試，但不能取代本流程要求的前端 Scenario 瀏覽器端對端證據。

Playwright 不是所有專案的無條件預設：伺服器端渲染且沒有瀏覽器互動或非 Web 前端時，依實際執行環境選擇；既有團隊已有單一成熟且足以覆蓋本期互動的套件時，直接保留原技術棧，不呼叫 `clarify`。只有 5.1 所列的新專案未選定、既有能力不足，或多套可行框架沒有明確主框架時，才由 `clarify` 收斂。

### 5.3 Clarify 問題原則

只有當選擇會改變測試入口、task setup、Mock 能力或實作成本時才提問。問題至少要說明：

1. 專案目前的前端測試套件狀態，以及為什麼不能直接沿用一套已足夠的主套件。
2. 本期需要驗證哪些真實互動。
3. 推薦 Playwright 的原因與主要代價。
4. 使用者可以選擇 Playwright、沿用指定既有套件，或明確指定其他套件。

## 6. API 契約的單一來源

`api-plan.md` 同時約束：

- 後端 Scenario 的 endpoint、method、request、status 與 response。
- 前端 Scenario 的 Mock request match 與 response fixture。
- `task-backend.md` 與 `task-frontend.md` 的實作步驟。
- `analyze` 的實作前契約一致性檢查。
- `/implement` 的實作後契約驗證閘門。
- `task-integration.md` 的真串接驗收。

必須遵守：

1. 前端 Mock 不得自行新增、改名或省略契約欄位。
2. 後端實作不得另回傳一套未寫入 `api-plan.md` 的形狀。
3. `e2e-test-plan` 與 `task-plan` 只引用同一份 endpoint 與資料形狀，不複製後再自由改寫。
4. `api-plan` 樣板必須以固定欄位保存 method、path、status、request 與 response，讓契約可被機械比對，不只供人工閱讀。
5. `api-plan.md` 先於 Scenario 產生，因此只保存穩定的契約案例 ID、User Story 與必要證據來源，不預猜 Scenario ID；後產生的 `e2e-test-plan.md` 與三份 `task-plan` 必須以契約案例 ID 反向引用。
6. `e2e-test-plan.md` 的前端 Scenario 必須明列 API 使用狀態；不碰 API 時，API 與 API 契約案例都固定寫「不適用」，只要碰 API 就至少引用一個契約案例。後端與整合 Scenario 一律引用至少一個契約案例。
7. 實作前的 `analyze` 檢查 `api-plan.md` 的固定欄位是否完整、每項必要證據來源是否同時落到對應的 `e2e-test-plan` 分層與 task，以及所有引用的契約案例是否存在；契約引用按「外層 User Story ＋ Scenario」逐則比對，不能以同故事其他 Scenario 的引用頂替。此時不得宣稱已驗證尚未產生的實作。
8. 實作後由 `/implement` 呼叫同一個契約 validator。固定輸入為 `api-plan.md` 的結構化契約、前端 Mock 的攔截條件與 response fixture、後端契約測試的 request、預期 response 與執行時實際 response，以及整合測試擷取的 request／response 證據。
9. `/implement` 必須在受影響 Scenario 完成前檢查該 endpoint，在 User Story 層內全綠閘門檢查該故事全部 endpoints，並在完全端對端驗收完成時比對實際擷取的契約證據。任何 method、path、status、request 或 response 不一致，都禁止把 Scenario、User Story 或整合任務標成完成。
10. 暫時無法機械解析的契約部分才補人工檢查；validator 必須列出未覆蓋欄位，未覆蓋到驗收主斷言所需欄位時視為阻擋，不得用人工確認直接略過。
11. 完全端對端驗收開始前，必須確認前端 API Mock 已停用。
12. Scenario 契約閘門以本則契約 ID 限縮；User Story 完成閘門與整合驗收以故事選取全部契約，不得帶 Scenario 或單一契約篩選而漏驗。
13. 新產生的 `technical-research.md` 與 `plan.md` 必須以 `--require-v2` 驗證；只要 package 存在可機械驗證契約，也視為流程版本 2。上述兩份產物、`api-plan.md`、`e2e-test-plan.md` 或任一 task 刪掉版本標記都必須失敗，不能退回舊驗證路徑；既有流程版本 1 產物則以未帶 `--require-v2` 的相容模式驗證。
14. task 內的累積測試、故事測試、全層回歸、資料重設與整合執行必須是非空白、可解析且能辨認用途的執行器命令；資料重設不能用一般 `npm test` 冒充，`echo`、`true`、相似檔名或假路徑驗證器、命令串接與吞錯寫法都視為失敗。
15. 契約證據須以 `source` 欄位宣告層別，記錄可辨認的測試執行器命令與實際有效且具時區的產生時間；不強迫合法的 `npm test` 或 `python3 -m pytest` 在命令名稱重複層別。後端／前端證據使用 `S-n-m`，整合證據的 Scenario ID 固定等於契約的 `US-n`。
16. 人工可讀的每個 Responses 案例與測試規劃資料列都必須明列一個契約案例 ID，並與可機械驗證契約雙向覆蓋；Responses 下的實際 JSON 範例也必須通過同案例 response Schema，不能只對 ID 與 status。
17. request／response Schema 不接受空物件 `{}`；無 body 固定使用 `{"type":"null"}`，避免用空 Schema 關閉實際驗證。
18. 命令檢查必須展開 `npx`、`pnpm`、`yarn`、`bun`、`uv run` 等包裝器後辨認真正執行器；包在合法啟動器裡的 `echo`、`true`、`printf` 或假 Python 執行檔仍須失敗。
19. 整合固定欄位宣告 Mock 停用後，其他敘述不得再保留、使用或重新啟用 Mock；矛盾文字本身就是阻擋。

## 7. Scenario 代理與完整 TDD 循環

### 7.1 代理生命週期

`/implement` 是外層編排者；每個前端或後端 Scenario 只建立一個 Scenario Agent。該代理必須持有本則完整 context，連續跑完 Red → Green → Refactor，不能在三個階段間換代理或重新把整個 User Story 當成新進場。

同一層、同一 User Story 內的 Scenario 預設依 task 順序序列執行，不平行修改共享程式碼。

### 7.2 Scenario Agent 輸入

- layer。
- plan-package。
- User Story ID 與名稱。
- Scenario ID、標題與 AC／Edge 來源。
- 本則受測行為、觀測通道與主斷言。
- 本則 Green 實作邊界與不驗證範圍。
- 本則 Refactor 允許範圍。
- 已選定測試套件與執行命令。
- 本 User Story 已完成 Scenario 測試集合。
- 需要的 `api-plan.md`、`ui-plan.md`、data plan 與既有程式碼片段。

### 7.3 Red

Red 前先執行環境預檢，確認測試入口可啟動、既有 User Story 測試為綠、必要 fixture 可建立。環境預檢不是正式案例類型。

合格 Red 必須：

- 新測試可執行。
- 失敗到達本則預定的公開觀測通道與主斷言。
- 失敗原因是尚未實作的行為，不是建置、連線、selector、fixture 或測試語法錯誤。
- 沒有先寫產品行為讓測試通過。

若測試在新增時已經通過，不製造假紅燈。先確認斷言完整，再以暫時破壞相關行為且完成後還原的敏感度檢查，證明測試真的能抓到錯誤；結果記錄為「既有綠燈且敏感度已驗證」。

### 7.4 Green

Green 只實作讓本則主測試通過所需的最少行為：

- 不預作下一個 Scenario。
- 不以修改或放寬測試掩蓋缺陷。
- 不在前端容忍與 `api-plan.md` 不一致的第二套 response。
- 允許新增必要的輔助測試，但本則完成證據仍以 Scenario 端對端測試為準。

### 7.5 Refactor

Refactor 只能在本則已綠後進行，且不得新增需求：

- 可整理本則新增或實際碰到的程式碼、測試與共用結構。
- 若整理共享程式碼，必須跑本 User Story 已完成 Scenario 的累積測試。
- 若需要新的行為、跨多個尚未完成 Scenario 的設計或改變 API 契約，停止 Refactor，回到對應 Scenario 或上游 artifact。

### 7.6 Scenario Agent 輸出

- 測試檔案與主斷言。
- Red 指令、失敗位置與合格紅燈證據。
- Green 指令與通過證據。
- Refactor 改動範圍與維持綠燈證據。
- User Story 層內全綠閘門結果。
- 修改檔案清單。
- 未完成、阻塞或意外既有綠燈狀態。

只有輸出齊備且閘門通過，`/implement` 才能勾選本則完成進度。

## 8. User Story 層內全綠閘門

這個閘門的目的，是確認目前 Scenario 的局部實作沒有破壞同層、同一 User Story 已經完成的行為。它不是第二輪 User Story TDD，也不直接負責寫程式。

### 8.1 執行時機

1. Scenario 開始前，先跑目前已完成的 User Story 測試，建立綠燈基準線。
2. Scenario 完成 Refactor 後，跑「先前已完成 Scenario + 本則 Scenario」的累積測試。
3. 該層 User Story 全部 Scenario 完成後，再跑完整 User Story 測試集合。
4. 該層 User Story 完成時，另跑該層全套測試，確認沒有破壞先前完成的其他 User Story。

### 8.2 失敗處理

- 本則修改弄紅先前 Scenario：本則 Scenario Agent 不得結束，由本則修改者修復，直到新舊 Scenario 同時全綠。
- 發現尚未被任何 Scenario 描述的交互行為：新增或歸入一則可獨立命名的 Scenario，再以 Scenario 粒度跑 TDD。
- 發現 AC、Edge 或 API 契約互相衝突：停止實作，回到 `analyze`、`clarify` 或上游 artifact 修正。
- 不建立「User Story Green」去一次修完所有紅燈。

### 8.3 測試集合與組合旅程

預設的 User Story 全綠閘門是執行既有 Scenario 測試集合，不必為了形式再建立一支重複測試。

只有多個 Scenario 組合後產生一個尚未被單則測試證明的重要行為時，才增加該層 User Story 組合旅程。若組合旅程失敗，仍回送到可命名的 Scenario 修復，不在旅程內直接實作。

## 9. 前端 Scenario 測試設計

前端 Scenario 的主要證據為執行期 Web 應用的瀏覽器測試：

```text
Playwright
→ 真 Vite 頁面
→ 真 DOM 與前端 JavaScript
→ 依 api-plan.md 建立的 API Mock
→ 使用者看得見的結果
```

前端測試必須：

- 優先以角色、標籤、可見名稱或明確測試識別定位元素，不依賴易碎的 CSS 結構。
- 等待可觀測狀態，不使用固定秒數等待。
- 每則 Scenario 隔離瀏覽器狀態、Mock 資料、local storage、時間與檔案 fixture。
- 上傳使用固定測試檔案。
- 拖放同時驗證操作後的畫面狀態；持久化則留到完全端對端或有真實儲存邊界的測試。
- 不把呼叫內部函式或檢查 Mock 呼叫次數當成 Scenario 完成證據。

## 10. 後端 Scenario 測試設計

後端 Scenario 從 `api-plan.md` 定義的公開 API 進入，執行真實路由、應用邏輯與可控測試資料庫／檔案系統，再由正式 API response 或正式讀取 API 觀測結果。

後端測試不得：

- 只測 private method 或內部 helper。
- Mock 自家 service、repository 或 controller 協作後宣稱端對端完成。
- 直接查資料庫取代正式 API 結果，除非該項本身是資料層專用驗證而不是 Scenario 完成證據。

## 11. User Story 完全端對端驗收

### 11.1 前置條件

- 該 User Story 的後端層內全綠閘門已通過。
- 該 User Story 的前端層內全綠閘門已通過。
- 前端 API Mock 已停用。
- 真前端、真後端、真資料庫／檔案環境可啟動並重置。

### 11.2 執行方式

完全端對端以 User Story 為粒度，從真瀏覽器執行一條能證明獨立使用者價值的完整路徑。它是驗收與回歸閘門，不預設製造 Red，也不拆成 Red、Green、Refactor 三個工作。

整合 task 的可機械欄位固定為 `Mock：停用`、`前端：真實執行期頁面`、`API：正式 API`、`後端：真實後端`。契約證據命令只以 User Story 選取該故事全部契約，不得再加 Scenario 或單一契約 ID。

### 11.3 失敗處理

- 若失敗來自前端或後端行為缺口，將可重現失敗回送到對應 Scenario，完成 Scenario RGB 後重跑完全端對端。
- 若失敗來自前後端契約不一致，先以 `api-plan.md` 判定哪一方偏離，再回送該層 Scenario。
- 若失敗只存在於 proxy、啟動設定或真串接環境，建立可重現該接線缺陷的整合回歸驗證後修復，再重跑 User Story 完全端對端。
- 不在整合工作中直接擴充未被 Scenario 或上游規格定義的新行為。

## 12. 契約與流程檢查

### 12.1 Analyze 的實作前檢查

- 技術研究與 plan 已明確記錄前端測試套件。
- 前端存在時，task setup 有對應的安裝、設定、啟動與測試命令。
- `api-plan.md` 具備可解析的 method、path、status、request 與 response 固定欄位。
- `api-plan.md` 的人工 Responses、測試規劃與可機械驗證契約逐案例雙向覆蓋，人工 JSON 範例符合機械 Schema，且沒有空 Schema。
- `e2e-test-plan` 與三份 `task-plan` 對 API 契約的引用皆對齊 `api-plan.md`。
- `e2e-test-plan` 的 blocked 章節固定使用 ID／描述／阻塞原因三欄表格；沒有項目時也保留三個「（無）」欄位。
- 每則前端 Scenario 明列 API 使用狀態，且 API 與 API 契約案例的「不適用」狀態一致。
- Scenario、契約與外層 User Story 三者一致；即使正確故事已有引用，額外掛到錯故事仍視為失敗。
- 每則前端／後端 Scenario 都有完整 Red、Green、Refactor 與主斷言。
- `受測行為`、`實作計畫`、`整理範圍` 各只出現一次並分別位於 Red、Green、Refactor，不能由正確位置的副本掩護錯置內容。
- 一個 Scenario 的三階段由同一個 Scenario Agent 執行。
- Scenario 完成條件包含位於 Refactor 後的 User Story 層內全綠閘門。
- 該層 User Story 完成條件包含位於最後一則 Scenario 層內全綠後的該層全套回歸。
- 整合 task 是 User Story 完全端對端驗收，不含假的預期 Red。
- 整合的 Mock、前端、API、後端欄位使用固定值，契約證據只限縮 User Story，不限縮單一 Scenario。
- 每一則整合 Scenario 的前置資料本身都明列可重置測試資料。
- 整合失敗能回送到 Scenario 或接線回歸驗證，而不是在整合區塊任意實作。

### 12.2 Implement 的實作後閘門

- Scenario 完成前，契約 validator 已比對該 Scenario 實際使用的前端 Mock 或後端契約測試與 `api-plan.md`。
- User Story 層內全綠前，契約 validator 已比對該故事所有 endpoints 在目前層要求的證據來源，不只檢查本次新增的一則，也不提前要求尚未執行的其他層證據。
- 完全端對端驗收完成前，契約 validator 已比對真串接時擷取的 request／response 證據，且前端 API Mock 確實停用。
- 所有測試、契約案例與契約命令都以單行欄位解析，通過非空白、用途、標準驗證器路徑與包裝器內層執行器／實際測試子命令檢查；`playwright --help`、`playwright --version` 與只列測試不執行的命令不算證據。證據的有效產生時間、來源與 Scenario 粒度符合目前層別，同時不錯殺未把層別寫進命令名稱的合法測試入口。
- validator 失敗或主斷言所需欄位無法解析時，禁止勾選對應 Scenario、User Story 或整合任務完成，並依第 11.3 節回送修復。

## 13. 對水球原始包的採用判斷

水球原始壓縮包由 skill 套件、rules、templates 與少量套件中繼資料組成，沒有實際專案、前端測試碼、`package.json` 或 Playwright 設定，不能作為「已實作前端 TDD」的證據。

原始包的技術研究範例採用 Vitest + Supertest 驗證 API，拖放與整體前端操作留給手動驗證，並明確排除完整瀏覽器端對端框架。這不符合州巧目前要支援前端瀏覽器 TDD 的目標。

下列觀念州巧原本已經具備或本輪已獨立討論成立，不因水球包出現才採用：

- Scenario 對準公開可觀測行為。
- 一次處理一個主要行為。
- Red 必須因正確行為缺口而失敗。
- Green 只做本則需要的行為。
- Refactor 不擴充需求。
- User Story 完成前需要故事範圍的全綠驗證。

因此不把這些包裝成「搬入水球設計」。水球原始包只作為比較來源；任何規則都必須先證明能解決州巧的實際問題，才進入修改提案。

## 14. Skill engineering 實作範圍

本輪修改涵蓋：

- `technical-research`：偵測與收斂前端測試套件，必要時呼叫 `clarify`。
- `plan.md`／technical research 產物：保存已選定測試套件與用途。
- `api-plan`：提供可被前端 Mock、後端測試與 analyze 對齊的契約資訊。
- `e2e-test-plan`：保留 Scenario，不新增 Slice／Journey 類型；明確分開前端、後端與完全端對端驗收。
- `task-plan`：前後端一則 Scenario 一個 RGB；整合改成 User Story 驗收閘門。
- `implement`：一個 Scenario Agent 跑完整 RGB，執行 User Story 層內全綠閘門，並在 Scenario、User Story 與整合完成點呼叫契約 validator。
- `tdd-e2e-red`／`green`／`refactor`：成為同一 Scenario Agent 內連續階段，不作為重開代理的邊界。
- `analyze`：增加測試套件、實作前 API 契約、層內全綠與整合邊界檢查，不驗證尚未產生的實作。

實作已依 `skill-engineering` 的編排提案完成；使用者已明確授權本輪不等待提案確認，直接修改 skill chain，交付前仍依專案規則完成本機檢查、審查與隔離驗證。
