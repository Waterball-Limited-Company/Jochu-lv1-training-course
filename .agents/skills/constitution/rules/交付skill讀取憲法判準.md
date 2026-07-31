# Rule 1 - 交付 skill 進場必須依 lazy load 讀取適用憲法

- Level: `MUST`
- 凡約定遵守本判準的交付 skill，在其 Phase 1（或第一個成果 phase）開頭 MUST 先讀取本 RuleFile。
- 若存在 `.constitution/core.md`，MUST 讀取該檔全文（core 為跨 skill 基線，不可跳過）。
- 若存在 `.constitution/<本 skill 的 name>.md`（`<name>` 與本 skill 目錄／front matter `name` 對齊，例如 `api-plan`），MUST 讀取該檔全文。
- 兩檔皆不存在時，不視為錯誤；依 Rule 2 警告後繼續。
- 不可再尋找或要求專案根目錄單檔 `constitution.md`。
- 不可為了「省事」而略過已存在的 core，也不可在未宣告適用時去讀與本 skill 無關的其他 skill 憲法（analyze 等比對角色除外，見該 skill 自身規則）。

## Good Example

- 這個例子是好的，因為先讀判準，再 lazy load core 與自身面向檔。

```text
READ `.agents/skills/constitution/` 內「交付skill讀取憲法判準.md」
READ `.constitution/core.md`（若存在）
READ `.constitution/api-plan.md`（本 skill 為 api-plan 且檔案存在）
→ 再繼續本 skill 其餘 Phase 1 步驟
```

## Bad Example

- 這個例子是壞的，因為讀已淘汰的根單檔，或完全不讀憲法。

```text
READ 專案根 constitution.md
直接讀 spec／templates，從未開啟 .constitution/
```

# Rule 2 - 缺檔時警告後繼續，不得因缺憲法而強制中止

- Level: `MUST`
- 若 `.constitution/core.md` 不存在，交付 skill MUST 留下可察覺警告（例如「未找到 `.constitution/core.md`，依本 skill 預設繼續」），然後**繼續**執行。
- 若 `.constitution/<本 skill name>.md` 不存在，MAY 省略專用警告；不得因缺面向檔而停止。
- 缺檔時退回該 skill 原有預設規則與產物契約；不自行發明一份臨時憲法。
- 本規則不適用於 `/constitution`（寫入方）：對選定目標缺檔時應新建，見 `產物路徑與改動邊界.md`。

## Good Example

- 這個例子是好的，因為缺 core 仍可完成交付，且有警告。

```text
警告：未找到 .constitution/core.md，本輪依 api-plan 預設規則繼續。
→ 繼續產出 api-plan.md
```

## Bad Example

- 這個例子是壞的，因為把缺憲法當成硬閘門。

```text
未找到 .constitution/core.md，停止 /implement，請先執行 /constitution
```

# Rule 3 - 有憲法時衝突以憲法為準

- Level: `MUST`
- 當本次已讀取之憲法檔（core 與／或自身 skill 憲法）存在時，其 MUST 條文優先於該交付 skill 的預設慣例、樣板預設與「習慣寫法」。
- core 與自身 skill 憲法衝突時，以 core 為準。
- 若憲法與本 skill rules／templates 衝突，MUST 調整本次步驟、選型或產出以符合憲法，不得默默忽略。
- 不可為了遷就本次方便而改寫憲法內容（修憲屬 `/constitution` 或人工編輯）。

## Good Example

- 這個例子是好的，因為產出遷就憲法。

```text
skill 預設可引入 ORM；core 禁止 ORM
→ technical-research／實作不採用 ORM
```

## Bad Example

- 這個例子是壞的，因為明知違憲仍照 skill 預設產出。

```text
core 禁止前端 framework，仍在 research 選 React 且不標衝突
```

# Rule 4 - 只萃取與本 skill 相關的約束，但不得假裝沒讀到相干 MUST

- Level: `SHOULD`
- 各 skill 應依自身職責套用已讀憲法中的相關條文（例如 api-plan 偏 API 契約形狀；data-plan 偏資料表約束；implement 偏堆疊禁准）。
- 若某條 MUST 明明約束本 skill 的產出或行為，不得以「非我章節」為由忽略。
- 無相關條文時，不必改寫本 skill 的正常路徑。

## Good Example

- 這個例子是好的，因為有對焦又沒漏相干硬規則。

```text
ui-plan：套用 core 前端基線；不改寫與 UI 無關的 DB 稽核欄位細節
```

## Bad Example

- 這個例子是壞的，因為漏掉明顯相干的 MUST。

```text
implement 後端時忽略 core「不以 ORM 存取資料庫」
```
