# Threat work

The common active parent for threat hunting, threat research, and detection
engineering.

| Area | Purpose |
|---|---|
| [`hunts/`](hunts/) | Test reusable threat hypotheses across a population or time range. |
| [`research/`](research/) | Preserve sourced analysis and explicit hunt or detection candidates. |
| [`detections/`](detections/) | Maintain repeatable detection logic and its deployment, tuning, and validation material. |

Research may produce a hunt or detection candidate, and a validated hunt may
inform a detection, but promotion between areas is always explicit and
reviewed. Do not treat proximity in the repository as proof of production
readiness.

All executable content follows the
[`repository contract`](../repo-contract.md). Agentic one-shots and Babbler
pipeline logic remain in the separate
[`louisgiles/oneshots`](https://github.com/louisgiles/oneshots) repository.

This is a scaffold only. Consolidation of the frozen `threathunting/`,
`threathunting-research/`, and `detectionlogic/` roots is a separate queued
task; no legacy artifact was migrated here.
