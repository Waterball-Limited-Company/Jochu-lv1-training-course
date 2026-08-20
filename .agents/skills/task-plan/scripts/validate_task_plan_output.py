# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import re
import shlex
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## 1. 規格閱讀",
    "## 2. 環境建立",
    "## 3. User Story 實作計劃",
    "## 4. 進度總覽",
    "## 5. 假設",
]

LAYER_FILES = {
    "後端": "task-backend.md",
    "前端": "task-frontend.md",
    "整合": "task-integration.md",
}

FLOW_V2_RE = re.compile(r"(?mi)^流程版本\s*[:：]\s*2\s*$")
US_RE = re.compile(r"^### (US-\d+)\s+.+\（優先級：P\d+\）\s*$", re.M)
US_LEVEL_RGB_HEADING_RE = re.compile(r"(?m)^#### (Red|Green|Refactor)\s*$")
SCENARIO_HEADING_RE = re.compile(r"(?m)^#### ((?:S-\d+-\d+)|(?:US-\d+))\s+.+$")
E2E_SCENARIO_RE = re.compile(r"^#### Scenario:\s+((?:S-\d+-\d+)|(?:US-\d+))\s+", re.M)
RED_ITEM_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-red`?\s*—\s*((?:S-\d+-\d+)|(?:US-\d+))\s+"
)
GREEN_ITEM_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-green`?\s*—\s*((?:S-\d+-\d+)|(?:US-\d+))"
)
REFACTOR_ITEM_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/tdd-e2e-refactor`?\s*—\s*((?:S-\d+-\d+)|(?:US-\d+))"
)
CHECKBOX_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?/(tdd-e2e-(?:red|green|refactor))`?"
)
SCENARIO_GATE_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?User Story 層內全綠閘門`?\s*—\s*(S-\d+-\d+)"
)
US_GATE_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?User Story 完成閘門`?\s*—\s*(US-\d+)"
)
INTEGRATION_GATE_RE = re.compile(
    r"(?m)^\s*-\s*\[[ xX]\]\s*`?User Story 完全端對端驗收`?\s*—\s*(US-\d+)"
)
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
FORBIDDEN_VERIFY_RE = re.compile(
    r"確認本 US 的 TDD E2E Red 測試皆已實作且皆為紅燈"
)
FORBIDDEN_US_GREEN_RE = re.compile(r"讓本 US 既有 Red 全綠")

RED_FIELDS = ("前置", "打", "看", "期望")
SLICE_RED_FIELDS = RED_FIELDS + ("還沒做時",)
SHELL_CONTROL_RE = re.compile(r"(?:&&|\|\||[;|<>]|\$\(|`)")
TEST_COMMAND_HINT_RE = re.compile(
    r"(?i)(?:^|[\s:/_.-])(test|tests|e2e|spec|specs|playwright|cypress|pytest|rspec|verify|check)(?:$|[\s:/_.-])"
)
SCRIPT_TEST_HINT_RE = re.compile(
    r"(?i)(?:^|[\s:/_.-])(test|tests|e2e|spec|specs|verify|check)(?:$|[\s:/_.-])"
)
DATA_COMMAND_HINT_RE = re.compile(
    r"(?i)(?:^|[\s:/_.-])(data|database|db|reset|seed|fixture|migrat\w*)(?:$|[\s:/_.-])"
)
MOCK_CONTRADICTION_RE = re.compile(
    r"(?i)(?:"
    r"(?:不(?:需要|必須|會|要|需|予以)?|未|無法|無須|毋須|不用|免(?:於)?)\s*(?:停用|關閉|移除)[^\n]{0,40}mock"
    r"|mock[^\n]{0,30}(?:不(?:需要|必須|會|要|需|予以)?|未|無法|無須|毋須|不用|免(?:於)?)\s*(?:停用|關閉|移除)"
    r"|(?:仍(?:然)?|繼續)\s*(?:保留|使用|啟用|開啟)?[^\n]{0,30}mock"
    r"|mock[^\n]{0,30}(?:仍(?:然)?|繼續)\s*(?:保留|使用|啟用|開啟)"
    r"|mock[^\n]{0,20}(?:保持|維持)\s*(?:啟用|開啟|使用)"
    r"|(?<!不)(?<!未)(?<!不會)(?<!不再)(?<!無須)(?<!毋須)(?:沿用|啟用|開啟)\s*(?:既有|原有)?[^\n]{0,20}mock"
    r"|mock[^\n]{0,20}(?<!不)(?<!未)(?<!不會)(?<!不再)(?<!無須)(?<!毋須)(?:沿用|啟用|開啟)"
    r")"
)
MOCK_SAFE_NEGATION_RE = re.compile(
    r"(?i)(?:"
    r"(?:不(?:會|再|會再|會重新|再重新)?|未|無須|毋須|絕不)\s*(?:再(?:次)?|重新)?\s*(?:沿用|保留|使用|啟用|開啟)\s*(?:api\s*)?mock"
    r"|(?:api\s*)?mock[^\n]{0,16}(?:不(?:會|再|會再|會重新|再重新)?|未|無須|毋須|絕不)\s*(?:再(?:次)?|重新)?\s*(?:沿用|保留|使用|啟用|開啟)"
    r")"
)
FORBIDDEN_FAKE_COMMANDS = {"echo", "printf", "true", "false", ":"}
PYTHON_EXECUTABLE_RE = re.compile(r"python(?:\d+(?:\.\d+)*)?")
KNOWN_TEST_RUNNERS = {
    "playwright",
    "cypress",
    "vitest",
    "jest",
    "mocha",
    "ava",
    "pytest",
    "rspec",
}
KNOWN_DATA_RUNNERS = {"prisma", "knex", "sequelize", "typeorm"}
NON_EXECUTING_TEST_ARGS = {
    "--help",
    "-h",
    "--version",
    "version",
    "help",
    "--list",
    "--listTests",
    "--collect-only",
    "--co",
    "--dry-run",
    "--ui",
    "--if-present",
    "--ignore-scripts",
}
MANAGER_OPTIONS_WITH_VALUE = {
    "--filter",
    "-F",
    "--dir",
    "-C",
    "--cwd",
    "--workspace",
    "-w",
    "--prefix",
    "--package",
    "-p",
    "--call",
    "-c",
    "--node-options",
    "--npm",
    "--cache",
    "--registry",
    "--userconfig",
}
EVIDENCE_VALIDATOR_RELATIVE = (
    ".agents/skills/implement/scripts/validate_api_contract_evidence.py"
)
EVIDENCE_VALIDATOR_ABSOLUTE = (
    Path(__file__).resolve().parents[4] / EVIDENCE_VALIDATOR_RELATIVE
).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate task-plan artifacts for a specs package."
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Path to specs/<NNN-plan-package> directory",
    )
    return parser.parse_args()


def e2e_layer_scenarios(e2e_text: str, layer: str) -> list[str]:
    parts = re.split(r"(?m)^## ", e2e_text)
    body = ""
    for part in parts:
        if part.startswith(layer):
            body = part
            break
    return E2E_SCENARIO_RE.findall(body)


def section_three(text: str) -> str:
    if "## 3. User Story 實作計劃" not in text:
        return ""
    sec3 = text.split("## 3. User Story 實作計劃", 1)[1]
    if "## 4." in sec3:
        sec3 = sec3.split("## 4.", 1)[0]
    return sec3


def has_label(chunk: str, label: str) -> bool:
    return f"{label}：" in chunk or f"{label}:" in chunk


def label_value(chunk: str, label: str) -> str | None:
    match = re.search(
        rf"(?m)^[ \t]*-[ \t]*{re.escape(label)}[：:][ \t]*(.*?)[ \t]*$", chunk
    )
    return match.group(1).strip() if match else None


def label_positions(chunk: str, label: str) -> list[int]:
    return [
        match.start()
        for match in re.finditer(
            rf"(?m)^[ \t]*-[ \t]*{re.escape(label)}[：:]", chunk
        )
    ]


def executable_name(token: str) -> str:
    return token.rsplit("/", 1)[-1]


def exact_python_executable(token: str) -> bool:
    return PYTHON_EXECUTABLE_RE.fullmatch(executable_name(token)) is not None


def has_mock_contradiction(text: str) -> bool:
    without_safe_negations = MOCK_SAFE_NEGATION_RE.sub("", text)
    return MOCK_CONTRADICTION_RE.search(without_safe_negations) is not None


def wrapper_payload_index(tokens: list[str], start: int) -> int | None:
    index = start
    while index < len(tokens):
        token = tokens[index]
        if token in MANAGER_OPTIONS_WITH_VALUE:
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        return index
    return None


def wrapper_payload(tokens: list[str], start: int) -> str | None:
    """Return the first non-option payload after a package runner."""
    index = wrapper_payload_index(tokens, start)
    return executable_name(tokens[index]) if index is not None else None


def manager_payload_index(tokens: list[str]) -> int | None:
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token in MANAGER_OPTIONS_WITH_VALUE:
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        return index
    return None


def test_runner_invocation_is_valid(tokens: list[str], runner_index: int) -> bool:
    runner = executable_name(tokens[runner_index])
    if runner not in KNOWN_TEST_RUNNERS:
        return False
    args = tokens[runner_index + 1 :]
    if any(arg in NON_EXECUTING_TEST_ARGS for arg in args):
        return False
    if runner == "playwright":
        return bool(args) and args[0] == "test"
    if runner == "cypress":
        return bool(args) and args[0] == "run"
    return True


def data_runner_invocation_is_valid(tokens: list[str], runner_index: int) -> bool:
    runner = executable_name(tokens[runner_index])
    args = tokens[runner_index + 1 :]
    return (
        runner in KNOWN_DATA_RUNNERS
        and bool(args)
        and not any(arg in NON_EXECUTING_TEST_ARGS for arg in args)
    )


def command_is_recognized(tokens: list[str], *, purpose: str) -> bool:
    if not tokens:
        return False
    executable = executable_name(tokens[0])
    raw_command = " ".join(tokens)
    if executable in FORBIDDEN_FAKE_COMMANDS:
        return False
    if any(token in NON_EXECUTING_TEST_ARGS for token in tokens[1:]):
        return False
    if executable == "npm":
        hint_re = DATA_COMMAND_HINT_RE if purpose == "data" else TEST_COMMAND_HINT_RE
        payload_index = manager_payload_index(tokens)
        if payload_index is None:
            return False
        payload = executable_name(tokens[payload_index])
        if payload in FORBIDDEN_FAKE_COMMANDS:
            return False
        if payload == "run":
            target = wrapper_payload(tokens, payload_index + 1)
            script_hint_re = (
                DATA_COMMAND_HINT_RE if purpose == "data" else SCRIPT_TEST_HINT_RE
            )
            return (
                target is not None
                and target not in FORBIDDEN_FAKE_COMMANDS
                and script_hint_re.search(target) is not None
            )
        if payload in {"exec", "x"}:
            runner_index = wrapper_payload_index(tokens, payload_index + 1)
            if runner_index is None:
                return False
            return (
                data_runner_invocation_is_valid(tokens, runner_index)
                if purpose == "data"
                else test_runner_invocation_is_valid(tokens, runner_index)
            )
        return hint_re.search(payload) is not None
    if executable in {"pnpm", "yarn", "bun"}:
        if any(executable_name(token) in FORBIDDEN_FAKE_COMMANDS for token in tokens[1:]):
            return False
        payload_index = manager_payload_index(tokens)
        if payload_index is None:
            return False
        payload = executable_name(tokens[payload_index])
        hint_re = DATA_COMMAND_HINT_RE if purpose == "data" else TEST_COMMAND_HINT_RE
        allowed = KNOWN_DATA_RUNNERS if purpose == "data" else KNOWN_TEST_RUNNERS
        if payload == "run":
            target = wrapper_payload(tokens, payload_index + 1)
            script_hint_re = (
                DATA_COMMAND_HINT_RE if purpose == "data" else SCRIPT_TEST_HINT_RE
            )
            return (
                target is not None
                and target not in FORBIDDEN_FAKE_COMMANDS
                and script_hint_re.search(target) is not None
            )
        if payload in {"exec", "dlx", "x"}:
            runner_index = wrapper_payload_index(tokens, payload_index + 1)
            if runner_index is None:
                return False
            return (
                data_runner_invocation_is_valid(tokens, runner_index)
                if purpose == "data"
                else test_runner_invocation_is_valid(tokens, runner_index)
            )
        if payload in allowed:
            return (
                data_runner_invocation_is_valid(tokens, payload_index)
                if purpose == "data"
                else test_runner_invocation_is_valid(tokens, payload_index)
            )
        script_hint_re = DATA_COMMAND_HINT_RE if purpose == "data" else SCRIPT_TEST_HINT_RE
        return script_hint_re.search(payload) is not None
    if executable in {"npx", "bunx"}:
        if any(executable_name(token) in FORBIDDEN_FAKE_COMMANDS for token in tokens[1:]):
            return False
        payload_index = manager_payload_index(tokens)
        if payload_index is None:
            return False
        return (
            data_runner_invocation_is_valid(tokens, payload_index)
            if purpose == "data"
            else test_runner_invocation_is_valid(tokens, payload_index)
        )
    if executable == "uv":
        if len(tokens) < 3 or tokens[1] != "run":
            return False
        nested = tokens[2:]
        return command_is_recognized(nested, purpose=purpose)
    if exact_python_executable(tokens[0]):
        return (
            len(tokens) >= 3
            and tokens[1] == "-m"
            and test_runner_invocation_is_valid(tokens[2:], 0)
        )
    if executable == "go":
        return len(tokens) >= 2 and tokens[1] == "test"
    if executable == "cargo":
        return len(tokens) >= 2 and tokens[1] == "test"
    if executable == "dotnet":
        return len(tokens) >= 2 and tokens[1] == "test"
    if executable == "deno":
        return len(tokens) >= 2 and tokens[1] == "test"
    if executable == "composer":
        return len(tokens) >= 2 and tokens[1] in {"test", "run-script"}
    if executable == "bundle":
        return len(tokens) >= 3 and tokens[1:3] == ["exec", "rspec"]
    if executable == "mix":
        return len(tokens) >= 2 and tokens[1] == "test"
    if executable == "swift":
        return len(tokens) >= 2 and tokens[1] == "test"
    if executable == "xcodebuild":
        return "test" in tokens[1:]
    if executable in KNOWN_TEST_RUNNERS:
        return test_runner_invocation_is_valid(tokens, 0)
    if executable in {
        "mvn",
        "gradle",
        "gradlew",
        "make",
        "just",
        "task",
        "docker",
    }:
        if any(executable_name(token) in FORBIDDEN_FAKE_COMMANDS for token in tokens[1:]):
            return False
        hint_re = DATA_COMMAND_HINT_RE if purpose == "data" else TEST_COMMAND_HINT_RE
        return len(tokens) >= 2 and hint_re.search(raw_command) is not None
    if tokens[0].startswith("./") or executable.endswith((".sh", ".bash")):
        hint_re = DATA_COMMAND_HINT_RE if purpose == "data" else TEST_COMMAND_HINT_RE
        return hint_re.search(executable) is not None
    return False


def validate_gate_command(
    prefix: str, chunk: str, label: str, *, purpose: str
) -> list[str]:
    value = label_value(chunk, label)
    if value is None:
        return [f"{prefix} {label} 必須提供非空白的可執行命令"]
    errors: list[str] = []
    if not (value.startswith("`") and value.endswith("`") and len(value) > 2):
        return [f"{prefix} {label} 必須是反引號包住的可執行命令"]
    raw_command = value[1:-1]
    if SHELL_CONTROL_RE.search(raw_command):
        errors.append(f"{prefix} {label} 不得串接、改向或吞掉失敗狀態")
    try:
        tokens = shlex.split(raw_command)
    except ValueError:
        return errors + [f"{prefix} {label} 命令無法解析"]
    if not command_is_recognized(tokens, purpose=purpose):
        errors.append(f"{prefix} {label} 必須呼叫可辨識的測試或任務執行器")
    hint_re = DATA_COMMAND_HINT_RE if purpose == "data" else TEST_COMMAND_HINT_RE
    if not hint_re.search(raw_command):
        expected = "資料重設" if purpose == "data" else "測試"
        errors.append(f"{prefix} {label} 命令未顯示{expected}用途")
    return errors


def validate_contract_evidence_command(
    prefix: str,
    chunk: str,
    *,
    source: str,
    user_story: str,
    scenario_id: str | None,
    require_contract_id: bool,
    expected_contract_ids: set[str] | None = None,
) -> list[str]:
    value = label_value(chunk, "契約證據")
    if value is None:
        return [f"{prefix} 契約證據必須提供非空白命令或明列不適用"]
    if value == "不適用":
        return []
    if not (value.startswith("`") and value.endswith("`") and len(value) > 2):
        return [f"{prefix} 契約證據必須是反引號包住的可執行命令"]

    errors: list[str] = []
    raw_command = value[1:-1]
    if SHELL_CONTROL_RE.search(raw_command):
        errors.append(f"{prefix} 契約證據命令不得串接、改向或吞掉失敗狀態")
    try:
        tokens = shlex.split(raw_command)
    except ValueError:
        return [f"{prefix} 契約證據命令無法解析"]

    script_indexes = [
        index
        for index, token in enumerate(tokens)
        if token.replace("\\", "/")
        in {EVIDENCE_VALIDATOR_RELATIVE, EVIDENCE_VALIDATOR_ABSOLUTE}
    ]
    valid_invocation = False
    if len(script_indexes) == 1:
        before = tokens[: script_indexes[0]]
        valid_invocation = (
            before == ["uv", "run"]
            or (len(before) == 1 and exact_python_executable(before[0]))
        )
    if not valid_invocation:
        errors.append(f"{prefix} 契約證據命令必須實際呼叫 validate_api_contract_evidence.py")

    def values_after(flag: str) -> list[str]:
        return [
            tokens[index + 1]
            for index, token in enumerate(tokens[:-1])
            if token == flag and not tokens[index + 1].startswith("--")
        ]

    for flag in ("--api-plan", "--evidence", "--user-story", "--require-source"):
        if not values_after(flag):
            errors.append(f"{prefix} 契約證據命令 missing {flag} value")
    if values_after("--user-story") != [user_story]:
        errors.append(f"{prefix} 契約證據命令 must scope {user_story}")
    if values_after("--require-source") != [source]:
        errors.append(f"{prefix} 契約證據命令 must require source {source}")
    if scenario_id is not None:
        if values_after("--scenario") != [scenario_id]:
            errors.append(f"{prefix} 契約證據命令 must scope {scenario_id}")
    elif values_after("--scenario"):
        errors.append(f"{prefix} User Story 閘門不得只選單一 Scenario")
    command_contract_ids = set(values_after("--contract-id"))
    has_contract_id = bool(command_contract_ids)
    if require_contract_id and not has_contract_id:
        errors.append(f"{prefix} Scenario 閘門必須列出 --contract-id")
    if (
        require_contract_id
        and expected_contract_ids
        and command_contract_ids != expected_contract_ids
    ):
        errors.append(
            f"{prefix} --contract-id {sorted(command_contract_ids)} 必須等於契約案例 {sorted(expected_contract_ids)}"
        )
    if not require_contract_id and has_contract_id:
        errors.append(f"{prefix} User Story 閘門必須選取故事全部契約，不得限縮 --contract-id")
    return errors


def validate_scenario_block(
    path_name: str,
    us_id: str,
    heading_id: str,
    block: str,
    layer: str,
) -> list[str]:
    errors: list[str] = []
    prefix = f"{path_name}: {us_id} {heading_id}"

    red_ids = RED_ITEM_RE.findall(block)
    green_ids = GREEN_ITEM_RE.findall(block)
    refactor_ids = REFACTOR_ITEM_RE.findall(block)

    if red_ids != [heading_id]:
        errors.append(f"{prefix} Red ID {red_ids} != heading {heading_id}")
    if green_ids != [heading_id]:
        errors.append(f"{prefix} Green ID {green_ids} != heading {heading_id}")
    if refactor_ids != [heading_id]:
        errors.append(f"{prefix} Refactor ID {refactor_ids} != heading {heading_id}")

    commands = CHECKBOX_RE.findall(block)
    if commands != ["tdd-e2e-red", "tdd-e2e-green", "tdd-e2e-refactor"]:
        errors.append(
            f"{prefix} checkbox order {commands} != red → green → refactor"
        )

    if not has_label(block, "受測行為"):
        errors.append(f"{prefix} missing nested 受測行為")
    if not has_label(block, "實作計畫"):
        errors.append(f"{prefix} missing nested 實作計畫")
    if not has_label(block, "整理範圍"):
        errors.append(f"{prefix} missing nested 整理範圍")

    required_fields = SLICE_RED_FIELDS if layer in {"後端", "前端"} else RED_FIELDS
    for field in required_fields:
        if not has_label(block, field):
            errors.append(f"{prefix} 受測行為 missing {field}")

    if "本則不驗證" not in block:
        errors.append(f"{prefix} Green missing 本則不驗證")

    return errors


def validate_v2_layer_scenario(
    path_name: str,
    us_id: str,
    heading_id: str,
    block: str,
    layer: str,
) -> list[str]:
    errors = validate_scenario_block(path_name, us_id, heading_id, block, "後端")
    prefix = f"{path_name}: {us_id} {heading_id}"

    gate_ids = SCENARIO_GATE_RE.findall(block)
    if gate_ids != [heading_id]:
        errors.append(f"{prefix} 層內全綠閘門 ID {gate_ids} != heading {heading_id}")
    gate_match = SCENARIO_GATE_RE.search(block)
    red_match = RED_ITEM_RE.search(block)
    green_match = GREEN_ITEM_RE.search(block)
    refactor_matches = list(REFACTOR_ITEM_RE.finditer(block))
    refactor_match = refactor_matches[-1] if refactor_matches else None
    if (
        gate_match is not None
        and refactor_match is not None
        and gate_match.start() < refactor_match.end()
    ):
        errors.append(f"{prefix} 層內全綠閘門必須位於 Refactor 之後")
    refactor_boundary_index = block.rfind("不准擴到")
    if (
        refactor_boundary_index < 0
        or refactor_match is None
        or refactor_boundary_index < refactor_match.end()
    ):
        errors.append(f"{prefix} Refactor 必須明列不准擴到的需求邊界")
    elif gate_match is not None and gate_match.start() < refactor_boundary_index:
        errors.append(f"{prefix} 層內全綠閘門必須位於完整 Refactor 邊界之後")

    behavior_positions = label_positions(block, "受測行為")
    implementation_positions = label_positions(block, "實作計畫")
    refactor_scope_positions = label_positions(block, "整理範圍")
    behavior_position = behavior_positions[0] if behavior_positions else None
    implementation_position = (
        implementation_positions[0] if implementation_positions else None
    )
    refactor_scope_position = (
        refactor_scope_positions[0] if refactor_scope_positions else None
    )
    if (
        red_match is not None
        and green_match is not None
        and (
            len(behavior_positions) != 1
            or behavior_position is None
            or not red_match.end() <= behavior_position < green_match.start()
        )
    ):
        errors.append(f"{prefix} 受測行為必須位於 Red 區塊")
    if (
        green_match is not None
        and refactor_match is not None
        and (
            len(implementation_positions) != 1
            or implementation_position is None
            or not green_match.end() <= implementation_position < refactor_match.start()
            or "本則不驗證" not in block[green_match.end() : refactor_match.start()]
        )
    ):
        errors.append(f"{prefix} 實作計畫與本則不驗證必須位於 Green 區塊")
    if (
        refactor_match is not None
        and gate_match is not None
        and (
            len(refactor_scope_positions) != 1
            or refactor_scope_position is None
            or not refactor_match.end() <= refactor_scope_position < gate_match.start()
            or "不准擴到" not in block[refactor_match.end() : gate_match.start()]
        )
    ):
        errors.append(f"{prefix} 整理範圍與不准擴到必須位於 Refactor 區塊")

    for label in ("契約案例", "累積測試", "契約證據", "完成"):
        if not has_label(block, label):
            errors.append(f"{prefix} missing {label}")

    gate_region = block.split("User Story 層內全綠閘門", 1)[-1]
    if "User Story 完成閘門" in gate_region:
        gate_region = gate_region.split("User Story 完成閘門", 1)[0]
    if CHECKBOX_RE.search(gate_region) or any(
        has_label(gate_region, label)
        for label in ("受測行為", "實作計畫", "整理範圍")
    ):
        errors.append(f"{prefix} 層內全綠閘門之後不得再出現 RGB 階段內容")
    errors.extend(
        validate_gate_command(prefix, gate_region, "累積測試", purpose="test")
    )
    if not label_value(gate_region, "完成"):
        errors.append(f"{prefix} 層內全綠閘門必須在自身區塊明列完成條件")
    source = "backend-contract" if layer == "後端" else "frontend-mock"
    contract_value = label_value(block, "契約案例")
    evidence_value = label_value(gate_region, "契約證據")
    if not contract_value:
        errors.append(f"{prefix} 契約案例必須列出契約 ID 或明列不適用")
    if (contract_value == "不適用") != (evidence_value == "不適用"):
        errors.append(f"{prefix} 契約案例與契約證據的不適用狀態必須一致")
    errors.extend(
        validate_contract_evidence_command(
            prefix,
            gate_region,
            source=source,
            user_story=us_id,
            scenario_id=heading_id,
            require_contract_id=True,
            expected_contract_ids=set(
                re.findall(r"\bAPI-\d{3}-C\d+\b", contract_value or "")
            ),
        )
    )
    expected_us_number = us_id.removeprefix("US-")
    scenario_us_number = heading_id.split("-")[1]
    if scenario_us_number != expected_us_number:
        errors.append(f"{prefix} Scenario does not belong to {us_id}")

    return errors


def validate_v2_integration_scenario(
    path_name: str,
    us_id: str,
    heading_id: str,
    block: str,
) -> list[str]:
    errors: list[str] = []
    prefix = f"{path_name}: {us_id} {heading_id}"

    if CHECKBOX_RE.search(block):
        errors.append(f"{prefix} integration must not contain TDD phase checkboxes")
    if re.search(r"(?i)預期\s*(?:TDD\s*)?Red", block):
        errors.append(f"{prefix} integration must not invent an expected Red")

    gate_ids = INTEGRATION_GATE_RE.findall(block)
    if gate_ids != [heading_id]:
        errors.append(f"{prefix} 完全端對端驗收 ID {gate_ids} != heading {heading_id}")

    for label in (
        "前置閘門",
        "Mock",
        "前端",
        "API",
        "後端",
        "資料",
        "執行",
        "觀測",
        "期望",
        "契約案例",
        "契約證據",
        "失敗路由",
    ):
        if not has_label(block, label):
            errors.append(f"{prefix} missing {label}")

    contract_value = label_value(block, "契約案例")
    evidence_value = label_value(block, "契約證據")
    if not contract_value:
        errors.append(f"{prefix} 契約案例必須列出契約 ID")
    if (contract_value == "不適用") != (evidence_value == "不適用"):
        errors.append(f"{prefix} 契約案例與契約證據的不適用狀態必須一致")

    errors.extend(
        validate_contract_evidence_command(
            prefix,
            block,
            source="integration",
            user_story=us_id,
            scenario_id=None,
            require_contract_id=False,
        )
    )
    errors.extend(validate_gate_command(prefix, block, "資料", purpose="data"))
    errors.extend(validate_gate_command(prefix, block, "執行", purpose="test"))

    fixed_values = {
        "Mock": "停用",
        "前端": "真實執行期頁面",
        "API": "正式 API",
        "後端": "真實後端",
    }
    for label, expected in fixed_values.items():
        if label_value(block, label) != expected:
            errors.append(f"{prefix} {label} must be exactly {expected}")
    if has_mock_contradiction(block):
        errors.append(f"{prefix} integration contains text that keeps or re-enables Mock")
    if heading_id != us_id:
        errors.append(f"{prefix} integration heading must equal outer User Story")

    return errors


def validate_task_file(
    path: Path, layer: str, expected_ids: list[str], *, require_v2: bool
) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing file: {path}"]

    text = path.read_text(encoding="utf-8")
    has_v2_marker = bool(FLOW_V2_RE.search(text))
    is_v2 = has_v2_marker or require_v2
    if require_v2 and not has_v2_marker:
        errors.append(f"{path.name}: 流程版本 2 package 缺少 `流程版本: 2`")
    if PLACEHOLDER_RE.search(text):
        errors.append(f"{path.name}: unresolved placeholders remain")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: missing section {section}")

    if "## 2. Setup" in text or re.search(r"(?m)^## 2\.\s*Setup\b", text):
        errors.append(f"{path.name}: section 2 must be 環境建立, not Setup")

    if "完成定義" in text:
        errors.append(f"{path.name}: must not contain 完成定義")

    if FORBIDDEN_VERIFY_RE.search(text):
        errors.append(f"{path.name}: must not contain US-level Red verify item")

    if FORBIDDEN_US_GREEN_RE.search(text):
        errors.append(f"{path.name}: must not contain US-level Green 讓本 US 既有 Red 全綠")

    sec3 = section_three(text)
    us_matches = list(US_RE.finditer(sec3))
    if not us_matches:
        errors.append(f"{path.name}: no User Story headings under section 3")

    actual_ids: list[str] = []
    for i, match in enumerate(us_matches):
        start = match.end()
        end = us_matches[i + 1].start() if i + 1 < len(us_matches) else len(sec3)
        block = sec3[start:end]
        us_id = match.group(1)

        if "#### AC / Edge" not in block:
            errors.append(f"{path.name}: {us_id} missing #### AC / Edge")

        rgb_headings = US_LEVEL_RGB_HEADING_RE.findall(block)
        if rgb_headings:
            errors.append(
                f"{path.name}: {us_id} must not use US-level #### {', '.join(rgb_headings)}"
            )

        scenario_matches = list(SCENARIO_HEADING_RE.finditer(block))
        if not scenario_matches:
            errors.append(f"{path.name}: {us_id} has no Scenario heading")

        for j, scenario in enumerate(scenario_matches):
            heading_id = scenario.group(1)
            if layer == "整合":
                if not re.fullmatch(r"US-\d+", heading_id):
                    errors.append(
                        f"{path.name}: {us_id} integration heading {heading_id} must be US-n"
                    )
            elif not re.fullmatch(r"S-\d+-\d+", heading_id):
                errors.append(
                    f"{path.name}: {us_id} {layer} heading {heading_id} must be S-n-m"
                )

            chunk_end = (
                scenario_matches[j + 1].start()
                if j + 1 < len(scenario_matches)
                else len(block)
            )
            chunk = block[scenario.start() : chunk_end]
            actual_ids.append(heading_id)
            if is_v2 and layer == "整合":
                errors.extend(
                    validate_v2_integration_scenario(
                        path.name, us_id, heading_id, chunk
                    )
                )
            elif is_v2:
                errors.extend(
                    validate_v2_layer_scenario(
                        path.name, us_id, heading_id, chunk, layer
                    )
                )
            else:
                errors.extend(
                    validate_scenario_block(path.name, us_id, heading_id, chunk, layer)
                )

        if is_v2 and layer != "整合":
            us_gate_ids = US_GATE_RE.findall(block)
            if us_gate_ids != [us_id]:
                errors.append(
                    f"{path.name}: {us_id} completion gate IDs {us_gate_ids} != [{us_id}]"
                )
            us_gate_match = US_GATE_RE.search(block)
            scenario_gate_matches = list(SCENARIO_GATE_RE.finditer(block))
            if (
                us_gate_match is not None
                and scenario_matches
                and (
                    us_gate_match.start() < scenario_matches[-1].start()
                    or (
                        scenario_gate_matches
                        and us_gate_match.start() < scenario_gate_matches[-1].end()
                    )
                )
            ):
                errors.append(
                    f"{path.name}: {us_id} 完成閘門必須位於最後一則 Scenario 的層內全綠閘門之後"
                )
            for label in ("User Story 測試", "全層回歸", "契約證據"):
                if not has_label(block, label):
                    errors.append(f"{path.name}: {us_id} completion gate missing {label}")
            completion_region = block.split("User Story 完成閘門", 1)[-1]
            errors.extend(
                validate_gate_command(
                    f"{path.name}: {us_id} completion gate",
                    completion_region,
                    "User Story 測試",
                    purpose="test",
                )
            )
            errors.extend(
                validate_gate_command(
                    f"{path.name}: {us_id} completion gate",
                    completion_region,
                    "全層回歸",
                    purpose="test",
                )
            )
            source = "backend-contract" if layer == "後端" else "frontend-mock"
            completion_evidence = label_value(completion_region, "契約證據")
            story_has_contract = bool(re.search(r"\bAPI-\d{3}-C\d+\b", block))
            if story_has_contract and completion_evidence == "不適用":
                errors.append(
                    f"{path.name}: {us_id} completion gate 有契約案例，不得把契約證據標成不適用"
                )
            errors.extend(
                validate_contract_evidence_command(
                    f"{path.name}: {us_id} completion gate",
                    completion_region,
                    source=source,
                    user_story=us_id,
                    scenario_id=None,
                    require_contract_id=False,
                )
            )

    if actual_ids != expected_ids:
        errors.append(
            f"{path.name}: Scenario IDs {actual_ids} != e2e ## {layer} {expected_ids}"
        )

    return errors


def main() -> int:
    args = parse_args()
    package = Path(args.package)
    if not package.is_dir():
        print(f"ERROR: package directory not found: {package}", file=sys.stderr)
        return 2

    e2e_path = package / "e2e-test-plan.md"
    if not e2e_path.is_file():
        print(f"ERROR: missing {e2e_path}", file=sys.stderr)
        return 2

    e2e_text = e2e_path.read_text(encoding="utf-8")
    task_dir = package / "task-plan"
    errors: list[str] = []

    api_path = package / "system-analyze" / "api-plan.md"
    api_text = api_path.read_text(encoding="utf-8") if api_path.is_file() else ""
    task_texts = {
        filename: (task_dir / filename).read_text(encoding="utf-8")
        for filename in LAYER_FILES.values()
        if (task_dir / filename).is_file()
    }
    has_machine_contract = "## 可機械驗證契約" in api_text
    package_v2 = (
        has_machine_contract
        or bool(FLOW_V2_RE.search(api_text))
        or bool(FLOW_V2_RE.search(e2e_text))
        or any(FLOW_V2_RE.search(text) for text in task_texts.values())
    )
    if has_machine_contract and not FLOW_V2_RE.search(api_text):
        errors.append("api-plan.md: 可機械驗證契約缺少 `流程版本: 2`")
    if package_v2 and not FLOW_V2_RE.search(e2e_text):
        errors.append("e2e-test-plan.md: 流程版本 2 package 缺少 `流程版本: 2`")

    for layer, filename in LAYER_FILES.items():
        expected = e2e_layer_scenarios(e2e_text, layer)
        errors.extend(
            validate_task_file(
                task_dir / filename, layer, expected, require_v2=package_v2
            )
        )

    if errors:
        print("INVALID")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
