---
name: constitution
description: 建立或修訂 `.constitution/` 下的開發規範（憲法）：先讓使用者選擇 core 與／或各交付 skill 憲法，再依類型寫入 front matter 與約定章節，並更新版本與最後修訂；不同步修改其他 skill 或 templates。Use when the user invokes /constitution, asks to create or update the project constitution / 開發規範, or needs to amend project-wide or skill-scoped development constraints.
disable-model-invocation: true
---

# Constitution

建立或修訂 `.constitution/` 內的憲法產物：`core.md`（跨 skill）與／或 `<skill-name>.md`（面向技術約束）。本 skill 只維護這些檔，修訂時不同步改其他 skill 或 templates。交付 skill 如何讀取憲法見 `rules/交付skill讀取憲法判準.md`（由各交付 skill 自行掛接）。

# SOP

## Phase 1 -- 收斂寫入目標並判定新建或修訂

1. WRITE 向使用者列出可建立／修訂的憲法目標並請其多選：第一個選項永遠是 `core`，其餘為交付 skill 名（至少包含 analyze、api-plan、data-plan、e2e-test-plan、implement、ooa-plan、specify、system-analyze、task-plan、technical-research、tdd-e2e-green、tdd-e2e-red、tdd-e2e-refactor、ui-plan）；未獲選擇前停止。
2. READ 讀取使用者需求，以及每個已選目標對應的既有檔（若存在）：`.constitution/core.md` 或 `.constitution/<skill-name>.md`。
3. READ 讀取 `rules/產物路徑與改動邊界.md`，確認輸出路徑、front matter、建立／修訂邊界、完成條件。
4. THINK 依本次已載入規則，為每個目標判定「新建」或「修訂」，並整理待寫入的變更意圖與 metadata 預期。

## Phase 2 -- 先處理高影響缺口

1. READ 讀取 `rules/內容邊界與版本判準.md`，確認 core／skill 各自可寫入章節、抽象層級與版本升降規則。
2. THINK 依本次已載入規則盤點會改變原則／技術基線／效力的高影響缺口。
3. DELEGATE 若高影響缺口應先拍板，呼叫 `/clarify`；未獲回答前停止後續寫入。

## Phase 3 -- 依目標寫入 `.constitution/`

1. READ 若目標含 `core`：讀取 `templates/constitution.md` 與 `templates/constitution.example.md`。若目標含 skill 憲法：讀取 `templates/constitution-skill.md` 與 `templates/constitution-skill.example.md`。
2. WRITE 依骨架與已收斂內容，將每個目標寫入對應路徑（新建則建立完整初稿；修訂則更新對應章節、front matter 與 metadata）。

## Phase 4 -- 驗證並交付

1. READ 回頭檢查每個已寫入檔是否符合本次已載入規則：路徑在 `.constitution/`、front matter 齊全、章節契約正確、內容不越界、版本／最後修訂已依規則更新、未同步改動其他 skill／templates；若不符合，立即修正。
2. WRITE 向使用者交付路徑清單與本次變更摘要（各目標為新建或修訂、版本變更）。
