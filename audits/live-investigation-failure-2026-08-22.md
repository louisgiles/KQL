# Live investigation query failure record

Date: 2026-08-22

## Scope

This is a read-only audit of the active `investigation/**/*.kql` surface on
`louisgiles/KQL` main at commit
`fd5bf0a88c9b1118d085441317b26d3746af9fc7`.

The execution target is Microsoft Sentinel Log Analytics. The analyst starts
from entities already present in a live incident and needs repeatable evidence
that is fast to run and easy to read. Entity extraction is not a missing step.

All nine active files were generated on 2026-08-22. Together they contain
3,103 lines. None has a recorded exact-content Sentinel runtime validation.

## Active inventory

| Path | Lines | Audit result |
| --- | ---: | --- |
| `investigation/identity/device-code/rapid-decision.kql` | 1,167 | Not fit for live use. A 90-day multi-scan rule engine is labelled quick triage. |
| `investigation/identity/device-code/post-auth-scope.kql` | 458 | Not fit for live use. A global latest-100 cap is applied before priority. |
| `investigation/identity/device-code/campaign-scope.kql` | 309 | Not fit for live use. Exact-IP assumptions, silent set caps, and recency-first loss can misstate scope. |
| `investigation/pivots/actor.kql` | 171 | Not fit for live use. The newest 20 rows across four tables are not identity or audit posture. |
| `investigation/pivots/device.kql` | 199 | Not fit for live use. The newest 20 rows across five noisy tables can represent only minutes of activity. |
| `investigation/pivots/ip.kql` | 179 | Not fit for live use. Per-source rollups destroy chronology and silently cap values. |
| `investigation/pivots/process.kql` | 186 | Not fit for live use. The newest 30 combined events can lose the target process chain. |
| `investigation/pivots/session.kql` | 172 | Not fit for live use. Its CloudApp session branch uses the wrong time and session contracts. |
| `investigation/timeline/correlated-context.kql` | 262 | Not fit for live use. It unions OR matches and labels the result correlated. |

## Root cause 1: wrong Sentinel Log Analytics time contract

The active endpoint paths use the Defender Advanced Hunting column
`Timestamp`. The standard Sentinel Log Analytics tables use `TimeGenerated`.

Affected checked-in lines:

- `device.kql`: 42, 46, 66, 70, 89, 93, 113, 117, 136, 140.
- `ip.kql`: 95, 98.
- `process.kql`: 46, 56, 78, 83, 101, 106, 124, 129.
- `session.kql`: 104, 113.
- `correlated-context.kql`: 141, 147, 166, 172, 192, 197.

Microsoft's Azure Monitor references declare `TimeGenerated` for the Sentinel
tables used here:

- [DeviceProcessEvents](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceprocessevents)
- [DeviceFileEvents](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicefileevents)
- [DeviceNetworkEvents](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicenetworkevents)
- [DeviceRegistryEvents](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceregistryevents)
- [DeviceEvents](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceevents)
- [CloudAppEvents](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/cloudappevents)
- [Azure Monitor standard columns](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-standard-columns)

`union isfuzzy=true` does not make an existing table's wrong column contract
safe. Schema-blind parser success cannot establish compatibility.

`session.kql` has a second silent failure at lines 105-108. It looks for
top-level `SessionId` and `CorrelationId` in `CloudAppEvents` with
`column_ifexists()`. The documented Log Analytics schema exposes session
identifiers through dynamic `SessionData`. Missing top-level fields become
empty strings, so the branch can return no cloud activity while appearing to
have checked it.

## Root cause 2: global caps starve evidence sources

`device.kql` demonstrates the failure exactly:

- Lines 14-20 define `now()`, a two-hour lookback, one-hour lookforward, and
  `MaxRows = 20`.
- Lines 37-155 combine five high-volume endpoint tables.
- Line 156 keeps only the newest 21 events across all five tables.
- Line 159 keeps only the newest 20.
- Lines 197-199 sort that already-discarded slice into ascending order.

The result is not a two-hour behavioral view. It is the latest 20 eligible
events. Twenty events generated in two minutes produce approximately two
minutes of visible investigation history. A truncation row does not restore
discarded process, file, network, registry, or security evidence.

The same source-blind loss occurs in:

- `actor.kql`: lines 16-17, 129, 132, 169-171.
- `process.kql`: lines 18-19, 144, 147, 184-186.
- `session.kql`: lines 17-18, 130, 133, 170-172.
- `correlated-context.kql`: lines 19-20, 214, 217, 260-262.
- `post-auth-scope.kql`: lines 19, 22, 360, 363. Priority is only applied at
  lines 441-442, after evidence has been lost.
- `campaign-scope.kql`: lines 19, 22, 145, 150. Priority is only applied at
  lines 291-292.

`ip.kql` has silent inner caps instead. Lines 118-125 reduce all activity to one
row per source, while lines 122-124 retain only eight accounts, devices, and
activities. Chronology cannot be recovered from that rollup.

## Root cause 3: output implies analysis the query did not perform

`correlated-context.kql` matches any supplied entity with OR conditions across
its sources at lines 53-56, 79-80, 101-102, 121-122, 142-145, 167-170, and
193-195. It does not establish a relationship between the returned events.
Labelling the union a correlated timeline can imply a coherent sequence that
was never demonstrated.

The general pivots force source-native evidence into eight generic columns:
`EventTime`, `EvidenceType`, `Entity`, `RelatedEntity`, `Summary`, `Evidence`,
`Decision`, and `NextAction`. Important fields are hidden in a dynamic bag.
Generic decision and action prose repeats across rows and consumes the grid
space needed for visual comparison.

`rapid-decision.kql` is the most extreme example:

- Lines 36-41 declare thresholds that have not been tenant calibrated.
- Lines 177-565 repeatedly scan up to 90 days of `SigninLogs`.
- Lines 568-582 assemble the result through 15 scalar joins.
- Lines 800-1004 convert hard-coded classifications and novelty rules into
  `CONTAIN NOW` or `VERIFY NOW`.
- Lines 1042-1144 build a large nested evidence object.
- Lines 1145-1167 return 22 columns from a 1,167-line quick-triage file.

This replaces direct behavioral evidence with an unvalidated decision engine.
It also violates the repository audit at
`docs/archive-query-audit-2026-08-22.md` lines 165-170, which says not to put a
90-day baseline in the first query and not to label a 400-to-700-line plan a
quick dive.

## Root cause 4: zero operational validation

The repository records no exact-source live Sentinel validation:

- `investigation/README.md` lines 33-35 mark device-code, endpoint, session, and
  timeline runtime or schema validation as outstanding.
- `investigation/identity/device-code/README.md` line 25 marks all three
  device-code files outstanding.
- The same README lines 239-246 list tenant cases that have not been completed.
- `docs/kql-validation.md` lines 16-39 says the smoke test is schema-blind and
  cannot prove table presence, columns, types, runtime, or results.

A parser pass is not evidence that a query works in a live investigation. The
observed device run is negative operational evidence: it returned an unusable
20-row slice covering about two minutes.

## Archive is not a fallback

The archive contains 46 blobs: 34 source artifacts and 12 documentation files.
`docs/archive-query-audit-2026-08-22.md` lines 18-20 states that none is
approved for activation. `archive/README.md` lines 8-10 states that access does
not prove Sentinel compatibility.

Nevertheless, active `investigation/README.md` lines 11-12 and 18-19 directs
the analyst to archived workbenches when active content is unvalidated. This
replaces broken generated queries with stale unvalidated queries and must not
remain an operational route.

## Required disposition

1. Remove all nine files from the operational launcher immediately. Do not
   present any as production-ready or as a live fallback.
2. Do not reactivate archived KQL. Preserve it only as historical evidence of
   useful questions and known failure modes.
3. Rebuild the active investigation surface one query at a time for Sentinel
   Log Analytics, starting from entities already supplied by the incident.
4. Give each query one clear live-triage question, a meaningful investigation
   window, source-native readable columns, and preserved chronology.
5. Do not apply a global row cap across heterogeneous sources. Any necessary
   sampling must be explicit, source-aware, and incapable of silently removing
   an evidence class.
6. Keep observed facts separate from analyst determinations. Do not emit an
   automated containment verdict from uncalibrated heuristics.
7. Require the exact checked-in source to compile and run in the Sentinel Log
   Analytics blade against completed incidents or controlled cases in every
   actual workspace where it will be used before activation.
8. Record the commit or content hash, workspace schema, scenario, runtime, row
   behavior, coverage limits, and analyst acceptance for every activated file.
