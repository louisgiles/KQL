#!/usr/bin/env python3
"""Regression tests for the active investigation approval gate."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check-investigation-approvals.py"
QUERY_PATH = "investigation/identity/test-grid.kql"
QUERY = """let TargetUPN = "";
let Evidence = materialize(
    SigninLogs
    | where TimeGenerated >= ago(7d)
    | where isnotempty(TargetUPN)
    | where UserPrincipalName =~ TargetUPN);
let RowsInBound = toscalar(Evidence | count);
let FirstEventInBound = toscalar(Evidence | summarize min(TimeGenerated));
let LastEventInBound = toscalar(Evidence | summarize max(TimeGenerated));
Evidence
| extend RowsInBound, FirstEventInBound, LastEventInBound
| order by TimeGenerated desc, Id asc
"""


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class ApprovalGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "investigation" / "identity").mkdir(parents=True)
        (self.root / "validation" / "receipts" / "identity").mkdir(parents=True)
        (self.root / "investigation" / "README.md").write_text(QUERY_PATH, encoding="utf-8")
        (self.root / QUERY_PATH).write_text(QUERY, encoding="utf-8")
        self.query_hash = sha256_text(QUERY)
        self.entry = {
            "path": QUERY_PATH,
            "query_sha256": self.query_hash,
            "domain": "identity",
            "incident_title_aliases": ["test incident"],
            "role": "Quick",
            "required_entity": "user principal name",
            "entity_variable": "TargetUPN",
            "default_bound": "2h",
            "default_bound_seconds": 7200,
            "validation_status": "approved",
            "result_mode": "raw",
            "expected_tables": ["SigninLogs"],
            "optional_tables": [],
            "requires_missing_source": False,
            "workspace_profile": "production",
            "case_thresholds": {
                "sparse_max_rows": 20,
                "normal_min_rows": 21,
                "high_volume_min_rows": 1001,
            },
        }
        self.receipt = {
            "schema_version": 2,
            "query_path": QUERY_PATH,
            "query_sha256": self.query_hash,
            "execution_surface": "Microsoft Sentinel Log Analytics",
            "result_mode": "raw",
            "requires_missing_source": False,
            "expected_tables": ["SigninLogs"],
            "workspace_profile": "production",
            "default_bound_seconds": 7200,
            "result_grid_review": {
                "analyst": "louisgiles",
                "outcome": "approved",
                "reviewed_at": "2026-08-22T12:00:00Z",
            },
            "workspaces": [
                {
                    "workspace_reference": "workspace-a",
                    "runs": [
                        self.build_run("sparse", 5),
                        self.build_run("normal", 42),
                        self.build_run("high-volume", 1200),
                        self.build_run("no-data", 0),
                    ],
                }
            ],
        }
        self.write_json("investigation/launcher.json", {"schema_version": 2, "entries": [self.entry]})
        self.write_json("validation/workspaces.json", {"schema_version": 1, "profiles": {"production": ["workspace-a"]}})
        self.write_receipt()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def build_run(self, case: str, count: int) -> dict[str, object]:
        first = "2026-08-22T10:00:00Z" if count else None
        last = "2026-08-22T10:30:00Z" if count else None
        return {
            "case": case,
            "run_id": f"workspace-a-{case}",
            "status": "pass",
            "elapsed_seconds": 1.5,
            "entity_fingerprint": "a" * 64,
            "window_start": "2026-08-22T09:00:00Z",
            "window_end": "2026-08-22T11:00:00Z",
            "executed_at": "2026-08-22T12:00:00Z",
            "query_parameters_sha256": "b" * 64,
            "source_query_sha256": "c" * 64,
            "result_export_sha256": "d" * 64,
            "source_count": count,
            "returned_count": count,
            "source_first_event": first,
            "returned_first_event": first,
            "source_last_event": last,
            "returned_last_event": last,
            "warnings": [],
            "live_repairs": 0,
        }

    def write_json(self, relative: str, value: object) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def write_receipt(self) -> None:
        self.write_json("validation/receipts/identity/test-grid.json", self.receipt)

    def execute(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "-B", str(CHECKER), str(self.root)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_exact_source_passes(self) -> None:
        result = self.execute()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_raw_row_cap_is_rejected_even_when_hashes_match(self) -> None:
        capped = QUERY + "| top MaxRows by TimeGenerated\n"
        (self.root / QUERY_PATH).write_text(capped, encoding="utf-8")
        capped_hash = sha256_text(capped)
        self.entry["query_sha256"] = capped_hash
        self.receipt["query_sha256"] = capped_hash
        self.write_json("investigation/launcher.json", {"schema_version": 2, "entries": [self.entry]})
        self.write_receipt()
        result = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not cap returned evidence rows", result.stdout)

    def test_huge_elapsed_integer_fails_without_crashing(self) -> None:
        self.receipt["workspaces"][0]["runs"][0]["elapsed_seconds"] = 10 ** 400
        self.write_receipt()
        result = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("elapsed_seconds must be finite and below 120", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_case_label_cannot_hide_zero_normal_volume(self) -> None:
        self.receipt["workspaces"][0]["runs"][1] = self.build_run("normal", 0)
        self.write_receipt()
        result = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not satisfy 'normal' case thresholds", result.stdout)

    def test_receipt_cannot_invent_workspace_scope(self) -> None:
        self.receipt["workspaces"][0]["workspace_reference"] = "invented-workspace"
        self.write_receipt()
        result = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must exactly match the registered workspace profile", result.stdout)

    def test_duplicate_json_keys_fail_without_crashing(self) -> None:
        (self.root / "validation" / "workspaces.json").write_text(
            '{"schema_version":1,"schema_version":1,"profiles":{}}\n',
            encoding="utf-8",
        )
        result = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate JSON key", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
