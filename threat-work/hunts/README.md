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

- [`endpoint/cloudflare-tunnel/`](endpoint/cloudflare-tunnel/) - behaviour-based Cloudflare Tunnel deployment/execution hunt with preserved validation and triage notes.
- [`endpoint/high-volume-url-file-pull/`](endpoint/high-volume-url-file-pull/) - scored target-service volume, file-origin, and execution hunt ported from preserved PR #13.

The legacy high-volume URL file-pull PR #13 head remains preserved at
`archive/pr-13-highvol-url-filepull-2026-08-20`. The v2 module records its
provenance and adapts it to the current hunt contract without changing that
archive.

Query-bearing modules follow the
[`repository contract`](../../repo-contract.md). Migration into this folder
preserves useful logic; it does not by itself promote a hunt into a detection.
