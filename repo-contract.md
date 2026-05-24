# Repo Contract

The rules every `.kql` file and family folder in this repo is expected to follow.
This document is the authoritative reference; `README.md` remains the front door.

## Query standard

Every `.kql` file must declare these fields in a comment block at the top:

```
// name:              Short descriptive name
// purpose:           One sentence — what this query answers
// starting_entities: What the analyst provides (e.g. UPN, IP, SessionId)
// required_tables:   Tables the query breaks without
// optional_tables:   Enrichment tables — graceful failure if absent
// variables:         let-block variables the analyst populates
// done_criteria:     What "finished investigating" looks like
// output_type:       analysis | narrative
```

## Parameterisation

All analyst-supplied inputs go in a `let` block at the top of every query.
No inline filters for investigation-scoped values.

```kql
let targetUser = "";
let lookback = 14d;
let targetIP = "";
```

## Family structure

Every investigation family contains:

| File | Status | Purpose |
|---|---|---|
| `deep-dive.kql` | Required | Evidence engine — structured analytical output |
| `narrative-gen.kql` | Required | Closure-ready note generation |
| `notes.md` | Required | Use case, starting entities, done criteria, data dependencies |
| `quick-dive.kql` | Optional | Fast decision-gate triage — one-row-ish output that tells the analyst whether the deep-dive is worth running |

Endpoint is the exception — it uses three deep dives (process, file, network)
instead of one. Each endpoint sub-family follows the same file contract:
required `deep-dive.kql` + `narrative-gen.kql` + `notes.md`, optional
`quick-dive.kql`.

### `quick-dive.kql` (optional)

A family or sub-family may ship zero or one `quick-dive.kql`. Its job is fast
prevalence-first triage: enough signal to decide whether to escalate to the
deep-dive, not a full investigation. It must carry the full contract header
block with `output_type: quick-triage`. Absence of a `quick-dive.kql` is not
drift — it just means the family hasn't needed one.

## Scratchpad

`scratchpad/` is a top-level folder for precise one-off tool queries that
do not recur often enough to belong to a family. Examples: a single
investigation's bespoke join, an ad-hoc check tied to a specific alert
shape, a query written for one ticket and kept for reference.

Scratchpad queries are **explicitly exempt from the family contract**:

- No mandatory header block.
- No companion `narrative-gen.kql`.
- No `notes.md`.
- No `.kql` extension policing (recommended but not required).
- They are never counted as a family and never re-flagged as drift or as
  an incomplete family in audits.

If a scratchpad query starts being reached for repeatedly, promote it
into a family (or a sub-family under an existing family) and apply the
full contract at that point.

## Data dependency tags

Every table referenced in a query gets one of three tags in the family's
`notes.md`:

- **Required** — query breaks without it.
- **Optional enrichment** — left-outer joined or coalesced; sparse results
  are fine.
- **Avoid as hard dependency** — known coverage or freshness issues; never
  use in `where` clauses.

## Closure language

Four determination buckets. Match the pattern, not the exact wording:

- **Benign** — expected behaviour, no action required.
- **Precautionary benign** — likely fine, worth noting or monitoring.
- **Review required** — ambiguous, needs senior eyes or additional context.
- **Suspicious / escalate** — indicators of compromise or policy violation.

## Validation

Each family maintains three test cases in `notes.md`:

- Known benign.
- Ambiguous.
- Known bad or clearly suspicious.

New query versions run against all three before merge.

## Folder layout

```
kql/
├── README.md
├── repo-contract.md
├── 01-sign-in/
├── 02-auth-changes/
├── 03-office-ops/
├── 04-azure-activity/
├── 05-endpoint/
├── 06-email/
├── cross-family/
└── scratchpad/
```

Current folders in this repo use slightly different names (`identity/`,
`authentication/`, `office-activity/`, `azure-activity/`, `endpoint/`,
`email/`). They map 1:1 to the numbered folders above and are treated as
the same families under the contract.
