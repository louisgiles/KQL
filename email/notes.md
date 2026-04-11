# email (≈ 06-email)

Email investigation family. Scope: phishing, malicious attachment and
URL delivery, post-delivery actions, inbox rule abuse triggered by email
activity, and mail-flow anomalies.

## Use case

An analyst arrives with an email signal: a user-reported phish, a
Defender for Office 365 alert, a post-delivery ZAP event, or a URL
click on a detonated link. This family walks the message through
delivery, recipient exposure, click telemetry, and follow-on actions.

## Starting entities

- Recipient UPN
- Sender address
- Subject fragment or message id
- NetworkMessageId
- URL / click id

## Queries in this family

| File | Role | Notes |
|---|---|---|
| `email-investigation-deep-dive.kql` | deep-dive (analysis) | **Stub — empty.** See compliance notes below. |

No `narrative-gen.kql` yet.

## Data dependencies

Planned once the deep dive is authored:

| Table | Tag |
|---|---|
| `EmailEvents` | **Required** |
| `EmailUrlInfo` | **Required** — URL pivot. |
| `EmailAttachmentInfo` | **Required** — attachment pivot. |
| `UrlClickEvents` | **Optional enrichment** — Safe Links click telemetry. |
| `EmailPostDeliveryEvents` | **Optional enrichment** — ZAP / manual remediation trail. |

## Done criteria

Triage is finished when:

1. Every recipient of the message has been enumerated.
2. Every delivered click or attachment detonation has a classification.
3. Any follow-on sign-in activity from clicked-through users has been
   checked against the identity family's triage engine.
4. Remediation actions (ZAP, soft-delete, block sender) have been
   recorded.
5. The event has been mapped to one of the four closure buckets.

## Closure language

- **Benign** — expected marketing or transactional mail, no
  credential-harvest indicators, no recipient clicks.
- **Precautionary benign** — suspicious-looking but filtered or
  ZAP'd before any user interaction.
- **Review required** — delivered phishing-style mail with clicks but
  no credential submission or downstream sign-in anomaly.
- **Suspicious / escalate** — successful credential harvest indicator,
  attachment detonation with malicious verdict, or any recipient who
  clicked and then shows downstream identity-layer anomalies.

## Validation — test cases

1. **Known benign.** Legitimate newsletter to multiple recipients, no
   clicks, no remediation.
2. **Ambiguous.** Phishing-style lure delivered to inbox, one recipient
   click, no credential submission detected, no downstream sign-in
   anomaly.
3. **Known bad / clearly suspicious.** Credential-harvest phish
   delivered to 20 users, three clicks, one downstream sign-in from a
   new country within the hour.

## Contract compliance notes

- `email-investigation-deep-dive.kql` is an empty 1-byte placeholder.
  It should be authored to the contract or flagged for deletion.
- No `narrative-gen.kql` exists — author or flag.
