# Artifact 轉換檢查表

## 任務資訊

- 參考 artifact: `/.agents/skills/my-specify/templates/spec.example.md`
- 目標 artifact: `使用者滿意的新 spec 成品`
- 本輪目標: `把既有 spec 格式改成 FR 與成功標準都歸屬在 User Story 內的 target artifact`

## Benchmark 可借鑑之處

- 整體規格文件的章節骨架與寫作語氣
- 使用者故事、驗收情境與關鍵實體的表達方式

## 必須改寫之處

- FR 原本散在故事外，需求單位與階層不清楚
- 成功標準原本散在故事外，無法回掛到對應故事價值

## 高影響缺口

- 改寫後要不要完全以 User Story 為主體
- 跨故事限制要放在故事內還是全域約束區

## 澄清決策

- 採完全以 User Story 為主體的整體結構
- 跨故事限制另外保留在全域約束區

## 結構轉換動作

- 保留: 使用者故事敘事、驗收情境與關鍵實體章節
- 上提: 相簿不可嵌套這類跨故事限制到全域約束區
- 下放: FR 到各自 User Story
- 合併: 建立相簿與整理照片為同一個核心故事
- 刪除: 舊版獨立全域功能需求區與全域成功標準區

## Target Artifact 完成定義

- 每個 User Story 內都有自己的 FR、成功標準、驗收情境與邊界情境
- 全域限制只留在 `共通規則與全域約束`

## 後續工程化輸入

- target artifact 已可作為 template 萃取來源：是
- target artifact 已可作為 skill 工程 benchmark：是
