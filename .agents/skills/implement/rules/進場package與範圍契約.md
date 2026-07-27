# Rule 1 - plan-package 以掃描為主、多個才問

- Level: `MUST`
- 若使用者／呼叫已提供 `plan-package`（僅目錄名，不含 `specs/`），直接使用。
- 若未提供：掃描 `specs/*/task-plan/` 中存在 `task-backend.md` 或 `task-frontend.md` 或 `task-integration.md` 的 package。
  - 恰有一個：採用它。
  - 零個：停止並回報需先完成 `/task-plan`。
  - 多個：必須詢問使用者選哪一個，不可擅自選。
- 路徑一律 `specs/<plan-package>/task-plan/...`。

## Good Example

- 這個例子是好的，因為只有一個 package 時自動採用。

```text
掃到 specs/001-photo-albums/task-plan/
→ plan-package = 001-photo-albums
```

## Bad Example

- 這個例子是壞的，因為多個 package 時默默選了第一個。

```text
有 001-photo-albums 與 002-xxx → 直接用 001
```

# Rule 2 - 進場必須確認範圍選單（四選一）

- Level: `MUST`
- 在開始執行任何 task 步驟前，必須取得本輪範圍，選項固定為：
  1. 僅後端（`task-backend.md`）
  2. 僅前端（`task-frontend.md`）
  3. 後端 → 前端
  4. 後端 → 前端 → 整合
- 若使用者已在呼叫參數中明確指定且可映射到上列之一，可不再重複詢問。
- 順序以選項寫死為準；若要非常規順序，應經 Others／補充說明後才執行。

## Good Example

- 這個例子是好的，因為選了 4 後層序列清楚。

```text
選擇 4 → backend, frontend, integration
```

## Bad Example

- 這個例子是壞的，因為沒問範圍就三層全跑。

```text
直接依序跑完所有 task-*.md
```

# Rule 3 - 對應 task 檔必須存在

- Level: `MUST`
- 選定範圍後，序列中每一層的 `task-<layer>.md` 都必須存在於 `specs/<plan-package>/task-plan/`。
- 缺檔則停止並回報，不可改跑其他層充數。

## Good Example

- 這個例子是好的，因為選「僅前端」且檔案存在。

```text
specs/001-photo-albums/task-plan/task-frontend.md ✓
```

## Bad Example

- 這個例子是壞的，因為選含整合但缺少 task-integration.md 仍硬跑。

```text
缺 task-integration.md → 跳過整合繼續報成功
```
