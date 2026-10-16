# Babbler lineage

Earlier builds of the Babbler probabilistic sign-in scorer, kept so the
design history is readable. The current single-user engine is
[`../Babbl33r.kql`](../Babbl33r.kql); the tenant-wide hunt is in
[`../../threat-work/hunts/identity/babbler-novelty/`](../../threat-work/hunts/identity/babbler-novelty/).

| File | Build | What changed |
| --- | --- | --- |
| [`v0.1.0-babbler.kql`](v0.1.0-babbler.kql) | 0.1.0 | Original probabilistic sign-in review: 90-day baseline, 24-hour score window, nine-dimension Good-Turing novelty. |
| [`v0.2.0-babbler.kql`](v0.2.0-babbler.kql) | 0.2.0 | Adds explicit health and coverage diagnostics. |
| [`v0.3.0-babbl3r.kql`](v0.3.0-babbl3r.kql) | 0.3.0 | Applicability-aware coverage; separate raw and disposition-adjusted novelty. |
| [`v0.3.1-workbench.kql`](v0.3.1-workbench.kql) | 0.3.1 | Hardened analyst workbench with cockpit outputs. |
| [`b32-one-shot-section-v0.1.0.kql`](b32-one-shot-section-v0.1.0.kql) | one-shot 0.1.0 | Union-safe `IdentityPostureSection` for the agentic one-shot. The tenant hunt is frozen to this build. |
| [`dev-checks/`](dev-checks/) | | Small `SigninLogs` ingestion-delay and flow-duplication checks used while building the scorer. |

These are history, not runtime. Use `Babbl33r.kql` for live work.
