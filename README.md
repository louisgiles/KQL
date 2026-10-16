## My Personal KQL Library.
- This is a library of KQL queries built for SOC investigation within sentinel.
- These are practical triage ready queries designed for real incident response.
- This library is built from hands-on experience acquired throughout my career as a SOC Analyst.

## Design principles:
These queries are written against the following philosophies:
1. Clarity. Live environments are loud. It's easy to miss the tree for the forest. These queries aim to cut through the noise.
2. Minimalism. These queries are not a substitute for understanding, nor a crutch. Effective analysis is manual. Effective understanding is not automatic.
3. Speed. Queries are tightly scoped. Full-table scans are expensive, not just in time.
4. Humility. Arrogance kills agility. Danger lies outside of awareness. Always assume the answer is outside of understanding.
5. Concision. Queries are intentionally lean and organised by category. Do more with less.

## Structure

Organised into six numbered investigation families plus supporting
top-level folders. Each family is self-contained — its own queries,
its own `notes.md`, its own done criteria.

| Folder | Family |
|---|---|
| `01-sign-in/` | Sign-in triage. Anomalous logins, risky sign-ins, IP / device / location familiarity, MFA posture. Includes `Babbl33r.kql`, a probabilistic sign-in novelty scorer (Good-Turing estimation), and its build history in `babbler-lineage/`. |
| `02-auth-changes/` | Authentication-change triage. Password resets, MFA registrations / removals, security-info changes, role assignments. |
| `03-office-ops/` | Office / M365 operations triage. Mailbox permissions, inbox rules, forwarding, transport rules, delegation. Includes The Curio Cabinet, a rare-operations hunt. |
| `04-azure-activity/` | Azure control-plane triage. Resource creation / deletion, RBAC changes, Key Vault, NSG edits. |
| `05-endpoint/` | Endpoint triage. Three sub-families: `process/`, `file/`, `network/`. |
| `06-email/` | Email triage. Phishing, malicious attachment / URL delivery, post-delivery actions, click exposure. |
| `scratchpad/` | One-off tool queries that do not recur often enough to be a family. Exempt from the family contract. |

Supporting folders:

| Folder | Purpose |
|---|---|
| `playbooks/` | Multi-step paths for a specific incident class. Currently device-code authentication: a four-step triage funnel and a three-part scope module. |
| `lookups/` | Single-question queries (one entity, one question, raw rows) for checking a detail before or alongside a family deep-dive. |
| `threat-work/` | Hunts, research and detection candidates: Cloudflare Tunnel, high-volume URL file pulls, tenant-wide Babbler novelty, DDNS detections. |

Cross-family pivots (Email → SignIn, SignIn → AuthChanges, etc.) are
deliberately out of scope for v1 and parked for a future addition. A
skeleton lives at `cross-family/pivot-patterns.md` but is not part of
the contract.

Every family ships at minimum a `deep-dive.kql`, a `narrative-gen.kql`,
and a `notes.md`. Optional `quick-dive.kql` per family or sub-family.
The endpoint family is the contract exception — three sub-families
each shipping the full contract — see `05-endpoint/notes.md`.

The authoritative rule-set lives in `repo-contract.md`.

### Usage

Each query is standalone — paste into the Sentinel logs blade (or
Defender Advanced Hunting for endpoint / email) and populate the
`let`-block variables at the top. Required and optional tables are
declared in each query's header block and summarised in the family's
`notes.md`.

### Validation

Every `.kql` file is parsed on each pull request by a small harness built
on `Microsoft.Azure.Kusto.Language`, and a lint step rejects
`format_datetime()` patterns that Sentinel refuses at runtime. Parsing
proves syntax, not schema or behaviour; see `docs/kql-validation.md`.

```powershell
pwsh ./scripts/test-kql.ps1
python3 ./scripts/lint-kql-runtime-literals.py .
```

### Note:
This is a personal reference library, not an open-source project. All work is my own.
Contributions are not accepted but feel free to fork and adapt for your own environment.
Reach out to me on LinkedIn if you make any adjustments or additions, I'd love to hear what other people are engaged in.
https://www.linkedin.com/in/louis-giles/
