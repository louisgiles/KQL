# 03-office-ops

Office / M365 operations investigation family. Scope: mailbox rule
creation, inbox manipulation, SharePoint / OneDrive access patterns,
Teams activity, mass file downloads, and delegation changes.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | TODO — empty stub. |
| `narrative-gen.kql` | narrative | TODO — not yet authored. |

## Starting entities

- TODO (likely: UPN, client IP, mailbox identifier, SiteUrl).

## Required tables

- TODO (likely: `OfficeActivity`).

## Optional tables

- TODO (likely: `CloudAppEvents` — **optional enrichment** for MCAS /
  Defender for Cloud Apps; `EmailEvents` — **optional enrichment**
  when the pivot is an inbox rule).

## Done criteria

- TODO. Every non-routine operation has an identified actor; new
  inbox rules inspected; mass-download events classified; external
  sharing classified against policy.

## Validation — test cases

1. **Known benign — TODO.** User organises mail into personal folders
   via a new inbox rule scoped to internal senders.
2. **Ambiguous — TODO.** User downloads several hundred files from a
   SharePoint site during an offboarding window.
3. **Known bad / clearly suspicious — TODO.** New inbox rule named " "
   that forwards all messages to an external address and marks as
   read.
