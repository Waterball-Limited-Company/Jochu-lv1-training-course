# Rule 1 - Inventory 只抽穩定 ID 與短摘要

- Level: `MUST`
- 建立 inventory 時，每筆只保留：穩定 key（優先使用檔內既有 ID）、一句短摘要、來源檔相對路徑。
- 不可把整份規格原文複製進報告或當成比對本體；比對對象是 inventory，不是全文 dump。
- 不另存獨立 inventory 檔；inventory 僅供本輪偵測與填入報告矩陣使用。

## Good Example

- 這個例子是好的，因為條目短、可對齊、可重跑。

```text
US1-FR1 | 可建立並命名相簿 | spec.md
AC-1-1 | 建旅行相簿並匯入多格式 | spec.md / e2e 對應
POST /albums | 建立相簿 | api-plan.md
S-1-1 | 後端 Scenario | e2e-test-plan.md
```

## Bad Example

- 這個例子是壞的，因為把整段 AC 原文貼進 inventory，失去索引用途。

```text
把 AC-1-1 完整段落與前後文一起貼進清單再全文語意比對
```

# Rule 2 - 各產物應抽取的 key 類型固定

- Level: `MUST`
- 依實際存在的產物抽取：
  - `spec.md`：US、`USn-FRm`、AC／Edge、`GR-xxx`、關鍵實體名稱（若有）
  - `api-plan.md`：HTTP method＋path、對應 FR／US（若有追溯表）
  - `ui-plan.md`：頁面／業務邏輯 ID 或穩定標題、對應 US／FR（若有）
  - `data-plan.md`／`DDL.md`：實體名稱、關鍵欄位／約束名稱（足以做跨層對齊）
  - `e2e-test-plan.md`：Scenario ID（如 `S-1-1`）、對應欄位中的 US／AC／Edge／FR／API／UI、測試摘要總表列
  - `task-plan/*`：與 Scenario／US／AC／Edge 可對齊的章節或步驟標識（依各檔既有標題／編號）
- 某類產物不存在時，跳過該類抽取，不虛構 key。

## Good Example

- 這個例子是好的，因為 key 來源清楚且可互相對表。

```text
spec：US1-FR4
api：PATCH /photos/:id → US1-FR4
e2e：S-1-2 → AC-1-2、US1-FR4、PATCH /photos/:id
```

## Bad Example

- 這個例子是壞的，因為用自由描述當 key，無法穩定對齊。

```text
「移動照片那個功能」↔「改歸屬 API」↔「第二個測試」
```

# Rule 3 - 優先信任檔內既有追溯，再補缺口

- Level: `SHOULD`
- 若產物已有追溯總表或對應欄位（例如 api 追溯總表、e2e 對應欄位、測試摘要總表），應先據此建立映射，再檢查「表內引用是否真實存在於目標 inventory」。
- 不可忽略既有追溯、全部改用關鍵字模糊猜測。

## Good Example

- 這個例子是好的，因為先吃 e2e 對應欄位，再驗證 API 是否真的在 api-plan。

```text
S-1-1 對應欄位列 POST /albums → 確認 api-plan 有此 endpoint
```

## Bad Example

- 這個例子是壞的，因為丟棄對應欄位，只用詞彙相似度硬配。

```text
忽略對應欄位，憑「相簿」兩字把任意 API 配到任意 Scenario
```
