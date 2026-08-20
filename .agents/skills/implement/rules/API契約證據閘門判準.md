# Rule 1 - api-plan 是三種證據的單一契約來源

- Level: `MUST`
- 流程版本 2 的前端 API Mock、後端契約測試與整合完全端對端證據，必須以 `system-analyze/api-plan.md` 的「可機械驗證契約」為準。
- 必要證據來源固定為 `backend-contract`、`frontend-mock`、`integration`；只有契約案例的 `required_evidence` 有列入，才列入該閘門分母。
- 人類閱讀表格與機械契約不一致時停止，先修 `api-plan.md`，不可讓三層各自維護另一份真相。

## Good Example

```text
API-001-C1 required_evidence 含 frontend-mock
→ 前端測試依同一 request／response schema 建 Mock 並產證據
```

## Bad Example

```text
前端手寫一份 fixtures，後端另抄一份欄位，兩份都不追 api-plan
```

# Rule 2 - 證據必須由測試執行產生

- Level: `MUST`
- 每份證據檔須記錄來源、實際有效且具時區的產生時間、產生它的測試命令與逐契約實際 request／response；時間可省略小數秒，也可使用 JavaScript `toISOString()` 產生的毫秒格式，但日期、時間與時區都必須實際有效。`source` 欄位負責宣告層別，測試命令本身只須能解析為可辨識的測試執行器，因此 `npm test`、`pnpm test`、`yarn test`、`bun test` 或 `python3 -m pytest` 可以合法使用，不強迫命令名稱重複層別。使用套件或環境包裝器時仍須略過 `--package` 等選項及其值，檢查真正執行的內層 payload；Playwright 必須實際執行 `playwright test`，Cypress 必須執行 `cypress run`，只跑 `--help`、`--version`、`--list` 或 `--collect-only` 不算證據。`npx echo`、`npx --package @playwright/test sh -c 'exit 0'`、`pnpm true`、`uv run printf`、命令串接與吞錯寫法一律拒絕。不得在測試跑完後手動補一份宣稱通過的 JSON。
- 每筆證據的 `scenario_id` 必須屬於契約的 `user_story`；User Story 閘門即使不帶 `--scenario`，也不能拿其他故事的測試紀錄頂替。
- 後端與前端證據的 `scenario_id` 固定使用 `S-n-m`；整合證據固定等於契約的 `US-n`，不得拿薄切片 Scenario 冒充 User Story 完全端對端驗收。
- 使用 `scripts/validate_api_contract_evidence.py` 驗證契約覆蓋、method、path、status 與 request／response schema。
- 每次閘門必須明列目前證據層的 `--require-source`：後端用 `backend-contract`、前端用 `frontend-mock`、整合用 `integration`；不得在後端階段要求尚未執行的前端或整合證據。
- 前端／後端 Scenario 閘門以本則全部 `--contract-id` 限縮；User Story 完成閘門與整合完全端對端閘門只用 `--user-story` 選取該故事全部契約，不得沿用單一 Scenario 的 `--scenario` 或 `--contract-id` 篩選而漏驗。
- 閘門命令失敗、缺證據或證據來源錯誤，都不得勾選。

## Good Example

```text
Playwright 測試執行 → reporter 寫 frontend-mock 證據 → 驗證程式比對 api-plan → 通過
```

## Bad Example

```text
測試沒輸出證據，開發者手動建立 {"passed": true}
```

# Rule 3 - 契約失敗先判定漂移方

- Level: `MUST`
- 前端或後端證據不符時，先以 `api-plan.md` 判定是實作／Mock 漂移，還是需求已變而契約尚未更新。
- 契約仍正確時修漂移的一側；需求真的改變時回到 `/api-plan` 更新契約，再重跑 `/analyze` 與受影響的 task 計畫。
- 不可為了讓整合全綠，同時任意改前端 Mock、後端 response 與斷言。

## Good Example

```text
api-plan 要求 201，後端回 200 → 修後端並重跑 backend-contract
```

## Bad Example

```text
後端回什麼就把前端 Mock 和測試一起改成什麼
```
