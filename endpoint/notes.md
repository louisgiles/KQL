# endpoint (≈ 05-endpoint)

Endpoint triage family. This is the contract exception: instead of a single
`deep-dive.kql`, the family ships three parallel deep dives, one per
Defender for Endpoint event table.

## Use case

An analyst arrives with a Defender/MDE alert: a device name, an entity
(filename, hash, command fragment, URL, IP), and an alert timestamp. The
three queries walk the process, file, and network dimensions of that alert
inside a ±15 minute window.

## Starting entities

- Device name (primary)
- Entity — one of: process name, command fragment, filename, SHA256, URL,
  domain, or IP
- Alert timestamp (ISO 8601)

## Queries in this family

| File | Role | Notes |
|---|---|---|
| `process-events` | deep-dive (analysis) — "what executed?" | `DeviceProcessEvents`, with BenignFlag suppression for Defender/WU/svchost/telemetry noise. |
| `file-events` | deep-dive (analysis) — "what appeared or changed?" | `DeviceFileEvents`, with BenignFlag suppression for Defender definition updates, WU staging, Prefetch, event logs. |
| `network-events` | deep-dive (analysis) — "where did it connect?" | `DeviceNetworkEvents`, with BenignFlag suppression for Microsoft telemetry, WU, OCSP/CRL, Office. |

No `narrative-gen.kql` exists yet for this family. Endpoint narratives are
currently written by hand from the three deep-dive outputs. A dedicated
closure-note generator is a planned addition.

## Data dependencies

| Table | Tag | Used by |
|---|---|---|
| `DeviceProcessEvents` | **Required** | process-events |
| `DeviceFileEvents` | **Required** | file-events |
| `DeviceNetworkEvents` | **Required** | network-events |

No optional-enrichment joins in the current deep dives. `DeviceEvents`,
`DeviceImageLoadEvents`, and `DeviceRegistryEvents` are candidates for
future enrichment but are currently **Avoid as hard dependency** —
coverage varies by onboarding profile.

## Done criteria

Triage is finished when:

1. Every non-BenignFlag row in each of the three deep dives has been
   classified or escalated.
2. The initiating process chain has been walked back to a user-initiated
   parent or an identified service.
3. Any file written has been accounted for (origin URL, originating IP,
   hash reputation).
4. Any network destination has been classified against known-good infra,
   or escalated for reputation lookup.
5. The alert has been mapped to one of the four closure buckets.

## Closure language

- **Benign** — every non-Microsoft-signed row is accounted for by a known
  admin, user, or management agent.
- **Precautionary benign** — unusual but explainable activity (e.g. a
  one-off admin script from a trusted operator, an expected deployment).
- **Review required** — unfamiliar binary launched by a legitimate parent,
  LOLBin usage without clear context, new outbound destination from a
  non-browser process.
- **Suspicious / escalate** — unsigned binary from user temp, encoded
  PowerShell, C2-style beaconing pattern, credential theft tool
  signatures, persistence mechanism writes.

## Validation — test cases

1. **Known benign.** Defender definition update window on a healthy
   endpoint. All process, file, and network rows should BenignFlag to
   the bottom; top of each deep dive should be empty or near-empty.
2. **Ambiguous.** Developer running ad-hoc PowerShell against a public
   API from a managed laptop during working hours. Process deep dive
   shows `powershell.exe` with an unfamiliar command line; network
   deep dive shows an unknown-but-plausible destination.
3. **Known bad / clearly suspicious.** LOLBin execution (e.g.
   `mshta.exe` or `rundll32.exe` spawning `cmd.exe`) followed by a
   file write to `\Users\Public\` and an outbound connection to a
   non-Microsoft IP. All three deep dives should light up with
   non-benign rows at the top.

## Contract compliance notes

- Queries use a top-of-file `let` block — compliant with the
  parameterisation rule.
- Header comments describe purpose and usage but do not yet follow the
  full contract field block (`name`, `starting_entities`,
  `required_tables`, etc.). Retrofit pending.
- File names omit the `.kql` extension. Extension normalisation pending.
- No `narrative-gen.kql` yet; this is a known gap for this family.
