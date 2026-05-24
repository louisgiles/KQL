# 05-endpoint

Endpoint investigation family. Contract exception: ships **three
parallel sub-families** (process, file, network) instead of a single
`deep-dive.kql` / `narrative-gen.kql` pair at the family root.

## Sub-families

| Sub-family | Primary table | When to use | Notes |
|---|---|---|---|
| [`process/`](process/notes.md) | `DeviceProcessEvents` | Alert is on something that ran (process name, command line, SHA256 of an executed image). | [process/notes.md](process/notes.md) |
| [`file/`](file/notes.md) | `DeviceFileEvents` | Alert is on something that appeared on disk (FileCreated, FileRenamed, FileModified, FileDeleted). | [file/notes.md](file/notes.md) |
| [`network/`](network/notes.md) | `DeviceNetworkEvents` | Alert is on a connection (RemoteUrl, RemoteIP, RemotePort, periodic-beacon match). | [network/notes.md](network/notes.md) |

Each sub-family ships the full contract: `deep-dive.kql` +
`narrative-gen.kql` + `notes.md`, plus an optional `quick-dive.kql`.

## Cross-cutting design

All three sub-families share three architectural conventions. The
details live in each sub-family's `notes.md`; the headlines are:

- **Anchor model.** `AnchorMode = "alert"` centres on `AlertTime`.
  Each sub-family also offers an origin mode
  (`process_origin` / `file_origin` / `network_origin`) for alerts
  that fire on downstream events well after the actual lifecycle.
- **Composite `(ProcessId, ProcessCreationTime)` keying.** Every
  cross-table join uses the composite key, never bare `ProcessId`.
  Defends against PID reuse across the 24h forward window.
- **Togglable sections.** Each `deep-dive.kql` ships per-section
  boolean toggles so the analyst can narrow output to the section
  that matters for the alert.

## Starting entities (family-wide)

Every sub-family takes `AlertTime` + `DeviceName` plus at least one
table-specific entity. See the per-sub-family notes for the full
list.

## Required tables (family-wide)

- `DeviceProcessEvents` — required by `process/`.
- `DeviceFileEvents` — required by `file/`.
- `DeviceNetworkEvents` — required by `network/`.

## Done criteria (family-wide)

Each sub-family carries its own done criteria. A typical endpoint
investigation closes when:

1. The right sub-family has been selected for the alert shape.
2. The alert's chain has been walked end-to-end across whichever
   process / file / network surfaces are relevant.
3. Each finding has been mapped to one of the four closure buckets
   (**benign**, **precautionary benign**, **review required**,
   **suspicious / escalate**).
4. The sub-family's `narrative-gen.kql` output has been pasted into
   the ticket.

## Validation — test cases

Test cases live in the per-sub-family `notes.md` files:

- [process/notes.md — Validation](process/notes.md#validation--test-cases)
- [file/notes.md — Validation](file/notes.md#validation--test-cases)
- [network/notes.md — Validation](network/notes.md#validation--test-cases)
