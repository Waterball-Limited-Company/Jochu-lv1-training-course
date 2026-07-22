---
name: ui-plan
description: 將已收斂的功能規格、技術可行性研究與上游合約整理成以業務邏輯與頁面切分的繁體中文人機介面合約（非視覺 Design），輸出到 specs/<NNN-plan-package>/system-analyze/ui-plan.md。Use when the user invokes /ui-plan, asks for UI Plan / screen contract during system analysis, or needs to derive page contracts from spec.md and technical-research.md.
disable-model-invocation: true
---

# UI Plan

將同 package 的 `spec.md`、`technical-research.md`（與可選的 `api-plan.md`、`data-plan.md`、clarify 決策）整理成可 Review 的人機介面合約：依業務邏輯切分跨頁 Sequence 並追溯 US／FR／AC；以可獨立到達的全頁為顆粒度，展開呈現內容、頁內操作 Flow、導覽與操作↔API 對應。非視覺 Design。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取使用者需求、同 package 的 `spec.md`、`system-analyze/technical-research.md`、既有 `system-analyze/` 產物（若有 `api-plan.md`、`data-plan.md`）與 `templates/ui-plan.example.md`，確認功能主題、US／FR／AC 清單、技術選型、畫面與導覽線索。
2. THINK 若 `technical-research.md` 不存在，停止後續步驟，先請使用者完成 `/technical-research` 或經 `/system-analyze` 主鏈產出。
3. READ 讀取 `rules/輸出檔案定位判準.md`，確認最終 `ui-plan.md` 的目錄與檔名。
4. THINK 依本次已載入規則，整理 `plan-package`、目標路徑、標題 metadata（功能分支／建立日期／狀態）與預計涵蓋的業務邏輯與頁面。

## Phase 2 -- 先處理高影響缺口

1. READ 讀取 `rules/澄清缺口與假設標記判準.md`，確認高影響缺口如何 `/clarify` 或標 `[NEEDS CLARIFICATION]`，以及低風險如何只寫 `## 假設`。
2. THINK 依本次已載入規則，盤點會改變頁面集合、業務邏輯切分、導覽拓樸或操作↔API 主對應的高影響缺口與可進假設的低風險項。
3. DELEGATE 若高影響缺口應先拍板，呼叫 `/clarify`；若需先產出可 Review 暫定內容，後續正文必須內嵌 `[NEEDS CLARIFICATION: …]`，低風險僅寫檔末 `## 假設`，不自行腦補成定案。

## Phase 3 -- 收斂業務邏輯與頁面設計

1. READ 讀取 `rules/業務邏輯切分與追溯判準.md` 與 `rules/頁面邊界與合約展開判準.md`，確認業務邏輯編號／跨頁 Sequence／US-FR-AC 追溯，以及頁面邊界／呈現／Flow／導覽／API 對應寫法。
2. THINK 依本次已載入規則，把 US／FR 映射到業務邏輯與頁面，收斂導覽關係與操作↔API 對應；前端互動手段須對齊 technical-research。

## Phase 4 -- 寫出 ui-plan

1. READ 讀取 `templates/ui-plan.md` 與 `templates/ui-plan.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/system-analyze/ui-plan.md`。

## Phase 5 -- 驗證結構與修正

1. DELEGATE 執行 `uv run .agents/skills/system-analyze/ui-plan/scripts/validate_ui_plan_output.py --input specs/<NNN-plan-package>/system-analyze/ui-plan.md`，檢查必要章節、業務邏輯與頁面結構是否完整。
2. READ 回頭檢查最終 ui-plan 是否符合本次已載入規則：業務邏輯連續編號並追溯 US／FR／AC、僅全頁算頁面、各頁含職責／呈現／Flow／導覽／API 對應、檔末 `## 假設` 章節存在、高影響未決已用 `[NEEDS CLARIFICATION]`（若有）、且不與 technical-research 主選型矛盾；若不符合，立即修正。
