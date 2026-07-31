# Frontend Implement Status

**PASS**

- Node.js：`v24.14.0`（LTS）
- 建置：`npm --prefix frontend run build` → PASS
- 測試：`npm --prefix frontend test` → PASS（1 test file、25 tests；20 個前端 Scenario 全涵蓋）
- Lint／IDE diagnostics：0 errors

## 主要摩擦

- Shell 環境帶有未知 npm `devdir` 設定，直接執行 `npm run` 曾錯誤解析到 monorepo 根目錄；改用明確的 `npm --prefix frontend ...` 後正常。
- Vite 初始骨架只有展示頁，需完整替換為原生 DOM History router、六頁、Mock API 與 jsdom 驗收測試。
- 一般開發／建置預設使用真實 `/api` fetch（含 `credentials: include`）；設定 `VITE_USE_MOCK=true` 可切換為同介面的可控 Mock 供本層獨立驗收。
