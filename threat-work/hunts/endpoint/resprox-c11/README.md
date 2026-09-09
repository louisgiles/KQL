# C11: familiar executable, changed observed destinations

Draft hunt for retrospective testing in **Microsoft Sentinel / Log Analytics**.
It asks whether a previously observed executable SHA1 contacted a hostname absent
from its own observed history. It does not establish forwarding, unauthorized
use, or a continuously unchanged installation. Configuration, modules, users and
purpose can change while the executable hash stays the same.

This implements the narrowed [C11 research design](../../../research/resprox-research-loops.md)
and [Q04 comparison](../../../research/resprox-direction-reviews.md). It does not
complete a research pass or constitute a deployed detection.

## Run the back-test

1. Open **Logs** in one customer workspace. Start with a small, known Windows
   device cohort using `DeviceIds`; optionally restrict `ProcessNames`. Empty
   filters select the whole workspace and can be expensive.
2. Run [coverage.kql](./coverage.kql). Its default split is 2026-08-19 through
   2026-09-02 for baseline, then 2026-09-02 through 2026-09-09 for candidates.
   Set the same fixed UTC `EndTime`, cohort and windows in both queries. Use
   complete days: 7 candidate days and 14 baseline days; keep any experiment
   within 1–7 candidate and 7–28 baseline days. Include the full interval in the
   Logs time selector. A baseline shorter than retention permits is inconclusive.
3. Inspect action/field availability. Coverage inventories actions separately;
   [backtest.kql](./backtest.kql) defaults to `ConnectionSuccess`. An empty coverage
   result means no matching observations, not absence of proxy activity.
4. Run `backtest.kql`. Review `Comparison`, both novelty flags, assessment
   columns, hostname fractions and hash examples. `MinBaselineNamedDays=3`
   requires three baseline days with usable names; this is an experimental
   support rule, not a validated threshold or sensor-uptime measurement.
5. Set `IncludeUnchanged=true` when exporting a complete observed-host panel
   for labelled comparison. Export coverage too: entities with no usable
   candidate hostname cannot appear in the destination result.

Repeat earlier fixed splits separately. Baseline is `[BaselineStart, CandidateStart)`;
candidate is `[CandidateStart, EndTime)`. No candidate event enters the baseline.
This is an event-time retrospective query over currently retained records, not
an online replay of when late events became available.

## Read the comparison correctly

The application key is workspace ID (`TenantId`), device ID, lower-case process
folder path and filename. This location-based Windows comparator is not verified
product identity. C11 adds SHA1 to that same key. A moved path or new hash may
lose history; it must not become an automatic anomaly.

| Result | Meaning / next action |
|---|---|
| Both methods | Hostname absent from observed build history and application history; check expected workload/configuration changes. |
| C11 only | Application saw the hostname under another or unknown hash. Inspect upgrades, reversions and parallel versions before treating the distinction as useful. |
| Unassessable | Missing identity/hash/named history or sparse support. Inspect coverage; null is not false. |
| Neither method | Observed before; retained with `IncludeUnchanged=true`. This is not a benign verdict. |
| Unexpected comparator inconsistency | Stop and inspect query/source changes; on matched support an app-new host must also be build-new. |

Hash-specific baseline destinations are a subset of application baseline
destinations. Therefore C11 can **add** destination leads to this comparator;
more hits do not establish better detection. `MultipleHashesObserved` and up to
eight hash examples expose mixed-build context. No peer-rarity gate, reputation
filter, browser exclusion, score or top-N truncation is applied.

The result unit is workspace/device/application/hash/observed hostname, with one
latest raw witness and its process ID/start key, event time and ReportId. Use
that witness when pivoting (equal timestamps may select a different witness); do not lend its process context to every event in
the seven-day aggregate. Per-build/application counts repeat across destination
rows: deduplicate their respective keys before measuring population coverage.
Event-row counts are not bytes, concurrent sockets, unique requests or forwarding
volume. Duplicate ingestion may affect counts but not destination membership.

## Telemetry and coverage limits

- **Required:** `DeviceNetworkEvents`, populated identity/history/name fields,
  and a query context supporting the joins used here. Table, retention, table
  plan and field population are unconfirmed. `TimeGenerated` is the documented
  endpoint-recorded event time; `TenantId` is the workspace ID, not an Entra
  directory identifier. [Microsoft table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicenetworkevents).
- **Destination lane:** lowercase exact observed hostname from `RemoteUrl`
  URL/FQDN; discard URL paths and a trailing dot. IP literals, single-label names,
  invalid names and missing names are excluded from this lane and remain in
  coverage counts. No fallback to `RemoteIP`, domain-root reduction, later DNS
  resolution or claim that the name equals the physical peer. The witness keeps
  the original name and peer separately. [URL parsing](https://learn.microsoft.com/en-us/kusto/query/parse-url-function).
- **Optional investigation:** process lineage/modules, event-time software
  configuration and approval, current role-valid control intelligence, or
  receiver/task evidence. None is queried or assumed present. Avoid feeds,
  sign-ins and additional endpoint tables as hard dependencies for this test.
- Observed active days and name fractions do not prove collection continuity.
  Verify comparable onboarding, routing/name visibility and retention before
  interpreting absence from baseline. Treat changed visibility as inconclusive.
  `ConnectionSuccess` is a transport observation, not application acceptance or
  proof that another control allowed the traffic.

The reused event set is time/cohort/action filtered and projected before
`materialize`. Start small and record runtime; its shared per-node cache is
limited, and no runtime or cost benchmark is claimed.
[Microsoft materialize guidance](https://learn.microsoft.com/en-us/kusto/query/materialize-function).

## Decide whether the extra hash condition earns its place

Freeze the split, cohort, baseline support and review budget before inspecting
outcomes. Use the same destination results, collapse to the same
device/application case unit, and deduplicate common cases. Have a reviewer
adjudicate with method labels hidden where practical. Record a concrete changed
investigation decision and review time, not just counts. Compare matched-eligible
cases separately from the broader app comparator; use coverage to report losses
from absent hashes/names, new builds and short history.

Include ordinary feature/configuration changes, upgrades/reversions, unchanged
workloads and approved forwarding. Label observed audience change, independently
confirmed role change, relay participation and event-time authorization separately.
Unknown labels stay unknown. Reject the exact-build addition if it produces no
reproducible decision/review-effort benefit or primarily adds version-history
artefacts. Without independent forwarding truth, report no relay precision/recall.

## Validation

On 2026-09-09, both queries passed Microsoft
`@kusto/language-service-next@12.4.1` syntax and semantic binding against an explicit
schema from the current Microsoft table reference. Positive, unknown-column and
malformed-syntax controls verified the checker. Independent code review checked
join cardinality, missingness and comparator semantics. The repository's
`pwsh ./scripts/test-kql.ps1` could not run locally because PowerShell and .NET
are absent. No Kusto engine, sensor/lab, customer data or tenant execution ran;
the following are **designed expected cases**, not executed KQL results.

| Case (adequate named history unless stated) | Expected C11 / app result |
|---|---|
| Same hash, previously seen hostname | false / false |
| Same hash, hostname absent under every prior hash | true / true |
| Hostname seen under another prior hash only | true / false; other/unknown-hash flag |
| Current hash new at this path; app has history; new hostname | null / true |
| Current hash absent; app has history; new hostname | null / true |
| No baseline hostname observations at all | null / null |
| Fewer than three named baseline days for the build | C11 null; comparator depends on its own support |
| Approved and unauthorized forwarding with identical observations | Same flags; approval requires independent evidence |
| Candidate names absent/IP-only | No destination row; visible coverage exclusion |
| Event exactly at split / end | Candidate / excluded |

An adjudicated unexpected role change warrants configuration/ownership and
process investigation. Containment or a proxy-abuse conclusion requires
additional evidence. Useful hunt value and research novelty remain unproved.
