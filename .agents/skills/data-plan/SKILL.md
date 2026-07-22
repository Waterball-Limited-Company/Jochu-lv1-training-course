---
name: data-plan
description: 將已收斂的功能規格與技術可行性研究整理成資料實體合約（實體欄位、欄位約束、領域假設），並在需要任何 DB 持久化時另產 DDL.md（ERD、設計脈絡、DDL、引擎假設），輸出到 specs/<NNN-plan-package>/system-analyze/。Use when the user invokes /data-plan, asks for Data Plan / data model / DDL during system analysis, or needs to derive persistence contracts from spec.md and technical-research.md.
disable-model-invocation: true
---

# Data Plan

將同 package 的 `spec.md`、`technical-research.md`（與可選的 clarify 決策）整理成可 Review 的持久化介面合約：`data-plan.md` 以資料實體為單位展開欄位／驗證規則／US 追溯與衍生屬性，並以「因為…（FR／US），所以…」寫**實體內部**約束與領域假設；若 plan／research 顯示會用任何 DB 做持久化讀寫，另產 `DDL.md`（ERD、設計脈絡、可執行 DDL、引擎／落表假設）。`spec.md` 的 `## 關鍵實體` 僅作種子／參考；落表與欄位決策由本 skill 萃取。下游有 DB 時應同時對齊兩檔；無 DB 時只對齊 `data-plan.md`。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取使用者需求、同 package 的 `spec.md`（含 `## 關鍵實體` 若有）、`system-analyze/technical-research.md`、既有 clarify 決策（若有）與 `templates/data-plan.example.md`，確認功能主題、US／FR／邊界、關鍵實體種子、技術選型與持久化線索。
2. THINK 若 `technical-research.md` 不存在，停止後續步驟，先請使用者完成 `/technical-research` 或經 `/system-analyze` 主鏈產出。
3. READ 讀取 `rules/輸出檔案定位判準.md`，確認 `data-plan.md`／按需 `DDL.md` 的路徑、檔名、標題 metadata，以及何時必須產出 `DDL.md`。
4. THINK 依本次已載入規則，收斂 `plan-package`、目標路徑、標題 metadata，以及本次是否需要 `DDL.md`（任何 DB 持久化讀寫＝需要）。

## Phase 2 -- 先處理高影響缺口

1. READ 讀取 `rules/澄清缺口與假設標記判準.md`，確認高影響缺口如何 `/clarify` 或標 `[NEEDS CLARIFICATION]`，以及低風險如何寫入各檔 `## 假設`。
2. THINK 依本次已載入規則，盤點會改變實體集合、關聯基數、主鍵／唯一鍵策略或讓多張表同時改寫的高影響缺口與可進假設的低風險項。
3. DELEGATE 若高影響缺口應先拍板，呼叫 `/clarify`；若需先產出可 Review 暫定內容，後續正文必須內嵌 `[NEEDS CLARIFICATION: …]`，低風險僅寫對應檔末 `## 假設`，不自行腦補成定案。

## Phase 3 -- 收斂實體與欄位約束

1. READ 讀取 `rules/資料實體與欄位萃取判準.md` 與 `rules/約束清單因果表述判準.md`，確認實體／欄位與**實體內部**約束的寫法。
2. THINK 依本次已載入規則：若 `spec.md` 有 `## 關鍵實體`，先盤點實體名／描述／關鍵屬性作為種子；若無，改以 US／FR／邊界為起點。
3. THINK 依本次已載入規則，決定落表集合（含中介表）、欄位、衍生屬性與欄位／屬性約束；種子僅供參考；儲存選型對齊 technical-research。關聯形狀（基數、缺邊、級聯）留待有 DB 時在 `DDL.md` 處理，不寫進約束清單。

## Phase 4 -- 寫出 data-plan.md

1. READ 讀取 `templates/data-plan.md` 與 `templates/data-plan.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/system-analyze/data-plan.md`，順序為實體 → 約束清單 → 領域 `## 假設`（不含 ERD／DDL）。

## Phase 5 -- 按需寫出 DDL.md

1. THINK 若 Phase 1 判定不需要 `DDL.md`，跳過本 phase。
2. READ 若需要 `DDL.md`：讀取 `rules/ERD關聯與基數判準.md`、`rules/DDL單一腳本撰寫判準.md`、`templates/DDL.md` 與 `templates/DDL.example.md`，確認 ERD、設計脈絡、DDL 與引擎假設寫法。
3. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/system-analyze/DDL.md`，順序為 ERD → 設計脈絡 → DDL → 引擎／落表 `## 假設`；假設與 `data-plan.md` 分層不重複。

## Phase 6 -- 驗證結構與修正

1. READ 回頭檢查：`data-plan.md` 實體六欄完整、約束僅實體內部、領域假設存在且無 ERD／SQL；若本次需 DB，則 `DDL.md` 存在，含 Mermaid ERD、設計脈絡（無關聯則宣告本期無跨實體關聯）、單一 DDL 腳本與引擎假設，且能對上 data-plan 可落庫項與設計脈絡；種子有去向；選型不與 research 矛盾；若不符合，立即修正。
