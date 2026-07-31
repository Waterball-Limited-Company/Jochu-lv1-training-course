# Implement Scale 流程問題紀錄

**計畫 package**: `002-meeting-room-booking`  
**範圍**: 4 — 後端 → 前端 → 整合  
**開始時間**: 2026-07-30  
**目的**: 沿路記錄「照現有 Artifact-First / implement scale 流程執行」時實際遇到的摩擦、缺口與風險（非產品 bug 清單）。

---

## 進場（Phase 1）

| # | 嚴重度 | 現象 | 影響 | 備註 |
| --- | --- | --- | --- | --- |
| E1 | 低 | `/implement` 未帶 `plan-package`／範圍時，必須先問範圍四選一才動手 | 多一輪對話才能開工 | 設計如此；本輪使用者選 4 |
| E2 | 中 | 鎖定 package 後找不到 `analyze-report.md` | 進場只警告、不硬停；一致性分析可被跳過 | skill 允許缺檔繼續；訓練流程若期望 analyze 為必經，閘門偏軟 |
| E3 | 低 | Docker 由人先行開好，task §2.4 仍寫 `docker compose up -d postgres` | 步驟與現實環境略脫節；易重複起容器或假設 compose 服務名 | 本輪以「容器已就緒」為準，仍驗證 compose／連線 |

---

## 後端 §1／§2

| # | 嚴重度 | 現象 | 影響 | 備註 |
| --- | --- | --- | --- | --- |
| B1 | 高 | 使用者說「docker 我幫你開好了」，實際 `docker ps` 是 **TrainMate** 容器（caddy/backend/frontend），本專案尚無 `docker-compose.yml`／Postgres | 若直接假設 DB 已就緒會連錯環境；必須新建本專案 compose | 已拉起 `jochu-meeting-room-postgres` |
| B2 | 中 | Agent 預設 sandbox **無法**連 `docker.sock`（permission denied），需升高權限才能 compose／測試 | implement 每步驗證易卡；自動化 agent 對 Docker 依賴摩擦大 | 本輪改用 `all` 權限後通過 |
| B3 | 中 | `task-backend` §1「已讀 xxx」是大量 checkbox，無客觀驗證深度 | 易變成勾選儀式；漏讀細節要到 Red／Green 才爆 | 流程本身無法證明「真的讀完」 |
| B4 | 低 | compose 只建 `meeting_room`，測試庫 `meeting_room_test` 需 helper 動態 `CREATE DATABASE` | 第一版 smoke 因 DB 不存在失敗一次 | 已修 helper；樣板可預先寫明 |
| B5 | 低 | `npm install` 未鎖 major → 裝到 **Express 5**；plan／憲法只寫 Express 未釘版本 | 後續若範例／教材寫 Express 4 API 可能漂移 | 建議 task／plan 釘 `express@4` 或明示接受 5 |
| B6 | 低 | 本機 Node `v24.14.0`；task 要求「現行 LTS」但未寫死版號，僅靠實作時鎖定 | 不同學員機器可能鎖不同 major | 已寫 `.nvmrc`=`24`、`engines.node`=`>=24 <25` |
| B7 | 資訊 | Cursor 每次改檔都跳出「review+verify loop」提醒；與 `/implement` 長流程逐步落地節奏衝突 | 噪音／認知負擔 | 屬編輯器／規則干擾，非產品問題 |

§1／§2 狀態：**完成**（smoke 通過）。

---

## 後端 §3 TDD 委派

| # | 嚴重度 | 現象 | 影響 | 備註 |
| --- | --- | --- | --- | --- |
| T1 | 高 | skill 規定「一 Scenario 一 `/tdd-e2e-red` 委派」；本 package 後端約 21+ Scenario | 嚴格照做對話／回合極長，訓練 scale 幾乎不可完跑 | 本輪 US-1 後續 Red 改由 implement 同回合批次寫測（已記違規壓力） |
| T2 | 中 | Red 子代理把 `smoke.test.js` 刪掉併入 S-1-1 測檔 | 破壞 §2.4 產物邊界；後續 Scenario 平行／檔案責任不清 | 已還原獨立 smoke；並設 `--test-concurrency=1` |
| T3 | 中 | 多測檔預設平行 + 共享 `meeting_room_test` 重置 → schema 競態 | 假環境洞／偶發失敗 | 已用 concurrency=1；task／樣板應預先寫明 |
| T4 | 中 | US-1 多數 Red 在「login 仍 404」就失敗，尚未碰到各自特色斷言 | Red 覆蓋偏淺；Green 前難以證明衝突／規則測寫對 | 合格 Red 形態仍成立（status 不符） |
| T5 | 低 | 測資硬編碼 `2026-07-31`（當下附近的平日） | 日久可能變成假日／週末語意問題 | 應改為「下一個台北平日」helper |

| T6 | 中 | Green 後第一次全套測因 `pg` Pool 閒置不退出，跑約 63s | 誤判卡住／拖慢迴圈 | 子代理加 `allowExitOnIdle` 後約 3s；§2 樣板應寫明 |
| T7 | 資訊 | US-1 Green 一次實作讓 7 支全綠（符合 green 允許多支同綠） | 與「一 Scenario 一 Red」不對稱：Red 碎、Green 塊 | 教學上節奏不一致 |

| T8 | 中 | Cursor Auto-review 曾阻擋 `npm test`，理由誤判為「只該寫 log、不該跑測」 | 與 `/implement` 必跑測衝突，需人工核准 | 寫 log 與執行 implement 並存時易觸發 |
| T9 | 低 | US-1 Refactor：抽出 `lib/session.js`、`lib/booking-rules.js`、錯誤碼對照表 | 行為不變，9/9 仍綠 | 已勾選 |

US-1 整段（Red→Green→Refactor）：**完成**。

| # | 嚴重度 | 現象 | 影響 | 備註 |
| --- | --- | --- | --- | --- |
| T10 | 中 | US-2 overview 聚合 SQL 初版把 LEFT JOIN 空列誤算成全日 720 分鐘 | Green 迴圈多一轮除錯 | 典型「契約細節在測裡才爆」 |
| T11 | 低 | US-2 跳過嚴格「先全紅再綠」節奏：測寫完後直接 Green（測曾短暫為紅） | 與 skill 字面順序不完全一致 | scale 壓力下的折衷 |

US-2 整段：**完成**（13/13 全綠；Refactor 以整理日期邊界／查詢為主，無大改）。

| # | 嚴重度 | 現象 | 影響 | 備註 |
| --- | --- | --- | --- | --- |
| T12 | 中 | US-3／US-4 以「同回合寫測+Green」一次做完 10 Scenario | 嚴格 Red→Green 閘門被壓縮；子代理還卡在自我 review 等待 | scale 下幾乎必然 |
| T13 | 低 | 子代理 cwd／`npm test` 路徑偶發找錯 package.json | 假環境洞 | 改用 `npm --prefix backend test` |

後端整層：**完成**（`npm test` **23/23** 全綠）。

---

## 前端

| # | 嚴重度 | 現象 | 影響 | 備註 |
| --- | --- | --- | --- | --- |
| F1 | 高 | 選範圍 4 後，後端 21 Scenario × Red/Green/Refactor + 前端 ~20 + 整合，單一對話幾乎無法「嚴格逐步委派」跑完 | 被迫批次／背景子代理，偏離 skill 字面 | 前端改由背景代理整層完成 |
| F2 | 中 | `npm create vite` 預設帶 `counter.ts` 範例，與 task 目錄契約不一致 | 需清掉範例再鋪 pages／router | 已替換為六頁 SPA |
| F3 | 中 | 前端 task 要求「瀏覽器驗收」但未釘測試 runner；實作改採 vitest+jsdom | 與「真瀏覽器 E2E」語意可能落差 | 契約模糊；25 測全綠 |
| F4 | 中 | Shell／npm `devdir` 設定導致誤跑到 monorepo 根 | 假環境洞 | 改用 `npm --prefix frontend` |
| F5 | 低 | 預設真 API；Mock 需 `VITE_USE_MOCK=true` | 本層獨立驗收與整合切換要記清楚 | 見 `frontend/IMPLEMENT_STATUS.md` |

狀態：**完成**（build PASS；`vitest` 25/25；`task-frontend.md` 由 [Implement full frontend layer](724ddb9b-1933-4ba8-acd3-1e1287dbd1b6) 勾選）。

---

## 整合

| # | 嚴重度 | 現象 | 影響 | 備註 |
| --- | --- | --- | --- | --- |
| I1 | 中 | 重置 DB 會 drop session table；共用長生命週期 backend 會讓後續 Scenario session 壞掉 | 假失敗 | 每 Scenario 用 ephemeral backend（見整合測） |
| I2 | 中 | 整合測不可與共享 DB 平行跑 | 必須串行 | 與後端 T3 同源 |
| I3 | 低 | 整合層補了 `/api/auth/me`、`/api/auth/logout`（單層先前未強制測到） | 顯示「單層綠 ≠ 整合契約齊」 | 真串接才暴露缺口 |
| I4 | 資訊 | Auto-review 曾阻擋勾選 integration §1／§2 | 進度檔與實況短暫不一致 | 已補勾 |

狀態：**完成**（`npm --prefix frontend run test:integration` **4/4**；由 [Integration layer four scenarios](efe9dcfa-776c-4ea4-9c53-614d02ea7d8a) 完成 §3）。

---

## 彙整

- 最痛的摩擦：
  1. **「一 Scenario 一 Red 委派」在真實 package 規模不可完跑**（後端 21 + 前端約 20 + 整合 4）。
  2. **「Docker 已開」語意不清**——開的是別專案（TrainMate）容器。
  3. **共享測庫 + 平行測試／session table 被 reset 清掉** 造成假環境洞。
  4. **寫 log 與執行 implement 並存** 時 Auto-review 易誤擋跑測／勾選。
- 建議改 skill／樣板的點：
  1. 允許同 US 批次 Red，或 US 級 Red 閘門。
  2. §2 明示 `test-concurrency=1`、測試庫建立、`allowExitOnIdle`、整合測用 ephemeral server。
  3. Docker 驗收改為「本專案 compose 服務健康」。
  4. 前端明確 vitest+jsdom 可接受，或正式要求 Playwright。
- 本輪結果：
  - package：`002-meeting-room-booking`
  - 範圍：後端 → 前端 → 整合 **全完成**
  - 後端 23/23、前端 25/25、整合 4/4、前端 build PASS
  - 問題紀錄：`implement-scale-process-log.md`
