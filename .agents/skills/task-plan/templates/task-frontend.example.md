# 實作計畫（前端）：相簿管理

流程版本: 2
功能分支: `001-photo-albums`
建立日期: 2026-08-20
狀態: 草稿

---

## 1. 規格閱讀

- [ ] 讀取規格、API 契約、端對端測試計畫與前端系統分析

```bash
ls specs/001-photo-albums
```

---

## 2. 環境建立

- [ ] 建立 Playwright 瀏覽器測試與依 `api-plan.md` 回應的 API Mock

---

## 3. User Story 實作計劃

### US-1 建立相簿（優先級：P1）

#### AC / Edge

- 可輸入相簿名稱並送出
- 成功後畫面顯示新相簿

#### S-1-1 建立名為「旅行」的相簿

- [ ] `/tdd-e2e-red` — S-1-1 建立名為「旅行」的相簿:
  - 受測行為：
    - 前置：瀏覽器開啟相簿首頁，API Mock 依契約回應
    - 打：在真實頁面輸入「旅行」並按建立
    - 看：Playwright 觀測頁面與瀏覽器網路請求
    - 期望：頁面出現「旅行」，送出的 request 符合契約
    - 文案：建立相簿
    - 還沒做時：頁面沒有建立控制項，主斷言失敗
  - 契約案例：API-001-C1
- [ ] `/tdd-e2e-green` — S-1-1:
  - 實作計畫：
    - 完成建立表單、API 呼叫與成功畫面更新的最少行為
    - 本則不驗證：真實後端與資料庫接線
- [ ] `/tdd-e2e-refactor` — S-1-1:
  - 整理範圍：
    - 只整理本則新增的元件與 API 呼叫
    - 不准擴到其他 User Story
- [ ] `User Story 層內全綠閘門` — S-1-1:
  - 累積測試：`npm run test:e2e:frontend -- --grep US-1`
  - 契約證據：`uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence frontend/test-results/api-contract.json --user-story US-1 --scenario S-1-1 --contract-id API-001-C1 --require-source frontend-mock`
  - 完成：同層、同一 User Story 到目前 Scenario 的測試與契約證據全部通過

#### S-1-2 顯示缺少名稱錯誤

- [ ] `/tdd-e2e-red` — S-1-2 顯示缺少名稱錯誤:
  - 受測行為：
    - 前置：瀏覽器開啟相簿首頁，API Mock 依 API-001-C2 回應
    - 打：在真實頁面未填相簿名稱就送出
    - 看：Playwright 觀測錯誤文案、清單與瀏覽器網路請求
    - 期望：頁面顯示「name is required」，且沒有新增相簿
    - 文案：name is required
    - 還沒做時：頁面尚未處理 400 回應，主斷言失敗
  - 契約案例：API-001-C2
- [ ] `/tdd-e2e-green` — S-1-2:
  - 實作計畫：
    - 加入呈現 API 驗證錯誤且不更新相簿清單的最少行為
    - 本則不驗證：真實後端與其他錯誤類型
- [ ] `/tdd-e2e-refactor` — S-1-2:
  - 整理範圍：
    - 只整理本則新增的錯誤狀態與畫面呈現
    - 不准擴到其他 User Story
- [ ] `User Story 層內全綠閘門` — S-1-2:
  - 累積測試：`npm run test:e2e:frontend -- --grep US-1`
  - 契約證據：`uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence frontend/test-results/api-contract.json --user-story US-1 --scenario S-1-2 --contract-id API-001-C2 --require-source frontend-mock`
  - 完成：同層、同一 User Story 到目前 Scenario 的測試與契約證據全部通過

- [ ] `User Story 完成閘門` — US-1:
  - User Story 測試：`npm run test:e2e:frontend -- --grep US-1`
  - 全層回歸：`npm run test:e2e:frontend`
  - 契約證據：`uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence frontend/test-results/api-contract.json --user-story US-1 --require-source frontend-mock`

---

## 4. 進度總覽

| User Story | Scenario | Red | Green | Refactor | 層內全綠 |
| --- | --- | --- | --- | --- | --- |
| US-1 | S-1-1 | 待執行 | 待執行 | 待執行 | 待執行 |
| US-1 | S-1-2 | 待執行 | 待執行 | 待執行 | 待執行 |

| User Story | 完成閘門 |
| --- | --- |
| US-1 | 待執行 |

---

## 5. 假設

- Playwright 已由技術研究選定為瀏覽器端對端測試工具。
