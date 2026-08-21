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

The prior standalone Cloudflare scratchpad was not kept here as an orphaned
research file; it now lives with the related hunt as preserved supporting notes
under `../hunts/endpoint/cloudflare-tunnel/`.

The [`repository contract`](../../repo-contract.md) governs this area; its KQL
header requirements apply only to executable files.
