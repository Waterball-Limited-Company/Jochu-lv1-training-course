# Skill 工程編排提案

狀態：已實作；交付閘門結果以本輪最終回報為準

## 任務資訊

- 處理路徑: `optimize`
- 改動範圍: `chain rewrite`
- 目標 Skills: `technical-research`、`api-plan`、`e2e-test-plan`、`task-plan`、`analyze`、`implement`、`tdd-e2e-red`、`tdd-e2e-green`、`tdd-e2e-refactor`

## 控制平面重建

- 技術研究先偵測既有前端測試套件；只有新專案未選定、既有能力不足，或多套可行但沒有主套件時才呼叫 `clarify`。Web 瀏覽器端對端預設推薦 Playwright。
- `api-plan.md` 同時保存可讀契約與可機械解析的 method、path、status、request、response，供前端 Mock、後端契約測試與整合證據共用；後產生的 e2e 與 task 以穩定契約案例 ID 反向引用，不要求 api-plan 預知 Scenario。
- 端對端計畫維持後端、前端、整合三層：前後端以 Scenario 為 TDD 顆粒度，整合以 User Story 為完全端對端驗收。
- 後端與前端任務維持三份 task 產物中的兩份，每則 Scenario 由一位 Scenario Agent 連續完成 Red、Green、Refactor，再通過 User Story 層內全綠閘門。
- 任務驗證器不只檢查四種 checkbox 存在，也強制層內全綠閘門位於該 Scenario 的 Refactor 後，故事完成閘門位於最後一則 Scenario 的層內全綠閘門後。
- Red／Green／Refactor 的核心欄位各只能出現一次且必須位於自己的 phase；正確欄位不能掩護其他 phase 的錯置副本。
- 整合任務保留第三份 task 產物，但改成 User Story 完全端對端驗收，不再假造 Red、Green、Refactor。
- `analyze` 只做實作前的規劃契約檢查；`implement` 在實作後的 Scenario、User Story、整合完成點執行契約證據驗證。
- 新產出的 technical research 與 plan 由主流程以 `--require-v2` 錨定版本；package 的可機械驗證契約再錨定下游版本。任何產物不得透過刪除版本標記退回舊驗證；契約引用同時核對 Scenario ID、外層 User Story 與契約所屬故事。
- 前端 Scenario 以固定 API 欄位宣告是否碰 API；只要碰 API 就逐 Scenario 引用契約，不能由同一故事的其他 Scenario 代替。
- 整合以固定 Mock／前端／API／後端欄位證明真串接；契約證據只限縮 User Story，不得縮成單一 Scenario。
- 任務驗證器將欄位值限制在同一行，拒絕空白命令／契約案例、用途錯置、Mock 矛盾、假驗證器路徑，並略過 `--package` 等包裝器選項及其值後檢查真正 payload，拒絕 `echo`、`sh -c 'exit 0'`、`true` 等假測試與吞錯命令；Mock 判斷先排除「不使用／未啟用／不會重新啟用」等明確安全語意，避免誤殺。
- 端對端計畫驗證器要求 blocked 章節保留三欄表格；沒有 blocked 項時也以三個「（無）」欄位表示，讓規則、樣板、範例與機械檢查一致。
- 每一則整合 Scenario 的前置資料都必須自行明列可重置測試資料，不能只靠整合章節前言宣告一次。
- 契約證據驗證器檢查可辨認的測試產生命令、實際有效且具時區的時間與各層 Scenario ID 格式；時間同時接受省略小數秒與 JavaScript `toISOString()` 毫秒格式，層別由 `source` 宣告，不錯殺一般合法測試命令。
- `api-plan.md` 的人工 Responses、測試規劃與機械契約必須逐案例雙向覆蓋，人工 JSON 範例也須符合機械 Schema；request／response 不接受會關閉驗證的空 Schema。
- 同一 User Story 的 Scenario 依序執行；每則完成後跑該故事累積測試，故事邊界再跑整層回歸。整合錯誤依行為、契約或接線分類回送。

## 步驟決策

- `前端測試套件決策`：rewrite SOP，derive rule，更新 technical research 與 plan 樣板及驗證器。
- `API 單一契約來源`：rewrite SOP，derive rule，更新 api-plan 樣板與結構驗證器。
- `API 規劃引用檢查`：derive script，由 `analyze` 在實作前執行。
- `後端／前端／整合證明邊界`：rewrite 現有 e2e 規則、樣板與驗證器，不新增 Slice 或 Journey 類型。
- `三份任務產物`：保留檔案拓樸；重寫後端／前端 Scenario 區塊與整合 User Story 驗收區塊，更新驗證器。
- `Scenario Agent 生命週期`：rewrite implement SOP 與委派規則，derive template 固定單一代理輸入與回報契約。
- `實作後 API 契約證據`：derive rule、derive template、derive script，在三個完成點阻擋契約漂移。
- `Red／Green／Refactor`：保留三個既有 skill 作為同一 Scenario Agent 內的連續階段；移除整合層責任，補前端真瀏覽器與 Mock 邊界、故事累積全綠交接。
- `既有正確 TDD 判準`：keep，保留正確紅燈、最少 Green 與 Refactor 不擴充需求，不宣稱源自水球原始包。
- `舊 US 顆粒度未追蹤規則檔`：不引用、不修改、不刪除，列為使用者既有內容。

## 檔案動作

### 新增 / 更新

- Update `technical-research/SKILL.md`、前端測試選型規則、research／plan 樣板與驗證器。
- Update `api-plan/SKILL.md`、Endpoint 契約規則、api-plan 樣板與驗證器。
- Update `e2e-test-plan/SKILL.md`、證明邊界／對應欄位規則、樣板與驗證器。
- Update `task-plan/SKILL.md`、產物結構／實作意圖規則、六份樣板與驗證器。
- Update `analyze/SKILL.md`、inventory／比對規則；新增規劃契約引用驗證腳本。
- Update `implement/SKILL.md`、執行／進度／回報規則與範圍樣板。
- Add Scenario Agent handoff 骨架與範例。
- Add API 契約證據骨架、範例、規則與機械驗證腳本。
- Update `tdd-e2e-red`、`tdd-e2e-green`、`tdd-e2e-refactor` 的 SOP 與相關規則。

### 刪除

- 不刪除實體檔案。
- 從新控制平面移除「整合也跑 Red／Green／Refactor」與「每個 phase 可視為獨立代理工作」的舊責任。
- 不修改 `specs/001-photo-albums/` 既有示範產物。

## 驗證方式

- 執行各既有產物驗證器的測試 fixture，確認新版產物通過、缺少新閘門或整合殘留 RGB 時失敗。
- 對 API 契約證據驗證器建立通過、method 漂移、response 形狀漂移、缺必要來源與路徑參數等隔離 fixture。
- 執行 skill 引用分析器，確認新增規則、樣板、腳本皆回掛主 SOP；兩份使用者既有未追蹤 US 規則例外列出。
- 執行 Markdown、Python 編譯與 `git diff --check`。
- 確認 `specs/001-photo-albums/` 無任何異動。
- 整批完成後依序進行一位審查代理與一位全新暫存環境驗證代理。

## 實作閘門

- 根因與設計已由使用者逐輪修正；第五輪審查與續修第一版發現的命令、Mock、契約、時間、跨行空值及 blocked 格式缺口，已進入使用者授權的續修版本，審查與隔離驗證結果以本輪最終交付為準。
- 使用者已明確授權不等待提案確認，直接依本提案實作。
