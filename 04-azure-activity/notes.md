# 04-azure-activity

Azure resource-plane investigation family. Scope: resource creation
and deletion, role assignments on subscriptions and resource groups,
Key Vault access, storage account changes, and network rule
modifications.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | TODO — empty stub. |
| `narrative-gen.kql` | narrative | TODO — not yet authored. |

## Starting entities

- TODO (likely: subscription id, resource id, actor UPN / service
  principal object id, caller IP).

## Required tables

- TODO (likely: `AzureActivity`).

## Optional tables

- TODO (likely: `AzureDiagnostics` — **optional enrichment** for Key
  Vault, NSG flow, and resource-specific logs; `SigninLogs` /
  `AADServicePrincipalSignInLogs` — **optional enrichment** to tie
  the actor to auth context).

## Done criteria

- TODO. Every non-routine control-plane operation has an identified
  actor and a business justification (ticket, PIM activation, change
  record); public-exposure changes walked through with the resource
  owner.

## Validation — test cases

1. **Known benign — TODO.** IaC pipeline service principal deploys a
   new resource group and assigns scoped RBAC.
2. **Ambiguous — TODO.** Console NSG rule change by an on-call
   engineer outside the normal change window.
3. **Known bad / clearly suspicious — TODO.** Newly-created service
   principal granted Owner at subscription scope, followed by Key
   Vault secret reads.
