# Device-code authentication playbook

A four-step triage sequence for a suspicious device-code sign-in in Microsoft
Sentinel Log Analytics.

## Design explanation

Occam's razor governs this module: the simplest sequence that answers the
triage question is the right one. The repository already holds a maximal
single-query engine for this alert class
([`../../identity/device-code/`](../../identity/device-code/)); this playbook
is its deliberate counterpart — four small queries an analyst pastes in run
order, each answering exactly one question, each independently runnable.

The sequence is a decision funnel ordered by discriminating power per unit of
effort:

1. **Who asked for the token, and from where** (`1-signin-deep-dive.kql`).
   Device-code flow exists for input-constrained clients, so the client
   application is the strongest single discriminator. CLI and developer
   tooling (Azure CLI, Azure PowerShell, Graph CLI, Visual Studio) is the
   population device code was designed for and leans benign. The
   Microsoft Authentication Broker and FOCI family clients (Office, Teams)
   lean malicious in a device-code context, because they are what
   device-code phishing tradecraft requests — the broker path can end in a
   Primary Refresh Token and attacker device registration (Storm-2372
   pattern). The second discriminator is geography: in device-code phishing
   the **attacker's** infrastructure redeems the code, so the grant arrives
   from an IP, ASN, or country the user and device have no history with.
   Both discriminators live in one query because they come from the same
   sign-in rows.
2. **Is this novel for the user** (`2-user-precedent.kql`). Novelty is the
   cheapest strong signal and is deliberately a simple count: has this user
   ever completed device-code auth before, with which apps, from where.
   An empty result is itself evidence — first-ever use sharpens suspicion.
3. **Is this normal for the tenant** (`3-tenant-prevalence.kql`). The same
   simple count tenant-wide. A tenant where engineers run device-code auth
   daily reads the same sign-in very differently from a tenant where it has
   never been seen. Steps 2 and 3 are separate queries so either can be
   skipped when the answer is already known.
4. **What did the identity do with the access** (`4-audit-last-24h.kql`).
   Only reached when suspicion survives steps 1–3. A bounded 24-hour
   `AuditLogs` sweep for the identity, surfacing the post-compromise actions
   that change containment scope: security-info and MFA changes, device
   registration, consent grants, application credentials, role membership.

Design choices that follow from the razor:

- No joins between steps; each query resolves its own inputs from declared
  `let` parameters.
- Leanings, not verdicts. The client-app lists are visible, editable evidence
  at the top of step 1, and the output carries a signals column rather than a
  computed determination. The analyst decides; the mapping to the repository
  determination vocabulary is below.
- Baselines end at `InvestigationStart` so the activity under investigation
  cannot normalise itself.
- Uncertainty stays visible: geography flags return null (not false) when no
  baseline exists, and an empty precedent result means "no precedent
  observed", never "benign".

## Analyst run order

1. `1-signin-deep-dive.kql` — set `TargetUPN`, adjust the investigation
   window. Read `AppLeaning`, the geography-change flags, and
   `EscalationSignals` per sign-in.
2. `2-user-precedent.kql` — same `TargetUPN`; set `InvestigationStart` to the
   start of the window under investigation. Empty result = no precedent.
3. `3-tenant-prevalence.kql` — no entities required. Compare the tenant's
   device-code app mix and frequency with the sign-in from step 1.
4. `4-audit-last-24h.kql` — default is the literal last 24 hours of audit
   logs for the user. To scope post-authentication activity instead, set
   `AnchorTime` to the device-code sign-in time and `Lookforward` to `24h`.
5. Stop when the evidence supports a decision. Escalate confirmed or
   unresolved suspicion into the deep queries in
   [`../../identity/device-code/`](../../identity/device-code/)
   (`post-auth-scope.kql`, `campaign-scope.kql`) using the `SignInId` and
   `CorrelationId` carried in step 1 output.

## Starting entities and variables

| Variable | Steps | Meaning |
| --- | --- | --- |
| `TargetUPN` | 1, 2, 4 | Required. Exact user principal name. |
| `InvestigationStart` / `InvestigationEnd` | 1 | Window under investigation; default last 7 days. |
| `InvestigationStart` | 2, 3 | End of the precedent/prevalence baseline; default `now()`. Set it to the start of the window under investigation. |
| `BaselineLookback` | 1 | Geography familiarity baseline; default 30 days ending at `InvestigationStart`. |
| `PrecedentLookback` / `PrevalenceLookback` | 2, 3 | Count baseline; default 90 days ending at `InvestigationStart`. |
| `AnchorTime`, `Lookback`, `Lookforward` | 4 | Audit window; default the last 24 hours from now. |
| `CliLeaningApps`, `BrokerFociApps`, `DrsResourceAppId` | 1 | Editable classification lists (exact app IDs). |
| `SensitiveOperationTerms` | 4 | Editable keyword list that marks audit rows `review first`. |

## Dependencies

| Classification | Data | Behaviour |
| --- | --- | --- |
| Required (steps 1–3) | `SigninLogs` | Carries device-code sign-ins, client app, IP, geography, and device detail. Absence prevents any answer. |
| Required (step 4) | `AuditLogs` | Carries directory changes initiated by or targeting the identity. Absence prevents the step-4 answer only. |
| Optional enrichment | `OriginalTransferMethod` column | Read with `column_ifexists`; when present, sign-ins transferred from a device-code flow are included. |
| Avoid as hard dependency | UEBA, `IdentityInfo`, threat-intelligence tables | Not referenced; their absence never suppresses a result. |

Device-code rows are matched on `AuthenticationProtocol == "deviceCode"`,
plus `OriginalTransferMethod` values `deviceCodeFlow`/`deviceCode` where that
column exists. Non-interactive token continuation is out of scope here; it
belongs to the deep module.

## Time behaviour

- Step 1: bounded investigation window (default 7 days) plus a 30-day
  familiarity baseline ending at `InvestigationStart`.
- Steps 2–3: 90-day count baseline ending at `InvestigationStart`.
- Step 4: `AnchorTime - Lookback` to `AnchorTime + Lookforward`, default the
  last 24 hours; routine maximum 7 days total.
- The Logs time selector must include the full baseline range, not just the
  investigation window.

## Output and decision effect

Step 1 returns one row per device-code sign-in:

| Column | Effect |
| --- | --- |
| `AppLeaning` | `CLI/dev tooling - leans benign`, `Broker/FOCI client - leans malicious`, or `Unclassified - verify manually`. |
| `NewCountryForUser`, `NewAsnForUser`, `NewCountryForDevice` | `true` = not in the baseline; `null` = no baseline to compare, which is uncertainty, not safety. |
| `BrokerToDrs` | `true` when the Authentication Broker requested the Device Registration Service — the PRT/device-join tradecraft path. |
| `EscalationSignals` | Compact list of every triggered signal, or `none`. |
| `SignInId`, `CorrelationId` | Carry into the deep module on escalation. |

Steps 2–3 return one row per client app with attempts, successes, first/last
seen, active days, and (tenant) distinct users. Step 4 returns audit rows
with a `Direction` (initiated by user / targets user) and `Sensitivity`
(`review first` sorts above `routine`).

Mapping to the repository determination vocabulary:

- **Precautionary benign** — CLI-leaning app, familiar geography, established
  user and tenant precedent, and the user verbally confirms the action.
  Telemetry alone never concludes benign.
- **Review required** — any unclassified app, null baseline flag, absent
  precedent, or unverified user confirmation: continue to the next step.
- **Suspicious / escalate** — `BrokerToDrs`, or a malice-leaning client
  combined with new user/device geography, or sensitive audit operations in
  step 4: contain and escalate into the deep module.

## Done criteria

The playbook is complete when:

1. Every device-code sign-in in the window has a client-app leaning and
   geography flags.
2. User precedent and tenant prevalence counts are recorded, including an
   explicit "no precedent" where the result was empty.
3. The 24-hour audit sweep has been run, or explicitly skipped because
   steps 1–3 supported closure.
4. The outcome is containment, verified closure, or a named escalation into
   `../../identity/device-code/`.

## Coverage limits

- Geography baselines are only as good as 30/90 days of `SigninLogs`
  retention; null flags mark the gap.
- The client-app lists are deliberately small and must be extended per
  tenant; unclassified is a prompt to verify, not a verdict.
- `DeviceDetail.deviceId` does not prove which physical device polled the
  code.
- Step 4 keyword sensitivity is a triage sort order, not a taxonomy;
  `routine` rows can still matter.
- `dcount()` is approximate.

## Validation

Static checks:

```powershell
pwsh ./scripts/test-kql.ps1
python3 ./scripts/lint-kql-runtime-literals.py .
```

Parser success is grammar-only. Before operational use, compile and execute
each step in the intended workspace against a known-benign CLI case, a
broker/FOCI case, a no-precedent user, and an empty tenant baseline, and
record runtimes. Tenant runtime validation is currently outstanding.

References:

- [SigninLogs schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs)
- [AuditLogs schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/auditlogs)
- [Microsoft Entra authentication flows](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-authentication-flows)
- [Microsoft analysis of Storm-2372 device-code phishing](https://www.microsoft.com/en-us/security/blog/2025/02/13/storm-2372-conducts-device-code-phishing-campaign/)
