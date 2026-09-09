# Threat research

Source-backed technical research and explicit candidates for later hunting or
detection work.

Research belongs here when it separates sourced fact, analyst inference, and a
testable hypothesis, with source and observation dates where freshness matters.
Research is not represented as executable or production-ready until it is
reviewed and promoted into `../hunts/` or `../detections/`.

Keep per-incident investigation in `../../investigation/` and agentic one-shot
development in the separate
[`louisgiles/oneshots`](https://github.com/louisgiles/oneshots) repository.

## Current material

- [`2026/`](2026/) — migrated dated research, including the seven-day threat-hunting candidate review and CVE-2026-18577 notes.
- [`resprox-research-loops.md`](resprox-research-loops.md) — canonical residential-proxy research programme, evidence, candidate register and pass state.
- [`resprox-direction-reviews.md`](resprox-direction-reviews.md) — Louis-authorized 120-minute direction-review gate and refinements to the remaining ResProx tasks.

## ResProx invocation requirement

For work on `resprox-research-loops.md`, read the latest main-branch
`resprox-direction-reviews.md` at the start of every invocation alongside the
canonical programme. Check whether its 120-minute direction review is due and
apply its pending-task refinements before executing the one permitted numbered
pass. During the normal canonical save, carry the applicable refinements into
the task/handoff without rewriting completed findings or advancing extra passes.
These requirements apply only to ResProx; all existing repository, telemetry,
validation, concurrency and safety boundaries remain in force.

The review file is an invocation-time gate, not a scheduler. Do not claim a
new timer or unattended review was enabled by this documentation change.

The prior standalone Cloudflare scratchpad was not kept here as an orphaned
research file; it now lives with the related hunt as preserved supporting notes
under `../hunts/endpoint/cloudflare-tunnel/`.

The [`repository contract`](../../repo-contract.md) governs this area; its KQL
header requirements apply only to executable files.
