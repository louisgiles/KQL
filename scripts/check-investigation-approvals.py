#!/usr/bin/env python3
"""Reject active investigation KQL without exact-source operational evidence."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_CASES = ("sparse", "normal", "high-volume", "no-data")
EXECUTION_SURFACE = "Microsoft Sentinel Log Analytics"
RESULT_MODES = {"raw", "aggregate", "coverage"}
LAUNCHER_ROLES = {"Quick", "Deep", "Posture"}
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def add_error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.as_posix()}: {message}")


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value}")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def read_text(path: Path, errors: list[str], root: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        add_error(errors, path.relative_to(root), f"cannot read UTF-8 text: {exc}")
        return None


def read_json(path: Path, errors: list[str], root: Path) -> Any:
    text = read_text(path, errors, root)
    if text is None:
        return None
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        add_error(errors, path.relative_to(root), f"invalid strict JSON: {exc}")
        return None


def nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.utcoffset() is not None else None
    except ValueError:
        return None


def validate_bound_pair(
    first: Any,
    last: Any,
    location: str,
    receipt_path: Path,
    errors: list[str],
) -> None:
    first_time = parse_timestamp(first)
    last_time = parse_timestamp(last)
    if first_time is None or last_time is None:
        add_error(errors, receipt_path, f"{location} requires ISO 8601 first and last event bounds")
    elif first_time > last_time:
        add_error(errors, receipt_path, f"{location} first event is after last event")


def validate_common_run(
    run: dict[str, Any],
    location: str,
    receipt_path: Path,
    errors: list[str],
) -> None:
    if run.get("status") != "pass":
        add_error(errors, receipt_path, f"{location}.status must be pass")
    if run.get("warnings") != []:
        add_error(errors, receipt_path, f"{location}.warnings must be empty")
    if run.get("live_repairs") != 0:
        add_error(errors, receipt_path, f"{location}.live_repairs must be 0")
    elapsed = run.get("elapsed_seconds")
    valid_elapsed = (
        isinstance(elapsed, int)
        and not isinstance(elapsed, bool)
        and 0 <= elapsed < 120
    ) or (
        isinstance(elapsed, float)
        and math.isfinite(elapsed)
        and 0 <= elapsed < 120
    )
    if not valid_elapsed:
        add_error(errors, receipt_path, f"{location}.elapsed_seconds must be finite and below 120")
    if not isinstance(run.get("run_id"), str) or not run["run_id"].strip():
        add_error(errors, receipt_path, f"{location}.run_id is required")
    for key in (
        "entity_fingerprint",
        "query_parameters_sha256",
        "source_query_sha256",
        "result_export_sha256",
    ):
        if not valid_sha256(run.get(key)):
            add_error(errors, receipt_path, f"{location}.{key} must be a lowercase SHA-256")
    window_start = parse_timestamp(run.get("window_start"))
    window_end = parse_timestamp(run.get("window_end"))
    if window_start is None or window_end is None or window_start >= window_end:
        add_error(errors, receipt_path, f"{location} requires an ordered ISO 8601 validation window")
    if parse_timestamp(run.get("executed_at")) is None:
        add_error(errors, receipt_path, f"{location}.executed_at must be an ISO 8601 timestamp")


def validate_reconciled_bounds(
    run: dict[str, Any],
    count: int,
    location: str,
    receipt_path: Path,
    errors: list[str],
) -> None:
    keys = (
        "source_first_event",
        "returned_first_event",
        "source_last_event",
        "returned_last_event",
    )
    if count == 0:
        for key in keys:
            if run.get(key) is not None:
                add_error(errors, receipt_path, f"{location}.{key} must be null when source_count is zero")
        return
    if run.get("source_first_event") != run.get("returned_first_event"):
        add_error(errors, receipt_path, f"{location} source and returned first events differ")
    if run.get("source_last_event") != run.get("returned_last_event"):
        add_error(errors, receipt_path, f"{location} source and returned last events differ")
    validate_bound_pair(
        run.get("source_first_event"),
        run.get("source_last_event"),
        location,
        receipt_path,
        errors,
    )


def validate_raw_run(run: dict[str, Any], location: str, receipt_path: Path, errors: list[str]) -> None:
    source_count = run.get("source_count")
    returned_count = run.get("returned_count")
    if not nonnegative_integer(source_count) or not nonnegative_integer(returned_count):
        add_error(errors, receipt_path, f"{location} counts must be nonnegative integers")
        return
    if source_count != returned_count:
        add_error(errors, receipt_path, f"{location} source_count and returned_count differ")
    validate_reconciled_bounds(run, source_count, location, receipt_path, errors)


def validate_aggregate_run(run: dict[str, Any], location: str, receipt_path: Path, errors: list[str]) -> None:
    source_count = run.get("source_count")
    accounted_count = run.get("accounted_source_count")
    returned_count = run.get("returned_count")
    if not all(nonnegative_integer(value) for value in (source_count, accounted_count, returned_count)):
        add_error(errors, receipt_path, f"{location} counts must be nonnegative integers")
        return
    if source_count != accounted_count:
        add_error(errors, receipt_path, f"{location} source_count and accounted_source_count differ")
    if (source_count == 0 and returned_count != 0) or (source_count > 0 and returned_count == 0):
        add_error(errors, receipt_path, f"{location}.returned_count is inconsistent with source_count")
    validate_reconciled_bounds(run, source_count, location, receipt_path, errors)


def validate_coverage_run(
    run: dict[str, Any],
    expected_tables: list[str],
    location: str,
    receipt_path: Path,
    errors: list[str],
) -> tuple[int | None, set[str]]:
    tables = run.get("tables")
    if not isinstance(tables, list):
        add_error(errors, receipt_path, f"{location}.tables must be a list")
        return None, set()
    names = [table.get("table") for table in tables if isinstance(table, dict)]
    if len(names) != len(tables) or not all(isinstance(name, str) and name for name in names):
        add_error(errors, receipt_path, f"{location}.tables requires a string table name in every row")
        return None, set()
    if len(names) != len(set(names)):
        add_error(errors, receipt_path, f"{location}.tables contains duplicate table names")
    if set(names) != set(expected_tables):
        add_error(errors, receipt_path, f"{location}.tables must exactly match launcher expected_tables")
    returned_count = run.get("returned_count")
    if not nonnegative_integer(returned_count) or returned_count != len(expected_tables):
        add_error(errors, receipt_path, f"{location}.returned_count must equal expected table count")

    total = 0
    unavailable: set[str] = set()
    for index, table in enumerate(tables):
        table_location = f"{location}.tables[{index}]"
        source_status = table.get("source_status")
        reported_status = table.get("reported_status")
        if source_status not in {"available", "unavailable"}:
            add_error(errors, receipt_path, f"{table_location}.source_status must be available or unavailable")
            continue
        if reported_status != source_status:
            add_error(errors, receipt_path, f"{table_location} source and reported status differ")
        if source_status == "unavailable":
            unavailable.add(table["table"])
            for key in (
                "source_count",
                "reported_count",
                "source_first_event",
                "reported_first_event",
                "source_last_event",
                "reported_last_event",
            ):
                if table.get(key) is not None:
                    add_error(errors, receipt_path, f"{table_location}.{key} must be null when unavailable")
            continue
        source_count = table.get("source_count")
        reported_count = table.get("reported_count")
        if not nonnegative_integer(source_count) or not nonnegative_integer(reported_count):
            add_error(errors, receipt_path, f"{table_location} counts must be nonnegative integers")
            continue
        total += source_count
        if source_count != reported_count:
            add_error(errors, receipt_path, f"{table_location} source and reported counts differ")
        first_keys = ("source_first_event", "reported_first_event")
        last_keys = ("source_last_event", "reported_last_event")
        if source_count == 0:
            for key in first_keys + last_keys:
                if table.get(key) is not None:
                    add_error(errors, receipt_path, f"{table_location}.{key} must be null for zero rows")
        else:
            if table.get(first_keys[0]) != table.get(first_keys[1]):
                add_error(errors, receipt_path, f"{table_location} first-event bounds differ")
            if table.get(last_keys[0]) != table.get(last_keys[1]):
                add_error(errors, receipt_path, f"{table_location} last-event bounds differ")
            validate_bound_pair(
                table.get(first_keys[0]),
                table.get(last_keys[0]),
                table_location,
                receipt_path,
                errors,
            )
    return total, unavailable


def validate_case_volume(
    case: str,
    row_count: int | None,
    thresholds: dict[str, int],
    location: str,
    receipt_path: Path,
    errors: list[str],
) -> None:
    if row_count is None:
        return
    sparse_max = thresholds.get("sparse_max_rows")
    normal_min = thresholds.get("normal_min_rows")
    high_min = thresholds.get("high_volume_min_rows")
    if not all(nonnegative_integer(value) for value in (sparse_max, normal_min, high_min)):
        add_error(errors, receipt_path, f"{location} cannot apply invalid case thresholds")
        return
    valid = (
        (case == "sparse" and 1 <= row_count <= sparse_max)
        or (case == "normal" and normal_min <= row_count < high_min)
        or (case == "high-volume" and row_count >= high_min)
        or (case == "no-data" and row_count == 0)
        or case == "missing-source"
    )
    if not valid:
        add_error(errors, receipt_path, f"{location} row count does not satisfy {case!r} case thresholds")


def validate_registry(root: Path, errors: list[str]) -> dict[str, list[str]]:
    path = root / "validation" / "workspaces.json"
    record = read_json(path, errors, root)
    if not isinstance(record, dict) or record.get("schema_version") != 1:
        add_error(errors, path.relative_to(root), "schema_version must be 1")
        return {}
    profiles = record.get("profiles")
    if not isinstance(profiles, dict):
        add_error(errors, path.relative_to(root), "profiles must be an object")
        return {}
    validated: dict[str, list[str]] = {}
    for name, workspaces in profiles.items():
        if not isinstance(name, str) or not name.strip():
            add_error(errors, path.relative_to(root), "profile names must be nonempty strings")
            continue
        if (
            not isinstance(workspaces, list)
            or not workspaces
            or not all(isinstance(item, str) and item.strip() for item in workspaces)
            or len(workspaces) != len(set(workspaces))
        ):
            add_error(errors, path.relative_to(root), f"profile {name!r} must contain unique workspace aliases")
            continue
        validated[name] = workspaces
    return validated


def validate_launcher(
    root: Path,
    query_paths: set[str],
    workspace_profiles: dict[str, list[str]],
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    path = root / "investigation" / "launcher.json"
    record = read_json(path, errors, root)
    if not isinstance(record, dict) or record.get("schema_version") != 2:
        add_error(errors, path.relative_to(root), "schema_version must be 2")
        return {}
    entries = record.get("entries")
    if not isinstance(entries, list):
        add_error(errors, path.relative_to(root), "entries must be a list")
        return {}
    by_path: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        location = f"entries[{index}]"
        if not isinstance(entry, dict):
            add_error(errors, path.relative_to(root), f"{location} must be an object")
            continue
        query_path = entry.get("path")
        if not isinstance(query_path, str) or not query_path.startswith("investigation/") or not query_path.endswith(".kql"):
            add_error(errors, path.relative_to(root), f"{location}.path must name active investigation KQL")
            continue
        if query_path in by_path:
            add_error(errors, path.relative_to(root), f"duplicate launcher path {query_path}")
        by_path[query_path] = entry
        for key in ("domain", "required_entity", "entity_variable", "default_bound"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                add_error(errors, path.relative_to(root), f"{location}.{key} is required")
        aliases = entry.get("incident_title_aliases")
        if not isinstance(aliases, list) or not aliases or not all(isinstance(alias, str) and alias.strip() for alias in aliases):
            add_error(errors, path.relative_to(root), f"{location}.incident_title_aliases must be a nonempty string list")
        if entry.get("role") not in LAUNCHER_ROLES:
            add_error(errors, path.relative_to(root), f"{location}.role must be Quick, Deep, or Posture")
        if entry.get("validation_status") != "approved":
            add_error(errors, path.relative_to(root), f"{location}.validation_status must be approved")
        if not valid_sha256(entry.get("query_sha256")):
            add_error(errors, path.relative_to(root), f"{location}.query_sha256 must be lowercase SHA-256")
        mode = entry.get("result_mode")
        if mode not in RESULT_MODES:
            add_error(errors, path.relative_to(root), f"{location}.result_mode is invalid")
        expected = entry.get("expected_tables")
        optional = entry.get("optional_tables")
        if not isinstance(expected, list) or not expected or not all(isinstance(item, str) and item for item in expected) or len(expected) != len(set(expected)):
            add_error(errors, path.relative_to(root), f"{location}.expected_tables must contain unique table names")
            expected = []
        if not isinstance(optional, list) or not all(isinstance(item, str) and item for item in optional) or len(optional) != len(set(optional)):
            add_error(errors, path.relative_to(root), f"{location}.optional_tables must contain unique table names")
            optional = []
        if not set(optional).issubset(set(expected)):
            add_error(errors, path.relative_to(root), f"{location}.optional_tables must be a subset of expected_tables")
        entry["_validated_expected_tables"] = expected
        requires_missing = entry.get("requires_missing_source")
        expected_missing = len(expected) > 1 or bool(optional)
        if not isinstance(requires_missing, bool) or requires_missing != expected_missing:
            add_error(errors, path.relative_to(root), f"{location}.requires_missing_source must be true for multi-table or optional-table queries")
        if expected_missing and mode != "coverage":
            add_error(errors, path.relative_to(root), f"{location} multi-table and optional-table queries currently require coverage result mode")
        bound_seconds = entry.get("default_bound_seconds")
        if not isinstance(bound_seconds, int) or isinstance(bound_seconds, bool) or bound_seconds <= 0:
            add_error(errors, path.relative_to(root), f"{location}.default_bound_seconds must be a positive integer")
        profile = entry.get("workspace_profile")
        if not isinstance(profile, str) or profile not in workspace_profiles:
            add_error(errors, path.relative_to(root), f"{location}.workspace_profile must name a registered profile")
        thresholds = entry.get("case_thresholds")
        if not isinstance(thresholds, dict):
            add_error(errors, path.relative_to(root), f"{location}.case_thresholds is required")
            entry["_validated_thresholds"] = None
        else:
            sparse = thresholds.get("sparse_max_rows")
            normal = thresholds.get("normal_min_rows")
            high = thresholds.get("high_volume_min_rows")
            if not all(nonnegative_integer(value) for value in (sparse, normal, high)) or not (1 <= sparse < normal < high):
                add_error(errors, path.relative_to(root), f"{location}.case_thresholds must satisfy 1 <= sparse < normal < high")
                entry["_validated_thresholds"] = None
            else:
                entry["_validated_thresholds"] = thresholds
                if entry.get("domain", "").lower() == "endpoint" and (normal < 21 or high < 1001):
                    add_error(errors, path.relative_to(root), f"{location} endpoint thresholds require normal >= 21 and high-volume >= 1001")

    for query_path in sorted(query_paths - set(by_path)):
        add_error(errors, path.relative_to(root), f"active query missing from launcher: {query_path}")
    for query_path in sorted(set(by_path) - query_paths):
        add_error(errors, path.relative_to(root), f"launcher points to missing active query: {query_path}")
    return by_path


def validate_static_query(
    query_path: Path,
    query_text: str,
    entry: dict[str, Any],
    root: Path,
    errors: list[str],
) -> None:
    relative = query_path.relative_to(root)
    lines = query_text.splitlines()
    executable = "\n".join(line for line in lines if not line.lstrip().startswith("//"))
    lower = executable.lower()
    if re.search(r"\bsearch\b", lower):
        add_error(errors, relative, "active investigation KQL must not use search")
    if len(lines) > 150:
        add_error(errors, relative, "active investigation KQL exceeds the 150-line hard limit")
    if "TimeGenerated" not in executable:
        add_error(errors, relative, "active investigation KQL must use Sentinel TimeGenerated")
    if entry.get("domain", "").lower() == "endpoint" and re.search(r"\bTimestamp\b", executable):
        add_error(errors, relative, "Sentinel endpoint KQL must not use Defender Advanced Hunting Timestamp")
    if entry.get("result_mode") == "raw":
        if re.search(r"\b(take|top|limit|sample)\b", lower):
            add_error(errors, relative, "raw investigation KQL must not cap returned evidence rows")
        if not re.search(r"\b(order|sort)\s+by\b[^\n]*,[^\n]*", lower):
            add_error(errors, relative, "raw investigation KQL requires deterministic multi-key ordering")
        for token in ("RowsInBound", "FirstEventInBound", "LastEventInBound"):
            if token not in executable:
                add_error(errors, relative, f"raw investigation KQL must expose {token}")
    expected_tables = entry.get("expected_tables")
    entity_variable = entry.get("entity_variable")
    if isinstance(expected_tables, list):
        for table in expected_tables:
            if not isinstance(table, str):
                continue
            match = re.search(rf"\b{re.escape(table)}\b", executable)
            if match is None:
                add_error(errors, relative, f"expected table {table} is not referenced")
                continue
            nearby = executable[match.end():match.end() + 800]
            if not re.search(r"\|\s*where\s+TimeGenerated\b", nearby):
                add_error(errors, relative, f"{table} does not receive an early TimeGenerated filter")
            if isinstance(entity_variable, str) and entity_variable not in nearby:
                add_error(errors, relative, f"{table} does not receive an early {entity_variable} entity filter")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    investigation_root = root / "investigation"
    receipt_root = root / "validation" / "receipts"
    query_files = sorted(investigation_root.rglob("*.kql"))
    query_paths = {path.relative_to(root).as_posix() for path in query_files}
    workspace_profiles = validate_registry(root, errors)
    launcher = validate_launcher(root, query_paths, workspace_profiles, errors)
    launcher_readme = read_text(investigation_root / "README.md", errors, root) or ""

    for query in query_files:
        relative_query = query.relative_to(root)
        query_path = relative_query.as_posix()
        try:
            query_bytes = query.read_bytes()
            query_text = query_bytes.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            add_error(errors, relative_query, f"cannot read UTF-8 query bytes: {exc}")
            continue
        query_hash = hashlib.sha256(query_bytes).hexdigest()
        entry = launcher.get(query_path)
        if entry is None:
            continue
        if entry.get("query_sha256") != query_hash:
            add_error(errors, Path("investigation/launcher.json"), f"{query_path} hash does not match")
        if query_path not in launcher_readme:
            add_error(errors, Path("investigation/README.md"), f"human launcher is missing {query_path}")
        validate_static_query(query, query_text, entry, root, errors)

        receipt = receipt_root / query.relative_to(investigation_root).with_suffix(".json")
        receipt_relative = receipt.relative_to(root)
        if not receipt.is_file():
            add_error(errors, relative_query, f"missing approval receipt {receipt_relative}")
            continue
        record = read_json(receipt, errors, root)
        if not isinstance(record, dict):
            continue
        if record.get("schema_version") != 2:
            add_error(errors, receipt_relative, "schema_version must be 2")
        if record.get("query_path") != query_path or record.get("query_sha256") != query_hash:
            add_error(errors, receipt_relative, "query path or hash does not match active source")
        if record.get("execution_surface") != EXECUTION_SURFACE:
            add_error(errors, receipt_relative, f"execution_surface must be {EXECUTION_SURFACE!r}")
        for key in ("result_mode", "requires_missing_source", "expected_tables", "workspace_profile", "default_bound_seconds"):
            if record.get(key) != entry.get(key):
                add_error(errors, receipt_relative, f"{key} must equal launcher metadata")
        grid_review = record.get("result_grid_review")
        if not isinstance(grid_review, dict) or grid_review.get("analyst") != "louisgiles" or grid_review.get("outcome") != "approved" or parse_timestamp(grid_review.get("reviewed_at")) is None:
            add_error(errors, receipt_relative, "result_grid_review requires louisgiles, approved, and an ISO timestamp")

        profile_name = entry.get("workspace_profile")
        required_workspaces = workspace_profiles.get(profile_name, [])
        workspaces = record.get("workspaces")
        if not isinstance(workspaces, list):
            add_error(errors, receipt_relative, "workspaces must be a list")
            continue
        references = [workspace.get("workspace_reference") for workspace in workspaces if isinstance(workspace, dict)]
        if len(references) != len(workspaces) or not all(isinstance(item, str) for item in references):
            add_error(errors, receipt_relative, "every workspace requires a string workspace_reference")
            continue
        if len(references) != len(set(references)):
            add_error(errors, receipt_relative, "workspace_reference values must be unique")
        if set(references) != set(required_workspaces):
            add_error(errors, receipt_relative, "workspaces must exactly match the registered workspace profile")

        required_cases = set(BASE_CASES)
        if entry.get("requires_missing_source"):
            required_cases.add("missing-source")
        all_run_ids: set[str] = set()
        for workspace_index, workspace in enumerate(workspaces):
            location = f"workspaces[{workspace_index}]"
            runs = workspace.get("runs")
            if not isinstance(runs, list):
                add_error(errors, receipt_relative, f"{location}.runs must be a list")
                continue
            cases = [run.get("case") for run in runs if isinstance(run, dict)]
            if len(cases) != len(runs) or not all(isinstance(case, str) for case in cases):
                add_error(errors, receipt_relative, f"{location}.runs requires string case labels")
                continue
            if len(cases) != len(set(cases)) or set(cases) != required_cases:
                add_error(errors, receipt_relative, f"{location}.runs must contain each required case exactly once")
            for run_index, run in enumerate(runs):
                run_location = f"{location}.runs[{run_index}]"
                if not isinstance(run, dict):
                    add_error(errors, receipt_relative, f"{run_location} must be an object")
                    continue
                validate_common_run(run, run_location, receipt_relative, errors)
                run_id = run.get("run_id")
                if isinstance(run_id, str):
                    if run_id in all_run_ids:
                        add_error(errors, receipt_relative, f"duplicate run_id {run_id!r}")
                    all_run_ids.add(run_id)
                mode = entry.get("result_mode")
                row_count: int | None = None
                unavailable_tables: set[str] = set()
                if mode == "raw":
                    validate_raw_run(run, run_location, receipt_relative, errors)
                    if nonnegative_integer(run.get("source_count")):
                        row_count = run["source_count"]
                elif mode == "aggregate":
                    validate_aggregate_run(run, run_location, receipt_relative, errors)
                    if nonnegative_integer(run.get("source_count")):
                        row_count = run["source_count"]
                elif mode == "coverage":
                    row_count, unavailable_tables = validate_coverage_run(
                        run,
                        entry.get("_validated_expected_tables", []),
                        run_location,
                        receipt_relative,
                        errors,
                    )
                case = run.get("case")
                thresholds = entry.get("_validated_thresholds")
                if isinstance(case, str) and isinstance(thresholds, dict):
                    validate_case_volume(case, row_count, thresholds, run_location, receipt_relative, errors)
                if case == "normal":
                    start = parse_timestamp(run.get("window_start"))
                    end = parse_timestamp(run.get("window_end"))
                    expected_seconds = entry.get("default_bound_seconds")
                    if start is not None and end is not None and isinstance(expected_seconds, int) and (end - start).total_seconds() != expected_seconds:
                        add_error(errors, receipt_relative, f"{run_location} must use the launcher default bound")
                if case == "missing-source":
                    optional_tables = set(entry.get("optional_tables", []))
                    required_tables = set(entry.get("_validated_expected_tables", [])) - optional_tables
                    if optional_tables:
                        if not (unavailable_tables & optional_tables):
                            add_error(errors, receipt_relative, f"{run_location} must prove an unavailable optional source")
                        if unavailable_tables & required_tables:
                            add_error(errors, receipt_relative, f"{run_location} cannot lose a required source")
                    elif not unavailable_tables:
                        add_error(errors, receipt_relative, f"{run_location} must prove at least one unavailable source")

    if errors:
        print("Active investigation approval check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Active investigation approval check passed: {len(query_files)} active query file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
