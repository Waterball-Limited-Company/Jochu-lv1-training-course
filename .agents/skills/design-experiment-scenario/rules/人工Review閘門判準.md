# Rule 1 - 每個產出階段結束後必須停等人工 Review

- Level: `MUST`
- 在 Phase 2（情境清單）、Phase 3（Prompt 規範）、Phase 4（依路徑：Artifact 為一致性報告／Skill 為「使用者已下 skill-engineering」確認）、Phase 5（Skill Eng 驗證紀錄）寫出產物或到達停點後，必須明確停等使用者 Review 或修改。
- 未收到確認（或等價指示如「通過」「確認」「go 下一階段」）前，不得進入下一 Phase。
- 停等時必須告訴使用者：本階段產物是什麼、請確認什麼、如何表示通過或要改什麼。

## Good Example

- 這個例子是好的，因為停點與確認方式依路徑清楚。

```md
Phase 2：請勾選課堂實驗選項字母（例如 `A` 或 `A, C`）。

Phase 3：請確認 Prompt 規範（標明實驗路徑 Artifact 或 Skill）。

Phase 4（Artifact）：請確認三跑一致性報告。
Phase 4（Skill）：正式 Prompt 已列出——請自行下 /skill-engineering 並貼上；本執行者不會直接改目標 skill。
```

## Bad Example

- 這個例子是壞的，因為產出後直接往下做，或 Skill 路徑擅自三跑改 skill。

```md
已列出情境，接著我先把 Prompt 規範與三跑都做完。
```

# Rule 2 - 使用者修改意見優先於原草案

- Level: `MUST`
- 若使用者要求修改目標、情境排序、規範條款或驗證結論，必須先依意見更新產物，再重新進入該階段的 Review 停等。
- 不可表面接受修改、卻在下一階段沿用舊草案。

## Good Example

- 這個例子是好的，因為先改產物再停等。

```md
已依你的意見刪除選項 H 並重排序 → 請再次確認勾選字母。
```

## Bad Example

- 這個例子是壞的，因為口頭答應但下一階段仍用舊清單。

```md
了解，那我們用原選項 A 繼續寫規範。
```

# Rule 3 - 允許使用者縮範圍，禁止執行者擅自擴範圍

- Level: `MUST`
- 使用者可決定本期只做到某一階段（例如 Artifact 只到三跑、Skill 只到交付 Prompt）。
- 執行者不得在未要求下自動補做完整學員 SOP、下游全鏈接線、或直接改目標 skill。
- 若發現必要的已知債，可寫在產物「已知債」區，但仍須停等，不可逕自開工。

## Good Example

- 這個例子是好的，因為尊重本期邊界。

```md
本期到交付 /skill-engineering Prompt 為止；正式改 tdd-e2e-green 由使用者下指令。
```

## Bad Example

- 這個例子是壞的，因為擅自擴大。

```md
順手把目標 skill 與課綱全部改完。
```
