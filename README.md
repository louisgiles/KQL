# KQL

A personal KQL workbench for SOC investigation, threat hunting,
threat research, and detection engineering in Microsoft Sentinel and Defender.

> **Operational stop:** active placement does not mean incident-ready. Only an
> exact file SHA marked `passed` in
> [`validation/sentinel-live.json`](validation/sentinel-live.json) may be used
> as a validated query. Every current active query is pending or failed as of
> 2026-08-22.

## Design principles

1. **Clarity:** live environments are loud; queries should expose the evidence that changes the decision.
2. **Minimalism:** use the smallest query that answers the investigative question.
3. **Speed:** keep time windows and table scans bounded.
4. **Humility:** make uncertainty and missing coverage visible.
5. **Concision:** prefer compact, decision-oriented output over raw event dumps.

## Active v2 entry points

| Canonical area | Purpose |
|---|---|
| [`investigation/`](investigation/) | Reusable, incident-led investigation queries and playbooks. |
| [`threat-work/hunts/`](threat-work/hunts/) | Hypothesis-led, population-wide threat hunts. |
| [`threat-work/research/`](threat-work/research/) | Source-backed research and hunt or detection candidates. |
| [`threat-work/detections/`](threat-work/detections/) | Reusable detection-engineering logic and production rule packages. |

## Archived investigation workbenches

The [`archive launcher`](archive/) provides direct access to all preserved
quick dives, deep dives, narrative generators, and focused investigation
utilities. Use its compatibility status before copying a query into Sentinel.
The archive is accessible reference material, not a runtime-readiness claim.

The active `threat-work/` tree contains the audited threat-hunt, research,
and detection-engineering material migrated from the legacy roots. The active
`investigation/` tree now provides fresh actor, IP, device, session, process,
and correlated-timeline candidates built after the blank-slate reset.
Operational state comes only from the live-validation manifest.

## Choose the right area

- Investigating a live user, device, IP, session, process, message, or resource: start in `investigation/`.
- Testing a threat hypothesis across a population or time range: use `threat-work/hunts/`.
- Recording sourced intelligence, technical analysis, or a candidate idea: use `threat-work/research/`.
- Building or tuning alert logic intended for repeatable deployment: use `threat-work/detections/`.
- Building agentic one-shot or Babbler pipeline logic: use [`louisgiles/oneshots`](https://github.com/louisgiles/oneshots), not an active KQL area.
- Reusing a previous quick dive, deep dive, or narrative while the active v2
  surface is rebuilt: start at the [`archive launcher`](archive/).

The authoritative requirements for active content are in
[`repo-contract.md`](repo-contract.md). Validation guidance lives in
[`docs/kql-validation.md`](docs/kql-validation.md), with tooling under
[`scripts/`](scripts/), [`tests/`](tests/), and [`.github/`](.github/).

## Migration boundary

The former investigation workbenches are preserved directly beneath
[`archive/investigation/`](archive/investigation/) and indexed from the
[`archive launcher`](archive/). Babbler, probe, and one-shot lineage remains
beneath `archive/investigation-legacy-2026-08-21/`. Active `investigation/`
content is implemented from current requirements rather than silently copied
or promoted from the archive.

The old `detectionlogic/` and `threathunting-research/` roots have been retired
from active `main` after their useful content was consolidated beneath
`threat-work/`. The remaining `threathunting/` content is Babbler-derived
research only; it stays temporarily in place until the queued `oneshots`
migration verifies the destination copy.

The exact pre-reset tree is preserved at
[`archive/legacy-2026-08-20`](https://github.com/louisgiles/KQL/tree/archive/legacy-2026-08-20)
at commit `409ff36da16d8b43e0248e17d2a81f65d8a07db2`. The unmerged high-volume
URL file-pull hunt from PR #13 is separately preserved at
[`archive/pr-13-highvol-url-filepull-2026-08-20`](https://github.com/louisgiles/KQL/tree/archive/pr-13-highvol-url-filepull-2026-08-20).

Babbler and one-shot source material stays recoverable in KQL until its
destination in `louisgiles/oneshots` has been verified.

## Validation

Runnable queries use the `.kql` extension and are syntax-checked with:

```powershell
pwsh ./scripts/test-kql.ps1
python3 ./scripts/lint-kql-runtime-literals.py .
python3 ./scripts/check-sentinel-live-validation.py . --all
```

The parser and static lint are preflight checks only. A new or changed KQL file
must execute successfully in its declared surface, then receive a
content-bound live-validation record before it can be pushed or merged as
usable. Any content change invalidates the record.

This is a personal reference library rather than an open-source project. All
work is my own; feel free to fork and adapt it for your environment.
