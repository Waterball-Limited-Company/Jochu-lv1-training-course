---
name: my-specify
description: 將自然語言產品需求整理成以 User Story 為主體、FR 與驗收標準都歸屬於故事內的繁體中文 spec，並輸出到 specs/<NNN-plan-package>/spec.md。
disable-model-invocation: true
---

# My Specify

將使用者以自然語言描述的產品需求，整理成可評估、可驗證、以 User Story 為主體的繁體中文 spec。此 skill 的目標不是直接做系統設計，而是先把需求邊界、故事切分、FR 歸屬、驗收標準、假設與待澄清缺口整理成穩定格式。

# SOP

## Phase 1 -- 收斂輸入與輸出契約

1. READ 讀取使用者需求、現有上下文與 `templates/spec.example.md`，確認本次功能主題、主要角色、外部互動對象、明確範圍、非範圍與使用者已提供的約束。
2. READ 讀取 `rules/輸入切分與範圍界定判準.md` 與 `rules/輸出檔案定位與plan-package判準.md`，確認如何把原始敘述切成 spec 輸入單位，以及最終 `spec.md` 的目錄命名方式。
3. THINK 依本次已載入規則，整理 `初次輸入`、補充輸入、角色與外部互動者、範圍與非範圍、預計輸出的 `plan-package` 與目標檔案路徑。

## Phase 2 -- 先處理高影響缺口

1. READ 讀取 `rules/澄清缺口與假設標記判準.md`，確認哪些缺口必須先澄清，哪些可以先帶著顯式假設繼續。
2. THINK 依本次已載入規則，盤點會改變故事邊界、角色權限、公開性、狀態轉換、付款與退款規則、或驗收單位的高影響缺口。
3. DELEGATE 若仍有高影響缺口會改變 spec 主結構，呼叫 `/clarify` 先向使用者提問；若剩餘缺口屬局部不確定性，則在後續故事內以 `[NEED CLARIFICATION: ...]` 顯式標記，不自行腦補。

## Phase 3 -- 切分使用者故事並回掛需求

1. READ 讀取 `rules/使用者故事切分與排序判準.md` 與 `rules/故事內需求與驗收歸屬判準.md`，確認如何切出可獨立驗證的故事，並把 FR、邊界條件與驗收標準回掛到對應故事內。
2. THINK 依本次已載入規則，把需求整理成依價值與前置關係排序的 User Story，為每個故事補齊敘事、優先級、FR、優先序原因、獨立驗證方式、邊界條件與驗收標準。

## Phase 4 -- 收斂跨故事資訊並寫出 spec

1. READ 讀取 `rules/跨故事資訊放置判準.md` 與 `templates/spec.template.md`，確認哪些資訊應留在全域區，哪些應只存在於個別故事內，以及最終骨架格式。
2. THINK 依本次已載入規則，整理跨故事的共通限制、非目標、全域前提、權限限制、狀態名詞與其他不應重複散落的資訊，並收斂 `# 原始需求` 與 `## 假設` 內容。
3. WRITE 依 `templates/spec.template.md` 的骨架與 `templates/spec.example.md` 的完成態，將結果寫入 `specs/<NNN-plan-package>/spec.md`。

## Phase 5 -- 驗證結構與修正

1. DELEGATE 執行 `uv run .agents/skills/my-specify/scripts/validate_spec_output.py --input specs/<NNN-plan-package>/spec.md`，檢查必要章節、User Story 區塊與 FR 歸屬是否完整。
2. READ 回頭檢查最終 spec 是否符合本次已載入規則：User Story 是主要驗證單位、FR 與驗收標準都歸屬在故事內、跨故事資訊沒有重複散落、待澄清缺口有明確標記；若不符合，立即修正。
