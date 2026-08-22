# Investigation

This is the operational surface for Microsoft Sentinel Log Analytics live
triage.

It is intentionally empty while the replacement queries complete exact-source
actual-workspace validation. The previous generated pivots and device-code modules were
removed because none qualified for live use.

## What active means

A file may enter this directory only when it meets
[`docs/live-investigation-standard.md`](../docs/live-investigation-standard.md):

- it runs in the Sentinel Log Analytics blade;
- it starts from an entity already visible in the incident;
- it answers one investigative question;
- it uses a meaningful bounded window based on `now()` and `ago()`;
- it preserves the full bounded result or makes coverage explicit;
- it has no hidden row cap;
- it uses stable, readable evidence columns;
- its exact committed content has passed repeated zero-repair execution in the
  actual Sentinel Log Analytics workspace and the analyst has approved the grid.

Parser success is not operational validation.

Promotion is also blocked until repository rules require the KQL smoke job and
final-head code-owner approval. CODEOWNERS declarations alone do not enforce
those protections.

## Current validation work

Quarantined identity, audit, and endpoint design samples live under
[`validation/live-triage-pilot/`](../validation/live-triage-pilot/). They are
not approved for live-incident testing or active use. Initial tests must use
completed incidents or controlled cases in the actual workspace.

The top-level archive is historical reference material. It is not a fallback
for live investigation and nothing there is approved for activation without a
new review and exact-source actual-workspace validation.
