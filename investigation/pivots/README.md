# cross-family pivot patterns

Reference for the common multi-family pivots an analyst will run. Each
section below names the pivot path and the join key(s) that stitch one
family to the next. No queries yet — this file is a skeleton.

## Email → SignIn

> TODO. The click-to-compromise path: a delivered phish is clicked by a
> recipient and that recipient's identity footprint then goes sideways.

- Starting entities: `NetworkMessageId`, recipient UPN, click timestamp
- Pivot key(s): recipient UPN, click time → `UserPrincipalName` and a
  narrow `TimeGenerated` window in `SigninLogs`
- First-family query:
- Second-family query:
- Join shape:
- Expected output:

## SignIn → AuthChanges

> TODO. Tamper-after-compromise path: an anomalous sign-in is followed
> (or preceded) by a security-info or MFA change on the same account.

- Starting entities: UPN, sign-in `CorrelationId`, timestamp
- Pivot key(s): UPN → `AuditLogs.TargetResources[*].userPrincipalName`
  within a narrow window around the sign-in
- First-family query:
- Second-family query:
- Join shape:
- Expected output:

## AuthChanges → AzureActivity

> TODO. Escalation path: an auth-change (password reset, MFA
> registration, privileged role add) is followed by control-plane
> activity in Azure from the same principal.

- Starting entities: actor UPN or service principal object id, change
  timestamp
- Pivot key(s): actor identity → `AzureActivity.Caller` /
  `Claims_d.upn` / object id
- First-family query:
- Second-family query:
- Join shape:
- Expected output:

## Endpoint → Network → SignIn

> TODO. Host-first path: a suspicious endpoint process makes an
> outbound connection, the destination matches a public egress IP, and
> that same egress IP later shows up in `SigninLogs` against the same
> account or a different one.

- Starting entities: device name, process alert timestamp, destination
  IP/URL
- Pivot key(s): `DeviceNetworkEvents.RemoteIP` → `SigninLogs.IPAddress`
  on a forward time window
- First-family query:
- Second-family query:
- Third-family query:
- Join shape:
- Expected output:
