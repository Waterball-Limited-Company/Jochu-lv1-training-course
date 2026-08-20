# Scenario Agent 交接

scenario-agent-id: {{SCENARIO_AGENT_ID}}
layer: {{LAYER}}
plan-package: {{PLAN_PACKAGE}}
user-story: {{USER_STORY_ID}}
scenario: {{SCENARIO_ID}} {{SCENARIO_TITLE}}

## 執行順序

1. 讀取下列已定位片段，不重新擴張需求範圍。
2. 先跑同層、同 User Story 已完成 Scenario 的累積測試，確認進場基準為綠。
3. 執行 `/tdd-e2e-red`，保存正確紅燈證據。
4. 在同一代理脈絡執行 `/tdd-e2e-green`，只做最少 Green。
5. 在同一代理脈絡執行 `/tdd-e2e-refactor`，不得擴充需求。
6. 執行 User Story 層內全綠閘門與契約證據驗證。
7. 回報各階段狀態、命令、證據檔、變更檔與第一個未完成階段。

## 已定位片段

task:
{{TASK_SCENARIO_BLOCK}}

e2e:
{{E2E_SCENARIO_BLOCK}}

system-analyze:
{{SYSTEM_ANALYZE_FRAGMENTS}}

API 契約案例:
{{API_CONTRACT_FRAGMENTS}}

## 執行邊界

允許修改:
{{ALLOWED_PATHS}}

禁止修改:
{{FORBIDDEN_PATHS}}

測試與證據命令:
{{TEST_AND_EVIDENCE_COMMANDS}}

既有進度與證據:
{{EXISTING_PROGRESS_AND_EVIDENCE}}
