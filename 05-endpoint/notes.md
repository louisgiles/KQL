# 05-endpoint

Endpoint triage family. Contract exception: ships three parallel deep
dives (process, file, network) instead of a single `deep-dive.kql`.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `process-events.kql` | analysis | "What executed?" — process chain around an alert timestamp. |
| `file-events.kql` | analysis | "What appeared or changed?" — file creation/modification around an alert. |
| `network-events.kql` | analysis | "Where did it connect?" — outbound/inbound network around an alert. |
| `narrative-gen.kql` | narrative | TODO — not yet authored. |

## Starting entities

- Device name (primary)
- Entity — process name, command fragment, filename, SHA256, URL,
  domain, or IP
- Alert timestamp (ISO 8601)

## Required tables

- `DeviceProcessEvents` — **required** by `process-events.kql`.
- `DeviceFileEvents` — **required** by `file-events.kql`.
- `DeviceNetworkEvents` — **required** by `network-events.kql`.

## Optional tables

- TODO. Candidates for future enrichment (`DeviceEvents`,
  `DeviceImageLoadEvents`, `DeviceRegistryEvents`) would currently be
  tagged **avoid as hard dependency** — coverage varies by onboarding
  profile.

## Done criteria

- TODO. Every non-BenignFlag row across the three deep dives is
  classified or escalated; initiating process chain walked back to a
  user or service; file writes accounted for (origin URL, IP, hash);
  network destinations classified.

## Validation — test cases

1. **Known benign — TODO.** Defender definition update window on a
   healthy endpoint — all rows BenignFlag to the bottom.
2. **Ambiguous — TODO.** Developer ad-hoc PowerShell against a public
   API from a managed laptop during working hours.
3. **Known bad / clearly suspicious — TODO.** LOLBin chain
   (`mshta.exe` or `rundll32.exe` spawning `cmd.exe`) followed by a
   write to `\Users\Public\` and an outbound to a non-Microsoft IP.
