# High-probability, low-severity threat hunts

**Last researched:** 13 November 2026  
**Latest research run:** 02 — two new candidates, plus a correction to Run 01  
**Active candidates:** Four; H002 retired as already known  
**Scheduled research:** Hourly through the final scheduled run at 08:00 Europe/London on 14 November 2026  
**Execution surface:** Microsoft Sentinel / Log Analytics workspaces only  
**Status:** Researched hunt hypotheses; no client queries have been run or results claimed.

## Purpose and selection standard

Find identifiable unwanted software and related activity that is worth checking across client estates: a good chance of a useful finding, a clear explanation of what the evidence proves, and a low initial severity when the finding is limited to unapproved software. Wave Browser, PDF Polish, Shift Browser and ClickFix are the examples that established the brief; they are not counted as new candidates in this run.

**High fidelity means confidence in the observed application or behaviour.** Whether it is unwanted depends on client policy and context. Low severity applies to the finding being investigated, not every possible consequence of the software. Independent evidence of malicious execution changes the assessment.

The likelihood of a hit across clients is not yet measured. Selection below uses published distribution evidence, real enterprise observations and identifiable artefacts; it does not promise a hit or assign invented percentages. Existing, persistent software is in scope even when the supporting research is older than seven days.

## Already covered or excluded

| Subject | Decision |
| --- | --- |
| PC App Store and VeryFast-related pivots | Already well known, confirmed by the user on 13 November 2026. H002 retired; do not propose aliases or minor variants as new candidates. Web Companion replaces its slot in Run 01. |
| Wave Browser, PDF Polish, Shift Browser, ClickFix | Already-known calibration examples; do not count them as fresh candidates. |
| OneStart / BaoLoader-associated activity | Not suitable for a routine low-severity PUP entry on the evidence reviewed. Preserve the distinction between product presence and malicious activity. [^excluded-onestart] |

Retired IDs are not reused. The active candidates below total four: two from the corrected first run and two from Run 02.

## Hunt index

| ID | Candidate | Why it earns a first pass | Initial finding sought | Status |
| --- | --- | --- | --- | --- |
| [H001](#h001-onelaunch) | OneLaunch | Historical consumer scale and an actual corporate hunt finding; now a sweep for remaining installations. | Corroborated execution of unapproved OneLaunch. | Researched; not run |
| [H003](#h003-adaware-web-companion) | Adaware Web Companion | Bundled distribution acknowledged by its publisher; organisational cases documented by Trustwave. | Corroborated unapproved runtime and related browser-setting activity. | Run 01 replacement; not run |
| [H004](#h004-relevantknowledge) | RelevantKnowledge | Freeware distribution and identifiable measurement-software components. | Corroborated unapproved research-panel software activity. | Run 02; not run |
| [H005](#h005-bright-vpn) | Bright VPN | Consumer distribution with a disclosed connection-sharing background component. | Corroborated unapproved VPN/background-component activity. | Run 02; not run |

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

**Workspace boundaries:** Defender XDR incident/alert integration and raw-event collection are separate. Each needed raw table must actually be ingested. `DeviceTvmSoftwareInventory` is not supplied to Sentinel through the standard event-streaming route; these hunts do not depend on it. Queries developed from this document must use the Log Analytics schema, including `TimeGenerated` for `DeviceProcessEvents`. [^ms-stream][^ms-process]

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

## H003: Adaware Web Companion

**Added:** Run 01 correction, replacing the redundant PC App Store candidate. H002 is retired.

### Hypothesis and likely value

Windows clients that permit freeware may retain an unapproved Adaware/Lavasoft Web Companion installation, with continuing runtime and browser-setting activity.

**Reported facts:** Malwarebytes identifies `PUP.Optional.WebCompanion` and describes bundled installation with search-setting changes. The publisher's FAQ acknowledges bundled distribution and inadvertent user acceptance. Trustwave's 2023 manufacturing report documents organisational cases involving the application, including an MSI-to-PowerShell installation chain. [^wc-mb][^wc-faq][^wc-trustwave]

**Assessment:** A practical consumer-software exposure hunt supported by both the distribution mechanism and actual business-environment observations. The organisational evidence is historical; current prevalence across clients is unmeasured.

### Verified starting pivots

| Pivot | Source and interpretation |
| --- | --- |
| `WebCompanion.exe`; supporting `WebCompanion.Loader.exe` and `WebCompanionInstaller.exe` | Component names in Trend Micro's original analysis. Keep installed runtime, loader and installer outcomes distinct. [^wc-trend] |
| `\Lavasoft\Web Companion\Application\` | Historical product-directory suffix documented under Program Files. Inspect returned paths; do not make this old location the only discovery route. [^wc-trend] |
| `PUP.Optional.WebCompanion`; `PUA:Win32/WebCompanion` | Malwarebytes and Microsoft detection-name leads, subject to action/remediation review. [^wc-mb][^wc-ms] |

### High-level hunt idea

Use the common 30-day starting window and expand within retention where useful.

1. **Discover execution.** Find the distinctive product components in workspace process events. Corroborate the actual product through its directory, metadata, available signature evidence or another component.
2. **Separate installation from use.** Distinguish a downloaded/blocked installer from an executing application. Summarise first/last activity and distinct active days; inspect startup-related events if collected.
3. **Review acquisition and changes.** Examine the preceding installer and descendants. Look for product-linked browser-setting or persistence changes only where the workspace captures those events. An obfuscated delivery chain warrants inspection of what actually ran.
4. **Establish approval.** Check the client's software baseline and the user's installation context. Record confirmed unwanted use separately from approved software, blocked attempts and historical remnants.

**Minimum viable route:** Workspace-ingested `DeviceProcessEvents`, or collected 4688/Sysmon 1 events, with enough identity evidence to corroborate the product. File, registry, certificate and network data are optional enrichment.

### Positive finding, noise and severity

**High-confidence positive:** Corroborated Web Companion runtime execution during the window. Unapproved presence or unwanted browser-setting changes can support a low-severity finding. A domain visit or an installer name alone cannot establish this.

Deliberate approved installation is a possible benign explanation. Investigate the delivery chain without automatically attributing every suspicious installer behaviour to the installed application. Trustwave's observed PowerShell delivery is a reason to examine payloads, not a reason to presume every Web Companion installation is compromised. [^wc-trustwave] Elevate independently established malicious execution, sensitive-data exposure or security-control interference.

## H004: RelevantKnowledge

**Added:** Run 02.

### Hypothesis and likely value

Windows endpoints may be running unapproved internet-usage measurement software acquired with freeware. The intended finding is identifiable research-panel software operating on a work endpoint outside the client's approved baseline.

**Reported facts:** Malwarebytes documents RelevantKnowledge's inclusion in freeware bundles and its collection of internet-usage information. A public execution from 8 December 2025 shows the established product components in a freeware installation chain. Comscore's current privacy page lists RelevantKnowledge among its research panels and describes opt-in participation. [^rk-mb][^rk-anyrun][^rk-comscore]

**Assessment:** The bundling route and durable runtime identifiers justify a focused sweep. This is a plausible discovery candidate, with no current enterprise hit rate established. PremierOpinion is related panel context and is not counted as a separate new hunt.

### Verified starting pivots

| Pivot | Source and interpretation |
| --- | --- |
| `rlvknlg.exe`, `rlvknlg32.exe`, `rlvknlg64.exe`, `rlservice.exe` | Components documented by Trend Micro and corroborated in a later public execution. Use exact names with product identity evidence. [^rk-trend][^rk-anyrun] |
| `\RelevantKnowledge\` under Program Files / Program Files (x86), plus service identifier `RelevantKnowledge` | Product-directory and service corroboration; architecture and version may change the full path. Trend Micro documents these within a larger bundler, not as the identity of every bundled component. [^rk-trend] |
| `PUP.Optional.RelevantKnowledge`; `Adware:Win32/RelevantKnowledge!MTB` | Vendor detection leads. A prevented installation remains separate from observed runtime execution. [^rk-mb][^rk-ms] |

### High-level hunt idea

Use the common 30-day starting window, extending for acquisition context if retained.

1. **Find product execution.** Search workspace process telemetry for the named components, corroborating the product directory, returned metadata or another component on the same endpoint.
2. **Identify continuing activity.** Separate installation, uninstall commands and blocked attempts from recurring service/runtime execution. Summarise users, first/last seen and active days.
3. **Review provenance and supporting activity.** Inspect parent installers, product-specific service or registry events, and attributable network activity where available. Network communication supports activity but does not reveal exactly what information was transmitted.
4. **Check consent and business approval.** Determine whether research-panel participation was intentional and permitted on that work device. Investigate additional unexpected payloads independently of the panel software.

**Minimum viable route:** Ingested `DeviceProcessEvents` or collected 4688/Sysmon 1, with corroborating product identity. File, registry, service, certificate and network evidence are optional; a missing service-creation event does not rule out an older installation.

### Positive finding, noise and severity

**High-confidence positive:** Corroborated RelevantKnowledge runtime activity. If unapproved, this supports a low-severity software/privacy finding. It does not prove credential theft, sensitive-data transmission or the contents of any collected data.

Intentional approved panel participation is a real alternative explanation, consistent with the operator's published model. [^rk-comscore] Do not equate a user's acceptance with corporate approval. Escalate separately evidenced sensitive-data exposure, malicious payload execution or material harmful changes. Do not import a sandbox's broad automated threat labels into a product-wide verdict.

## H005: Bright VPN

**Added:** Run 02.

### Hypothesis and likely value

Windows endpoints may have an unapproved Bright VPN installation whose bundled background component offers the device's connection for Bright Data's public-web collection service.

**Reported facts:** Bright VPN's FAQ says its free service is funded by letting Bright Data retrieve public web data through the user's connection, and describes a separate background service. Its partner programme advertises affiliate/pay-per-install distribution. Malwarebytes classifies the related BrightData software family as PUPs. [^bv-faq][^bv-partners][^bv-mb]

**Assessment:** There is a specific network-governance reason to investigate this product beyond generic VPN inventory. Distribution evidence makes a sweep plausible, but does not establish enterprise prevalence. This card identifies an application and capability; it does not infer proxy participation from IP reputation, connection fan-out or a shared vendor domain.

### Verified starting pivots

| Pivot | Source and interpretation |
| --- | --- |
| `Bright VPN.exe` within a `\Bright VPN\` directory | Observed branded runtime identity. Corroborate product metadata, path and execution context rather than matching every VPN application. [^bv-sample] |
| `net_updater32.exe` within `\Bright VPN\`, with `win_brightvpn.com` in the command line | Product-specific combination seen in public execution records. The argument is an identification marker; do not treat it as proof of a DNS lookup. The generic updater filename alone is insufficient. [^bv-sample] |
| Product `Bright VPN` / company `Bright Data Ltd.` metadata; `PUP.Optional.BrightData` detection | Sample metadata and a broader family detection are supporting leads, not verified signer evidence or unique proof of this product. [^bv-sample-2026][^bv-mb] |

The cited executions are from November 2025 and January 2026. Their artefacts are examples, not an exhaustive catalogue of current versions.

### High-level hunt idea

Use the common 30-day starting window and the retained history for installation context.

1. **Discover the specific product.** Search workspace process events for the branded runtime or the updater path-and-argument combination. Where command-line data is missing, use another corroborated product route rather than a generic updater-name match.
2. **Separate installation and operation.** Review parent/child execution and repeated desktop/service activity. Distinguish a blocked installer or old files from application execution during the window.
3. **Corroborate the background component.** Inspect available service, registry, file and process-associated network events. Record separately whether the desktop application, background component and any actual relaying behaviour are evidenced.
4. **Apply policy and assess impact.** Establish whether consumer VPN use and the associated connection-sharing arrangement were approved. Review unexpected descendants or material network effects when supported by telemetry.

**Minimum viable route:** Workspace-ingested `DeviceProcessEvents` or collected Windows/Sysmon process events with sufficient product/path/command-line evidence. Network, certificate, file and persistence records are enrichment.

### Positive finding, noise and severity

**High-confidence positive:** Corroborated execution of the Bright VPN product or its identified background component. Unapproved operation can support a low-severity software/network-sharing policy finding.

Deliberate approved use is a plausible benign explanation. The provider's disclosed model is not proof that this endpoint actually relayed third-party requests during the hunt window. Updater contact, the software name and a PUP alert do not establish malicious proxy use, a stolen session or endpoint compromise. Independently evidenced malicious payloads, sensitive-data exposure or material network impact warrant a separate severity assessment.

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

1. Read this file, its already-covered/excluded list and existing repository research first. Append **two distinct new candidates** to this same file, with stable IDs and an updated index. Do not repeat PC App Store or related aliases. Rebrands, aliases and minor variations of an existing candidate do not count as new hunts; retired IDs must not be reused.
2. For each candidate, record the source-backed finding, why a useful hit is plausible, precise starting pivots, a high-level hunt idea, Sentinel telemetry dependencies, benign explanations, and what a positive does and does not establish.
3. Separate reported facts from assessment and proposed hunting. Date the research and preserve source-age limitations. Update an existing card in place when new evidence changes its suitability, with a note in the run log.
4. Keep the scope at research and high-level hunt design unless query implementation is requested. Do not substitute Defender XDR Advanced Hunting for the required Log Analytics execution surface.
5. Record actual analyst feedback when supplied. Never turn a research candidate, blocked attempt or missing-data result into a claimed client finding. If two defensible candidates cannot be found, record the shortfall rather than pad the register.

## Run log

| Run | Date | Added | Research decisions |
| --- | --- | --- | --- |
| 01 | 2026-11-13 | Initially H001 OneLaunch; H002 PC App Store | OneLaunch scoped to remaining installations. H002 was subsequently retired following user feedback. OneStart excluded from the low-severity pair. No client results asserted. [^excluded-onestart] |
| 01 correction | 2026-11-13 | H003 Web Companion replaces H002 | User confirmed PC App Store is already well known. Removed its active card and added a persistent exclusion; preserved its retired ID. |
| 02 | 2026-11-13 | H004 RelevantKnowledge; H005 Bright VPN | Added two distinct product-specific hunts, including approval/consent checks and strict limits on claims about data collection or actual relaying. No client queries run. |

## Sources

All sources reviewed on **13 November 2026**. Undated pages are not represented as newly published research. Public sandbox observations establish sample-specific artefacts, not estate prevalence.

[^ol-mb]: Malwarebytes, [PUP.Optional.OneLaunch](https://www.malwarebytes.com/blog/detections/pup-optional-onelaunch), undated detection description.
[^ol-cybersift]: CyberSift, [Potentially Unwanted Software on Corporate Endpoints](https://www.cybersift.com/post/potentially-unwanted-software-on-corporate-endpoints). Page displays “Mar 27” without a year in the retrieved body; one corporate workstation reported.
[^ol-about]: OneLaunch, [About us](https://onelaunch.com/about-us), undated vendor user-scale claim.
[^ol-home]: OneLaunch, [Official homepage](https://onelaunch.com/), current download-withdrawal notice observed on the review date.
[^ol-sigma]: SigmaHQ, [DNS Query Request To OneLaunch Update Service](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/dns_query/dns_query_win_onelaunch_update_service.yml), 26 February 2024; status `test`, level `low`. Used as a documented pivot, not an implemented rule.
[^ms-stream]: Microsoft Learn, [Stream Microsoft Defender XDR data to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender), raw-table selection and unsupported TVM-table guidance.
[^ms-process]: Microsoft Learn, [Log Analytics DeviceProcessEvents reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/deviceprocessevents), workspace fields and semantics.
[^ms-cert]: Microsoft Learn, [Log Analytics DeviceFileCertificateInfo reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/devicefilecertificateinfo), certificate fields and SHA1 linkage.
[^ms-windows]: Microsoft Learn, [Windows agent-based Sentinel connectors](https://learn.microsoft.com/en-us/azure/sentinel/connect-services-windows-based), collection routes and destination tables.
[^ms-4688]: Microsoft Learn, [Event 4688: A new process has been created](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688), process creation and command-line audit prerequisites.
[^ms-sysmon]: Microsoft Learn, [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon), event types and collection capabilities.
[^ms-pua]: Microsoft Learn, [Detect and block potentially unwanted applications](https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus), PUA classification and prevention semantics.
[^excluded-onestart]: Expel, [The history of AppSuite: the certs of the BaoLoader developer](https://expel.com/blog/the-history-of-appsuite-the-certs-of-the-baoloader-developer/), original research linking OneStart and related products to the same developer operation; used for exclusion from this run's low-severity pair.

[^wc-mb]: Malwarebytes, [PUP.Optional.WebCompanion](https://www.malwarebytes.com/blog/detections/pup-optional-webcompanion), undated detection description.
[^wc-faq]: Adaware Web Companion, [Official FAQ](https://www.webcompanion.com/en/help.php), undated; bundled distribution and inadvertent acceptance described by the publisher.
[^wc-trustwave]: Trustwave, [2023 Manufacturing Threat Landscape](https://www.trustwave.com/hubfs/Web/Library/Documents_pdf/2023_Trustwave_Manufacturing_Sector_Threat_Landscape.pdf), printed page 32 / PDF page 34; organisational WebCompanion delivery observations.
[^wc-trend]: Trend Micro, [PUA.MSIL.WebCompanion.AE](https://www.trendmicro.com/vinfo/us/threat-encyclopedia/malware/PUA.MSIL.WebCompanion.AE), historical sample analysis; product components and installation paths.
[^wc-ms]: Microsoft Security Intelligence, [PUA:Win32/WebCompanion](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=PUA%3AWin32%2FWebCompanion&threatId=403868), 21 August 2023; detection naming only.
[^rk-mb]: Malwarebytes, [PUP.Optional.RelevantKnowledge](https://www.malwarebytes.com/blog/detections/pup-optional-relevantknowledge), undated description of freeware bundling and internet-usage measurement.
[^rk-trend]: Trend Micro, [Adware.Win32.FusionCore.AD](https://www.trendmicro.com/vinfo/us/threat-encyclopedia/malware/adware.win32.fusioncore.ad), 6 February 2020; sample first observed in April 2019. RelevantKnowledge is one component of this analysed bundle.
[^rk-anyrun]: ANY.RUN, [Free Video Cutter Joiner installation chain](https://any.run/report/f5a5c6a0b882cfc24f87457c53c508d67b9d6e8c5bbe9a60278836dbd953444f/5f6e38ca-7d06-419d-b6c7-10216ea7bb18), 8 December 2025; RelevantKnowledge runtime and service execution, used as sample evidence only.
[^rk-comscore]: Comscore, [Privacy](https://www.comscore.com/About/Privacy), current undated corporate policy identifying its research panels and describing opt-in participation.
[^rk-ms]: Microsoft Security Intelligence, [Adware:Win32/RelevantKnowledge!MTB](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=Adware%3AWin32%2FRelevantKnowledge%21MTB&ThreatID=413972), 5 December 2023; detection naming only.
[^bv-faq]: Bright VPN, [Official FAQ](https://brightvpn.com/faq), current undated explanation of public-web collection through users' connections and its background service.
[^bv-partners]: Bright VPN, [Partner programme](https://brightvpn.com/partners), undated affiliate/pay-per-install distribution description; marketing user counts are not treated as enterprise prevalence.
[^bv-mb]: Malwarebytes, [PUP.Optional.BrightData](https://www.malwarebytes.com/blog/detections/pup-optional-brightdata), undated detection description covering the broader Bright Data software family.
[^bv-sample]: ANY.RUN, [Bright VPN installer execution](https://any.run/report/1929fa577e90828053bfa6e9524837b75ddc2bb8c00578d7ef6754cef37e25ac/1a0281d9-ccbb-42c6-ab9f-30d742d5e5a2), 6 November 2025; runtime/updater paths and product argument, not a product-wide maliciousness verdict.
[^bv-sample-2026]: ANY.RUN, [BrightVPN-Setup-1.572.298.exe](https://any.run/report/1929fa577e90828053bfa6e9524837b75ddc2bb8c00578d7ef6754cef37e25ac/b819185f-9c09-4be2-9e0a-2f117b34e842), 31 January 2026; sample metadata and related component activity.
