# 06-email

Email investigation family. Scope: phishing, malicious attachment and
URL delivery, post-delivery actions, inbox rule abuse triggered by
email activity, and mail-flow anomalies.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | TODO — empty stub. |
| `narrative-gen.kql` | narrative | TODO — not yet authored. |

## Starting entities

- TODO (likely: recipient UPN, sender address, subject fragment,
  `NetworkMessageId`, URL / click id).

## Required tables

- TODO (likely: `EmailEvents`, `EmailUrlInfo`, `EmailAttachmentInfo`).

## Optional tables

- TODO (likely: `UrlClickEvents` — **optional enrichment** for Safe
  Links click telemetry; `EmailPostDeliveryEvents` — **optional
  enrichment** for ZAP / manual remediation trail).

## Done criteria

- TODO. Every recipient enumerated; every click or attachment
  detonation classified; any follow-on sign-in activity checked
  against the 01-sign-in triage engine; remediation actions (ZAP,
  soft-delete, block sender) recorded.

## Validation — test cases

1. **Known benign — TODO.** Legitimate newsletter to multiple
   recipients with no clicks and no remediation.
2. **Ambiguous — TODO.** Phishing-style lure delivered to inbox with
   one click but no credential submission and no downstream sign-in
   anomaly.
3. **Known bad / clearly suspicious — TODO.** Credential-harvest
   phish delivered to multiple users with clicks and a downstream
   sign-in from a new country inside the hour.
