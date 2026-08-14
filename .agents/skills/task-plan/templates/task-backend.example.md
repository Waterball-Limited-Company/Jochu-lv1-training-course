# 實作計畫（後端）：照片相簿整理應用程式

**功能分支**: `001-photo-albums`  
**建立日期**: 2026-07-27  
**狀態**: 草稿

---

## 1. 規格閱讀

- [ ] 已讀 `plan.md`（Node 20、`backend/` 結構、`node:test`）
- [ ] 已讀 `technical-research.md`（Express／SQLite／multer／sharp）
- [ ] 已讀 `DDL.md`（`albums` → `photos`、外鍵、`PRAGMA foreign_keys`）
- [ ] 已讀 `api-plan.md`（`/api` 前綴、狀態碼與形狀）
- [ ] 已讀 `e2e-test-plan.md` 的 `## 後端`
- [ ] 確認後端 Scenario 無 blocked 項

```bash
ls specs/001-photo-albums/plan.md \
   specs/001-photo-albums/system-analyze/technical-research.md \
   specs/001-photo-albums/system-analyze/DDL.md \
   specs/001-photo-albums/system-analyze/api-plan.md \
   specs/001-photo-albums/e2e-test-plan.md
```

---

## 2. 環境建立

### 2.1 工具與目錄

- [ ] 確認本機 Node 為 20.x LTS

```bash
node -v
```

- [ ] 建立 `backend/` 骨架（對齊 `plan.md`：`src/`、`db/`、`data/`、`tests/`；業務路由可先空，app 須可被 import）

```bash
mkdir -p backend/src/db backend/db backend/data/uploads backend/data/thumbs \
  backend/tests/helpers backend/tests/fixtures
ls -ld backend backend/src backend/db backend/tests
```

- [ ] 設定 `.gitignore`（至少忽略 `node_modules/`、`data/`、`.env`）

### 2.2 套件與腳本

- [ ] 初始化 `backend` 為 ESM，安裝 runtime／測試依賴（對齊 plan：express、multer、better-sqlite3、sharp；測試用 node:test + 請求客戶端）
- [ ] `package.json` 的 `type` 為 `module`；`npm test` 指向 `node --test`

```bash
cd backend
npm pkg get type
npm pkg get scripts.test
```

### 2.3 Schema 與環境變數

- [ ] 將 `DDL.md` SQL 落到 `backend/db/schema.sql`（含 `albums`、`photos`）
- [ ] 提供 `.env.example`（埠、DB 路徑、uploads／thumbs；測試路徑由 helper 覆寫為暫存目錄）

```bash
grep -n "CREATE TABLE albums" backend/db/schema.sql
grep -n "CREATE TABLE photos" backend/db/schema.sql
```

### 2.4 測試基建

- [ ] 準備測試用影像 fixture（JPEG／PNG／WebP＋至少一個不支援檔）
- [ ] 準備測試 helper：可 import app、可重置暫存 DB 並套用 schema、API 一律走 `/api`
- [ ] 撰寫最小 smoke：證明 app 可載入（不斷言業務行為）
- [ ] 本節不可做出建立「旅行」或上傳照片

```bash
cd backend
npm test
```

---

## 3. User Story 實作計劃

### US-1 建立相簿並整理照片（優先級：P1）

#### AC / Edge

- AC-1-1 假設使用者尚未建立任何相簿，當建立一個名為「旅行」的相簿並一次匯入多張 JPEG、PNG 與 WebP 照片，則系統應顯示「旅行」相簿且內含這些照片（本層拆成 S-1-1 建立、S-1-6 匯入）
- AC-1-2 假設使用者已建立多個相簿且某張照片已屬於相簿 A，當使用者將該照片加入相簿 B，則該照片應只出現在相簿 B，且不再出現在相簿 A
- Edge-G-2 當系統偵測到會造成同一張照片同時屬於多個相簿的操作時，必須改為將該照片移動到目標相簿，不得保留多重歸屬
- Edge-1-1 當使用者建立空相簿但尚未加入照片時，系統仍應顯示該相簿
- Edge-1-2 當使用者選取不支援的檔案格式時，系統應拒絕匯入並說明僅支援 JPEG、PNG、WebP
- Edge-G-1 當使用者嘗試以任何操作把相簿放進另一個相簿中時，系統必須阻止此行為

#### S-1-1 建立名為「旅行」的相簿

- [ ] `/tdd-e2e-red` — S-1-1 建立名為「旅行」的相簿:
  - 受測行為：
    - 前置：尚未有任何相簿
    - 打：`POST /api/albums`
    - 看：`POST /albums` 的回應，再讀 `GET /albums`。不要直接查資料表
    - 期望：「旅行」相簿存在（建立 201；列表看得到「旅行」）
    - 還沒做時：建立後列表看不到「旅行」
- [ ] `/tdd-e2e-green` — S-1-1:
  - 實作計畫：
    - 落地 `POST /albums`：寫入 `albums`、`name` 驗證；`GET /albums` 足以看到「旅行」
    - 本則不驗證：批次匯入、日期分組、拖放
- [ ] `/tdd-e2e-refactor` — S-1-1:
  - 整理範圍：
    - 在綠燈下整理 `POST /albums` 與列表讀回的命名／去重
    - 不准擴到批次匯入、日期分組、拖放

#### S-1-6 一次將 JPEG、PNG 與 WebP 加入「旅行」相簿

- [ ] `/tdd-e2e-red` — S-1-6 一次將 JPEG、PNG 與 WebP 加入「旅行」相簿:
  - 受測行為：
    - 前置：已有空的「旅行」相簿；本機有 JPEG、PNG、WebP 各至少一張
    - 打：`POST /api/albums/:albumId/photos`
    - 看：`POST /albums/:albumId/photos` 的回應，再讀 `GET /albums/:albumId/photos`
    - 期望：該相簿內含剛加入的那些照片（上傳 201）
    - 還沒做時：上傳後「旅行」裡看不到剛加入的 JPEG、PNG、WebP
- [ ] `/tdd-e2e-green` — S-1-6:
  - 實作計畫：
    - 落地 `POST /albums/:albumId/photos`：multer 收多檔、MIME 限 JPEG／PNG／WebP、原檔進 uploads、sharp 縮圖、列寫入 `photos.album_id`
    - 本則不驗證：建立相簿、不支援格式拒絕、跨相簿移動
- [ ] `/tdd-e2e-refactor` — S-1-6:
  - 整理範圍：
    - 在綠燈下整理上傳路徑、MIME 檢查與縮圖組裝
    - 不准擴到建立相簿、不支援格式拒絕、跨相簿移動

#### S-1-2 將已歸屬照片改加入另一相簿後只留在目標相簿

- [ ] `/tdd-e2e-red` — S-1-2 將已歸屬照片改加入另一相簿後只留在目標相簿:
  - 受測行為：
    - 前置：已有「旅行」與「家庭」；要移動的那張照片目前在「旅行」
    - 打：`PATCH /api/photos/:id`
    - 看：`PATCH /photos/:id` 的回應，再分別讀「旅行」與「家庭」的照片列表
    - 期望：該張只在「家庭」、不在「旅行」（200，`album_id` 為家庭）
    - 還沒做時：移動後該張仍在「旅行」，或「家庭」看不到該張
- [ ] `/tdd-e2e-green` — S-1-2:
  - 實作計畫：
    - 落地 `PATCH /photos/:id`：`UPDATE` 覆寫 `album_id`（1:N 移動）
    - 本則不驗證：上傳、拖放、空狀態文案
- [ ] `/tdd-e2e-refactor` — S-1-2:
  - 整理範圍：
    - 在綠燈下整理覆寫歸屬的資料存取
    - 不准擴到上傳、拖放、空狀態文案

#### S-1-3 空相簿尚未加入照片時仍應顯示

- [ ] `/tdd-e2e-red` — S-1-3 空相簿尚未加入照片時仍應顯示:
  - 受測行為：
    - 前置：尚未有任何相簿
    - 打：`POST /api/albums`（建立空的「草稿」，未上傳任何照片）
    - 看：`GET /albums` 的列表是否含「草稿」
    - 期望：「草稿」相簿仍被顯示（`photo_count` 可為 0）
    - 還沒做時：未上傳照片時列表看不到「草稿」
- [ ] `/tdd-e2e-green` — S-1-3:
  - 實作計畫：
    - 確認空相簿仍出現在 `GET /albums`；必要時補 `photo_count` 為 0
    - 本則不驗證：匯入、名稱必須是「旅行」
- [ ] `/tdd-e2e-refactor` — S-1-3:
  - 整理範圍：
    - 在綠燈下整理空相簿列表與 `photo_count`
    - 不准擴到匯入、名稱必須是「旅行」

#### S-1-4 選取不支援格式時拒絕匯入並說明支援範圍

- [ ] `/tdd-e2e-red` — S-1-4 選取不支援格式時拒絕匯入並說明支援範圍:
  - 受測行為：
    - 前置：已有空的「旅行」相簿；本機有至少一個不支援的檔（例如 HEIC）
    - 打：`POST /api/albums/:albumId/photos`
    - 看：`POST /albums/:albumId/photos` 的錯誤回應與說明
    - 期望：系統拒絕匯入
    - 文案：僅支援 JPEG、PNG、WebP（415 或 api-plan 等價；`error.message`／`details`）
    - 還沒做時：檔案被收下，或錯誤沒說僅支援 JPEG、PNG、WebP
- [ ] `/tdd-e2e-green` — S-1-4:
  - 實作計畫：
    - 不支援格式回 415＋共通錯誤形狀；相簿照片張數不變；路徑一律 `/api`
    - 本則不驗證：成功上傳、跨相簿移動
- [ ] `/tdd-e2e-refactor` — S-1-4:
  - 整理範圍：
    - 在綠燈下整理 415 錯誤形狀
    - 不准擴到成功上傳、跨相簿移動

#### S-1-5 拒絕相簿巢狀並維持單層

- [ ] `/tdd-e2e-red` — S-1-5 拒絕相簿巢狀並維持單層:
  - 受測行為：
    - 前置：已有「旅行」「家庭」「工作」
    - 打：`POST /api/albums`
    - 看：`POST /albums` 不得帶父相簿；`GET /albums` 仍是單層
    - 期望：所有相簿仍維持單層
    - 還沒做時：能建立子相簿
- [ ] `/tdd-e2e-green` — S-1-5:
  - 實作計畫：
    - `POST /albums` 不提供巢狀欄位（帶了則忽略或 400）；`GET /albums` 回扁平 `groups[].albums[]`
    - 本則不驗證：拖放組內排序
- [ ] `/tdd-e2e-refactor` — S-1-5:
  - 整理範圍：
    - 在綠燈下整理單層契約（忽略／拒絕巢狀欄位）
    - 不准擴到拖放組內排序

---

### US-2 在主頁面依日期瀏覽相簿（優先級：P2）

#### AC / Edge

- AC-2-1 假設使用者已在不同日期建立多個相簿，當使用者進入主頁面，則系統應依各相簿的建立日期將相簿分組顯示
- Edge-2-1 當某個日期分組下沒有任何相簿時，系統不應顯示空白日期分組

#### S-2-1 主頁依相簿建立日期分組顯示

- [ ] `/tdd-e2e-red` — S-2-1 主頁依相簿建立日期分組顯示:
  - 受測行為：
    - 前置：「旅行」「家庭」建於 2026-07-11；「工作」建於 2026-07-20。旅行 5 張、家庭 0 張、工作 12 張
    - 打：`GET /api/albums`
    - 看：`GET /albums` 回傳的日期分組
    - 期望：依各相簿的建立日期將相簿分組顯示（200；`groups[]` 依 `group_date`）
    - 還沒做時：「旅行／家庭」與「工作」沒有依 2026-07-11、2026-07-20 分開
- [ ] `/tdd-e2e-green` — S-2-1:
  - 實作計畫：
    - 完善 `GET /albums`：由 `created_at` 衍生 `group_date`，組裝 `groups[]`；組內依 `sort_order` 升冪；`photo_count` 查詢衍生不落庫
    - 本則不驗證：組內拖放、空白分組
- [ ] `/tdd-e2e-refactor` — S-2-1:
  - 整理範圍：
    - 在綠燈下整理分組組裝與 `photo_count` 查詢
    - 不准擴到組內拖放、空白分組

#### S-2-2 沒有相簿的日期不顯示空白分組

- [ ] `/tdd-e2e-red` — S-2-2 沒有相簿的日期不顯示空白分組:
  - 受測行為：
    - 前置：只有 2026-07-11、2026-07-20 有相簿；例如 2026-07-15 沒有
    - 打：`GET /api/albums`
    - 看：`GET /albums` 的分組列表（不可出現沒有相簿的日期）
    - 期望：不顯示那些沒有相簿的空白日期分組
    - 還沒做時：出現沒有相簿的日期分組
- [ ] `/tdd-e2e-green` — S-2-2:
  - 實作計畫：
    - 不輸出空日期分組；無相簿時可回空 `groups`；家庭 0 張仍留在 2026-07-11
    - 本則不驗證：組內順序
- [ ] `/tdd-e2e-refactor` — S-2-2:
  - 整理範圍：
    - 在綠燈下整理空白分組過濾
    - 不准改組內順序

---

### US-3 透過拖放重新排列相簿（優先級：P3）

#### AC / Edge

- AC-3-2 假設使用者已完成一次相簿拖放排序，當使用者重新整理或再次進入主頁面，則系統應仍依先前保存的順序顯示相簿

#### S-3-2 拖放排序後重新整理或再進主頁仍保留順序

- [ ] `/tdd-e2e-red` — S-3-2 拖放排序後重新整理或再進主頁仍保留順序:
  - 受測行為：
    - 前置：2026-07-11 原本旅行在前、家庭在後；已重排成家庭在前、旅行在後。「工作」仍在 2026-07-20
    - 打：`PATCH /api/albums/reorder`
    - 看：`PATCH /albums/reorder` 之後再讀 `GET /albums`
    - 期望：再讀列表時組內順序與重排一致（200）
    - 還沒做時：再讀列表時，2026-07-11 仍是旅行在前
- [ ] `/tdd-e2e-green` — S-3-2:
  - 實作計畫：
    - 落地 `PATCH /albums/reorder`：僅允許同分組；寫回各 album `sort_order`（0 起）；跨組／遺漏 ID 依 api-plan 回 400／404
    - 本則不驗證：畫面是否立刻重排；跨組拖放
- [ ] `/tdd-e2e-refactor` — S-3-2:
  - 整理範圍：
    - 在綠燈下整理 reorder 寫入與列表讀回
    - 不准擴到畫面立刻重排、跨組拖放

---

### US-4 在相簿內以平鋪方式預覽照片（優先級：P3）

#### AC / Edge

- AC-4-1 假設某個相簿內已有多張照片，當使用者打開該相簿，則系統應以平鋪式預覽顯示相簿中的照片
- Edge-4-1 當相簿內尚無照片時，系統應顯示可理解的空狀態，而不是空白畫面

#### S-4-1 打開含多張照片的相簿以平鋪預覽顯示

- [ ] `/tdd-e2e-red` — S-4-1 打開含多張照片的相簿以平鋪預覽顯示:
  - 受測行為：
    - 前置：「旅行」內已有多張照片
    - 打：`GET /api/albums/:albumId/photos`
    - 看：`GET /albums/:albumId/photos` 的照片列表與預覽網址
    - 期望：回傳「旅行」的多筆照片（含預覽網址；200；排序依 `created_at` 升冪）
    - 還沒做時：「旅行」照片列表是空的，或缺少預覽網址
- [ ] `/tdd-e2e-green` — S-4-1:
  - 實作計畫：
    - 完善 `GET /albums/:albumId/photos`：依 `album_id` 查詢、`created_at` 升冪、組裝 `/media/` URL；縮圖失敗時 `thumbnail_url` 可 null
    - 本則不驗證：空狀態文案、上傳
- [ ] `/tdd-e2e-refactor` — S-4-1:
  - 整理範圍：
    - 在綠燈下整理照片列表與媒體 URL 組裝
    - 不准擴到空狀態文案、上傳

#### S-4-2 空相簿打開時顯示可理解的空狀態

- [ ] `/tdd-e2e-red` — S-4-2 空相簿打開時顯示可理解的空狀態:
  - 受測行為：
    - 前置：已有空的「家庭」相簿
    - 打：`GET /api/albums/:albumId/photos`
    - 看：`GET /albums/:albumId/photos` 的空列表（請求仍成功）
    - 期望：空相簿回成功與空列表
    - 還沒做時：打開空相簿失敗，或回了非空照片列
- [ ] `/tdd-e2e-green` — S-4-2:
  - 實作計畫：
    - 空相簿不 404（相簿存在時），回空陣列
    - 本則不驗證：畫面上的空狀態用字
- [ ] `/tdd-e2e-refactor` — S-4-2:
  - 整理範圍：
    - 在綠燈下整理空列表成功態
    - 不准改畫面上的空狀態用字

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor |
| ---------- | -------- | --- | ----- | -------- |
| US-1       | S-1-1    | ⬜   | ⬜     | ⬜        |
| US-1       | S-1-6    | ⬜   | ⬜     | ⬜        |
| US-1       | S-1-2    | ⬜   | ⬜     | ⬜        |
| US-1       | S-1-3    | ⬜   | ⬜     | ⬜        |
| US-1       | S-1-4    | ⬜   | ⬜     | ⬜        |
| US-1       | S-1-5    | ⬜   | ⬜     | ⬜        |
| US-2       | S-2-1    | ⬜   | ⬜     | ⬜        |
| US-2       | S-2-2    | ⬜   | ⬜     | ⬜        |
| US-3       | S-3-2    | ⬜   | ⬜     | ⬜        |
| US-4       | S-4-1    | ⬜   | ⬜     | ⬜        |
| US-4       | S-4-2    | ⬜   | ⬜     | ⬜        |

---

## 5. 假設

- S-3-1、S-3-3 僅前端落地，本檔不列
- 一則 Scenario 一個區塊；區塊內 Red → Green → Refactor。Refactor 只整理這一則剛綠的碼，不准擴到下一則；由同一輪 implement 做完，不為第三格新開讀規格的呼叫
- 斷言走 API 觀測通道，不要直接查資料表
