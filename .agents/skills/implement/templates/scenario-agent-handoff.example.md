# Scenario Agent 交接

scenario-agent-id: frontend-US-1-S-1-1
layer: frontend
plan-package: 001-photo-albums
user-story: US-1
scenario: S-1-1 建立名為「旅行」的相簿

## 執行順序

1. 讀取下列已定位片段，不重新擴張需求範圍。
2. 先跑同層、同 User Story 已完成 Scenario 的累積測試，確認進場基準為綠。
3. 執行 `/tdd-e2e-red`，保存正確紅燈證據。
4. 在同一代理脈絡執行 `/tdd-e2e-green`，只做最少 Green。
5. 在同一代理脈絡執行 `/tdd-e2e-refactor`，不得擴充需求。
6. 執行 User Story 層內全綠閘門與契約證據驗證。
7. 回報各階段狀態、命令、證據檔、變更檔與第一個未完成階段。

## 已定位片段

task:
- Red 由真實瀏覽器輸入「旅行」並送出。
- Green 只完成表單、API 呼叫與成功呈現。
- Refactor 只整理本則元件與 API 呼叫。
- 層內全綠命令：`npm run test:e2e:frontend -- --grep US-1`

e2e:
- S-1-1：頁面建立「旅行」後必須顯示相簿卡片。

system-analyze:
- UI 建立表單片段。
- `POST /albums` API 片段。

API 契約案例:
- API-001-C1

## 執行邊界

允許修改:
- `frontend/src/`
- `frontend/tests/`

禁止修改:
- `backend/`
- `specs/001-photo-albums/`

測試與證據命令:
- `npm run test:e2e:frontend -- --grep US-1`
- `uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence frontend/test-results/api-contract.json --user-story US-1 --scenario S-1-1 --contract-id API-001-C1 --require-source frontend-mock`

既有進度與證據:
- 尚未開始。
