# Investigation pivots

Five small entry points for a live incident. Pick the query matching the most
reliable starting entity. Do not run all five by default.

| Query | Starting entity | Primary decision |
| --- | --- | --- |
| `actor.kql` | User principal name | Which identity, Microsoft 365, or Azure events need immediate validation? |
| `ip.kql` | IPv4 or IPv6 address | Which source families, accounts, and devices did the IP touch in the incident window? |
| `device.kql` | Defender `DeviceId` or exact device name | Which recent process, file, network, or security events change isolation scope? |
| `session.kql` | Session, correlation, or original-request ID | Did the authentication context continue into other identity or cloud activity? |
| `process.kql` | Defender device ID plus process ID and creation time | What did the exact process execute, write, contact, or change? |

## Dependencies

| Query | Required | Optional enrichment | Avoided as a hard dependency |
| --- | --- | --- | --- |
| actor | At least one of `SigninLogs`, `AuditLogs`, `OfficeActivity`, `AzureActivity` | The other listed tables | Long identity baselines |
| IP | At least one of the declared identity, M365, Azure, or endpoint tables | Remaining declared tables | Threat intelligence and 90-day prevalence |
| device | At least one declared Defender endpoint table | Remaining endpoint tables | `DeviceInfo` freshness as a gate |
| session | At least one of `SigninLogs`, `AADNonInteractiveUserSignInLogs`, `CloudAppEvents` | Remaining declared tables | Session inference from IP alone |
| process | `DeviceProcessEvents` | `DeviceNetworkEvents`, `DeviceFileEvents`, `DeviceRegistryEvents` | Filename-only process identity |

Queries use `union isfuzzy=true` where a source is optional. This allows an
absent optional table to be ignored, but tenant schema drift can still cause a
runtime error and must be recorded as missing coverage.

## Time windows

- Actor, device, session, and process pivots default to two hours before and
  one hour after the supplied anchor.
- The IP pivot defaults to four hours before and one hour after the anchor.
- Permitted routine bounds are up to seven days. Longer baselines belong in an
  explicit follow-on query or hunt.

## Output and done criteria

All pivots implement the root investigation output contract. Stop when the
rows identify the primary event, affected entities, decisive evidence, and a
specific containment or follow-on step. Continue only when the result is
truncated, ambiguous, missing required telemetry, or points to another entity.

## Validation limits

The repository smoke test validates KQL grammar only. Before production use,
run each query against representative empty, benign, suspicious, truncated,
missing-table, and schema-variant cases and record runtime evidence for the
declared default window.

