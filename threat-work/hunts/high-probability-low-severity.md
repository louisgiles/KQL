# High-probability, low-severity threat hunts

**Last researched:** 13 November 2026  
**Latest research run:** 09 — 08:00 evidence corrections, final ranking and identifier audit; no new packs
**Active candidates:** Twelve low-severity H packs (H001, H003, H004, H005, H007, H008, H009, H010, H011, H012, H013, H014), and three escalation E packs (E001, E002, E003). H002 and H006 retired.
**Scheduled research:** Hourly through the final scheduled run at 08:00 Europe/London on 14 November 2026  
**Execution surface:** Microsoft Sentinel / Log Analytics workspaces only  
**Status:** Researched hunt hypotheses; no client queries have been run or results claimed.

## Purpose and selection standard

Prioritise high-probability, high-fidelity, low-initial-severity findings that can be investigated through Sentinel Log Analytics. **PDF Polish, PDF Spark and Shift Browser are confirmed previous hits** used as calibration for sibling software and advertising routes. Wave Browser and ClickFix are already known too. Do not re-count any of them as new.

**High fidelity means confidence in the observed application or behaviour.** Whether it is unwanted depends on client policy and context. Low severity applies to the finding being investigated, not every possible consequence of the software. Independent evidence of malicious execution changes the assessment.

The likelihood of a hit across clients is not yet measured. Selection below uses published distribution evidence, real enterprise observations and identifiable artefacts; it does not promise a hit or assign invented percentages. Existing, persistent software is in scope even when the supporting research is older than seven days.

## Already covered or excluded

| Subject | Decision |
| --- | --- |
| PC App Store and VeryFast-related pivots | Already well known, confirmed by the user on 13 November 2026. H002 retired; do not propose aliases or minor variants as new candidates. Web Companion replaces its slot in Run 01. |
| PDF Polish, PDF Spark, Shift Browser | **Confirmed previous hits.** PDF Polish version metadata identifies Jia Hao; an analysis of Doc Convert Wizard links the same company field to PDFPolish, FoodFormula and ProfessionalConverter folders. G DATA reports DocConvertWizard and Food/Meal Formula as Projextor malware, **but does not name PDF Polish**: this is a lead, not proven family attribution. PDF Spark has Mainstay Crypto LLC and Crowd Sync LLC publisher identities; Unit 42 lists both under OneBrowser Signers without naming PDF Spark. Authentic Shift is Shift Technologies Inc. Advertising similarity does not prove shared ownership. [^pdf-polish][^pdf-spark][^pdf-control][^shift][^pdf-signer][^r04-gdata] |
| Wave Browser, ClickFix | Already known; excluded as new. |
| OneStart / BaoLoader-associated activity | Not suitable for a routine low-severity PUP entry. [^excluded-onestart] |
| H006 HollowMare | Retired from the low-severity list in Run 04, re-filed as E003 after the Unit 42 signer evidence. This historical ID is not reused. [^hollow][^pdf-signer] |

Retired IDs are not reused. Twelve active low-severity packs are indexed below; H006 was reclassified as E003, not counted as new.

## Hunt index — low-severity packs

**Likelihood tiers are evidence categories, not client hit probabilities.** A = measured recent activity (**provider-level** when the count is not product-specific); B = a dated real-environment report or a currently offered product without measured prevalence; C = older/undated sources or sandbox-only evidence. **A live download page alone is insufficient evidence for a NEW pack under Review 008; older packs are retained with limitations.** Source date and installation date are different. **Run order** favours direct product activity, specificity and evidence age over marketing volume.

| Run order | ID | Candidate | Tier | Newest evidence and limitation | Added | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [H005](#h005-bright-sdk--luminati-sdk-in-host-apps) | Bright/Luminati SDK in host apps | **A (provider-level)** | 30 Sep 2026: ~1.47m Gen-protected active Windows users observed 1–15 Sep; embedded SDKs excluded | Run 02, widened 03 | Finished: identifiable SDK; no current corporate prevalence |
| 2 | [H009](#h009-hola-browser-and-desktop-vpn) | Hola Browser / desktop VPN | **A (provider-level)** | 30 Sep 2026: ~664k provider-associated Windows users observed 1–15 Sep; not branded-app hits | Run 05 | Finished: branded execution; miner findings escalate |
| 3 | [H007](#h007-dragon-boss-solutions-browser-updaters) | Dragon Boss browser/updater family | **A** | 14 Apr 2026: 23,565 sinkhole source IPs including 2,223 UK; not devices | Run 04 | Finished: product presence; separate AV-removal escalation |
| 4 | [H010](#h010-honeygain-windows-bandwidth-sharing-app) | Honeygain Windows | **A (provider-level)** | 30 Sep 2026: ~68k provider-associated Windows users observed 1–15 Sep; not relay proof | Run 05 | Finished: branded execution; relay unproven |
| 5 | [H008](#h008-infatica-p2b-proxy-component) | Infatica P2B component | **A (provider-level)** | 30 Sep 2026: ~56k Gen-protected active Windows users observed 1–15 Sep; not P2B-specific | Run 04 | Finished: product execution; relay unproven |
| 6 | [H011](#h011-iobit-driver-booster-for-windows) | IObit Driver Booster 14 | **B (live download)** | 13 Nov 2026: official product download live; 16 Sep 2026 release; enterprise prevalence unknown | Run 07 | Finished: branded process/path; separate PUP detection |
| 7 | [H012](#h012-utorrent-classic-for-windows) | µTorrent Classic Windows | **B (live download)** | 13 Nov 2026: official Classic download live; 2021 PUA bundle classification is historical | Run 07 | Finished: process/path corroboration; transfers unproven |
| 8 | [H013](#h013-outbyte-driver-updater) | Outbyte Driver Updater | **B (live download)** | 13 Nov 2026 official download live; July 2026 removal guidance; no estate prevalence measured | Run 08 | Finished: product path/metadata; generic process paired |
| 9 | [H014](#h014-driverpack-online-and-notifier) | DriverPack Online and Notifier | **B (live download)** | 13 Nov 2026 official download live; 2018 Notifier artefacts historical | Run 08 | Finished: branded runtime plus product metadata; bundles assessed separately |
| 10 | [H003](#h003-adaware-web-companion) | Adaware Web Companion | **B (live download)** | 13 Nov 2026: official Windows download page live; business report from 2023 | Run 01 replacement | Finished: typed identifiers; current estate use unmeasured |
| 11 | [H001](#h001-onelaunch) | OneLaunch | **B (residual)** | 27 Mar 2026 corporate sighting; new downloads withdrawn | Run 01 | Finished: distinctive runtime; remaining installations only |
| — | [H004](#h004-relevantknowledge) | RelevantKnowledge | **C** | 8 Dec 2025 sandbox; live privacy-panel listing ≠ current installs | Run 02 | Incomplete: recent real-world presence evidence |

**Status:** Finished means sourced, product-specific standalone identifier without command lines, typed table and explicit match meaning. It does not mean verified tenant execution. No tenant data queried in any run.

**Applies to every card:** Start with 30 days of **actually ingested** Windows process events in **Sentinel Log Analytics** (streamed `DeviceProcessEvents` or collected Windows 4688 / Sysmon 1). Extend to 90 days only where retained. Confirm product identity beyond a filename; version metadata is not a validated signer. File/registry/certificate/network/security-product data are optional where ingested. Distinguish installer, prevented execution, ongoing runtime, historical residue and verified traffic. Low severity refers only to a software-policy finding *without separate malicious behaviour*. Apply each client's approval policy. No client results have been queried or claimed.

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

**Assessment (tier B):** CyberSift's **27 March 2026** report identifies OneLaunch on a real corporate workstation—the most recent dated organisational observation in the original register. The date is the **article publication**, not a proven installation date. OneLaunch has withdrawn new downloads; remaining installations are the target, not a proven growing campaign.

### Verified starting pivots

| Pivot | Source and interpretation |
| --- | --- |
| `OneLaunch.exe` | Product process identified in SigmaHQ's original OneLaunch updater rule. Use as a discovery seed, then corroborate identity. [^ol-sigma] |
| `update.onelaunch.com` | SigmaHQ pairs this exact DNS name with `OneLaunch.exe`. Process-attributed updater traffic is much stronger than an unattributed DNS hit. [^ol-sigma] |
| `PUP.Optional.OneLaunch` | Vendor detection-name lead. Check whether the record concerns an installed application, a block or historical remediation. [^ol-mb] |

**Typed identifier table (Run 06):** SigmaHQ's 26 February 2024 rule pairs the executable and updater hostname; a named detection is not execution.

| Product | Identifier type | Exact value | Log Analytics table.column, if ingested | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| OneLaunch | process | `OneLaunch.exe` | `DeviceProcessEvents.FileName` | **standalone** branded execution seed, confirm metadata/path | [^ol-sigma] |
| OneLaunch | updater DNS | `update.onelaunch.com` | collected Sysmon 22 in `WindowsEvent.EventData`, or suitable ingested process-attributed DNS field | **pair with OneLaunch.exe**; DNS-only is not program execution | [^ol-sigma] |
| OneLaunch | detection | `PUP.Optional.OneLaunch` | `SecurityAlert.AlertName` or ingested `DeviceEvents.AdditionalFields` | **standalone detection lead**, verify outcome | [^ol-mb] |

**Finished boundary:** Real organisational observation dated 27 March 2026 plus process-identification evidence. Low severity requires corroborated unapproved execution. Neither a historical block nor a DNS request proves active installation.

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

**Assessment (tier B, live distribution):** The bundled route and business observations remain relevant but historical. The publisher was still offering a Windows download on **13 November 2026**; this proves an available distribution route, **not** installation prevalence on managed devices. [^r06-wc-live]

### Verified starting pivots

| Pivot | Source and interpretation |
| --- | --- |
| `WebCompanion.exe`; supporting `WebCompanion.Loader.exe` and `WebCompanionInstaller.exe` | Component names in Trend Micro's original analysis. Keep installed runtime, loader and installer outcomes distinct. [^wc-trend] |
| `\Lavasoft\Web Companion\Application\` | Historical product-directory suffix documented under Program Files. Inspect returned paths; do not make this old location the only discovery route. [^wc-trend] |
| `PUP.Optional.WebCompanion`; `PUA:Win32/WebCompanion` | Malwarebytes and Microsoft detection-name leads, subject to action/remediation review. [^wc-mb][^wc-ms] |

**Typed identifier table (Run 06):** Trend Micro's original sample lists the exact product path; directory and metadata must be checked on modern versions.

| Product | Identifier type | Exact value | Log Analytics table.column, if ingested | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| Web Companion | process | `WebCompanion.exe` | `DeviceProcessEvents.FileName` | **standalone** branded runtime candidate; corroborate path/product | [^wc-trend] |
| Web Companion | historical installed executable path | `%Program Files%\Lavasoft\Web Companion\Application\WebCompanion.exe` | `DeviceProcessEvents.FolderPath` | **standalone** combined path/name, expand variable as appropriate | [^wc-trend] |
| Web Companion | loader component | `WebCompanion.Loader.exe` | `DeviceProcessEvents.FileName` | **standalone** distinct component candidate; establish role | [^wc-trend] |
| Web Companion | installer-labelled component | `WebCompanionInstaller.exe` | `DeviceProcessEvents.FileName` or `DeviceFileEvents.FileName` | **standalone** install lead, not proof of runtime | [^wc-trend] |
| Web Companion | vendor detection | `PUP.Optional.WebCompanion` | `SecurityAlert.AlertName` or ingested `DeviceEvents.AdditionalFields` | **standalone** detection lead, inspect block/remediation | [^wc-mb] |

**Finished boundary:** Current available download and product-specific executable(s), not independently measured current enterprise adoption. Authorised user installation is possible; unwanted browser changes must be shown rather than presumed.

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

**Typed identifier table (Run 06):** Trend Micro's historical FusionCore bundle documents these exact product files and a service string; it is **not 2026 prevalence evidence**.

| Product | Identifier type | Exact value | Log Analytics table.column, if ingested | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| RelevantKnowledge | process | `rlvknlg.exe` | `DeviceProcessEvents.FileName` | **standalone** distinctive process seed; corroborate product | [^rk-trend] |
| RelevantKnowledge | service executable | `rlservice.exe` | `DeviceProcessEvents.FileName` | **standalone** executable seed, confirm product path | [^rk-trend] |
| RelevantKnowledge | installed executable path | `%Program Files%\RelevantKnowledge\rlvknlg.exe` | `DeviceProcessEvents.FolderPath` | **standalone** combined path/name, historical sample | [^rk-trend] |
| RelevantKnowledge | service label | `RelevantKnowledge` | collected service-creation event name / `DeviceEvents.AdditionalFields` | **pair with product path/process**; change events are not service inventory | [^rk-trend] |
| RelevantKnowledge | detection | `PUP.Optional.RelevantKnowledge` | `SecurityAlert.AlertName` or ingested `DeviceEvents.AdditionalFields` | **standalone** detection lead, check prevention/remediation | [^rk-mb] |

**Incomplete — likelihood:** Comscore presently lists the RelevantKnowledge research panel, and the 8 December 2025 sandbox shows execution **inside a sandbox**; neither is a recent real-world distribution/endpoint sighting. The identifier table is finished, but the pack cannot meet the current-presence standard. [^rk-anyrun][^r06-rk-panel]

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

## H005: Bright SDK / Luminati SDK in host apps

**Added:** Run 02 as Bright VPN; widened **in place** in Run 03 per Review 001. Bright VPN and EarnApp remain example host apps rather than fresh candidate IDs.

**Hypothesis:** Third-party Windows utilities can embed the **Bright SDK**, formerly **Luminati SDK**, allowing an unapproved background component on a managed endpoint without a Bright VPN installation. A capability for public-web collection using participant connections is documented by Bright VPN; evidence of the component does **not** prove actual relaying on a specific device. [^bv-faq][^bv-partners][^bv-mb]

**Evidence (tier A for observed Bright Data Windows software at provider level; embedded SDK prevalence remains unmeasured):** On **13 November 2026**, the vendor's current programme page listed Windows hosts WiFi Mouse, Megacubo TV, Daemon Tools and DriverHub, and its Windows-capable tooling FAQ was updated **22 July 2026**. Those are publisher marketing claims about supported integrations, **not proof any present build on a client ships the SDK**. [^r06-sdk-live][^r06-sdk-tools] A **June 2023** Mouse Server execution shows SDK inside an unrelated application's directory. Bright VPN ANY.RUN reports **6 Nov 2025** and **31 Jan 2026** share SHA-256 `1929fa577e90828053bfa6e9524837b75ddc2bb8c00578d7ef6754cef37e25ac`: **one installer detonated twice**, not two builds or distinct infections. No SDK-only business prevalence measured. [^sdk-mouse][^bv-sample][^bv-sample-2026]

**Newer measured evidence:** Gen Digital published its **30 September 2026** analysis of active protected Windows systems observed **1–15 September 2026**: approximately **1.47 million users had software associated with Bright Data**, the largest provider footprint in that sample. Gen explicitly excluded SDKs embedded inside other applications. This strengthens the case for a Bright-branded software sweep, **not** a specific probability of finding the embedded SDK in an MSSP client. Neither presence nor publisher-level measurement establishes traffic relaying. [^r05-gen]

| Pivot | Evidence and bounds |
| --- | --- |
| `net_updater32.exe` / `net_updater64.exe` **in any directory** | SDK candidates. Verify via version product `Bright SDK` or `Luminati SDK`, host, related modules and actual signer where available. Never use a loose updater filename as final identification. Vendor integration guide redirects behind authentication and could not be read in full. [^sdk-guide][^sdk-mouse] |
| `"C:\Program Files\Mouse Server\net_updater32.exe" --install win_wifimouse.necta.us` | **Exact ANY.RUN Process information** command, PID 2228, **29 Jun 2023**, with `Company: Luminati Networks Ltd.` and `Description: Luminati SDK Updater`. Its **Modules** section lists `c:\program files\mouse server\lum_sdk32.dll`. `win_wifimouse.necta.us` identifies this **host**; `--install win_<app-id>` is a sample-supported **shape**, not mandatory on every build. [^sdk-mouse] |
| `Bright VPN.exe` (runtime), `brightvpn_installer.exe` (installer), `net_updater32.exe` (candidate SDK) | Names visible in **2025** public report. The formerly claimed `\Bright VPN\` plus `win_brightvpn.com` path/argument is **UNCONFIRMED** by the publicly visible process details: do **not** treat it as verified. [^bv-sample][^bv-sample-2026] |
| `PUP.Optional.BrightData` | Broad product-family detection lead, not proof of a running SDK or proxy relay. [^bv-mb] |

**Typed identifier table (Run 06):** The 2023 ANY.RUN **Process information** provides the path, description and command-line sample; **Modules** lists the DLL. An undated file-reference page supplies the service name. The full publisher C/C++ guide redirects to authentication and is **not used as an independent source for new identifiers**.

| Product | Identifier type | Exact source value | Log Analytics table.column, if ingested | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| Bright/Luminati SDK | distinctive module/file | `lum_sdk32.dll` | `DeviceFileEvents.FileName` for **file event only**; actual loaded module needs separate module telemetry | **standalone SDK file lead**, not execution | [^sdk-mouse] |
| Luminati SDK | version description | `Luminati SDK Updater` | `DeviceProcessEvents.ProcessVersionInfoFileDescription` | **pair with net_updater32.exe**, sample description | [^sdk-mouse][^r06-sdk-file] |
| Bright/Luminati SDK | generic updater | `net_updater32.exe` | `DeviceProcessEvents.FileName` | **pair with SDK metadata/DLL/host folder**; never alone | [^sdk-mouse][^r06-sdk-file] |
| Luminati SDK in Mouse Server | observed exact process path | `C:\Program Files\Mouse Server\net_updater32.exe` | `DeviceProcessEvents.FolderPath` | **standalone path+name** for this sample host; don't require Mouse Server elsewhere | [^sdk-mouse] |
| Luminati SDK in Mouse Server | observed installation argument | `--install win_wifimouse.necta.us` | `DeviceProcessEvents.ProcessCommandLine`, if populated | **pair with updater**; optional, not required | [^sdk-mouse] |
| Bright VPN host | service identifier on file-reference page | `luminati_net_updater_win_brightvpn_com` | collected service-install name or ingested `DeviceEvents.AdditionalFields` | **standalone service lead**, corroborate actual executable | [^r06-sdk-file] |
| EarnApp (Bright Data host) | historical branded executable and path | `earnapp.exe` in `C:\Program Files (x86)\EarnApp\` | `DeviceProcessEvents.FolderPath` | **standalone combined path and product filename**; version 1.597.152 only; not a relaying verdict | [^r09-earnapp] |
| EarnApp updater | historical generic updater in product folder | `net_updater32.exe` in `C:\Program Files (x86)\EarnApp\` | `DeviceProcessEvents.FolderPath` | **pair with EarnApp folder/product**; filename alone not valid | [^r09-earnapp] |
| Bright Data family | detection | `PUP.Optional.BrightData` | `SecurityAlert.AlertName` / ingested `DeviceEvents.AdditionalFields` | **standalone detection lead**, can refer to VPN not embedded SDK | [^bv-mb] |

**Finished boundary:** Exact host-specific service/path or SDK DLL provides a no-command-line identification lead; confirm actual updater/host execution before reporting active use. A DLL file event, installer, or product-marketing example does not establish proxy traffic or a current enterprise installation.

**High-level Sentinel hunt:** Sweep available process-creation telemetry for both updater filenames at **all paths**; corroborate product and embedded host. Use recorded argument `win_<app-id>` when available and associate it with the host application. Optional ingested files, services, registry and process-attributed network events clarify continued activity. Separate a blocked installer, executable runtime, and actual relaying. Check whether the host *and SDK* are approved.

**Noise/escalation:** Approved consumer software may be benign. A vendor domain, updater, service or PUA flag alone does not establish malicious proxy operation. Escalate independently verified malware execution, harmful outbound usage or sensitive-data exposure.

## H007: Dragon Boss Solutions browser updaters

**Hypothesis, tier A (L3):** Huntress reported on **14 April 2026** that Dragon Boss Solutions-signed browsers/updaters were active in real environments. Its 24-hour sinkhole received connections from **23,565 unique IPs across 124 countries, 2,223 UK**. IP counts are not device or estate prevalence. Vendors had called the software PUP/adware, **but Huntress also observed security-tool removal via malicious updates**; the latter is an incident, not routine PUP presence. [^r04-huntress]

**Exact identifier table.** Huntress sections “Variations of executables” Table 7, “File system artifacts”, “Code signing”, “Scheduled tasks” and “WMI artifacts”. An exact filename is a seed; verify path/signer where possible.

| Product | Identifier type | Exact source value | Log Analytics table.column | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| Family | certificate signer | Dragon Boss Solutions LLC | DeviceFileCertificateInfo.Signer linked on SHA1 to DeviceProcessEvents | standalone family identifier; requires certificate ingestion | [^r04-huntress] |
| Chromstera Browser | process name | ChromsteraUpdater.exe | DeviceProcessEvents.FileName | standalone seed; validate software identity | [^r04-huntress] |
| Chromstera Browser | folder | C:\Program Files (x86)\Chromstera Browser Solutions\Chromstera Browser | DeviceProcessEvents.FolderPath | pair with ChromsteraUpdater.exe | [^r04-huntress] |
| Artificius Browser | process name | ArtificiusUpdater.exe | DeviceProcessEvents.FileName | standalone seed; validate identity | [^r04-huntress] |
| Artificius Browser | folder | C:\Program Files (x86)\Artificius Browser Solutions\Artificius Browser | DeviceProcessEvents.FolderPath | pair with ArtificiusUpdater.exe | [^r04-huntress] |
| World Wide Web | process name | WorldWideWeb.exe | DeviceProcessEvents.FileName | standalone seed; validate identity | [^r04-huntress] |
| World Wide Web | folder | C:\Program Files (x86)\World Wide Solutions\World Wide Web\ | DeviceProcessEvents.FolderPath | pair with WorldWideWeb.exe | [^r04-huntress] |
| Updater in the `Web Genius` folder (product name unverified) | process name | UniversalUpdater.exe | DeviceProcessEvents.FileName | pair with Web Genius folder (generic name) | [^r04-huntress] |
| `Web Genius` directory (not verified product branding) | folder | C:\Program Files (x86)\Web Genius Solutions\Web Genius | DeviceProcessEvents.FolderPath | pair with UniversalUpdater.exe | [^r04-huntress] |
| Additional updater | process name | ReadySpaceThree.exe | DeviceProcessEvents.FileName | pair with `FutureSpaceThree` folder or verified signer | [^r04-huntress] |
| Additional updater | historical path in Huntress executable table | C:\Program Files (x86)\FutureSpaceThreeSolutions\FutureSpaceThree | DeviceProcessEvents.FolderPath | pair with ReadySpaceThree.exe | [^r04-huntress] |
| Additional updaters | process names | WinDefenseThree.exe; RaceCarTwo.exe; TableBoatTwo.exe | DeviceProcessEvents.FileName | pair with source-described corresponding program folder or signer | [^r04-huntress] |
| **Malware escalation** | scheduled tasks | ClockSetupWmiAtBoot; RemoveClockPeriodic | DeviceEvents.AdditionalFields when ActionType=ScheduledTaskCreated, or ingested task events | standalone malicious-chain lead | [^r04-huntress] |
| **Malware escalation** | WMI consumers | MbRemovalMbSetupKillConsumer; MbRemovalMbSetupKillConsumerTrace | DeviceEvents.AdditionalFields when ActionType=WmiBindEventFilterToConsumer | standalone malicious-chain lead | [^r04-huntress] |
| **Malware escalation** | scripts | ClockRemoval.ps1; ClockRemoval-WmiBoot.ps1 | DeviceFileEvents.FileName | standalone malicious-chain lead with contextual verification | [^r04-huntress] |
| **Malware escalation** | folder | %SystemRoot%\System32\config\systemprofile\AppData\Local\WMILoad\ | DeviceFileEvents.FolderPath | pair with task, script or WMI lead | [^r04-huntress] |

**Hunt:** Look for process execution in the 30-day retained window, validate publisher/product or distinctive folder, then inspect any collected task, WMI, AV-exclusion, file and installer events. Process names alone do not demonstrate a current install; browser cache files and DNS-only traffic are not positives. **A confirmed matched process proves family presence, not that the endpoint received the AV killer.** The ClockRemoval/WMI/Defender-disable chain is escalation-grade. Legitimate intentional third-party browser adoption is possible, subject to client approval, but does not make security-control disabling benign.

## H008: Infatica P2B proxy component

**Hypothesis, tier A (provider-level, L4):** Infatica SDK/P2B may be installed alongside consumer software. Malwarebytes classifies it as a potentially unwanted proxy service that may be bundled. GridinSoft **updated an account on 11 August 2026** describing reports following codec installs, but this is not measured enterprise prevalence or proof the official K-Lite package bundles it. [^r04-infatica-mb][^r04-infatica-grid]

**Newer measured evidence:** Gen Digital's **30 September 2026** report observed around **56,000 active Gen-protected Windows users associated with Infatica between 1 and 15 September 2026**. This is a provider-level count that excludes embedded SDKs and does **not** show 56,000 `infatica-service-app.exe` installations, proxy relays or client findings. [^r05-gen]

**Exact identifier table.** File.net “File information” gives the executable, product names and example directories. The digital signer was **not independently verified**; do not treat the claimed publisher as a certificate value.

| Product | Identifier type | Exact source value | Log Analytics table.column | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| Infatica SDK/P2B | process name | infatica-service-app.exe | DeviceProcessEvents.FileName | standalone distinctive executable seed; corroborate host path | [^r04-infatica-file] |
| Infatica SDK/P2B | folder | C:\Program Files (x86)\Infatica P2B\ | DeviceProcessEvents.FolderPath | pair with infatica-service-app.exe | [^r04-infatica-file] |
| Infatica-m | sample folder | C:\Users\Eldar\AppData\Local\Infatica-m\ | DeviceProcessEvents.FolderPath | pair with infatica-service-app.exe; Eldar is an example username, not a fixed user predicate | [^r04-infatica-file] |
| Infatica | product label | Infatica SDK; Infatica-m; Infatica Service | DeviceProcessEvents.ProcessVersionInfoProductName where present | pair with the Infatica executable; file.net gives the labels but not exact field mapping | [^r04-infatica-file] |
| Infatica | vendor detection | PUP.Optional.Infatica | Ingested DeviceEvents.AdditionalFields or SecurityAlert.ExtendedProperties when label is present | standalone **detection** lead, not confirmed runtime | [^r04-infatica-mb] |

**Hunt:** Confirm observed process execution within 30 retained days, identify the host software and program path, then correlate available process-attributed traffic, startup or service creation. A process plus distinctive path establishes component execution **not proven third-party proxy relay**. Intentional opt-in software and authorised research tools are possible benign explanations; client approval is separate. Escalate corroborated covert traffic relaying, installed loader or related compromise. **Declined unsupported identifiers:** DigitalPulseService.exe is not proven Infatica; the service name and infatica_agent.exe variant are unverified here; the Sophos support page and FreeFixer pages did not open fully.

## H009: Hola Browser and desktop VPN

**Hypothesis, tier A (provider-level, L5):** Hola's Windows Browser and desktop VPN remain available on **13 November 2026**. Gen Digital published **30 September 2026** measurements of about **664,000 active Windows users with software associated with Hola** on active Gen-protected Windows systems observed **1–15 September 2026**. This is *not* Hola Browser-specific execution, client/UK-estate prevalence, or proof of relayed traffic; the research excludes embedded SDKs. This branded Windows-product hunt is distinct from H005's embedded Bright SDK despite the related proxy business model. [^r05-gen][^r05-hola-vendor]

**Exact identifier table** — original Sophos “Here's looking at me.exe” analysis, Hola product listing and an older installer sample; a source-observed path is not a fleet-level installation count.

| Product | Type | Exact value | Log Analytics table.column | Match rule | Source |
| --- | --- | --- | --- | --- | --- |
| Hola Windows branded app | folder used by running program | `C:\Program Files\Hola\` | `DeviceProcessEvents.FolderPath` | **standalone** path-specific family execution lead, validate version/product and child process | [^r05-hola-sophos] |
| Hola Browser | advertised Windows version | `1.258.330` | `DeviceProcessEvents.ProcessVersionInfoProductVersion` **when populated** | pair with Hola executable/path; website's version is **not** independently observed process metadata | [^r05-hola-vendor] |
| Hola Browser | installer file | `Hola-Browser.exe` | `DeviceProcessEvents.FileName` or `DeviceFileEvents.FileName` | pair with product and ancestry; **installer-stage only**, old sample | [^r05-hola-installer] |
| **Escalation** | miner-specific file hash | `e3541caf708c075f0bb22fc68b03acd8457fea7cf0732ea935b1eb016d1c7721` | `DeviceProcessEvents.SHA256` / `DeviceFileEvents.SHA256` where populated | **standalone sample hash**, not every Hola version | [^r05-hola-sophos] |
| **Escalation** | unexpected service binary path | `C:\Program Files\Hola\HolaMonitorService.exe` | `DeviceProcessEvents.FolderPath` | **standalone combined path+file** miner-stage lead | [^r05-hola-sophos] |
| **Escalation** | registered service | `hola_monitor_svc` | collected Windows Service-install event fields or `DeviceEvents.AdditionalFields` if ingested | **standalone** malicious-chain *creation event* lead; not proof current service state | [^r05-hola-sophos] |

**Hunt:** Across available Sentinel process creation events, find executed Hola-folder processes and corroborate the branded application against the client's software policy. Free Hola may offer peer contribution; Premium usage need not—do not infer relay or maliciousness from branded software alone. **Separate incident pivot:** Sophos documented an unexpected signed-delivery-pipeline component, later identified as a cryptominer, which added a Defender exclusion and registered `hola_monitor_svc`; Hola told Sophos the distribution problem was fixed. A matching miner hash/service or control tampering warrants escalation, not a low-severity PUP outcome. Intentional authorised consumer VPN use can be benign. [^r05-hola-vendor][^r05-hola-sophos]

## H010: Honeygain Windows bandwidth-sharing app

**Hypothesis, tier A (provider-level, L7):** Gen Digital's **1–15 September 2026** active protected Windows dataset found approximately **68,000 active users with software associated with Honeygain**; neither client prevalence nor confirmed proxy relaying is measured. Honeygain's Windows app was still available **13 November 2026**; the vendor updated its support page **22 October 2026**. It is a distinct user-facing product, not an H005/H008 SDK alias. [^r05-gen][^r05-hg-vendor]

**Exact identifier table** — product-specific files from PaysFair's **24 September 2026** “What the Honeygain installer puts on your PC” static extraction; **a competitor's report, no sample execution**. Folder/key from Honeygain's official “Clean reinstall” steps. The strings are useful seeds, not proven executed processes until seen in an ingested workspace.

| Product | Type | Exact value | Log Analytics table.column | Match rule | Source |
| --- | --- | --- | --- | --- | --- |
| Honeygain UI | installed executable name in file table | `Honeygain.exe` | `DeviceProcessEvents.FileName` | **standalone** branded runtime candidate; confirm actual process/product | [^r05-hg-static] |
| Honeygain updater | executable name in file table | `HoneygainUpdater.exe` | `DeviceProcessEvents.FileName` | pair with Honeygain product identity/path; updater not relay | [^r05-hg-static] |
| Honeygain engine | DLL name in installer | `hgwin.dll` | `DeviceFileEvents.FileName` | pair with Honeygain product folder; file event is not DLL-load evidence | [^r05-hg-static] |
| Honeygain | installer file | `Honeygain_install.exe` | `DeviceProcessEvents.FileName` or `DeviceFileEvents.FileName` | **standalone installer lead**, not runtime proof | [^r05-hg-static][^r05-hg-sample] |
| Honeygain older runtime | version 0.10.7.0 application directory and process name | `C:\Users\UserName\AppData\Roaming\Honeygain` and `Honeygain.exe` | `DeviceProcessEvents.FolderPath` | **standalone branded process plus folder**, with variable username; old version and not current install proof | [^r09-hg-path] |
| Honeygain | local folder | `%localappdata%\Honeygain`; `%appdata%\Honeygain` | `DeviceFileEvents.FolderPath` or `DeviceProcessEvents.FolderPath` when appropriate events exist | pair with process; vendor describes **leftovers** too | [^r05-hg-vendor] |
| Honeygain | user registry key | `HKEY_CURRENT_USER\Software\Honeygain` | `DeviceRegistryEvents.RegistryKey` where collected | pair with process; a change event is not current inventory | [^r05-hg-vendor] |

**Hunt:** Confirm execution of branded software via Sentinel process telemetry in a 30-day window, identify the user/authorised installation, and optionally correlate network, file and registry events if ingested. `Honeygain.exe` execution establishes product use, **not** that `hgwin.dll` loaded or that third-party traffic flowed. Escalate covert installation, demonstrated traffic relay inconsistent with client policy, or independently evidenced malware. A knowingly authorised earning app could be benign under policy. PaysFair's installer and the public sandbox sample have the **same hash**, so they are not two builds or two observed infections. [^r05-hg-static][^r05-hg-sample]

## H011: IObit Driver Booster for Windows

**Hypothesis, tier B (Review 007 L7):** An unapproved consumer driver updater may be installed on managed Windows endpoints. **Likely-now evidence:** IObit announced Driver Booster **14 on 16 September 2026**, and the official free Windows download was live **13 November 2026**. Malwarebytes labels IObit's specific product `PUP.Optional.iObitDriverBooster`, a PUP not proof of malware. This must **not** be confused with Energizer Softech's different `PUP.Optional.DriverBooster`. Distribution is current; estate prevalence is not measured. [^r07-iobit-press][^r07-iobit-live][^r07-iobit-mb]

**Exact identifier table:** Malwarebytes paths and tasks describe version **6.3.0 in its 12 March 2019 removal log**, not guaranteed paths for version 14.

| Product | Type | Exact value from source | Sentinel Log Analytics table.column, if collected | Match criterion | Source |
| --- | --- | --- | --- | --- | --- |
| IObit Driver Booster | executable | `DriverBooster.exe` | `DeviceProcessEvents.FileName` | **standalone** branded runtime lead; validate product/path | [^r07-iobit-mb] |
| IObit Driver Booster | historical installed executable | `C:\Program Files (x86)\IObit\Driver Booster\6.3.0\DriverBooster.exe` | `DeviceProcessEvents.FolderPath` | **standalone** combined exact path+filename; old-version example only | [^r07-iobit-mb] |
| IObit Driver Booster | historical scheduled task | `Driver Booster Scheduler` | collected `WindowsEvent.EventData` task-creation events | pair with runtime; events are not live task inventory | [^r07-iobit-mb] |
| IObit Driver Booster | historical scheduled task | `Driver Booster SkipUAC ({username})` | collected `WindowsEvent.EventData` task-creation events | pair with runtime; username variable | [^r07-iobit-mb] |
| IObit Driver Booster | PUP classification | `PUP.Optional.iObitDriverBooster` | `SecurityAlert.AlertName` or ingested vendor detection field | **standalone detection lead**, not execution proof | [^r07-iobit-mb] |

**Hunt:** Across 30 retained days of Sentinel Windows process telemetry, seek `DriverBooster.exe` with the IObit product folder and corroborating version/metadata; use scheduler or file evidence only if ingested. Record execution, user and approval separately from mere installers and blocks. **Proves:** branded updater execution, not malware or which drivers were changed. **Benign:** authorised technician use. **Escalate:** corroborated malicious downloads, unapproved driver modification or security-control interference. **Signer screen:** an older version contains IObit-related company metadata, not independently validated current Authenticode; the review's Unit 42 CL-UNK-1090/OneBrowser signer list has no observed IObit name, but absence is not a safety clearance.

## H012: uTorrent Classic for Windows

**Hypothesis, tier B (Review 007 L7):** A Windows endpoint runs a consumer peer-to-peer download client outside the client's permitted software. The publisher's **Windows Classic download remained live 13 November 2026**; advertised lifetime downloads are **not** present-day enterprise installations. Microsoft's named `PUA:Win32/uTorrent_BundleInstaller` classification was last updated **15 February 2021** and refers to a bundled installer, not automatic malware attribution to all clients. [^r07-ut-live][^r07-ut-ms]

**Exact identifier table:** Two full application paths are transcribed from a user's **1 March 2025** Malwarebytes support post. They demonstrate real product locations historically, not current estate scale.

| Product | Type | Exact source value | Sentinel Log Analytics table.column, if collected | Match criterion | Source |
| --- | --- | --- | --- | --- | --- |
| µTorrent Classic | executable | `uTorrent.exe` | `DeviceProcessEvents.FileName` | **standalone** branded process lead; corroborate path/product | [^r07-ut-forum] |
| µTorrent Classic | installed executable | `C:\Program Files (x86)\uTorrent\uTorrent.exe` | `DeviceProcessEvents.FolderPath` | **standalone** combined brand-folder+file | [^r07-ut-forum] |
| µTorrent Classic | per-user installed executable | `C:\Users\{Username}\AppData\Roaming\uTorrent\uTorrent.exe` | `DeviceProcessEvents.FolderPath` | **standalone** combined brand-folder+file; variable username | [^r07-ut-forum] |
| µTorrent Classic | bundle PUA detection | `PUA:Win32/uTorrent_BundleInstaller` | `SecurityAlert.AlertName` or appropriate ingested vendor field | **standalone detection lead**; verify prevention outcome | [^r07-ut-ms] |

**Hunt:** Corroborate running branded client and user/path over the retained window; where available, examine attributed peer connections and the execution of downloaded payloads. **Proves:** µTorrent execution, **not** illegal download, exfiltration or malware. **Benign:** approved P2P transfers and legitimate client use. **Escalate:** independent malicious downloaded-executable execution, sensitive-file transfer or externally reachable service contrary to policy. **Signer screen:** a legacy 2015 diagnostic listed company metadata `BitTorrent, Inc.` and product `µTorrent`, not a currently verified code signer; the Unit 42 list has no observed matching company, which is not evidence of safety. [^r07-ut-legacy]

## H013: Outbyte Driver Updater

**Hypothesis, tier B (Review 007 L7):** Some managed Windows endpoints run an unapproved consumer driver updater. Outbyte's official Windows download was live **13 November 2026**, GridinSoft updated removal guidance **7 July 2026**, and Malwarebytes classifies the broader Outbyte product family as PUP.Optional.Outbyte. **Live distribution, not measured enterprise prevalence.** [^r08-ob-live][^r08-ob-grid][^r08-ob-mb]

**Identifier provenance (Review 008 correction verified):** One public ANY.RUN installer sample from **17 May 2025**, under **Processes → Process information**, PID **4164** quotes exactly `"C:\Program Files (x86)\Outbyte\Driver Updater\DriverUpdater.exe"` and lists **Company: Outbyte**, **Description: Driver Updater**. The same executable appears as a lowercase full path in that process's **Modules** section (and in PIDs 2064/4212). These are historical sample details; the current build is not shown using the same directory. The automated “stealer” verdict alone does not prove exfiltration by every authentic Outbyte application. [^r08-ob-sample]

| Product | Type | Exact value | Log Analytics table.column if ingested | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| Outbyte Driver Updater **2024 installer**, not verified runtime | Authenticode signer in GridinSoft Certificate Chain Analysis | `Outbyte Computing Pty Ltd` | `DeviceFileCertificateInfo.Signer` if ingested, correlated by file SHA1 | **standalone signed-installer identity lead**; does not prove current runtime signer | [^r09-ob-signer] |
| Outbyte Driver Updater | runtime full path | C:\Program Files (x86)\Outbyte\Driver Updater\DriverUpdater.exe | DeviceProcessEvents.FolderPath | **standalone** full product path and executable | [^r08-ob-sample] |
| Outbyte Driver Updater | process | DriverUpdater.exe | DeviceProcessEvents.FileName | **pair with Outbyte path or metadata**; other vendors use it | [^r08-ob-file] |
| Outbyte Driver Updater | version company | Outbyte | DeviceProcessEvents.ProcessVersionInfoCompanyName | **pair with executable and folder**; metadata not verified signer | [^r08-ob-sample] |
| Outbyte Driver Updater | version description | Driver Updater | DeviceProcessEvents.ProcessVersionInfoFileDescription | **pair with Outbyte name/path** | [^r08-ob-sample] |
| Outbyte software family | PUP name | PUP.Optional.Outbyte | SecurityAlert.AlertName or vendor detection field | **standalone detection lead**; may be a block, not this exact product | [^r08-ob-mb] |

**Hunt:** In a 30-day window of collected Sentinel process events, find full product path or pair generic process with Outbyte-specific metadata, group by device/user/repeat execution and check approval. **Proves:** product execution, not a malware verdict or driver change. **Benign:** authorised technician use. **Escalate:** separately supported malicious child process, unapproved driver modification or security-control tampering. **Signer screen:** `Outbyte` version metadata is not Authenticode. GridinSoft independently reports **`Outbyte Computing Pty Ltd` as the signer of a November 2024 installer**; this must not be generalized to all running builds. No observed match to the reviewed Unit 42 campaign signers is **not** a safety clearance. [^r09-ob-signer]

## H014: DriverPack Online and Notifier

**Hypothesis, tier B (Review 007 L7):** Managed endpoints may run DriverPack Online, perhaps with its historically bundled Notifier, without approval. Official **DriverPack Online 17.11.108** remained available **13 November 2026**. Malwarebytes documents the PUP.Optional.DriverPack bundled-offer concern, but its cited removal log is **6 May 2018**. Live download does not quantify current business installs. [^r08-dp-live][^r08-dp-mb]

**Identifier provenance:** Historical process attribution and version info are recorded at file.net; **Malwarebytes' May 2018 removal log puts `DriverPack.exe` in `\AppData\Local\Temp\7ZipSfx.000\`, not a persistent installed runtime**. Notifier executable paths, task names and DRPSu traces likewise come from that old log. Do not assert the current version has identical persistence. Official FAQ says DriverPack can run **without installation**. [^r08-dp-file][^r08-dp-faq]

| Product | Type | Exact value | Log Analytics table.column if ingested | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| DriverPack | `DriverPack.exe` execution seed (2018 trace only) | `DriverPack.exe` | `DeviceProcessEvents.FileName` | **pair with verified DriverPack product metadata and the temporary self-extraction path**; not a standalone installed runtime claim | [^r08-dp-mb][^r08-dp-file] |
| DriverPack Online | May 2018 temporary process path | `C:\Users\{username}\AppData\Local\Temp\7ZipSfx.000\DriverPack.exe` | `DeviceProcessEvents.FolderPath` | **pair with product metadata**; execution of a temporary extracted binary, not installed-product proof | [^r08-dp-mb] |
| DriverPack | version product | DriverPack Solution | DeviceProcessEvents.ProcessVersionInfoProductName | **standalone** product metadata on observed execution, not validated signer | [^r08-dp-file] |
| DriverPack Online | version product | driverpack online | DeviceProcessEvents.ProcessVersionInfoProductName | **standalone** product metadata on observed execution | [^r08-dp-file] |
| DriverPack Notifier | 2018 task-cache registry | HKLM\SOFTWARE\MICROSOFT\WINDOWS NT\CURRENTVERSION\SCHEDULE\TASKCACHE\TREE\DRIVERPACK NOTIFIER | DeviceRegistryEvents.RegistryKey | **standalone historical persistence lead**, not proof task is active | [^r08-dp-mb] |
| DriverPack Notifier | May 2018 process in system-wide installed folder | `C:\Program Files (x86)\DriverPack Notifier\DriverPackNotifier.exe` | `DeviceProcessEvents.FolderPath` | **standalone combined branded path and exe**, older build only | [^r08-dp-mb] |
| DriverPack Notifier | May 2018 process in per-user installed folder | `C:\Users\{username}\AppData\Roaming\DriverPack Notifier\DriverPackNotifier.exe` | `DeviceProcessEvents.FolderPath` | **standalone combined branded path and exe**, older build only | [^r08-dp-mb] |
| DriverPack | 2018 additional scheduled task | `DRPNPS` | collected `WindowsEvent.EventData` task-creation events or `DeviceEvents.AdditionalFields` | **standalone historical task-creation lead**, not current task inventory | [^r08-dp-mb] |
| DriverPack | 2018 registry | `HKCU\SOFTWARE\DRPSU` | `DeviceRegistryEvents.RegistryKey` if collected | **standalone historical registry-event lead**, not proof of installed state | [^r08-dp-mb] |
| DriverPack | 2018 folder | C:\Users\{username}\AppData\Roaming\DRPSu\ | DeviceFileEvents.FolderPath | **pair with product process**; username variable | [^r08-dp-mb] |
| DriverPack | PUP detection | PUP.Optional.DriverPack | SecurityAlert.AlertName or vendor detection field | **standalone detection lead**, check prevention state | [^r08-dp-mb] |

**Hunt:** In actual Sentinel process events, establish the product and execution time; optionally corroborate file/registry activity where ingested. Do not equate installer downloads, blocks or residual tasks with execution. **Proves:** identified DriverPack executed; not malicious download, bundle installation or unwanted driver change. **Benign:** approved technician portable usage. **Escalate:** confirmed malicious bundled payload, unauthorised driver installation or security-tool interference. **Signer screen:** historical Kuzyakov Artur Vyacheslavovich IP is not on the reviewed Unit 42 escalation signer list; present-day Authenticode was not validated.

## Same route, not low severity — escalation packs

These are **incident leads**, separate from the low-severity H list; neither a PUP label nor a shared search-advert route proves a host is infected.

| Run order | ID | Pack | Newest dated source | Added | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | [E001](#e001-pdf-spark-and-onebrowser) | PDF Spark / OneBrowser signer overlap | OneBrowser guide updated 4 Nov 2026 | Run 04 | Finished: qualified signer/process/task pivots |
| 2 | [E003](#e003-cl-unk-1090-and-hollowmare-document-tools) | CL-UNK-1090 / HollowMare document tools | Intezer 27 Jul 2026, SagePDF observed Jan 2026 | Run 04 reclassification of H006 | Finished: sample and installer stages separated |
| 3 | [E002](#e002-jia-hao-document-utility-siblings-and-projextor-comparison) | Jia Hao / PDF Polish sibling context and Projextor | G DATA 17 Aug 2026; PDF Polish 10 Apr 2026 | Run 05 | Finished: malware-grade investigation; attribution qualified |

### E001: PDF Spark and OneBrowser

**Why check now:** PDF Spark is a confirmed previous hit. Malwarebytes identifies Mainstay Crypto LLC as PDF Spark publisher; Unit 42's **20 May 2026** signer table lists **Mainstay Crypto LLC** and **Crowd Sync LLC** under **OneBrowser Signers** but **does not name PDF Spark**. A German SOC case dated **26 Aug 2026** describes SparkOnSoft and OneBrowser on two RDS servers. GridinSoft's OneBrowser guide updated **4 Nov 2026** gives specific updater persistence. **Shared signer-group membership is not proof every PDF Spark installer dropped OneBrowser.** [^pdf-spark][^pdf-signer][^r04-teamit][^r04-onebrowser]

**Identifier table** — exact strings from Unit 42 Table 1 and GridinSoft's “Quick answer”, “Stop OneBrowser updater services and tasks” and “Registry keys”.

| Product | Type | Exact value | Log Analytics table.column | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| PDF Spark / overlap | signer | Mainstay Crypto LLC | DeviceFileCertificateInfo.Signer linked by SHA1 to DeviceProcessEvents | standalone signer lead; corroborate product | [^pdf-spark][^pdf-signer] |
| PDF Spark / overlap | signer | Crowd Sync LLC | DeviceFileCertificateInfo.Signer linked by SHA1 to DeviceProcessEvents | standalone signer lead; corroborate product | [^pdf-signer] |
| OneBrowser group | signer | WORK PRODUCT, INC. | DeviceFileCertificateInfo.Signer linked by SHA1 to DeviceProcessEvents | standalone signer lead; verify file | [^pdf-signer] |
| OneBrowser group | signer | Chickadee Digital; Riya Software; Eman Group, LLC | DeviceFileCertificateInfo.Signer linked by SHA1 to DeviceProcessEvents | standalone family lead; verify file | [^pdf-signer] |
| OneBrowser | updater path/process | %LocalAppData%\OB\OneBUpdate\OneBUpdateService.exe | DeviceProcessEvents.FolderPath | standalone combined path/process match | [^r04-onebrowser] |
| OneBrowser | updater process | OBUpdateService.exe | DeviceProcessEvents.FileName | standalone distinctive updater seed; verify path | [^r04-onebrowser] |
| OIBrowser | process | oibrowser.exe | DeviceProcessEvents.FileName | standalone distinctive process; verify product | [^r04-onebrowser] |
| OneBrowser | scheduled task | OBUpdate | DeviceEvents.AdditionalFields for ActionType=ScheduledTaskCreated, or collected Windows task events | standalone persistence lead | [^r04-onebrowser] |
| OneBrowser | scheduled task | OneBUpdate | DeviceEvents.AdditionalFields for ActionType=ScheduledTaskCreated, or collected Windows task events | standalone persistence lead | [^r04-onebrowser] |
| OneBrowser | service | onebupdate; obupdate; oibupdate | DeviceEvents.AdditionalFields for ActionType=ServiceInstalled or collected service events | standalone persistence lead; verify service executable | [^r04-onebrowser] |
| OneBrowser | registry | HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\OneBrowser.exe | DeviceRegistryEvents.RegistryKey | standalone registration-event lead, not live inventory | [^r04-onebrowser] |

**Hunt:** On an endpoint with past PDF Spark, first search exact OneBrowser process, service, scheduled-task and registry paths over whatever Log Analytics retention exists. Then correlate actual execution with the earlier installer tree, signer and downstream payloads. Changes to the root certificate store are an **investigative idea, not a source-verified OneBrowser-specific IOC**; pursue only with supporting telemetry. An installer file, signer, blocked download or OneBrowser registry remnant alone does not prove a currently malicious stage. Confirmed OneBrowser deployment plus anomalous persistence, credential or second-stage access requires incident assessment. Sophos KBA-000043676 returned only a loading shell, so it was not used for new identifiers.

### E002: Jia Hao document-utility siblings and Projextor comparison

**Rationale — escalation, not routine PUP:** PDF Polish is a **confirmed previous hit**. A **10 April 2026** ANY.RUN sample executed `PDF Polish.exe` under `\AppData\Roaming\PDFPolish\` and showed **Jia Hao** in *process version company metadata*, **not independently verified digital-signature identity**. Rabbit Knight's **4 April 2026** sample of Doc Convert Wizard has `doc-wizard.exe` with the same company metadata and references a shared `main.js` hash across `DocConvertWizard`, `FoodFormula`, `ProfessionalConverter` and `PDFPolish`. G DATA's independent **17 August 2026** report classifies DocConvertWizard, Food/Meal Formula, Kitchen Canvas and PDF-tool installers as **Projextor malware**. **G DATA never identifies PDF Polish, Jia Hao or ProfessionalConverter as Projextor:** code/metadata similarity is an investigation lead, not proven attribution. [^pdf-polish][^r05-jia][^r05-gdata]

**Exact identifier table:** ANY.RUN “General Info”, “Process information” and “Registry activity”; Rabbit Knight “Files analyzed”/“Living Off the Land”; G DATA “Installation and Infection Chain”/“IOCs”. Names/hashes are sample-specific; do not conflate separate installer builds.

| Product | Type | Exact value | Log Analytics table.column | Match rule | Source |
| --- | --- | --- | --- | --- | --- |
| PDF Polish | installed runtime path, example username | `C:\Users\admin\AppData\Roaming\PDFPolish\PDF Polish.exe` | `DeviceProcessEvents.FolderPath` | **standalone sample-specific combined path**; generalise user profile when hunting | [^r05-polish-sample] |
| PDF Polish / Doc Wizard | version company, **not signer** | `Jia Hao` | `DeviceProcessEvents.ProcessVersionInfoCompanyName` | pair with `PDF Polish.exe` / `doc-wizard.exe` and product path | [^r05-polish-sample][^r05-jia] |
| PDF Polish | runtime executable | `PDF Polish.exe` | `DeviceProcessEvents.FileName` | pair with `\AppData\Roaming\PDFPolish\` | [^r05-polish-sample] |
| PDF Polish | installer file | `PDFImage_519340.exe` | `DeviceProcessEvents.FileName` / `DeviceFileEvents.FileName` | **standalone installer-stage lead**, no durable installation inference | [^r05-polish-sample] |
| PDF Polish | registration key | `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\PDFPolish` | `DeviceRegistryEvents.RegistryKey` when ingested | **standalone** registration **write-event** lead, not current inventory | [^r05-polish-sample] |
| Doc Convert Wizard | product process | `doc-wizard.exe` | `DeviceProcessEvents.FileName` | pair with company `Jia Hao` and product `Doc Convert Wizard` | [^r05-jia] |
| Doc Convert Wizard | install-stage filename | `FlipFormat_947850.exe` | `DeviceProcessEvents.FileName` or `DeviceFileEvents.FileName` | **standalone installer lead**; different from G DATA `FlipFormat_610220.exe` | [^r05-jia][^r05-gdata] |
| Related document-utility contexts | observed directories | `DocConvertWizard`; `FoodFormula`; `ProfessionalConverter`; `PDFPolish` | `DeviceProcessEvents.FolderPath` | pair with company metadata or matching `main.js`; generic folder alone not attribution | [^r05-jia] |
| Projextor | first-stage sample SHA256 (file `PDFGrip_646990.exe`) | `71656539cc644513396f56100ffb56f9ef9eaa5b7a16b0773d6e5d370a912a88` | `DeviceFileEvents.SHA256` / `DeviceProcessEvents.SHA256` where populated | **standalone malicious sample hash**; install-stage only | [^r05-gdata] |
| Projextor | named installer files | `FoodFormula_822670.exe`; `KitchenCanvas_748343.exe` | `DeviceFileEvents.FileName` or `DeviceProcessEvents.FileName` | **standalone** install-stage leads; verify hashes/stages | [^r05-gdata] |
| Projextor | download URL | `conv.doceditorinc.com/latest/part` | `DeviceNetworkEvents.RemoteUrl` or proxy full-URL field when present | pair with relevant installer process; URL-only not proof of payload | [^r05-gdata] |
| Doc Convert Wizard | installer download URL | `tool.securedocumentinstaller.com/appsectools` | `DeviceNetworkEvents.RemoteUrl` / collected proxy full URL when present | pair with Doc Wizard installer; endpoint is not proof of successful delivery | [^r05-jia] |

**Hunt on a known PDF Polish host:** Check retained process/registry evidence for PDFPolish, `Jia Hao`-branded document tools and siblings; trace installer ancestry and any downloads, script/module content if separately collected, persistence, new binaries and suspicious network events. Separately look for G DATA's *specific* Projextor files/hashes; a shared six-digit installer suffix also appears on PDF Spark and is **not a family identifier**. Rabbit Knight's proposed DLL sideload via `libEGL.dat` is explicitly **unverified**; a standard Nativefier `main.js` is not itself malicious proof. A confirmed executable, hash or implant provides an **incident lead**, not proof of one actor, credential theft or execution of the hypothesised payload. [^r05-jia][^r05-gdata]

### E003: CL-UNK-1090 and HollowMare document tools

**Re-filed from H006, not a new H ID.** Intezer's **27 Jul 2026** prose calls part of HollowMare PUA, yet its IOC table labels ConvertyFile / OneZip as stealers and CrystalPDF as stealer/installer. Unit 42's **20 May 2026** Table 1 groups signers for SagePDF, PowerDoc, ConvertyFile, OneZip and CrystalPDF under CL-UNK-1090, treated as malware-grade. **TAMARISK INTERACTIVE LTD**, associated by Intezer with PDFDoc / PowerPlayer, is **absent** from Unit 42's list, so those are contested associations. [^hollow][^pdf-signer]

**Identifier table** — exact strings from Intezer “Hollow Mare” IOC section and Unit 42 signer table. TEMP values are *installer-stage traces*, not durable installation proof.

| Product | Type | Exact value | Log Analytics table.column | Condition | Source |
| --- | --- | --- | --- | --- | --- |
| SagePDF | signer | Chrono Orion LTD | DeviceFileCertificateInfo.Signer joined by SHA1 to process/file | standalone signer lead | [^hollow][^pdf-signer] |
| SagePDF | installer-stage file | %TEMP%\SagePdf\SageId.txt | DeviceFileEvents.FolderPath + FileName | standalone file-artifact lead, not runtime | [^hollow] |
| PowerDoc | signer | GOLD HARMONY LTD | DeviceFileCertificateInfo.Signer joined by SHA1 to process/file | standalone signer lead | [^hollow][^pdf-signer] |
| PowerDoc | installed process/path | %LocalAppData%\pwrDoc\PowerDoc.exe | DeviceProcessEvents.FolderPath | standalone combined path/process | [^hollow] |
| PowerDoc | persisted file | %LocalAppData%\pwrDoc\pwrDoc.txt | DeviceFileEvents.FolderPath + FileName | standalone file-artifact lead | [^hollow] |
| ConvertyFile | signer | TAU CENTAURI LTD | DeviceFileCertificateInfo.Signer joined by SHA1 to process/file | standalone signer lead | [^hollow][^pdf-signer] |
| ConvertyFile | installer-stage file | %TEMP%\ConvertyFile\CFInfo.txt | DeviceFileEvents.FolderPath + FileName | standalone installer lead | [^hollow] |
| OneZip | signer | G.R.CIGAR. LTD | DeviceFileCertificateInfo.Signer joined by SHA1 to process/file | standalone signer lead | [^hollow][^pdf-signer] |
| OneZip | installer-stage file | %TEMP%\O\OZInfo.txt | DeviceFileEvents.FolderPath + FileName | standalone installer lead | [^hollow] |
| CrystalPDF | signer | VAST LAKE LTD | DeviceFileCertificateInfo.Signer joined by SHA1 to process/file | standalone signer lead | [^hollow][^pdf-signer] |
| CrystalPDF | embedded signer | LONG SOUND LTD | DeviceFileCertificateInfo.Signer joined by SHA1 to process/file | standalone signer lead | [^hollow][^pdf-signer] |
| CrystalPDF | task | Crystal_updater | DeviceEvents.AdditionalFields for ActionType=ScheduledTaskCreated or collected task event | standalone persistence lead | [^hollow] |
| PDFDoc | installer-stage file | %TEMP%\DocID\DocID.txt | DeviceFileEvents.FolderPath + FileName | standalone installer lead | [^hollow] |
| PDFDoc / PowerPlayer | signer not in Unit 42 table | TAMARISK INTERACTIVE LTD | DeviceFileCertificateInfo.Signer joined by SHA1 to process/file | standalone contested signer lead; identify product | [^hollow] |
| PowerPlayer | installer-stage file | %TEMP%\PwrId\PwrId.txt | DeviceFileEvents.FolderPath + FileName | standalone installer lead | [^hollow] |
| PowerPlayer | installer-stage process | NativePowerPlayer.exe under %TEMP%\PowerPlayer\ | DeviceProcessEvents.FileName + FolderPath | standalone combined path/name, not durable installed software | [^hollow] |

**Hunt:** Prefer signer-backed product execution, the exact PowerDoc runtime, and Crystal_updater where available; TEMP paths are historical installer leads. Correlate downstream processes, browser data access, related file writes and network events before attributing exfiltration. A certificate, product presence or stage file does not itself prove theft. Escalate independently supported stealer, loader, remote payload or exfiltration. Shared search-advert route with PDF Polish / Spark is not verified shared ownership. Do not label all PDFDoc / PowerPlayer samples CL-UNK-1090 merely by proximity.

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
| 03 | 2026-11-13 | H006 HollowMare document/browser-change pack (one candidate; one evidence-based shortfall) | **Review 003 · 2026-11-13 01:02 GMT**, reviewed register `b8153a2`, reviews.md SHA `a30fbcd586b720a60c26d2110b1ee3f429143ed9` read before research; itemised action/decline record below. No client data accessed. |
| 04 | 2026-11-13 | H007 Dragon Boss, H008 Infatica, E001 PDF Spark/OneBrowser, reclassified H006 into E003 | Read **Review 007 · 2026-11-13 02:46 GMT**, reviewed register commit 05a9a36, review-file SHA 33247266896ac3f03072ddac0980a64ac1e6adff. Detailed action/decline record below. Six active H packs, two E packs; no client queries. |
| 05 | 2026-11-13 | H009 Hola, H010 Honeygain, E002 Jia Hao/Projextor | Review 007 followed; existing fixes verified, 04:00 E002 carryover actioned, two recent measured/provider-level leads chosen, L8 deferred; details below. No client queries. |
| 06 | 2026-11-13 | No new IDs; H001/H003/H004/H005 evidence and typed tables; both indexes re-ranked | Review 007 and 05:00 plan followed. H001/H003/H005 finished; H004 remains incomplete because real-world current activity was not verified. No client queries. |
| 07 | 2026-11-13 | H011 IObit Driver Booster; H012 µTorrent Classic; no E additions | Review 007 read; remaining L8/L6 examined but not promoted, L7 sourced as two current-download low-severity packs. Detailed action log below. No tenant queries. |
| 08 | 2026-11-13 | H013 Outbyte Driver Updater; H014 DriverPack Online/Notifier | Review 007 and 07:00 orders followed; L8/L6 examined and declined; L7 produced two current-download candidates, with exact historical artefacts. See details below. No tenant queries. |
| 09 | 2026-11-13 | No new IDs; Review 008 corrections 1–7, new provider counts, ranking and identifier audit | Review 008 at 07:57 GMT read first; fixes and lead decisions itemised below. No client data queried. |

### Run 03: review actions, corrections and deliberate shortfall

**Read first:** **Review 003 · 2026-11-13 01:02 GMT**, reviewed register commit `b8153a2`, review-file blob `a30fbcd586b720a60c26d2110b1ee3f429143ed9`. Standing guidance and the updated lead queue followed; `reviews.md` was not modified.

- **Review 003 Next #1 / L1 — researched, DECLINED a new low-severity ID.** Verified PDF Spark signers **Mainstay Crypto LLC** and **Crowd Sync LLC** and source-linked OneBrowser/software under those signers. Public original research by Unit 42 describes this ecosystem as **TamperedChef-style malware** with arbitrary-payload, stealer/RAT capability; a **26 Aug 2026** SOC case describes malicious software on two RDS servers. This makes a **high-priority separate malware hunt**, not a safe “low-severity PUA” pack. **Run 04 correction:** Unit 42 itself links the signer names to OneBrowser, not to PDF Spark by product; PDF Spark's separate publisher evidence is from Malwarebytes and the Controlware report. Sophos signer-specific KBA (dated **24 Sep 2026** in the review) could not be opened in full. Relevant installer/brand names `PDFSparkWare_*.exe`, `PDFSparkOnSoft.exe`, `pdfsetup.exe` and `OneBrowser` are **research context**, not approved low-severity pivots. **Shortfall deliberately accepted**. [^pdf-signer]
- **Review 003 Next #1 / L2 — ACTIONED:** H006 includes SagePDF, PowerDoc and PowerPlayer browser-change indicators, shared search-ad route but not a falsely shared signer. **DECLINED** treating ConvertyFile/OneZip stealer evidence, SilentMare or documented malicious CrystalPDF cases as low severity. [^hollow][^pdf-control]
- **Review 003 Next #2 — ACTIONED with limit:** Found PDF Polish dated **10 Apr 2026** process version field `Company: Jia Hao` and a Nullsoft installer. **Actual code signer not verified**; no documented same-publisher new product. Already-covered entry says so rather than guessing. [^pdf-polish]
- **Review 003 Next #3 — ACTIONED:** No JustAskJacky, SilentMare, TamperedChef, tampered OneBrowser/AppSuite or other malware reclassified as low-severity.
- **Review 002 items 1–3 — ACTIONED:** Added PDF Spark as confirmed previous hit; compared the distinct publishers and advertising channels; added evidence-based likelihood tiers, newest source activity and recency ordering; H001 B, H003 C, H004 C. **Review 002 #4 — DECLINED/deferred:** Honeygain and other unrelated consumers await **L3–L5** because Review 003 explicitly prioritises L1 and L2. **#5 — ACTIONED:** Carried Review 001 guidance forward.
- **Review 001 corrections 1–4 — ACTIONED:** Corrected H001 27 March 2026 publication date and assessment, not installation date; corrected **one Bright installer hash analysed twice**; labelled prior `\Bright VPN\`/`win_brightvpn.com` path/argument **unconfirmed** and added installer-stage `brightvpn_installer.exe`; separated index `Added` from uniform `Not run` status.
- **Review 001 Next 1–2 — ACTIONED:** Added tier definitions and expanded existing H005 from a Bright VPN name-only hunt to Bright/Luminati **SDK across any host path**, with exact SDK command and source report section. The vendor guide redirects to login; full text **not** claimed to be read. EarnApp remains host context, not new ID.
- **Review 001 Next 4–5 — ACTIONED:** Added one compact new pack and shared `Applies to every card` guidance. **A single defensible pack beats a forced second**; L1 needs separate higher-severity treatment. Later runs should research L3 then L4 then L5. No workspaces queried and no field results claimed.

### Run 04: Review 007 corrections and Next run account

**Read before research:** Review 007 · **2026-11-13 02:46 GMT**; reviewed register commit **05a9a36**; reviews.md blob **33247266896ac3f03072ddac0980a64ac1e6adff**. Read the brief, orders, Standing guidance, lead queue, sweep sheet and newest review. This run did not edit reviews.md. Reviewer reported no 02:00 commit; whether that run attempted and failed cannot be established, so no cause is invented.

- **Next #1 — actioned:** named the review, its timestamp, reviewed commit and SHA; recorded no verified 02:00 completion.
- **Next #2 / Review 006 Corrections #1–4 — actioned:** retired H006; moved its sourced content into E003, including installer-stage versus installed markers; corrected the count and indexes. Corrected the Unit 42 signer-only wording (including old Run 03 note) and Shift's manuals/recipes/templates wording and 18 Aug 2025 page date.
- **Review 005 Corrections #1–3 — actioned/partial:** fixed H005 index anchor. E003 has a typed identifier table; H005 is explicitly **incomplete** pending a similarly typed table and firmer current-prevalence evidence, instead of falsely claiming finish. Added the Jia Hao/DocConvertWizard/Projextor relationship to already-covered PDF Polish, clearly marking that G DATA never names PDF Polish itself.
- **Next #3 — actioned:** added **E001** for PDF Spark/OneBrowser with source-linked Task/Service/Updater pivots and a no-direct-family-link caveat. **E002 declined for this run / deferred** under Review 007's explicit 04:00 instruction and the maximum one *new* E pack per run. E003 is a correction, not a new E discovery.
- **Next #4 — actioned:** added **H007 from L3** using the Huntress research and 23,565 unique IPs/2,223 UK; added **H008 from L4** with Infatica component and dated 11 Aug report. Both are low severity **only for confirmed unauthorised presence without separate malicious behaviour**.
- **Next #5 / Standing guidance 8 — actioned:** checked the signers **Dragon Boss Solutions LLC** and **Infatica pte ltd** against the opened Unit 42 May 2026 Table 1: neither appears. Infatica signer remains **unverified** and is not relied on as a code-certificate IOC. Absence from the signer list does not prove safety; Huntress's AV-killer artefacts mandate escalation.
- **Declined unsupported leads:** no Digital Pulse=Infatica alias; no guessed Infatica service name; no unconfirmed FreeFixer or Sophos-KBA identifiers (the linked pages did not open). E002 is next-review work, not silently dropped. Existing incomplete H001/H003/H004/H005 remain on the index; no padding or fabricated client results. Typed tables here describe *where to match if ingested*, not queries run or live inventories.

### Run 05: Review 007 follow-through, E002 and two evidence-ranked leads

**Mandatory pre-research review:** **Review 007 · 2026-11-13 02:46 GMT**, reviewing register commit **`05a9a36`**, `reviews.md` blob **`33247266896ac3f03072ddac0980a64ac1e6adff`**. Read **The brief, Orders until 08:00, Standing guidance, Lead queue, Verified sweep sheet and newest review** before any new candidate research; rechecked SHA before write. `reviews.md` unmodified.

- **Next #1 — ACTIONED:** Named exact review/commit/SHA. Review 007 had found no 02:00 commit; no reliable cause for that missed run, so no invented explanation. Run 04 subsequently landed.
- **Next #2 / Review 006 Corrections 1–4 — ALREADY ACTIONED in Run 04:** H006 retired/re-filed as E003, the installer-stage TEMP paths labelled, Unit 42/PDF Spark signer relation qualified, Shift date/marketing wording corrected. Verified present; did not reword settled cards.
- **Next #3 — E001 ALREADY ACTIONED in Run 04; E002 ACTIONED NOW:** The explicit 04:00 carryover from Review 007 is E002, built as the run's **one new escalation pack** using G DATA, Rabbit Knight and PDF Polish ANY.RUN. Declined unsupported attribution of PDF Polish to Projextor and generic numeric-suffix linkage. [^r05-gdata][^r05-jia][^r05-polish-sample]
- **Next #4 — L3/L4 ALREADY ACTIONED in Run 04:** H007 and H008 indexed. For 04:00's **two best open leads**, chose **L5 Hola → H009** and **L7 Honeygain → H010** over more historical leads, because Gen's September 2026 Windows-active provider data and currently live vendor downloads meet the *likely now* standard. Counts are **provider-associated** and not confirmed app-process execution or Chorus hit rates. Distinct branded products, not rebranded Bright SDK or Infatica. [^r05-gen][^r05-hola-vendor][^r05-hg-vendor]
- **L8 PacketShare/IPIDEA — DEFERRED:** Google's **28 January 2026** takedown makes current functioning uncertain; earlier PacketShare file evidence alone doesn't show post-takedown activity. L6 and remaining L7 torrent/driver tools deferred because this run focused on better-evidenced contemporary distributions. [^r05-ipidea]
- **Next #5 / Standing guidance 8 — ACTIONED:** Checked new H identifiers against Unit 42's 20 May 2026 malware-grade signer set in the review sweep sheet. Neither H009 nor H010 uses a listed signer as a positive; absence is **not** evidence of safety. Sophos's miner/AV-exclusion chain is a distinct **escalation**, not reclassified as PUP.
- **Review 005 corrections 1–3 — ALREADY/PARTIALLY ACTIONED:** H005 anchor and PDF Polish uncertainty corrected previously. H005 still **incomplete** (SDK-specific contemporary prevalence and typed table); no false “finished” declaration.
- **Format, integrity and scope — ACTIONED:** New H cards share existing “Applies to every card” policy; each has a source-backed no-command-line standalone seed, table/column, positive/negative interpretation and severity branch. Retained existing IDs and footnotes; no client workspaces were accessed, no KQL was generated and no client results were asserted.

### Run 06: 05:00 finish-and-prioritise audit

**Review read before research:** **Review 007 · 2026-11-13 02:46 GMT**; **reviewed register commit `05a9a36`**; `reviews.md` blob SHA **`33247266896ac3f03072ddac0980a64ac1e6adff`**. Read The brief, Orders until 08:00, Standing guidance, Lead queue, Verified sweep sheet and newest review; `reviews.md` remained unmodified.

- **Review Next #1 — actioned:** Exact review/commit/SHA named. Reviewer saw no 02:00 commit; the cause of any missed execution is unknown and is not invented.
- **Next #2 / Review 006 corrections 1–4 — already actioned in Run 04:** H006 retired as E003; installer-stage paths separated from installed runtime, PDF Spark/Unit 42 signer overlap qualified, Shift source wording/date corrected. Counts and index checked again.
- **Next #3 — already actioned:** E001 saved in Run 04 and E002 in Run 05. **No new E pack** during the 05:00 quality-only run. E003 remains separate escalation material.
- **Next #4 — already actioned:** L3/L4 written in Run 04 as H007/H008, L5/L7 in Run 05 as H009/H010. **Declined additional candidates now** because the 05:00 Orders explicitly require finishing rather than adding; L8/IPIDEA remains a cautious lead after Google's network disruption.
- **Next #5 / Standing guidance 8 — actioned:** Prior Dragon Boss and Infatica signer comparisons to Unit 42 remain in the log; none of the new typed fields is represented as a clean malware-signer verdict. Process matches do not establish harm; AV-removal and miner chains remain escalation-grade.
- **Review 005 typed-table correction — actioned:** Gave H001, H003, H004 and H005 product/type/exact value/workspace field/standalone-or-pair/source tables. Verified SigmaHQ, Trend Micro, Malwarebytes, Comscore and the original Mouse Server sandbox; source age and authentication-gated SDK guide clearly labelled. No generic `net_updater32.exe` match is standalone.
- **05:00 Orders — actioned:** No new packs. Re-ranked both H and E indexes in actual run order. H001 is now finished on a real March 2026 corporate sighting; H003 on live 13 November publisher distribution and typed application execution pivots; H005 on a current Windows SDK partner programme and typed SDK/host identifiers. **H004 remains Incomplete**: 2025 sandbox evidence and the current panel privacy listing do not establish recent installation on real machines. This is an evidence shortfall, not a hidden success.
- **Integrity/scope — actioned:** Existing cards/footnotes retained; approved use, runtime, downloaded installer, detection/blocked attempt, file artefact and third-party relaying remain separate conclusions. No Log Analytics workspaces queried, KQL generated, or findings claimed.

### Run 07: 06:00 new-candidate research

**Read before any candidate research:** **Review 007 · 2026-11-13 02:46 GMT**; its reviewed register commit was `05a9a36` and latest `reviews.md` main-branch blob SHA is `33247266896ac3f03072ddac0980a64ac1e6adff`. Read the brief, orders, Standing guidance, lead queue, Verified sweep sheet, and newest review. `reviews.md` was not edited.

- **Review 007 Next #1 — actioned:** Review heading/time, reviewed commit and blob SHA recorded. The reviewer reported no 02:00 commit; whether a 02:00 run was attempted or why it failed cannot be determined, so no cause is invented.
- **Next #2, Review 006 corrections 1–4, Review 005 corrections 1–3 — already actioned in Runs 04–06:** H006 retired to E003; temporary versus installed artefacts separated; PDF Spark/OneBrowser signer linkage qualified; Shift source wording/date corrected; H005 anchor and typed identifiers corrected; already-covered PDF Polish attribution qualified. Rechecked current file, no redundant edits.
- **Next #3 — already actioned:** E001 added Run 04 and E002 Run 05; E003 is the moved H006. No escalation pack newly justified under the 06:00 plan.
- **Next #4 / 06:00 order — partly already actioned, two new packs added:** L3/H007 and L4/H008 from Run 04 are complete. L5/H009 and Honeygain/H010 from Run 05 already cover those leads. Investigated remaining **L8 IPIDEA/PacketShare**, then **L6 PDFFlows**, before taking L7. **L8 declined as a finished *PacketShare* ID:** Lumen Black Lotus Labs **24 July 2026** documents IPIDEA network recovery to nearly ten million daily IPs, but that is **not** a verified post-disruption PacketShare Windows installation or active executable sighting; the sweep sheet's PacketShare path/file observations are from **2025**. The network also includes malware-backed installations, so avoid low-severity attribution to network-wide traffic. Keep L8 open pending current product-specific proof. [^r07-lumen]
- **L6 declined:** Joe Sandbox July 2026 PDFFlows/WinRAR analysis could not be opened. A current product-style PDFFlows marketing site does not verify the installer content or an active misleading download campaign. No claim of a genuine WinRAR payload in current builds; keep lead open.
- **L7 actioned with evidence bar:** **H011 IObit Driver Booster** and **H012 µTorrent Classic**, two separate publishers/products with **official live Windows downloads checked 13 Nov 2026** and historically observed distinctive exe/path artefacts. IObit released major version 14 **16 Sep 2026**. Vendor PUP names are sourced but old and kept separate from runtime execution; neither current-download page establishes a client hit. Correctly distinguish IObit's tool from Energizer Softech's similarly named product. Both tier B, not speculative tier A. [^r07-iobit-press][^r07-iobit-live][^r07-iobit-mb][^r07-ut-live][^r07-ut-ms]
- **Next #5 / Standing guidance 8 — actioned:** Checked historical company strings IObit and BitTorrent, Inc. against the review's Unit 42 signer list; no observed match. **No current Authenticode signer was verified**, and absence from the listed campaign signers is not proof of harmlessness. Any verified listed signer would demand an escalation pack. Each new identifier has a source, Log Analytics field, and standalone/pair role; generic download/setup names were not used alone.
- **Formatting, shortfall and scope — actioned:** No existing cards deleted or rewritten. New cards are compact and defer to the shared 30-day/telemetry/approval standard. The 06:00 two-candidate target was met without counting L8's network recovery as PacketShare deployment. No KQL generated or client workspaces accessed.


### Run 08: 07:00 evidence-ranked candidate research

**Read first:** **Review 007 · 2026-11-13 02:46 GMT** (reviewed register commit **05a9a36**, main-branch reviews.md blob SHA **33247266896ac3f03072ddac0980a64ac1e6adff**). Read brief, orders, Standing guidance, lead queue, Verified sweep sheet and newest review before researching. This was still the newest review even though earlier runs had since advanced the register. Reviews.md was not edited.

- **Review 007 Next #1 — actioned:** Exact review, timestamp, reviewed commit, SHA recorded. Review's 02:00 missing-commit observation acknowledged; whether a run was attempted or why it failed remains unknown.
- **Next #2 / Review 006 corrections 1–4 and Review 005 corrections 1–3 — already completed in Runs 04–06 and rechecked:** H006 retired into E003, temporary versus installed paths distinguished, PDF Spark/OneBrowser signer association qualified, Shift page details corrected, H005 index anchor and identifier table fixed, PDF Polish attribution caveat preserved. No duplicate edits.
- **Review 007 Correction #2 — followed:** DigitalPulseService.exe was **not** attributed to Infatica. Evidence for equivalence is missing.
- **Next #3 — already completed:** E001 added Run 04, E002 Run 05 and E003 reclassified in Run 04. No independently supported new malware-grade pack, so none added.
- **Next #4 / 07:00 plan — actioned with declines:** L3/H007 and L4/H008 completed earlier. **L8 PacketShare/IPIDEA declined as finished:** a GridinSoft ThreatInfo entry dated **12 September 2026** shows a PacketShare file sample but does not prove an actively installed Windows app following the network disruption; Lumen's recovery data is network-level, not PacketShare deployment. [^r08-packet] **L6 PDFFlows declined:** the alleged genuine-WinRAR delivery report could not be reliably opened previously, and no current live misleading installer was independently substantiated. Proceeded to L7: official Outbyte and DriverPack Windows downloads were live **13 November 2026**, permitting **H013** and **H014**. Both **Tier B**, without quantified enterprise prevalence. [^r08-ob-live][^r08-dp-live]
- **Next #5 / Standing guidance 8 — actioned:** Checked historical Outbyte version company and DriverPack's Kuzyakov Artur Vyacheslavovich IP reference against the Unit 42 escalation signers in the review sweep sheet; neither observed match. Not validated as current signing; absence is not safety proof. Outbyte's generic DriverUpdater.exe only paired with folder/product metadata. Exact Outbyte path taken from the sandbox **Processes → Process information**; historical Notifier values from the cited 2018 log. Two new cards each have source, Log Analytics table.column and standalone/pair columns.
- **Integrity and scope — actioned:** No existing cards removed or rewritten, other than required header, index, run log and new append-only references. No aliases double-counted, no untested KQL and no client workspace or Defender Advanced Hunting access. One 2025 sandbox installer was one sample; no evidence of traffic relay or compromise inferred from PUP matches.


### Run 09: 08:00 final ranking, Review 008 corrections and source audit

**Mandatory review read BEFORE researching:** **Review 008 · 2026-11-13 07:57 GMT** (the last review); it reviewed register commit **`d01a695`**; latest main-branch `reviews.md` blob **`9d70fb6565850e9bb81aa13a8e7a71d5dca72c4f`**. Read The brief, Orders, Standing guidance, Lead queue, Verified sweep sheet and the complete newest review; checked for review changes before commit. Did **not** edit `reviews.md`.

- **Next #1 — ACTIONED:** review heading, time, reviewed commit and blob SHA recorded; every numbered correction and Next item accounted for below.
- **Next #2 / correction 1 — ACTIONED:** renamed the H012 heading to ASCII `uTorrent` and fixed its index anchor without changing the H012 ID or its substantive card.
- **Correction 2 — ACTIONED:** independently opened the 17 May 2025 ANY.RUN Outbyte report; in **Processes → Process information PID 4164** it literally quotes `"C:\Program Files (x86)\Outbyte\Driver Updater\DriverUpdater.exe"` with `Company: Outbyte` and `Description: Driver Updater`; **Modules** repeats the installed file in lowercase. Therefore retained the full-path row as **confirmed for this single 2025 detonation**, not current prevalence. Added the separately verified **`Outbyte Computing Pty Ltd`** certificate signer from GridinSoft's **Certificate Chain Analysis**, correctly scoped to its November 2024 installer and not a blanket runtime-signature claim. [^r08-ob-sample][^r09-ob-signer]
- **Correction 3 — ACTIONED:** the 6 May 2018 Malwarebytes trace puts `DriverPack.exe` in `\AppData\Local\Temp\7ZipSfx.000\`; downgraded the loose name to **pair**, and explicitly denied that this temporary execution proves an installed runtime. Added both historical `DriverPackNotifier.exe` locations, `DRPNPS` task and `HKCU\SOFTWARE\DRPSU` registry event. No historical task or registry change is a live-inventory claim. [^r08-dp-mb]
- **Correction 4 — ACTIONED:** the Gen Digital **1–15 September 2026** observation window is explicit in H009, H010 and the existing Gen source note; H010 also gains a historical version **0.10.7.0** `Honeygain.exe` + `AppData\Roaming\Honeygain` folder combination, with the observed username a **placeholder**. [^r05-gen][^r09-hg-path]
- **Correction 5 — ACTIONED:** H007 now calls `Web Genius` a **folder**, not a verified product name; added the `ReadySpaceThree.exe` and `FutureSpaceThreeSolutions\FutureSpaceThree` pair from Huntress's **Variations of executables** table. Existing `UniversalUpdater.exe` path remains attached to Web Genius, not World Wide Web. [^r04-huntress]
- **Correction 6 — ACTIONED:** H005 now ranks **A (provider-level)** with Gen Digital's approximately **1.47 million active protected Windows users associated with Bright Data** in **1–15 September 2026**; **embedded SDKs are excluded** from the measurement. Added EarnApp 1.597.152 `earnapp.exe` and co-installed generic `net_updater32.exe` with their branded install folder, as **host-app context in H005**, not a new hunt or proof of relay. The EarnApp source is an observed version/uninstaller record, not an organisational sighting. [^r05-gen][^r09-earnapp]
- **Correction 7 — ACTIONED:** H008 now ranks **A (provider-level)** with the approximately **56,000 Infatica-associated protected Windows users** in the same Gen snapshot. Gen did **not** count embedded SDKs, and the figure does not prove that specific `infatica-service-app.exe` ran. [^r05-gen]
- **Next #2 / final ranking — ACTIONED:** reordered H to **H005, H009, H007, H010, H008, H011, H012, H013, H014, H003, H001**, leaving incomplete **H004 unranked**; reordered E to **E001, E003, E002**. Provider-level counts are clearly labelled and never translated into client hit rates. None of the existing IDs or substantive cards was removed.
- **Next #3 and 08:00 plan — ACTIONED, zero new packs deliberately:** completed all requested corrections and evidential checks rather than padding the register with weak current-prevalence claims. Source-supported 2026 publisher metrics strengthen H005/H008, but do not create new distinct products.
- **Next #4 lead queue — RESEARCHED and DECLINED promotion:** **L11** first: Gen measured IPRoyal ~7,900 and PacketStream ~5,300 active protected Windows users at **provider level**, while the documented **Pawns.app.exe** Windows install path is from a **31 May 2025** software page. This is **not a post-November-2025 Pawns.app Windows installation or current PacketStream executable**; NetNut's ~474,000 provider users likewise lack a source-verified Windows product identifier. L11 remains open for product-specific evidence. **L9 OfferCore/InstallCore** detection labels and **L10 CHIP Downloader** installer names can uncover blocked downloads, but neither presently yields a newly verified active, branded, non-temp runtime with a dated real-host sighting. No misleading pack was added. **L8 PacketShare** remains open because the post-January-2026 IPIDEA network recovery and file samples do not prove an active PacketShare Windows installation. [^r05-gen][^r09-pawns]
- **Next #4 signer check — ACTIONED:** compared the newly checked Outbyte installer identity and Bright Data/EarnApp host context against the review's Unit 42 malware-grade signer list before retaining low-severity classifications; no matching named signer was established. This absence **is not safety proof**; sample-specific malware and control-tampering evidence still override low initial severity.
- **Next #5 — ACTIONED:** kept H and E in separate indexes; H004 remains **Incomplete** for lack of recent verified real-world presence. No `DriverPack.exe` in a Temp folder is tagged standalone; generic updater names require a verified product/path pair. Product presence, download, block, historic residue, current execution and relaying remain distinct. No KQL or other detection implementation was generated; no client workspaces were queried.

## Sources

All sources reviewed on **13 November 2026**. Undated pages are not represented as newly published research. Public sandbox observations establish sample-specific artefacts, not estate prevalence.

[^ol-mb]: Malwarebytes, [PUP.Optional.OneLaunch](https://www.malwarebytes.com/blog/detections/pup-optional-onelaunch), undated detection description.
[^ol-cybersift]: CyberSift, [Potentially Unwanted Software on Corporate Endpoints](https://www.cybersift.com/post/potentially-unwanted-software-on-corporate-endpoints), **27 March 2026** (page displays “Mar 27”; indexed publication metadata establishes year). One corporate workstation; no separately verified installation date.
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

[^pdf-polish]: ANY.RUN, [PDFImage_519340.exe / PDF Polish](https://any.run/report/aedc27e467ca25aee298b4bc85ee57d83bceb049ce751c06dac50cc20aea6712/44d19d08-5913-4254-8cc3-84c56759f670), **10 Apr 2026**: **Process information** `"C:\Users\admin\AppData\Roaming\PDFPolish\PDF Polish.exe"`, product metadata `Company: Jia Hao`; **General Info** Nullsoft installer. Signer not independently verified.
[^pdf-spark]: Malwarebytes, [PUP.Optional.SparkOnSoft](https://www.malwarebytes.com/blog/detections/pup-optional-sparkonsoft), updated **24 Oct 2025**, PDF Spark branding/Mainstay Crypto LLC.
[^pdf-control]: Controlware, [Beyond Potentially Unwanted Apps](https://www.controlware.de/fileadmin/controlware/sonstiges/dokumente/Security_Hinweise/Controlware_Beyond_Potentially_Unwanted_Apps_2025.pdf), **Dec 2025** PDF tooling investigation, **Oct 2025** customer observations, PDF Spark certs for Mainstay Crypto LLC/Crowd Sync LLC and significantly malicious other converter activity.
[^shift]: Malwarebytes, [PUP.Optional.ShiftBrowser](https://www.malwarebytes.com/blog/detections/pup-optional-shiftbrowser), page modified **18 August 2025**, confusing advertising for **manuals, recipes and templates** (not specifically PDF); authentic Shift Technologies Inc. identity documented in [repo September 2026 Shift report](../research/2026/2026-09-02-shift-browser-security-assessment.md).
[^pdf-signer]: Palo Alto Networks Unit 42, [Tracking TamperedChef Clusters via Certificate and Code Reuse](https://unit42.paloaltonetworks.com/tracking-tampered-chef-clusters/), **20 May 2026**, Table 1 lists Mainstay Crypto LLC / Crowd Sync LLC in **OneBrowser Signers** but **never names PDF Spark**; this is a signer link only. It describes several distinct malware clusters and stealer/RAT risk. Team-IT Group, [SparkOnSoft & OneBrowser corporate SOC case](https://www.team-it-group.de/blog/sparkonsoft-onebrowser-malware-soc-fallstudie), **26 Aug 2026**, two RDS servers. Sophos [KBA-000043676](https://support.sophos.com/support/s/article/KBA-000043676?language=en_US), **24 Sep 2026** per review, full content unavailable in this run.
[^hollow]: Intezer Research, [Two Trojan Families Trotting in Through Google Search Ads](https://research.intezer.com/blog/2026/07/two-trojan-families/), **27 Jul 2026**, HollowMare section and **Hollow Mare IOC table**, lists SagePDF/PowerDoc/PowerPlayer signatures/paths and distinguishes serious stealer/downloader findings.
[^sdk-guide]: Bright SDK, [Windows SDK Integration Guide (C/C++)](https://help.bright-sdk.com/hc/en-us/articles/16679042461329-Windows-SDK-Integration-Guide-C-C), complete guide currently redirects to authenticated support.
[^sdk-mouse]: ANY.RUN, [Mouse Server / Luminati SDK](https://any.run/report/ac6b186d8971f71d8a2d9477d71526fc8a0e5f7d03772c9e134813bce4fb2c89/6329de9f-12e9-4564-bdb7-db6dd99d68ad), **29 Jun 2023**, **Process information** PID 2228 exact command; **Modules** `lum_sdk32.dll`, one sample.

[^r04-huntress]: Huntress, [When PUPs Grow Fangs](https://www.huntress.com/blog/pups-grow-fangs), **14 April 2026**, opened **13 Nov 2026**. Identifier transcriptions: “Variations of executables” Table 7; “Code signing”; “File system artifacts”; “Scheduled tasks”; “WMI artifacts”. Sinkhole: 23,565 unique source IPs, 2,223 UK, not unique devices or client hit rate.
[^r04-infatica-file]: file.net, [infatica-service-app.exe](https://www.file.net/process/infatica-service-app.exe.html), “File information” section opened **13 Nov 2026**. Descriptive file metadata, not independently verified Authenticode evidence; no current presence date is asserted.
[^r04-infatica-grid]: GridinSoft, [K-Lite Infatica Removal](https://blog.gridinsoft.com/k-lite-codec-pack-infatica-removal/), page last updated **11 Aug 2026**, opened 13 Nov. Reports of Infatica after codec installs, not quantified estate prevalence or proof the official codec pack bundles it.
[^r04-infatica-mb]: Malwarebytes, [PUP.Optional.Infatica](https://www.malwarebytes.com/blog/detections/pup-optional-infatica), opened 13 Nov. Classifies a proxy-service PUP potentially arriving in bundles; no novel executable/path supplied.
[^r04-teamit]: Team-IT Group, [SparkOnSoft and OneBrowser SOC case](https://www.team-it-group.de/blog/sparkonsoft-onebrowser-malware-soc-fallstudie), **26 Aug 2026**, opened 13 Nov, reports software on two RDS servers. Does not establish every PDF Spark installer delivers OneBrowser.
[^r04-onebrowser]: GridinSoft, [OneBrowser Removal: Delete OneBUpdate and OB Leftovers](https://blog.gridinsoft.com/onebrowser-removal/), updated **4 Nov 2026**, opened 13 Nov. Exact names from “Quick answer”, “Stop OneBrowser updater services and tasks”, “Files and folders”, “Registry keys”. Third-party cleanup artefacts, not proof of live tenant deployment.
[^r04-gdata]: G DATA, [Projextor: Abusing Electron in Trojanized Productivity Applications](https://blog.gdatasoftware.com/2026/08/38468-projextor-abusing-electron), **17 Aug 2026**, opened 13 Nov, names DocConvertWizard, Food/Meal Formula and Kitchen Canvas, but does **not** name PDF Polish or Jia Hao. Packaging (NSIS, Squirrel, Inno Setup) and numbered installer suffixes alone cannot establish family identity.
[^r05-gen]: Gen Digital, [“Your IP, Their Traffic”](https://www.gendigital.com/blog/insights/research/residential-proxy-networks), published **30 Sep 2026**, reports **September 2026** protected Windows active users with software associated with a provider: Hola ~664k, Honeygain ~68k. Does **not** quantify specific branded executables, enterprise-only installations, active relay or embedded SDKs. Opened in Run 05.
[^r05-hola-vendor]: Hola official [Windows product downloads](https://hola.org/products/shared-dc), offering Browser and Windows desktop builds **1.258.330** when opened **13 Nov 2026**; [Hola Browser](https://hola.org/browser) and [FAQ](https://hola.org/faq) describe the free peer-resource versus Premium arrangement. Advertised version is not verified endpoint process metadata. Opened in Run 05.
[^r05-hola-sophos]: Sophos X-Ops, [“You do surprise me.exe: An unexpected executable in Hola Browser”](https://www.sophos.com/en-us/blog/you-do-surprise-me-exe-an-unexpected-executable-in-hola-browser), published **4 Jun 2026** per [publisher's author listing](https://www.sophos.com/en-gb/author/sophos-x-ops). “Here's looking at me.exe” and “Patching the pipeline”: SHA256, miner, copied process, service and vendor's fix claim. Does not implicate every Hola version. Opened in Run 05.
[^r05-hola-installer]: ANY.RUN, [`Hola-Browser.exe`](https://any.run/report/6f8dcbf79c942763ee42eaa733dc4e6d468bea5a4a0f739a9bf23084bac21294/650c037a-96d8-401c-8487-5a212760d6d3), **23 Feb 2025**, General Info; historic installer sample only, no current enterprise-prevalence claim. Automated loader verdict is sample-specific. Opened in Run 05.
[^r05-hg-vendor]: Honeygain, [official downloads](https://www.honeygain.com/download/), live **13 Nov 2026**; [“Windows: installation problems”](https://support.honeygain.com/hc/en-us/articles/30688446564636-Windows-installation-problems), updated **22 Oct 2026**, “Clean reinstall” lists Honeygain folders and HKCU key; these can be remnants. Opened in Run 05.
[^r05-hg-static]: PaysFair (commercial rival), [“What is inside Honeygain”](https://paysfair.com/blog/whats-inside-honeygain/), updated **24 Sep 2026**, “What we did” and installer's file table. Static study of `Honeygain_install.exe`, SHA256 `eaf6cf8841c168fa3d3a2d2e2d0b9c06693998415d125969824b987247fdad7c`; **no program execution or traffic observed**. Biased source disclosed and treated as identifier evidence only. Opened in Run 05.
[^r05-hg-sample]: ANY.RUN, [`Honeygain_install.exe`](https://any.run/report/eaf6cf8841c168fa3d3a2d2e2d0b9c06693998415d125969824b987247fdad7c/b798a2ed-c077-410f-8dd4-9aef21d3a917), **13 Mar 2026**, General Info, same SHA256 as static study: **one sample/build, not two infections**. Opened in Run 05.
[^r05-gdata]: G DATA, [“Projextor: Abusing Electron in Trojanized Productivity Applications”](https://blog.gdatasoftware.com/2026/08/38468-projextor-abusing-electron), **17 Aug 2026**; “Installation and Infection Chain” and “IOCs”. Names/hashes/URL copied from original. It **does not name PDF Polish or Jia Hao**. Opened in Run 05.
[^r05-jia]: Rabbit Knight, [“The FlipFormat_# Illusion: The Magic of the Doc Convert Wizard”](https://medium.com/@rabbit_knight/the-flipformat-illusion-the-magic-of-the-doc-convert-wizard-10036623d0e8), **4 Apr 2026**, “Files analyzed”, “Living Off the Land”, downloader and hypothetical DLL sideload. `Jia Hao` is *version metadata*, not independently verified signer. Opened in Run 05.
[^r05-polish-sample]: ANY.RUN, [`PDFImage_519340.exe` / PDF Polish](https://any.run/report/aedc27e467ca25aee298b4bc85ee57d83bceb049ce751c06dac50cc20aea6712/44d19d08-5913-4254-8cc3-84c56759f670), **10 Apr 2026**, “General Info”, “Process information” and “Registry activity”. The user `admin` is a *sandbox example*, not fixed hunting predicate. Opened in Run 05.
[^r05-ipidea]: Google Threat Intelligence Group, [“No Place Like Home Network: Disrupting the World's Largest Residential Proxy Network”](https://cloud.google.com/blog/topics/threat-intelligence/disrupting-largest-residential-proxy-network), **28 Jan 2026**, original takedown report; disruption does not establish every PacketShare binary stopped. Opened Run 05.

[^r06-wc-live]: Adaware Web Companion, [official Windows download](https://www.webcompanion.com/en/) and [publisher download landing page](https://free.webcompanion.com/), checked **13 Nov 2026**; proves available distribution only.
[^r06-rk-panel]: Comscore, [research panel privacy listing](https://www.comscore.com/About/Privacy), checked **13 Nov 2026**; lists RelevantKnowledge but gives no current installation count or dated endpoint sighting.
[^r06-sdk-live]: Bright SDK, [official monetisation partner page](https://bright-sdk.com/monetization), checked **13 Nov 2026**; named Windows examples are publisher claims, not verified current deployed binaries.
[^r06-sdk-tools]: Bright SDK, [official integration tools description](https://help.bright-sdk.com/hc/en-us/articles/49017749085713-What-integration-tools-does-Bright-SDK-provide), updated **22 Jul 2026**, opened 13 Nov; describes Windows support and tooling, not population.
[^r06-sdk-file]: file.net, [net_updater32.exe details](https://www.file.net/process/net_updater32.exe.html), opened **13 Nov 2026**, undated reference of SDK labels and specific Bright VPN service; not a fresh incident nor certificate validation.
[^r07-iobit-press]: IObit, [Driver Booster 14 launch press release](https://www.iobit.com/en/pressroom-driver-booster-14-launches-with-new-game-dll-fixer-and-expanded-23m%2B-driver-database-785.php), **16 Sep 2026**; opened 13 Nov. Current product release, not enterprise adoption.
[^r07-iobit-live]: IObit, [official Driver Booster 14 Windows download](https://www.iobit.com/en/driver-booster.php), live **13 Nov 2026**. No independent current-user count.
[^r07-iobit-mb]: Malwarebytes, [PUP.Optional.iObitDriverBooster](https://www.malwarebytes.com/blog/detections/pup-optional-iobitdriverbooster), opened 13 Nov; main process/path and two scheduler task names appear under “Malwarebytes removal log”/“Traces/IOCs”, sample date **12 Mar 2019**, version **6.3.0**. Not IObit version 14 or Energizer's similarly named product.
[^r07-ut-live]: µTorrent, [official product page](https://www.utorrent.com/) and [Windows Classic download page](https://www.utorrent.com/intl/it/downloads/win/), live **13 Nov 2026**, static overall download claims not active Windows/enterprise prevalence. Windows page's `%AppData%\uTorrent` language-pack directory is not proof of execution.
[^r07-ut-ms]: Microsoft Security Intelligence, [uTorrent PUA classification search](https://www.microsoft.com/en-us/wdsi/threats/threat-search?query=PUA%3AWin32%2FuTorrent), opened 13 Nov; bundled-installer PUA label last updated **15 Feb 2021**. Does not establish installation or malicious client use.
[^r07-ut-forum]: Malwarebytes support forum, [uTorrent exception thread](https://forums.malwarebytes.com/topic/323305-resolved-any-way-to-exclude-utorrent-from-scans/), **1 Mar 2025** user report of executable and two exact Windows paths. User report is not provider-certified prevalence or a present-day sample.
[^r07-ut-legacy]: µTorrent Community Forum, [2015 antivirus troubleshooting log](https://forum.utorrent.com/topic/98398-utorrentexe-detected-by-anti-virus-and-anti-malware-software/), **7 May 2015** original diagnostic file version info `Company="BitTorrent, Inc."` and `ProductName="µTorrent"`; not current digital signing validation.
[^r07-lumen]: Lumen Black Lotus Labs, [“Symbiotic Parasites: The Modern Proxy Ecosystem”](https://www.lumen.com/blog/en-us/symbiotic-parasites-the-modern-proxy-ecosystem), **24 Jul 2026**, section “IPIDEA”; IPIDEA network recovery and ~10m daily IPs not attributable specifically to PacketShare Windows installs.

[^r08-ob-live]: Outbyte, [official Driver Updater Windows download](https://outbyte.com/software/driver-updater/), live **13 Nov 2026**. Does not measure enterprise installs.
[^r08-ob-grid]: GridinSoft, [Outbyte Driver Updater removal](https://blog.gridinsoft.com/outbyte-driver-updater-removal/), last updated **7 Jul 2026**, current removal guidance not estate prevalence.
[^r08-ob-mb]: Malwarebytes, [PUP.Optional.Outbyte](https://www.malwarebytes.com/blog/detections/pup-optional-outbyte), opened **13 Nov 2026**; detection applies broadly, not an observed Outbyte Driver Updater instance.
[^r08-ob-sample]: ANY.RUN, [windows-outbyte-driver-updater.exe](https://any.run/report/3c3204ce0daa4fd1af3d4f017fba57b793651719944c317324b23ef2bb867195/64713c27-ff5c-4099-9c17-7d0d11875282), **17 May 2025**, **Processes → Process information** PID 2064/4164/4212: exact C:\Program Files (x86)\Outbyte\Driver Updater\DriverUpdater.exe, version Company Outbyte and Description Driver Updater. **One sandbox installer/sample**, not multiple enterprise sightings or proven stealer operations.
[^r08-ob-file]: file.net, [DriverUpdater.exe](https://www.file.net/process/driverupdater.exe.html), opened **13 Nov 2026**, generic filename shared with multiple products, thus never a standalone Outbyte verdict.
[^r08-dp-live]: DriverPack, [official administrator downloads](https://driverpack.io/en/foradmin/), live **13 Nov 2026**, DriverPack Online 17.11.108, current distribution only.
[^r08-dp-mb]: Malwarebytes, [PUP.Optional.DriverPack](https://www.malwarebytes.com/blog/detections/pup-optional-driverpack), “Short bio” and **6 May 2018 removal log**; task-cache path and DRPSu folder observed historically, not current release.
[^r08-dp-file]: file.net, [DriverPack.exe file information](https://www.file.net/process/driverpack.exe.html), opened **13 Nov 2026**, process and historic product metadata DriverPack Solution / driverpack online, not validated current signer.
[^r08-dp-faq]: DriverPack, [How to install DriverPack](https://driverpack.io/en/faq/install), opened **13 Nov 2026**, says no conventional installation is required.
[^r08-packet]: GridinSoft ThreatInfo, [PacketShare.exe file](https://threatinfo.net/files/PacketShare.exe-833ad5d123c61568a48e713dda647162), analysis date **12 Sep 2026**, product PacketShare, reported signer DATALABS LIMITED; file sample not known active install or post-disruption traffic; ignore stale relative-age text.

[^r09-ob-signer]: GridinSoft, [outbyte-driver-updater.exe file analysis](https://gridinsoft.com/online-virus-scanner/id/d567b038197b308d90bea2c10217842a557b384df4bec6e68086e705a697911b), analysed **8 Feb 2025**; **Certificate Chain Analysis → Signers** explicitly `Outbyte Computing Pty Ltd`, signed **28 Nov 2024**. This is the **installer**, not verified present-day `DriverUpdater.exe`.
[^r09-hg-path]: Advanced Uninstaller, [Honeygain 0.10.7.0](https://www.advanceduninstaller.com/Honeygain-3f2ab2050f1108e67d21b5e44607b2ce-application.htm), “A guide to uninstall Honeygain” names the **`C:\Users\UserName\AppData\Roaming\Honeygain`** folder and `Honeygain.exe` main executable; `UserName` is the page's placeholder. Old version only, not a 2026 endpoint sighting.
[^r09-earnapp]: Advanced Uninstaller, [EarnApp 1.597.152](https://www.advanceduninstaller.com/EarnApp-22ac4b24a2ac35f6b4197f8ead05ae4b-application.htm), “A way to uninstall EarnApp”: publisher `Bright Data Ltd.`, install folder `C:\Program Files (x86)\EarnApp`, executable `earnapp.exe` and co-installed `net_updater32.exe`. App/version-specific software record, not observed enterprise execution or proof of traffic relaying.
[^r09-pawns]: Advanced Uninstaller, [Pawns.app 1.23.4](https://www.advanceduninstaller.com/Pawns_app-1_23_4-36259ad20e4e014b2c68d68c42c15472-application.htm), page written **31 May 2025**, historical `Pawns.app.exe` under `C:\Program Files\Pawns.app\`. That file-specific evidence predates the 12-month cutoff despite September 2026 **provider-level** IPRoyal measurement in Gen Digital's separate report.
