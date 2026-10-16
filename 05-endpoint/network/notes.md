# 05-endpoint / network

Network-anchored sub-family of the endpoint investigation family.
Scope: outbound and inbound network alerts from
`DeviceNetworkEvents` — where the device connected, which process
initiated it, how normal the destination is, what nearby behaviour
accompanied it.

Network telemetry is weak on intent. Queries in this sub-family do
not call activity "C2" or "exfiltration"; they surface destination
normality, process-destination pairing, traffic-shape signals, and
nearby behaviour, and leave the verdict to the analyst.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `quick-dive.kql` | quick-triage | Fast prevalence-first decision gate. One-row output with destination normality, process-destination relationship, cautious traffic-shape classification, nearby behaviour counts. |
| `deep-dive.kql` | analysis | Seven togglable sections: target network event, destination prevalence, process-destination relationship, initiating-process context, related network activity in the window, nearby behaviour, traffic-shape and risk signals. |
| `narrative-gen.kql` | narrative | Dash-prefixed ticket note summarising traffic shape, prevalence, process-destination relationship, nearby behaviour, and a cautious determination line. |

## Anchor model

Deep-dive supports two anchor modes:

- **`AnchorMode = "alert"`** *(default)* — centre the window on
  `AlertTime`.
- **`AnchorMode = "network_origin"`** — look up the first matching
  network event for the target within a 90d lookback and re-anchor
  on that timestamp. Use when the alert fires on a downstream event
  (e.g. periodic beacon match) well after the first connection.

Quick-dive and narrative-gen are alert-anchored only.

## Composite keying

Process joins (initiating-process metadata and chain context) use
composite `(InitiatingProcessId, InitiatingProcessCreationTime)`
keys. Defends against PID reuse across the forward window. Never
join on bare `InitiatingProcessId`.

## Starting entities

- **`AlertTime`** — datetime from the alert.
- **`DeviceName`** (`HostToCheck`).
- **`RemoteUrl`** (`RemoteUrlToCheck`).
- **`RemoteIP`** (`RemoteIPToCheck`).
- **`RemotePort`** (`RemotePortToCheck`).
- **`InitiatingProcessFileName`** (`ProcessNameToCheck`).
- **`InitiatingProcessSHA256`** (`ProcessSHA256ToCheck`).
- **`InitiatingProcessId`** (`ProcessIdToCheck`) — paired with `InitiatingProcessCreationTime` for the composite key.
- **`CommandLine` substring** (`CommandLineToCheck`).

## Variables

| Variable | Default | Role |
|---|---|---|
| `AlertTime` | `2026-01-01T00:00:00Z` | Centre of the event window. |
| `AnchorMode` *(deep-dive)* | `"alert"` | `alert` or `network_origin`. |
| `TimeToCheck` | `10m` | Window either side of the anchor. |
| `BaselineWindow` / `BaselineLabel` | `90d` / `"90d"` | Destination prevalence baseline. |
| `ForwardWindow` *(deep-dive, quick-dive, narrative-gen)* | `24h` (deep-dive) / `1h` (others) | Forward window for related-network and nearby-behaviour scans. |
| `AncestryLookback` *(deep-dive)* | `24h` | Backward window for initiating-process chain context. |
| `Run*` toggles *(deep-dive)* | `true` | `RunTargetNetworkEvent`, `RunDestinationPrevalence`, `RunProcessDestinationRelationship`, `RunInitiatingProcessContext`, `RunRelatedNetworkActivity`, `RunNearbyBehaviour`, `RunTrafficShapeAndRiskSignals`. |

## Required tables

- **`DeviceNetworkEvents`** — **Required**. Primary source. Every
  query breaks without it.

## Optional tables

- **`DeviceProcessEvents`** — **Optional enrichment**, deep-dive
  only. Initiating-process metadata (signing, parent, command line)
  and lightweight chain context via composite key.
- **`DeviceFileEvents`** — **Optional enrichment**. Nearby file
  activity from the initiating process in the forward window.
- **`DeviceRegistryEvents`** — **Optional enrichment**. Nearby
  registry activity from the initiating process.
- **`DeviceEvents`** — **Optional enrichment**. MDE response
  signals (`SmartScreen*`, `ExploitGuardNetworkProtectionBlocked`),
  plus persistence surfaces.

## Done criteria

1. Target network event(s) located in `NetworkScope` /
   `DeviceNetworkEvents` within `AlertTime ± TimeToCheck`. Anchor
   mode chosen explicitly when the alert fired late.
2. Destination prevalence checked against `BaselineWindow`: how
   many devices have connected to this `RemoteIP` / `RemoteUrl`
   tenant-wide, how often, over how many days.
3. Process-destination relationship classified: is this
   `InitiatingProcessFileName` known to talk to this destination,
   or is the pairing new.
4. Initiating-process chain reviewed (deep-dive
   `RunInitiatingProcessContext`): parent, command line, signing.
5. Related network activity in the forward window walked: did the
   same destination get hit again, did the same process reach
   elsewhere.
6. Nearby file / registry / MDE behaviour reviewed: did the
   connection accompany a file write, registry persistence, or
   MDE response.
7. Traffic-shape signals reviewed cautiously: long-running,
   periodic, high-byte-count, off-hours.
8. Each finding mapped to one of the four closure buckets
   (**benign**, **precautionary benign**, **review required**,
   **suspicious / escalate**). The query refuses to commit to
   "C2" or "exfil" — that's the analyst's call.
9. The narrative-gen output has been pasted into the ticket.

## Validation — test cases

> TODO: replace the placeholders below with real anonymised examples
> pulled from completed investigations.

1. **Known benign — TODO.** Browser process connects to a
   high-prevalence Microsoft endpoint during working hours from a
   managed laptop.
   *Expected:* destination prevalence high, process-destination
   pairing well-established, no nearby file or registry activity;
   quick-dive closes.
2. **Ambiguous — TODO.** Custom in-house tool connects to a
   business-partner API endpoint that is new to the tenant.
   *Expected:* destination prevalence low; process-destination
   pairing new; no MDE response; deep-dive lands review-required
   with a prompt to confirm the business context.
3. **Known bad / clearly suspicious — TODO.** Recently-written
   binary in `\Users\Public\` connects out to a non-Microsoft IP
   on a non-standard port. Subsequent periodic connections at
   regular intervals.
   *Expected:* destination prevalence near zero;
   process-destination pairing new; traffic shape periodic;
   nearby file-write present; `ExploitGuardNetworkProtectionBlocked`
   or `SmartScreen*` may fire; deep-dive lands escalate.
