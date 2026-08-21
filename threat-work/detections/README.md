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

## Current modules

- [`ddns/`](ddns/) — migrated DDNS detection candidates covering bulletproof-hosting ranges, DDNS subdomains, DDNS URL clicks, and non-browser DDNS egress.

These files were structurally consolidated from the legacy `detectionlogic/`
root and given active-tree metadata, but migration is not a production-readiness
claim. The module README records inherited dependency and tuning gaps that must
be resolved before deployment.

Detection packages follow the
[`repository contract`](../../repo-contract.md).
