# 04-azure-activity

Azure control-plane investigation family. Scope: subscription and
resource-group changes, resource creation and deletion, role
assignments at management-group / subscription / resource-group
scope, Key Vault access policy changes, network security group rule
edits, storage and networking changes — anything that lands in
`AzureActivity`.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `quick-dive.kql` | quick-triage | Fast behavioural-context decision gate. Answers: what happened, is it normal for the actor, is it normal for the tenant, what is weird, does this require the deep-dive. |
| `deep-dive.kql` | analysis | Toggled evidence engine — core alert scope, operation classification, behavioural baselines (actor history per operation / IP / subscription / resource type), related activity in correlation window, risk-signal aggregation, and actor sign-in context near `AlertTime`. |
| `narrative-gen.kql` | narrative | Dash-prefixed paste-ready ticket note covering actor identity classification (user / service principal / managed identity), prevalence for actor and tenant, related activity, sign-in context, recent SP credential / role changes, and a determination line. |

## Purpose

Triage a Sentinel Azure-Activity alert end to end. The alert provides
`AlertTime`, `Caller`, `CallerIpAddress`, `OperationName`,
`ResourceId`, and `SubscriptionId`. Benignity here is
prevalence-based: most control-plane operations are normal for the
actor and the tenant — the suspicious ones are the rare,
unfamiliar, or chained ones.

## Starting entities

- **`AlertTime`** — datetime from the alert. Centre of the
  `EventWindow` scope.
- **`Caller`** (`CallerToCheck`) — UPN, service principal display
  name, or app id. Filtered via `contains`.
- **`CallerIpAddress`** (`CallerIpToCheck`) — source IP from the
  alert. Filtered via `contains`.
- **`OperationName`** (`OperationToCheck`) — operation from the
  alert. Matches `OperationNameValue` or `OperationName`. Leave empty
  for all operations in the window.
- **`ResourceId`** (`ResourceIdToCheck`) — full or partial resource
  id.
- **`SubscriptionId`** (`SubscriptionIdToCheck`) — subscription id.

## Variables

| Variable | Default | Role |
|---|---|---|
| `AlertTime` | `2026-01-01T00:00:00Z` | Centre of the event window. |
| `AlertTitle` | `""` | Free-text alert title — drives `ActivityCategory` classification (`deployment` / `deletion` / `other`). |
| `CallerToCheck` / `CallerIpToCheck` / `OperationToCheck` / `ResourceIdToCheck` / `SubscriptionIdToCheck` | `""` | Scope filters. |
| `EventWindow` | `1h` | Window either side of `AlertTime` for the alert scope and related-activity scan. |
| `BaselineWindow` | `90d` | Historical baseline window. Strictly prior to `AlertTime - EventWindow` so the alert never contributes to its own baseline. |
| `SigninWindow` *(deep-dive)* | `24h` | Actor sign-in context window. |
| `IdentityContextWindow` *(narrative-gen)* | `24h` | Window for SP credential / role changes and user sign-in context. |
| `BaselineLabel` *(narrative-gen, quick-dive)* | `"90d"` | Human label used inside the narrative text. |
| `Run*` toggles *(deep-dive)* | `true` | Toggle each deep-dive section: `RunCoreActivity`, `RunOperationClassification`, `RunBehaviouralBaseline`, `RunRelatedActivity`, `RunRiskSignals`, `RunActorSigninContext`. |

## Required tables

- **`AzureActivity`** — **Required**. Primary source for every
  query. Scoped to `AlertTime ± EventWindow` before any joins.

## Optional tables

- **`SigninLogs`** — **Optional enrichment**. Actor sign-in context
  near `AlertTime` (IP, location, result, risk level, risk detail,
  device trust). Used by deep-dive (`RunActorSigninContext`) and
  narrative-gen (`UserSigninContext`). Left-joined; missing rows
  leave the row with null sign-in posture.
- **`AuditLogs`** — **Optional enrichment**, narrative-gen only.
  Used for service-principal credential changes
  (`SpCredentialChanges`) and SP role changes (`SpRoleChanges`)
  within `IdentityContextWindow` of `AlertTime` — the standard
  "did this Azure activity follow a fresh credential or role grant?"
  check.

## Done criteria

1. Every event in the `AlertTime ± EventWindow` scope has been
   classified against actor history (`ActorOperationBaseline`),
   tenant history (`TenantOperationBaseline`), and related activity
   under the same correlation id.
2. Risk-signal flags (`RunRiskSignals`) have been read and any
   `RARE_*`, `NEW_IP_FOR_ACTOR`, `NEW_OPERATION_FOR_ACTOR`,
   `PERSISTENCE_CHAIN`, or `LOW_TENURE_ACTOR` row has been explained
   or escalated.
3. For any user-actor row, the actor's sign-in context near
   `AlertTime` has been reviewed against the 01-sign-in triage
   engine.
4. For any service-principal actor, recent SP credential / role
   changes have been reviewed via the narrative-gen output (or
   directly in `AuditLogs`).
5. The event has been mapped to one of the four closure buckets
   (**benign**, **precautionary benign**, **review required**,
   **suspicious / escalate**).
6. The narrative-gen output has been pasted into the ticket.

## Validation — test cases

> TODO: replace the placeholders below with real anonymised examples
> pulled from completed investigations.

1. **Known benign — TODO.** IaC pipeline service principal deploys
   a new resource group and assigns scoped RBAC; actor has thousands
   of historical operations of this exact shape; tenant prevalence is
   high; no related credential changes.
   *Expected:* quick-dive returns "Likely benign — routine IaC
   deployment"; deep-dive shows zero rare/new-for-actor flags;
   narrative-gen converges benign.
2. **Ambiguous — TODO.** On-call engineer makes a console NSG rule
   change outside the normal change window from an unfamiliar IP.
   *Expected:* quick-dive surfaces `NEW_IP_FOR_ACTOR`; deep-dive
   lands review-required; narrative-gen prompts a change-record
   check.
3. **Known bad / clearly suspicious — TODO.** Newly-created service
   principal granted Owner at subscription scope, followed inside the
   correlation window by Key Vault secret reads. Narrative-gen's SP
   credential-changes block fires; deep-dive shows
   `NEW_OPERATION_FOR_ACTOR + LOW_TENURE_ACTOR + PERSISTENCE_CHAIN`.
   *Expected:* suspicious — escalate.
