# Threat hunts

Reusable, hypothesis-led searches across a defined population and time range.

A hunt belongs here when it states the behaviour being tested, scope, expected
benign noise, telemetry limits, and the result that warrants investigation.
It does not belong here merely because it queries multiple devices or users.

Keep live-incident pivots in `../../investigation/`, sourced candidate notes in
`../research/`, deployable alert logic in `../detections/`, and agentic
one-shots in the separate
[`louisgiles/oneshots`](https://github.com/louisgiles/oneshots) repository.

Future query-bearing modules must follow the
[`repository contract`](../../repo-contract.md). This folder is currently a
scaffold; no legacy hunt was migrated by this change.
