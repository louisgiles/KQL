# TI URL/Domain Host Hit — Investigation Playbook

Triage flow for a Threat Intelligence map alert where a managed host (MDE-onboarded) connected to a flagged URL, domain, or IP. Confirms the hit, establishes surrounding context, and rules out execution / persistence / lateral movement before closure.

## Scope

**Use when:**
- TI map alert fires for a URL, domain, or IP match originating from a host in MDE
- Initial entity is a `DeviceName` plus a network indicator

**Do not use when:**
- TI hit has no associated device (proxy/firewall log only) — different playbook
- Mail-only TI hit with no device side — go straight to query 08
- Identity-only TI hit (sign-in risk) — different playbook

## Parameters

Substitute the bracketed tokens in each `.kql` file before running.

| Token | Description | Example |
|---|---|---|
| `<HOST>` | DeviceName from the alert | `ed-ap-2188` |
| `<URL_TOKEN>` | Substring matching the TI URL | `wavebrowser` |
| `<DOMAIN_TOKEN>` | Substring matching the TI domain | `wavebrowser.co` |
| `<IP>` | RemoteIP from the alert | `98.89.133.35` |
| `<START>` / `<END>` | Investigation window (datetime literals) | `2026-04-25 19:05` / `2026-04-25 19:25` |
| `<START_MINUS>` | Wider start (logon context) | `2026-04-25 17:00` |
| `<LOOKBACK>` | Email lookback window | `14d` |
| `<PROCESS>` | InitiatingProcessFileName from Q01 | `msedge.exe` |
| `<TOKEN>` | Free-form indicator string for Q04/Q05 | `wave` |

If a token doesn't apply (e.g. no IP available, no naming token to filter file events), drop the corresponding clause from the query — do not leave the placeholder in.

## Run order

`01 → 02 → 03 → 04 → 05` are the always-run baseline. The remainder are conditional based on what the baseline surfaces.

## Query index

| # | File | Purpose | Always run? |
|---|---|---|---|
| 01 | `01_confirm_ti_hit.kql` | Confirm the TI URL/IP hit and capture the initiating process | Yes |
| 02 | `02_initiating_process_context.kql` | What else the initiating process was doing in the window | Yes |
| 03 | `03_process_tree.kql` | Process activity on the host across the window | Yes |
| 04 | `04_file_drops.kql` | Files written to disk in the window | Yes |
| 05 | `05_registry_persistence.kql` | Registry persistence and browser-hijacker artefacts | Yes |
| 06 | `06_dns_resolution.kql` | DNS queries to the TI domain | Conditional |
| 07 | `07_persistence_tasks_services.kql` | Scheduled tasks, services, WMI persistence | Conditional |
| 08 | `08_email_vector.kql` | Email/Safe Links delivery vector | Conditional |
| 09 | `09_logon_context.kql` | Active sessions on the host at the time | Conditional |
| 10 | `10_internal_reach.kql` | Internal/lateral connections from the host | Conditional |
| 11 | `11_tenant_scope.kql` | Cross-host tenant-wide scope of the indicator | Conditional |

## Decision logic — conditional queries

**Run 06 (DNS)** when the TI is a domain and you want to confirm name resolution occurred independent of the connection. Caveat: `DnsQueryResponse` events under `DeviceEvents` depend on MDE sensor configuration and are not guaranteed.

**Run 07 (Tasks/Services)** when:
- Q03 shows suspicious child processes (LOLBins, scripting hosts, unsigned binaries from user-writable paths)
- Q04 shows executable or script drops
- Anything in the baseline suggests payload execution

**Run 08 (Email)** when the initiating process in Q01 is a browser, mail client, or Office application AND the URL could plausibly have been clicked rather than ad-served, redirected, or typed. Skip when the initiating process is a service host, background updater, or the surrounding network context shows ad-network rendering (malvertising pattern).

**Run 09 (Logon)** when:
- Confirming whether a user was actively signed in vs. background process activity
- Multi-user host or shared kiosk
- Suspicion of remote access (RDP, ScreenConnect, AnyDesk)

**Run 10 (Internal reach)** when:
- Q03 or Q04 shows execution
- Need to rule out lateral movement before closing
- Verdict trending toward True Positive

**Run 11 (Tenant scope)** before closing any True Positive — confirms whether the indicator hit other hosts in the tenant and informs blast radius.

## Closure verdict matrix

| Findings pattern | Verdict |
|---|---|
| TI hit only, browser context, no drops, no persistence, ad-network surroundings | Benign Positive (malvertising / drive-by) |
| TI hit only, browser context, no drops, but user-typed/bookmarked URL | Informational — user awareness |
| TI hit + executable/script drop, no execution observed | True Positive — Contained |
| TI hit + execution + persistence | True Positive — Compromise — Escalate |
| TI hit + lateral connections | True Positive — Compromise — Escalate, isolate host |

## Closure note skeleton

```
Incident Closure Note
Analyst Name: <ANALYST>
Entities:
- Host: <HOST>
- User: <USER>
- TI Match: <URL> (<IP>)
- Initiating Process: <PROCESS>

Actions taken:
- TimeGenerated: <START>–<END>
- Confirmed TI hit on <URL> from <HOST> via <PROCESS> (<USER>).
- Reviewed DeviceNetworkEvents context: <observation>.
- Reviewed DeviceProcessEvents: <child process observation>.
- Reviewed DeviceFileEvents: <file drop observation or "no artefacts written">.
- Reviewed DeviceRegistryEvents: <persistence observation or "no persistence created">.
- [Conditional] DNS / persistence / email / logon / lateral / tenant-scope observations.

Verdict: <BP / TP / Informational>. <One-line rationale>. <Further action or "no further action required">.
```
