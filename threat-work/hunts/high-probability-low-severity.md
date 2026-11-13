# High-probability, low-severity threat hunts

**Last researched:** 13 November 2026  
**Latest research run:** 03 — one new pack and one evidence-based shortfall  
**Active candidates:** Five; H002 retired as already known  
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
| PDF Polish, PDF Spark, Shift Browser | **Confirmed previous hits.** PDF Polish sample metadata identifies `Jia Hao` but no verified code signer; PDF Spark samples signed under Mainstay Crypto LLC and Crowd Sync LLC; authentic Shift publisher is Shift Technologies Inc. Advertising similarity is not common ownership. [^pdf-polish][^pdf-spark][^pdf-control][^shift] |
| Wave Browser, ClickFix | Already known; excluded as new. |
| OneStart / BaoLoader-associated activity | Not suitable for a routine low-severity PUP entry on the evidence reviewed. Preserve the distinction between product presence and malicious activity. [^excluded-onestart] |

Retired IDs are not reused. The active candidates below total five: two from corrected Run 01, two from Run 02 and one new Run 03 pack.

## Hunt index

**Likelihood tiers are evidence categories, not hit-rate forecasts:** **A** means measured active software prevalence within 12 months; **B** means a dated organisational sighting or observed recent distribution/sample, but no measured relevant population; **C** means mainly historic/undated evidence. A later paper date is not an installation date. Index ordered B before C; no active card has robust A-grade prevalence.

| ID | Candidate | Tier | Newest dated presence evidence | Added | Status |
| --- | --- | --- | --- | --- | --- |
| [H001](#h001-onelaunch) | OneLaunch | **B** | 27 Mar 2026 corporate hunt report | Run 01 | Not run |
| [H005](#h005-bright-sdk-luminati-sdk-in-host-apps) | Bright/Luminati SDK across host apps | **B (tentative)** | 31 Jan 2026 second detonation of Nov 2025 sample (one hash) | Run 02; expanded Run 03 | Not run |
| [H006](#h006-hollowmare-document-tool-browser-change-pack) | HollowMare browser-change pack | **B (tentative)** | Jan 2026 variant discussed in Jul 2026 research | Run 03 | Not run |
| [H004](#h004-relevantknowledge) | RelevantKnowledge | **C** | 8 Dec 2025 sandbox sample, no measured corporate rate | Run 02 | Not run |
| [H003](#h003-adaware-web-companion) | Adaware Web Companion | **C** | 2023 company sightings; newer product guidance undated | Run 01 correction | Not run |

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

## H006: HollowMare document-tool browser-change pack

**Added:** Run 03 from **Review 003 lead L2**. **B tentative.** **Hypothesis:** misleading search advertisements for PDF, archive and media tools lead to deceptive installers that covertly change search engines or install extensions. Intezer's **27 July 2026** research calls the **HollowMare browser-changing subset PUA**, describing the newer **SagePDF** variant in **January 2026**. This is an *advertising-route* sibling of confirmed PDF-related hits; there is **no established common publisher, signer or November distribution**. [^hollow]
**Per-product pivot table, exact strings from Intezer's Hollow Mare IOC section** (not sandbox process descriptions):

| Sibling | Source-backed identifier | Interpretation |
| --- | --- | --- |
| **SagePDF** | `%TEMP%\SagePdf\SageId.txt`; sample signing subject `Chrono Orion LTD`; SHA-256 `287a3a052ff0b2c495658fa90c5a9bd76f16d832d82138f6f8e87f9e2f578ab1` | Sample/artifact; **not runtime proof**. |
| **PowerDoc** | `%LocalAppData%\pwrDoc\PowerDoc.exe`; `%LocalAppData%\pwrDoc\pwrDoc.txt`; signing subject `GOLD HARMONY LTD` | Specific program/file markers; corroborate process execution. |
| **PowerPlayer** | `%TEMP%\PowerPlayer\NativePowerPlayer.exe`; signing subject `TAMARISK INTERACTIVE LTD` | Temporary launcher, not guaranteed long-term persistence. |

**High-level Sentinel hunt:** Search collected process events for exact named applications, corroborate their paths/product identity and any available signer; correlate browser search/extension changes with file/registry telemetry **only where ingested**. Record installer-only vs active execution vs proven browser change, and check client approval.
**Noise and severity dispute:** Unrelated search redirects and old installer files are not product hits. **Controlware Dec 2025 judged related CrystalPDF/PowerDoc samples malware**, citing persistence and communications; Intezer's broader report contains **stealer/exfiltration** entries for ConvertyFile/OneZip and **downloader/backdoor SilentMare**. **Keep those high-severity behaviours outside this low-severity pack**, and escalate observed malware execution, unauthorised persistence or data access. [^hollow][^pdf-control]
**Likelihood limitation:** A July research publication and January observed variant do not prove active distribution in November. Re-rate downward if newer enterprise evidence cannot be found.

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

### Run 03: review actions, corrections and deliberate shortfall

**Read first:** **Review 003 · 2026-11-13 01:02 GMT**, reviewed register commit `b8153a2`, review-file blob `a30fbcd586b720a60c26d2110b1ee3f429143ed9`. Standing guidance and the updated lead queue followed; `reviews.md` was not modified.

- **Review 003 Next #1 / L1 — researched, DECLINED a new low-severity ID.** Verified PDF Spark signers **Mainstay Crypto LLC** and **Crowd Sync LLC** and source-linked OneBrowser/software under those signers. Public original research by Unit 42 describes this ecosystem as **TamperedChef-style malware** with arbitrary-payload, stealer/RAT capability; a **26 Aug 2026** SOC case describes malicious software on two RDS servers. This makes a **high-priority separate malware hunt**, not a safe “low-severity PUA” pack. Sophos signer-specific KBA (dated **24 Sep 2026** in the review) could not be opened in full. Relevant installer/brand names `PDFSparkWare_*.exe`, `PDFSparkOnSoft.exe`, `pdfsetup.exe` and `OneBrowser` are **research context**, not approved low-severity pivots. **Shortfall deliberately accepted**. [^pdf-signer]
- **Review 003 Next #1 / L2 — ACTIONED:** H006 includes SagePDF, PowerDoc and PowerPlayer browser-change indicators, shared search-ad route but not a falsely shared signer. **DECLINED** treating ConvertyFile/OneZip stealer evidence, SilentMare or documented malicious CrystalPDF cases as low severity. [^hollow][^pdf-control]
- **Review 003 Next #2 — ACTIONED with limit:** Found PDF Polish dated **10 Apr 2026** process version field `Company: Jia Hao` and a Nullsoft installer. **Actual code signer not verified**; no documented same-publisher new product. Already-covered entry says so rather than guessing. [^pdf-polish]
- **Review 003 Next #3 — ACTIONED:** No JustAskJacky, SilentMare, TamperedChef, tampered OneBrowser/AppSuite or other malware reclassified as low-severity.
- **Review 002 items 1–3 — ACTIONED:** Added PDF Spark as confirmed previous hit; compared the distinct publishers and advertising channels; added evidence-based likelihood tiers, newest source activity and recency ordering; H001 B, H003 C, H004 C. **Review 002 #4 — DECLINED/deferred:** Honeygain and other unrelated consumers await **L3–L5** because Review 003 explicitly prioritises L1 and L2. **#5 — ACTIONED:** Carried Review 001 guidance forward.
- **Review 001 corrections 1–4 — ACTIONED:** Corrected H001 27 March 2026 publication date and assessment, not installation date; corrected **one Bright installer hash analysed twice**; labelled prior `\Bright VPN\`/`win_brightvpn.com` path/argument **unconfirmed** and added installer-stage `brightvpn_installer.exe`; separated index `Added` from uniform `Not run` status.
- **Review 001 Next 1–2 — ACTIONED:** Added tier definitions and expanded existing H005 from a Bright VPN name-only hunt to Bright/Luminati **SDK across any host path**, with exact SDK command and source report section. The vendor guide redirects to login; full text **not** claimed to be read. EarnApp remains host context, not new ID.
- **Review 001 Next 4–5 — ACTIONED:** Added one compact new pack and shared `Applies to every card` guidance. **A single defensible pack beats a forced second**; L1 needs separate higher-severity treatment. Later runs should research L3 then L4 then L5. No workspaces queried and no field results claimed.

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
[^shift]: Malwarebytes, [PUP.Optional.ShiftBrowser](https://www.malwarebytes.com/blog/detections/pup-optional-shiftbrowser), undated PDF/manual/recipe misleading ads; authentic Shift Technologies Inc. identity documented in [repo September 2026 Shift report](../research/2026/2026-09-02-shift-browser-security-assessment.md).
[^pdf-signer]: Palo Alto Networks Unit 42, [Tracking TamperedChef Clusters via Certificate and Code Reuse](https://unit42.paloaltonetworks.com/tracking-tampered-chef-clusters/), **2026**, names Mainstay Crypto LLC/Crowd Sync LLC in OneBrowser signer group and describes distinct malware clusters, loaders/infostealers/RAT risk. Team-IT Group, [SparkOnSoft & OneBrowser corporate SOC case](https://www.team-it-group.de/blog/sparkonsoft-onebrowser-malware-soc-fallstudie), **26 Aug 2026**, two RDS servers. Sophos [KBA-000043676](https://support.sophos.com/support/s/article/KBA-000043676?language=en_US), **24 Sep 2026** per review, full content unavailable in this run.
[^hollow]: Intezer Research, [Two Trojan Families Trotting in Through Google Search Ads](https://research.intezer.com/blog/2026/07/two-trojan-families/), **27 Jul 2026**, HollowMare section and **Hollow Mare IOC table**, lists SagePDF/PowerDoc/PowerPlayer signatures/paths and distinguishes serious stealer/downloader findings.
[^sdk-guide]: Bright SDK, [Windows SDK Integration Guide (C/C++)](https://help.bright-sdk.com/hc/en-us/articles/16679042461329-Windows-SDK-Integration-Guide-C-C), complete guide currently redirects to authenticated support.
[^sdk-mouse]: ANY.RUN, [Mouse Server / Luminati SDK](https://any.run/report/ac6b186d8971f71d8a2d9477d71526fc8a0e5f7d03772c9e134813bce4fb2c89/6329de9f-12e9-4564-bdb7-db6dd99d68ad), **29 Jun 2023**, **Process information** PID 2228 exact command; **Modules** `lum_sdk32.dll`, one sample.
