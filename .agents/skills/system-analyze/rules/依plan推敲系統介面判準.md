# Rule 1 - 必須從 plan.md 推敲本次介面，不加專用欄位

- Level: `MUST`
- 本次要跑哪些系統介面，必須由同 package 的 `plan.md` 推敲（必要時對照 `technical-research.md`），**不可**新增「交付範圍」或等價專用欄位當契約。
- 推敲線索至少包含：技術選型概述、Language／Dependencies、Project Type、專案結構（有無 `backend/`／`frontend/`）、Storage、Constraints／選型中的否定句（例如「本期不做 Web UI」）。
- 硬停對話必須列出「即將執行的介面清單」，讓使用者在回「繼續」前有機會改口。

## Good Example

- 這個例子是好的，因為用既有欄位與否定句收斂介面，並在硬停時明示清單。

```md
plan 線索：Dependencies 有 Backend＋Frontend；結構有 backend/ 與 frontend/；Storage 有 SQLite
即將執行：data-plan、api-plan、ui-plan
```

## Bad Example

- 這個例子是壞的，因為要求新增欄位才敢委派。

```md
plan 沒有「交付範圍」三欄，無法判斷要不要跑 ui-plan，直接三介面全跑。
```

# Rule 2 - Data 幾乎常駐；api／ui 依 plan 選填

- Level: `MUST`
- 預設必須委派 `/data-plan`。僅當 `plan.md`／research **明確**表示本期無持久化、或不變更資料模型時，才可跳過 data-plan。
- `/api-plan`：僅當 plan 顯示有後端／HTTP API／`backend/` 等交付時委派；否則跳過。
- `/ui-plan`：僅當 plan 顯示有 Web UI／Frontend／`frontend/` 等交付時委派；否則跳過。
- 有跑的介面仍依序：data → api → ui（跳過者不產檔、不列入齊全檢查）。

## Good Example

- 這個例子是好的，因為後端 API-only 時跳過 ui，且仍跑 data。

```md
plan：僅 backend/、無 frontend/、選型概述寫明本期不做 Web UI、Storage 有 SQLite
委派：data-plan、api-plan；跳過 ui-plan
```

## Bad Example

- 這個例子是壞的，因為在明確無 UI 時仍強制跑 ui-plan。

```md
Constraints 已寫「本期不做前端」，仍委派 ui-plan 以求五檔齊全。
```

# Rule 3 - 齊全檢查只涵蓋本次必跑產物

- Level: `MUST`
- 完成條件：`technical-research.md` 與 `plan.md` 必有；外加本次推敲結果中「必跑」的介面檔。
- 不可再要求「無論 plan 為何，data／api／ui 三檔都必須存在」才結束。
- 若重產上游，必須依序重跑其後仍屬本次集合的下游。

## Good Example

- 這個例子是好的，因為 API-only 套件在缺 `ui-plan.md` 時仍可結束。

```md
必跑：research、plan、data-plan、api-plan
缺 ui-plan.md → 仍可結束（本次未選 UI）
```

## Bad Example

- 這個例子是壞的，因為用舊的五檔齊全標準卡住按需流程。

```md
缺 ui-plan.md → 強制回到 Phase 補產，即使 plan 寫明無前端。
```
