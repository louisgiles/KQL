#!/usr/bin/env python3
"""Block active KQL promotion without exact-content live validation."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


ACTIVE_ROOTS = ("investigation/", "threat-work/")
ALLOWED_STATUSES = {"pending", "failed", "passed"}
ALLOWED_SURFACES = {
    "sentinel-log-analytics",
    "defender-advanced-hunting",
    "azure-data-explorer",
}
SHA1_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_PASS_CHECKS = (
    "full_query_executed",
    "no_runtime_errors",
    "expected_output_shape",
)
REQUIRED_SCENARIOS = {"exact-source", "representative-incident"}


def is_active_kql(path: str) -> bool:
    return path.endswith(".kql") and path.startswith(ACTIVE_ROOTS)


def normalize_repo_path(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe repository path {value!r}")
    return path.as_posix()


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    framed = b"blob " + str(len(content)).encode("ascii") + b"\0" + content
    return hashlib.sha1(framed).hexdigest()


def source_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_utc(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() is not None and parsed.utcoffset().total_seconds() == 0


def load_manifest(path: Path) -> tuple[dict[str, dict], list[str]]:
    errors: list[str] = []
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {}, [f"KQLLIVE001 cannot read {path}: {error}"]

    if document.get("schema_version") != 1:
        errors.append("KQLLIVE001 manifest schema_version must be 1")

    records = document.get("records")
    if not isinstance(records, list):
        return {}, errors + ["KQLLIVE001 manifest records must be an array"]

    by_path: dict[str, dict] = {}
    for index, record in enumerate(records):
        prefix = f"KQLLIVE001 record {index + 1}"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        try:
            record_path = normalize_repo_path(record.get("path", ""))
        except ValueError as error:
            errors.append(f"{prefix}: {error}")
            continue
        if not is_active_kql(record_path):
            errors.append(f"{prefix} path is not active KQL: {record_path!r}")
            continue
        if record_path in by_path:
            errors.append(f"{prefix} duplicates {record_path}")
            continue

        sha = record.get("git_blob_sha")
        if not isinstance(sha, str) or SHA1_PATTERN.fullmatch(sha) is None:
            errors.append(f"{prefix} has an invalid git_blob_sha")

        source_hash = record.get("source_sha256")
        if not isinstance(source_hash, str) or SHA256_PATTERN.fullmatch(source_hash) is None:
            errors.append(f"{prefix} has an invalid source_sha256")

        surface = record.get("execution_surface")
        if surface not in ALLOWED_SURFACES:
            errors.append(f"{prefix} has an invalid execution_surface")
        if record_path.startswith("investigation/") and surface != "sentinel-log-analytics":
            errors.append(f"{prefix} investigation KQL must target sentinel-log-analytics")

        status = record.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{prefix} has an invalid status")

        reason = record.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{prefix} must include a reason")

        if status == "passed":
            if record.get("executed_query_sha256") != source_hash:
                errors.append(
                    f"{prefix} passed record requires executed_query_sha256 "
                    "equal to source_sha256"
                )
            if not parse_utc(record.get("validated_at_utc")):
                errors.append(f"{prefix} passed record requires a UTC validated_at_utc")
            if not isinstance(record.get("validated_by"), str) or not record["validated_by"].strip():
                errors.append(f"{prefix} passed record requires validated_by")
            scenarios = record.get("scenarios")
            if not isinstance(scenarios, list) or not scenarios or not all(
                isinstance(item, str) and item.strip() for item in scenarios
            ):
                errors.append(f"{prefix} passed record requires non-empty scenarios")
            elif not REQUIRED_SCENARIOS.issubset(set(scenarios)):
                errors.append(
                    f"{prefix} passed record requires scenarios: "
                    + ", ".join(sorted(REQUIRED_SCENARIOS))
                )
            evidence = record.get("evidence")
            if not isinstance(evidence, str) or not evidence.strip():
                errors.append(f"{prefix} passed record requires sanitized evidence")
            checks = record.get("checks")
            if not isinstance(checks, dict) or any(checks.get(name) is not True for name in REQUIRED_PASS_CHECKS):
                errors.append(
                    f"{prefix} passed record requires true checks for "
                    + ", ".join(REQUIRED_PASS_CHECKS)
                )

        by_path[record_path] = record

    return by_path, errors


def active_files(repo_root: Path) -> set[str]:
    return {
        path.relative_to(repo_root).as_posix()
        for root_name in ("investigation", "threat-work")
        for path in (repo_root / root_name).rglob("*.kql")
        if (repo_root / root_name).is_dir()
    }


def changed_files(repo_root: Path, base: str) -> set[str]:
    command = [
        "git",
        "-C",
        str(repo_root),
        "diff",
        "--name-only",
        "--diff-filter=ACMR",
        f"{base}...HEAD",
        "--",
        "investigation",
        "threat-work",
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return {
        normalize_repo_path(line.strip())
        for line in result.stdout.splitlines()
        if line.strip() and is_active_kql(normalize_repo_path(line.strip()))
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--manifest",
        default="validation/sentinel-live.json",
        help="Manifest path relative to repo root",
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true", help="Require every active KQL file to have passed")
    selection.add_argument("--base", help="Require active KQL changed since this git base")
    selection.add_argument("--files", nargs="+", help="Require these repository paths")
    selection.add_argument(
        "--manifest-only",
        action="store_true",
        help="Validate manifest structure and content hashes without requiring passed status",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = repo_root / args.manifest
    records, errors = load_manifest(manifest_path)
    current_files = active_files(repo_root)

    missing_records = sorted(current_files - set(records))
    stale_records = sorted(set(records) - current_files)
    errors.extend(f"KQLLIVE001 manifest is missing {path}" for path in missing_records)
    errors.extend(f"KQLLIVE001 manifest references missing file {path}" for path in stale_records)

    for path in sorted(current_files & set(records)):
        actual_sha = git_blob_sha(repo_root / path)
        if records[path].get("git_blob_sha") != actual_sha:
            errors.append(
                f"KQLLIVE001 {path} content SHA is {actual_sha}, "
                f"manifest has {records[path].get('git_blob_sha')}"
            )
        actual_source_hash = source_sha256(repo_root / path)
        if records[path].get("source_sha256") != actual_source_hash:
            errors.append(
                f"KQLLIVE001 {path} source SHA256 is {actual_source_hash}, "
                f"manifest has {records[path].get('source_sha256')}"
            )

    try:
        if args.manifest_only:
            required = set()
        elif args.all:
            required = current_files
        elif args.base:
            required = changed_files(repo_root, args.base)
        else:
            required = {normalize_repo_path(path) for path in args.files}
    except (RuntimeError, ValueError) as error:
        errors.append(f"KQLLIVE001 cannot resolve validation scope: {error}")
        required = set()

    for path in sorted(required):
        if not is_active_kql(path):
            errors.append(f"KQLLIVE001 requested path is not active KQL: {path}")
            continue
        if path not in current_files:
            errors.append(f"KQLLIVE001 requested active KQL does not exist: {path}")
            continue
        record = records.get(path)
        if record is None:
            continue
        if record.get("status") != "passed":
            errors.append(
                f"KQLLIVE002 {path} is {record.get('status')}: "
                f"{record.get('reason', 'no reason recorded')}"
            )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"Sentinel live-validation gate failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Sentinel live-validation gate passed for {len(required)} active KQL file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
