# 02-auth-changes

Authentication-change investigation family. Scope: password resets, MFA
registrations and removals, security-info modifications, Strong
Authentication disable/enable, Conditional Access policy edits, and
role assignments that touch the auth surface.

## Purpose

Given an auth-change audit event, answer the seven triage questions a
reviewer asks at triage:

1. Who is the actor and who is the target.
2. What was changed (operation, modified properties, old vs new).
3. Is the actor's recent sign-in posture clean (IP, location, risk
   level, MFA, device trust).
4. Is the actor privileged or otherwise expected to make this kind of
   change.
5. Is the target account privileged or sensitive.
6. Is the action frequent or unusual for this actor (historical count
   of the same operation by the same actor, baselined on the
   90d-to-investigation window).
7. Does the weighted verdict converge benign or need escalation.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | Evidence engine. Filters `AuditLogs` to auth-change operations, enriches with `IdentityInfo`, privileged-user baseline, actor historical frequency, and the actor's recent `SigninLogs` posture, then emits a weighted `RiskScore` / `TriageVerdict`. |
| `narrative-gen.kql` | narrative | Closure note. Target-UPN-focused — pulls each auth-method change for the user, joins sign-in context within `SigninContextWindow` of each change, and emits a ticket-ready text summary. Does not overlap the deep dive's row-per-event scoring. |

## Starting entities

- Actor UPN (`ActorToCheck`) — the principal performing the change.
- Target UPN (`TargetToCheck`) — the principal whose account was
  modified. For self-service changes actor and target are the same.
- Operation name fragment (`OperationFilter`) — optional free-text
  filter against `OperationName`, e.g. `"Reset password"` or
  `"security info"`.

## Required tables

- `AuditLogs` — **Required**. All auth-change operations flow through
  this table. Every pivot in `deep-dive.kql` starts here.

## Optional tables

- `IdentityInfo` — **Optional enrichment**. Looked up twice (once for
  actor, once for target) for job title, department, manager, assigned
  roles, and identity-level risk. Both joins are `leftouter` and every
  enriched column is `coalesce`'d so sparse `IdentityInfo` rows do not
  drop audit events or poison the risk scoring.
- `SigninLogs` — **Optional enrichment**. Used to pull the actor's most
  recent sign-in (IP, location, result, risk level, risk detail,
  trust type, MFA requirement) and a small stats bundle (sign-in
  count, failure count, distinct IPs, distinct locations) over
  `SigninLookback`. Both subqueries are left-joined; missing rows
  leave the posture columns null and only the two posture-related
  risk factors (`_actorSigninRisk`, `_actorUntrustedDevice`) zero out.
  A missing `SigninLogs` row never drops an audit event.

## Variables

| Variable | Default | Role |
|---|---|---|
| `TimeToCheck` | `14d` | Main investigation window. |
| `ActorToCheck` | `""` | Actor UPN substring filter. |
| `TargetToCheck` | `""` | Target UPN substring filter. |
| `OperationFilter` | `""` | Free-text filter against `OperationName`. |
| `SigninLookback` | `24h` | Window for actor sign-in posture check. |
| `ActorHistoryWindow` | `90d` | Baseline window for actor's historical op frequency; strictly prior to `TimeToCheck` so the action under review never contributes to its own baseline. |

## Done criteria

1. Every row has a `TriageVerdict`.
2. Every `🔴 HIGH-RISK` and `🟠 MEDIUM-RISK` row has been explained
   — known helpdesk pattern, legitimate self-service change, PIM
   activation with matching change record — or escalated.
3. For any row touching a privileged target, the actor's
   `ActorLastSignin*` columns have been reviewed and classified
   against the four closure buckets.
4. `ModifiedProperties` has been read for any row whose operation is
   `Update user`, `Update conditional access policy`, or similar —
   the actual old/new values matter there.
5. The event has been mapped to one of the four closure buckets
   (**benign**, **precautionary benign**, **review required**,
   **suspicious / escalate**).

## Closure language

- **Benign** — helpdesk-driven password reset or user-driven MFA
  registration during working hours from a compliant device, high
  `HistoricalOpCount` for this actor, non-privileged target.
- **Precautionary benign** — self-service MFA registration from a
  new IP inside a known travel window; low but non-zero
  `HistoricalOpCount`; non-privileged target.
- **Review required** — `ACTOR_FIRST_TIME_OP` on a non-privileged
  target, or an admin change with a clean sign-in posture but no
  matching change record.
- **Suspicious / escalate** — any combination of
  `TARGET_PRIVILEGED` with `ACTOR_SIGNIN_RISK`,
  `SELF_SERVICE_ON_PRIV_ACCOUNT` with `ACTOR_UNTRUSTED_DEVICE`,
  `ACTOR_NOT_PRIVILEGED_CHANGING_PRIV`, or a security-info
  deletion followed by a `Reset password` from the same actor
  inside the window.

## Validation — test cases

> TODO: replace the placeholders below with real anonymised examples
> pulled from completed investigations.

1. **Known benign — TODO.** Helpdesk operator runs `Reset password`
   against a non-privileged user during business hours. Actor has
   thousands of historical `Reset password` events. Actor's last
   sign-in is from the org's admin jump-box, Azure AD joined, no
   risk detail.
   *Expected:* `deep-dive.kql` returns `🟢 LIKELY BENIGN`; no flags
   other than possibly `ACTOR_SIGNIN_FAILURES` if the actor had a
   single typo.
   *Fill in:* actor UPN placeholder, target UPN placeholder,
   timestamp.

2. **Ambiguous — TODO.** User self-registers a new MFA method
   (`User registered security info`) from a residential IP inside a
   known business-trip window on an unmanaged personal device.
   *Expected:* `🟡 LOW-RISK` or `🟠 MEDIUM-RISK`, flagged with
   `ACTOR_UNTRUSTED_DEVICE` and possibly `ACTOR_FIRST_TIME_OP` if
   this is the user's first self-service registration in 90 days.
   *Fill in:* UPN placeholder, IP, travel context.

3. **Known bad / clearly suspicious — TODO.** A non-helpdesk actor
   runs `User deleted security info` against a privileged target,
   followed by `Reset password` against the same target, from an
   IP with `medium` `RiskLevelDuringSignIn` and a non-AAD-joined
   device.
   *Expected:* `🔴 HIGH-RISK` with
   `ACTOR_NOT_PRIVILEGED_CHANGING_PRIV`, `TARGET_PRIVILEGED`,
   `ACTOR_SIGNIN_RISK`, `ACTOR_UNTRUSTED_DEVICE`, and likely
   `ACTOR_FIRST_TIME_OP` firing together.
   *Fill in:* actor UPN, target UPN, IP, timestamps.
