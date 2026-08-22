# Active investigation approval receipts

Every active investigation KQL file requires a JSON receipt at the matching
path beneath this directory. For example:

~~~text
investigation/identity/signin/behaviour-grid.kql
validation/receipts/identity/signin/behaviour-grid.json
~~~

The receipt binds actual-workspace execution evidence and result-grid review to
the exact SHA-256 of the active query. Each intended workspace has its own
complete run set. Use a non-secret alias in workspace_reference; never store
tenant credentials or tokens. The required aliases come from the code-owned
validation/workspaces.json registry. A receipt cannot declare its own scope.

## Raw result example

~~~json
{
  "schema_version": 2,
  "query_path": "investigation/identity/signin/behaviour-grid.kql",
  "query_sha256": "64 lowercase hexadecimal characters",
  "execution_surface": "Microsoft Sentinel Log Analytics",
  "result_mode": "raw",
  "requires_missing_source": false,
  "expected_tables": ["SigninLogs"],
  "workspace_profile": "production",
  "default_bound_seconds": 604800,
  "result_grid_review": {
    "analyst": "louisgiles",
    "outcome": "approved",
    "reviewed_at": "ISO 8601 timestamp"
  },
  "workspaces": [
    {
      "workspace_reference": "non-secret actual workspace alias",
      "runs": [
        {
          "case": "normal",
          "run_id": "unique validation-run identifier",
          "status": "pass",
          "elapsed_seconds": 1.2,
          "entity_fingerprint": "SHA-256 of a non-reversible validation entity reference",
          "window_start": "ISO 8601 timestamp",
          "window_end": "ISO 8601 timestamp",
          "executed_at": "ISO 8601 timestamp",
          "query_parameters_sha256": "SHA-256 of canonical declared parameters",
          "source_query_sha256": "SHA-256 of the independent reconciliation query",
          "result_export_sha256": "SHA-256 of the exported result evidence",
          "source_count": 42,
          "returned_count": 42,
          "source_first_event": "ISO 8601 timestamp",
          "returned_first_event": "same ISO 8601 timestamp",
          "source_last_event": "ISO 8601 timestamp",
          "returned_last_event": "same ISO 8601 timestamp",
          "warnings": [],
          "live_repairs": 0
        }
      ]
    }
  ]
}
~~~

## Result modes

| Mode | Reconciliation |
| --- | --- |
| raw | Source and returned row counts, first event, and last event must match. |
| aggregate | accounted_source_count must equal source_count; the minimum first-seen and maximum last-seen returned by the groups must match the source bounds. |
| coverage | tables records each expected table's source status, count, first event, and last event beside the values reported by the query. |

Each workspace must include sparse, normal, high-volume, and no-data runs.
Multi-table and optional-table queries set requires_missing_source to true and
also require a missing-source run. Until per-table reconciliation exists for
other result modes, these queries can be promoted only as coverage queries.
All runs must have no warnings and zero live
repairs, and each run must complete in under 120 seconds. The code-owned
launcher defines result mode, expected and optional tables, workspace profile,
canonical default-bound seconds, and case thresholds. The normal run must use
that exact default bound. Receipt metadata must match the launcher exactly. Any KQL edit
changes the hash and invalidates the receipt.

Every run records a unique ID, entity fingerprint, exact window, execution
time, canonical parameter hash, independent reconciliation-query hash, and
exported-result hash. The checker validates structure and reconciliation. It
cannot prove that a manually authored receipt came from Sentinel, so repository
rules must require final-head code-owner approval by louisgiles for the active
query, receipt, launcher, registry, checker, workflow, and standard.

The machine-readable launcher at investigation/launcher.json must list the same
active path and hash, its domain, common incident-title aliases, Quick, Deep, or
Posture role, required entity and variable, validated default bound, result
mode, source tables, workspace profile, case thresholds, and approved status.
The human launcher in investigation/README.md must link the same path.
