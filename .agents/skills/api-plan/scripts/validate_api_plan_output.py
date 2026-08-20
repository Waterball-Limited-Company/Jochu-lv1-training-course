# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
ENTITY_HEADING_RE = re.compile(r"^## 資料實體：.+$")
ENDPOINT_HEADING_RE = re.compile(r"^### Endpoint：`.+`$")
STATUS_HEADING_RE = re.compile(r"^##### .+$")
TITLE_RE = re.compile(r"^# API 計畫：.+$")
BRANCH_RE = re.compile(r"^\*\*功能分支\*\*:\s*`[^`]+`$")
CREATED_DATE_RE = re.compile(r"^\*\*建立日期\*\*:\s*\d{4}-\d{2}-\d{2}$")
STATUS_RE = re.compile(r"^\*\*狀態\*\*:\s*.+$")
FLOW_VERSION_RE = re.compile(r"^流程版本:\s*2$")
JSON_FENCE_RE = re.compile(r"^```json\s*$")
BAD_ERROR_CODE_RE = re.compile(r'"code"\s*:\s*"Status Code"')
ENDPOINT_SIGNATURE_RE = re.compile(
    r"^### Endpoint：`(GET|POST|PUT|PATCH|DELETE)\s+([^`]+)`$"
)
STATUS_CODE_RE = re.compile(r"^#####\s+(\d{3})\b")
CONTRACT_ID_RE = re.compile(r"^API-\d{3}-C\d+$")
MISSING_JSON_EXAMPLE = object()

MACHINE_CONTRACT_HEADING = "## 可機械驗證契約"
CONTRACT_REQUIRED_FIELDS = {
    "contract_id",
    "user_story",
    "required_evidence",
    "method",
    "path",
    "status",
    "request",
    "response",
}
CONTRACT_ALLOWED_FIELDS = CONTRACT_REQUIRED_FIELDS
ALLOWED_EVIDENCE_SOURCES = {"backend-contract", "frontend-mock", "integration"}
ALLOWED_SCHEMA_TYPES = {
    "null",
    "boolean",
    "integer",
    "number",
    "string",
    "array",
    "object",
}

REQUIRED_TOP_LEVEL = [
    "## API Schema 描述",
    "## 共通錯誤格式",
    "## 追溯總表（快速 Review）",
    "## 假設",
]

ENDPOINT_REQUIRED_MARKERS = [
    "#### Parameters",
    "#### Request body",
    "#### Responses",
    "#### 測試規劃",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structure of an api-plan Markdown artifact."
    )
    parser.add_argument("--input", required=True, help="Path to the api-plan.md file")
    return parser.parse_args()


def find_ranges(lines: list[str], heading_re: re.Pattern[str]) -> list[tuple[int, int]]:
    headings = [idx for idx, line in enumerate(lines) if heading_re.match(line.strip())]
    if not headings:
        return []

    stop_markers = {
        MACHINE_CONTRACT_HEADING,
        "## 追溯總表（快速 Review）",
        "## 假設",
    }
    stop_index = next(
        (idx for idx, line in enumerate(lines) if line.strip() in stop_markers),
        len(lines),
    )

    ranges: list[tuple[int, int]] = []
    for position, start in enumerate(headings):
        if position + 1 < len(headings):
            end = headings[position + 1]
        else:
            end = stop_index
        ranges.append((start, end))
    return ranges


def section_has_marker(section_lines: list[str], marker: str) -> bool:
    return any(line.strip() == marker for line in section_lines)


def status_has_json_fence(section_lines: list[str], status_idx: int) -> bool:
    cursor = status_idx + 1
    while cursor < len(section_lines):
        stripped = section_lines[cursor].strip()
        if not stripped:
            cursor += 1
            continue
        if STATUS_HEADING_RE.match(stripped) or stripped.startswith("#### "):
            return False
        if JSON_FENCE_RE.match(stripped):
            return True
        cursor += 1
    return False


def validate_common_error_section(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next(
        (idx for idx, line in enumerate(lines) if line.strip() == "## 共通錯誤格式"),
        None,
    )
    if start is None:
        return errors

    end = next(
        (
            idx
            for idx, line in enumerate(lines[start + 1 :], start=start + 1)
            if line.startswith("## ")
        ),
        len(lines),
    )
    section = "\n".join(lines[start:end])
    if '"error"' not in section:
        errors.append("共通錯誤格式: missing `error` envelope example")
    if '"code"' not in section or '"message"' not in section or '"details"' not in section:
        errors.append("共通錯誤格式: envelope must include code / message / details")
    if BAD_ERROR_CODE_RE.search(section):
        errors.append("共通錯誤格式: `code` must not be the placeholder `Status Code`")
    if "```json" not in section:
        errors.append("共通錯誤格式: missing json code fence")
    return errors


def validate_assumption_section(lines: list[str]) -> list[str]:
    errors: list[str] = []
    start = next((idx for idx, line in enumerate(lines) if line.strip() == "## 假設"), None)
    if start is None:
        return errors

    if start != max(idx for idx, line in enumerate(lines) if line.startswith("## ")):
        errors.append("## 假設 must be the last top-level section")

    bullet_count = 0
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("- "):
            bullet_count += 1

    if bullet_count < 1:
        errors.append("## 假設 must contain at least one `- ` bullet item")
    return errors


def validate_endpoint(section_lines: list[str], label: str) -> list[str]:
    errors: list[str] = []
    text = "\n".join(section_lines)

    for marker in ENDPOINT_REQUIRED_MARKERS:
        if not section_has_marker(section_lines, marker):
            errors.append(f"{label}: missing `{marker}`")

    if "| 對應 FR |" not in text and "對應 FR" not in text:
        errors.append(f"{label}: missing 對應 FR")

    status_indexes = [
        idx for idx, line in enumerate(section_lines) if STATUS_HEADING_RE.match(line.strip())
    ]
    if not status_indexes:
        errors.append(f"{label}: missing at least one `#####` response status heading")
    else:
        for idx in status_indexes:
            heading = section_lines[idx].strip()
            if not status_has_json_fence(section_lines, idx):
                errors.append(f"{label}: `{heading}` missing json code fence body")

    if "| 情境" not in text or "預期 Status" not in text:
        errors.append(f"{label}: 測試規劃 table must include 情境 and 預期 Status")

    return errors


def validate_entity(section_lines: list[str], label: str) -> list[str]:
    errors: list[str] = []
    text = "\n".join(section_lines)

    if "### 對應 User Story" not in text:
        errors.append(f"{label}: missing `### 對應 User Story`")
    if "### 實體形狀（欄位 + 範例資料）" not in text:
        errors.append(f"{label}: missing `### 實體形狀（欄位 + 範例資料）`")
    if "欄位說明（非型別定義）" not in text:
        errors.append(f"{label}: missing 欄位說明（非型別定義）")
    if "與資料實體 DDL Mapping" not in text:
        errors.append(f"{label}: missing DDL Mapping hint")

    endpoint_starts = [
        idx for idx, line in enumerate(section_lines) if ENDPOINT_HEADING_RE.match(line.strip())
    ]
    if not endpoint_starts:
        errors.append(f"{label}: missing at least one Endpoint")
        return errors

    for position, start in enumerate(endpoint_starts):
        end = (
            endpoint_starts[position + 1]
            if position + 1 < len(endpoint_starts)
            else len(section_lines)
        )
        endpoint_lines = section_lines[start:end]
        heading = section_lines[start].strip()
        errors.extend(validate_endpoint(endpoint_lines, f"{label} / {heading}"))

    return errors


def extract_machine_contracts(lines: list[str]) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    start = next(
        (idx for idx, line in enumerate(lines) if line.strip() == MACHINE_CONTRACT_HEADING),
        None,
    )
    if start is None:
        return None, [f"missing `{MACHINE_CONTRACT_HEADING}`"]

    fence_start = next(
        (
            idx
            for idx in range(start + 1, len(lines))
            if lines[idx].strip() == "```json"
        ),
        None,
    )
    if fence_start is None:
        return None, ["可機械驗證契約: missing json fence"]
    fence_end = next(
        (
            idx
            for idx in range(fence_start + 1, len(lines))
            if lines[idx].strip() == "```"
        ),
        None,
    )
    if fence_end is None:
        return None, ["可機械驗證契約: json fence is not closed"]

    try:
        payload = json.loads("\n".join(lines[fence_start + 1 : fence_end]))
    except json.JSONDecodeError as exc:
        return None, [f"可機械驗證契約: invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        errors.append("可機械驗證契約: top level must be an object")
        return None, errors
    return payload, errors


def validate_schema(schema: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(schema, dict):
        return [f"{label}: schema must be an object"]
    if not schema:
        return [f'{label}: empty schema is forbidden; use {{"type":"null"}} for no body']

    schema_type = schema.get("type")
    if schema_type not in ALLOWED_SCHEMA_TYPES:
        errors.append(f"{label}: unsupported or missing schema type `{schema_type}`")

    if "required" in schema:
        required = schema["required"]
        if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
            errors.append(f"{label}: required must be a list of strings")

    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict):
            errors.append(f"{label}: properties must be an object")
        else:
            for name, child in properties.items():
                errors.extend(validate_schema(child, f"{label}.properties.{name}"))

    if "items" in schema:
        errors.extend(validate_schema(schema["items"], f"{label}.items"))

    if "enum" in schema and not isinstance(schema["enum"], list):
        errors.append(f"{label}: enum must be a list")
    if "additionalProperties" in schema and not isinstance(
        schema["additionalProperties"], bool
    ):
        errors.append(f"{label}: additionalProperties must be boolean")
    return errors


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


def validate_example_against_schema(value: Any, schema: Any, label: str) -> list[str]:
    if not isinstance(schema, dict):
        return [f"{label}: schema must be an object"]
    if not schema:
        return [f'{label}: empty schema is forbidden; use {{"type":"null"}} for no body']

    expected = schema.get("type")
    if not isinstance(expected, str) or not value_type_matches(value, expected):
        return [f"{label}: example does not match type {expected}"]

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{label}: example does not match const")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{label}: example is not in enum")

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
                    errors.extend(
                        validate_example_against_schema(
                            value[name], child_schema, f"{label}.{name}"
                        )
                    )
            if schema.get("additionalProperties") is False:
                for name in value.keys() - properties.keys():
                    errors.append(f"{label}: unexpected property {name}")

    if expected == "array" and isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            errors.extend(
                validate_example_against_schema(
                    item, schema["items"], f"{label}[{index}]"
                )
            )
    return errors


def parse_response_json_example(
    section_lines: list[str], status_index: int, label: str
) -> tuple[Any, list[str]]:
    cursor = status_index + 1
    while cursor < len(section_lines):
        stripped = section_lines[cursor].strip()
        if STATUS_HEADING_RE.match(stripped) or stripped.startswith("#### "):
            return MISSING_JSON_EXAMPLE, [f"{label}: missing JSON response example"]
        if stripped == "```json":
            fence_end = next(
                (
                    index
                    for index in range(cursor + 1, len(section_lines))
                    if section_lines[index].strip() == "```"
                ),
                None,
            )
            if fence_end is None:
                return MISSING_JSON_EXAMPLE, [f"{label}: JSON response fence is not closed"]
            try:
                return (
                    json.loads("\n".join(section_lines[cursor + 1 : fence_end])),
                    [],
                )
            except json.JSONDecodeError as exc:
                return MISSING_JSON_EXAMPLE, [f"{label}: invalid response JSON: {exc}"]
        cursor += 1
    return MISSING_JSON_EXAMPLE, [f"{label}: missing JSON response example"]


def markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def human_endpoint_contracts(
    lines: list[str],
) -> tuple[dict[tuple[str, str], dict[str, Any]], list[str]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    errors: list[str] = []
    starts = [
        idx for idx, line in enumerate(lines) if ENDPOINT_SIGNATURE_RE.match(line.strip())
    ]
    top_level_stops = {
        MACHINE_CONTRACT_HEADING,
        "## 追溯總表（快速 Review）",
        "## 假設",
    }
    for position, start in enumerate(starts):
        signature = ENDPOINT_SIGNATURE_RE.match(lines[start].strip())
        if signature is None:
            continue
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        for idx in range(start + 1, end):
            if lines[idx].strip() in top_level_stops or lines[idx].startswith("## 資料實體："):
                end = idx
                break
        endpoint_lines = lines[start:end]
        endpoint_label = f"{signature.group(1)} {signature.group(2)}"
        metadata_end = next(
            (
                idx
                for idx, line in enumerate(endpoint_lines)
                if line.strip() == "#### Parameters"
            ),
            len(endpoint_lines),
        )
        metadata_ids = set(
            re.findall(r"API-\d{3}-C\d+", "\n".join(endpoint_lines[:metadata_end]))
        )
        statuses: set[int] = set()
        response_cases: set[tuple[int, str]] = set()
        response_examples: dict[tuple[int, str], Any] = {}
        for line_index, line in enumerate(endpoint_lines):
            heading = line.strip()
            status_match = STATUS_CODE_RE.match(heading)
            if status_match is None:
                continue
            status = int(status_match.group(1))
            statuses.add(status)
            ids = set(re.findall(r"API-\d{3}-C\d+", heading))
            if len(ids) != 1:
                errors.append(
                    f"Endpoint {endpoint_label}: response {status} heading must name exactly one contract_id"
                )
            else:
                contract_id = next(iter(ids))
                response_case = (status, contract_id)
                response_cases.add(response_case)
                example, example_errors = parse_response_json_example(
                    endpoint_lines,
                    line_index,
                    f"Endpoint {endpoint_label}: response {status} / {contract_id}",
                )
                errors.extend(example_errors)
                if example is not MISSING_JSON_EXAMPLE:
                    response_examples[response_case] = example

        test_cases: set[tuple[int, str]] = set()
        test_start = next(
            (
                idx
                for idx, line in enumerate(endpoint_lines)
                if line.strip() == "#### 測試規劃"
            ),
            None,
        )
        if test_start is not None:
            table_lines = [
                line.strip()
                for line in endpoint_lines[test_start + 1 :]
                if line.strip().startswith("|")
            ]
            if not table_lines:
                errors.append(f"Endpoint {endpoint_label}: 測試規劃缺少表格")
            else:
                headers = markdown_cells(table_lines[0])
                if headers[:3] != ["契約案例", "情境", "預期 Status"]:
                    errors.append(
                        f"Endpoint {endpoint_label}: 流程版本 2 測試規劃欄位必須是 契約案例 / 情境 / 預期 Status"
                    )
                for row in table_lines[2:]:
                    cells = markdown_cells(row)
                    if len(cells) < 3:
                        errors.append(
                            f"Endpoint {endpoint_label}: 測試規劃資料列欄位不足"
                        )
                        continue
                    ids = set(re.findall(r"API-\d{3}-C\d+", cells[0]))
                    status_match = re.fullmatch(r"`?(\d{3})`?", cells[2])
                    if len(ids) != 1 or status_match is None:
                        errors.append(
                            f"Endpoint {endpoint_label}: 每個測試規劃資料列必須有一個 contract_id 與三位數 Status"
                        )
                        continue
                    test_cases.add((int(status_match.group(1)), next(iter(ids))))

        key = (signature.group(1), signature.group(2))
        if key in result:
            errors.append(f"duplicate Endpoint section: {endpoint_label}")
        result[key] = {
            "statuses": statuses,
            "metadata_ids": metadata_ids,
            "response_cases": response_cases,
            "response_examples": response_examples,
            "test_cases": test_cases,
        }
    return result, errors


def validate_machine_contracts(lines: list[str]) -> list[str]:
    payload, errors = extract_machine_contracts(lines)
    if payload is None:
        return errors
    if payload.get("version") != 1:
        errors.append("可機械驗證契約: version must be 1")
    contracts = payload.get("contracts")
    if not isinstance(contracts, list) or not contracts:
        return errors + ["可機械驗證契約: contracts must be a non-empty list"]

    human, human_errors = human_endpoint_contracts(lines)
    errors.extend(human_errors)
    seen_ids: set[str] = set()
    machine_cases: set[tuple[str, str, int, str]] = set()
    for index, contract in enumerate(contracts, start=1):
        label = f"可機械驗證契約 contracts[{index}]"
        if not isinstance(contract, dict):
            errors.append(f"{label}: must be an object")
            continue
        missing = CONTRACT_REQUIRED_FIELDS - set(contract)
        if missing:
            errors.append(f"{label}: missing fields {', '.join(sorted(missing))}")
            continue
        unexpected = set(contract) - CONTRACT_ALLOWED_FIELDS
        if unexpected:
            errors.append(
                f"{label}: unsupported fields {', '.join(sorted(unexpected))}"
            )

        contract_id = contract["contract_id"]
        if not isinstance(contract_id, str) or not CONTRACT_ID_RE.fullmatch(contract_id):
            errors.append(f"{label}: invalid contract_id `{contract_id}`")
        elif contract_id in seen_ids:
            errors.append(f"{label}: duplicate contract_id `{contract_id}`")
        else:
            seen_ids.add(contract_id)

        if not re.fullmatch(r"US-\d+", str(contract["user_story"])):
            errors.append(f"{label}: user_story must use US-n")
        sources = contract["required_evidence"]
        if not isinstance(sources, list) or not sources:
            errors.append(f"{label}: required_evidence must be a non-empty list")
        elif not all(source in ALLOWED_EVIDENCE_SOURCES for source in sources):
            errors.append(f"{label}: required_evidence contains an unsupported source")
        elif len(sources) != len(set(sources)):
            errors.append(f"{label}: required_evidence must not contain duplicates")

        method = contract["method"]
        path = contract["path"]
        status = contract["status"]
        if method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            errors.append(f"{label}: unsupported method `{method}`")
        if not isinstance(path, str) or not path.startswith("/"):
            errors.append(f"{label}: path must start with /")
        if not isinstance(status, int) or not 100 <= status <= 599:
            errors.append(f"{label}: status must be an integer from 100 to 599")
        if (
            isinstance(contract_id, str)
            and CONTRACT_ID_RE.fullmatch(contract_id)
            and method in {"GET", "POST", "PUT", "PATCH", "DELETE"}
            and isinstance(path, str)
            and path.startswith("/")
            and isinstance(status, int)
            and 100 <= status <= 599
        ):
            machine_cases.add((method, path, status, contract_id))

        errors.extend(validate_schema(contract["request"], f"{label}.request"))
        errors.extend(validate_schema(contract["response"], f"{label}.response"))

        human_entry = (
            human.get((method, path))
            if isinstance(method, str) and isinstance(path, str)
            else None
        )
        if human_entry is None:
            errors.append(f"{label}: `{method} {path}` has no matching Endpoint section")
        else:
            statuses = human_entry["statuses"]
            mentioned_ids = human_entry["metadata_ids"]
            response_cases = human_entry["response_cases"]
            response_examples = human_entry["response_examples"]
            test_cases = human_entry["test_cases"]
            if isinstance(status, int) and status not in statuses:
                errors.append(f"{label}: status {status} is missing from the Endpoint Responses")
            if isinstance(contract_id, str) and contract_id not in mentioned_ids:
                errors.append(f"{label}: contract_id is not listed in the Endpoint table")
            if isinstance(status, int) and isinstance(contract_id, str):
                if (status, contract_id) not in response_cases:
                    errors.append(
                        f"{label}: Endpoint response heading must map status {status} to {contract_id}"
                    )
                elif (status, contract_id) in response_examples:
                    errors.extend(
                        validate_example_against_schema(
                            response_examples[(status, contract_id)],
                            contract["response"],
                            f"{label}: human response example",
                        )
                    )
                if (status, contract_id) not in test_cases:
                    errors.append(
                        f"{label}: 測試規劃 must map status {status} to {contract_id}"
                    )

    for (method, path), human_entry in human.items():
        for status, contract_id in human_entry["response_cases"] | human_entry["test_cases"]:
            if (method, path, status, contract_id) not in machine_cases:
                errors.append(
                    f"Endpoint {method} {path}: human case {contract_id} / {status} has no machine contract"
                )
    return errors


def validate(path: Path) -> list[str]:
    if not path.exists():
        return [f"Input not found: {path}"]

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors: list[str] = []

    head = [line.strip() for line in lines[:10]]
    if not lines or not TITLE_RE.match(head[0] if head else ""):
        errors.append("missing top-level heading '# API 計畫：…'")
    if not any(BRANCH_RE.match(line) for line in head):
        errors.append("missing metadata line for 功能分支")
    if not any(CREATED_DATE_RE.match(line) for line in head):
        errors.append("missing metadata line for 建立日期")
    if not any(STATUS_RE.match(line) for line in head):
        errors.append("missing metadata line for 狀態")

    for header in REQUIRED_TOP_LEVEL:
        if not any(line.strip() == header for line in lines):
            errors.append(f"missing `{header}`")

    if PLACEHOLDER_RE.search(content):
        errors.append("output still contains unreplaced {{PLACEHOLDER}} tokens")

    errors.extend(validate_common_error_section(lines))
    errors.extend(validate_assumption_section(lines))

    entity_ranges = find_ranges(lines, ENTITY_HEADING_RE)
    if not entity_ranges:
        errors.append("missing at least one `## 資料實體：` section")
    else:
        for start, end in entity_ranges:
            label = lines[start].strip()
            errors.extend(validate_entity(lines[start:end], label))

    uses_v2 = any(FLOW_VERSION_RE.match(line.strip()) for line in lines[:12])
    has_machine_section = any(line.strip() == MACHINE_CONTRACT_HEADING for line in lines)
    if has_machine_section and not uses_v2:
        errors.append("可機械驗證契約 requires metadata `流程版本: 2`")
    if uses_v2 or has_machine_section:
        errors.extend(validate_machine_contracts(lines))

    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    errors = validate(path)

    if errors:
        print(f"INVALID: {path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"VALID: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
