# Prompt 撰寫規範：抽換 API Artifact → OpenAPI

**實驗路徑**: `Artifact`
**對應課堂實驗**: A（api-plan.md → openapi.yaml）
**建立日期**: 2026-07-30
**狀態**: 待 Review

## 規範目的

讓「修改 Artifact」的 Prompt 在不同 model 下仍維持相近品質，並符合大顆粒度、可重複使用的寫法。

## 適用範圍

- 來源：`system-analyze/api-plan.md`（或同結構 Markdown API 計畫）
- 目標：OpenAPI 3.0.3 YAML（`openapi.yaml`）

## 撰寫原則

1. 用「請參照…，將此 Artifact 修改，符合以下規範」開頭，不要寫成長篇規格書。
2. 條列 5～10 條大顆粒度要求：格式、路徑、結構、忠實對齊、資訊承載、錯誤／安全、完成自檢。
3. 實作細節少寫；靠 OpenAPI 慣例與原 Artifact 補齊。
4. 規範文件與單次 Prompt 草稿分開：規範可複用，草稿可變。

## 建議結構（大顆粒度）

1. 參照來源 Artifact  
2. 目標格式與檔案型態  
3. 寫入位置／暫定檔名策略  
4. 文件必要頂層結構  
5. 與原 Artifact 對齊（不增刪 API）  
6. 原資訊如何用 OpenAPI 欄位承接  
7. 錯誤與 ID、安全機制  
8. 完成物與自檢清單  

## 必須鎖住的範圍（不寫就容易偏）

- OpenAPI **3.0.3**、輸出 **YAML**（不要 Markdown／JSON OpenAPI）
- 頂層至少：`openapi`、`info`（title／version／description）、`paths`；共用型別與錯誤在 `components`
- 不新增、不擅自刪減原 path／method
- 共通錯誤可重用並被引用；對外 ID 用字串 UUID
- 公開與受保護端點可區分

## 避免寫法

- 把完整 OpenAPI 規格書貼進 Prompt  
- 允許「順便重設計 API」  
- 只在聊天給摘要、不要求寫檔  

## 品質穩定檢查（跨 model）

- 版本是否為 3.0.3、是否為可 parse 的 YAML  
- endpoint 集合是否與來源一致  
- 是否有共用 Error schema  
- 三跑時是否「大品質同檔」（允許 naming 漂移）  

## 本輪 Prompt 草稿（可選）

請參照同 package 的 `system-analyze/api-plan.md`，我們要將此 Artifact 進行修改，符合以下規範：

1. 將其改寫為 OpenAPI 3.0.3 格式，輸出為 YAML 檔（不要 Markdown、不要 JSON OpenAPI）。
2. 檔案寫入與目前 Artifact 相同的地方，檔案名稱也需相同，可以先用暫定檔名確認內文沒問題之後再覆蓋原檔名。
3. 文件結構須符合 OpenAPI 常見寫法，開頭至少包含：openapi、info（含 title、version、description）、paths；共用型別與錯誤格式放在 components。
4. 內容須對齊原 Artifact：原有的 path、method、Request／Response／錯誤狀態都要保留對應；不要新增原檔沒有的 API，也不要擅自刪減。
5. 原檔的資料實體、說明、設計備註、FR／US 追溯，改用 OpenAPI 慣用欄位（例如 tags、summary、description、schema），不可有資訊遺漏。
6. 共通錯誤格式須收成可重用的 schema，並讓各錯誤回應引用它；對外資源 ID 以字串 UUID 表達。
7. 若原檔有登入／session 等安全方式，用 OpenAPI 的 security 機制表達；公開端點與受保護端點要能區分。
8. 完成後只需產出完整 openapi.yaml，並用簡短清單自檢：版本正確、YAML 可讀、Endpoint 與原檔對齊、錯誤 schema 有共用。

---

# （對照）Skill 路徑草稿長什麼樣

**實驗路徑**: `Skill` 時，草稿給**使用者**下指令，例如：

請呼叫 `/skill-engineering`，目標 skill 為 `.agents/skills/tdd-e2e-green/`。我們要將此 Skill 優化，符合以下規範：

1. …

禁止寫成「直接改本目錄 SKILL.md」或「將此 Artifact 修改」。Phase 4 不對 skill 做三跑直接改檔。

## Review 停等

請確認或修改本規範；Artifact 路徑確認後進三跑；Skill 路徑確認後交付使用者下 `/skill-engineering`（禁止對 skill 三跑直接改檔）。
