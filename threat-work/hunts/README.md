# Threat hunts

Reusable, hypothesis-led searches across a defined population and time range.

A hunt belongs here when it states the behaviour being tested, scope, expected
benign noise, telemetry limits, and the result that warrants investigation.
It does not belong here merely because it queries multiple devices or users.

Keep live-incident pivots in `../../investigation/`, sourced candidate notes in
`../research/`, deployable alert logic in `../detections/`, and agentic
one-shots in the separate
[`louisgiles/oneshots`](https://github.com/louisgiles/oneshots) repository.

## Current modules

- [`endpoint/cloudflare-tunnel/`](endpoint/cloudflare-tunnel/) — behaviour-based Cloudflare Tunnel deployment/execution hunt with preserved validation and triage notes.

The high-volume URL file-pull hunt from open PR #13 is intentionally not folded
into this migration. Its exact branch is separately preserved at
`archive/pr-13-highvol-url-filepull-2026-08-20` so review can resolve it without
silently changing the historical PR.

Query-bearing modules follow the
[`repository contract`](../../repo-contract.md). Migration into this folder
preserves useful logic; it does not by itself promote a hunt into a detection.
