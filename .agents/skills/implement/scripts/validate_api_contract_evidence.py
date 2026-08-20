# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

MACHINE_CONTRACT_HEADING = "## 可機械驗證契約"
ALLOWED_SOURCES = {"backend-contract", "frontend-mock", "integration"}
SHELL_CONTROL_RE = re.compile(r"(?:&&|\|\||[;|<>]|\$\(|`)")
TEST_COMMAND_HINT_RE = re.compile(
    r"(?i)(?:^|[\s:/_.-])(test|tests|e2e|spec|specs|playwright|cypress|pytest|rspec|verify|check)(?:$|[\s:/_.-])"
)
SCRIPT_TEST_HINT_RE = re.compile(
    r"(?i)(?:^|[\s:/_.-])(test|tests|e2e|spec|specs|verify|check)(?:$|[\s:/_.-])"
)
ISO_TIMESTAMP_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?(?:Z|[+-]\d{2}:\d{2})"
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
RECORD_FIELDS = {
    "contract_id",
    "scenario_id",
    "method",
    "path",
    "status",
    "request",
    "response",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate test-generated API evidence against api-plan.md."
    )
    parser.add_argument("--api-plan", required=True, help="Path to api-plan.md")
    parser.add_argument(
        "--evidence", action="append", required=True, help="Evidence JSON; repeatable"
    )
    parser.add_argument("--user-story")
    parser.add_argument("--scenario", action="append", default=[])
    parser.add_argument("--contract-id", action="append", default=[])
    parser.add_argument(
        "--require-source",
        action="append",
        choices=sorted(ALLOWED_SOURCES),
        required=True,
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def load_contracts(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path}") from exc
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == MACHINE_CONTRACT_HEADING)
        fence_start = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "```json")
        fence_end = next(i for i in range(fence_start + 1, len(lines)) if lines[i].strip() == "```")
    except StopIteration as exc:
        raise ValueError("api-plan.md 缺少可機械驗證契約 JSON") from exc
    try:
        payload = json.loads("\n".join(lines[fence_start + 1 : fence_end]))
    except json.JSONDecodeError as exc:
        raise ValueError(f"api-plan.md 契約 JSON 無法解析: {exc}") from exc
    contracts = payload.get("contracts") if isinstance(payload, dict) else None
    if not isinstance(contracts, list) or not contracts:
        raise ValueError("api-plan.md 契約 contracts 必須是非空陣列")
    return [item for item in contracts if isinstance(item, dict)]


def value_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    return False


def validate_value(value: Any, schema: Any, label: str) -> list[str]:
    if not isinstance(schema, dict):
        return [f"{label}: schema must be an object"]
    if not schema:
        return [f'{label}: empty schema is forbidden; use {{"type":"null"}} for no body']
    errors: list[str] = []
    expected = schema.get("type")
    if not isinstance(expected, str) or not value_type_matches(value, expected):
        return [f"{label}: value does not match type {expected}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{label}: value does not match const")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{label}: value is not in enum")

    if expected == "object" and isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for name in required:
                if name not in value:
                    errors.append(f"{label}: missing required property {name}")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for name, child_schema in properties.items():
                if name in value:
                    errors.extend(validate_value(value[name], child_schema, f"{label}.{name}"))
            if schema.get("additionalProperties") is False:
                for name in value.keys() - properties.keys():
                    errors.append(f"{label}: unexpected property {name}")

    if expected == "array" and isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            errors.extend(validate_value(item, schema["items"], f"{label}[{index}]"))
    return errors


def path_matches(template: str, actual: str) -> bool:
    pattern = re.escape(template)
    pattern = re.sub(r"\\\{[^{}]+\\\}", r"[^/]+", pattern)
    pattern = re.sub(r":[A-Za-z_][A-Za-z0-9_]*", r"[^/]+", pattern)
    return re.fullmatch(pattern, actual) is not None


def user_story_for_scenario(scenario_id: str) -> str | None:
    if re.fullmatch(r"US-\d+", scenario_id):
        return scenario_id
    match = re.fullmatch(r"S-(\d+)-\d+", scenario_id)
    return f"US-{match.group(1)}" if match else None


def executable_name(token: str) -> str:
    return token.rsplit("/", 1)[-1]


def exact_python_executable(token: str) -> bool:
    return PYTHON_EXECUTABLE_RE.fullmatch(executable_name(token)) is not None


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


def command_is_recognized(tokens: list[str]) -> bool:
    if not tokens:
        return False
    executable = executable_name(tokens[0])
    raw_command = " ".join(tokens)
    if executable in FORBIDDEN_FAKE_COMMANDS:
        return False
    if any(token in NON_EXECUTING_TEST_ARGS for token in tokens[1:]):
        return False
    if executable == "npm":
        payload_index = manager_payload_index(tokens)
        if payload_index is None:
            return False
        payload = executable_name(tokens[payload_index])
        if payload in FORBIDDEN_FAKE_COMMANDS:
            return False
        if payload == "run":
            target = wrapper_payload(tokens, payload_index + 1)
            return (
                target is not None
                and target not in FORBIDDEN_FAKE_COMMANDS
                and SCRIPT_TEST_HINT_RE.search(target) is not None
            )
        if payload in {"exec", "x"}:
            runner_index = wrapper_payload_index(tokens, payload_index + 1)
            return (
                runner_index is not None
                and test_runner_invocation_is_valid(tokens, runner_index)
            )
        return TEST_COMMAND_HINT_RE.search(payload) is not None
    if executable in {"pnpm", "yarn", "bun"}:
        if any(executable_name(token) in FORBIDDEN_FAKE_COMMANDS for token in tokens[1:]):
            return False
        payload_index = manager_payload_index(tokens)
        if payload_index is None:
            return False
        payload = executable_name(tokens[payload_index])
        if payload == "run":
            target = wrapper_payload(tokens, payload_index + 1)
            return (
                target is not None
                and target not in FORBIDDEN_FAKE_COMMANDS
                and SCRIPT_TEST_HINT_RE.search(target) is not None
            )
        if payload in {"exec", "dlx", "x"}:
            runner_index = wrapper_payload_index(tokens, payload_index + 1)
            return (
                runner_index is not None
                and test_runner_invocation_is_valid(tokens, runner_index)
            )
        if payload in KNOWN_TEST_RUNNERS:
            return test_runner_invocation_is_valid(tokens, payload_index)
        return SCRIPT_TEST_HINT_RE.search(payload) is not None
    if executable in {"npx", "bunx"}:
        if any(executable_name(token) in FORBIDDEN_FAKE_COMMANDS for token in tokens[1:]):
            return False
        payload_index = manager_payload_index(tokens)
        return (
            payload_index is not None
            and test_runner_invocation_is_valid(tokens, payload_index)
        )
    if executable == "uv":
        return len(tokens) >= 3 and tokens[1] == "run" and command_is_recognized(tokens[2:])
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
        return len(tokens) >= 2 and TEST_COMMAND_HINT_RE.search(raw_command) is not None
    if tokens[0].startswith("./") or executable.endswith((".sh", ".bash")):
        return TEST_COMMAND_HINT_RE.search(executable) is not None
    return False


def validate_producer_command(command: str, label: str) -> list[str]:
    errors: list[str] = []
    if SHELL_CONTROL_RE.search(command):
        errors.append(f"{label}: producer.command must not chain, redirect, or mask failure")
    try:
        tokens = shlex.split(command)
    except ValueError:
        return errors + [f"{label}: producer.command cannot be parsed"]
    if not command_is_recognized(tokens):
        errors.append(f"{label}: producer.command must call a recognized test runner")
    if not TEST_COMMAND_HINT_RE.search(command):
        errors.append(f"{label}: producer.command does not identify a test command")
    return errors


def valid_generated_at(value: Any) -> bool:
    if not isinstance(value, str) or ISO_TIMESTAMP_RE.fullmatch(value) is None:
        return False
    normalized = re.sub(
        r"\.(\d{1,9})(?=Z|[+-])",
        lambda match: "." + (match.group(1) + "000000")[:6],
        value,
    )
    normalized = normalized[:-1] + "+00:00" if normalized.endswith("Z") else normalized
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def select_contracts(contracts: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    contract_filter = set(args.contract_id)
    for contract in contracts:
        if args.user_story and contract.get("user_story") != args.user_story:
            continue
        if contract_filter and contract.get("contract_id") not in contract_filter:
            continue
        selected.append(contract)
    return selected


def validate_evidence(
    selected: list[dict[str, Any]],
    all_contract_ids: set[str],
    evidence_paths: list[Path],
    required_sources: set[str],
    allowed_scenarios: set[str],
) -> list[str]:
    errors: list[str] = []
    contracts_by_id = {item.get("contract_id"): item for item in selected}
    records_by_key: dict[tuple[str, str], list[dict[str, Any]]] = {}

    for path in evidence_paths:
        payload = load_json(path)
        if not isinstance(payload, dict):
            errors.append(f"{path}: top level must be an object")
            continue
        source = payload.get("source")
        if payload.get("version") != 1:
            errors.append(f"{path}: version must be 1")
        if source not in ALLOWED_SOURCES:
            errors.append(f"{path}: invalid source {source}")
            continue
        producer = payload.get("producer")
        if not isinstance(producer, dict):
            errors.append(f"{path}: producer.command is required")
        else:
            command = producer.get("command")
            if not isinstance(command, str) or not command:
                errors.append(f"{path}: producer.command is required")
            else:
                errors.extend(validate_producer_command(command, str(path)))
            generated_at = producer.get("generated_at")
            if not valid_generated_at(generated_at):
                errors.append(f"{path}: producer.generated_at must be ISO-8601 with timezone")
        records = payload.get("records")
        if not isinstance(records, list):
            errors.append(f"{path}: records must be an array")
            continue
        for index, record in enumerate(records):
            label = f"{path}: records[{index}]"
            if not isinstance(record, dict):
                errors.append(f"{label} must be an object")
                continue
            missing = RECORD_FIELDS - record.keys()
            if missing:
                errors.append(f"{label} missing {sorted(missing)}")
                continue
            unexpected = record.keys() - RECORD_FIELDS
            if unexpected:
                errors.append(f"{label} unexpected fields {sorted(unexpected)}")
            for field in ("contract_id", "scenario_id", "method", "path"):
                if not isinstance(record[field], str) or not record[field]:
                    errors.append(f"{label}: {field} must be a non-empty string")
            if not all(
                isinstance(record[field], str) and record[field]
                for field in ("contract_id", "scenario_id", "method", "path")
            ):
                continue
            contract_id = record["contract_id"]
            if contract_id not in all_contract_ids:
                errors.append(f"{label}: unknown contract_id {contract_id}")
                continue
            contract = contracts_by_id.get(contract_id)
            if contract is None:
                continue
            if source not in contract.get("required_evidence", []):
                errors.append(f"{label}: source {source} is not required by {contract_id}")
            scenario_story = user_story_for_scenario(record["scenario_id"])
            if scenario_story is None:
                errors.append(f"{label}: invalid scenario_id {record['scenario_id']}")
            elif scenario_story != contract.get("user_story"):
                errors.append(
                    f"{label}: scenario_id belongs to {scenario_story}, not {contract.get('user_story')}"
                )
            if source == "integration" and record["scenario_id"] != contract.get(
                "user_story"
            ):
                errors.append(
                    f"{label}: integration evidence scenario_id must equal {contract.get('user_story')}"
                )
            if source != "integration" and not re.fullmatch(
                r"S-\d+-\d+", record["scenario_id"]
            ):
                errors.append(
                    f"{label}: {source} evidence scenario_id must use S-n-m"
                )
            if allowed_scenarios and record["scenario_id"] not in allowed_scenarios:
                errors.append(f"{label}: scenario_id is outside the requested scope")
            if record["method"] != contract.get("method"):
                errors.append(f"{label}: method does not match {contract_id}")
            if not path_matches(str(contract.get("path")), str(record["path"])):
                errors.append(f"{label}: path does not match {contract_id}")
            if record["status"] != contract.get("status"):
                errors.append(f"{label}: status does not match {contract_id}")
            errors.extend(validate_value(record["request"], contract.get("request"), f"{label}.request"))
            errors.extend(validate_value(record["response"], contract.get("response"), f"{label}.response"))
            records_by_key.setdefault((contract_id, source), []).append(record)

    for contract in selected:
        contract_id = contract.get("contract_id")
        sources = set(contract.get("required_evidence", []))
        sources &= required_sources if required_sources else sources
        for source in sources:
            if not records_by_key.get((contract_id, source)):
                errors.append(f"{contract_id}: missing evidence source {source}")
    for source in required_sources:
        if not any(source in set(contract.get("required_evidence", [])) for contract in selected):
            errors.append(f"requested source {source} is not required by selected contracts")
    return errors


def main() -> int:
    args = parse_args()
    try:
        contracts = load_contracts(Path(args.api_plan))
        selected = select_contracts(contracts, args)
        if not selected:
            raise ValueError("filters selected no API contracts")
        errors = validate_evidence(
            selected,
            {
                item["contract_id"]
                for item in contracts
                if isinstance(item.get("contract_id"), str)
            },
            [Path(item) for item in args.evidence],
            set(args.require_source),
            set(args.scenario),
        )
    except ValueError as exc:
        print(f"INVALID\n- {exc}")
        return 1
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
