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

| File | Purpose |
|---|---|
| `deep-dive.kql` | Evidence engine — structured analytical output |
| `narrative-gen.kql` | Closure-ready note generation |
| `notes.md` | Use case, starting entities, done criteria, data dependencies |

Endpoint is the exception — it uses three deep dives (process, file, network)
instead of one.

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
└── cross-family/
```

Current folders in this repo use slightly different names (`identity/`,
`authentication/`, `office-activity/`, `azure-activity/`, `endpoint/`,
`email/`). They map 1:1 to the numbered folders above and are treated as
the same families under the contract.
