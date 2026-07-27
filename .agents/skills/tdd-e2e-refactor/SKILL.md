---
name: tdd-e2e-refactor
description: 由 implement 在該 US Green 全綠後呼叫：依 layer、plan-package、單一 User Story 與 Refactor 實作計畫，在行為與契約不變下做去重、可讀／可維護整理與計畫點名的風格對齊；過程可多次跑該層全套測試，結束必須仍全綠並回報。Use when implement invokes /tdd-e2e-refactor, or when executing a task-plan Refactor checkbox for one User Story.
disable-model-invocation: true
---

# TDD E2E Refactor

由 `/implement` 在該 US 已 Green 全綠後呼叫。一次針對**一個 User Story**：依 Refactor 實作計畫整理程式碼與測試（去重、非功能品質、計畫點名的對齊風格／抽層），**不改行為與契約**。過程可多次執行該層全套測試；結束時必須仍全綠。不代勾 `task-*.md` checkbox。

# SOP

## Phase 1 -- 校驗呼叫輸入

1. READ 讀取 implement 帶入的 `layer`、`plan-package`、User Story 識別、Refactor 實作計畫。
2. READ 讀取 `rules/呼叫輸入與US範圍契約.md`，確認必填欄位與單 US 邊界。
3. THINK 依本次已載入規則校驗輸入；若不通過，停止並進入 Phase 4 回報。

## Phase 2 -- 載入重構 context 並確認起點全綠

1. READ 讀取 `rules/Context與重構範圍判準.md`、`rules/Refactor完成條件與改動邊界.md`，確認可載內容、允許／禁止範圍，以及起點／終點全綠閘門。
2. READ 依本次已載入規則載入：Refactor 實作計畫、將整理的程式／測試、必要時點名的 SA 片段。
3. READ 讀取該層測試腳本定義（如 `package.json` 的 `scripts`）。
4. THINK 依本次已載入規則收斂全套測試指令；找不到則進入 Phase 4 回報。
5. DELEGATE 執行該層全套測試。
6. THINK 依本次已載入規則判定起點是否可進入重構；若不通過，進入 Phase 4 回報。

## Phase 3 -- 依計畫重構並保持全綠

1. WRITE 依本次已載入規則與實作計畫進行重構。
2. DELEGATE 執行該層全套測試。
3. THINK 依本次已載入規則判定是否仍全綠、是否繼續重構，或進入 Phase 4（成功或失敗回報）。

## Phase 4 -- 回報 implement

1. READ 讀取 `rules/回報與環境洞交接.md`，確認回報欄位。
2. WRITE 依本次已載入規則，向 implement 回報本次結果。
