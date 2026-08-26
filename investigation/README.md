# Investigation

Fresh, incident-led KQL built after the 2026-08-21 blank-slate reset.
Nothing in this active tree was copied from `../archive/`.

## Runtime status

The repository parser is grammar-only. An active query is not operationally
ready until its exact source has compiled and executed in the intended
Sentinel Log Analytics workspace. Until that evidence is recorded, use the
[`archived investigation launcher`](../archive/) when a preserved workbench
better matches the incident.

## Fastest path

1. Run an active rapid-decision module first only when its exact version has
   passed Sentinel runtime validation in the workspace.
2. If a preserved family matches the incident, open its quick or deep dive
   directly from the [`archive launcher`](../archive/).
3. Use [`pivots/`](pivots/) only for a narrower question that the family
   workbench does not answer.
4. Confirm the primary event and immediate blast radius.
5. Run [`timeline/correlated-context.kql`](timeline/correlated-context.kql)
   only when a short identity, endpoint, Microsoft 365, and Azure sequence will
   change containment scope.
6. Stop when the output supports containment, closure, or a specific next
   question. Do not run every query by default.

## Active modules

| Module | Purpose |
| --- | --- |
| [`identity/device-code/`](identity/device-code/) | Quick rapid decision plus deep post-authentication and exact-IP campaign scope. Tenant runtime validation remains outstanding. |
| [`playbooks/device-code-auth/`](playbooks/device-code-auth/) | Four-step Occam's-razor triage sequence: sign-in deep dive, user precedent, tenant prevalence, 24h audit sweep. Tenant runtime validation remains outstanding. |
| [`pivots/`](pivots/) | Small actor, IP, device, session, and process candidates. Endpoint and session branches require Sentinel schema validation. |
| [`timeline/`](timeline/) | A bounded cross-domain timeline candidate. Endpoint branches require Sentinel schema validation. |

## Rapid-decision coverage

**1 of 10 implemented. 9 remaining. Runtime validation is tracked separately.**

| Decision | Status |
| --- | --- |
| Suspicious device-code authentication | Implemented in [`identity/device-code/`](identity/device-code/); tenant runtime validation outstanding. |
| Remaining high-frequency malicious investigation classes | 9 not yet implemented. |

The remaining nine classes must be explicitly named and prioritised before
implementation. They are not inferred from archived queries or generic alert
categories.

## Pivot and timeline output contract

General pivots and the correlated timeline return these core columns:

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

Each general query emits an explicit status row for invalid input and for no
matching telemetry. Row-limited queries also emit a truncation row. Missing
telemetry is never reported as benign evidence.

Rapid-decision modules may instead return a compact one-row determination
contract documented in their local README. They must still expose invalid
scope, missing coverage, decisive evidence, and the immediate next action.

## Design boundary

- These are investigation queries, not population hunts or detections.
- Default windows are incident-sized. Longer prevalence and baseline checks
  are explicit follow-on work.
- Queries are independently runnable and do not depend on hidden fragments.
- The three-query device-code investigation path and the four-step
  device-code playbook under [`playbooks/`](playbooks/) are active. The AiTM
  and malware playbooks remain queued tasks.
- Babbler and agentic one-shot logic belongs in `louisgiles/oneshots`.

## Validation

All runnable files follow `../repo-contract.md` and are covered by the
repository KQL parser smoke test. Parser success does not prove table presence,
schema compatibility, runtime performance, or decision accuracy in a tenant.
