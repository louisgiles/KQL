# Babbler and one-shot material audit

Date: 2026-08-21

## Scope and method

This audit covers every blob on:

- `louisgiles/KQL@b97b1a448be23390e56ae942ee3f368412c34860` (70 files)
- `louisgiles/oneshots@2b0bc6bccd4885b7397365dd9547d1ac959346ec` (42 files)

The inventory checked file names and contents for the Babbler lineage, `b32`,
workbench variants, Stage 20, `IdentityPostureSection`, one-shot
implementations, input adapters, validation material, runtime plans, and
documentation references. It also inspected every KQL file in the current
`highriskofficeops` run pack so dependencies without Babbler in the file name
were not missed.

## Executive decision

The authoritative Stage 20 implementation is Babbler identity-posture section
0.2.0 from blob `c556f0a8a1d3eaed918726da3f7a9b60deba31ad`, currently archived at:

`archive/investigation-legacy-2026-08-21/01-sign-in/Babbl33r.kql`

The exact implementation from `let IdpTargetUPN` through
`IdentityPostureSection` is already embedded unchanged in
`oneshots/highriskofficeops/poc-run-pack/13_complete_one_shot_draft_v0.1.0.kql`.
The assembly correctly supplies `TargetUPN`, `AnchorTime`, and
`AssessmentCutoffUTC` and omits the standalone output head. The only text
between that exact block and Section 4 is assembly chunk markup.

That embedded copy does not finish the migration:

1. `oneshots` has no standalone, reviewable copy of the canonical Stage 20
   source.
2. Its source manifest and integration documents still name the retired active
   path `louisgiles/KQL/01-sign-in/Babbl33r.kql`.
3. The complete assembly is explicitly a development artifact and exceeded the
   ten-minute interactive query limit.
4. The runtime smoke query deliberately stubs Stage 20, and the validation
   matrix still marks the v0.2.0 tenant tests as required.

The next migration should therefore establish the standalone source and its
lineage inside `oneshots`, update pins and documentation there, and run the
listed tenant validation before any KQL source is removed. It must not create a
second independently edited implementation.

## KQL inventory and disposition

| Artifact | Role | Dependencies and contract | Disposition |
| --- | --- | --- | --- |
| `archive/investigation-legacy-2026-08-21/01-sign-in/Babbler` | Original probabilistic sign-in review | `SigninLogs`; 90-day baseline, 24-hour score window, nine-dimensional Good-Turing novelty | Historical lineage only. Preserve with the migrated Babbler history, not as runtime. |
| `archive/investigation-legacy-2026-08-21/01-sign-in/Babbler 2` | Test build 0.2.0 | `SigninLogs`; adds explicit health and coverage diagnostics | Historical lineage only. |
| `archive/investigation-legacy-2026-08-21/01-sign-in/Babbl3r` | Test build 0.3.0 | `SigninLogs`; applicability-aware coverage and separate raw/disposition-adjusted novelty | Historical lineage only. |
| `archive/investigation-legacy-2026-08-21/01-sign-in/babbler 031 (workbench)` | Hardened workbench 0.3.1 | `SigninLogs`; analyst cockpit outputs and the validated scoring engine | Reference implementation for parity, not Stage 20 runtime. |
| `archive/investigation-legacy-2026-08-21/01-sign-in/b32` | Production one-shot section 0.1.0 | `TargetUPN`, `AnchorTime`, `SigninLogs`; emits union-safe `IdentityPostureSection` | Superseded runtime predecessor. Preserve as lineage because tenant research is pinned to its blob. |
| `archive/investigation-legacy-2026-08-21/01-sign-in/Babbl33r.kql` | Hardened Stage 20 section 0.2.0 | `TargetUPN`, `AnchorTime`, immutable `AssessmentCutoffUTC`, `SigninLogs`; fail-open status; bounded union-safe findings | Canonical migration source. Move an exact standalone copy into `oneshots`; do not rewrite during the move. |
| `threathunting/babbler_hunt_research_v0_1_0_rc2.kql` | Tenant-wide manual research workbench | `SigninLogs`; frozen to `b32` blob `fa52de065f4335ef8c1b99b28e1ab1afe92e5269`; per-actor novelty, not compromise probability | Babbler-derived research. Move to a clearly labelled research area in `oneshots`; do not treat it as Stage 20 or a deployable detection. |
| `archive/investigation-legacy-2026-08-21/03-office-ops/rare-office-ops-one-shot.kql` | “Curio Cabinet” workspace hunt | `OfficeActivity` only; no alert or entity input; two-window rarity analysis | Exclude from the agentic one-shot migration. “One-shot” here means a standalone analyst hunt. Keep it archived until the later archive audit decides its hunt disposition. |

All Babbler scoring logic is self-contained in these files. No separate helper
module is required. The important embedded dependencies are the disposition
ledger, stable flow collapse, cutoff-safe `UserId` resolution, baseline
health/coverage checks, bounded findings, and the shared union-safe output
schema.

## Canonical Stage 20 contract

Babbler 0.2.0 is the only candidate that satisfies the current one-shot
point-in-time contract:

- Public inputs: `TargetUPN`, `AnchorTime`, `AssessmentCutoffUTC`.
- Required table: `SigninLogs`.
- Availability boundary: `ingestion_time()`.
- Event boundary: `CreatedDateTime`, falling back to `TimeGenerated`.
- Indexed pruning boundary: `TimeGenerated`.
- Score window: one day before the anchor.
- Baseline window: the preceding 90 days.
- Fail-open conditions include invalid inputs or cutoff, unsafe ingestion
  coverage, unresolved or ambiguous `UserId`, missing stable flow keys,
  incomplete result coverage, no score-window flows, and insufficient
  baseline.
- Output: one status row plus at most 20 findings and an explicit truncation
  sentinel when candidates are omitted.
- Public table:
  `IdentityPostureSection(SectionOrder, FindingOrder, Section, RecordType,
  Priority, EventTime, Entity, FindingKey, Title, Note, Evidence)`.

Do not promote `b32` 0.1.0 as the migration source. It lacks the explicit
assessment cutoff and hardened replay-safety contract added in 0.2.0.

## Current oneshots implementation

The `highriskofficeops/poc-run-pack` is a coherent development and validation
pack for an alert-driven Rare Office Operations one-shot.

### Upstream inputs and gates

- `02_section1_context_adapter_v0.2.1.kql` produces
  `OfficeOperationEvents` and `OfficeOperationContextSection` from
  `OfficeActivity` and `SecurityAlert`.
- `04_identity_alert_gate_draft_v0.1.0.kql` uses `SigninLogs`,
  `OfficeActivity`, and `SecurityAlert` for deterministic identity evidence.
- `04_babbler_input_adapter_test_v0.1.0.kql` converts exactly one ready Office
  event into the scalar actor, anchor, and cutoff expected by Babbler. Zero,
  multiple, or incomplete events fail open through
  `BabblerInputAdapterSection`.
- The adapter and assembly set `AssessmentCutoffUTC` from the one-shot alert
  cutoff. The Office operation event time remains Babbler's anchor.

### Stage 20 and downstream consumers

- `13_complete_one_shot_draft_v0.1.0.kql` contains the exact canonical v0.2.0
  Stage 20 core and records source blob
  `c556f0a8a1d3eaed918726da3f7a9b60deba31ad`.
- `08_foundry_evidence_envelope_v0.1.0.kql` consumes
  `BabblerInputAdapterSection` and `IdentityPostureSection`. Eligibility
  requires Babbler's `Evidence.section_state` to be `ready`; baseline
  readiness alone is not sufficient.
- `05_actor_operation_frequency_v0.1.0.kql`,
  `06_tenant_operation_frequency_v0.1.0.kql`, and
  `07_target_impact_v0.1.0.kql` are sibling evidence sections, not Babbler
  helpers.
- `10-ASSEMBLY-SKELETON.kql` documents the intended union order and currently
  contains a placeholder for the exact Babbler block.

### Runtime state

- The combined development assembly uses `SigninLogs`, `OfficeActivity`,
  and `SecurityAlert`, but the repository records that it exceeded the
  ten-minute interactive execution limit.
- `14_runtime_smoke_v0.1.0.kql` validates the contract and deterministic run
  state while explicitly returning “Babbler identity posture not evaluated in
  runtime smoke mode”.
- `14_stage2_identity_gate_runtime_v0.1.0.kql` validates the deterministic
  identity gate without Babbler, frequency, impact, or Foundry.
- `14-STAGED-RUNTIME-PLAN.md` requires Babbler to run separately with the
  explicit actor, anchor, and cutoff until the staged runner is complete.

There is therefore source-level parity but no complete runtime parity result.

## Validation assets and outstanding gates

The following assets must travel with and continue to govern the implementation:

- `00-SOURCE-MANIFEST.md`: blob pins and source lineage.
- `00-SHARED-CONTRACT.md`: immutable cutoff, event anchor, union schema, and
  deterministic gate rules.
- `00-VALIDATION-MATRIX.md`: replay, flow collapse, empty score-window,
  ambiguous `UserId`, truncation, AitM, and device-code cases.
- `SECTION3-BABBLER-INTEGRATION.md`: exact vendoring procedure, scalar adapter
  behavior, and promotion gates.
- `12-POC-DONE-CRITERIA.md`: compile, performance, output, fail-open, and
  evidence eligibility criteria.
- `13-HEAD-OF-CYBER-POC-BRIEF.md`: prior scoring-parity claim and the remaining
  complete-assembly work.
- `14-RUNTIME-SMOKE-VALIDATION.md` and
  `14-STAGED-RUNTIME-PLAN.md`: the boundary between smoke coverage and a
  complete runtime pass.
- `04_babbler_input_adapter_test_v0.1.0.kql`: executable adapter lock.

Outstanding v0.2.0 tenant gates are concrete:

1. Compile the standalone section in the target workspace.
2. Prove frozen-cutoff replay by excluding rows ingested after the cutoff and
   post-anchor identity mappings.
3. Prove MFA sequence collapse and fail-open behavior when stable keys are
   unavailable.
4. Exercise empty score-window, zero/multiple `UserId`, missing ingestion
   coverage, and internal truncation.
5. Re-run known AitM positive and device-code cases under the pinned 0.2.0
   semantics.
6. Meet the recorded performance target: no more than 100 seconds and p95 no
   more than 60 seconds on the replay sample.
7. Verify the Foundry envelope remains ineligible for every non-ready or
   truncated Stage 20 state.

## Documentation reference audit

KQL references are present in the root `README.md`, `archive/README.md`,
archived investigation READMEs, `repo-contract.md`, and the `threat-work`
READMEs. They correctly state that active Babbler and agentic one-shot work
belongs in `louisgiles/oneshots`, and that source must remain recoverable until
the destination is verified.

The current `oneshots` source manifest, GitHub placement guide, run order,
assembly skeleton, and Section 3 integration guide still point to
`louisgiles/KQL/01-sign-in/Babbl33r.kql`. That path no longer exists on KQL
main after the blank-slate reset. The pinned blob remains valid and recoverable
under `archive/investigation-legacy-2026-08-21/01-sign-in/Babbl33r.kql`, but
the active documentation is stale.

`NOTES-4-7.md` also refers to “production b32”. That is historical wording and
must be updated to the 0.2.0 standalone source when the migration lands.

## Migration plan for the next P0

1. Copy the exact `Babbl33r.kql` blob into a stable standalone path in
   `oneshots`, for example
   `highriskofficeops/poc-run-pack/section3_babbler_identity_posture_v0.2.0.kql`.
2. Copy the five predecessor variants into an explicitly historical Babbler
   lineage folder in `oneshots`; preserve their bytes and record each source
   blob.
3. Move the tenant research workbench into an explicitly non-runtime research
   folder in `oneshots`, retaining its `b32` pin and interpretation warnings.
4. Update the source manifest, placement guide, run order, assembly skeleton,
   integration guide, and `NOTES-4-7.md` so the standalone `oneshots` file is
   the only active source path.
5. Add a mechanical parity check that compares the canonical block with the
   vendored Stage 20 block in the combined assembly, excluding only the three
   standalone parameter defaults and final output head.
6. Run the outstanding tenant validation matrix. Record exact query/runtime
   evidence rather than relying on the earlier workbench parity claim.
7. Only after destination content and validation are verified, remove the
   migrated active KQL research copy and clean stale KQL references in the
   separately queued cleanup task. Do not delete the archived source first.

## Non-goals for the migration

- Do not redesign the scoring model while moving it.
- Do not promote the 0.3.1 workbench, `b32`, or tenant research query as the
  Stage 20 runtime.
- Do not move the Curio Cabinet hunt merely because its title contains
  “one-shot”.
- Do not describe runtime smoke or source-level parity as a complete one-shot
  runtime pass.
- Do not maintain independently editable copies of Stage 20 in both
  repositories.
