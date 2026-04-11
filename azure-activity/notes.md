# azure-activity (≈ 04-azure-activity)

Azure resource-plane investigation family. Scope: resource creation and
deletion, role assignments on subscriptions and resource groups, Key
Vault access, storage account changes, and network rule modifications.

## Use case

An analyst arrives with an Azure signal: a new role assignment at
subscription scope, a Key Vault secret read from an unexpected actor,
a storage account made public, a network security group rule added.
This family surfaces the action, identifies the actor, and places the
event on a timeline against that actor's sign-in and auth history.

## Starting entities

- Subscription id
- Resource id
- Actor UPN or service principal object id
- Caller IP

## Queries in this family

| File | Role | Notes |
|---|---|---|
| `azure-activity-deep-dive.kql` | deep-dive (analysis) | **Stub — empty.** See compliance notes below. |

No `narrative-gen.kql` yet.

## Data dependencies

Planned once the deep dive is authored:

| Table | Tag |
|---|---|
| `AzureActivity` | **Required** |
| `AzureDiagnostics` | **Optional enrichment** — Key Vault, NSG flow, etc. |
| `SigninLogs` / `AADServicePrincipalSignInLogs` | **Optional enrichment** — correlate actor to auth context. |

## Done criteria

Triage is finished when:

1. Every non-routine control-plane operation has an identified actor
   and a business justification (ticket, PIM activation, change record).
2. Role assignments at subscription or resource group scope have been
   reviewed for principal type and scope appropriateness.
3. Any public exposure change (storage, NSG, firewall) has been walked
   through with the resource owner.
4. The event has been mapped to one of the four closure buckets.

## Closure language

- **Benign** — expected IaC deployment, identified pipeline service
  principal, change record matches.
- **Precautionary benign** — manual console change by a known admin
  outside change window but with a ticket.
- **Review required** — role assignment at subscription scope to a
  principal whose purpose isn't obvious, or a public-exposure change
  without an attached change record.
- **Suspicious / escalate** — Owner/Contributor granted to a newly
  created service principal; Key Vault secret read from a new IP;
  storage account made anonymously readable without change record.

## Validation — test cases

1. **Known benign.** IaC pipeline service principal deploys a new
   resource group and assigns RBAC scoped to it.
2. **Ambiguous.** Console-driven NSG rule change by an on-call engineer
   outside the normal change window.
3. **Known bad / clearly suspicious.** Newly-created SP granted Owner
   at subscription scope, followed by Key Vault secret reads.

## Contract compliance notes

- `azure-activity-deep-dive.kql` is an empty 1-byte placeholder. It
  should be authored to the contract or flagged for deletion.
- No `narrative-gen.kql` exists — author or flag.
