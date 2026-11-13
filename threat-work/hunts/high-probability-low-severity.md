# High-probability, low-severity threat hunts

**Last researched:** 13 November 2026  
**Latest research run:** 05 — two low-severity packs H009/H010 and E002 Jia Hao / Projextor escalation pack
**Active candidates:** Eight low-severity H packs (H001, H003, H004, H005, H007, H008, H009, H010), and three escalation E packs (E001, E002, E003). H002 and H006 retired.
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

Retired IDs are not reused. Eight active low-severity packs are indexed below; H006 was reclassified as E003, not counted as new.

## Hunt index — low-severity packs

**Likelihood tiers are evidence categories, not client hit-rate predictions.** A = measured contemporary activity across a real population; B = a recent dated observation, distribution account or sample without a reliable population denominator; C = mostly historical or undated distribution. An article's publication date is not an installation date. Ordered by strength and recency.

| ID | Candidate | Tier | Newest dated evidence | Added | Status |
| --- | --- | --- | --- | --- | --- |
| [H009](#h009-hola-browser-and-desktop-vpn) | Hola Browser / desktop VPN | **A (provider-level)** | 30 Sep 2026: ~664k provider-associated active Windows users; live downloads 13 Nov | Run 05 (L5) | Finished: branded presence, miner escalates |
| [H010](#h010-honeygain-windows-bandwidth-sharing-app) | Honeygain Windows bandwidth-sharing | **A (provider-level)** | 30 Sep 2026: ~68k active Windows users; vendor support 22 Oct | Run 05 (L7) | Finished: branded execution, relay unproven |
| [H007](#h007-dragon-boss-solutions-browser-updaters) | Dragon Boss Solutions browser/updater family | **A** | 14 Apr 2026: 23,565 source IPs, of which 2,223 UK | Run 04 (L3) | Finished: presence only; check malware escalation |
| [H008](#h008-infatica-p2b-proxy-component) | Infatica P2B component | **B** | 11 Aug 2026: published consumer-install follow-up | Run 04 (L4) | Finished: product execution; relaying unproven |
| [H001](#h001-onelaunch) | OneLaunch | **B** | 27 Mar 2026 corporate report | Run 01 | Incomplete: typed identifier table |
| [H005](#h005-bright-sdk--luminati-sdk-in-host-apps) | Bright/Luminati SDK in host apps | **B (tentative)** | 31 Jan 2026 repeat detonation of one 2025 installer | Run 02, widened Run 03 | Incomplete: current corporate prevalence and typed table |
| [H004](#h004-relevantknowledge) | RelevantKnowledge | **C** | 8 Dec 2025 public sandbox execution | Run 02 | Incomplete: evidence of current real-world distribution |
| [H003](#h003-adaware-web-companion) | Adaware Web Companion | **C** | 2023 company sightings | Run 01 replacement | Incomplete: recent dated organisational evidence |

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

## H005: Bright SDK / Luminati SDK in host apps

**Added:** Run 02 as Bright VPN; widened **in place** in Run 03 per Review 001. Bright VPN and EarnApp remain example host apps rather than fresh candidate IDs.

**Hypothesis:** Third-party Windows utilities can embed the **Bright SDK**, formerly **Luminati SDK**, allowing an unapproved background component on a managed endpoint without a Bright VPN installation. A capability for public-web collection using participant connections is documented by Bright VPN; evidence of the component does **not** prove actual relaying on a specific device. [^bv-faq][^bv-partners][^bv-mb]

**Evidence (B, tentative):** A **June 2023** Mouse Server execution shows SDK inside an unrelated application's directory. Bright VPN ANY.RUN reports **6 Nov 2025** and **31 Jan 2026** share SHA-256 `1929fa577e90828053bfa6e9524837b75ddc2bb8c00578d7ef6754cef37e25ac`: **one installer detonated twice**, not two builds or distinct infections. No SDK-only business prevalence measured. [^sdk-mouse][^bv-sample][^bv-sample-2026]

| Pivot | Evidence and bounds |
| --- | --- |
| `net_updater32.exe` / `net_updater64.exe` **in any directory** | SDK candidates. Verify via version product `Bright SDK` or `Luminati SDK`, host, related modules and actual signer where available. Never use a loose updater filename as final identification. Vendor integration guide redirects behind authentication and could not be read in full. [^sdk-guide][^sdk-mouse] |
| `"C:\Program Files\Mouse Server\net_updater32.exe" --install win_wifimouse.necta.us` | **Exact ANY.RUN Process information** command, PID 2228, **29 Jun 2023**, with `Company: Luminati Networks Ltd.` and `Description: Luminati SDK Updater`. Its **Modules** section lists `c:\program files\mouse server\lum_sdk32.dll`. `win_wifimouse.necta.us` identifies this **host**; `--install win_<app-id>` is a sample-supported **shape**, not mandatory on every build. [^sdk-mouse] |
| `Bright VPN.exe` (runtime), `brightvpn_installer.exe` (installer), `net_updater32.exe` (candidate SDK) | Names visible in **2025** public report. The formerly claimed `\Bright VPN\` plus `win_brightvpn.com` path/argument is **UNCONFIRMED** by the publicly visible process details: do **not** treat it as verified. [^bv-sample][^bv-sample-2026] |
| `PUP.Optional.BrightData` | Broad product-family detection lead, not proof of a running SDK or proxy relay. [^bv-mb] |

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
| Web Genius | process name | UniversalUpdater.exe | DeviceProcessEvents.FileName | pair with Web Genius folder (generic name) | [^r04-huntress] |
| Web Genius | folder | C:\Program Files (x86)\Web Genius Solutions\Web Genius | DeviceProcessEvents.FolderPath | pair with UniversalUpdater.exe | [^r04-huntress] |
| Additional updaters | process names | WinDefenseThree.exe; RaceCarTwo.exe; TableBoatTwo.exe | DeviceProcessEvents.FileName | pair with source-described corresponding program folder or signer | [^r04-huntress] |
| **Malware escalation** | scheduled tasks | ClockSetupWmiAtBoot; RemoveClockPeriodic | DeviceEvents.AdditionalFields when ActionType=ScheduledTaskCreated, or ingested task events | standalone malicious-chain lead | [^r04-huntress] |
| **Malware escalation** | WMI consumers | MbRemovalMbSetupKillConsumer; MbRemovalMbSetupKillConsumerTrace | DeviceEvents.AdditionalFields when ActionType=WmiBindEventFilterToConsumer | standalone malicious-chain lead | [^r04-huntress] |
| **Malware escalation** | scripts | ClockRemoval.ps1; ClockRemoval-WmiBoot.ps1 | DeviceFileEvents.FileName | standalone malicious-chain lead with contextual verification | [^r04-huntress] |
| **Malware escalation** | folder | %SystemRoot%\System32\config\systemprofile\AppData\Local\WMILoad\ | DeviceFileEvents.FolderPath | pair with task, script or WMI lead | [^r04-huntress] |

**Hunt:** Look for process execution in the 30-day retained window, validate publisher/product or distinctive folder, then inspect any collected task, WMI, AV-exclusion, file and installer events. Process names alone do not demonstrate a current install; browser cache files and DNS-only traffic are not positives. **A confirmed matched process proves family presence, not that the endpoint received the AV killer.** The ClockRemoval/WMI/Defender-disable chain is escalation-grade. Legitimate intentional third-party browser adoption is possible, subject to client approval, but does not make security-control disabling benign.

## H008: Infatica P2B proxy component

**Hypothesis, tier B (L4):** Infatica SDK/P2B may be installed alongside consumer software. Malwarebytes classifies it as a potentially unwanted proxy service that may be bundled. GridinSoft **updated an account on 11 August 2026** describing reports following codec installs, but this is not measured enterprise prevalence or proof the official K-Lite package bundles it. [^r04-infatica-mb][^r04-infatica-grid]

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

**Hypothesis, tier A (provider-level, L5):** Hola's Windows Browser and desktop VPN remain available on **13 November 2026**. Gen Digital published **30 September 2026** measurements of about **664,000 active Windows users with software associated with Hola** in its September snapshot. This is *not* Hola Browser-specific execution, client/UK-estate prevalence, or proof of relayed traffic; the research excludes embedded SDKs. This branded Windows-product hunt is distinct from H005's embedded Bright SDK despite the related proxy business model. [^r05-gen][^r05-hola-vendor]

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

**Hypothesis, tier A (provider-level, L7):** Gen Digital's **September 2026** Windows protection dataset found approximately **68,000 active users with software associated with Honeygain**; neither client prevalence nor confirmed proxy relaying is measured. Honeygain's Windows app was still available **13 November 2026**; the vendor updated its support page **22 October 2026**. It is a distinct user-facing product, not an H005/H008 SDK alias. [^r05-gen][^r05-hg-vendor]

**Exact identifier table** — product-specific files from PaysFair's **24 September 2026** “What the Honeygain installer puts on your PC” static extraction; **a competitor's report, no sample execution**. Folder/key from Honeygain's official “Clean reinstall” steps. The strings are useful seeds, not proven executed processes until seen in an ingested workspace.

| Product | Type | Exact value | Log Analytics table.column | Match rule | Source |
| --- | --- | --- | --- | --- | --- |
| Honeygain UI | installed executable name in file table | `Honeygain.exe` | `DeviceProcessEvents.FileName` | **standalone** branded runtime candidate; confirm actual process/product | [^r05-hg-static] |
| Honeygain updater | executable name in file table | `HoneygainUpdater.exe` | `DeviceProcessEvents.FileName` | pair with Honeygain product identity/path; updater not relay | [^r05-hg-static] |
| Honeygain engine | DLL name in installer | `hgwin.dll` | `DeviceFileEvents.FileName` | pair with Honeygain product folder; file event is not DLL-load evidence | [^r05-hg-static] |
| Honeygain | installer file | `Honeygain_install.exe` | `DeviceProcessEvents.FileName` or `DeviceFileEvents.FileName` | **standalone installer lead**, not runtime proof | [^r05-hg-static][^r05-hg-sample] |
| Honeygain | local folder | `%localappdata%\Honeygain`; `%appdata%\Honeygain` | `DeviceFileEvents.FolderPath` or `DeviceProcessEvents.FolderPath` when appropriate events exist | pair with process; vendor describes **leftovers** too | [^r05-hg-vendor] |
| Honeygain | user registry key | `HKEY_CURRENT_USER\Software\Honeygain` | `DeviceRegistryEvents.RegistryKey` where collected | pair with process; a change event is not current inventory | [^r05-hg-vendor] |

**Hunt:** Confirm execution of branded software via Sentinel process telemetry in a 30-day window, identify the user/authorised installation, and optionally correlate network, file and registry events if ingested. `Honeygain.exe` execution establishes product use, **not** that `hgwin.dll` loaded or that third-party traffic flowed. Escalate covert installation, demonstrated traffic relay inconsistent with client policy, or independently evidenced malware. A knowingly authorised earning app could be benign under policy. PaysFair's installer and the public sandbox sample have the **same hash**, so they are not two builds or two observed infections. [^r05-hg-static][^r05-hg-sample]

## Same route, not low severity — escalation packs

These are **incident leads**, separate from the low-severity H list; neither a PUP label nor a shared search-advert route proves a host is infected.

| ID | Pack | Newest dated source | Added | Status |
| --- | --- | --- | --- | --- |
| [E001](#e001-pdf-spark-and-onebrowser) | PDF Spark / OneBrowser signer overlap | OneBrowser guide updated 4 Nov 2026 | Run 04 | Finished: qualified signer/process/task pivots |
| [E002](#e002-jia-hao-document-utility-siblings-and-projextor-comparison) | Jia Hao / PDF Polish sibling context and Projextor | G DATA 17 Aug 2026; PDF Polish 10 Apr 2026 | Run 05 | Finished: malware-grade investigation; attribution qualified |
| [E003](#e003-cl-unk-1090-and-hollowmare-document-tools) | CL-UNK-1090 / HollowMare document tools | Intezer 27 Jul 2026, SagePDF observed Jan 2026 | Run 04 reclassification of H006 | Finished: sample and installer stages separated |

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
