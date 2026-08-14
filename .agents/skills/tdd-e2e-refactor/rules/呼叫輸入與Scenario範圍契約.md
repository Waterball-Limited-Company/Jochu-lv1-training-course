# Rule 1 - 呼叫時必須帶齊本則必填欄位

- Level: `MUST`
- implement 呼叫 `/tdd-e2e-refactor` 時必須顯式提供：`layer`、`plan-package`（僅目錄名，不含 `specs/`）、本則 ID／標題、該格「整理範圍」。
- 本則 ID：後端／前端為 `S-n-m`；整合為 `US-n`。不可改傳整個 User Story 當工作範圍。
- 缺少必填欄位時必須停止並回報。

## Good Example

- 這個例子是好的，因為本則與整理範圍齊備。

```text
layer: frontend
plan-package: 001-photo-albums
本則: S-1-1
整理範圍: 在綠燈下整理剛寫的建立表單／POST /albums 命名與去重；不准擴到批次匯入
```

## Bad Example

- 這個例子是壞的，因為未指定本則與範圍就開始大範圍重構。

```text
US: US-1
把 frontend 全部重構一遍
```

# Rule 2 - 一次呼叫只處理一個 Scenario

- Level: `MUST`
- 一次呼叫只整理本則「整理範圍」點名的程式與測試；不可借機做同 US 下一則或跨 US 大重構。
- 在該則 Green 之後立刻執行，不必等本 US 其他則全綠。

## Good Example

- 這個例子是好的，因為鎖在 S-1-1 剛綠的建立表單。

```text
S-1-1 剛綠 → 只整理建立表單／POST /albums
```

## Bad Example

- 這個例子是壞的，因為等 US-1 全綠才重構，或順便整理 S-1-6。

```text
等 S-1-1～S-1-6 全綠後一次 Refactor
S-1-1 refactor 順便改加入照片
```
