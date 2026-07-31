# Rule 1 - 有帳密／session 認證時必須產出 Auth 基線 Scenario

- Level: `MUST`
- 當同 package 的 `spec.md`／`api-plan.md`／憲法顯示本期採帳密或伺服端 session 認證時，`e2e-test-plan.md` MUST 產出可執行的 **Auth 基線** Scenario（可掛在最早需要登入的 US 下，或獨立小節），至少覆蓋：
  1. 有效帳密登入成功並建立可續用的 session／登入態；
  2. 以既有 session 還原目前使用者（對齊 current-user／`/me` 類能力）；
  3. 登出（或等價撤銷）後，受保護操作被拒絕。
- 不可只把登入寫進業務 Scenario 的 Given，卻完全沒有可獨立證明的 Auth 基線 Scenario。
- 具體 path／欄位仍對齊該功能 `api-plan.md`；本規則只強制「要有這類可測基線」，不發明憲法未允許的堆疊。

## Good Example

- 這個例子是好的，因為 Auth 有獨立可追蹤 Scenario，業務 Scenario 再依賴它。

```md
#### Scenario: S-1-0 登入成功並建立可續用會話
#### Scenario: S-1-0b 以會話還原目前使用者
#### Scenario: S-1-0c 登出後受保護操作被拒絕
#### Scenario: S-1-1 登入後建立合法預約並確認
```

## Bad Example

- 這個例子是壞的，因為全檔只有業務預約 Scenario，登入僅出現在 Given。

```md
#### Scenario: S-1-1 登入後建立合法預約並確認
  Given 員工已登入
  When 送出預約
  Then …
（檔中無任何登入／還原／登出的獨立 Scenario）
```

# Rule 2 - Auth 基線須在後端與前端落點出現（整合按需）

- Level: `SHOULD`
- 後端區塊 SHOULD 以 API 證明 login／current-user／logout（或等價）契約。
- 前端區塊 SHOULD 以 UI 證明登入成功、還原登入態、登出後導向或拒絕受保護頁。
- 整合區塊僅在 Then 必須真串接才有意義時再加（例如跨頁重新載入後仍由後端還原會話）；不必為 Auth 基線強行灌三層重複。

## Good Example

- 這個例子是好的，因為後端／前端都有 Auth 基線，整合只留跨頁還原。

```text
後端: S-1-0 login／me／logout
前端: S-1-0 登入頁→Home、重新整理仍登入、登出
整合:（可選）重新整理後仍見本人預約
```

## Bad Example

- 這個例子是壞的，因為只在整合才第一次出現 logout／me。

```text
後端／前端業務 Scenario 全綠 → 整合才發現沒有 /me
```
