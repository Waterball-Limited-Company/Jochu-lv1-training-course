# Rule 1 - 各層必讀集合以本則與層別為準；已有片段不重載

- Level: `MUST`
- 必須持有該則在 `specs/<plan-package>/e2e-test-plan.md` 的區塊（Gherkin＋對應欄位）；優先用 implement 帶入的片段。
- 另依 `layer` 從 `specs/<plan-package>/system-analyze/` 持有 SA 片段：
  - `backend`：`api-plan.md`、`DDL.md`、`data-plan.md`
  - `frontend`：`ui-plan.md`、`data-plan.md`；寫 Mock 時另加 `api-plan.md`
- 已持有的檔與區塊不得再整段重開。不得載入：`technical-research.md`、`spec.md`、`plan.md`、整份 `task-*.md`（受測行為已由 prompt 帶入）。

## Good Example

- 這個例子是好的，因為後端 Red 只用已帶的 e2e 該則與點名 api／DDL／data 片段。

```text
layer=backend, 本則=S-1-1
→ 使用已定位的 e2e S-1-1 區塊
→ 使用已定位的 POST /albums 契約與 albums 表片段
```

## Bad Example

- 這個例子是壞的，因為順便整份重讀 spec 與 technical-research。

```text
每次 Red 先讀完 spec.md + technical-research.md + 整份 api-plan.md
```

# Rule 2 - 只讀受測行為點名的介面元素；只走觀測通道

- Level: `MUST`
- 對 SA 檔不得整檔通讀；只讀受測行為（與 e2e 對應欄位）點名到的 endpoint、頁面、實體或其他介面元素。
- 測試必須只打「打」、只看「看」寫明的正式介面（執行期畫面或正式 API）。
- `backend` 必須由正式 API 進入真後端與可重設測試資料；不得直接呼叫內部 service 或直接查資料表取代端對端證據。
- `frontend` 必須使用 technical research／plan 已選定的瀏覽器端對端套件開啟執行期前端；API 只能在邊界依交接中的 `api-plan.md` 契約案例建立 Mock。jsdom 元件測試可補充，但不能充當本 Scenario 主證據。
- **禁止**把 `system-analyze/ui/*.html` 或其他雛形檔當受測物或測試入口。
- 寫測時若斷言仍缺形狀／欄位／狀態碼等細節，可再手術式補讀**相關**契約片段；不可借機通讀無關章節。

## Good Example

- 這個例子是好的，因為觀測通道是執行期主頁，不是雛形。

```text
看：執行期主頁（不是 ui/index.html）
→ 測試打開 Vite 執行期頁面，不斷言 system-analyze/ui/index.html
```

## Bad Example

- 這個例子是壞的，因為把雛形當受測物，或「需要契約」變成整份 api-plan。

```text
測試去讀 system-analyze/ui/index.html 有沒有「旅行」
點名一個 endpoint，卻把 api-plan 全檔載入
```

# Rule 3 - 行為以 Gherkin 為準，受測行為指定要驗證的期望

- Level: `MUST`
- 測試的 Given／When／Then 行為必須對齊該 Scenario 的 Gherkin。
- 受測行為只指定「要驗證什麼／期望什麼」，不指定測試手段；不得覆蓋或改寫 Gherkin 的驗收語意。
- 若兩者明顯矛盾，必須停止並回報 implement，不可默默選邊繼續寫測。

## Good Example

- 這個例子是好的，因為 Then 跟 Gherkin，期望跟受測行為。

```text
Gherkin Then：主頁顯示「旅行」
受測行為：期望主頁看得到「旅行」；還沒做時看不到「旅行」
→ 斷言對齊 Then 與受測行為期望
```

## Bad Example

- 這個例子是壞的，因為受測行為少寫一步就省略 Gherkin 的關鍵 Then。

```text
Gherkin 要求「不再出現在 A」，受測行為只寫「移動成功」
→ 測試只 assert 成功，不管 A 是否仍有該照片
```
