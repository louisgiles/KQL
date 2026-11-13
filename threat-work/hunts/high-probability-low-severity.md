# High-probability, low-severity threat hunts

**Last researched:** 13 November 2026  
**Research run:** 01 — two new candidates  
**Execution surface:** Microsoft Sentinel / Log Analytics workspaces only  
**Status:** Researched hunt hypotheses; no client queries have been run or results claimed.

## Purpose and selection standard

Find identifiable unwanted software and related activity that is worth checking across client estates: a good chance of a useful finding, a clear explanation of what the evidence proves, and a low initial severity when the finding is limited to unapproved software. Wave Browser, PDF Polish, Shift Browser and ClickFix are the examples that established the brief; they are not counted as new candidates in this run.

**High fidelity means confidence in the observed application or behaviour.** Whether it is unwanted depends on client policy and context. Low severity applies to the finding being investigated, not every possible consequence of the software. Independent evidence of malicious execution changes the assessment.

The likelihood of a hit across clients is not yet measured. Selection below uses published distribution evidence, real enterprise observations and identifiable artefacts; it does not promise a hit or assign invented percentages. Existing, persistent software is in scope even when the supporting research is older than seven days.

## Hunt index

| ID | Candidate | Why it earns a first pass | Initial finding sought | Status |
| --- | --- | --- | --- | --- |
| [H001](#h001-onelaunch) | OneLaunch | Historical consumer scale and an actual corporate hunt finding; now a sweep for remaining installations. | Corroborated execution of unapproved OneLaunch. | Researched; not run |
| [H002](#h002-pc-app-store) | PC App Store, with VeryFast-related pivots | Repeated enterprise observations of its distribution channel, plus recognisable runtime artefacts. | Corroborated execution of an unapproved PUP/adware application. | Researched; not run |

**Suggested starting window:** 30 days of available endpoint telemetry. Extend to 90 days where retention and cost permit if recent results are sparse or installation context is missing. These are proposed working windows, not vendor requirements. First observed activity within retention is not necessarily the installation date.

## Sentinel visibility required

Assess each workspace separately. Confirm that the selected source has recent events from the Windows endpoint population being hunted, and record its retained time range. A table name, connector or licence alone is not proof of coverage.

| Question | Usable workspace telemetry | What to check |
| --- | --- | --- |
| Did the application execute? **Required for a confirmed execution finding.** | `DeviceProcessEvents` streamed into the workspace; alternatively collected Windows Security event 4688 or Sysmon event 1. | Device, time, executable path/name and available command line or parent. Native 4688 command-line capture requires a separate policy. [^ms-process][^ms-4688][^ms-sysmon] |
| Was it installed or made persistent? **Optional corroboration.** | `DeviceFileEvents`, `DeviceRegistryEvents`, or equivalent collected Windows/Sysmon events. | Product-specific file writes, autorun targets or task/service details, if collected. Event streams do not enumerate all existing files or persistence. [^ms-stream][^ms-sysmon] |
| Is its signing identity corroborated? **Optional enrichment.** | `DeviceFileCertificateInfo`, if ingested, matched to the relevant executable's SHA1. | Certificate signer/trust evidence. A missing row is not proof that the file is unsigned. [^ms-cert] |
| Did the product communicate externally? **Optional corroboration.** | `DeviceNetworkEvents`, Sysmon DNS/network events, or attributed DNS/proxy logs already ingested. | Match the actual process when available; otherwise retain a network lead. A domain lookup alone does not establish installation. [^ms-stream][^ms-sysmon] |
| Was a download, installation or execution blocked? **Optional lead.** | Relevant `DeviceEvents` / `SecurityAlert` or another ingested security-product log. | Read the action and remediation outcome. Detection is not proof of successful execution. [^ms-stream][^ms-pua] |

**Workspace boundaries:** Defender XDR incident/alert integration and raw-event collection are separate. Each needed raw table must actually be ingested. `DeviceTvmSoftwareInventory` is not supplied to Sentinel through the standard event-streaming route; neither hunt depends on it. Queries developed from this document must use the Log Analytics schema, including `TimeGenerated` for `DeviceProcessEvents`. [^ms-stream][^ms-process]

For Windows alternatives, Security Events via AMA uses `SecurityEvent`; Windows Forwarded Events uses `WindowsEvent`, including forwarded Security events. Inspect the configured route and event payload rather than assuming a universal table. [^ms-windows]

`ProcessVersionInfoCompanyName` and other version fields are metadata, not verified signers. `InitiatingProcessSignatureStatus` concerns the initiating process, not automatically the newly created executable. [^ms-process] Certificate evidence can strengthen identification; it does not establish business approval or safe behaviour.

## H001: OneLaunch

### Hypothesis and likely value

Some managed Windows endpoints may still run OneLaunch outside the client's approved software baseline. A narrowly scoped sweep should produce identifiable software findings suitable for low-severity review.

**Reported facts:** Malwarebytes identifies the application as `PUP.Optional.OneLaunch` and describes installer-driven browser-setting changes without consent. CyberSift reports finding it on a monitored corporate workstation during a proactive hunt. That is a real business-environment sighting, not evidence of widespread deployment across businesses. [^ol-mb][^ol-cybersift]

The vendor's undated About page claims a milestone of one million daily users. Its current homepage says downloads are no longer available and existing users will continue to receive support. Treat the scale claim as historical, self-reported consumer context. This is a hunt for remaining installations, not a newly expanding campaign. [^ol-about][^ol-home]

**Assessment:** A worthwhile residual-software sweep with a particularly specific process/network pivot. Confidence in identifying a match is stronger than the evidence for current enterprise prevalence.

### Verified starting pivots

| Pivot | Source and interpretation |
| --- | --- |
| `OneLaunch.exe` | Product process identified in SigmaHQ's original OneLaunch updater rule. Use as a discovery seed, then corroborate identity. [^ol-sigma] |
| `update.onelaunch.com` | SigmaHQ pairs this exact DNS name with `OneLaunch.exe`. Process-attributed updater traffic is much stronger than an unattributed DNS hit. [^ol-sigma] |
| `PUP.Optional.OneLaunch` | Vendor detection-name lead. Check whether the record concerns an installed application, a block or historical remediation. [^ol-mb] |

The SigmaHQ reference is dated 26 February 2024 and marked `test` / `low`. It supports the historical pivot, not a claim that the rule has been validated in these workspaces. Its ATT&CK tags are not evidence that an updater request demonstrates credential theft. [^ol-sigma]

### High-level hunt idea

1. **Find execution candidates.** Search the chosen process source for the exact product executable. Review returned paths, product metadata, command lines and hashes. Do not substitute generic Chromium process names for the product identity.
2. **Corroborate the application.** Prefer execution linked to the exact updater hostname, or corroborate with available signing information and product-specific installation/persistence evidence. Match process instances by device and available unique process identifiers, or PID plus creation time, rather than PID alone.
3. **Establish observed use.** Summarise first/last execution, users and distinct active days. Recurrence supports continued activity during the window; one installer launch or an old remnant is a different finding. Expand into nearby installation/updater events when the source of installation is visible.
4. **Decide whether it is unwanted.** Check the client's software approval and the user's installation context. Review unexpected descendants or adjacent payloads before closing the finding as an ordinary unapproved application.

**Minimum viable route:** Process telemetry plus corroborating product identity. Process-attributed DNS/network activity is the preferred additional signal; it is not a mandatory dependency for every client.

### Positive finding, noise and severity

**High-confidence positive:** OneLaunch execution during the hunt window, with product identity corroborated beyond a bare filename. If the client has not approved it, this supports an unwanted-software finding at low initial severity. It does not establish compromise or prove the application is still installed at the time of reporting.

Approved intentional use is a possible benign outcome. Website visits, updater-domain DNS alone, blocked downloads and old quarantine records remain weaker leads. Browser imports, routine updater activity and ordinary browser child processes are not sufficient evidence of malicious behaviour.

Escalate when separately supported evidence shows malicious payload execution, security-control interference or another compromise indicator. Do not raise severity solely because the software is a browser or a PUP, and do not use its PUP label to dismiss suspicious follow-on activity.

## H002: PC App Store

### Hypothesis and likely value

Some managed Windows endpoints may have an active, unapproved PC App Store installation or related VeryFast component. Its application identity and service/runtime traces offer concrete, repeatable discovery points.

**Reported facts:** Red Canary classifies PC App Store as a PUP. Its 2026 report describes continued 2025 observations of PC App Store installers delivering Amber Albatross, a separate malicious activity chain. This supplies enterprise relevance, but neither the report's customer percentage nor its threat ranking measures PC App Store installation prevalence. [^pc-redcanary]

Microsoft has an `Adware:Win32/PCAppStore!MTB` detection entry, published 11 July 2023. Malwarebytes documents `PUP.Optional.VeryFast`, including a legacy executable and service useful for expanding the search. [^pc-ms][^pc-mb]

**Assessment:** A good first-pass candidate because the product has stable identification opportunities and documented operational relevance. The intended low-severity result is unapproved application activity; checking what the application installed is an essential triage step.

### Verified starting pivots

| Pivot | Source and interpretation |
| --- | --- |
| `PCAppStore.exe` / `PcAppStore.exe` | Case variants of the product executable; use case-insensitive matching. A 24 February 2025 sample reports ProductName `PC App Store`, CompanyName `Fast Corporation LTD`, FileDescription `PC App Store Runtime`, and InternalName `fa_rss.exe`. These are sample metadata, not certificate validation. [^pc-anyrun] |
| `C:\Program Files (x86)\PCAppStore\` and `PcAppStoreSRV.exe` | Observed installed directory and service executable in a 12 January 2026 sandbox execution. Useful corroboration, not an exhaustive path specification. [^pc-triage] |
| `fa_rss.exe` and service `FastSRV` | Malwarebytes' VeryFast traces. Treat these as related discovery leads and verify the actual product; do not automatically equate every VeryFast detection with the current PC App Store runtime. [^pc-mb] |
| `Adware:Win32/PCAppStore!MTB`; `PUP.Optional.VeryFast` | Security-product label pivots where relevant logs are ingested. [^pc-ms][^pc-mb] |
| `pcapp[.]store`; `ev.pcapp[.]store` | Observed product network destinations in an independent January 2026 analysis. Optional corroboration when attributable to the process, not standalone compromise indicators. [^pc-network] |

Malwarebytes spells the publisher `Fast Corporate LTD`; the cited sample metadata uses `Fast Corporation LTD`. Preserve the observed distinction. A generic match on “Fast”, `Setup.exe` or “App Store” is too broad. This card concerns the identified Fast product, not Microsoft Store or a different product sharing an app-store name.

### High-level hunt idea

1. **Discover and confirm identity.** Sweep available process telemetry for the runtime and related legacy executable. Corroborate using product metadata, the observed product directory, a matching service/runtime relationship, or independently verified signing evidence. Search the related identity as well as the current filename so a rename does not become the only reason for a miss.
2. **Separate acquisition from operation.** Distinguish installer execution in Downloads, blocked attempts, an installed runtime and recurring service/application activity. Record first/last seen and active days by workspace and endpoint. A downloaded file does not prove installation.
3. **Inspect subsequent installation activity.** Review descendants, file writes and associated network activity around first observed execution and updater runs. Identify what was downloaded and whether it executed. Retain the product's PUP finding separately from any confirmed secondary payload.
4. **Apply the client's policy.** Establish whether it was intentionally approved. Produce an actionable software finding where it is unapproved; record authorised use separately. If the secondary-activity view is unavailable, retain that limitation rather than concluding the endpoint is clean.

**Minimum viable route:** Process telemetry plus corroborating product identity. File, service, registry, network and security-control events strengthen the assessment where already available in the workspace.

### Positive finding, noise and severity

**High-confidence positive:** Corroborated execution of the identified PC App Store runtime or a verified related component. Low initial severity is appropriate to a finding limited to unapproved PUP/adware activity, subject to client policy.

**Escalation boundary:** Red Canary describes downstream obfuscated payload execution and reconnaissance associated with Amber Albatross. A linked suspicious download/execution chain or independent evidence of credential access warrants a separate, higher-severity assessment. A generic PowerShell process or a sandbox verdict alone is not enough to attribute that family. [^pc-redcanary]

Approved use, blocked installers, historical remnants and unrelated similarly named software must not be counted as active unwanted installations. Product metadata can be copied. Old sample paths and hashes can corroborate identity, but should not become the only discovery route or a blanket safety verdict.

## Recording a result

Use these outcomes consistently when the hunts are actually run:

| Outcome | What it means |
| --- | --- |
| Confirmed application execution | Product identity and execution are corroborated; approval is recorded separately. |
| Installation/persistence artefacts only | Relevant traces found, but execution is not demonstrated. |
| Blocked attempt | A prevention event is established; successful installation/execution remains unproven. |
| Network lead only | Product-associated traffic without sufficient endpoint attribution. |
| No matches within verified coverage | No relevant evidence in the stated population, sources and window. |
| Not assessable | The required telemetry or endpoint coverage is missing. |

For each run, record the number of workspaces and endpoints actually covered, the time range, confirmed findings, approval decisions and visibility limitations. This is how the register's expected yield becomes evidence from the estate. Keep individual device/user evidence with the relevant investigation; add aggregate feedback here.

## Rules for subsequent research runs

1. Read this file and existing repository research first. Append **two distinct new candidates** to this same file, with stable IDs and an updated index. Rebrands, aliases and minor variations of an existing candidate do not count as two new hunts.
2. For each candidate, record the source-backed finding, why a useful hit is plausible, precise starting pivots, a high-level hunt idea, Sentinel telemetry dependencies, benign explanations, and what a positive does and does not establish.
3. Separate reported facts from assessment and proposed hunting. Date the research and preserve source-age limitations. Update an existing card in place when new evidence changes its suitability, with a note in the run log.
4. Keep the scope at research and high-level hunt design unless query implementation is requested. Do not substitute Defender XDR Advanced Hunting for the required Log Analytics execution surface.
5. Record actual analyst feedback when supplied. Never turn a research candidate, blocked attempt or missing-data result into a claimed client finding. If two defensible candidates cannot be found, record the shortfall rather than pad the register.

## Run log

| Run | Date | Added | Research decisions |
| --- | --- | --- | --- |
| 01 | 2026-11-13 | H001 OneLaunch; H002 PC App Store | OneLaunch scoped to remaining installations. PC App Store scoped to PUP presence with secondary-activity triage. OneStart excluded from the low-severity pair because Expel links it to the BaoLoader developer's operation. No client results asserted. [^excluded-onestart] |

## Sources

All sources reviewed on **13 November 2026**. Undated pages are not represented as newly published research. Public sandbox observations establish sample-specific artefacts, not estate prevalence.

[^ol-mb]: Malwarebytes, [PUP.Optional.OneLaunch](https://www.malwarebytes.com/blog/detections/pup-optional-onelaunch), undated detection description.
[^ol-cybersift]: CyberSift, [Potentially Unwanted Software on Corporate Endpoints](https://www.cybersift.com/post/potentially-unwanted-software-on-corporate-endpoints). Page displays “Mar 27” without a year in the retrieved body; one corporate workstation reported.
[^ol-about]: OneLaunch, [About us](https://onelaunch.com/about-us), undated vendor user-scale claim.
[^ol-home]: OneLaunch, [Official homepage](https://onelaunch.com/), current download-withdrawal notice observed on the review date.
[^ol-sigma]: SigmaHQ, [DNS Query Request To OneLaunch Update Service](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/dns_query/dns_query_win_onelaunch_update_service.yml), 26 February 2024; status `test`, level `low`. Used as a documented pivot, not an implemented rule.
[^pc-redcanary]: Red Canary, [Amber Albatross — 2026 Threat Detection Report](https://redcanary.com/threat-detection-report/threats/amber-albatross/), reporting 2025 observations; sections “Analysis”, “Intrusion chain” and “Take action”.
[^pc-ms]: Microsoft Security Intelligence, [Adware:Win32/PCAppStore!MTB](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=Adware%3AWin32%2FPCAppStore%21MTB&ThreatID=367081), 11 July 2023. Supports detection naming; detailed behaviour is not supplied.
[^pc-mb]: Malwarebytes, [PUP.Optional.VeryFast](https://www.malwarebytes.com/blog/detections/pup-optional-veryfast), undated detection description and artefact list.
[^pc-anyrun]: ANY.RUN, [PcAppStore.exe sample analysis](https://any.run/report/6fb23dcb8ae019046b8c09fe164e8d49d8d541c3604122ac640ea5a33ede3b13/a9a14ff4-6b84-49b4-aa6a-2e4225c406f0), 24 February 2025; sample metadata and execution only.
[^pc-triage]: Triage, [Public execution 260112-2yrm1sgz4e](https://tria.ge/260112-2yrm1sgz4e/behavioral1), 12 January 2026; observed PCAppStore installation path and service executable.
[^pc-network]: Rifteyy, [PC App Store deceptor network analysis](https://rifteyy.org/report/pc-app-store), 7 January 2026; original network experiment, used only for product-associated destinations.
[^ms-stream]: Microsoft Learn, [Stream Microsoft Defender XDR data to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender), raw-table selection and unsupported TVM-table guidance.
[^ms-process]: Microsoft Learn, [Log Analytics DeviceProcessEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceprocessevents), workspace fields and semantics.
[^ms-cert]: Microsoft Learn, [Log Analytics DeviceFileCertificateInfo reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicefilecertificateinfo), certificate fields and SHA1 linkage.
[^ms-windows]: Microsoft Learn, [Windows agent-based Sentinel connectors](https://learn.microsoft.com/en-us/azure/sentinel/connect-services-windows-based), collection routes and destination tables.
[^ms-4688]: Microsoft Learn, [Event 4688: A new process has been created](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688), process creation and command-line audit prerequisites.
[^ms-sysmon]: Microsoft Learn, [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon), event types and collection capabilities.
[^ms-pua]: Microsoft Learn, [Detect and block potentially unwanted applications](https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus), PUA classification and prevention semantics.
[^excluded-onestart]: Expel, [The history of AppSuite: the certs of the BaoLoader developer](https://expel.com/blog/the-history-of-appsuite-the-certs-of-the-baoloader-developer/), original research linking OneStart and related products to the same developer operation; used for exclusion from this run's low-severity pair.
