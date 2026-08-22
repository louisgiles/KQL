# Device-code authentication

Use this module when a Microsoft Entra sign-in alert indicates a suspicious
direct device-code authentication flow and the analyst needs a containment
decision quickly.

## Programme status

This is rapid containment decision **1 of 10**. The device-code decision is
complete and **9 decisions remain**.

This count measures implemented rapid-decision coverage. It does not mark the
broader universal device-code playbook or tenant runtime validation complete.

## Query

| File | Output | Purpose |
|---|---|---|
| `rapid-decision.kql` | One decision row | Resolves the client and resource path, user and tenant device-code history, network change, evidence quality, and immediate action. |

## Starting entities

Required:

- `TargetUPN`: exact user principal name.
- `AlertTime`: actual UTC sign-in time, not incident creation time.

Preferred or optional:

- `TargetSignInId`: `SigninLogs.Id`, preferred for disambiguation.
- `TargetCorrelationId`: correlation identifier.
- `TargetIPAddress`: exact source IP address.
- `BrokerDRSProhibitedByPolicy`: set to `true` only when tenant policy explicitly prohibits Authentication Broker to Device Registration Service device-code use.

## Dependencies

| Classification | Data | Behaviour |
|---|---|---|
| Required | `SigninLogs` | Absence prevents a valid decision. |
| Optional enrichment | None | The query has no enrichment-table dependency. |
| Avoid as hard dependency | `IdentityInfo`, UEBA, risk-user, and threat-intelligence tables | Their absence never suppresses the primary result. |

The source tenant is anchored from `AADTenantId`. The query does not use a
workspace-wide baseline across unrelated tenants.

## Time behaviour

- Target search: five minutes before and after `AlertTime`, with one hour of physical ingestion slack.
- Clean familiarity baseline: 90 days ending 24 hours before the target window.
- Literal prior-use interval: the 90 days immediately before the target window.
- Near-incident clustering: the excluded 24 hours before the target window.
- Default ingestion grace: two days at baseline edges.

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

Static structure, logic, safety, and performance review passed. Before
production use, run:

```powershell
pwsh ./scripts/test-kql.ps1
```

Then compile and execute expected-looking, suspicious, partial-coverage,
Broker to DRS, GSA, duplicate-flow, and failed-flow cases in a representative
Sentinel workspace. Record complete-query P95 runtime and calibrate the exposed
thresholds.

Primary references:

- [SigninLogs schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs)
- [Microsoft Entra authentication flows](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-authentication-flows)
- [Microsoft analysis of Storm-2372 device-code phishing](https://www.microsoft.com/en-us/security/blog/2025/02/13/storm-2372-conducts-device-code-phishing-campaign/)
