---
name: data-plan
description: 將已收斂的功能規格與技術可行性研究整理成以資料實體為顆粒度的繁體中文資料模型合約（實體欄位、ERD、約束、DDL、假設），輸出到 specs/<NNN-plan-package>/system-analyze/data-plan.md。Use when the user invokes /data-plan, asks for Data Plan / data model / DDL during system analysis, or needs to derive persistence contracts from spec.md and technical-research.md.
disable-model-invocation: true
---

# Data Plan

將同 package 的 `spec.md`、`technical-research.md`（與可選的 clarify 決策）整理成可 Review 的持久化介面合約：以資料實體為單位展開欄位／驗證規則／US 追溯與衍生屬性；以 Mermaid ERD 表達關聯與基數；以「因為…（FR／US），所以…」寫約束；文末給單一可執行 DDL，並以與 `spec.md` 同格式的 `## 假設` 收斂第一版設計假設。data-plan 是系統分析中供下游引用的持久化真相；`spec.md` 的 `## 關鍵實體` 僅作種子／參考，落表與欄位決策由本 skill 萃取。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取使用者需求、同 package 的 `spec.md`（含 `## 關鍵實體` 若有）、`system-analyze/technical-research.md`、既有 clarify 決策（若有）與 `templates/data-plan.example.md`，確認功能主題、US／FR／邊界條件、關鍵實體種子、技術選型與持久化線索。
2. THINK 若 `technical-research.md` 不存在，停止後續步驟，先請使用者完成 `/technical-research` 或經 `/system-analyze` 主鏈產出。
3. READ 讀取 `rules/輸出檔案定位判準.md`，確認最終 `data-plan.md` 的目錄、檔名與標題 metadata。
4. THINK 依本次已載入規則，收斂 `plan-package`、目標路徑、標題 metadata（功能分支／建立日期／狀態）與預計涵蓋的資料實體範圍。

## Phase 2 -- 先處理高影響缺口

1. READ 讀取 `rules/澄清缺口與假設標記判準.md`，確認高影響缺口如何 `/clarify` 或標 `[NEEDS CLARIFICATION]`，以及低風險如何只寫 `## 假設`。
2. THINK 依本次已載入規則，盤點會改變實體集合、關聯基數、主鍵／唯一鍵策略或讓多張表同時改寫的高影響缺口與可進假設的低風險項。
3. DELEGATE 若高影響缺口應先拍板，呼叫 `/clarify`；若需先產出可 Review 暫定內容，後續正文必須內嵌 `[NEEDS CLARIFICATION: …]`，低風險僅寫檔末 `## 假設`，不自行腦補成定案。

## Phase 3 -- 從關鍵實體種子與 spec 收斂實體、關聯與約束

1. READ 讀取 `rules/資料實體與欄位萃取判準.md`、`rules/ERD關聯與基數判準.md`、`rules/約束清單因果表述判準.md` 與 `rules/DDL單一腳本撰寫判準.md`，確認實體／欄位／ERD／約束／DDL 的寫法與判準。
2. THINK 依本次已載入規則：若 `spec.md` 有 `## 關鍵實體`，先盤點實體名／描述／關鍵屬性作為種子清單；若無該章節，改以 US／FR／邊界為起點。
3. THINK 依本次已載入規則，由本 skill 決定落表集合（含中介表）、欄位、衍生屬性、關聯基數、因果約束與 DDL；種子僅供參考，不強制一關鍵實體一表；儲存／執行環境選型須對齊 technical-research。

## Phase 4 -- 寫出 data-plan

1. READ 讀取 `templates/data-plan.md` 與 `templates/data-plan.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/system-analyze/data-plan.md`，順序為實體 → ERD → 約束清單 → DDL → 檔末假設。

## Phase 5 -- 驗證結構與修正

1. READ 回頭檢查最終 data-plan 是否符合本次已載入規則：實體欄位六欄完整、會落成表的概念都有一級實體、ERD 僅 Mermaid、約束為「因為…（FR／US），所以…」、DDL 為文末單一腳本且能對上約束、檔末 `## 假設` 存在；若有 `## 關鍵實體`，每個種子皆有去向且非默默消失；選型不與 research 矛盾；若不符合，立即修正。
