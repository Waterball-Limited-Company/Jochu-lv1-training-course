# Rule 1 - 各層必讀集合以 Scenario 與層別為準

- Level: `MUST`
- 每次都必須載入該 Scenario 在 `specs/<plan-package>/e2e-test-plan.md` 的區塊（Gherkin＋對應欄位）。
- 另依 `layer` 從 `specs/<plan-package>/system-analyze/` 載入 SA 片段：
  - `backend`：`api-plan.md`、`DDL.md`、`data-plan.md`
  - `frontend`：`ui-plan.md`、`data-plan.md`；寫 Mock 時另加 `api-plan.md`
  - `integration`：`ui-plan.md`、`api-plan.md`、`data-plan.md`（不含 `DDL.md`）
- 不得載入：`technical-research.md`、`spec.md`、`plan.md`、整份 `task-*.md`（實作計畫已由 prompt 帶入）。

## Good Example

- 這個例子是好的，因為後端 Red 只開 e2e 該 Scenario 與點名到的 api／DDL／data 片段，且路徑在 `system-analyze/`。

```text
layer=backend, plan-package=001-photo-albums, S-1-1
→ specs/001-photo-albums/e2e-test-plan.md 的 S-1-1 區塊
→ specs/.../system-analyze/api-plan.md 的 POST /albums、POST .../photos、GET ...
→ 同目錄 DDL.md／data-plan.md 中 albums、photos 相關片段
```

## Bad Example

- 這個例子是壞的，因為順便整份重讀 spec 與 technical-research。

```text
每次 Red 先讀完 spec.md + technical-research.md + 整份 api-plan.md
```

# Rule 2 - 只讀實作計畫點名的介面元素，需要再補相關契約

- Level: `MUST`
- 對 SA 檔不得整檔通讀；只讀實作計畫（與 e2e 對應欄位）點名到的 endpoint、頁面、實體或其他介面元素。
- 寫測時若斷言仍缺形狀／欄位／狀態碼等細節，可再手術式補讀**相關**契約片段；不可借機通讀無關章節。

## Good Example

- 這個例子是好的，因為先讀點名 endpoint，缺 response 形狀再補該 endpoint 章節。

```text
實作計畫點名 PATCH /photos/:id
→ 只開 api-plan 該 endpoint
→ 需要 body 範例時再讀同一 endpoint 的請求／回應區塊
```

## Bad Example

- 這個例子是壞的，因為「需要契約」變成整份 api-plan 從頭讀到尾。

```text
點名一個 endpoint，卻把 api-plan 全檔載入
```

# Rule 3 - 行為以 Gherkin 為準，實作計畫負責落點

- Level: `MUST`
- 測試的 Given／When／Then 行為必須對齊該 Scenario 的 Gherkin。
- 實作計畫只導航如何打 API／操作 UI／使用 Mock 等落點，不得覆蓋或改寫 Gherkin 的驗收語意。
- 若兩者明顯矛盾，必須停止並回報 implement，不可默默選邊繼續寫測。

## Good Example

- 這個例子是好的，因為 Then 跟 Gherkin，路徑跟實作計畫。

```text
Gherkin Then：照片只在相簿 B
實作計畫：PATCH 後分別 GET A／B 的 photos
→ 斷言對齊 Then；呼叫方式對齊實作計畫
```

## Bad Example

- 這個例子是壞的，因為實作計畫少寫一步就省略 Gherkin 的關鍵 Then。

```text
Gherkin 要求「不再出現在 A」，實作計畫只寫 PATCH 200
→ 測試只 assert 200，不管 A 是否仍有該照片
```
