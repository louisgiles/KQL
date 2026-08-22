# Sentinel live-validation records

`sentinel-live.json` is the operational source of truth for active KQL.
Directory placement and parser success do not imply readiness.

## States

| State | Meaning |
|---|---|
| `pending` | Exact content has no successful live execution record. |
| `failed` | Exact content has a known semantic, runtime, or output defect. |
| `passed` | Exact content executed successfully in the declared surface and returned the expected output shape. |

Only `passed` may be described as validated or used as an incident-ready
artifact.

## Content binding

Each record contains both:

- `git_blob_sha`: the Git object identity for the exact file bytes.
- `source_sha256`: the SHA256 of the raw UTF-8 file.

Any byte change invalidates the record. Do not place a source hash inside the
query because that creates a self-reference.

## Passing record

A `passed` record must add:

```json
{
  "status": "passed",
  "executed_query_sha256": "<must equal source_sha256>",
  "validated_at_utc": "2026-08-22T10:00:00Z",
  "validated_by": "analyst handle",
  "scenarios": [
    "exact-source",
    "representative-incident"
  ],
  "evidence": "Sanitized Sentinel execution reference",
  "checks": {
    "full_query_executed": true,
    "no_runtime_errors": true,
    "expected_output_shape": true
  }
}
```

Never commit client UPNs, IP addresses, tenant IDs, incident details, or query
results as evidence.

`exact-source` runs the unchanged repository file and binds execution to
`source_sha256`. `representative-incident` runs the same logic with only the
declared analyst inputs populated and confirms a realistic nonempty result.

## Verification

```bash
python3 scripts/check-sentinel-live-validation.py . --files path/to/query.kql
```

Use `--all` for a full operational readiness audit. CI checks changed active
KQL against the exact-content records and fails closed.

The stronger future control is a read-only Azure OIDC job that verifies the
`LAQueryLogs.QueryText` SHA256 and requires `ResponseCode == 200`.
