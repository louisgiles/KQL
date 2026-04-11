# identity (≈ 01-sign-in)

Sign-in and identity-layer investigation family. Covers sign-in triage,
baseline behaviour, failed-auth patterns, MFA gap detection, token replay,
privileged account activity, and service principal authentication.

## Use case

An analyst arrives with an identity-layer signal: a risky sign-in alert, a
flagged UPN, an unfamiliar IP, a privileged role activation, or a service
principal behaving unusually. This family provides the evidence engine and
the closure note for that triage.

## Starting entities

- UPN (primary)
- IP address
- Device display name
- Service principal id / app id
- Correlation id (for token replay work)

## Queries in this family

| File | Role | Notes |
|---|---|---|
| `sign-in-triage-plus-risk-scoring-engine` | deep-dive (analysis) | Weighted risk scoring across nine signals. |
| `sign-in-investigation-narrative-gen` | narrative-gen (narrative) | Closure-ready per-user summary. |
| `sign-in-baseline-behaviour` | deep-dive support (analysis) | 30-day baseline for "normal". |
| `failed-auth-pattern` | deep-dive support (analysis) | Password spray, brute force, credential stuffing. |
| `mfa-authentication-finder` | deep-dive support (analysis) | MFA gaps, legacy protocol bypass, CA exemptions. |
| `anomalous-token-replay` | deep-dive support (analysis) | Token replay, impossible travel, device/UA shift, AiTM. |
| `privileged-account-activity-monitor` | deep-dive support (analysis) | PIM activations, high-risk ops, privileged sign-ins. |
| `service-principal-auth-tracker` | deep-dive support (analysis) | SP sign-ins, new creds, permission grants, off-hours. |

## Data dependencies

| Table | Tag | Used by |
|---|---|---|
| `SigninLogs` | **Required** | all sign-in queries |
| `AADServicePrincipalSignInLogs` | **Required** | service-principal-auth-tracker |
| `AuditLogs` | **Required** | privileged-account-activity-monitor, service-principal-auth-tracker, narrative-gen, triage engine |
| `IdentityInfo` | **Optional enrichment** | narrative-gen, triage engine (job title, manager, assigned roles) |
| `IdentityLogonEvents` | **Avoid as hard dependency** | referenced in `failed-auth-pattern` comment but not joined; coverage gaps reported |
| `IdentityDirectoryEvents` | **Avoid as hard dependency** | referenced in `privileged-account-activity-monitor` comment but not used in filters |

## Done criteria

Triage is finished when:

1. Every elevated risk score row has been explained (user action, known
   travel, recent device change, etc.) or escalated.
2. Most recent sign-in has been classified against the four closure buckets.
3. Source IP has been checked against org-wide history (days seen in org /
   days seen for this user).
4. MFA audit trail has been reviewed for the last 24h.
5. If privileged: PIM activations and high-risk ops have been walked through.
6. The narrative-gen output has been pasted into the ticket.

## Closure language

- **Benign** — baseline sign-ins, known device, org-familiar IP, MFA
  satisfied, no audit-log churn.
- **Precautionary benign** — new but plausible IP (travel, tethering),
  unmanaged but compliant device, single late-night sign-in matching role.
- **Review required** — new IP to org, new device to user, CA policy not
  applied but no MFA tampering, SP new source IP but known resource.
- **Suspicious / escalate** — token replay indicators, MFA audit-log
  modifications inside the sign-in window, impossible travel, password
  spray source hitting the account, privileged role add without PIM
  justification.

## Validation — test cases

1. **Known benign.** Daily driver UPN signing in from office IP on
   managed laptop, MFA satisfied via PhoneAppNotification. Triage engine
   should return `🟢 LIKELY BENIGN`; narrative should mention high-freq
   org IP and managed device.
2. **Ambiguous.** UPN signing in from a residential IP seen in the org
   for the first time, unmanaged personal device, MFA satisfied. Triage
   engine should land in `🟡 LOW-RISK` to `🟠 MEDIUM-RISK`; analyst has
   to decide travel vs. theft.
3. **Known bad / clearly suspicious.** UPN with a 24h MFA registration
   change followed by sign-in from a new country with impossible-travel
   flag and a `tokenIssuerAnomaly` risk event. Triage engine should land
   `🔴 HIGH-RISK`; narrative should surface the MFA audit trail alert and
   the AiTM indicator.

## Contract compliance notes

- Most queries here pre-date the contract header block. They should be
  retrofitted with the full `name / purpose / starting_entities /
  required_tables / optional_tables / variables / done_criteria /
  output_type` block before the next merge.
- Several files are missing the `.kql` extension. Extension normalisation
  is pending a rename pass.
- `sign-in-triage-plus-risk-scoring-engine` and
  `sign-in-investigation-narrative-gen` fulfil the `deep-dive.kql` and
  `narrative-gen.kql` roles respectively, under their current names.
