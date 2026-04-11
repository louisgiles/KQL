# office-activity (≈ 03-office-ops)

Office / M365 operations investigation family. Scope: mailbox rule
creation, inbox manipulation, SharePoint/OneDrive access patterns, Teams
activity, mass file downloads, and delegation changes.

## Use case

An analyst arrives with a signal that a user's Office footprint has
changed in a suspicious way: a new inbox rule forwarding externally,
mass OneDrive downloads, unusual SharePoint site access, delegation
granted on a mailbox. This family surfaces those events and correlates
them to the source identity.

## Starting entities

- UPN
- Client IP
- SiteUrl / mailbox identifier

## Queries in this family

| File | Role | Notes |
|---|---|---|
| `office-activity-deep-dive` | deep-dive (analysis) | **Stub — empty.** See compliance notes below. |

No `narrative-gen.kql` yet.

## Data dependencies

Planned once the deep dive is authored:

| Table | Tag |
|---|---|
| `OfficeActivity` | **Required** |
| `CloudAppEvents` | **Optional enrichment** — MCAS/Defender for Cloud Apps supplementary context. |
| `EmailEvents` | **Optional enrichment** — when the pivot is an inbox rule. |

## Done criteria

Triage is finished when:

1. Every non-routine operation in the window has an identified actor.
2. New inbox rules have been read for forwarding or deletion patterns.
3. Mass-download events have been classified against normal user
   behaviour.
4. Any external sharing has been classified against org policy.
5. The event has been mapped to one of the four closure buckets.

## Closure language

- **Benign** — expected business usage within baseline thresholds.
- **Precautionary benign** — bulk download from a leaving user during
  an approved handover window.
- **Review required** — new inbox rule that isn't obviously forwarding,
  or unusual site access pattern without a clear business reason.
- **Suspicious / escalate** — inbox rule forwarding externally or
  auto-deleting matches; mass download followed by external sharing;
  delegation granted to an unexpected principal.

## Validation — test cases

1. **Known benign.** User organises mail into personal folders via a
   new inbox rule scoped to internal senders only.
2. **Ambiguous.** User downloads 500 files from a SharePoint site
   during an offboarding window.
3. **Known bad / clearly suspicious.** New inbox rule named " " that
   forwards all messages to an external address and marks as read.

## Contract compliance notes

- `office-activity-deep-dive` is an empty 1-byte placeholder and is
  missing the `.kql` extension. It should be authored to the contract
  or flagged for deletion.
- No `narrative-gen.kql` exists — author or flag.
