# 實作計畫（整合）：相簿管理

流程版本: 2
功能分支: `001-photo-albums`
建立日期: 2026-08-20
狀態: 草稿
範圍: 真實瀏覽器、前端、正式 API、後端與可重設測試資料庫

---

## 1. 規格閱讀

- [ ] 讀取規格、API 契約、端對端測試計畫與前後端任務計畫

```bash
ls specs/001-photo-albums/task-plan
```

---

## 2. 環境建立

- [ ] 啟動完整系統，確認 API Mock 與其他替身已停用

---

## 3. User Story 實作計劃

### US-1 建立相簿（優先級：P1）

#### AC / Edge

- 使用者由瀏覽器建立相簿後，重新整理仍可看到資料

#### US-1 由瀏覽器建立相簿並持久保存

- [ ] `User Story 完全端對端驗收` — US-1:
  - 前置閘門：後端與前端的 US-1 完成閘門皆已通過
  - Mock：停用
  - 前端：真實執行期頁面
  - API：正式 API
  - 後端：真實後端
  - 資料：`npm run test:data:reset`
  - 執行：`npm run test:e2e:integration -- --grep US-1`
  - 觀測：真實瀏覽器畫面、網路請求與重新整理後的資料
  - 期望：建立「旅行」後重新整理仍顯示「旅行」
  - 契約案例：API-001-C1
  - 契約證據：`uv run .agents/skills/implement/scripts/validate_api_contract_evidence.py --api-plan specs/001-photo-albums/system-analyze/api-plan.md --evidence test-results/integration-api-contract.json --user-story US-1 --require-source integration`
  - 失敗路由：行為缺口回到對應層 Scenario；契約不一致依 api-plan.md 判定漂移方；接線或環境缺口留在整合驗收修復

---

## 4. 進度總覽

| User Story | 完全端對端驗收 |
| --- | --- |
| US-1 | 待執行 |

---

## 5. 假設

- 整合環境可重設測試資料，且不連到正式資料。
