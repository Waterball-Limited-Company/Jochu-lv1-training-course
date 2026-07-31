---
name: ooa-plan
description: 在 technical-research／plan 之後、data／api／ui 之前，以簡化循環星形法產出物件導向分析（OOA）合約 ooa.md（Use Case Diagram → UC 敘述 → 領域 Class → 業務 Sequence）。Use when the user invokes /ooa-plan, asks for OOA / 物件導向分析 / Use Case／領域模型 during system analysis, or needs domain analysis before interface plans.
disable-model-invocation: true
---

# OOA Plan

將同 package 的 `spec.md`、已存在之 `system-analyze/technical-research.md` 與 package 根目錄 `plan.md`，整理成可 Review 的 OOA 合約 `ooa.md`：依簡化循環星形法依序產出 Use Case Diagram、Use Case 敘述（階層固定為 User Story → Use Case）、領域 Class Diagram、業務 Sequence Diagram。C4 Context／Container 不屬於本 skill（留在 technical-research）。下游 data／api／ui 可對齊本檔領域語彙，但本 skill **不**代寫介面合約。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取 `.agents/skills/constitution/` 內 RuleFile「交付skill讀取憲法判準.md」，以及專案根目錄 `constitution.md`（若存在）。
2. THINK 依本次已載入之憲法讀取規則處理缺檔或套用約束：缺檔則警告後繼續；有檔則萃取與本 skill 相關之規範，後續步驟／產出與憲法衝突時以憲法為準。
3. READ 讀取使用者需求、同 package 的 `spec.md`、`system-analyze/technical-research.md`、package 根目錄 `plan.md`、既有 clarify 決策（若有）與 `templates/ooa.example.md`，確認功能主題、US／Actor、領域範圍與技術邊界。
4. THINK 若 `technical-research.md` 或 `plan.md` 不存在，停止後續步驟，先請使用者完成 `/technical-research`（或經 `/system-analyze` 產出 research＋plan）後再呼叫本 skill。
5. READ 讀取 `rules/輸出檔案定位判準.md`，確認 `ooa.md` 與 Use Case 附屬圖檔路徑、標題 metadata。
6. THINK 依本次已載入規則，收斂 `plan-package`、目標路徑與標題 metadata。

## Phase 2 -- 先處理高影響缺口

1. READ 讀取 `rules/澄清缺口與假設標記判準.md`，確認高影響缺口如何 `/clarify` 或標 `[NEEDS CLARIFICATION]`，以及低風險如何寫入 `## 假設`。
2. THINK 依本次已載入規則，盤點會改變 Actor 集合、Use Case 邊界、領域實體集合或業務流程成敗條件的高影響缺口與可進假設的低風險項。
3. DELEGATE 若高影響缺口應先拍板，呼叫 `/clarify`；若需先產出可 Review 暫定內容，後續正文必須內嵌 `[NEEDS CLARIFICATION: …]`，低風險僅寫檔末 `## 假設`，不自行腦補成定案。

## Phase 3 -- 依循環星形法收斂四步分析

1. READ 讀取 `rules/循環星形法與敘述階層判準.md`，確認四步順序、US→UC 階層、Diagram 語法邊界與業務 Sequence 邊界。
2. THINK 依本次已載入規則與 `spec.md` 的 User Story／角色，收斂：Actor 與 Use Case 清單、各 US 底下的 UC 敘述、領域類別與關聯、以及足以說明關鍵業務成敗的 Sequence 集合（不求覆蓋每一 UC）。

## Phase 4 -- 寫出 ooa.md 與 Use Case 附屬圖

1. READ 讀取 `templates/ooa.md` 與 `templates/ooa.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將 Use Case Diagram 的 PlantUML 源寫入同目錄 `ooa-use-case.puml`，並匯出／嵌入 `ooa-use-case.png`（或當次約定檔名）；再將完整 `ooa.md` 寫入 `specs/<NNN-plan-package>/system-analyze/ooa.md`，章節順序固定為：Use Case Diagram → Use Case 敘述 → 領域 Class Diagram → 業務 Sequence Diagram → `## 假設`。
3. THINK 若環境無法匯出 PNG，仍須留下 `.puml` 與 `ooa.md` 內對圖檔的引用說明，並在 `## 假設` 註明圖檔待補；不可改用 flowchart 冒充 Use Case Diagram。

## Phase 5 -- 結構檢查與收尾

1. READ 回頭檢查：`ooa.md` 存在且四步＋假設齊全；敘述階層為 US→UC；Use Case association 只連 Actor↔Use Case；領域 Class 無 Service／Policy；Sequence 僅業務參與者與領域物件；路徑與標題對齊輸出規則；若不符合，立即修正。
2. WRITE 在對話簡述產物路徑與四步摘要；下一步交回呼叫端（例如 `/system-analyze` 後續介面委派或人工 Review），本 skill 不代跑 data／api／ui。
