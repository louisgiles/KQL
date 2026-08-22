# KQL

A personal, incident-ready KQL library for SOC investigation, threat hunting,
threat research, and detection engineering in Microsoft Sentinel and Defender.

## Design principles

1. **Clarity** — live environments are loud; queries should expose the evidence that changes the decision.
2. **Minimalism** — use the smallest query that answers the investigative question.
3. **Speed** — keep time windows and table scans bounded.
4. **Humility** — make uncertainty and missing coverage visible.
5. **Concision** — prefer compact, decision-oriented output over raw event dumps.

## Active v2 entry points

| Canonical area | Purpose |
|---|---|
| [`investigation/`](investigation/) | Reusable, incident-led investigation queries and playbooks. |
| [`threat-work/hunts/`](threat-work/hunts/) | Hypothesis-led, population-wide threat hunts. |
| [`threat-work/research/`](threat-work/research/) | Source-backed research and hunt or detection candidates. |
| [`threat-work/detections/`](threat-work/detections/) | Reusable detection-engineering logic and production rule packages. |

The active `threat-work/` tree contains the audited threat-hunt, research,
and detection-engineering material migrated from the legacy roots. The active
`investigation/` tree now provides fresh actor, IP, device, session, process,
and correlated-timeline entry points built after the blank-slate reset.

## Choose the right area

- Investigating a live user, device, IP, session, process, message, or resource: start in `investigation/`.
- Testing a threat hypothesis across a population or time range: use `threat-work/hunts/`.
- Recording sourced intelligence, technical analysis, or a candidate idea: use `threat-work/research/`.
- Building or tuning alert logic intended for repeatable deployment: use `threat-work/detections/`.
- Building agentic one-shot or Babbler pipeline logic: use [`louisgiles/oneshots`](https://github.com/louisgiles/oneshots), not an active KQL area.

The authoritative requirements for active content are in
[`repo-contract.md`](repo-contract.md). Validation guidance lives in
[`docs/kql-validation.md`](docs/kql-validation.md), with tooling under
[`scripts/`](scripts/), [`tests/`](tests/), and [`.github/`](.github/).

## Migration boundary

The former numbered investigation families, `cross-family/`, and `scratchpad/`
are preserved beneath `archive/investigation-legacy-2026-08-21/`. Active
`investigation/` content is implemented from current requirements rather than
copied or promoted from the archive.

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
```

The smoke test is grammar-only. Table availability, schema coverage, runtime
semantics, and analyst decisions still require validation against the intended
environment.

This is a personal reference library rather than an open-source project. All
work is my own; feel free to fork and adapt it for your environment.
