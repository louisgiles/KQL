# Archived investigation launcher

This is the direct entry point to the investigation workbenches preserved by
the 2026-08-21 blank-slate reset. The investigation tree now sits directly at
[`archive/investigation/`](investigation/) instead of being buried inside the
dated source snapshot.

The restructure moved the query sources without changing their KQL. Making a
query accessible does not promote it or prove that it runs in Microsoft
Sentinel Log Analytics. Read the runtime status before copying a query.

## Query launcher

Use a quick dive as the first decision gate when one exists, use the deep dive
for the evidence-led investigation, then use the narrative generator only
after the evidence supports a determination.

| Family | Quick dive | Deep dive | Narrative | Current Sentinel Logs status |
| --- | --- | --- | --- | --- |
| Identity sign-in | Not present | [Open deep dive](investigation/identity/sign-in/deep-dive.kql) | [Open narrative](investigation/identity/sign-in/narrative-gen.kql) | Static candidate, runtime unverified. `IdentityInfo` and `AuditLogs` are compile dependencies in the preserved source. |
| Identity authentication changes | Not present | [Open deep dive](investigation/identity/auth-changes/deep-dive.kql) | [Open narrative](investigation/identity/auth-changes/narrative-gen.kql) | Conditional. Requires `AuditLogs`, `IdentityInfo`, and `SigninLogs` despite the historical optional labels. |
| Endpoint process | [Open quick dive](investigation/endpoint/process/quick-dive.kql) | [Open deep dive](investigation/endpoint/process/deep-dive.kql) | [Open narrative](investigation/endpoint/process/narrative-gen.kql) | Known incompatible with the standard Sentinel table schema until `Timestamp` is ported to `TimeGenerated`. |
| Endpoint file | [Open quick dive](investigation/endpoint/file/quick-dive.kql) | [Open deep dive](investigation/endpoint/file/deep-dive.kql) | [Open narrative](investigation/endpoint/file/narrative-gen.kql) | Known incompatible with the standard Sentinel table schema until `Timestamp` is ported to `TimeGenerated`. |
| Endpoint network | [Open quick dive](investigation/endpoint/network/quick-dive.kql) | [Open deep dive](investigation/endpoint/network/deep-dive.kql) | [Open narrative](investigation/endpoint/network/narrative-gen.kql) | Known incompatible with the standard Sentinel table schema until `Timestamp` is ported to `TimeGenerated`. |
| Microsoft 365 email | [Open quick dive](investigation/m365/email/quick-dive.kql) | [Open deep dive](investigation/m365/email/deep-dive.kql) | [Open narrative](investigation/m365/email/narrative-gen.kql) | Quick dive is conditional on all referenced email tables. Deep dive is known incompatible because its endpoint branches use `Timestamp`. |
| Microsoft 365 Office operations | Not present | [Open deep dive](investigation/m365/office-operations/deep-dive.kql) | [Open narrative](investigation/m365/office-operations/narrative-gen.kql) | Conditional. Requires `OfficeActivity`, `AuditLogs`, `IdentityInfo`, and `SigninLogs`. |
| Azure activity | [Open quick dive](investigation/cloud/azure-activity/quick-dive.kql) | [Open deep dive](investigation/cloud/azure-activity/deep-dive.kql) | [Open narrative](investigation/cloud/azure-activity/narrative-gen.kql) | Quick dive has no immediate static Sentinel schema blocker. Deep dive is conditional on `SigninLogs`. Runtime remains unverified. |

## Focused utilities

| Query | Purpose | Runtime status |
| --- | --- | --- |
| [Application credential added](investigation/identity/app-credential-added.kql) | Audit-focused application credential and persistence review. | Legacy reference, runtime unverified. |
| [Mass account deletion](investigation/identity/mass-account-deletion.kql) | Compact cross-source account-deletion context. | Legacy reference, runtime unverified. |
| [IP prevalence sweep](investigation/pivots/ip-prevalence-sweep.kql) | Wide cross-domain IP prevalence check. | Legacy reference with a high-cost 90-day scan. |

## Static compatibility findings

The 13 archived quick and deep dives were statically audited for the Sentinel
Log Analytics surface:

- 7 have a known standard-Sentinel compile blocker;
- 5 compile only when historically labelled optional tables are present;
- 1, the Azure Activity quick dive, has no immediate schema blocker from its
  declared required table;
- none of the 13 contains the KQL `search` operator.

This is static evidence only. A parser pass cannot prove table presence,
column compatibility, tenant coverage, runtime cost, or correct investigative
output. A query becomes runtime-validated only after its exact source has
compiled and executed in Sentinel with the result recorded.

## Preserved lineage

The dated [`investigation-legacy-2026-08-21/`](investigation-legacy-2026-08-21/)
folder now contains the Babbler, probe, and one-shot lineage that does not
belong in the investigation launcher. The exact pre-reset repository remains
available on branch
[`archive/legacy-2026-08-20`](https://github.com/louisgiles/KQL/tree/archive/legacy-2026-08-20).
