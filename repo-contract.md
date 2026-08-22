# Repository contract

This is the authoritative contract for new and changed content in the active
v2 query base. `README.md` is the front door; a module README may strengthen
these requirements but must not weaken them.

## Scope

This contract applies to:

- `investigation/**`
- `threat-work/**`

The former numbered investigation families plus legacy `cross-family/` and
`scratchpad/` are preserved under the top-level archive and are not active
sources. The remaining `threathunting/` content is a temporary Babbler/one-shot
holding area only and must not receive new threat-hunt work. The retired
`detectionlogic/` and `threathunting-research/` roots remain recoverable from
the named legacy archive, not as active v2 locations.

## Canonical layout

```text
KQL/
├── investigation/
├── threat-work/
│   ├── hunts/
│   ├── research/
│   └── detections/
├── docs/
├── scripts/
└── tests/
```

| Area | Owns | Does not own |
|---|---|---|
| `investigation/` | Reusable queries that answer questions during a live incident. | Population-wide hunts, research notes, deployable detections, or agentic one-shots. |
| `threat-work/hunts/` | Reusable, hypothesis-led searches across a population or time range. | Single-incident triage or production alert packages. |
| `threat-work/research/` | Source-backed technical research and explicit hunt or detection candidates. | Content represented as deployment-ready without validation. |
| `threat-work/detections/` | Repeatable detection logic and its deployment, tuning, and validation material. | Unvalidated research hypotheses or one-off incident queries. |

## Executable KQL standard

Every runnable query must use the `.kql` extension and begin with a comment
header declaring:

```text
// name:              Short descriptive name
// purpose:           The question this query answers
// starting_entities: Analyst-supplied entities, or none for a population hunt
// required_tables:   Tables without which the query cannot answer its question
// optional_tables:   Enrichment tables whose absence is tolerated
// variables:         Analyst-populated let variables
// time_window:       Default and permitted investigation or hunt bounds
// done_criteria:     Evidence required to stop, contain, close, or progress
// artifact_type:     investigation | hunt | detection
// output_type:       analysis | narrative | quick-triage
```

Research Markdown and other non-executable support files do not use the KQL
header.

## Parameters and time bounds

- Put analyst inputs and tunable thresholds in a `let` block at the top.
- Do not bury investigation-scoped values in inline filters.
- Use an explicit, bounded time window. A query must not default to an unbounded table scan.
- Explain any deliberately wide baseline separately from the scoring or event window.
- Keep a runnable file paste-ready; do not require hidden fragments or manual edits outside its declared parameters.

## Module documentation

Any directory containing runnable KQL must contain a local `README.md` that
states:

- analyst purpose and when to use the module;
- required starting entities and variables;
- required, optional, and avoided data dependencies;
- time-window behaviour;
- output schema and how it changes the decision;
- done criteria and unresolved coverage limits;
- validation evidence or fixture references.

The old mandatory `deep-dive.kql` plus `narrative-gen.kql` family pairing is
retired. Modules should contain only the artifacts their operational purpose
requires.

## Dependency behaviour

Classify every referenced table in the local README:

- **Required** - absence prevents a valid answer.
- **Optional enrichment** - sparse or absent coverage is tolerated and must not suppress the primary result.
- **Avoid as hard dependency** - known freshness or coverage risk; never use it as a silent gate.

When required evidence is missing, the query or its documentation must make
that limitation visible. Do not turn missing telemetry into benign evidence.

## Purpose-oriented output

Executable queries should return the evidence shape required by their stated
purpose. Live investigation output must follow
[`docs/live-investigation-standard.md`](docs/live-investigation-standard.md):
stable source-native columns, complete bounded chronology where raw evidence is
required, and explicit coverage where aggregation is appropriate.

Do not force unrelated sources into a generic evidence bag or repeat generic
decision and next-action prose on every investigation row. Query compactness
must not be achieved by silently discarding evidence.

Where a determination is appropriate, use one of these meanings consistently:

- **Benign** - expected behaviour; no action required.
- **Precautionary benign** - likely expected; record or monitor as specified.
- **Review required** - unresolved evidence or coverage requires another check.
- **Suspicious / escalate** - evidence supports containment, escalation, or policy action.

## Area-specific readiness

### Investigation

Organise modules by investigative objective and source-native evidence type,
not by arbitrary numbering or incident title. Every active investigation query
must pass the live-investigation standard and exact-source actual-workspace validation.
Quarantined design samples remain outside `investigation/` until promotion.

### Hunts

A hunt must state its hypothesis, population, window, expected benign noise,
coverage limits, and the output that warrants deeper investigation. A hunt is
not automatically a detection candidate.

### Research

Research must distinguish sourced fact, analyst inference, and proposed
hypothesis. Record source and observation dates where they affect validity.
Promotion into `hunts/` or `detections/` is an explicit reviewed change.

### Detections

A production-ready detection package must keep its KQL with a local README,
analytic-rule YAML where applicable, tuning guidance, and a validation or test
fixture reference. Detailed naming and packaging conventions may strengthen
this baseline in the queued folder-contract task.

Migrated legacy detection logic may remain explicitly marked as a candidate
while its semantics, dependencies, and tuning are revalidated; migration into
`threat-work/detections/` is not by itself a production-readiness claim.

## One-shot boundary

Agentic one-shots, Babbler stages, caller contracts, and their validation
lineage belong in `louisgiles/oneshots`. Do not create a second active
implementation under `investigation/` or `threat-work/`.

Legacy Babbler and one-shot source must remain recoverable in KQL until the
destination implementation has been verified. Migration must preserve useful
history before removing a source copy.

## Validation

- Run `pwsh ./scripts/test-kql.ps1` for syntax-level validation of `.kql` files.
- Validate live evidence queries against sparse, normal, high-volume, no-data,
  missing-source where applicable, result-integrity, runtime, and analyst-utility
  cases in the actual workspace.
- Use known-benign, ambiguous, and known-suspicious cases only for calibrated
  determination logic that actually emits a determination.
- Record schema, table-coverage, and runtime limitations; the parser cannot validate them.
- A passing parser check is necessary, not sufficient, evidence of readiness.
