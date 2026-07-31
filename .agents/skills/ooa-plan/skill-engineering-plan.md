# Skill 工程編排提案

## 任務資訊

- 處理路徑: `create`（主）＋後續 `optimize`（掛鏈，另開閘門）
- 改動範圍: `create new skill` → 再 `skill chain rewrite`
- 目標 Skills: `ooa-plan`（新建）；確認後再動 `system-analyze`

## 控制平面重建

- **本期先建** `.agents/skills/ooa-plan/`：最小 SOP，產出 `system-analyze/ooa.md`（循環星形法四步：Use Case Diagram → UC 敘述 → 領域 Class → 業務 Sequence）。
- 輸入契約：同 package `spec.md`、已存在之 `technical-research.md` 與 `plan.md`（OOA 插在 research／plan **之後**、data／api／ui **之前**）。
- C4 Context／Container **不**放進 OOA；維持在 `technical-research`（既有共識）。
- Use Case 圖：PlantUML 源檔＋匯出 PNG 嵌 Markdown（Preview 可讀）；Class／Sequence 用 Mermaid。
- **不**在本提案一次改 `system-analyze`：掛鏈屬既有 skill 優化，須另交根因確認閘門後再改編排（避免跳過 optimize lane）。

## 步驟決策

- `讀憲法`：keep inline（對齊 data-plan／api-plan）。
- `收斂 package／輸出路徑`：derive rule（`輸出檔案定位判準.md`）— 產物 `specs/<NNN>/system-analyze/ooa.md`，附屬 `ooa-use-case.puml`／`.png`。
- `高影響缺口`：derive rule（輕量，對齊 sibling 的澄清／假設標記）。
- `四步循環星形`：keep inline 於主 SOP 分 phase；細部「敘述階層 US→UC」「Sequence 僅業務語言」「Class 不含 Service／Policy」可按需 derive 1～2 份 rule，**先從最簡 SOP 起步、規則按需疊代**。
- `寫檔樣板`：template **已抽出**（`templates/ooa.md` + `ooa.example.md`）— derive-template 視為完成，SOP 回掛讀取時機即可。
- `驗證腳本`：本期 **不做**（避免過度工程）；靠結構檢查清單 inline。
- `掛進 system-analyze`：delete from 本 create 提案範圍；改列為後續 optimize + RCA。

## 檔案動作

### 新增 / 更新

- Create `.agents/skills/ooa-plan/SKILL.md`（最小 SOP）
- Keep `.agents/skills/ooa-plan/templates/ooa.md`
- Keep `.agents/skills/ooa-plan/templates/ooa.example.md`（溯源：`specs/002-meeting-room-booking/system-analyze/ooa.md`）
- Create（按需）`.agents/skills/ooa-plan/rules/輸出檔案定位判準.md`
- Create（按需）`.agents/skills/ooa-plan/rules/循環星形法與敘述階層判準.md`
- Create（按需）`.agents/skills/ooa-plan/rules/澄清缺口與假設標記判準.md`

### 刪除

- 無（新建 skill，無舊 SOP 可刪）
- 明確**不刪／不改**現有 `system-analyze` 委派順序，直到掛鏈 RCA 通過

## 驗證方式

- 對照定稿 example：四章＋假設皆在；敘述階層 US→UC；無實作分層混入 Sequence。
- `analyze_skill_references.py --skill .agents/skills/ooa-plan`：template／rule 皆被 SOP 引用、無孤兒。
- 人工：用 `002-meeting-room-booking` 想像重跑一輪，產物路徑與章節能對上 example。

## 實作閘門

- 本 create 提案已於 2026-07-30 **落地**：`SKILL.md`＋三份 rules＋既有 templates。
- 掛進 `/system-analyze`（plan 確認「繼續」之後、data／api／ui 之前）→ 另開 **optimize + 根因報告**，勿與本 create 混做。
- 約束：不要過度工程、先從最簡單 SOP 開始、rules 按需疊代且必須掛回主 SOP。
