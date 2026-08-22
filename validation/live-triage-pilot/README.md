# Live triage validation pilot

Status: quarantined design samples, not operational queries and not approved
for use during a live incident.

Lifecycle status is held in this README and the launcher manifest, not inside
the KQL blob. After analyst review, the final active-form blob is validated in
place here and may move into `investigation/` without a content change. Any KQL
edit after validation invalidates the receipt.

This pilot records small evidence-query designs for the
three highest-frequency needs currently identified:

- sign-in behaviour and identity posture;
- Entra audit chronology and posture;
- endpoint device coverage, activity, and source-native evidence.

Every query is written for Microsoft Sentinel Log Analytics. Endpoint files
use `TimeGenerated`, not Defender Advanced Hunting `Timestamp`.

## Operating model

1. Review the proposed question, inputs, output columns, and expected grid with
   the analyst before execution.
2. Use a completed incident or controlled case in the actual Sentinel Log
   Analytics workspace. Do not introduce a generated sample during a live
   incident.
3. Set the single declared entity and, only when needed, the lookback.
4. Ensure the portal time picker says `Set in query`.
5. Run the exact file without repairs.
6. Record execution time, rows, earliest event, latest event, warnings, and
   whether the grid was useful.
7. For raw evidence, reconcile the displayed row count and time span with a
   direct count over the same table, entity, and bound.
8. Promote only the exact source that passes the full gate in
   [`docs/live-investigation-standard.md`](../../docs/live-investigation-standard.md).

## Identity and audit

| Use | Question | Candidate |
| --- | --- | --- |
| Quick | What interactive sign-in records and properties does this identity show? | `identity/signin-behaviour-grid.kql` |
| Deep | How familiar is each interactive sign-in property for this identity? | `identity/signin-familiarity-grid.kql` |
| Posture | Which interactive sign-in combinations are habitual or new? | `identity/signin-posture-matrix.kql` |
| Quick | Which directory changes involved this identity? | `identity/audit-chronology.kql` |
| Posture | What audit-operation posture does this identity show? | `identity/audit-posture-matrix.kql` |

## Endpoint

| Use | Question | Candidate |
| --- | --- | --- |
| Quick | Which six core endpoint tables have data, and over what span? | `endpoint/device-coverage.kql` |
| Quick | When was each endpoint evidence family active? | `endpoint/device-activity-map.kql` |
| Deep | What executed? | `endpoint/device-processes.kql` |
| Deep | What connected? | `endpoint/device-network.kql` |
| Deep | What files changed? | `endpoint/device-files.kql` |
| Deep | Who authenticated and how? | `endpoint/device-logons.kql` |
| Deep | What registry state changed? | `endpoint/device-registry.kql` |
| Deep | What security-control or miscellaneous device actions occurred? | `endpoint/device-security-events.kql` |

The coverage and activity-map candidates orient the analyst across the full
24-hour window. The table-specific candidates default to a bounded two-hour
raw chronology and repeat the expected source count, earliest event, latest
event, and matched device identities on each returned row. Set the same
explicit interval in the orientation and raw queries when reconciling coverage.
None uses a hidden final-row cap.

## Explicit coverage limits

- The sign-in designs currently cover interactive user sign-ins in
  `SigninLogs`. They do not claim coverage of
  `AADNonInteractiveUserSignInLogs`, service principals, or managed identities.
- Endpoint orientation covers the six declared MDE event tables only.
- No design is complete merely because it parses or matches current published
  schemas. The actual workspace, result integrity, runtime, and grid still need
  analyst validation.
