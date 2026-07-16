---
name: artifact-to-skill
description: Transforms a benchmark artifact into a target artifact, extracts a reusable template, and engineers a reliable project skill with SOP, rules, templates, and validation. Use when the user wants to borrow a reference artifact format, reshape it into a desired artifact, then productize the whole reasoning and generation process as a skill.
disable-model-invocation: true
---

# Artifact to Skill

當使用者拿一份既有 artifact 當 benchmark，想先改成自己要的 target artifact，再萃取成樣板，最後把整套推理與生成方法工程化成 skill 時，先把 benchmark、target artifact、template 與 skill modules 分層，再按順序完成，不得直接跳到最後寫 `SKILL.md`。

# SOP

## Phase 1 -- 收斂 benchmark 與目標邊界

1. READ 讀取使用者需求、參考 artifact、目標 artifact 與相關上下文，確認本次是借鑑格式、重構結構、抽出樣板，還是要把整條流程工程化成新 skill。
2. READ 讀取 `rules/benchmark與目標artifact收斂判準.md` 與 `rules/clarify與推進時機判準.md`，確認 benchmark、target artifact、template 與最終 skill 的邊界，以及何時必須先澄清。
3. THINK 依本次已載入規則，收斂 benchmark artifact 的可借鑑部分、target artifact 的預期結果、預計輸出的層次與本次交付邊界。
4. DELEGATE 若高影響缺口會改變 artifact 階層、歸屬、樣板骨架或 skill 輸出契約，呼叫 `/clarify` 先收斂決策，收到回答前停止後續工程化。

## Phase 2 -- 先把 artifact 改到目標成品

1. READ 讀取 `rules/artifact改寫與結構重組判準.md`，確認如何根據使用者要求重組階層、歸屬、章節與驗證單位。
2. READ 讀取 `templates/artifact-transformation-checklist.template.md` 與 `templates/artifact-transformation-checklist.example.md`，確認 benchmark 到 target artifact 的映射方式。
3. THINK 依本次已載入規則，先把 benchmark artifact 拆成可操作的結構元素，再收斂哪些內容要保留、重組、上提、下放、合併或刪除。
4. WRITE 先產出一份 target artifact 成品；若使用者尚未滿意，持續以 target artifact 為主體反覆修正，直到它能作為後續樣板與工程化 benchmark。

## Phase 3 -- 從 target artifact 萃取樣板

1. READ 讀取 `rules/template萃取與placeholder邊界判準.md`，確認何時可抽成 placeholder、哪些內容應保留為固定骨架，以及骨架檔與範例檔的責任分工。
2. THINK 依本次已載入規則，把 target artifact 中固定結構與可變內容分離，收斂最小可用樣板。
3. WRITE 產出對應 template 與 example，確保骨架檔只保留固定結構與填位符號，範例檔則保留完整目標成品。

## Phase 4 -- 反推高可靠生成方法

1. READ 讀取 `rules/meta工程化與模組抽取判準.md`，確認哪些推理工作應保留在主 SOP，哪些判準應抽成 `rules/`，哪些固定骨架應抽成 `templates/`，哪些機械檢查應抽成 `scripts/`。
2. THINK 依本次已載入規則，從 target artifact 與 template 反推要穩定重現此成果所需的推理流程、決策節點、中繼 artifact、驗證方式與輸出契約。
3. WRITE 依 `templates/artifact-to-skill-plan.template.md` 與 `templates/artifact-to-skill-plan.example.md`，先產出一份工程化提案，說明主 SOP、rules、templates、scripts 與驗證策略。

## Phase 5 -- 落地並驗證新 skill

1. WRITE 依確認版提案建立或更新目標 skill 的 `SKILL.md`、`rules/`、`templates/`、`scripts/`，讓 benchmark、target artifact、template 與 validator 的 handoff 維持單一溯源。
2. DELEGATE 若需要檢查工程化結果是否完整，執行 `uv run .agents/skills/artifact-to-skill/scripts/validate_artifact_to_skill_outputs.py --skill-dir <target-skill-dir>`，檢查必要檔案、樣板雙檔與主 SOP 掛接是否齊備。
3. READ 回頭檢查最終 skill 是否符合本次已載入規則：先有 target artifact，後有 template，再有 skill modules；主 SOP 仍是控制平面，rules / templates / scripts 都有明確掛接時機；若不符合，立即修正。
