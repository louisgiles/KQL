# 03-office-ops

Office / M365 operations investigation family. Scope: mailbox permission
grants, inbox-rule creation, forwarding changes, transport-rule edits,
folder-permission edits, and delegation changes surfaced from
`OfficeActivity`.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | Evidence engine for an Office activity alert — scoped to `AlertTime ± EventWindow`, enriched with actor/target/delegee identity, privileged-role baseline, historical frequency, sign-in posture, and MFA-tamper check. |
| `narrative-gen.kql` | narrative | TODO — not yet authored. |

## Purpose

Triage an Office activity alert end to end. The alert gives you an actor
UPN and an `AlertTime`. The deep dive scopes `OfficeActivity` tightly to
a window either side of `AlertTime` (default ±1h), extracts the target
(mailbox, site, object) from `OfficeObjectId` / `Parameters`, extracts
any delegee / grantee / forwarding address from the parameter bag, and
produces one row per operation with a weighted `TriageVerdict`.

Office activity is noisy over wide windows. The `EventWindow` scoping is
the primary noise-control mechanism — historical baselines and sign-in
posture run against their own independent windows and never widen the
main pipeline.

## Starting entities

- **Actor UPN** — from the alert entities or analyst input.
- **AlertTime** — datetime from the alert. Used as the centre of the
  `EventWindow` scope.
- **Target** — NOT an alert entity. Extracted from `OfficeActivity`
  `OfficeObjectId` or the `Parameters` blob during the query.
- **Delegee / grantee / forwarding address** — NOT an alert entity.
  Extracted from `Parameters` (`User`, `Trustee`, `GrantSendOnBehalfTo`,
  `ForwardingAddress`, `ForwardingSmtpAddress`, `RedirectTo`).

## Variables

| Variable | Default | Purpose |
|---|---|---|
| `ActorToCheck` | `""` | Actor UPN — from the alert. |
| `AlertTime` | `datetime(null)` | Centre of the event window — from the alert. |
| `EventWindow` | `1h` | Primary scoping window around `AlertTime`. |
| `SigninLookback` | `24h` | Sign-in posture window either side of `AlertTime`. |
| `ActorHistoryWindow` | `90d` | Historical frequency baseline window, strictly prior to `AlertTime - EventWindow`. |

## Required tables

- **`OfficeActivity`** — **required**. Primary source. Query breaks
  without it. Scoped to `AlertTime ± EventWindow`.

## Optional tables

- **`IdentityInfo`** — **optional enrichment**. Three-way left-outer
  join for actor, target, and delegee (job title, manager, department,
  assigned roles, identity risk). Sparse results are fine.
- **`SigninLogs`** — **optional enrichment**. Actor sign-in posture —
  IP familiarity, device trust, MFA method, AAD risk signals. Left-
  joined by UPN; missing coverage leaves the row with null posture.
- **`AuditLogs`** — **optional enrichment**. Two independent uses:
  (1) privileged-user baseline built from role-assignment events over
  90 days, and (2) MFA-tamper check for any auth-method changes on the
  actor within 24h of `AlertTime`.

## High-risk operation list

Flagged via the `HIGH_RISK_OPERATION` factor:

- `Add-MailboxPermission`, `Remove-MailboxPermission`
- `Set-Mailbox`
- `New-InboxRule`, `Set-InboxRule`
- `New-TransportRule`, `Set-TransportRule`
- `Add-MailboxFolderPermission`, `Set-MailboxFolderPermission`

Forwarding is detected independently of the operation name via the
`FORWARDING_DETECTED` factor whenever `ForwardingAddress`,
`ForwardingSmtpAddress`, `RedirectTo`, or `DeliverToMailboxAndForward`
appears in the parameter bag.

## Risk factors

| Flag | Weight | Meaning |
|---|---|---|
| `HIGH_RISK_OPERATION` | 20 | Operation is in the high-risk list. |
| `FORWARDING_DETECTED` | 25 | Forwarding address or deliver-to-mailbox-and-forward set. |
| `EXTERNAL_DELEGATE` | 25 | Delegate identity is external to the tenant. |
| `ACTOR_PRIVILEGED` | 10 | Actor holds a privileged role — elevated blast radius. |
| `TARGET_PRIVILEGED` | 20 | Target is a privileged identity. |
| `DELEGEE_PRIVILEGED` | 20 | Grantee / delegee is a privileged identity. |
| `ACTOR_FIRST_TIME_OP` | 25 | Actor has never run this operation in `ActorHistoryWindow`. |
| `ACTOR_LOW_FREQ_OP` | 10 | Actor has run this operation 1–2 times historically. |
| `ACTOR_SIGNIN_RISK` | 20 | Elevated AAD risk on the actor's most recent sign-in. |
| `ACTOR_UNTRUSTED_DEVICE` | 10 | Last sign-in not from Azure AD joined / Hybrid. |
| `ACTOR_NO_MFA` | 15 | No MFA challenge detected on the most recent sign-in. |
| `ACTOR_MFA_TAMPERED` | 25 | Auth-method changes found for actor within 24h of `AlertTime`. |

Verdict thresholds:

| Score | Verdict |
|---|---|
| ≥ 70 | 🔴 HIGH-RISK |
| ≥ 45 | 🟠 MEDIUM-RISK |
| ≥ 20 | 🟡 LOW-RISK |
| < 20 | 🟢 LIKELY BENIGN |

## Done criteria

- Every row in the `EventWindow` scope has a `TriageVerdict`.
- Every `🔴` / `🟠` row has been explained (known admin task, known
  delegation pattern, change record) or escalated.
- Every `FORWARDING_DETECTED` row has the forwarding address resolved
  and classified (internal / external / mailbox-rule only).
- Every `EXTERNAL_DELEGATE` row has the grantee identity resolved and
  the business justification captured.
- Every `ACTOR_MFA_TAMPERED` row has the corresponding auth-method
  change investigated via the 02-auth-changes deep dive.
- Actor sign-in posture has been checked against 01-sign-in for every
  row touching a privileged target or delegee.

## Validation — test cases

1. **Known benign — TODO.** Exchange admin runs
   `Add-MailboxFolderPermission` granting `Reviewer` on a shared calendar
   to an internal colleague during business hours. Actor is privileged,
   target is internal, delegee is internal, no forwarding, historical
   op count is high, sign-in is clean. Expected verdict: 🟢 / 🟡.
2. **Ambiguous — TODO.** Non-admin user creates a `New-InboxRule` that
   moves messages from a specific internal sender into a subfolder, no
   forwarding, no external delegee, but it is the actor's first inbox
   rule in 90 days. Expected verdict: 🟡, analyst judgement.
3. **Known bad / clearly suspicious — TODO.** User account runs
   `Set-Mailbox` with `ForwardingSmtpAddress` pointed at an external
   domain, or `New-InboxRule` named `" "` that forwards all messages
   externally and marks them as read. Bonus points if an auth-method
   change also fired for the same actor within 24h. Expected verdict:
   🔴 with `FORWARDING_DETECTED + EXTERNAL_DELEGATE + ACTOR_MFA_TAMPERED`.
