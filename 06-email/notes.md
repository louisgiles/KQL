# 06-email

Email investigation family. Scope: phishing, malicious attachment and
URL delivery, sender / authentication posture, post-delivery actions
(ZAP / soft-delete), Safe Links click telemetry, recipient spread and
campaign correlation, and optional endpoint follow-up for clicks that
crossed into the host.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `quick-dive.kql` | quick-triage | Fast single-message decision gate. One-row-ish output covering sender / domain / recipient prevalence, authentication, URL / attachment context, delivery / remediation, and click exposure. Separates threat concern from exposure concern. |
| `deep-dive.kql` | analysis | Eleven-section toggled evidence engine. Anchors on a single target email, expands into auth & sender infrastructure, delivery / remediation, sender-domain / recipient baselines, similar-message spread, URL prevalence, attachment prevalence, click activity, post-delivery events, optional endpoint correlation, and a final risk-signals verdict block. |
| `narrative-gen.kql` | narrative | Dash-prefixed paste-ready ticket note summarising sender / auth posture, prevalence, URLs, attachments, delivery / remediation, clicks, threat concern, and exposure concern. |

## Purpose

Triage a Microsoft 365 Defender email alert end to end. Anchor on a
`NetworkMessageId` (or sender / recipient / subject fragment), check
whether the message is part of a wider campaign, decide whether the
content represents a real threat, and separately decide whether any
recipient actually clicked or downloaded.

## Starting entities

- **`NetworkMessageId`** — primary anchor. Both deep-dive and
  narrative-gen prefer this; quick-dive will fall back to the
  sender / recipient / subject combination if the id is unknown.
- **Sender address** — `SenderToCheck` against `SenderFromAddress`.
- **Recipient address** — `RecipientToCheck` against
  `RecipientEmailAddress`.
- **Subject fragment** — `SubjectToCheck` against `Subject`.

## Variables

| Variable | Default | Role |
|---|---|---|
| `TargetNetworkMessageId` *(narrative-gen, quick-dive)* / `NetworkMessageIdToCheck` *(deep-dive)* | `""` | Primary anchor. |
| `SenderToCheck` / `RecipientToCheck` / `SubjectToCheck` | `""` | Fallback scope filters. |
| `SearchLookback` | `30d` | How far back to look for the target message. |
| `BaselineWindow` | `90d` | Historical baseline window for sender / domain / recipient / URL / attachment prevalence. |
| `BaselineLabel` | `"90d"` | Human label used inside the narrative text. |
| `CampaignWindow` *(deep-dive)* | `7d` | Window for similar-message and URL / attachment campaign spread. |
| `EndpointCorrelationWindow` *(deep-dive)* | `2h` | Window for the optional endpoint correlation section. |
| `Run*` toggles *(deep-dive)* | `true` (except `RunEndpointCorrelation` which defaults `false`) | Toggle each deep-dive section. |

## Required tables

- **`EmailEvents`** — **Required**. Primary source for every
  query. Carries `NetworkMessageId`, sender / recipient /
  authentication fields, delivery action and location, threat types,
  and the join key into the other email tables. Uses
  `column_ifexists` for fields that vary by tenant schema version.

## Optional tables

- **`EmailAttachmentInfo`** — **Optional enrichment**. Attachment
  metadata (`FileName`, `FileType`, `SHA256`) joined on
  `NetworkMessageId`. Drives the attachment prevalence and campaign
  spread sections.
- **`EmailUrlInfo`** — **Optional enrichment**. URL metadata
  (`Url`, `UrlDomain`, `UrlCount`) joined on `NetworkMessageId`.
  Drives URL prevalence and campaign spread.
- **`EmailPostDeliveryEvents`** — **Optional enrichment**.
  ZAP / manual remediation trail. Joined on `NetworkMessageId`.
- **`UrlClickEvents`** — **Optional enrichment**. Safe Links click
  telemetry. Joined on `Url` / `UrlDomain` and recipient.
- **`DeviceNetworkEvents` / `DeviceFileEvents` /
  `DeviceProcessEvents`** — **Optional enrichment**, deep-dive only,
  gated by `RunEndpointCorrelation = true`. Used when a recipient
  clicked and the investigation needs to see whether the host
  followed up with a request to the same domain, a file write, or
  a process spawn within `EndpointCorrelationWindow`.

## Done criteria

1. Target message identified (by `NetworkMessageId`, or unambiguously
   by sender + recipient + subject + time).
2. Sender / authentication posture reviewed: SPF, DKIM, DMARC, and
   compauth from `AuthenticationDetails`; sender IP and display-name
   spoofing patterns checked against the sender-domain baseline.
3. Delivery / remediation reviewed: `DeliveryAction`,
   `DeliveryLocation`, `ThreatTypes`, `ThreatNames`,
   `OrgLevelAction`, post-delivery ZAP / manual actions.
4. Prevalence reviewed: sender, sender domain, sender IP, display
   name, and recipient pairing against `BaselineWindow`.
5. Campaign spread reviewed: similar-message count over
   `CampaignWindow`, distinct recipients, URL and attachment spread
   across the org.
6. URL and attachment analysis reviewed: tenant rarity, click
   exposure (`UrlClickEvents`), attachment hash prevalence.
7. Click exposure separated from threat concern: a benign-looking
   message that was clicked still produces an exposure concern; a
   high-threat message that nobody clicked still produces a threat
   concern.
8. Where any recipient clicked, the recipient's downstream sign-in
   activity has been checked against the 01-sign-in triage engine.
   Where the click crossed onto the host, `RunEndpointCorrelation`
   has been enabled and the result reviewed.
9. The event has been mapped to one of the four closure buckets
   (**benign**, **precautionary benign**, **review required**,
   **suspicious / escalate**).
10. The narrative-gen output has been pasted into the ticket.

## Validation — test cases

> TODO: replace the placeholders below with real anonymised examples
> pulled from completed investigations.

1. **Known benign — TODO.** Legitimate newsletter to multiple
   recipients, high sender-domain prevalence, no clicks, no
   remediation, SPF/DKIM/DMARC pass.
   *Expected:* quick-dive returns "Likely benign — high-prevalence
   sender, no exposure"; deep-dive shows zero risk signals;
   narrative-gen converges benign with low threat / low exposure.
2. **Ambiguous — TODO.** Phishing-style lure delivered to inbox
   with one click but no credential submission and no downstream
   sign-in anomaly. Sender domain new to the org but auth passes.
   *Expected:* quick-dive surfaces `NEW_SENDER_DOMAIN` + `CLICKED`;
   deep-dive flags review-required; narrative-gen separates
   threat concern ("moderate — new domain, lure pattern") from
   exposure concern ("one click, no downstream impact").
3. **Known bad / clearly suspicious — TODO.** Credential-harvest
   phish delivered to multiple recipients with clicks, followed
   inside the hour by a sign-in from a new country for one of the
   clickers.
   *Expected:* deep-dive shows campaign spread + click exposure +
   endpoint correlation (if enabled); narrative-gen flags high
   threat concern and high exposure concern; pivot to 01-sign-in.
