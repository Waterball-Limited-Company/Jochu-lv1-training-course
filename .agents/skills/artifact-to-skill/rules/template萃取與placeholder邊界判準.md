# Rule 1 - 只有 target artifact 定稿後，才可開始萃取 template

- Level: `MUST`
- template 必須從已穩定的 target artifact 萃取，而不是從 benchmark 或半成品草稿萃取。
- 若 target artifact 的階層或欄位仍可能大改，應先停在成品改寫階段，不得提前抽骨架。

## Good Example

- 這個例子是好的，因為先有定稿成品，再抽樣板。

```md
1. 先把 target artifact 改到使用者滿意
2. 再把固定結構抽成 template
3. 保留完整成品作為 example
```

## Bad Example

- 這個例子是壞的，因為它在成品還沒穩定時就先抽 placeholder。

```md
1. 看完 benchmark 後直接建立 template
2. 之後再慢慢把 target artifact 改出來
```

# Rule 2 - template 只保留固定骨架，example 保留完整成品

- Level: `MUST`
- template 檔只保留固定結構、固定語法與待填內容的 placeholder。
- example 檔必須保留與 template 同結構的完整 target artifact 成品。
- 不可讓 template 塞滿一次性的具體內容，也不可讓 example 檔仍殘留 placeholder。

## Good Example

- 這個例子是好的，因為骨架與成品責任清楚。

```md
template：
- `{{USER_STORY_TITLE}}`
- `{{SUCCESS_CRITERIA_1}}`

example：
- `建立相簿並整理照片`
- `80% 的使用者能在 3 分鐘內建立至少 1 個相簿並加入照片`
```

## Bad Example

- 這個例子是壞的，因為骨架與成品角色顛倒。

```md
template：
- `建立相簿並整理照片`

example：
- `{{USER_STORY_TITLE}}`
```

# Rule 3 - placeholder 只覆蓋真正可變的語意槽位

- Level: `SHOULD`
- 萃取樣板時，應只把真正會變動的內容抽成 placeholder，固定標題、格式符號與結構關鍵字應保留在骨架中。
- 若某段內容在不同任務間通常保持不變，就不應過度抽象化。

## Good Example

- 這個例子是好的，因為它只抽出變動值。

```md
### 使用者故事 {{USER_STORY_NUMBER}} - {{USER_STORY_TITLE}}（優先級：{{USER_STORY_PRIORITY}}）
```

## Bad Example

- 這個例子是壞的，因為它連固定結構都一起抽掉了。

```md
{{USER_STORY_HEADING_LINE}}
```
