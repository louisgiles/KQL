import type { Pack } from './types';
const win = 'Windows Security Events via AMA, event 4688 with command-line auditing and ParentProcessName populated. Run within one customer workspace at a time.';
export const packs: Record<string, Pack> = {
 rmm: { id:'rmm', title:'Remote management spawning a download or shell', tables:['SecurityEvent'], techniques:['T1219','T1059.001'],
 hypothesis:'An unapproved remote management agent launches a shell or downloader to establish a second access channel.', prerequisites:win,
 query:`// Proposed hunt; not executed against your tenant.
SecurityEvent
| where TimeGenerated > ago(7d)
| where EventID == 4688
| where ParentProcessName contains "RMM.Agent" or ParentProcessName contains "ScreenConnect"
    or ParentProcessName contains "FaronicsDeployAgent" or ParentProcessName contains "MeshAgent"
| where NewProcessName has_any ("powershell.exe", "pwsh.exe", "cmd.exe", "msiexec.exe", "curl.exe")
| project TimeGenerated, Computer, Account, ParentProcessName, NewProcessName, CommandLine
| order by TimeGenerated desc`,
 steps:['Check the agent and management server against approved RMM inventory.','Pivot ±30 minutes on the host for MSI installation, new services and secondary agents.','Inspect download destinations and validate the session with the service desk.'],
 expected:'RMM processes launching shells or installers. Unapproved servers and a second newly installed agent strengthen the hypothesis.',falsePositives:['Approved support and software deployment','Planned RMM migrations and incident response'],limitations:'Names can be changed. A match alone is not compromise; missing command lines reduce visibility.' },
 identity: { id:'identity',title:'Successful sign-ins from a new ASN and country',tables:['SigninLogs'],techniques:['T1078','T1557'],
 hypothesis:'A compromised Entra account authenticates from a network and country absent from its recent history.',prerequisites:'31 days of Entra SigninLogs. Scores only accounts with ≥25 prior successful sign-ins across ≥7 days. Does not cover Google authentication.',
 query:`// Anomaly lead; not proof of AitM or token theft.
let baseline = materialize(SigninLogs
    | where TimeGenerated between (ago(31d) .. ago(1d))
    | where ResultType == "0"
    | extend Country=tostring(LocationDetails.countryOrRegion), ASN=tostring(AutonomousSystemNumber)
    | summarize Flows=count(), ActiveDays=dcount(startofday(TimeGenerated)), Countries=make_set(Country,256), ASNs=make_set(ASN,1024) by UserPrincipalName
    | where Flows >= 25 and ActiveDays >= 7);
SigninLogs
| where TimeGenerated > ago(1d)
| where ResultType == "0"
| extend Country=tostring(LocationDetails.countryOrRegion), ASN=tostring(AutonomousSystemNumber)
| where isnotempty(Country) and isnotempty(ASN) and ASN != "0"
| join kind=inner baseline on UserPrincipalName
| where not(set_has_element(Countries,Country)) and not(set_has_element(ASNs,ASN))
| project TimeGenerated, UserPrincipalName, IPAddress, Country, ASN, AppDisplayName, DeviceDetail, AuthenticationDetails, ConditionalAccessStatus, Flows, ActiveDays
| order by TimeGenerated desc`,
 steps:['Confirm network ownership, travel, VPN usage and device context.','Review authentication details, session continuity and recent identity alerts.','Pivot into audit and resource-access logs for new credentials, consent or mailbox activity.'],expected:'Established accounts using both a new ASN and country. Corroborate against device, user and downstream activity.',falsePositives:['Travel and corporate VPN changes','Mobile carriers and incomplete baselines'],limitations:'Misses familiar residential networks and stolen sessions without new interactive sign-ins. Geolocation is imperfect.' },
 oauth:{id:'oauth',title:'Consent and application credential changes',tables:['AuditLogs'],techniques:['T1098.001','T1528'],hypothesis:'A new OAuth grant or application credential provides unexpected access to mail, files or a service identity.',prerequisites:'Entra audit logs connected to Sentinel. Inspect nested target properties to determine the actual permissions and objects changed.',
 query:`AuditLogs
| where TimeGenerated > ago(7d)
| where OperationName has_any ("Consent to application", "Add delegated permission grant", "Add app role assignment", "Add service principal credentials", "Update application")
| extend ActorUPN=tostring(InitiatedBy.user.userPrincipalName), ActorApp=tostring(InitiatedBy.app.displayName), ActorIP=tostring(InitiatedBy.user.ipAddress)
| mv-expand Target=TargetResources
| project TimeGenerated, OperationName, Result, ActorUPN, ActorApp, ActorIP, TargetName=tostring(Target.displayName), TargetId=tostring(Target.id), ModifiedProperties=Target.modifiedProperties, CorrelationId
| order by TimeGenerated desc`,
 steps:['Resolve the target application and inspect permissions or credentials.','Verify changes with the application owner and change record.','Review service-principal sign-ins and resource access where collected.'],expected:'Unexpected grants or application changes; sensitive scopes and subsequent access increase concern.',falsePositives:['Application onboarding','Credential rotation and approved integrations'],limitations:'Attacker-owned tenants may leave no consent change in yours. This does not detect every use of Microsoft Graph.'},
 ransomware:{id:'ransomware',title:'Recovery inhibition and log clearing',tables:['SecurityEvent'],techniques:['T1490','T1070.001'],hypothesis:'An attacker disables recovery before impact or clears logs to conceal activity.',prerequisites:win,
 query:`SecurityEvent
| where TimeGenerated > ago(7d)
| where EventID == 4688
| extend Cmd=tolower(CommandLine)
| where (NewProcessName endswith "vssadmin.exe" and Cmd has_all ("delete","shadows"))
    or (NewProcessName endswith "wbadmin.exe" and Cmd has_all ("delete","catalog"))
    or (NewProcessName endswith "bcdedit.exe" and (Cmd has_all ("recoveryenabled","no") or Cmd has "ignoreallfailures"))
    or (NewProcessName endswith "wevtutil.exe" and Cmd has_any ("cl","clear-log"))
| project TimeGenerated, Computer, Account, ParentProcessName, NewProcessName, CommandLine
| order by TimeGenerated desc`,
 steps:['Check maintenance windows and backup-team approval.','Pivot to preceding remote logons and parent processes.','Check other hosts for the same account or commands; escalate corroborated activity.'],expected:'Recovery or log-clearing commands. Unexpected privileged accounts and multi-host spread strengthen concern.',falsePositives:['Backup maintenance','Imaging and recovery testing'],limitations:'A behavioural precursor only. Direct API activity and ransomware without these utilities are missed.'},
 web:{id:'web',title:'Encoded PeopleSoft paths and unusual requests',tables:['CommonSecurityLog'],techniques:['T1190','T1505.003'],hypothesis:'An attacker reaches a vulnerable PeopleSoft endpoint using an encoded path.',prerequisites:'CEF proxy or WAF events with RequestURL populated. Scope to the PeopleSoft application and check field mappings.',
 query:`CommonSecurityLog
| where TimeGenerated > ago(14d)
| where isnotempty(RequestURL)
| extend DecodedURL=url_decode(RequestURL)
| where DecodedURL contains "/PSEMHUB/" or RequestURL contains "/%50SEMHUB/"
| project TimeGenerated, DeviceVendor, DeviceProduct, DeviceName, SourceIP, DestinationIP, RequestMethod, RequestURL, DecodedURL, DeviceAction
| order by TimeGenerated desc`,
 steps:['Confirm product exposure and patched version from inventory.','Inspect raw and decoded paths, methods and available responses.','Correlate with application logs, new files and outbound traffic.'],expected:'Requests to PSEMHUB including encoded variants. A request alone does not establish successful exploitation.',falsePositives:['Vulnerability scanning','Legitimate PeopleSoft administration'],limitations:'Specific to PeopleSoft. CEF mappings vary; file creation needs host telemetry.'},
 edge:{id:'edge',title:'New outbound destinations from an exposed appliance',tables:['CommonSecurityLog'],techniques:['T1190','T1090'],hypothesis:'An exploited device starts communicating with external infrastructure absent from its baseline.',prerequisites:'CEF flows covering appliance egress and at least 15 days of history. Replace the example IP with affected asset IPs.',
 query:`// REPLACE with your appliance IPs. This example is a documentation address.
let AssetIPs=dynamic(["192.0.2.10"]);
let previous=materialize(CommonSecurityLog
    | where TimeGenerated between (ago(15d) .. ago(1d))
    | where SourceIP in (AssetIPs)
    | where isnotempty(DestinationIP)
    | distinct SourceIP, DestinationIP, DestinationPort);
CommonSecurityLog
| where TimeGenerated > ago(1d)
| where SourceIP in (AssetIPs)
| where isnotempty(DestinationIP)
| join kind=leftanti previous on SourceIP, DestinationIP, DestinationPort
| summarize FirstSeen=min(TimeGenerated), LastSeen=max(TimeGenerated), Events=count(), Actions=make_set(DeviceAction,20) by SourceIP, DestinationIP, DestinationPort, ApplicationProtocol
| order by Events desc`,
 steps:['Replace the asset list and verify baseline coverage.','Separate denied attempts from allowed sessions and identify destination ownership.','Correlate with crashes, admin logins and vendor forensic guidance.'],expected:'New peers or ports from scoped infrastructure. Unexpected allowed egress plus appliance artefacts warrants escalation.',falsePositives:['Vendor updates and CDN rotation','Monitoring and disaster recovery'],limitations:'Generic post-exploitation lead, not a CVE signature. NAT and missing baseline data can obscure results.'},
 linux:{id:'linux',title:'Persistence and download leads in Linux syslog',tables:['Syslog'],techniques:['T1053.003','T1059.004'],hypothesis:'A Linux host shows unexpected persistence or downloads in collected logs.',prerequisites:'Relevant auth, cron, service or audit messages in Syslog. Standard syslog is not a complete process record.',
 query:`Syslog
| where TimeGenerated > ago(7d)
| where SyslogMessage has_any ("crontab","authorized_keys","systemctl","curl","wget")
| project TimeGenerated, Computer, Facility, SeverityLevel, ProcessName, SyslogMessage
| order by TimeGenerated desc`,
 steps:['Scope to affected hosts and verify collected facilities.','Review changed crontabs, SSH keys and systemd units on the host.','Check commands and destinations against management activity.'],expected:'Leads around persistence and downloads; verify with host artefacts.',falsePositives:['Configuration management','Package installation and maintenance'],limitations:'Broad triage only. Many executions are absent from Syslog; no results cannot exclude compromise.'},
 supplychain:{id:'supplychain',title:'Developer tooling spawning suspicious commands',tables:['SecurityEvent'],techniques:['T1195.002','T1059.001'],hypothesis:'A compromised dependency or repository triggers unexpected shell activity from a developer runtime.',prerequisites:win+' Scope to developer and build hosts.',
 query:`SecurityEvent
| where TimeGenerated > ago(7d)
| where EventID == 4688
| where ParentProcessName has_any ("node.exe","python.exe","git.exe","Code.exe")
| where NewProcessName has_any ("powershell.exe","pwsh.exe","cmd.exe","curl.exe","certutil.exe")
| where CommandLine has_any ("http","encodedcommand","downloadstring","frombase64string","invoke-webrequest")
| project TimeGenerated, Computer, Account, ParentProcessName, NewProcessName, CommandLine
| order by TimeGenerated desc`,
 steps:['Identify the repository, dependency and preceding install command.','Compare with known build behaviour and inspect the destination safely.','Review the affected identity and CI audit logs for credential misuse.'],expected:'Shell or download activity originating in development processes; establish whether it matches normal setup.',falsePositives:['Build scripts and package post-install hooks','Developer setup and approved extensions'],limitations:'Windows starting point; Linux runners, macOS and CI control-plane events need separate telemetry.'},
 malware:{id:'malware',title:'Suspicious script interpreter chains',tables:['SecurityEvent'],techniques:['T1059.001','T1218.005'],hypothesis:'A document, browser or script host launches an interpreter with download or obfuscation arguments.',prerequisites:win,
 query:`SecurityEvent
| where TimeGenerated > ago(7d)
| where EventID == 4688
| where ParentProcessName has_any ("winword.exe","excel.exe","outlook.exe","mshta.exe","wscript.exe","cscript.exe","chrome.exe","msedge.exe")
| where NewProcessName has_any ("powershell.exe","pwsh.exe","cmd.exe","mshta.exe","rundll32.exe")
| where CommandLine has_any ("http","encodedcommand","frombase64string","downloadstring","javascript")
| project TimeGenerated, Computer, Account, ParentProcessName, NewProcessName, CommandLine
| order by TimeGenerated desc`,
 steps:['Establish the initial document, URL or user action.','Inspect arguments and correlate downloads and persistence.','Pivot on host, user and destination; compare with approved integrations.'],expected:'Unusual interpreter launches with download or obfuscation arguments. Corroborate before treating as malicious.',falsePositives:['Business macros and integrations','Application updaters and administrative scripts'],limitations:'Misses renamed tools, in-memory execution and activity lacking command-line auditing.'}
};
export const tableNames=['SecurityEvent','SigninLogs','AuditLogs','CommonSecurityLog','Syslog'];
export const statuses=['Queued','Investigating','Complete','Dismissed'];
export function inferCategory(text:string){
 const t=text.toLowerCase();
 if(/ransom|extortion/.test(t))return {category:'Ransomware',packs:['ransomware','rmm']};
 if(/peoplesoft|psemhub/.test(t))return {category:'Exploitation',packs:['web','edge']};
 if(/netscaler|citrix|firewall|appliance|zero.day|cve-/.test(t))return {category:'Exploitation',packs:['edge']};
 if(/rmm|screenconnect|remote management/.test(t))return {category:'Remote access',packs:['rmm']};
 if(/supply.chain|npm|pypi|github|package|repository/.test(t))return {category:'Supply chain',packs:['supplychain']};
 if(/google.*phish|phish.*google/.test(t))return {category:'Identity',packs:[]};
 if(/oauth|graph|consent|cloud|microsoft 365|onedrive/.test(t))return {category:'Cloud',packs:['oauth','identity']};
 if(/phish|identity|token|aitm|vishing|credential/.test(t))return {category:'Identity',packs:['identity','malware']};
 if(/linux|unix/.test(t))return {category:'Linux',packs:['linux']};
 if(/malware|backdoor|loader|stealer|trojan|campaign|apt/.test(t))return {category:'Malware',packs:['malware']};
 return {category:'Threat landscape',packs:[]};
}
