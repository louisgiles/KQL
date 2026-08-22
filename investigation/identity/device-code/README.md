# Device-code authentication

Use this module when a Microsoft Entra sign-in alert indicates a suspicious
direct device-code authentication flow and the analyst needs to decide whether
to verify, contain, or widen incident scope.

The incident is the launcher. Start with the exact UPN and actual sign-in time
already visible in the incident or alert. Do not run a separate entity
extraction step.

## Programme status

This module implements the three-part device-code investigation path:

1. rapid containment decision;
2. post-authentication session, token, application, resource, audit, and action
   scope;
3. exact-IP campaign scope across other users.

This is still rapid containment decision **1 of 10** across the wider
high-frequency investigation programme. The device-code decision is complete
and **9 rapid decisions remain**.

This count measures rapid-decision coverage, not the number of queries. Tenant
runtime validation of all three device-code queries remains outstanding.

## Query

| File | Depth | Output | Purpose |
|---|---|---|---|
| `rapid-decision.kql` | Quick | One decision row | Resolves the client and resource path, user and tenant device-code history, network change, evidence quality, and immediate action. |
| `post-auth-scope.kql` | Deep | Prioritised event grid | Shows exact session or token continuation, affected apps and resources, directory changes, Microsoft 365 operations, cloud-app activity, and Azure control-plane actions. |
| `campaign-scope.kql` | Deep | Prioritised scope grid | Shows other users, apps, resources, attempts, and successful flows from the anchor tenant and exact source IP. |

## Analyst run order

1. Populate the incident UPN and actual UTC sign-in time in
   `rapid-decision.kql`. Add `SigninLogs.Id` when available because it is the
   strongest disambiguator.
2. If the user denies the flow, the rapid decision says `CONTAIN NOW`, or
   containment impact is still unknown, run `post-auth-scope.kql` with the same
   incident values.
3. Run `campaign-scope.kql` when the source IP may represent phishing
   infrastructure, shared attacker infrastructure, or another affected user.
4. Stop when the result supports closure, containment, or one named follow-on
   question. Do not run every query by default.

`post-auth-scope.kql` and `campaign-scope.kql` both resolve their own anchor
from `SigninLogs`. They do not depend on output copied from
`rapid-decision.kql`.

## Starting entities

Required:

- `TargetUPN`: exact user principal name.
- `AlertTime`: actual UTC sign-in time, not incident creation time.

Preferred or optional for all three queries:

- `TargetSignInId`: `SigninLogs.Id`, preferred for disambiguation.
- `TargetCorrelationId`: correlation identifier.
- `TargetIPAddress`: exact source IP address.
- `BrokerDRSProhibitedByPolicy`: set to `true` only when tenant policy explicitly prohibits Authentication Broker to Device Registration Service device-code use.

`BrokerDRSProhibitedByPolicy` applies only to `rapid-decision.kql`.

## Dependencies

| Classification | Data | Behaviour |
|---|---|---|
| Required | `SigninLogs` | Resolves the alert anchor and powers the rapid decision and exact-IP campaign scope. Absence prevents a valid result. |
| Optional enrichment | `AADNonInteractiveUserSignInLogs` | Adds non-interactive token redemption and session continuation to `post-auth-scope.kql`. |
| Optional enrichment | `AuditLogs` | Adds Entra directory, authentication-method, group, app, consent, role, and credential changes initiated by the identity. |
| Optional enrichment | `OfficeActivity` | Adds Exchange, SharePoint, OneDrive, and Teams operations. |
| Optional enrichment | `CloudAppEvents` | Adds cloud application and object activity when Defender for Cloud Apps telemetry is connected. |
| Optional enrichment | `AzureActivity` | Adds Azure subscription and management-group control-plane actions. |
| Avoid as hard dependency | `IdentityInfo`, UEBA, risk-user, and threat-intelligence tables | Their absence never suppresses primary evidence. |

The deep post-auth query uses a fuzzy union with a typed empty branch so one
missing optional table does not suppress available sources. A result from one
source does not prove coverage in the others. Confirm connector ingestion and
retention before interpreting an empty domain as no activity.

The source tenant is anchored from `AADTenantId`. The query does not use a
workspace-wide baseline across unrelated tenants.

## Time behaviour

- Target search: five minutes before and after `AlertTime`, with one hour of physical ingestion slack.
- Clean familiarity baseline: 90 days ending 24 hours before the target window.
- Literal prior-use interval: the 90 days immediately before the target window.
- Near-incident clustering: the excluded 24 hours before the target window.
- Default ingestion grace: two days at baseline edges.
- Post-authentication scope: 15 minutes before through 24 hours after the alert
  by default; maximum routine lookforward 48 hours.
- Exact-IP campaign scope: 24 hours before and after the alert by default;
  maximum routine bound seven days in each direction.

The Logs time selector or API timespan must include the full baseline, clean
gap, and ingestion grace.

## Decision nodes

1. Client and resource: classifies Authentication Broker, Office Home,
   Microsoft 365 and Office, developer tooling, and the target resource as
   separate facts.
2. Protocol history: reports literal prior-90-day attempts, successful clean
   familiarity, recent 24-hour clustering, tenant frequency, and same-path
   frequency.
3. Network change: evaluates user ASN, country, and ASN-country pair, then
   compares them with the previous successful flow. Recorded-device history is
   corroborative only.

Default frequency thresholds are deliberately visible at the top of the query:

- established user use: at least 3 successful stable-key flows across 2 days;
- frequent tenant use: at least 20 successful stable-key flows across 5 users
  and 10 days;
- sudden network change: a changed pair within 7 days.

Calibrate these thresholds against representative tenants before operational
use.

## Output and action

Read the first five columns first:

| Column | Effect |
|---|---|
| `Determination` | `FIX SCOPE`, `CONTAIN NOW`, or `VERIFY NOW`. |
| `RecommendedAction` | Immediate analyst action. |
| `ContainmentTriggers` | Deterministic hard triggers, with no weighted score. |
| `ReviewFlags` | Ambiguity, missing coverage, and network caveats. |
| `DecisionSummary` | Compact client, protocol, tenant, network, device, and coverage evidence. |

Detailed trace identifiers, counts, classifications, quality states, and raw
context are retained in the dynamic `Evidence` bag.

Decision meaning:

- `FIX SCOPE`: the query did not isolate one successful direct device-code flow
  with a stable request, correlation, or sign-in key and source tenant.
- `CONTAIN NOW`: an explicit identity-risk, tenant-policy, Broker to DRS, or
  compound protocol and eligible-network hard trigger is present.
- `VERIFY NOW`: directly confirm the action with the user and sanctioned-use
  evidence. If denied, unrecognised, or not promptly verified, contain.

Telemetry alone never produces a benign determination. Known public app IDs,
tenant frequency, prior use, and familiar network history only change the
verification context.

### Post-authentication grid

Read these columns first:

| Column | Effect |
|---|---|
| `Priority` | `critical`, `high`, `review`, or a scope-fix status. |
| `AssociationConfidence` | `Exact`, `High`, `Contextual`, or `none`. |
| `AssociationBasis` | The field or constrained relationship that connected the row to the anchor. |
| `EvidenceType` and `SourceTable` | The activity domain and its originating Sentinel table. |
| `AppOrOperation` and `ResourceOrTarget` | What the associated identity did and where. |
| `Decision` and `NextAction` | Whether to escalate and the next containment or verification step. |

Exact confidence requires `UniqueTokenIdentifier`, `SessionId`, or
`OriginalRequestId`. Correlation ID is high confidence. Exact identity or
identity plus source IP inside the bounded post-authentication window is
contextual evidence and must not be represented as token proof.

Successful non-interactive token use is prioritised as critical. Sensitive
audit operations include privilege, credential, authentication-method,
application, service-principal, group-membership, and consent changes. M365,
cloud-app, and Azure control-plane rows similarly surface high-impact actions
without assuming that every action is malicious.

### Exact-IP campaign grid

The campaign query is deliberately strict. It matches:

- the anchor `AADTenantId`;
- the exact source IP, resolved from the anchor when not supplied;
- direct `AuthenticationProtocol == deviceCode` activity;
- a bounded campaign window.

It returns one row per user, client app, and target resource path with first and
last observation, stable-flow attempts, successful flows, trace identifiers,
network context, and the containment action. Another identity on the exact
tenant, IP, and protocol path is prioritised for escalation. No subnet,
geolocation, display-name, or workspace-wide similarity is treated as campaign
association.

## Done criteria

The investigation is complete when:

1. Exactly one successful direct device-code flow is isolated.
2. The client and target resource are classified separately.
3. User attempts, successful familiarity, tenant frequency, and same-path
   frequency are visible.
4. Current and previous user ASN-country pairs and their time gap are visible.
5. Recorded-device evidence is clearly treated as corroborative.
6. Coverage, fallback-key, Global Secure Access, and proxy caveats are resolved.
7. The recommended action is completed or the evidence-based override is
   recorded.
8. Associated session or token continuation and affected resources are known.
9. Directory, Microsoft 365, cloud-app, and Azure audit posture has been
   checked in every connected source relevant to the incident.
10. The exact-IP campaign query has either identified and scoped other users or
    its coverage limit has been recorded.

## Coverage and validation

- `90D_CLEAN_WINDOW_OBSERVED` requires events near both baseline edges and at
  least 60 active tenant days. It is a conservative proxy, not proof of perfect
  ingestion.
- `PRIOR_90D_WINDOW_OBSERVED` separately protects the literal prior-use answer.
- Incomplete coverage returns an unknown state and cannot create a novelty-only
  containment trigger.
- Network evidence cannot hard-trigger when the Global Secure Access field is
  unavailable or a GSA source address is not demonstrably restored.
- `DeviceDetail.deviceId` does not prove which physical device requested or
  polled the code.
- Display-name classification does not carry the same confidence as exact app
  and resource identifiers.
- `dcount()` remains approximate.

Static review is not a Sentinel runtime guarantee. Before production use, run:

```powershell
pwsh ./scripts/test-kql.ps1
python3 ./scripts/lint-kql-runtime-literals.py .
```

The runtime-literal lint rejects unsupported `format_datetime()` tokens in
active KQL. This guard was added after Sentinel rejected an invalid `T` and `Z`
format literal on 2026-08-22.

Then compile and execute expected-looking, suspicious, partial-coverage,
Broker to DRS, GSA, duplicate-flow, and failed-flow cases in a representative
Sentinel workspace. Also test exact token continuation, same-session resource
use, contextual audit activity, absent optional tables, a second user on the
exact IP, an empty campaign result, and both row-limit paths. Record
complete-query P95 runtime and calibrate the exposed thresholds. Do not present
the queries as production-ready until actual Sentinel compilation and execution
have passed.

Primary references:

- [SigninLogs schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs)
- [AADNonInteractiveUserSignInLogs schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/aadnoninteractiveusersigninlogs)
- [AuditLogs schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/auditlogs)
- [OfficeActivity schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/officeactivity)
- [CloudAppEvents schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/cloudappevents)
- [AzureActivity schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/azureactivity)
- [Microsoft Entra authentication flows](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-authentication-flows)
- [Microsoft analysis of Storm-2372 device-code phishing](https://www.microsoft.com/en-us/security/blog/2025/02/13/storm-2372-conducts-device-code-phishing-campaign/)
