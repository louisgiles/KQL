# 05-endpoint / process

Process-anchored sub-family of the endpoint investigation family.
Scope: process-based Defender alerts — what ran, who launched it,
what its command line shape looked like, what it spawned, and what
file / network / registry / MDE activity the chain produced.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `quick-dive.kql` | quick-triage | Fast process decision gate. One-row output with process identity, Defender / AMSI alert evidence, parent and command-line shape, tenant prevalence, nearby behaviour counts, cautious flags. |
| `deep-dive.kql` | analysis | Six togglable sections: process lifecycle, command-line analysis, two-level chain walk (grandparent → parent → target → child → grandchild), file activity by chain, network reach by chain, MDE actions. |
| `narrative-gen.kql` | narrative | Chain-aware, dash-prefixed ticket note. Five sections: identity, top-to-bottom chain walk with per-node signal counts, command-line shape, MDE response, closure signals. Operation rotation deliberately omitted — process incidents are chain-shaped, not operation-shaped. |

## Anchor model

Both deep-dive and narrative-gen support two anchor modes:

- **`AnchorMode = "alert"`** *(default)* — centre the window on
  `AlertTime`.
- **`AnchorMode = "process_origin"`** — look up the earliest matching
  `ProcessCreated` event for the target within a 90d lookback and
  re-anchor the window on that timestamp. Use when the alert fires
  on a downstream event well after the process started.

## Composite keying

Every join across `DeviceProcessEvents`, `DeviceFileEvents`,
`DeviceNetworkEvents`, `DeviceRegistryEvents`, and `DeviceEvents`
uses **composite `(ProcessId, ProcessCreationTime)` keys**, encoded
as `strcat(tostring(ProcessId), "|", tostring(ProcessCreationTime))`.
This defends against PID reuse across the 24h forward window. Never
join on bare `ProcessId` in this sub-family.

## Starting entities

- **`AlertTime`** — datetime from the alert.
- **`DeviceName`** (`HostToCheck`) — primary scope.
- **`ProcessName`** (`ProcessNameToCheck`) — file name match.
- **`SHA256`** (`ProcessSHA256ToCheck`) — preferred process anchor.
- **`ProcessId`** (`ProcessIdToCheck`) — paired with `ProcessCreationTime` for the composite key.
- **`CommandLine` substring** (`CommandLineToCheck`) — fragment match against `ProcessCommandLine`.
- **`Account`** (`AccountToCheck`, quick-dive only) — initiating account name.

At least one of `ProcessNameToCheck` / `ProcessSHA256ToCheck` /
`ProcessIdToCheck` / `CommandLineToCheck` is required to scope the
target.

## Variables

| Variable | Default | Role |
|---|---|---|
| `AlertTime` | `2026-01-01T00:00:00Z` | Centre of the event window. |
| `AnchorMode` *(deep-dive, narrative-gen)* | `"alert"` | `alert` or `process_origin`. |
| `TimeToCheck` | `5m` (deep-dive, narrative-gen) / `10m` (quick-dive) | Window either side of the anchor. |
| `AncestryLookback` *(deep-dive, narrative-gen)* | `24h` | How far back to walk for parent / grandparent creation events. |
| `ProcessLookupBack` *(quick-dive)* | `2h` | Backward window for the target-process lookup. |
| `BaselineWindow` / `BaselineLabel` *(quick-dive)* | `90d` / `"90d"` | Tenant prevalence baseline. |
| `ForwardWindow` *(quick-dive)* | `1h` | Forward window for nearby-behaviour counts. |
| `Run*` toggles *(deep-dive)* | `true` | `RunProcessLifecycle`, `RunCommandLineAnalysis`, `RunChainWalk`, `RunFileActivityByChain`, `RunNetworkReachByChain`, `RunMdeActions`. |

## Required tables

- **`DeviceProcessEvents`** — **Required**. Primary source. Every
  query breaks without it.

## Optional tables

- **`DeviceFileEvents`** — **Optional enrichment**. Per-node file
  activity counts (`FileCount`), file writes attributed to chain
  processes via composite-key join.
- **`DeviceNetworkEvents`** — **Optional enrichment**. Per-node
  network reach counts (`NetCount`), destinations attributed to
  chain processes.
- **`DeviceRegistryEvents`** — **Optional enrichment**. Per-node
  registry write counts (`RegCount`), persistence keys touched by
  chain processes.
- **`DeviceEvents`** — **Optional enrichment**. MDE response
  signals: `AntivirusDetection`, `AsrProcessBlocked`,
  `AsrLsassBlocked`, `SmartScreen*`, `ExploitGuardNetworkProtectionBlocked`,
  `TamperingAttempt`, `ProcessBlockedByPolicy`, plus persistence
  surfaces (services, scheduled tasks). Also carries Defender /
  AMSI alert evidence used as the quick-dive anchor.

## Done criteria

1. Anchor located: target process found in `ProcessScope`, with
   `AnchorMode` chosen explicitly when the alert fired late.
2. Chain walked: grandparent and parent identified via
   `AncestryLookback`; children and grandchildren collected in the
   forward window. Single-node chains explicitly acknowledged.
3. Per-node signal counts read: file, network, registry counts for
   each chain node; encoded / download-cradle / AMSI-bypass /
   obfuscation / length-anomaly command-line indicators surfaced.
4. MDE response reviewed: any of the seven response action types
   above plus early-termination explained.
5. Each finding mapped to one of the four closure buckets
   (**benign**, **precautionary benign**, **review required**,
   **suspicious / escalate**).
6. The narrative-gen output has been pasted into the ticket.

## Validation — test cases

> TODO: replace the placeholders below with real anonymised examples
> pulled from completed investigations.

1. **Known benign — TODO.** Vendor-signed installer spawns `msiexec`
   and a few benign children during a managed software-deploy window.
   *Expected:* chain is shallow, no command-line indicators, no MDE
   actions; quick-dive closes; narrative-gen converges benign.
2. **Ambiguous — TODO.** Developer ad-hoc PowerShell with an
   encoded-command flag against a public API from a managed laptop
   during working hours.
   *Expected:* `HasEncodedCommand` fires, chain shows
   `pwsh.exe`-spawned cmd, no MDE response, no file writes;
   deep-dive lands review-required.
3. **Known bad / clearly suspicious — TODO.** LOLBin chain
   (`mshta.exe` or `rundll32.exe` spawning `cmd.exe`) with a
   download-cradle command-line, followed by a file write to
   `\Users\Public\` and an outbound to a non-Microsoft IP.
   *Expected:* `HasDownloadCradle` + `_anyNetwork` + `_anyFileWrite`
   + likely `AsrProcessBlocked` or `AntivirusDetection`; deep-dive
   lands escalate.
