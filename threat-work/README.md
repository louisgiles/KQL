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

The audited legacy threat-work material is now consolidated here:

- `hunts/endpoint/cloudflare-tunnel/` — Cloudflare Tunnel deployment/execution hunt plus preserved analysis notes.
- `research/2026/` — dated threat-hunting candidates and CVE research.
- `detections/ddns/` — migrated DDNS detection candidates and their dependency/validation notes.

All executable content follows the
[`repository contract`](../repo-contract.md). Agentic one-shots and Babbler
pipeline logic remain in the separate
[`louisgiles/oneshots`](https://github.com/louisgiles/oneshots) repository.

The only remaining legacy `threathunting/` artifact on active `main` is the
Babbler-derived tenant research file that is explicitly queued for migration to
`oneshots`. The original pre-consolidation roots remain recoverable from the
named archive branch.
