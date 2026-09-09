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
- [`resprox-research-loops.md`](resprox-research-loops.md) — three-stage residential-proxy research restart, evidence gates and current state; includes a fixed link to the completed L01–L15 record.
- [`resprox-direction-reviews.md`](resprox-direction-reviews.md) — closure of the former timed direction-review programme and link to its historical record.

## ResProx working requirement

Read the latest main-branch `resprox-research-loops.md` and follow its current
stage, evidence gates and stop conditions. The former timed direction-review
requirement is superseded by Louis's requested task-list redraft. R1–R3 start
only when instructed; editing the plan does not execute research or resume
the paused automations. Read historical findings selectively where relevant.

This changes ResProx planning only. Existing repository scope, source,
telemetry, validation and concurrency requirements still apply.

The prior standalone Cloudflare scratchpad was not kept here as an orphaned
research file; it now lives with the related hunt as preserved supporting notes
under `../hunts/endpoint/cloudflare-tunnel/`.

The [`repository contract`](../../repo-contract.md) governs this area; its KQL
header requirements apply only to executable files.
