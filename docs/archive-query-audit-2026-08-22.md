# Archived investigation query audit

Date: 2026-08-22

## Scope and guardrail

This audit covers the complete top-level `archive/` tree on
`louisgiles/KQL@b97b1a448be23390e56ae942ee3f368412c34860`:

- 46 archived blobs in total;
- 34 query or source artifacts, including extensionless prototypes;
- 12 Markdown files that document the former query-family contracts.

The review is static. Speed classifications describe execution risk inferred
from time range, table fan-out, joins, unions, materialization, aggregation,
and output shape. They are not tenant runtime measurements.

Nothing in this audit approves an archived query for activation. The new
investigation base must be built from scratch. The artifacts below are useful
only as evidence about requirements, successful patterns, and failure modes.

## Executive decision

The archive contains strong investigation ideas but no query that should be
reactivated unchanged. Its best ideas are:

1. require a precise starting entity and a bounded event anchor;
2. show prevalence, nearby behavior, and cross-domain evidence before a
   narrative verdict;
3. normalize heterogeneous evidence into compact, predictable rows;
4. distinguish threat concern from exposure or blast-radius concern;
5. retain explicit no-data, ambiguous-input, unsafe-coverage, and truncation
   states instead of treating absence as benign;
6. use stable endpoint process keys and immutable ingestion cutoffs where
   replay correctness matters.

The dominant failure mode is that the former "quick" and narrative layers
often repeat most of the deep-dive computation. Several quick-dives are too
large for a first-120-seconds path, and several narrative generators create a
second implementation of the same decision logic. The fresh base should have
one evidence computation path with small views over its output, not three
independently maintained variants.

## Rating method

- **Speed risk: low** means a narrow, bounded query with little fan-out.
- **Speed risk: medium** means multiple bounded joins or tables, but a
  reasonably compact plan.
- **Speed risk: high** means a long baseline, wide table fan-out, many joins or
  materializations, or a large multi-section output.
- **Signal density: high** means most returned fields directly support a
  containment, escalation, or closure decision.
- **Signal density: medium** means useful evidence is mixed with substantial
  context or prose preparation.
- **Signal density: low** means diagnostic or raw telemetry dominates.

## Inventory

Paths beginning with `investigation/` below are relative to `archive/` after
the launcher restructure. The Babbler, probe, and rare Office operations
lineage paths remain relative to
`archive/investigation-legacy-2026-08-21/`. Operator counts are static counts
in the archived source.

| Artifact | Lines | Primary table coverage | materialize / join / union | Speed risk | Signal density | Decision use and disposition |
| --- | ---: | --- | ---: | --- | --- | --- |
| `01-sign-in/Babbl33r.kql` | 1,007 | `SigninLogs` | 10 / 0 / 4 | High | High | Replay-safe, fail-open Stage 20 contract is a useful requirement. Runtime source is migrating to `oneshots`; do not use in the investigation base. |
| `01-sign-in/Babbl3r` | 772 | `SigninLogs` | 8 / 0 / 1 | High | High | Historical scoring workbench. Superseded and strongly duplicated within the Babbler lineage. |
| `01-sign-in/Babbler` | 238 | `SigninLogs` | 3 / 0 / 1 | High | Medium | Early 90-day novelty model. Useful only as lineage for baseline-health lessons. |
| `01-sign-in/Babbler 2` | 498 | `SigninLogs` | 8 / 0 / 1 | High | High | Intermediate model with health diagnostics. Superseded lineage only. |
| `01-sign-in/b32` | 961 | `SigninLogs` | 16 / 0 / 5 | High | High | Former one-shot section. Superseded by Stage 20 v0.2.0 and migrating to `oneshots`. |
| `01-sign-in/babbler 031 (workbench)` | 836 | `SigninLogs` | 8 / 0 / 3 | High | High | Research cockpit, not an incident fast path. Near-duplicate of `Babbl3r`. |
| `01-sign-in/temp2` | 11 | `SigninLogs` | 0 / 0 / 0 | High | Low | Unbounded ingestion-delay probe. Diagnostic scratch only; unsafe as a reusable query. |
| `01-sign-in/temp3` | 16 | `SigninLogs` | 0 / 0 / 0 | Low | Low | Hard-coded two-minute request-ID probe. A reproducibility example, not reusable logic. |
| `01-sign-in/tenp4` | 19 | `SigninLogs` | 0 / 0 / 0 | High | Low | Unbounded flow-collapse delay probe. Diagnostic scratch only. |
| `03-office-ops/rare-office-ops-one-shot.kql` | 518 | `OfficeActivity` | 2 / 5 / 0 | High | High | Tenant-wide two-window rarity hunt. Keep separate from alert-driven investigation and from agentic one-shots. |
| `investigation/cloud/azure-activity/quick-dive.kql` | 216 | `AzureActivity`, `SigninLogs` | 1 / 6 / 0 | Medium | High | Good decision-gate questions, but six joins are too much for a universal first query. Reuse the questions, not the implementation. |
| `investigation/cloud/azure-activity/deep-dive.kql` | 548 | `AzureActivity`, `SigninLogs` | 5 / 14 / 0 | High | Medium | Rich actor, resource, and prevalence context. Split into requested pivots in the fresh base. |
| `investigation/cloud/azure-activity/narrative-gen.kql` | 613 | `AzureActivity`, `SigninLogs`, `AuditLogs` | 7 / 9 / 0 | High | Medium | Useful ticket fields, but repeats analysis to render prose. Narrative should consume evidence output instead. |
| `investigation/endpoint/file/quick-dive.kql` | 466 | Five Defender tables plus `AlertEvidence` | 6 / 8 / 1 | High | High | Prevalence-first intent is good; the implementation is not a fast path. |
| `investigation/endpoint/file/deep-dive.kql` | 450 | Five Defender endpoint tables | 2 / 1 / 2 | High | Medium | Twelve togglable sections are comprehensive but too bundled. Preserve file-origin, execution, and process-key requirements as separate pivots. |
| `investigation/endpoint/file/narrative-gen.kql` | 491 | Five Defender endpoint tables | 13 / 0 / 2 | High | Medium | Operation-aware lifecycle language is useful. Recomputing thirteen materialized datasets for prose is not. |
| `investigation/endpoint/network/quick-dive.kql` | 311 | Four Defender endpoint tables | 2 / 3 / 0 | Medium | High | Best of the endpoint quick patterns: cautious intent language plus destination and process prevalence. Still needs a smaller first step. |
| `investigation/endpoint/network/deep-dive.kql` | 664 | Five Defender endpoint tables | 11 / 9 / 2 | High | Medium | Strong evidence coverage, but seven sections and wide reuse create a heavy plan. |
| `investigation/endpoint/network/narrative-gen.kql` | 367 | Four Defender endpoint tables | 9 / 3 / 0 | High | Medium | Cautious determination language is good. It is highly similar to the quick-dive and should not remain a second compute path. |
| `investigation/endpoint/process/quick-dive.kql` | 566 | Five Defender tables plus `AlertEvidence` | 14 / 5 / 1 | High | High | Good process identity and prevalence questions, but clearly outside a first-120-seconds budget. |
| `investigation/endpoint/process/deep-dive.kql` | 343 | Four Defender endpoint tables | 2 / 2 / 2 | Medium | High | Stable process-chain pivots are valuable. Keep parent, target, child, file, and network stages independently runnable. |
| `investigation/endpoint/process/narrative-gen.kql` | 444 | Five Defender endpoint tables | 8 / 4 / 2 | High | Medium | Useful chain-shaped note model, but narrative generation should not rescan telemetry. |
| `investigation/identity/app-credential-added.kql` | 252 | `AuditLogs` | 1 / 6 / 0 | Medium | High | Focused, decision-relevant audit-event triage. Use its actor, target, credential, and prevalence questions as requirements. |
| `investigation/identity/auth-changes/deep-dive.kql` | 334 | `AuditLogs`, `SigninLogs`, `IdentityInfo` | 5 / 8 / 0 | Medium | High | Strong actor-versus-target and privilege framing. Weighted verdict should remain explainable evidence, not an opaque closure decision. |
| `investigation/identity/auth-changes/narrative-gen.kql` | 339 | `AuditLogs`, `SigninLogs`, `IdentityInfo` | 3 / 4 / 0 | Medium | Medium | Good closure fields, but duplicates the deep-dive decision path. |
| `investigation/identity/mass-account-deletion.kql` | 49 | `DeviceEvents`, `SecurityEvent`, `IdentityDirectoryEvents`, `IdentityInfo` | 0 / 1 / 1 | Low | High | Compact actor-anchored cross-source pattern. It lacks a complete reusable input and output contract, so retain only the pattern. |
| `investigation/identity/sign-in/deep-dive.kql` | 205 | `SigninLogs`, non-interactive sign-ins, `AuditLogs`, `IdentityInfo` | 2 / 8 / 1 | Medium | High | Compact compared with later families. Useful entity flexibility, but nine weighted signals should be exposed individually. |
| `investigation/identity/sign-in/narrative-gen.kql` | 195 | `SigninLogs`, `AuditLogs`, `IdentityInfo` | 2 / 5 / 0 | Medium | Medium | Smallest narrative generator, but still repeats sign-in analysis instead of formatting shared evidence. |
| `investigation/m365/email/quick-dive.kql` | 664 | Six Defender email tables | 7 / 10 / 6 | High | High | Threat-versus-exposure separation is excellent. The query is not quick and should be decomposed. |
| `investigation/m365/email/deep-dive.kql` | 1,235 | Six email tables plus three endpoint tables | 29 / 16 / 11 | High | Medium | Widest and heaviest archived investigation query. Eleven sections should become explicit on-demand pivots. |
| `investigation/m365/email/narrative-gen.kql` | 710 | Six Defender email tables | 4 / 10 / 6 | High | Medium | Useful campaign, delivery, remediation, and click summary. It duplicates the quick-dive substantially. |
| `investigation/m365/office-operations/deep-dive.kql` | 462 | `OfficeActivity`, `SigninLogs`, `AuditLogs`, `IdentityInfo` | 10 / 13 / 0 | High | High | Strong actor, target, delegee, auth-change, and prevalence model. Too much work for one default query. |
| `investigation/m365/office-operations/narrative-gen.kql` | 408 | `OfficeActivity`, `SigninLogs`, `AuditLogs`, `IdentityInfo` | 7 / 9 / 0 | High | Medium | Good operation translation and determination fields, but repeats the evidence path. |
| `investigation/pivots/ip-prevalence-sweep.kql` | 119 | Eight activity tables plus optional threat intelligence | 0 / 0 / 3 | High | High | Excellent normalized cross-domain pivot shape. A 90-day scan across up to nine sources must be opt-in, source-selective, and outside the immediate path. |

## Table coverage

The archive spans the major identity, Microsoft 365, Azure control-plane,
Defender endpoint, email, Windows security, directory, alert-evidence, and
threat-intelligence sources. That breadth is valuable as a coverage checklist,
but broad table coverage is not itself an investigation plan.

The fresh base should organize execution around the starting entity and
decision, then call only the relevant sources:

| Starting entity | Minimum early evidence | On-demand expansion |
| --- | --- | --- |
| User or session | interactive and non-interactive auth, risk/MFA/device context, source IP | auth changes, Office actions, Azure actions, related users |
| IP | current incident-window identity and device touches | longer prevalence, email infrastructure, threat intelligence |
| Device or process | exact process identity, ancestry, signer/hash/prevalence, immediate network/file actions | descendants, registry/persistence, related devices/users |
| Message, URL, or file | delivery/authentication, click or execution exposure, recipients/devices affected | campaign spread, post-delivery actions, endpoint correlation |
| Cloud resource or operation | actor, operation, scope, result, source IP, nearby changes | actor baseline, role/credential changes, related resources |

## Duplication and lineage

All 34 source blobs have distinct Git blob SHAs, so there are no byte-identical
duplicates. There is still substantial semantic and textual duplication.

A normalized five-token-shingle comparison found these strongest overlaps:

| Pair | Similarity | Interpretation |
| --- | ---: | --- |
| `Babbl3r` and `babbler 031 (workbench)` | 0.900 | Direct Babbler lineage; the workbench is a close successor. |
| endpoint network narrative and quick | 0.567 | Two outputs maintain much of the same evidence computation. |
| `Babbl3r` and `b32` | 0.493 | Babbler scoring lineage adapted to the one-shot section contract. |
| `b32` and `babbler 031 (workbench)` | 0.484 | Shared scoring engine with different presentation contracts. |
| email narrative and quick | 0.375 | Significant duplicated message, URL, attachment, and exposure logic. |
| office-operations deep and narrative | 0.269 | Shared actor, operation, sign-in, and identity context. |

The comparison is a structural indicator, not a semantic equivalence proof.
Shared comments and common KQL scaffolding can increase the score. The result
still confirms two important design decisions:

1. Babbler variants belong to one historical lineage in `oneshots`, not to the
   fresh investigation base.
2. Evidence calculation and presentation must be separated so quick, deep,
   and narrative outputs do not drift into parallel implementations.

## Lessons to carry into the fresh base

### Keep as requirements

- Every entry point requires a typed entity, an incident time, and a bounded
  lookback. Empty placeholder inputs must return an explicit status row.
- Use an immutable assessment cutoff when ingestion timing affects replay.
- Pre-filter and pre-project both sides before a join. Materialize only a
  dataset that is actually reused.
- Use stable keys for process and authentication flow correlation. A fallback
  key must be labelled as lower confidence.
- Return exact timestamps, affected entities, decisive evidence, containment
  implication, and unresolved questions.
- Bound samples and emit a truncation indicator rather than silently dropping
  rows or returning an unlimited raw dump.
- Treat optional tables as declared capability states. Missing telemetry is
  neither a successful query nor benign evidence.
- Keep prevalence distinct from maliciousness and keep threat concern distinct
  from exposure or blast radius.

### Do not repeat

- Do not put 90-day baselines or wide cross-table sweeps in the default first
  query.
- Do not call a 400-to-700-line multi-table plan a quick-dive.
- Do not require analysts to enable or disable a dozen sections inside one
  large query.
- Do not rescan source tables solely to generate prose.
- Do not collapse weighted heuristics into an unexplained benign or malicious
  verdict.
- Do not mix population-wide hunts, incident investigation, detection logic,
  scratch diagnostics, or one-shot pipeline stages in one active surface.
- Do not copy archived source into the new base. Reimplement the selected
  contracts with fresh, smaller queries and independent validation.

## First-120-seconds design target

The archive suggests a compact sequence for the separately queued new base:

1. **Validate context:** entity, anchor, cutoff, incident window, and available
   tables. Return status immediately if unsafe or ambiguous.
2. **Confirm the primary event:** one narrow source query with a small,
   deterministic output.
3. **Measure immediate exposure:** users, devices, sessions, messages, or
   resources touched inside the incident window.
4. **Find one decisive adjacent pivot:** authentication to cloud action,
   process to file/network, or message to click/execution.
5. **Choose containment or expansion:** output the next action and unresolved
   question rather than automatically running every baseline and narrative
   section.

Long prevalence windows, campaign expansion, process-chain depth, tenant
rarity, and narrative rendering should be explicit follow-on steps.

## Promotion gates for future queries

A new investigation query should not be promoted merely because an archived
counterpart exists. Promotion should require:

1. fresh implementation under the new contract;
2. documented inputs, time boundaries, required and optional tables, and output
   schema;
3. compile validation plus representative empty, missing-table, ambiguous,
   truncated, benign, and malicious cases;
4. measured tenant runtime for the intended window, including repeated-run
   evidence where p95 is claimed;
5. proof that the first-120-seconds path remains independently runnable;
6. confirmation that the output identifies affected entities, decisive
   evidence, containment action, and unresolved questions.

## Final disposition

- **Reference only:** all archived investigation-family queries and docs.
- **Owned by the separate migration:** the six Babbler lineage artifacts and
  their Stage 20 contract.
- **Hunt, not investigation:** `rare-office-ops-one-shot.kql`.
- **Diagnostic scratch only:** `temp2`, `temp3`, and `tenp4`.
- **No reactivation exceptions proposed:** the new reusable investigation base
  should proceed from a blank slate using the requirements above.
