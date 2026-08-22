# Investigation

Fresh, incident-led KQL built after the 2026-08-21 blank-slate reset.
Nothing in this active tree was copied from `../archive/`.

## Fastest path

1. Start with one supplied entity in [`pivots/`](pivots/).
2. Confirm the primary event and immediate blast radius.
3. Run [`timeline/correlated-context.kql`](timeline/correlated-context.kql)
   only when a short identity, endpoint, Microsoft 365, and Azure sequence will
   change containment scope.
4. Stop when the output supports containment, closure, or a specific next
   question. Do not run every query by default.

## Active modules

| Module | Purpose |
| --- | --- |
| [`pivots/`](pivots/) | Small actor, IP, device, session, and process entry points. |
| [`timeline/`](timeline/) | A bounded cross-domain timeline for already-scoped incidents. |

## Shared output contract

Every query returns the same core columns:

| Column | Meaning |
| --- | --- |
| `EventTime` | Exact event time or the supplied anchor for a status row. |
| `EvidenceType` | `status`, `identity`, `cloud`, `m365`, `endpoint`, or a narrower subtype. |
| `Entity` | Primary entity represented by the row. |
| `RelatedEntity` | Most useful adjacent pivot. |
| `Summary` | Compact factual description. |
| `Evidence` | Bounded structured details needed to verify the summary. |
| `Decision` | `Review required` or `Suspicious / escalate`; no automatic benign conclusion. |
| `NextAction` | The next containment or evidence step. |

Each query emits an explicit status row for invalid input and for no matching
telemetry. Row-limited queries also emit a truncation row. Missing telemetry is
never reported as benign evidence.

## Design boundary

- These are investigation queries, not population hunts or detections.
- Default windows are incident-sized. Longer prevalence and baseline checks
  are explicit follow-on work.
- Queries are independently runnable and do not depend on hidden fragments.
- The base exposes evidence and next actions. Universal device-code, AiTM, and
  malware playbooks remain separate queued tasks.
- Babbler and agentic one-shot logic belongs in `louisgiles/oneshots`.

## Validation

All runnable files follow `../repo-contract.md` and are covered by the
repository KQL parser smoke test. Parser success does not prove table presence,
schema compatibility, runtime performance, or decision accuracy in a tenant.

