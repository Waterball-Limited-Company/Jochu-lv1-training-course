# 實作計畫（後端）：相簿管理

流程版本: 2
功能分支: `001-photo-albums`
建立日期: 2026-08-20
狀態: 草稿

---

## 1. 規格閱讀

- [ ] 讀取規格、API 契約、端對端測試計畫與後端系統分析

```bash
ls specs/001-photo-albums
```

---

## 2. 環境建立

- [ ] 建立可重設的測試資料庫，並確認 `npm run test:e2e:backend` 可執行

---

## 3. User Story 實作計劃

### US-1 建立相簿（優先級：P1）

#### AC / Edge

- 相簿名稱為必填
- 建立成功後可由正式 API 查到

#### S-1-1 建立名為「旅行」的相簿

- [ ] `/tdd-e2e-red` — S-1-1 建立名為「旅行」的相簿:
  - 受測行為：
    - 前置：測試資料庫已重設
    - 打：由正式 HTTP API 建立相簿
    - 看：HTTP 回應與查詢 API
    - 期望：回傳 201，且查詢結果含「旅行」
    - 還沒做時：建立 API 回傳 404，主斷言失敗
  - 契約案例：API-001-C1
- [ ] `/tdd-e2e-green` — S-1-1:
  - 實作計畫：
    - 完成建立相簿的最少後端行為與資料寫入
    - 本則不驗證：前端呈現與相簿排序
- [ ] `/tdd-e2e-refactor` — S-1-1:
  - 整理範圍：
    - 只整理本則新增的建立相簿路徑
    - 不准擴到其他 User Story
- [ ] `User Story 層內全綠閘門` — S-1-1:
  - 累積測試：`npm run test:e2e:backend -- --grep US-1`
  - 契約證據：`uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence backend/test-results/api-contract.json --user-story US-1 --scenario S-1-1 --contract-id API-001-C1 --require-source backend-contract`
  - 完成：同層、同一 User Story 到目前 Scenario 的測試與契約證據全部通過

#### S-1-2 拒絕未提供相簿名稱

- [ ] `/tdd-e2e-red` — S-1-2 拒絕未提供相簿名稱:
  - 受測行為：
    - 前置：測試資料庫已重設
    - 打：由正式 HTTP API 送出沒有 name 的 request
    - 看：HTTP 錯誤回應與查詢 API
    - 期望：回傳 400 與名稱必填錯誤，且資料未新增
    - 還沒做時：API 未拒絕缺少 name 的 request，主斷言失敗
  - 契約案例：API-001-C2
- [ ] `/tdd-e2e-green` — S-1-2:
  - 實作計畫：
    - 加入拒絕缺少 name 與錯誤 envelope 的最少後端行為
    - 本則不驗證：前端錯誤呈現與其他驗證規則
- [ ] `/tdd-e2e-refactor` — S-1-2:
  - 整理範圍：
    - 只整理本則新增的名稱驗證與錯誤轉換
    - 不准擴到其他 User Story
- [ ] `User Story 層內全綠閘門` — S-1-2:
  - 累積測試：`npm run test:e2e:backend -- --grep US-1`
  - 契約證據：`uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence backend/test-results/api-contract.json --user-story US-1 --scenario S-1-2 --contract-id API-001-C2 --require-source backend-contract`
  - 完成：同層、同一 User Story 到目前 Scenario 的測試與契約證據全部通過

- [ ] `User Story 完成閘門` — US-1:
  - User Story 測試：`npm run test:e2e:backend -- --grep US-1`
  - 全層回歸：`npm run test:e2e:backend`
  - 契約證據：`uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence backend/test-results/api-contract.json --user-story US-1 --require-source backend-contract`

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

- 測試資料庫可在每次案例前重設。
