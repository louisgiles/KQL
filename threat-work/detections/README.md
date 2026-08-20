# Detection engineering

Reusable alert logic intended for repeatable deployment, tuning, validation,
and maintenance.

A production-ready detection package should keep its KQL with a local README,
analytic-rule YAML where applicable, tuning guidance, and a validation or test
fixture reference. Hypotheses that are not ready for that lifecycle belong in
`../research/` or `../hunts/`.

Keep per-incident pivots in `../../investigation/` and agentic one-shot or
Babbler pipeline logic in the separate
[`louisgiles/oneshots`](https://github.com/louisgiles/oneshots) repository.

Future detection packages must follow the
[`repository contract`](../../repo-contract.md). This folder is currently a
scaffold; no legacy detection was migrated by this change.
