# Rule 1 - 後端／前端切片對齊 AC／Edge；整合對齊 User Story

- Level: `MUST`
- `## 後端`／`## 前端` 的每則薄切片必須對齊一條驗收標準（AC）或一條可測邊界條件（Edge）。
- 不可為了湊數量而發明 spec 沒有的行為例子；也不可把多條無關 AC 塞進同一則切片。
- 若同一則切片同時涵蓋語意重複的 AC 與全域 Edge（例如移動照片與禁止多重歸屬），允許在「AC / Edge」小標下列出多條，但業務 Scenario ID 仍只有一個。
- 一則切片只對準一個主要意圖、一個 public seam。受測部位若要用「以及／然後再」才能講完，就拆則。同一條 AC 可對多則 Scenario（例如 AC-1-1 拆成建立與匯入）。
- `## 整合` 對準各 User Story 的獨立驗證，一則 US 一則 `US-n`，不必再掛 AC／Edge，也不可把後端／前端的 `S-x-y` 再抄一輪。
- 拆則理由與 TDD 節奏寫在 skill，不寫進產物旁白。

## Good Example

- 這個例子是好的，因為一則 Scenario 清楚對到 AC，必要時可併列同源 Edge。

```md
#### Scenario: S-1-2 將已歸屬照片改加入另一相簿後只留在目標相簿

**對應欄位**:

- **AC / Edge**
  - AC-1-2 …
  - Edge-G-2 …
```

## Bad Example

- 這個例子是壞的，因為一則 Scenario 混進多條無關驗收。

```md
#### Scenario: S-9-9 一次做完建立、拖放與平鋪

**對應欄位**:

- **AC / Edge**
  - AC-1-1 …
  - AC-3-1 …
  - AC-4-1 …
```

# Rule 2 - Scenario 編號與標題使用業務 ID，不加證明區塊括號

- Level: `MUST`
- 後端／前端標題格式為 `#### Scenario: S-<US>-<N> <業務標題>`。
- 整合標題格式為 `#### Scenario: US-<n> <驗收標題>`。
- 標題內不可加 `（後端）`／`（前端）`／`（整合）`；證明方式由所在的 `## 後端`／`## 前端`／`## 整合` 區塊區分。
- 同一 `S-x-y` 可同時出現在後端與前端；整合用 `US-n`，不要把薄切片再抄進整合。

## Good Example

- 這個例子是好的，因為切片與驗收編號乾淨，區塊標題承擔命名空間。

```md
## 後端

#### Scenario: S-1-1 建立名為「旅行」的相簿

## 整合

#### Scenario: US-1 建立兩個相簿並確認照片只在所屬相簿
```

## Bad Example

- 這個例子是壞的，因為把證明區塊寫進 Scenario 標題。

```md
#### Scenario: S-1-1（後端）建立「旅行」相簿並一次匯入多格式照片
```

# Rule 3 - 未澄清的邊界標 blocked，不產出可執行 Scenario

- Level: `MUST`
- 含 `[NEED CLARIFICATION: …]` 或明確依賴未拍板決策的 Edge，本輪不寫可執行 Scenario，改在「未產出 Scenario 的邊界（blocked）」表列原因。
- 不可自行腦補行為後當成已覆蓋。

## Good Example

- 這個例子是好的，因為未澄清項進入 blocked 表。

```md
## 未產出 Scenario 的邊界（blocked）

| ID | 描述 | 阻塞原因 |
| --- | --- | --- |
| Edge-3-2 | … | [NEED CLARIFICATION: 日期分組與自訂順序共存規則未定] |
```

## Bad Example

- 這個例子是壞的，因為未澄清仍寫成確定行為的 Scenario。

```md
#### Scenario: S-3-9 任意猜測跨組拖放後的順序
```

# Rule 4 - Edge ID 必須依 spec 條列順序穩定編號

- Level: `MUST`
- Edge ID 採 `Edge-<US序>-<該 US 邊界情境條列序>`；全域邊界採 `Edge-G-<全域邊界條列序>`。
- 編號僅為追溯穩定，不可依寫作當下隨意跳號或重編已發布 ID。

## Good Example

- 這個例子是好的，因為對齊 US-1 第一條邊界與全域第二條邊界。

```md
- Edge-1-1 …（對應 US-1 邊界情境第 1 條）
- Edge-G-2 …（對應全域邊界情境第 2 條）
```

## Bad Example

- 這個例子是壞的，因為同一邊界每次編號不同。

```md
本輪寫 Edge-A、下輪改 Edge-99
```
