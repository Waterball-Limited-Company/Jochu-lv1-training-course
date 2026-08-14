# 規格分析報告：照片相簿整理應用程式

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-29
**狀態**: 草稿

---

## 每階段產物盤點表


| 產物      | 路徑                                                            | 狀態  |
| ------- | ------------------------------------------------------------- | --- |
| 功能規格    | `specs/001-photo-albums/spec.md`                              | 存在  |
| 系統分析總覽  | `specs/001-photo-albums/plan.md`                              | 存在  |
| 技術研究    | `specs/001-photo-albums/system-analyze/technical-research.md` | 存在  |
| 資料計畫    | `specs/001-photo-albums/system-analyze/data-plan.md`          | 存在  |
| DDL     | `specs/001-photo-albums/system-analyze/DDL.md`                | 存在  |
| API 計畫  | `specs/001-photo-albums/system-analyze/api-plan.md`           | 存在  |
| UI 計畫   | `specs/001-photo-albums/system-analyze/ui-plan.md`            | 存在  |
| 端對端測試計畫 | `specs/001-photo-albums/e2e-test-plan.md`                     | 存在  |
| 後端實作計畫  | `specs/001-photo-albums/task-plan/task-backend.md`            | 存在  |
| 前端實作計畫  | `specs/001-photo-albums/task-plan/task-frontend.md`           | 存在  |
| 整合實作計畫  | `specs/001-photo-albums/task-plan/task-integration.md`        | 存在  |


> 狀態用語：`存在`／`缺失`／`不適用`（plan 未要求且合理跳過）。

---



## 問題總表


| 編號   | 比對依據  | 嚴重程度 | 位置                     | 摘要                                                                                                   | 建議處理                                                           |
| ---- | ----- | ---- | ---------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 一致-1 | 跨層一致性 | 中    | ui-plan.md／api-plan.md | UI「API 對應」使用 `{albumId}`／`{id}` 路徑參數寫法，api-plan Endpoint 使用 `:albumId`／`:id`；語意同一組 endpoint，但文件表記不一致 | 擇一統一（建議對齊 api-plan 的 `:param`），手動微調 `ui-plan.md` 即可；不需重跑 skill |


本輪無嚴重／高優先發現。

---



## 規格覆蓋矩陣


| 需求編號    | 摘要                 | 介面落點                                      | Scenario    | Task                                        | 備註                            |
| ------- | ------------------ | ----------------------------------------- | ----------- | ------------------------------------------- | ----------------------------- |
| US1-FR1 | 可建立並命名相簿           | `POST /albums`；主頁建立流程                     | S-1-1、S-1-3 | task-backend、task-frontend                  | —                             |
| US1-FR2 | 將照片加入指定相簿          | `POST /albums/:albumId/photos`；相簿詳情上傳     | S-1-1       | task-backend、task-frontend                  | —                             |
| US1-FR3 | 一次多選 JPEG／PNG／WebP | 同上上傳合約；mime 約束                            | S-1-1、S-1-4 | task-backend、task-frontend                  | Edge-1-2 對不支援格式               |
| US1-FR4 | 改歸屬＝移動             | `PATCH /photos/:id`；相簿詳情「移至其他相簿」          | S-1-2       | task-backend、task-frontend、task-integration | 對齊 GR-002                     |
| US2-FR1 | 主頁顯示所有相簿           | `GET /albums`；主頁                          | S-2-1       | task-backend、task-frontend                  | —                             |
| US2-FR2 | 依建立日期分組            | `GET /albums` 之 `group_date`；使用者故事 2       | S-2-1、S-2-2 | task-backend、task-frontend                  | —                             |
| US3-FR1 | 主頁拖放重排             | 主頁拖放；`PATCH /albums/reorder`              | S-3-1、S-3-3 | task-frontend（互動）；持久化見 FR2                  | S-3-1／S-3-3 僅前端落點（與 e2e 摘要一致） |
| US3-FR2 | 保存重排順序             | `PATCH /albums/reorder`；`sort_order`      | S-3-2       | task-backend、task-frontend、task-integration | —                             |
| US4-FR1 | 進入單一相簿             | `GET /albums/:albumId/photos`；相簿詳情        | S-4-1、S-4-2 | task-backend、task-frontend                  | —                             |
| US4-FR2 | 平鋪預覽               | 相簿詳情平鋪；photos URL 欄位                      | S-4-1       | task-backend、task-frontend                  | —                             |
| US4-FR3 | 空狀態                | 空陣列＋前端空狀態                                 | S-4-2       | task-backend、task-frontend                  | —                             |
| GR-001  | 相簿不可巢狀             | `POST /albums` 無巢狀欄位；data／DDL 無父子邊        | S-1-5       | task-backend、task-frontend                  | Edge-G-1                      |
| GR-002  | 一照片一相簿             | `photos.album_id` 1:N；`PATCH /photos/:id` | S-1-2       | task-backend、task-frontend、task-integration | Edge-G-2                      |


> 成功標準（`USn-SCm`）屬體驗／回饋 KPI，未列為可建置覆蓋分母。

---



## 驗收覆蓋矩陣


| AC／Edge  | 摘要            | Scenario | 後端  | 前端  | 整合  | Task 落點                    | 備註                  |
| -------- | ------------- | -------- | --- | --- | --- | -------------------------- | ------------------- |
| AC-1-1   | 建「旅行」並匯入多格式   | S-1-1    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |
| AC-1-2   | 改加入另一相簿後只留在目標 | S-1-2    | ✓   | ✓   | ✓   | 三層 task                    | —                   |
| Edge-G-2 | 禁止多重歸屬，改為移動   | S-1-2    | ✓   | ✓   | ✓   | 三層 task                    | 與 AC-1-2 同 Scenario |
| Edge-1-1 | 空相簿仍顯示        | S-1-3    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |
| Edge-1-2 | 不支援格式拒絕並說明    | S-1-4    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |
| Edge-G-1 | 拒絕相簿巢狀        | S-1-5    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |
| AC-2-1   | 主頁依建立日期分組     | S-2-1    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |
| Edge-2-1 | 無相簿之日期不顯示空白分組 | S-2-2    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |
| AC-3-1   | 拖放後立即見新順序     | S-3-1    | —   | ✓   | —   | task-frontend              | 互動呈現；後端刻意不列         |
| AC-3-2   | 重整後仍保留順序      | S-3-2    | ✓   | ✓   | ✓   | 三層 task                    | —                   |
| Edge-3-1 | 僅一相簿時拖放不混淆    | S-3-3    | —   | ✓   | —   | task-frontend              | 互動呈現；後端刻意不列         |
| AC-4-1   | 多張照片平鋪預覽      | S-4-1    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |
| Edge-4-1 | 空相簿可理解空狀態     | S-4-2    | ✓   | ✓   | —   | task-backend、task-frontend | —                   |


---



## 指標


| 指標                     | 數值  |
| ---------------------- | --- |
| 需求總數（FR／GR 計入覆蓋者）      | 13  |
| 有介面落點的需求數              | 13  |
| 有 Scenario 的需求數        | 13  |
| AC／Edge 總數             | 13  |
| 有 Scenario 的 AC／Edge 數 | 13  |
| 發現總數                   | 1   |
| 嚴重                     | 0   |
| 高                      | 0   |
| 中                      | 1   |
| 低                      | 0   |


---



## 其餘發現摘要

無。

跨層抽查摘要（未另列為發現）：

- e2e 對應欄位所引 API（`POST/GET/PATCH` 各路徑）皆存在於 `api-plan.md` 追溯總表。
- `data-plan`／`DDL`：`Album 1—0..* Photo`、`album_id` FK、無 `parent_album_id`，與 GR-001／GR-002 一致。
- UI 頁面（主頁、相簿詳情）與使用者故事 1–4 所對 API 皆可對回 api-plan（僅路徑參數表記見一致-1）。
- task 各層 Scenario 集合與 e2e 測試摘要總表落點一致（含 S-3-1／S-3-3 僅前端、整合僅 S-1-2／S-3-2）。

---



## 下一步建議

本輪無嚴重發現。請先 Review `specs/001-photo-albums/analyze-report.md`；若接受一致-1 的文件表記差異或已手動統一，即可執行 `/implement` 開始依 `task-plan/` 實作。若希望針對一致-1 提出具體補救編輯建議，可在對話指定即可（不會自動改檔）。

---



## 假設

- inventory 未另存檔；矩陣落點來自各產物既有 ID、api 追溯總表、e2e 對應欄位／測試摘要總表與 task 章節。
- AC／Edge 編號採 e2e-test-plan 之穩定 ID（spec 原文為條列驗收／邊界，由 e2e 編號追溯）。
- `USn-SCm` 成功標準不計入可建置覆蓋分母。
- S-3-1、S-3-3 僅前端、整合僅 S-1-2／S-3-2，視為與 e2e／task 假設對齊的刻意落點，不記為覆蓋缺口。

