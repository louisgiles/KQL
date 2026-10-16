# 05-endpoint / file

File-anchored sub-family of the endpoint investigation family. Scope:
file-based Defender alerts — what appeared on disk, who wrote it,
whether it ran, what it spawned, what network / registry / persistence
activity its creator and descendants produced, and what MDE response
fired.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `quick-dive.kql` | quick-triage | Fast decision gate. One-row-per-device output with file identity, Defender evidence, creator-process context, tenant prevalence, environment spread, nearby behaviour counts via creator `ProcKey`, cautious flags, score. |
| `deep-dive.kql` | analysis | Twelve togglable sections: file lifecycle, origin, creator chain, metadata (including signing via `DeviceFileCertificateInfo`), execution status, network reach, registry writes, sibling files, MDE actions, two-level creator ancestry (with row-projection fallback), two-level executed descendants, persistence creation by chain, preceding browser / script-host context. |
| `narrative-gen.kql` | narrative | Operation-aware dash-prefixed ticket note. Detects which lifecycle operation the target file underwent (`executed_payload`, `blocked_at_write`, `staged_inert`, `modified`, `renamed`, `deleted`) and rotates the projection accordingly. Shared file-identity header + arm-specific lifecycle shape + verdict-signals block (no committed verdict). |

## Anchor model

Both deep-dive and narrative-gen support two anchor modes:

- **`AnchorMode = "alert"`** *(default)* — centre the window on
  `AlertTime`.
- **`AnchorMode = "file_origin"`** — look up the `FileCreated`
  event for the target file within a 90d lookback and re-anchor on
  that timestamp. Use when the alert fires on a downstream event
  days or weeks after the actual file lifecycle (recycle-bin
  deletion, scheduled-scan match).

## Composite keying

Every join across `DeviceProcessEvents`, `DeviceNetworkEvents`,
`DeviceRegistryEvents`, and `DeviceEvents` uses composite
`(ProcessId, ProcessCreationTime)` keys for creator and forward-chain
(executed, child, grandchild) processes. Defends against PID reuse
across the 24h forward window.

Ancestry walks two levels back: **level 0** (creator) is always
available via row-projection from `FileScope`; **level 1** (parent)
and **level 2** (grandparent) depend on the creator's and parent's
creation events falling within `AncestryLookback`.

## Starting entities

- **`AlertTime`** — datetime from the alert.
- **`DeviceName`** (`HostToCheck`) — primary scope.
- **`FileName`** (`FileNameToCheck`).
- **`SHA256`** (`SHA256ToCheck`) — preferred file anchor.
- **`FolderPath`** (`FolderPathToCheck`).

At least one of `FileNameToCheck` / `SHA256ToCheck` /
`FolderPathToCheck` is required to scope the target.

## Variables

| Variable | Default | Role |
|---|---|---|
| `AlertTime` | `2026-01-01T00:00:00Z` | Centre of the event window. |
| `AnchorMode` *(deep-dive, narrative-gen)* | `"alert"` | `alert` or `file_origin`. |
| `TimeToCheck` | `5m` (deep-dive, narrative-gen) / `10m` (quick-dive) | Window either side of the anchor. |
| `AncestryLookback` *(deep-dive, narrative-gen)* | `24h` | How far back to walk for parent / grandparent creation events. |
| `PrecedingContextLookback` *(narrative-gen)* | `1h` | Window before the anchor for browser / email / script-host context. |
| `ForwardWindow` *(quick-dive)* | `1h` | Forward window for nearby-behaviour counts. |
| `BaselineWindow` / `SpreadLookback` / `BaselineLabel` *(quick-dive)* | `90d` / `90d` / `"90d"` | Tenant prevalence and environment-spread windows. |

## Required tables

- **`DeviceFileEvents`** — **Required**. Primary source. Every
  query breaks without it.

## Optional tables

- **`DeviceFileCertificateInfo`** — **Optional enrichment**,
  deep-dive only. Signing info for the target file's hash.
- **`DeviceProcessEvents`** — **Optional enrichment**. Creator
  process context, execution status (did the file run), two-level
  ancestry (parent, grandparent), two-level descendants (child,
  grandchild). All joined via composite key.
- **`DeviceNetworkEvents`** — **Optional enrichment**. Network
  reach by chain (creator and forward chain), plus the preceding
  browser / script-host context window in narrative-gen.
- **`DeviceRegistryEvents`** — **Optional enrichment**. Registry
  writes by chain, including persistence keys.
- **`DeviceEvents`** — **Optional enrichment**. MDE response
  signals (`AntivirusDetection`, `Asr*`, `SmartScreen*`,
  `ExploitGuardNetworkProtectionBlocked`), plus persistence surfaces
  (services, scheduled tasks).

## Done criteria

1. File lifecycle and origin mapped: where the file appeared, who
   wrote it, when. Anchor mode chosen explicitly when the alert
   fired late.
2. Creator process chain identified and walked two levels up
   (level 0 always available via row-projection; levels 1–2 via
   ancestry lookup) and two levels down (children, grandchildren).
3. Execution status determined: did the file run, and if so what
   did it spawn.
4. Network, registry, and persistence activity from creator,
   executed, and descendant processes reviewed.
5. Sibling files in the same `FolderPath` assessed for
   campaign / staging shape.
6. MDE actions on the target file (or its hash) reviewed.
7. Preceding browser / email / script-host activity in the window
   before the anchor reviewed (narrative-gen Section 12).
8. Each finding mapped to one of the four closure buckets
   (**benign**, **precautionary benign**, **review required**,
   **suspicious / escalate**).
9. The narrative-gen output has been pasted into the ticket.

## Validation — test cases

> TODO: replace the placeholders below with real anonymised examples
> pulled from completed investigations.

1. **Known benign — TODO.** Definition / engine update writes a
   signed file under `%ProgramData%\Microsoft\Windows Defender\` and
   never executes outside the Defender chain.
   *Expected:* narrative-gen detects `staged_inert` or
   `modified`; signing info present; no MDE response; quick-dive
   closes.
2. **Ambiguous — TODO.** Developer writes a fresh unsigned `.exe`
   under `\Users\<dev>\AppData\Local\Temp\` on a managed laptop and
   runs it once. No network, no persistence.
   *Expected:* narrative-gen detects `executed_payload`; tenant
   rarity high; no MDE response; deep-dive lands review-required.
3. **Known bad / clearly suspicious — TODO.** Unsigned binary
   dropped into `\Users\Public\`, written by an Office process,
   executed within seconds, spawns `cmd.exe` and reaches out to a
   non-Microsoft IP. Persistence registry key written.
   *Expected:* narrative-gen detects `executed_payload`;
   signing info absent; child process and network reach populated;
   `AsrProcessBlocked` or `AntivirusDetection` fires; deep-dive
   lands escalate.
