# 03-office-ops

Office / M365 operations investigation family. Scope: mailbox permission
grants, inbox-rule creation, forwarding changes, transport-rule edits,
folder-permission edits, delegation changes, and management-role
assignments surfaced from `OfficeActivity`.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | Operation-aware evidence engine — scoped to `AlertTime ± EventWindow`, filtered to a whitelist of meaningful operations, enriched with actor/target/delegee identity, sign-in posture, MFA tamper check, and a weighted triage verdict. |
| `narrative-gen.kql` | narrative | Ticket-ready closure note in analyst dash-prefixed format — timestamp, operation counts, plain-English translation, sign-in posture, MFA tamper result, identity context, and determination. |

## Purpose

Triage an Office activity alert end to end. The alert gives you an actor
UPN, an operation type, and an `AlertTime`. The deep dive scopes
`OfficeActivity` tightly to a window either side of `AlertTime` (default
±1h), filters to a whitelist of meaningful operations (excluding noise
like message reads, Teams reactions, mail item access), extracts the
target from `OfficeObjectId` / `Parameters`, extracts any delegee /
grantee / forwarding address from the parameter bag, translates each
operation into a plain-English sentence, and produces one row per
operation with a weighted `TriageVerdict`.

The narrative gen outputs a paste-ready analyst note in dash-prefixed
format — not a structured report.

## Starting entities

- **Actor UPN** — from the alert entities or analyst input.
- **OperationType** — operation name from the alert (e.g.
  `Add-MailboxPermission`, `New-InboxRule`, `Set-Mailbox`). Leave empty
  for all whitelisted ops in the window.
- **AlertTime** — datetime from the alert. Used as the centre of the
  `EventWindow` scope.
- **Target** — NOT an alert entity. Extracted from `OfficeActivity`
  `OfficeObjectId` or the `Parameters` blob during the query.
- **Delegee / grantee / forwarding address** — NOT an alert entity.
  Extracted from `Parameters` (`User`, `Trustee`, `GrantSendOnBehalfTo`,
  `ForwardingAddress`, `ForwardingSmtpAddress`, `RedirectTo`,
  `ForwardTo`).

## Variables

| Variable | Default | Purpose |
|---|---|---|
| `ActorToCheck` | `""` | Actor UPN — from the alert. |
| `OperationType` | `""` | Operation name from the alert. Empty = all whitelisted ops. |
| `AlertTime` | `datetime(null)` | Centre of the event window — from the alert. |
| `EventWindow` | `1h` | Primary scoping window around `AlertTime`. |
| `SigninLookback` | `24h` | Sign-in posture window either side of `AlertTime`. |
| `ActorHistoryWindow` | `90d` | Historical frequency baseline, strictly prior to `AlertTime - EventWindow`. Deep dive only. |

## Required tables

- **`OfficeActivity`** — **required**. Primary source. Query breaks
  without it. Scoped to `AlertTime ± EventWindow`, filtered to the
  operation whitelist before any joins.

## Optional tables

- **`IdentityInfo`** — **optional enrichment**. Three-way left-outer
  join for actor, target, and delegee (job title, department, manager,
  assigned roles). Sparse results are fine.
- **`SigninLogs`** — **optional enrichment**. Actor sign-in posture —
  IP org familiarity (`DaysSeenInOrg` via `dcount(datetime_part("day",
  TimeGenerated))`), `DaysSeenUser`, `UsersWithIP` count, device trust
  (trust type, managed, compliant, OS), MFA method, conditional access
  status, AAD risk level and detail. Left-joined by UPN; missing
  coverage leaves the row with null posture.
- **`AuditLogs`** — **optional enrichment**. Two independent uses:
  (1) privileged-user baseline built from role-assignment events over
  90 days (deep dive only), and (2) MFA-tamper check for any auth-method
  changes on the actor within 24h of `AlertTime`.

## Operation whitelist

Only these operations pass the filter. Everything else is noise:

- `Add-MailboxPermission`, `Remove-MailboxPermission`
- `Add-MailboxFolderPermission`, `Set-MailboxFolderPermission`,
  `Remove-MailboxFolderPermission`
- `Set-Mailbox`, `Set-MailboxCalendarConfiguration`
- `New-InboxRule`, `Set-InboxRule`, `Remove-InboxRule`
- `New-TransportRule`, `Set-TransportRule`, `Remove-TransportRule`
- `New-ManagementRoleAssignment`, `Remove-ManagementRoleAssignment`

## Risk factors (deep dive)

| Flag | Weight | Meaning |
|---|---|---|
| `HIGH_RISK_OP` | 20 | Operation is a mailbox permission grant, forwarding change, or inbox rule creation. |
| `TARGET_PRIVILEGED` | 20 | Target holds a privileged role. |
| `DELEGEE_PRIVILEGED` | 20 | Delegee/grantee holds a privileged role. |
| `DELEGEE_EXTERNAL` | 25 | Delegate identity is external to the tenant. |
| `ACTOR_FIRST_TIME_OP` | 25 | Actor has never performed this operation in `ActorHistoryWindow`. |
| `ACTOR_LOW_FREQ_OP` | 10 | Actor has performed this operation 1–2 times historically. |
| `ACTOR_SIGNIN_RISK` | 20 | Elevated AAD risk on actor's most recent sign-in. |
| `ACTOR_UNTRUSTED_DEVICE` | 10 | Last sign-in not from Azure AD joined / Hybrid. |
| `ACTOR_NO_MFA` | 15 | No MFA challenge detected on the session. |
| `ACTOR_MFA_TAMPERED` | 25 | Auth-method changes found for actor within 24h of `AlertTime`. |
| `FORWARDING_EXTERNAL` | 25 | Forwarding address points outside the tenant. |

Note: There is deliberately NO `ACTOR_PRIVILEGED` factor — anyone
performing these operations is inherently privileged. The deep dive notes
it but does not score it.

Verdict thresholds:

| Score | Verdict |
|---|---|
| ≥ 70 | 🔴 HIGH-RISK |
| ≥ 45 | 🟠 MEDIUM-RISK |
| ≥ 20 | 🟡 LOW-RISK |
| < 20 | 🟢 LIKELY BENIGN |

## Done criteria

- Every row in the `EventWindow` scope has a `TriageVerdict` and
  `ActionTranslation`.
- Every `🔴` / `🟠` row has been explained (known admin task, known
  delegation pattern, change record) or escalated.
- Every `FORWARDING_EXTERNAL` row has the forwarding address resolved
  and classified.
- Every `DELEGEE_EXTERNAL` row has the grantee identity resolved and
  business justification captured.
- Every `ACTOR_MFA_TAMPERED` row has the corresponding auth-method
  change investigated via the 02-auth-changes deep dive.
- Actor sign-in posture has been checked against 01-sign-in for every
  row touching a privileged target or delegee.
- Narrative gen output reviewed and pasted into the ticket.

## Validation — test cases

1. **Known benign — TODO.** Exchange admin runs `Add-MailboxPermission`
   granting `FullAccess` on a shared mailbox to an internal colleague,
   plus `Set-Mailbox` granting `SendOnBehalf`. Actor is privileged,
   target is internal, delegee is internal, no forwarding, historical
   op count is high, sign-in is clean from a high-frequency IP. Expected
   deep-dive verdict: 🟢 / 🟡. Expected narrative: "Converges benign."
2. **Ambiguous — TODO.** Non-admin user creates a `New-InboxRule` that
   moves messages from a specific internal sender into a subfolder, no
   forwarding, no external delegee, but it is the actor's first inbox
   rule in 90 days and the source IP has only been seen 2 days.
   Expected deep-dive verdict: 🟡. Expected narrative: "Review required."
3. **Known bad / clearly suspicious — TODO.** User account runs
   `New-InboxRule` named `" "` that forwards all messages to an external
   address and marks them as read. Source IP unfamiliar (1 day in org),
   no MFA challenge, and an auth-method registration fired for the same
   actor 3 hours before the rule creation. Expected deep-dive verdict:
   🔴 with `HIGH_RISK_OP + FORWARDING_EXTERNAL + ACTOR_FIRST_TIME_OP +
   ACTOR_NO_MFA + ACTOR_MFA_TAMPERED`. Expected narrative: "Suspicious.
   Escalate."
