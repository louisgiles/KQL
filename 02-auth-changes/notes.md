# 02-auth-changes

Authentication-change investigation family. Scope: MFA registrations
and removals, security-info resets, password resets, and related
Conditional Access policy changes.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | TODO — empty stub. |
| `narrative-gen.kql` | narrative | TODO — not yet authored. |

## Starting entities

- TODO (likely: UPN, actor UPN, `CorrelationId`).

## Required tables

- TODO (likely: `AuditLogs`).

## Optional tables

- TODO (likely: `SigninLogs` — **optional enrichment** to correlate
  tamper with sign-in; `IdentityInfo` — **optional enrichment** for
  actor/target context).

## Done criteria

- TODO. Every auth-change operation in the window has an identified
  actor and has been classified legitimate vs tamper.

## Validation — test cases

1. **Known benign — TODO.** Helpdesk password reset during business
   hours followed by normal user sign-in.
2. **Ambiguous — TODO.** Self-service MFA registration from a new IP
   inside a known travel window.
3. **Known bad / clearly suspicious — TODO.** Security-info deletion
   followed by MFA registration from a new country within 30 minutes
   of sign-in.
