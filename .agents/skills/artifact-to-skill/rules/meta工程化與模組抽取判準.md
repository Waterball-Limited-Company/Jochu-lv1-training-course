# Rule 1 - 先有 target artifact 與 template，才可反推 skill modules

- Level: `MUST`
- `SKILL.md`、`rules/`、`templates/`、`scripts/` 的設計，必須建立在已完成的 target artifact 與 template 之上。
- 不可在缺少 benchmark 成品與樣板的情況下，直接憑空寫一套 skill。

## Good Example

- 這個例子是好的，因為它先完成 artifact 與 template，再工程化 skill。

```md
1. benchmark -> target artifact
2. target artifact -> template
3. template -> SOP / rules / templates / scripts
```

## Bad Example

- 這個例子是壞的，因為它顛倒了依賴順序。

```md
1. 先寫 SKILL.md
2. 之後再決定 target artifact 長什麼樣
```

# Rule 2 - 高判斷工作留在主 SOP，穩定判準與固定骨架才抽成模組

- Level: `MUST`
- benchmark 到 target artifact 的判斷、澄清時機、工程化取捨應留在主 SOP。
- 可重複的判準適合抽成 `rules/`，固定中繼骨架適合抽成 `templates/`，機械式檢查適合抽成 `scripts/`。
- 不可用 template 取代高判斷推理，也不可用 script 取代設計決策。

## Good Example

- 這個例子是好的，因為主 SOP、rules、templates、scripts 分工清楚。

```md
- 主 SOP：先 benchmark，後 target artifact，再 template，再 skill engineering
- rules：artifact 切分、template 邊界、clarify 時機
- templates：轉換 checklist、engineering plan
- scripts：檢查必要檔案與樣板雙檔是否齊備
```

## Bad Example

- 這個例子是壞的，因為它把高判斷工作外包錯地方。

```md
- 用 template 決定 artifact 應該如何重組
- 用 script 決定哪些 modules 要新增
```

# Rule 3 - 工程化結果必須能回推到 benchmark 與 target artifact

- Level: `SHOULD`
- 新 skill 產出的每個 module 都應能回推到它服務的是 benchmark 到 target artifact 的哪一段轉換。
- 若某個 rule、template 或 script 無法指出自己支撐哪一段轉換，就應重新檢查是否有新增過度。

## Good Example

- 這個例子是好的，因為每個模組都可回掛。

```md
- `artifact-transformation-checklist.template.md`：支撐 benchmark -> target artifact 的映射
- `template萃取與placeholder邊界判準.md`：支撐 target artifact -> template
- `validate_artifact_to_skill_outputs.py`：支撐最終工程化結果驗證
```

## Bad Example

- 這個例子是壞的，因為新增模組沒有可追溯來源。

```md
- 新增 `rules/靈感整理.md`
- 新增 `templates/random-note.template.md`
```
