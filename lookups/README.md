# Lookups

Single-question queries for a live incident. Each one takes one entity, asks
one thing and returns raw rows. Reach for these when a family deep-dive is
more than the question needs, or to check one detail before running one.

All lookups target Sentinel Log Analytics (`TimeGenerated`) and carry the
header block from `../repo-contract.md`.

| Query | Starting entity | Question |
| --- | --- | --- |
| [`user-signin-timeline.kql`](user-signin-timeline.kql) | UPN | What does this user's recent sign-in activity look like, in order? |
| [`user-signin-history.kql`](user-signin-history.kql) | UPN | Has this user normally used this IP, location, app, client and device? |
| [`failed-signins-by-source.kql`](failed-signins-by-source.kql) | UPN | Where are the failed sign-ins coming from, and why are they failing? |
| [`device-code-legacy-auth.kql`](device-code-legacy-auth.kql) | UPN | Did the account use device code, ROPC or a legacy mail protocol? |
| [`entra-user-changes.kql`](entra-user-changes.kql) | UPN | What directory changes did the user make, or have made to them? |
| [`office-activity-by-user.kql`](office-activity-by-user.kql) | UPN | What did the user do across Exchange, SharePoint and OneDrive? |
| [`mail-trace.kql`](mail-trace.kql) | Email address | What mail was sent to or from the address, and where did it land? |
| [`url-clicks-by-user.kql`](url-clicks-by-user.kql) | UPN | Which links did the user click, and were any clicked through? |
| [`process-timeline.kql`](process-timeline.kql) | Device name | What ran on the device, and who ran it? |
| [`process-lineage.kql`](process-lineage.kql) | Device name, PID, time | What spawned the process, and what did it spawn? |
| [`hash-file-origin.kql`](hash-file-origin.kql) | File hash | Where has the hash appeared, and where did it come from? |
| [`device-connections.kql`](device-connections.kql) | Device name | Which destinations did the device connect to? |
| [`remote-logons-to-device.kql`](remote-logons-to-device.kql) | Device name | Who remotely authenticated to the device, and from where? |

Lookups are deliberately plain: no scoring, no verdict. The verdict comes from
the analyst or from the matching family's deep-dive and narrative generator.
