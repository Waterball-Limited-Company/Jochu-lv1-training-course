---
name: analyze
description: 在 task-plan 完成後，對同 package 的 spec、系統介面合約、e2e-test-plan 與 task-plan 做唯讀跨產物覆蓋與一致性分析，產出 package 根目錄 analyze-report.md；不修改來源規格。Use when the user invokes /analyze, asks for 規格一致性分析 / cross-artifact analysis after task-plan, or needs an implementation gate report before /implement.
disable-model-invocation: true
---

# Analyze

以同 package 已完成的 `task-plan/` 為前置閘門：盤點可分析產物、抽出 ID inventory、依「覆蓋＋跨層一致性」比對軸偵測，寫入 `specs/<NNN-plan-package>/analyze-report.md`（中文欄位總表／覆蓋矩陣）。來源規格唯讀；有嚴重發現時強烈建議先修再 `/implement`，並點名應重跑的 skill。對話收尾對齊 `/system-analyze` 收尾段格式。

# SOP

## Phase 1 -- 收斂 package 與前置產物

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」，以及專案根目錄 `constitution.md`（若存在）。
2. THINK 依本次已載入之憲法讀取規則處理缺檔或套用約束：缺檔則警告後繼續；有檔則萃取與本 skill 相關之規範，後續步驟／產出與憲法衝突時以憲法為準。
3. READ 讀取使用者需求與同 package 既有產物路徑線索，確認功能主題與 `plan-package`。
4. THINK 若同 package 尚無 `specs/<NNN-plan-package>/spec.md`，停止分析，先請使用者完成 `/specify` 或指定既有 package。
5. READ 讀取 `rules/輸出檔案定位判準.md`、`rules/前置產物與缺檔判準.md`，確認報告路徑與必備／選備產物清單。
6. THINK 依本次已載入規則盤點實際存在的產物；若缺必備產物（尤其 `task-plan/` 三檔與 `e2e-test-plan.md`），停止後續分析，指示補跑對應 skill；將「plan 標為必跑卻缺檔」的介面產物記為嚴重候選。

## Phase 2 -- 建立 inventory

1. READ 讀取 `rules/Inventory抽取判準.md`，以及 Phase 1 判定存在的 `spec.md`、`plan.md`、`system-analyze/` 介面檔、`e2e-test-plan.md`、`task-plan/` 各檔。
2. THINK 依本次已載入規則，只抽出穩定 ID 與短摘要，建立內部 inventory（需求／介面／Scenario／Task）；不把原文整份倒入報告。

## Phase 3 -- 依比對軸偵測

1. READ 讀取 `rules/比對軸與嚴重程度判準.md`。
2. THINK 依本次已載入規則，對 inventory 執行覆蓋與跨層一致性偵測，指派嚴重程度、穩定發現編號，並收斂覆蓋矩陣與指標；品質類（模糊詞／重複）不做或僅極輕量。

## Phase 4 -- 寫出分析報告

1. READ 讀取 `templates/analyze-report.md` 與 `templates/analyze-report.example.md`，確認骨架與完成態（中文欄位、可視化總表）。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/analyze-report.md`；不得修改任何來源規格檔。

## Phase 5 -- 對話收尾與嚴重項閘門

1. READ 讀取 `rules/對話產出與嚴重項閘門判準.md` 與已寫入的 `analyze-report.md`。
2. WRITE 依已載入規則，在對話輸出收尾段（對齊 `/system-analyze`：標題、本輪產物表、重點摘要、散文式下一步）；若有嚴重發現，強烈建議先處理後再 `/implement`，並點名應重跑的 skill 或手動修改目標；詢問是否要針對前 N 項提出補救編輯建議（不自動套用）。
3. READ 報告已寫入且對話收尾完成後，才結束本 skill。
