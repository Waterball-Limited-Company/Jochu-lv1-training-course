# 實作計畫（整合）：照片相簿整理應用程式

**功能分支**: `001-photo-albums`  
**建立日期**: 2026-07-27  
**狀態**: 草稿  
**範圍**: 前後端真串接（僅 Then 必須兩端一起才有意義的 Scenario）

---

## 1. 規格閱讀

- [ ] 已讀 `e2e-test-plan.md` 的 `## 整合`（本輪 S-1-2、S-3-2）
- [ ] 已讀 `task-backend.md`／`task-frontend.md` 對應 US
- [ ] 已讀 `api-plan.md`、`ui-plan.md`
- [ ] 確認整合 Scenario 無 blocked 項

```bash
ls specs/001-photo-albums/e2e-test-plan.md \
   specs/001-photo-albums/task-plan/task-backend.md \
   specs/001-photo-albums/task-plan/task-frontend.md \
   specs/001-photo-albums/system-analyze/api-plan.md \
   specs/001-photo-albums/system-analyze/ui-plan.md
```

---



## 2. 環境建立

### 2.1 前置確認

- [ ] `backend/` 可啟動且本檔所需 API 可用
- [ ] `frontend/` proxy `/api`、`/media` 指向該後端
- [ ] Node 20.x

```bash
node -v
ls backend/package.json frontend/package.json frontend/vite.config.js
```



### 2.2 串接與清場

- [ ] 約定兩端同時啟動方式
- [ ] 可重置 DB／uploads／thumbs，避免 Scenario 互相污染
- [ ] 最小連線：前端經 proxy 打到後端無連線錯誤

---



## 3. User Story 實作計劃



### US-1 建立相簿並整理照片（優先級：P1）



#### AC / Edge

- AC-1-2 假設使用者已建立多個相簿且某張照片已屬於相簿 A，當使用者將該照片加入相簿 B，則該照片應只出現在相簿 B，且不再出現在相簿 A
- Edge-G-2 當系統偵測到會造成同一張照片同時屬於多個相簿的操作時，必須改為將該照片移動到目標相簿，不得保留多重歸屬



#### Red

- [ ] `/tdd-e2e-red` — S-1-2 將已歸屬照片改加入另一相簿後只留在目標相簿（真串接）:
  - 實作計畫：
    - UI 在相簿詳情執行「移至其他相簿」→ 真打 `PATCH /photos/:id`
    - 再分別打開 A／B 詳情（真 `GET .../photos`）斷言只在 B、不在 A
    - 不得以前端 Mock 充數
- [ ] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [ ] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 確認前端移動操作走真 API（非 Mock），body `album_id` 對齊 api-plan
    - 確認後端覆寫歸屬後兩邊讀回一致；必要時修 proxy／錯誤處理／重新載入平鋪的接線，不另開平行契約



#### Refactor

- [ ] `/tdd-e2e-refactor` — 行為不變下整理串接路徑上的重複／錯誤處理（不改契約）

---



### US-3 透過拖放重新排列相簿（優先級：P3）



#### AC / Edge

- AC-3-2 假設使用者已完成一次相簿拖放排序，當使用者重新整理或再次進入主頁面，則系統應仍依先前保存的順序顯示相簿



#### Red

- [ ] `/tdd-e2e-red` — S-3-2 拖放排序後重新整理或再進主頁仍保留順序（真串接）:
  - 實作計畫：
    - 主頁同組拖放 → 真 `PATCH /albums/reorder` 寫入
    - 重整或再進主頁 → 真 `GET /albums` 組內順序與畫面一致
- [ ] `/tdd-e2e-red` — 執行本 User Story 的測試，確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈

#### Green

- [ ] `/tdd-e2e-green` — 讓本 US 既有 Red 全綠:
  - 實作計畫：
    - 確認 DnD 送出的 `group_date`＋完整 `album_ids` 與後端寫入一致
    - 重載路徑不吃過期 Mock；畫面順序對齊 DB `sort_order`



#### Refactor

- [ ] `/tdd-e2e-refactor` — 行為不變下整理 reorder 串接與重載流程

---



## 4. 進度總覽


| User Story | Scenario | Red | Green | Refactor |
| ---------- | -------- | --- | ----- | -------- |
| US-1       | S-1-2    | ⬜   | ⬜     | ⬜        |
| US-3       | S-3-2    | ⬜   | ⬜     | ⬜        |


---



## 5. 假設

- 僅 S-1-2、S-3-2；其餘單層證明留在後端／前端 task
- 若前後端對應 US 尚未 Green，先補齊再跑本檔

