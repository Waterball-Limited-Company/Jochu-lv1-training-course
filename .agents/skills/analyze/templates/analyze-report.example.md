# 規格分析報告：照片相簿整理應用程式

**功能分支**: `001-photo-albums`
**建立日期**: 2026-07-28
**狀態**: 草稿

---

## 每階段產物盤點表

| 產物 | 路徑 | 狀態 |
| --- | --- | --- |
| 功能規格 | `specs/001-photo-albums/spec.md` | 存在 |
| 系統分析總覽 | `specs/001-photo-albums/plan.md` | 存在 |
| 技術研究 | `specs/001-photo-albums/system-analyze/technical-research.md` | 存在 |
| 資料計畫 | `specs/001-photo-albums/system-analyze/data-plan.md` | 存在 |
| DDL | `specs/001-photo-albums/system-analyze/DDL.md` | 存在 |
| API 計畫 | `specs/001-photo-albums/system-analyze/api-plan.md` | 存在 |
| UI 計畫 | `specs/001-photo-albums/system-analyze/ui-plan.md` | 存在 |
| 端對端測試計畫 | `specs/001-photo-albums/e2e-test-plan.md` | 存在 |
| 後端實作計畫 | `specs/001-photo-albums/task-plan/task-backend.md` | 存在 |
| 前端實作計畫 | `specs/001-photo-albums/task-plan/task-frontend.md` | 存在 |
| 整合實作計畫 | `specs/001-photo-albums/task-plan/task-integration.md` | 存在 |

> 狀態用語：`存在`／`缺失`／`不適用`（plan 未要求且合理跳過）。

---

## 問題總表

| 編號 | 比對依據 | 嚴重程度 | 位置 | 摘要 | 建議處理 |
| --- | --- | --- | --- | --- | --- |
| 一致-1 | 跨層一致性 | 高 | e2e-test-plan.md（S-x-y）／api-plan.md | Scenario 對應欄位引用 `POST /albums/move`，但 api-plan 無此路徑 | 修正 `api-plan.md` 或 e2e 對應欄位後，視需要重跑 `/e2e-test-plan` |
| 覆蓋-1 | 覆蓋 | 中 | task-frontend.md | 某次要 Edge 僅有後端 Scenario，前端 Task 未點名 | Review 是否刻意只做後端證明；否則補 task-frontend 對應步驟 |

> 上表為範例完成態（含刻意衝突示範）；真實執行時依偵測結果填列。若無問題，保留表頭並於表下寫「本輪無問題」。

---

## 規格覆蓋矩陣

| 需求編號 | 摘要 | 介面落點 | Scenario | Task | 備註 |
| --- | --- | --- | --- | --- | --- |
| US1-FR1 | 可建立並命名相簿 | `POST /albums`；主頁／建立流程（ui-plan） | S-1-1、S-1-3 | task-backend、task-frontend、task-integration | — |
| US1-FR4 | 改歸屬為移動，不同時屬兩相簿 | `PATCH /photos/:id` | S-1-2 | task-backend、task-integration | 對齊 GR-002 |
| GR-001 | 相簿不可巢狀 | `POST /albums` 契約／領域約束 | （依 e2e 實際列） | task-backend | — |

---

## 驗收覆蓋矩陣

| AC／Edge | 摘要 | Scenario | 後端 | 前端 | 整合 | Task 落點 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-1-1 | 建「旅行」相簿並匯入多格式 | S-1-1 | ✓ | ✓ | ✓ | 三層 task 皆有對應 US-1 | — |
| AC-1-2 | 改加入另一相簿後只留在目標 | S-1-2 | ✓ | ✓ | ✓ | task-backend／integration | — |
| Edge-G-2 | 禁止多重歸屬，改為移動 | S-1-2 | ✓ | ✓ | ✓ | 與 AC-1-2 同 Scenario | — |

---

## 指標

| 指標 | 數值 |
| --- | --- |
| 需求總數（FR／GR 計入覆蓋者） | 12 |
| 有介面落點的需求數 | 12 |
| 有 Scenario 的需求數 | 11 |
| AC／Edge 總數 | 15 |
| 有 Scenario 的 AC／Edge 數 | 15 |
| 發現總數 | 2 |
| 嚴重 | 0 |
| 高 | 1 |
| 中 | 1 |
| 低 | 0 |

---

## 其餘發現摘要

無。

---

## 下一步建議

本輪無嚴重發現。請先 Review `analyze-report.md` 中的高／中項；確認可接受後再執行 `/implement` 開始實作。若要針對「高」項提出具體補救編輯建議，可在對話中指定前 N 項。

---

## 假設

- inventory 未另存檔；矩陣中的落點字串來自各產物既有 ID 與追溯欄位。
- 「不適用」僅用於 plan 未要求且合理跳過的介面產物。
