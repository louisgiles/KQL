# Cloudflare Tunnel hunt

## Analyst purpose

Use this module to identify Cloudflare Tunnel deployment or execution evidence
across endpoint telemetry without relying on campaign-specific IOCs. It is a
hunt, not an automatic malicious verdict: Cloudflare Tunnel is also legitimate
administration and development software.

## Starting entities and variables

`deployment.kql` can run population-wide. Optional `DeviceNameToCheck` and
`AccountToCheck` filters narrow the hunt. `HuntEnd`, `HuntWindow`, and
`BaselineWindow` define the scoring window and prior context.

## Dependencies

- **Required:** `DeviceProcessEvents`.
- **Optional enrichment:** `DeviceNetworkEvents`, included with `union isfuzzy=true` for successful connector-egress context.
- **Avoid as a hard dependency:** Cloudflare dashboard/API evidence unless a tenant-specific audit table is explicitly available; endpoint telemetry cannot prove dashboard-only tunnel creation before a local connector or artifact appears.

## Time behaviour

Default hunt window: 7 days. Default preceding baseline: 21 days. Both are
bounded by `HuntEnd`.

## Output and decision use

The query returns event-level device, actor, process, hash, command-line,
connector-egress, first-seen, and tenant-prevalence context. Review the raw
command, binary identity/path, actor, successful connector egress, and business
owner before deciding whether to contain, close, or extend the hunt.

## Done criteria

Stop when the deployment owner and intended published service are confirmed and
the process/network evidence is consistent with that explanation, or escalate
when the evidence supports unauthorized remote-access capability, deliberate
evasion, unknown control-plane ownership, or unresolved credential-backed
persistence.

## Known coverage limits

The preserved legacy analysis in [`notes.md`](notes.md) records observed benign
patterns and false positives. Two limits are particularly important:

- the current network arm associates TCP/UDP 7844 egress only when the
  initiating process/command line references cloudflared, so renamed-binary
  egress can lose network corroboration;
- wrapper commands and repository filenames containing `cloudflared` can create
  benign process hits on developer endpoints.

`IsRenamedCloudflared`, user-writable execution, credential arguments, first-seen
context, and port 7844 are prioritisation evidence, not standalone compromise
proof. Command lines may contain sensitive tokens and should be handled as
sensitive output.

## Validation

The migrated hunt preserves the prior query logic and adds the v2 artifact
metadata required by the repository contract. The supporting notes contain
multi-tenant observations and triage pivots. Revalidate syntax in CI and validate
runtime schema/telemetry in the target workspace before relying on the result.
