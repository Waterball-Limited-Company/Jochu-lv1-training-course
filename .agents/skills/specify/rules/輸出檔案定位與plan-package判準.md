# Rule 1 - 最終 spec 必須寫到 `specs/<NNN-plan-package>/spec.md`

- Level: `MUST`
- `my-specify` 的最終產物路徑固定為 `specs/<NNN-plan-package>/spec.md`。
- 不可把完成 spec 留在聊天訊息、暫存筆記或其他任意檔名中，否則後續工作流難以穩定接續。
- 若 `specs/` 目錄尚不存在，應先建立對應的 `plan-package` 目錄，再寫入 `spec.md`。

## Good Example

- 這個例子是好的，因為輸出路徑與 skill 契約完全對齊。

```text
specs/003-reading-list/spec.md
```

## Bad Example

- 這個例子是壞的，因為它把 spec 放到臨時位置，其他流程無法穩定接手。

```text
tmp/reading-list.md
```

# Rule 2 - `plan-package` 必須使用三位數前綴加主題 slug

- Level: `MUST`
- `plan-package` 必須採 `NNN-plan-package` 形式，其中 `NNN` 為三位數遞增前綴，`plan-package` 為對應主題的英文小寫 kebab-case slug。
- 若 `specs/` 底下已有既有項目，應取目前最大前綴加 1；若尚無任何項目，應從 `001` 開始。
- `slug` 應對齊主要功能主題，不可直接整句照抄原始需求。

## Good Example

- 這個例子是好的，因為它同時滿足編號規則與可讀主題。

```text
001-online-course-platform
003-reading-list
```

## Bad Example

- 這個例子是壞的，因為它缺少固定編號格式，且 slug 也過於隨意。

```text
1-reading-list
new spec for reading list
```

# Rule 3 - `功能分支` 應與目錄 package 對齊

- Level: `SHOULD`
- 寫入 spec 時，`**功能分支**` 欄位應與所在的 `plan-package` 使用相同字串，讓檔案內容與目錄名稱可互相對應。
- 若使用者已明確指定 branch 或 package 名稱，應優先沿用該名稱，而不是重新命名。
- `功能規格` 標題可保留較自然的中文功能名，不必和 slug 完全一致。

## Good Example

- 這個例子是好的，因為檔案路徑與欄位內容能互相追溯。

```md
**功能分支**: `003-reading-list`
```

## Bad Example

- 這個例子是壞的，因為目錄名稱與檔內欄位分離，容易造成後續引用混亂。

```md
**功能分支**: `readinglist-final-v2`
```
