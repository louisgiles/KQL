# TASKS

## Operating rule

This file is the work queue for the scheduled GitHub loop.

- Do **not** execute tasks outside the scheduled loop.
- At the start of each scheduled run, read the current repository state and this file before making changes.
- Work the highest-priority unblocked task first.
- Keep changes narrowly scoped; do not modify unrelated files.
- Update this file in the same PR as the work performed.
- Prefer one substantive task per PR unless a task explicitly requires coordinated cross-repo changes.
- If requirements are genuinely ambiguous or unsafe to infer, move the task to **BLOCKED** with the exact question or dependency.
- For cross-repository work, preserve history/content first; do not delete the source copy until the destination copy has been verified.
- Scheduled runs should open a **draft PR** for review rather than merge their own work.

## P0 — Repository reset and architecture

- [ ] **Fully audit the current `louisgiles/KQL` repository.** Inventory every query, research artifact, detection artifact, scratch/workbench file, documentation file, test/helper, and duplicated/obsolete item. Produce a clear disposition for each item: retain, restructure, migrate to `oneshots`, archive, consolidate, or retire.
- [ ] **Archive the existing KQL query base without losing history or useful material.** The goal is a clean active workspace while preserving the old repository content in an obvious archive location/state for reference.
- [ ] **Create a fresh active KQL query base.** The new top-level structure should separate:
  - investigation
  - threat-hunting / research / detection-engineering
  - documentation/supporting material where needed
- [ ] **Consolidate threat hunting, threat research, and detection engineering under one parent area with relevant subfolders.** Remove the current fragmentation between `threathunting`, `threathunting-research`, `detectionlogic`, scratch areas, and similar legacy locations while preserving useful content.
- [ ] **Create a dedicated investigation area.** Organise reusable investigative KQL by investigation objective rather than legacy numbering where practical, with a structure that is fast to navigate during live incidents.

## P0 — Move one-shot / Babbler work out of KQL

- [ ] **Audit all Babbler/Babbl3r/Babbl33r/b32/workbench and one-shot-related material currently in `louisgiles/KQL`.** Identify every relevant file, dependency, validation artifact, helper, and documentation reference.
- [ ] **Move all Babbler and one-shot-related work into `louisgiles/oneshots`.** Preserve the coherent implementation and supporting material there, including anything required for the existing one-shot architecture/contracts.
- [ ] **Verify the migrated material against the current `oneshots` structure/contracts before removing active copies from KQL.** Do not leave divergent duplicate implementations across the two repositories.
- [ ] **Clean KQL references after migration.** Remove or replace stale links/docs/tests that assume Babbler or one-shot code still lives in KQL.

## P0 — Investigation speed / containment playbooks

Target outcome: for common high-severity incident patterns, the analyst should reach the decisive containment evidence in roughly **2 minutes rather than 20**, with the first queries answering the highest-value questions first.

- [ ] **Audit the existing investigative query library for speed, signal density, table coverage, duplication, and decision usefulness.** Identify queries that are too broad, too noisy, too slow, or fail to answer an immediate containment decision.
- [ ] **Build a stronger reusable investigation query base.** Queries should prioritise actor/device/IP/session/process pivots, compact timelines, correlated identity + endpoint + cloud context, and outputs that directly support contain / do-not-contain / escalate decisions.
- [ ] **Create a universal malicious device-code incident playbook.** It should cut directly to: target identity, device-code/authentication evidence, source IP/infrastructure, session/token activity, affected apps/resources, post-auth actions, lateral/privilege impact, other affected users, and the minimum evidence required for immediate containment.
- [ ] **Create a universal AiTM sign-in playbook.** It should cut directly to: suspicious sign-in/session, token/session theft indicators, MFA/authentication context, IP/ASN/geo/device/client/app novelty, session continuation, mailbox/cloud follow-on activity, persistence, other affected identities, and immediate containment scope.
- [ ] **Create a universal malware war-room playbook.** It should cut directly to: device/user, process tree, initiating vector, hashes/signers/prevalence, file activity, network/C2, persistence, credential access/lateral indicators, related devices/users, timeline, and immediate isolation/containment scope.
- [ ] **For each universal playbook, build a minimal 'first 120 seconds' query sequence before deeper optional pivots.** The early sequence should be ordered by containment value rather than by data source.
- [ ] **Standardise playbook outputs.** Where practical, each playbook should end with a concise containment summary: entities affected, decisive malicious/benign evidence, blast radius, containment action, and unresolved questions.

## P1 — One-shot roadmap

- [ ] **Recommend five additional one-shots for `louisgiles/oneshots`.** For each recommendation include:
  - incident/problem class
  - why it is high value / high frequency / high analyst toil
  - required inputs
  - deterministic KQL sections/data sources
  - key gates that must prevent unsafe automated conclusions
  - expected output/decision
  - estimated analyst time saved
- [ ] **Rank the five recommendations by implementation priority** using operational value, data availability, determinism, false-positive risk, and fit with the existing one-shot architecture.

## P1 — Quality gates for the rebuilt query base

- [ ] Define naming conventions and folder contracts for investigation, hunting/research, and detection engineering.
- [ ] Remove or consolidate duplicated queries and workbench variants after preserving anything uniquely valuable.
- [ ] Ensure reusable queries have clear parameters, time windows, expected tables, output schema, and analyst purpose.
- [ ] Prefer compact, decision-oriented outputs over large raw event dumps.
- [ ] Add validation/linting/tests where they materially prevent broken KQL or schema drift.
- [ ] Update repository README/docs to explain the new structure and the fastest path for an analyst during an incident.

## BLOCKED

_None currently._

## DONE

- [x] Initial scheduled-loop backlog captured in `TASKS.md`.
