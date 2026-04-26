# 05-endpoint/file

File-activity triage. v2 of `deep-dive.kql` and `narrative-gen.kql` —
extends v1 with two-level chain walks (ancestry and descendants),
persistence detection (services and scheduled tasks), and preceding
browser/script-host context.

## Queries

| File | Output type | Purpose |
|---|---|---|
| `deep-dive.kql` | analysis | Eleven-section evidence engine for a file alert: lifecycle, creator context, file metadata, execution status, network reach, registry writes, sibling files, creator ancestry, executed descendants, persistence created, preceding context. |
| `narrative-gen.kql` | narrative | Closure-ready note: per-subsection rollups assembled into a single `InvestigationNarrative` string. |

## Starting entities

- `AlertTime` (datetime, from alert)
- `DeviceName` (host of the alert)
- One or more of: `FileName`, `SHA256`, `FolderPath`

## Required tables

- `DeviceFileEvents` — **required**.

## Optional tables

- `DeviceFileCertificateInfo` — **optional enrichment** (signing info).
- `DeviceProcessEvents` — **optional enrichment** (execution, ancestry, descendants).
- `DeviceNetworkEvents` — **optional enrichment** (network reach, preceding context).
- `DeviceRegistryEvents` — **optional enrichment** (registry writes, registry persistence).
- `DeviceEvents` — **optional enrichment** (services installed, scheduled tasks, AV/MDE actions).

## Parameter reference

| Parameter | Default | Meaning |
|---|---|---|
| `AlertTime` | `datetime(null)` | The alert anchor. All windows derive from this. |
| `TimeToCheck` | `5m` | File-scope window — `AlertTime ± TimeToCheck`. |
| `AncestryLookback` | `24h` | How far back to walk parent process tree. |
| `PrecedingContextLookback` | `30m` | Window before AlertTime for browser/email/script context. |
| `HostToCheck` | `""` | Substring match on `DeviceName`. Empty matches all. |
| `FileNameToCheck` | `""` | Substring match on `FileName`. |
| `SHA256ToCheck` | `""` | Substring match on `SHA256`. |
| `FolderPathToCheck` | `""` | Substring match on `FolderPath`. |

Internal derivations:

- `_windowStart = AlertTime - TimeToCheck`
- `_windowEnd = AlertTime + TimeToCheck`
- `_execWindowEnd = AlertTime + max_of(TimeToCheck, 24h)` — extends forward to catch delayed execution.

## Section toggle reference

| Toggle | Default | Section | Source |
|---|---|---|---|
| `RunFileLifecycle` | `true` | 1 — File Lifecycle | `DeviceFileEvents` |
| `RunCreatorContext` | `true` | 2 — Creator Context | `DeviceFileEvents` |
| `RunFileMetadata` | `true` | 3 — File Metadata | `DeviceFileEvents` + `DeviceFileCertificateInfo` |
| `RunExecutionStatus` | `true` | 4 — Execution Status | `DeviceProcessEvents` |
| `RunNetworkReach` | `true` | 5 — Network Reach | `DeviceNetworkEvents` (chain) |
| `RunRegistryWrites` | `true` | 6 — Registry Writes | `DeviceRegistryEvents` (chain) |
| `RunSiblingFiles` | `true` | 7 — Sibling Files | `DeviceFileEvents` (creator) |
| `RunCreatorAncestry` | `true` | 8 — Creator Ancestry | process tree 2 levels up from creator |
| `RunExecutedDescendants` | `true` | 9 — Executed Descendants | process tree 2 levels down from executed |
| `RunPersistenceCreated` | `true` | 10 — Persistence Created | services and scheduled tasks created by the chain |
| `RunPrecedingContext` | `true` | 11 — Preceding Context | browser/script-host activity before AlertTime |

## Signal interpretation

- **Lifecycle (Section 1):** the `FileOriginUrl`, `FileOriginIP`, and
  `FileOriginReferrerUrl` columns identify the download or copy source —
  empty values mean the origin was not captured (often the case for
  files unpacked from archives or written by SYSTEM-context installers).
- **Creator (Section 2):** unsigned binaries spawning installer-like
  children, browser processes writing executables, and `cmd.exe` /
  `powershell.exe` writing under `\Users\Public\` are all worth a
  closer look.
- **Metadata (Section 3):** `IsSigned=false` plus `PathCategory =
  User-Writable / Temp` is the canonical PUP / commodity-malware
  signature. `IsTrusted=false` on a signed binary points at expired,
  revoked, or untrusted-CA certs — common with bundleware.
- **Execution (Section 4):** absence is informative — if the file never
  executed within `_execWindowEnd`, persistence on a future trigger
  becomes the relevant question (Section 10).
- **Network reach (Section 5):** chain-process outbound to non-Microsoft
  destinations, especially short-lived hostnames or raw IPs, is the
  key indicator. Multi-destination fan-out from a Descendant role
  process is more suspicious than from a Creator.
- **Registry writes (Section 6):** writes under `Run`, `RunOnce`,
  `Userinit`, `Image File Execution Options`, or service-control
  subkeys are persistence — overlap with Section 10 by design.
- **Sibling files (Section 7):** if the creator wrote a single file,
  this is empty. If it wrote a payload set (DLLs, configs, scripts)
  expect 5-50 entries — read for unsigned, user-writable paths.
- **Ancestry (Section 8):** unusual roots are the signal — `services.exe`
  with a non-standard child, browser launched with `--no-startup-window`
  (URL-handler invocation), or unsigned binary spawning elevated
  installer all warrant escalation.
- **Descendants (Section 9):** LOLBins (`powershell`, `mshta`,
  `rundll32`), unsigned binaries in user-writable paths, and
  network-capable utilities (`curl`, `bitsadmin`, `certutil`) all
  indicate post-execution payload activity. Multi-level descendant
  chains where the root is a known PUP installer (`PcAppStore`,
  `WaveBrowser`, etc.) are typical.
- **Persistence (Section 10):** service installation under a chain
  process is the most common persistence path for installer-based
  PUPs/bundleware. Scheduled task creation by the chain is less common
  and warrants closer review of the task command and trigger.
- **Preceding context (Section 11):** malvertising redirect chains
  show `googlesyndication`, `doubleclick`, or known ad-network domains
  immediately before the download. Email vector clicks show
  `outlook.exe` or `teams.exe` as the initiator. Script-host activity
  (`powershell`, `mshta`, `certutil`) preceding a file drop is
  high-priority — typical of living-off-the-land downloaders.

## Done criteria

- File lifecycle mapped; origin URL/IP captured or accounted for.
- Creator process chain identified and walked two levels up (Section 8)
  and two levels down (Section 9).
- Execution status determined (Section 4); zero-execution outcome
  followed up with persistence check.
- Network and registry activity from Creator/Executed/Descendant
  processes reviewed (Sections 5, 6).
- Persistence creation by any chain process reviewed (Section 10).
- Sibling files assessed (Section 7).
- Preceding browser/email/script-host activity reviewed (Section 11).
- Each finding classified into one of the four closure buckets.

## Validation — test cases

1. **Known benign — TODO.** Defender definition update writing a
   DAT/VDM under `\ProgramData\Microsoft\Windows Defender\` —
   creator is a signed Microsoft binary, no execution, no chain
   activity.
2. **Ambiguous — TODO.** Bundleware installer (`PcAppStore.exe` or
   similar) under `\Users\<u>\Downloads\` — executes, spawns
   children, installs a service, registers a scheduled task; signed
   but not by a household publisher.
3. **Known bad / clearly suspicious — TODO.** LOLBin chain
   (`mshta.exe` or `rundll32.exe`) writing under `\Users\Public\`
   followed by an outbound to a non-Microsoft IP and a `Run`-key
   registry write.

## Handoff to process/

`file/deep-dive` walks 2 levels of process tree in each direction
(parent and grandparent backward, child and grandchild forward).
Beyond that, pivot to `process/deep-dive`.

When to pivot:

- Section 8 surfaces a grandparent that is itself suspicious — take
  its PID into `process/deep-dive` for full ancestry/activity
  context.
- Section 9 surfaces grandchildren that spawn further activity —
  pivot with the grandchild PID to walk its own chain.
- Investigation needs 3+ levels of tree walk in either direction.

What to take across:

- Specific PID (more reliable than process name due to PID reuse).
- AlertTime (anchor remains the same).
- HostToCheck (unchanged).

`process/deep-dive` surfaces full ancestry, descendants, and
per-process network/file/registry activity for any arbitrary PID
on the host.
