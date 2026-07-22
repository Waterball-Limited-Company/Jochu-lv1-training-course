---
name: api-plan
description: 將已收斂的功能規格、技術可行性研究與 data-plan／DDL（若有）整理成以資料實體切分、Endpoint 對齊 FR 的繁體中文 REST API Schema（單一 Markdown，參考 OpenAPI 可讀性但不產出 openapi.yml），並輸出到 specs/<NNN-plan-package>/system-analyze/api-plan.md。Use when the user invokes /api-plan, asks for API Plan / REST API Schema during system analysis, or needs to derive endpoint contracts from spec.md and technical-research.md.
disable-model-invocation: true
---

# API Plan

將同 package 的 `spec.md`、`technical-research.md`（與可選的 `data-plan.md`、`DDL.md`、clarify 決策）整理成可 Review 的 REST API Schema：以資料實體切分、實體對齊 US、Endpoint 對齊 FR；實體只寫欄位形狀與範例（型別與必填歸 data-plan；關聯／schema 歸 DDL.md）；Request／Response 完整展開；測試規劃只列情境名與預期 Status。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取使用者需求、同 package 的 `spec.md`、`system-analyze/technical-research.md`、既有 `system-analyze/` 產物（若有 `data-plan.md`；有 DB 時另讀 `DDL.md`）與 `templates/api-plan.example.md`，確認功能主題、US／FR 清單、技術選型、資料實體線索與既有約束。
2. THINK 若 `technical-research.md` 不存在，停止後續步驟，先請使用者完成 `/technical-research` 或經 `/system-analyze` 主鏈產出。
3. THINK 若判定本期有 DB 持久化但缺少 `DDL.md`，先請補跑 `/data-plan`（或經 `/system-analyze`），再繼續。
4. READ 讀取 `rules/輸出檔案定位判準.md`，確認最終 `api-plan.md` 的目錄與檔名。
5. THINK 依本次已載入規則，整理 `plan-package`、目標路徑、標題 metadata（功能分支／建立日期／狀態）與預計涵蓋的實體。

## Phase 2 -- 先處理高影響缺口

1. READ 讀取 `rules/澄清缺口與假設標記判準.md`，確認高影響缺口如何 `/clarify` 或標 `[NEEDS CLARIFICATION]`，以及低風險如何只寫 `## 假設`。
2. THINK 依本次已載入規則，盤點會改變資源切分、Endpoint 集合、錯誤語意或跨實體契約的高影響缺口與可進假設的低風險項。
3. DELEGATE 若高影響缺口應先拍板，呼叫 `/clarify`；若需先產出可 Review 暫定內容，後續正文必須內嵌 `[NEEDS CLARIFICATION: …]`，低風險僅寫檔末 `## 假設`，不自行腦補成定案。

## Phase 3 -- 收斂實體與 Endpoint 設計

1. READ 讀取 `rules/實體形狀與對齊判準.md` 與 `rules/Endpoint契約展開判準.md`，確認實體／US／形狀／DDL 邊界，以及 Endpoint／FR／Request-Response／測試規劃寫法。
2. THINK 依本次已載入規則，把 FR 映射到 Endpoint、把實體對齊 US，並收斂共通錯誤格式、設計備註與追溯關係；API 風格與執行環境須對齊 technical-research。

## Phase 4 -- 寫出 api-plan

1. READ 讀取 `templates/api-plan.md` 與 `templates/api-plan.example.md`，確認骨架與完成態。
2. WRITE 依骨架與範例，將結果寫入 `specs/<NNN-plan-package>/system-analyze/api-plan.md`。

## Phase 5 -- 驗證結構與修正

1. DELEGATE 執行 `uv run .agents/skills/api-plan/scripts/validate_api_plan_output.py --input specs/<NNN-plan-package>/system-analyze/api-plan.md`，檢查必要章節、實體與 Endpoint 結構是否完整。
2. READ 回頭檢查最終 api-plan 是否符合本次已載入規則：實體對齊 US、Endpoint 對齊 FR、形狀不含型別定義、Request／Response 完整展開、測試僅情境加 Status、檔末 `## 假設` 章節存在、高影響未決已用 `[NEEDS CLARIFICATION]`（若有）、且不與 technical-research 主選型矛盾；若不符合，立即修正。
