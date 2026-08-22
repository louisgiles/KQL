# Investigation

Fresh, incident-led KQL built after the 2026-08-21 blank-slate reset.
Nothing in this active tree was copied from `../archive/`.

## Runtime status

> **Operational stop:** none of these files currently has a `passed`
> exact-content receipt in `../validation/sentinel-live.json`. Do not use a
> pending or failed file in a live incident. The repository parser and static
> lint are preflight checks only.

## Fastest path

1. Confirm the selected file is marked `passed` for its exact SHA in the
   live-validation manifest.
2. If the incident matches a validated rapid-decision module, run that module
   first.
3. If a preserved family better matches the incident, use the
   [`archived investigation launcher`](../archive/) only after reviewing its
   compatibility status.
4. Otherwise use one supplied entity in [`pivots/`](pivots/) only after that
   exact file is validated.
5. Confirm the primary event and immediate blast radius.
6. Run [`timeline/correlated-context.kql`](timeline/correlated-context.kql)
   only when a short identity, endpoint, Microsoft 365, and Azure sequence will
   change containment scope and the exact file is validated.
7. Stop when the output supports containment, closure, or a specific next
   question. Do not run every query by default.

## Active modules

| Module | Current state | Purpose |
| --- | --- | --- |
| [`identity/device-code/`](identity/device-code/) | Pending live rerun | One-row rapid containment decision for a suspicious direct device-code sign-in. |
| [`pivots/`](pivots/) | Failed or pending | Small actor, IP, device, session, and process entry points. |
| [`timeline/`](timeline/) | Failed | A bounded cross-domain timeline for already-scoped incidents. |

## Rapid-decision coverage

**1 of 10 implemented. 0 of 10 live-validated. 9 remain unimplemented.**

| Decision | Status |
| --- | --- |
| Suspicious device-code authentication | Implemented, corrected, and awaiting exact-content Sentinel validation. |
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
- The device-code rapid decision is a candidate. The broader universal device-code
  playbook and the AiTM and malware playbooks remain queued tasks.
- Babbler and agentic one-shot logic belongs in `louisgiles/oneshots`.

## Validation

The parser and static lint are preflight only. Operational status is determined
solely by `../validation/sentinel-live.json`. The 2026-08-22 audit found
deterministic Sentinel blockers in the device, IP, process, session, timeline,
and device-code files. No file in this directory may be represented as usable
until its exact SHA is marked `passed`.
