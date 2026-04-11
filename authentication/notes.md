# authentication (≈ 02-auth-changes)

Authentication-change investigation family. Scope: MFA registrations and
removals, security-info resets, password resets, and related Conditional
Access policy changes.

## Use case

An analyst arrives with a suspected auth-layer tamper: a user registered
a new MFA method unexpectedly, a security-info deletion appeared in audit
logs, a password reset happened outside of helpdesk hours, or a CA policy
was modified. This family will correlate the tamper event to the sign-in
timeline and the administrative actor.

## Starting entities

- UPN
- Actor UPN (when a tamper was performed on another user's account)
- Correlation id

## Queries in this family

| File | Role | Notes |
|---|---|---|
| `auth-deep-dive.kql` | deep-dive (analysis) | **Stub — empty.** See compliance notes below. |

No `narrative-gen.kql` yet.

## Data dependencies

Planned once the deep dive is authored:

| Table | Tag |
|---|---|
| `AuditLogs` | **Required** — source of auth-change operations. |
| `SigninLogs` | **Required** — correlate tamper events to sign-in activity. |
| `IdentityInfo` | **Optional enrichment** — actor/target context. |

## Done criteria

Triage is finished when:

1. Every auth-change operation in the window has an identified actor.
2. Each change has been correlated with a sign-in from the same actor and
   classified as legitimate admin work or tamper.
3. If the change is on a privileged account, PIM activation history has
   been reviewed.
4. The event has been mapped to one of the four closure buckets.

## Closure language

- **Benign** — helpdesk-driven password reset or user-driven MFA
  registration during normal working hours from a known device.
- **Precautionary benign** — self-service MFA registration from a new
  device inside a known travel window.
- **Review required** — MFA registration or security-info deletion
  outside business hours without a matching helpdesk ticket.
- **Suspicious / escalate** — security-info deletion followed by a
  sign-in from a new IP, password reset performed by a non-helpdesk
  actor, or any auth-change on a privileged account without PIM context.

## Validation — test cases

1. **Known benign.** Helpdesk operator resets a user password during
   working hours, user signs in next morning from usual device.
2. **Ambiguous.** User self-registers a new phone for MFA from a new IP
   during a known business-trip window.
3. **Known bad / clearly suspicious.** Security info deleted followed by
   MFA registration from a new country inside 30 minutes of sign-in.

## Contract compliance notes

- `auth-deep-dive.kql` is an empty 1-byte placeholder. It should be
  authored to the contract (header block + parameterised `let` block) or
  flagged for deletion if the family is being deprioritised.
- No `narrative-gen.kql` exists — author or flag.
- Some auth-change content already lives in the `identity/` family
  (`mfa-authentication-finder`, `privileged-account-activity-monitor`).
  Decide whether to split those out into this family or leave them in
  `identity/` under the contract's "similar names" allowance.
