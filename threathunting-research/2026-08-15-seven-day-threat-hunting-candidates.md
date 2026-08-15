# Proactive Threat Hunting Research — 9–15 August 2026

**Research date:** 15 August 2026  
**Window:** 9–15 August 2026  
**Purpose:** Identify campaigns, threat actors, newly disclosed or newly exploited CVEs, and other developments with practical value for proactive threat hunting.

The selection below is biased toward **attackability + observability**: activity that can be translated into enterprise hunting hypotheses across endpoint, identity, cloud, network, and infrastructure telemetry rather than simply tracked as threat-news awareness.

---

## Executive shortlist

### 1. Lazarus / Operation Dream Job + CVE-2026-68820

**Priority:** Highest  
**Status:** Confirmed exploited zero-day

The strongest candidate of the week. Check Point attributed a new Operation Dream Job wave to Lazarus targeting defence/aerospace-related personnel through fake recruitment material. A trojanised PDF viewer dubbed **SecurityPDF** side-loads malicious code and deploys the **Troy** backdoor. Lazarus then exploits the Windows AFD.sys use-after-free **CVE-2026-68820** to gain SYSTEM and deploy its FudModule rootkit.

The chain also includes compromised Roundcube/WordPress infrastructure, RelayShell, and Microsoft Graph/OneDrive communications.

**Why hunt it:** This gives an unusually rich intrusion chain:

`social engineering → trojanised application → DLL side-loading → backdoor → Windows LPE → SYSTEM → kernel rootkit / EDR interference → cloud-assisted C2`

**High-value hypotheses:**

- Legitimate-looking document/PDF software unexpectedly loading DLLs from its local directory.
- Recruitment-themed downloads followed by execution.
- Uncommon processes interacting with Microsoft Graph or OneDrive.
- Suspicious privilege transition to SYSTEM after user-context execution.
- Security telemetry or controls abruptly disappearing after suspicious execution.
- Process, module-load, and network activity consistent with DLL side-loading followed by outbound C2.

**Primary reading:**

- Check Point Research — *Shattering the Dream: When a Job Offer Becomes a Zero-Day Attack*  
  https://research.checkpoint.com/2026/shattering-the-dream-when-a-job-offer-becomes-a-zero-day-attack/
- TechRadar — reporting on the North Korean recruitment campaign  
  https://www.techradar.com/pro/security/this-north-korean-recruitment-scam-was-so-convincing-it-even-fooled-google

---

### 2. VMware vCenter CVE-2026-59310 exploitation

**Priority:** Critical where VMware exists  
**Status:** Active exploitation

CVE-2026-59310 is a critical vCenter Syslog Server directory-traversal / remote-code-execution vulnerability. Active exploitation was identified during the research window. Shadowserver reporting indicates that compromised systems have been observed with a **reverse_ssh persistence mechanism**, and affected systems should be treated as fully compromised rather than as simple scanner hits.

**Why hunt it:** vCenter provides a strategically powerful position over virtual infrastructure. Successful exploitation has meaningful post-exploitation artefacts, giving defenders something substantially better than internet scanner noise to hunt.

**High-value hypotheses:**

- vCenter appliances spawning processes outside their historical baseline.
- New files or persistence artefacts on the appliance.
- Outbound SSH or reverse-tunnel behaviour originating from vCenter.
- Connections from vCenter to previously unseen internet destinations.
- vCenter compromise followed by unusual operations across multiple guest systems.

**Primary reading:**

- Broadcom security advisory  
  https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017
- Shadowserver — VMware vCenter CVE-2026-59310 exploitation victim reporting  
  https://www.shadowserver.org/what-we-do/network-reporting/vmware-vcenter-cve-2026-59310-exploitation-victim-special-report/

---

### 3. Gunra ransomware / Golden Community

**Priority:** High  
**Status:** Active campaign

A new joint advisory details the expanding Gunra ransomware-as-a-service operation. Initial access has included exploitation of internet-facing Fortinet infrastructure, followed by credential use, SMB movement, **Impacket `psexec.py` / `smbclient.py`**, VDI access, exfiltration, log destruction, and ransomware deployment.

**Why hunt it:** This is more useful than an encryptor-IOC hunt because the pre-encryption chain contains broadly reusable ransomware behaviours.

**High-value hypotheses:**

- VPN or perimeter access from previously unseen infrastructure followed shortly by internal SMB.
- Privileged authentication soon after remote-access activity.
- `psexec`-like remote service execution.
- A single identity traversing many internal systems in a short period.
- Unusual interactive activity through administrative or IT VDI.
- Backup or disaster-recovery manipulation.
- High-volume collection or exfiltration followed by log destruction.

**Primary reading:**

- CISA joint cybersecurity advisory AA26-222A  
  https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-222a
- ITPro — Gunra ransomware reporting  
  https://www.itpro.com/security/ransomware/warning-issued-over-gunra-ransomware-gang-as-attacks-ramp-up-globally

---

## Full candidate set

### 4. Metabase CVE-2026-72898

**Status:** Active exploitation / critical

An unauthenticated SQL-injection vulnerability in self-hosted Metabase's password-reset functionality can lead to administrative access and has been reported as exploited in the wild.

**Hunt focus:**

- Requests against password-reset API paths from unusual or external sources.
- Administrative sessions immediately following suspicious reset activity.
- Unexpected user, role, or configuration changes.
- Database access inconsistent with the affected host's normal behaviour.
- New outbound connectivity from the Metabase host after suspicious HTTP activity.

**Reading:**

- NVD — CVE-2026-72898  
  https://nvd.nist.gov/vuln/detail/CVE-2026-72898

---

### 5. City-Forum — Salesforce Experience Cloud + ServiceNow data theft

**Status:** Newly disclosed active campaign

Reco disclosed a long-running actor using custom tooling to enumerate and extract data exposed to unauthenticated or guest users through Salesforce Experience Cloud and ServiceNow portals.

This is particularly interesting because **nothing necessarily has to break**. There may be no malware, exploit, or failed-authentication event. The underlying action may be permitted by the application while still producing a damaging security outcome.

**Hunt focus:**

- High-volume guest-user enumeration.
- Repeated Aura, GraphQL, search, or object-discovery operations.
- Sequential access across large numbers of objects or records.
- Unusual source-IP or ASN concentration behind anonymous retrieval.
- Guest-user activity materially outside historical request volume.

**Reading:**

- Reco — City-Forum campaign  
  https://www.reco.ai/blog/city-forum-campaign-salesforce-servicenow
- Help Net Security — Salesforce / ServiceNow guest-user exposure  
  https://www.helpnetsecurity.com/2026/08/12/salesforce-servicenow-guest-user-exposure/

---

### 6. Coordinated GitHub PAT compromise / repository exfiltration

**Status:** Newly disclosed campaign

Wiz disclosed a multi-organisation investigation in which compromised employee personal access tokens were used for reconnaissance and large-scale private-repository cloning.

This is a strong behavioural-hunting candidate because the credentials themselves may be valid. The useful signal lies in how they are used.

**Hunt focus:**

- Bursts of `git.clone` activity.
- Previously unseen token / source-IP / ASN combinations.
- Unusual user agents using valid PATs.
- Repository access far above the identity's historical baseline.
- Broad private-repository cloning in a compressed time window.
- Cloud or SaaS authentication using credentials exposed in recently accessed repositories.

**Reading:**

- Wiz — investigation into GitHub PAT compromise  
  https://www.wiz.io/blog/investigating-github-pat-compromise

---

### 7. Commvault CVE-2026-13737 / CVE-2026-13738 / CVE-2026-13739

**Status:** Newly disclosed; exploitation not established in this research window

Commvault's August disclosures include two critical **CommServe command-execution authorisation bypasses** and an unauthenticated SSRF issue in a legacy Command Center endpoint.

Backup infrastructure warrants disproportionate attention because compromise of the recovery plane dramatically changes ransomware impact.

**Hunt focus:**

- Unexpected CommServe command execution.
- Administrative activity outside normal operator patterns.
- Unusual or destructive backup-job changes.
- New outbound requests originating from Command Center.
- Backup configuration deletion or modification without a valid change trail.

**Reading:**

- Commvault — August security / AI security discussion  
  https://www.commvault.com/blogs/how-commvault-leverages-frontier-ai-to-strengthen-software

---

### 8. Windows AD CS CVE-2026-62818

**Status:** Newly disclosed critical RCE; exploitation not confirmed in this research window

CVE-2026-62818 is a use-after-free vulnerability in Active Directory Certificate Services. A low-privileged authenticated remote attacker can send a crafted network request to an affected AD CS service.

Microsoft assessed exploitation as less likely at disclosure, but an enterprise CA is an identity trust anchor, so even a low-confidence exploitation hypothesis deserves attention where affected AD CS infrastructure exists.

**Hunt focus:**

- Unusual connections to CA servers from low-prevalence clients.
- Unexpected CA-side process execution.
- Process ancestry inconsistent with normal AD CS behaviour.
- Certificate issuance or template changes following anomalous network activity.
- New certificate, template, or CA administrative actions by unusual identities.

**Reading:**

- NVD — CVE-2026-62818  
  https://nvd.nist.gov/vuln/detail/CVE-2026-62818

---

### 9. Cisco ASA / FTD CVE-2026-20349

**Status:** Active exploitation

Cisco confirmed exploitation of a flaw affecting Remote Access SSL VPN functionality. An unauthenticated crafted HTTP request can force an ASA / FTD appliance to reload, resulting in denial of service.

This is less interesting for compromise hunting than the higher-ranked candidates, but it remains useful for infrastructure-focused hunting and correlation.

**Hunt focus:**

- Abnormal HTTP requests targeting internet-facing VPN interfaces.
- Appliance reloads or failovers correlated to external requests.
- Large-scale VPN-session collapse.
- Repeated source IPs or infrastructure associated with reload events.
- Coordinated activity across multiple perimeter devices.

**Reading:**

- Cisco security advisory  
  https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-vpn-dos-dzv4mQFF

---

### 10. JWR real-time phishing framework

**Status:** Newly disclosed tooling / campaign

Cisco Talos documented **JWR**, a previously undocumented phishing framework capable of live operator-controlled interaction with victims instead of relying solely on static credential harvesting.

The client maintains an **AES-CTR-encrypted WebSocket**, allowing operators to dynamically change pages while stealing credentials, identity data, and one-time codes.

**Hunt focus:**

- Newly registered or low-reputation lure domains.
- Persistent WebSocket connections from browsers to low-prevalence destinations.
- Brand/domain mismatch in browsing or proxy telemetry.
- Authentication events immediately following suspicious browsing sessions.
- MFA or OTP use associated with anomalous source infrastructure.
- Users moving from suspicious browser activity into new session/token creation.

**Reading:**

- Cisco Talos — *Dissecting the JWR phishing framework*  
  https://blog.talosintelligence.com/dissecting-the-jwr-phishing-framework/

---

## Prioritisation

### Immediate

1. **Lazarus / Operation Dream Job / CVE-2026-68820**
2. **VMware vCenter CVE-2026-59310**
3. **Gunra ransomware**
4. **Metabase CVE-2026-72898**

### Next wave / estate-dependent

5. **City-Forum — Salesforce + ServiceNow**
6. **GitHub PAT compromise**
7. **Commvault vulnerability cluster**

### Specific exposure / intelligence watch

8. **Windows AD CS CVE-2026-62818**
9. **Cisco ASA / FTD CVE-2026-20349**
10. **JWR phishing framework**

---

## Why the shortlist wins

### Lazarus

The best overall proactive-hunting candidate because it provides independent opportunities across:

- process execution;
- image/module loads;
- DLL side-loading;
- privilege escalation;
- cloud/network activity;
- endpoint-security interference;
- persistence and rootkit behaviour.

The behaviours also generalise beyond the published hashes and domains.

### VMware vCenter

The best **exposure-led** hunt. A vulnerable and exploited vCenter represents a control-plane compromise over virtual infrastructure, and reported reverse-SSH persistence provides a concrete post-exploitation hypothesis.

If there is no VMware in the target estate, remove this immediately and promote Metabase, City-Forum, or GitHub PAT abuse according to exposure.

### Gunra

The best **multi-stage ransomware** hunt. Its value lies in the sequence before encryption:

`perimeter access → credentials → SMB / Impacket → VDI / lateral movement → collection / exfiltration → defence or recovery impairment → encryption`

These behaviours can uncover ransomware activity beyond Gunra itself.

---

## Research conclusions

Five candidates in this set have confirmed attack activity associated with them during or around the research window:

- Lazarus / CVE-2026-68820
- VMware vCenter CVE-2026-59310
- Gunra ransomware
- Metabase CVE-2026-72898
- Cisco ASA / FTD CVE-2026-20349

Commvault and AD CS are primarily **exposure-led hunts** at this stage rather than confirmed intrusion campaigns.

City-Forum and GitHub PAT abuse are especially valuable conceptually because both challenge a common SOC assumption: that malicious activity should produce an obviously malicious authentication or exploit event. In both cases, the attacker can perform damaging actions through permissions or credentials the systems themselves regard as valid.

For conversion into a full hypothesis-led hunting package, **Lazarus / Operation Dream Job is the first-choice candidate** because the public research provides sufficient technical depth to build hunts across endpoint, process, file, identity, network, and cloud telemetry rather than reducing the exercise to IOC matching.
