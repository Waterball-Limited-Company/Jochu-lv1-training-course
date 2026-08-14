# 實作計畫（整合）：照片相簿整理應用程式

**功能分支**: `001-photo-albums`  
**建立日期**: 2026-07-27  
**狀態**: 草稿  
**範圍**: 前後端真串接（對準 spec 各 US 的獨立驗證；區塊 ID 用 `US-n`）

---

## 1. 規格閱讀

- [ ] 已讀 `e2e-test-plan.md` 的 `## 整合`（本輪 US-1～US-4）
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
- [ ] 測試入口為執行期畫面＋正式 API；不要把 `system-analyze/ui/*.html` 當測試入口
- [ ] 本節不可偷做各 US 驗收路徑（建立「旅行」、平鋪匯入、拖放排序）

---

## 3. User Story 實作計劃

### US-1 建立相簿並整理照片（優先級：P1）

#### AC / Edge

- spec US-1 獨立驗證：建立兩個相簿、分別加入照片、再把其中一張改加入另一本後，各張只在所屬相簿

#### US-1 建立兩個相簿並確認照片只在所屬相簿

- [ ] `/tdd-e2e-red` — US-1 建立兩個相簿並確認照片只在所屬相簿:
  - 受測行為：
    - 前置：尚未有任何相簿；本機有可加入的照片
    - 打：主頁建立相簿、相簿詳情加入照片與「移至其他相簿」
    - 看：執行期主頁與相簿詳情平鋪區，並用正式 API 讀回「旅行」「家庭」的照片列表。兩邊都要對，不能只看畫面或只看 API
    - 期望：各張照片出現在所屬相簿；被移動的那張只在「家庭」、不在「旅行」
- [ ] `/tdd-e2e-green` — US-1:
  - 實作計畫：
    - 確認前端建立／加入／移動走真 API（非 Mock），body 對齊 api-plan
    - 確認後端覆寫歸屬後兩邊讀回一致；必要時修 proxy／錯誤處理／重新載入平鋪的接線，不另開平行契約
    - 本則不驗證：不支援格式、空相簿卡、禁止巢狀、日期分組、拖放
- [ ] `/tdd-e2e-refactor` — US-1:
  - 整理範圍：
    - 在綠燈下整理建立／加入／移動的真串接路徑與錯誤處理
    - 不准擴到不支援格式、空相簿卡、禁止巢狀、日期分組、拖放

---

### US-2 在主頁面依日期瀏覽相簿（優先級：P2）

#### AC / Edge

- spec US-2 獨立驗證：主頁依各相簿建立日期分組顯示

#### US-2 主頁依建立日期分組顯示相簿

- [ ] `/tdd-e2e-red` — US-2 主頁依建立日期分組顯示相簿:
  - 受測行為：
    - 前置：「旅行」「家庭」建於 2026-07-11；「工作」建於 2026-07-20
    - 打：主頁的日期分組列表
    - 看：執行期主頁的日期標題與相簿卡，並用 `GET /albums` 讀回分組
    - 期望：相簿依各相簿的建立日期分組顯示
- [ ] `/tdd-e2e-green` — US-2:
  - 實作計畫：
    - 確認主頁吃真 `GET /albums`（非過期 Mock）；畫面日期標題與 API `groups[]` 一致
    - 必要時修 proxy／重載，不另開平行契約
    - 本則不驗證：空白日期分組、拖放
- [ ] `/tdd-e2e-refactor` — US-2:
  - 整理範圍：
    - 在綠燈下整理主頁分組的串接與重載
    - 不准擴到空白日期分組、拖放

---

### US-3 透過拖放重新排列相簿（優先級：P3）

#### AC / Edge

- spec US-3 獨立驗證：拖放當下畫面更新，重整後順序仍在

#### US-3 拖放後畫面立即更新且重整後仍保留

- [ ] `/tdd-e2e-red` — US-3 拖放後畫面立即更新且重整後仍保留:
  - 受測行為：
    - 前置：2026-07-11 有「旅行」「家庭」
    - 打：主頁同一天分組內拖放
    - 看：執行期主頁同一天內的卡片順序，重整後再看同一畫面，並用 `GET /albums` 讀回順序
    - 期望：拖放當下與重整後都依新順序顯示
- [ ] `/tdd-e2e-green` — US-3:
  - 實作計畫：
    - 確認 DnD 送出的 `group_date`＋完整 `album_ids` 與後端寫入一致
    - 重載路徑不吃過期 Mock；畫面順序對齊 DB `sort_order`
    - 本則不驗證：只有一本時的拖放
- [ ] `/tdd-e2e-refactor` — US-3:
  - 整理範圍：
    - 在綠燈下整理 reorder 串接與重載流程
    - 不准擴到只有一本時的拖放

---

### US-4 在相簿內以平鋪方式預覽照片（優先級：P3）

#### AC / Edge

- spec US-4 獨立驗證：打開相簿以平鋪預覽照片，不是單張翻頁或巢狀列表

#### US-4 打開相簿以平鋪預覽照片

- [ ] `/tdd-e2e-red` — US-4 打開相簿以平鋪預覽照片:
  - 受測行為：
    - 前置：「旅行」內已有多張照片
    - 打：相簿詳情的平鋪區
    - 看：執行期相簿詳情的平鋪區，並用 `GET /albums/:albumId/photos` 讀回照片列表
    - 期望：照片以平鋪式介面顯示，不是單張翻頁或巢狀列表
- [ ] `/tdd-e2e-green` — US-4:
  - 實作計畫：
    - 確認詳情平鋪吃真 `GET /albums/:albumId/photos`；畫面張數與 API 列表一致
    - 必要時修 `/media` proxy 與縮圖載入，不另開平行契約
    - 本則不驗證：空狀態文案
- [ ] `/tdd-e2e-refactor` — US-4:
  - 整理範圍：
    - 在綠燈下整理詳情平鋪的串接
    - 不准擴到空狀態文案

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor |
| ---------- | -------- | --- | ----- | -------- |
| US-1       | US-1     | ⬜   | ⬜     | ⬜        |
| US-2       | US-2     | ⬜   | ⬜     | ⬜        |
| US-3       | US-3     | ⬜   | ⬜     | ⬜        |
| US-4       | US-4     | ⬜   | ⬜     | ⬜        |

---

## 5. 假設

- 區塊 ID 用 `US-n`，對齊 e2e `## 整合`；不是把 S-1-2、S-3-2 再抄一遍
- 整合不要預期 TDD Red；邊界（不支援格式、只有一本不能拖、禁止巢狀）留在切片
- 若前後端對應 US 尚未 Green，先補齊再跑本檔
- 一則 US 驗收一個區塊；區塊內 Red → Green → Refactor。Refactor 只整理這一則剛綠的接線，不准擴到本則不驗證；由同一輪 implement 做完
