# 01-sign-in

Sign-in investigation family. Reference family — the shape every other
family should grow into.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | Deep-dive triage of a specific user, IP, or device with a weighted risk score across nine sign-in signals. |
| `narrative-gen.kql` | narrative | Produces a single-row closure-ready narrative summarising a user's sign-in posture, IP reputation, device posture, MFA method and audit trail. |

Supporting queries also live in this folder
(`sign-in-baseline-behaviour`, `failed-auth-pattern`,
`mfa-authentication-finder`, `anomalous-token-replay`,
`privileged-account-activity-monitor`, `service-principal-auth-tracker`).
They are not on the contract's `deep-dive.kql` / `narrative-gen.kql` path
but are called from the same triage flow.

## Starting entities

- UPN (primary — both queries key on `UserIdentityCheck`)
- IP address (`IPtoCheck` — deep-dive only)
- Device display name / `DeviceDetail` substring (`DeviceDetailtoCheck` — deep-dive only)

## Required tables

- `SigninLogs` — both queries break without it.

## Optional tables

- `IdentityInfo` — **optional enrichment**. Used for job title,
  assigned roles, manager, and identity-level risk level. Both queries
  `leftouter`-join on it; the output degrades gracefully to "N/A"
  values when rows are missing.
- `AuditLogs` — **optional enrichment**. Deep-dive uses it for
  new-starter detection (`Add user` operations in the last 90d).
  Narrative-gen uses it for the 24h MFA audit trail. Both are
  left-joined and the output accommodates empty results.

## Done criteria

1. Every elevated risk-score row in `deep-dive.kql` has been explained
   (known travel, device refresh, known-new-IP from an approved
   network) or escalated.
2. The most recent sign-in has been classified against the four
   closure buckets (**benign**, **precautionary benign**, **review
   required**, **suspicious / escalate**).
3. Source IP has been checked against org-wide history
   (`DaysIpSeenInOrg`) and user history (`DaysIpSeenUser`).
4. The 24h MFA audit trail has been reviewed via `narrative-gen.kql`
   (or directly in `AuditLogs`) and any registration or deletion
   event is accounted for.
5. The narrative-gen output has been pasted into the ticket.

## Validation — test cases

> TODO: replace the placeholders below with real anonymised examples
> pulled from completed investigations.

1. **Known benign — TODO.** Daily-driver UPN, single managed device,
   org-familiar IP, MFA satisfied, no audit-log churn.
   *Expected:* deep-dive returns `🟢 LIKELY BENIGN`; narrative-gen's
   IP-reputation line reads "high-freq organisational IP addresses".
   *Fill in:* UPN placeholder, IP, device, exact `TimeToCheck`.

2. **Ambiguous — TODO.** UPN signing in from a residential IP new to
   the org on an unmanaged personal device, MFA satisfied.
   *Expected:* deep-dive lands in `🟡 LOW-RISK` or `🟠 MEDIUM-RISK`
   with `IP_NEW_TO_ORG` and `UNMANAGED_DEVICE` flags; narrative-gen's
   IP-reputation line reads "ALERT: Most recent IP ... is NEW to the
   organisation".
   *Fill in:* UPN placeholder, IP, device, timestamp, travel context.

3. **Known bad / clearly suspicious — TODO.** UPN with a MFA
   registration change inside the 24h `MFAAuditWindow` followed by a
   sign-in from a new country with a `tokenIssuerAnomaly` risk event.
   *Expected:* deep-dive lands `🔴 HIGH-RISK`; narrative-gen's MFA
   audit trail line reads "ALERT: N MFA modification(s) in audit
   logs".
   *Fill in:* UPN placeholder, IP, country, audit-log operation name,
   timestamp.

## Babbl33r identity-posture section 0.2.0

`Babbl33r.kql` is the bounded Stage 20 identity-posture section. It emits
the shared 11-column evidence schema and at most 23 rows: status, summary, up
to 20 findings, and an optional truncation sentinel.

The three public inputs are `TargetUPN`, `AnchorTime`, and the immutable
`AssessmentCutoffUTC`. Event membership is based on
`coalesce(CreatedDateTime, TimeGenerated)`; historical availability is based
on `ingestion_time()`. Rows unavailable at the assessment cutoff are excluded,
and a missing ingestion timestamp makes `Evidence.section_state` non-ready.
Request/correlation identifiers are preferred over sign-in ID so multi-line MFA
records collapse to one authentication flow. Zero or multiple eligible UserIds
for the supplied UPN, or any fallback-keyed flow, makes the section non-ready.

Agentic callers must supply all inputs explicitly. The runner's indexed
`TimeGenerated` range must cover `[AnchorTime - 93d, AnchorTime + 2d)`;
`max_rows` must be at least 23. A consumer must prefer
`Evidence.section_state` over `baseline_state` and treat either
`RecordType == "truncation"` or `omitted_findings > 0` as incomplete
evidence. Do not expose this query to an actioning model until its manifest
pins the exact blob, its maximum result-character budget is measured, and the
workspace gates below pass.

### Validation cases

1. **Point-in-time replay.** Add a pre-anchor event ingested after the frozen
   cutoff and a post-anchor sign-in for the same UPN with a different UserId.
   Expected: neither affects the selected UserId, baseline, score, or emitted
   evidence for the frozen run. Two distinct pre-anchor, cutoff-eligible UserIds
   must instead report `multiple_user_ids_for_upn`.
2. **Authentication flow grouping.** Use a known multi-line MFA sequence with
   shared `OriginalRequestId` or `CorrelationId`, plus a row missing all
   stable identifiers. Expected: the MFA sequence is one flow; the missing-key
   case reports `fallback_flow_identity` and remains ineligible.
3. **Coverage and bounds.** Use a ready baseline with no score-window flows,
   then a case with more than 20 noteworthy flows. Expected: states are
   `no_score_window_flows` and `truncated`, respectively; the latter also
   emits a Priority-3 truncation row and neither is closure-eligible.

Before promotion, parse the file in CI, compile and execute it against a real
SigninLogs workspace, confirm `ingestion_time()` is populated, validate all
referenced columns, measure worst-case rows/characters, and demonstrate
runtime <=100 seconds with p95 <=60 seconds on representative high-volume
users. Until those checks are recorded, use is calibration-only.
