# Live investigation standard

This standard applies to reusable Microsoft Sentinel Log Analytics queries
used while an analyst is actively triaging an incident.

## Definition

A live-investigation query is a repeatable analyst instrument. It begins with
an entity already visible in the incident, answers one operational question,
and returns a complete and readable view of the bounded evidence needed for
that question.

Grammar-valid KQL is not enough. A query is operational only after the exact
saved source has passed repeated zero-repair execution in every actual Sentinel
Log Analytics workspace where it will be used and the analyst has approved its
result grid.

## Release gates

| Gate | Requirement |
| --- | --- |
| Execution surface | Microsoft Sentinel Log Analytics. Use the Azure Monitor table contract, including `TimeGenerated` for ingested Defender endpoint tables. |
| Input | One required incident entity. A bounded lookback may be adjustable. Do not require entity extraction or an alert timestamp when the incident already provides context. |
| Question | One query answers one named investigative question. Do not build a universal playbook inside a single file. |
| Time | Filter `TimeGenerated` immediately. Use `now()` and `ago()` for current triage. Every table leg receives its own time and entity filter. |
| Completeness | Raw evidence queries must not use arbitrary row caps. Repetitive data may be aggregated only when the output includes count, first seen, and last seen. |
| Chronology | Raw evidence is deterministically ordered by activity time and a stable identifier where available. Do not sort only after discarding rows. |
| Output | Project source-native evidence columns. Do not hide primary evidence in a dynamic bag or repeat generic decision and next-action prose on every row. |
| Missing data | Missing tables, missing fields, and no-data results remain unknown. They are never converted into benign evidence. |
| Size | Quick query target: 40 lines or fewer. Deep query target: 100 lines or fewer. More than 150 lines is rejected. |
| Runtime | Measure execution in the target blade. Two-minute execution is rejected for the normal live path. |
| Analyst utility | The analyst confirms that the result can be cognitively ingested during an incident. Parser, lint, and author confidence cannot substitute for this. |
| Result integrity | Reject partial-query warnings and reconcile source count, returned count, earliest event, and latest event over the same entity and bound. If the portal cannot return the full bounded result, narrow or deterministically partition the question and label the limitation. |

## Query classes

| Class | Proposed default bound | Output purpose |
| --- | ---: | --- |
| Interactive sign-in behaviour | 7 days | Dense authentication-flow grid for visual comparison. |
| Interactive sign-in familiarity | 30 days | Per-user IP, location, app, device, and user-agent prevalence beside each returned record. |
| Interactive identity posture | 14 days | Complete combinations with frequency, first seen, and last seen. |
| Audit chronology | 48 hours | Directory changes involving the supplied identity. |
| Audit posture | 14 days | Operation, relationship, service, and outcome patterns. |
| Endpoint coverage | 24 hours | Rows, earliest event, latest event, and freshness per expected table. |
| Endpoint activity map | 24 hours | Full-window event density by telemetry family and time bin. |
| Endpoint evidence | 2 hours | Table-specific chronology with source-count and time-span integrity metadata. |

These bounds are proposals until repeated use in the actual workspace proves
them useful. A different bound must represent a clear investigative question.
A window must never be shortened merely to make the result look small.

## Structure

Active queries are organized by analyst objective and evidence type, not by
incident title. Hundreds of alert titles should reuse a small number of stable
questions:

- What sign-in behaviour does this identity show?
- What identity posture is habitual or new?
- What directory changes involved this identity?
- Which endpoint tables contain evidence for this device?
- When was the device active?
- What executed, connected, changed files, authenticated, or changed registry
  state?

Cross-domain correlation is follow-on work. It must prove a relationship using
stable identifiers. A union of events that merely share any supplied entity is
not correlation.

The future `investigation/README.md` is a direct launcher, not a narrative
index. Each active row must expose domain, common incident-title aliases, Quick
query, Deep query, required entity, validated default bound, and validation
status. Archived Quick and Deep labels describe history only and never imply
operational approval.

## Exact-source validation

Generated KQL remains quarantined until the analyst has reviewed the proposed
question, inputs, columns, and expected grid. Initial execution uses completed
incidents or controlled cases, not an active incident. Every candidate must be
tested without editing the submitted source except for the declared entity
value and time bound.

Minimum identity and audit cases:

- populated user with repeated activity;
- populated user with sparse or null device, location, risk, or authentication
  fields;
- no-data user;
- a high-volume completed or controlled case in the actual workspace;
- row count and time span reconciled with a direct table count.

Minimum endpoint cases:

- device with more than 20 events;
- high-volume device with more than 1,000 events;
- no-data device;
- a controlled missing-table case when the actual workspace does not provide one;
- earliest and latest evidence reconcile with the requested bound;
- process correlation uses unique process identifiers when present and never a
  process ID alone.
- the returned row count and time span reconcile with a count over the same
  table, entity, and bound so service or client truncation cannot pass silently.

For endpoint validation, the normal case contains at least 21 source events
and the high-volume case contains at least 1,001. The launcher may set stricter
thresholds but cannot weaken these floors.

The validation record must bind the test to the exact Git blob or SHA-256,
record the actual workspace reference, entity fingerprint, exact parameters,
independent reconciliation query, exported-result hash, execution time, source
and returned row counts, earliest result, latest result, warnings, live repairs,
and analyst outcome. Sparse, normal, high-volume, and no-data cases must all
execute with zero repairs. Any KQL change invalidates the record.

Every active `investigation/**/*.kql` file requires a matching machine-checked
receipt under `validation/receipts/`. CI must reject a missing receipt, a hash
mismatch, failed result reconciliation, warnings, repairs, or absent analyst
approval. Raw grids reconcile source rows directly with returned rows.
Aggregates reconcile source rows with the sum of emitted group counts and their
first-seen/last-seen bounds. Coverage queries reconcile each expected table
independently.

Receipts contain a complete run set for every actual workspace where the query
will be used. Their workspace scope comes from a separate code-owned registry,
not from the receipt. Multi-table or optional-table queries also require a
controlled missing-source case. The launcher, not the receipt, declares result
mode, source tables, missing-source requirements, workspace profile, and case
thresholds.

Until raw and aggregate receipts support independent per-table availability
reconciliation, any active multi-table or optional-table query must use
coverage result mode. Its missing-source case must preserve required sources
and prove an unavailable optional source. A multi-table query without optional
sources must prove at least one unavailable declared source.

CI validates hashes, structure, thresholds, and reconciliation, but cannot
prove the provenance of manually entered execution evidence. Repository rules
must require the smoke job and final-head code-owner approval by louisgiles for
active queries and every file capable of weakening the gate. An automation may
not approve its own output.

The current static checker verifies that every launcher-declared table appears
and receives nearby time and entity filters. It does not yet derive the full
physical-table inventory from the Kusto syntax tree. Until that check exists,
final-head code-owner review must confirm that no undeclared table or unfiltered
table leg is present. This limitation must remain a tracked promotion blocker.

The active `investigation/launcher.json` manifest is machine checked against
every active path and content hash. It records domain, common incident-title
aliases, Quick/Deep/Posture role, required entity, validated default bound, and
approval status, result mode, exact table set, workspace profile, and volume
thresholds. It records both the human default bound and canonical bound seconds;
the normal validation run must use that exact duration. The human launcher must
link every same active path.

Lifecycle labels stay outside the KQL blob. The final active-form source is
validated while quarantined, then moved into `investigation/` without changing
its content. Editing the query after validation invalidates its receipt.

## Disallowed active patterns

- the KQL `search` operator in any form;
- unbounded or cross-table wildcard matching. A bounded, single-table
  `where * contains` is permitted only when broad occurrence matching is the
  named Quick question and stable fields cannot answer it reliably;
- an arbitrary final-row cap in a raw evidence query;
- global caps across multiple noisy sources;
- mandatory alert-time re-anchoring for a current incident;
- generated benign or malicious verdicts without calibrated tenant evidence;
- generic `Evidence`, `Decision`, and `NextAction` output replacing native
  evidence columns;
- Defender Advanced Hunting schema assumptions on the Sentinel Logs surface;
- raw `take`, `top`, `limit`, or `sample` row caps;
- raw output without deterministic multi-key ordering and explicit bounded-row
  count, first-event, and last-event fields;
- promotion based only on parser or lint results;
- stale archive content presented as a live fallback.

## Primary references

- [Optimize Azure Monitor log queries](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-optimization)
- [Kusto query limits](https://learn.microsoft.com/en-us/kusto/concepts/query-limits)
- [SigninLogs reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs)
- [AuditLogs reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/auditlogs)
- [Connect Defender XDR events to Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender)
- [DeviceProcessEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceprocessevents)
- [DeviceNetworkEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicenetworkevents)
- [DeviceFileEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicefileevents)
- [DeviceLogonEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicelogonevents)
- [DeviceRegistryEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceregistryevents)
- [DeviceEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceevents)
