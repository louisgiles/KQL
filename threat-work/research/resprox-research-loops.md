# ResProx — three-stage research restart

**Status:** redrafted; not started. This edit does not run research or resume the paused automations.  
**Start:** an explicit instruction to run R1. After that, evidence gates govern progression; routine authorized research needs no repeated permission.  
**Scope:** public-source research and this research file. Collection, tenant execution, hunt-module changes and production promotion are separate work.

## Objective

Find a defensible, potentially distinctive way to identify managed endpoints worth investigating for undisclosed residential-proxy activity in Microsoft Sentinel / Log Analytics. It must offer a plausible improvement in an analyst's next decision over a simpler hunt.

Keep observed activity, proxy participation, unauthorized use, network exposure, endpoint compromise and session compromise separate. Known software-governance/IOC hunts can be useful baselines; they do not satisfy the novelty objective by being renamed.

The [original sources and completed L01–L15 research](https://github.com/louisgiles/KQL/blob/32c14a53b579fbd4e4705071277fa55699c22621/threat-work/research/resprox-research-loops.md) remain preserved at a fixed commit. Read relevant findings selectively. C11 and other old candidates have no preferred position. Reopening a rejected claim requires a changed premise or new evidence.

## Task list and state

| Task | Work | Required result | Status |
|---|---|---|---|
| R1 | Explore different mechanisms | Up to two grounded questions with observable consequences | Not started |
| R2 | Challenge the finalists | One candidate with a fair baseline and decisive test, or stop | Not started |
| R3 | Build a small validation package | One concrete hunt design and comparison, or a precise blocker | Not started |

**Next eligible task:** R1, once instructed. **Active candidates:** none.  
**Consecutive checkpoints without progress:** 0/2. **R1 returns used:** 0/1.

Use R-prefixed candidate IDs. Track readiness separately from task completion. Allowed task states: not started, in progress, complete, blocked, stopped. Investigating a stage can finish with a failed gate; that does not authorize progression.

## R1 — Explore before selecting

1. Fix the analyst decision in one sentence. Start with managed endpoints; any identity or local-exposure branch must explain its separate decision.
2. Read the original observations and consequential primary evidence. Check what the growth premise measures without producing another market overview.
3. Explore three different causal mechanisms where evidence permits. Consider ownership, protocol behaviour, lifecycle, resource use and changes of purpose before translating ideas into tables. These are prompts, not candidate quotas. Variations of rarity/history/destination counts count as one family.
4. For each serious mechanism, give its predicted observation, strongest contradiction, closest simpler approach and possible added decision value. Allow one explicit additional-telemetry idea; do not invent ingestion to make it practical.
5. Map required source/table, fields and event semantics. Mark availability as documented only, sample-observed, or verified in the intended workspace. Missing tenant samples do not prevent exploration. Preserve the non-Edge `DeviceEvents.AdditionalFields` route without inventing JSON keys.
6. Compare against relevant archived failures, then select zero, one or two candidates.

**Gate:** Each selection has primary evidence, an explained mechanism, plausible collection, a simpler comparator and a named uncertainty a bounded test can resolve. Analogy alone fails. If none qualifies, stop.

**Output:** One comparison table and selection rationale, at most 500 words including source notes.

## R2 — Test the weakest link

Complete and challenge this chain for each finalist:

**Source observation → mechanism → recorded telemetry → hunt logic → analyst decision.**

Mark links as evidence, inference or unknown. Verify consequential schema claims with official documentation. Check scope, event times, joins and missing-data paths before scoring. Documented fields do not establish populated events.

Inspect the closest primary implementation or research method. State the exact difference and classify it as established technique, adaptation, or potentially distinct within the inspected sources. A feature missing from one implementation does not establish global novelty.

Use an independent reviewer to choose realistic benign and missingness controls before seeing tuned thresholds or expected rankings. Prefer primary traces or implementation behaviour where available. Model critique is reasoning assistance, not human adjudication or empirical evidence.

Freeze the investigation unit before comparison: one meaningful device/application episode or token case, with evidence rows inside it. Use comparable population, windows, coverage, case budget and method-independent ordering; expose exclusions and displaced cases.

Predeclare retain/narrow/reject outcomes. A benign twin limits attribution without automatically defeating hunt utility. Utility requires changed decisions or reduced review effort. Synthetic tests can falsify logic; designer-assigned labels cannot establish precision, prevalence or field value.

**Gate:** Select at most one candidate with a credible evidence chain and a test capable of changing the decision. A feasible future tenant test may proceed to R3 as a design. If no credible collection path exists, park the candidate and name the reopening condition.

**Output:** At most 500 words: objection, evidence/test result, decision, remaining uncertainty and next experiment.

## R3 — Deliver one validation package

Provide one candidate and its simplest baseline:

- Behaviour, mechanism, required/optional telemetry, exact fields, windows, entity keys, filters and joins.
- Concrete schema-grounded pseudocode, or an existing query link and precise corrections needed. Label unexecuted logic; use bounded `materialize()` for reused expressions where appropriate.
- Case-level output and witness events, coverage state, benign explanations, what a hit establishes and the analyst's first three pivots.
- Minimal reproducible controls, including exact inputs/code for any executed test.
- Validation protocol covering coverage/runtime, independent labels, case selection, decisions, analyst minutes, exclusions, displaced cases and acceptance/rejection/inconclusive outcomes.

Reuse existing modules where appropriate. Executable promotion follows the [repository contract](../../repo-contract.md) as separate reviewed work; this task does not silently expand its write scope.

Distinguish designed, logic-checked, sensor-observed and field-evaluated evidence. Parser success and assertion totals do not establish detection performance.

**Completion:** A validation-ready package requires a complete input contract and comparison. Otherwise deliver the precise blocked state. Neither outcome establishes efficacy.

**Output:** At most 500 explanatory words plus necessary readable pseudocode/test material. Aim for 150 code lines; justify essential excess instead of hiding complexity. Stop after delivery.

## Progress and stop rules

- A checkpoint must add an observation, derivation, feasibility finding or experiment that changes a claim, selection or next test. More citations, caveats, names or assertions do not qualify.
- Before an attempt, name the uncertainty, evidence sought and result that changes course. Two unsuccessful attempts to repair one mechanism park it; cosmetic edits do not reset the count.
- Two consecutive checkpoints without material progress stop the restart. If R2 rejects all finalists, permit one bounded return to R1 for a different mechanism. No further extension.
- Missing access limits validation; an impossible collection path blocks the mechanism's implementation. Do not confuse either with evidence of benign activity.
- Record negative results once. Repairs to earlier mistakes are corrections, not discoveries. No breakthrough labels from analogy, citation gaps or favourable synthetic fixtures.

## Output and saving

Keep one current result: decision, strongest idea, new evidence, objection, readiness and next test. Replace it as work advances; Git history preserves earlier versions. Research broadly, but retain at most eight decision-relevant source entries with precise claims, dates and links. Do not build parallel registers or another direction-review journal.

Chat updates: at most 100 words. Active file: under 2,500 prose words including current results. Necessary code and compact evidence rows are separate; no oversized appendices to evade the limit.

Fetch latest main and the current blob SHA before writing. Preserve concurrent changes and never duplicate a completed R task. Save state/result together and verify before claiming completion. This plan supersedes the historical 15-pass and timed-review instructions.

**Controlling rule:** If output grows faster than evidence, stop. State the missing observation, what it would settle and whether it is obtainable.

## Current result

No R-stage research has run. This is the task-list redraft only.
