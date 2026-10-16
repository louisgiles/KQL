# Babbler novelty hunt

Tenant-wide version of the Babbler sign-in scorer. It scores each user's
recent interactive sign-in flows against that user's own preceding baseline
using Good-Turing missing-mass estimation, then lists the most novel flows per
actor.

- **Query:** [`hunt-research-rc2.kql`](hunt-research-rc2.kql) (tenant research 0.1.0-rc2)
- **Surface:** Sentinel Log Analytics, `SigninLogs`
- **Window:** 1-day score window against a preceding per-actor baseline, both
  anchored on one fixed run time
- **Scoring source:** frozen to the `b32` one-shot section in
  [`../../../../01-sign-in/babbler-lineage/`](../../../../01-sign-in/babbler-lineage/)

Babbler measures how unusual a sign-in is for that actor. It does not estimate
compromise probability or rank one actor's risk against another's. A quiet
period still produces a most-novel row for every actor, so treat output as
leads to investigate with the `01-sign-in` family, not findings.

For a single-user, incident-time version, use
[`../../../../01-sign-in/Babbl33r.kql`](../../../../01-sign-in/Babbl33r.kql).
