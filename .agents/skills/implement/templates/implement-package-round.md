# Implement 進場 package 選單

<!-- 僅在掃描到多個 plan-package 時使用；鎖定後再輸出範圍選單。 -->

## 選擇功能目錄

**Context**  
掃描 `specs/*/task-plan/` 後找到多個可執行 package，需要你指定這一次要用哪一個（目錄名不含 `specs/`）。

**總結之提問**  
這次要實作哪個功能目錄？

**Options（單選）**

| 編號 | 選項 | 說明 |
| --- | --- | --- |
| 1 | `{{PACKAGE_OPTION_1}}` | {{PACKAGE_OPTION_1_DESC}} |
| 2 | `{{PACKAGE_OPTION_2}}` | {{PACKAGE_OPTION_2_DESC}} |
| 3 | Others | 上列沒有、或要指定其他 `NNN-slug`。 |

請回覆選項編號；若選 Others，請寫出 `plan-package` 目錄名。
