# DDNS detection candidates

This module preserves and normalises the legacy DDNS detection-engineering
logic under the active v2 tree. These are **detection candidates**, not a claim
that each file is deployment-ready.

## Files

- `ddns-bulletproof-infra.kql` — successful endpoint connections to TI-maintained bulletproof-hosting CIDR ranges.
- `ddns-subdomain.kql` — successful endpoint connections to subdomains of known dynamic-DNS providers, with process/path context and a simple severity score.
- `ddns-url-click.kql` — user clicks through to DDNS subdomains, enriched with message context.
- `non-browser-to-ddns.kql` — successful non-browser endpoint egress to DDNS subdomains with LOLBin/user-writable provenance scoring.

## Dependencies

- **Required:** `DeviceNetworkEvents` for the endpoint detections; `UrlClickEvents` and `EmailEvents` for the click detection.
- **Preferred enrichment/source:** tenant-managed `DDNS_Domains` and `BPH_Ranges` watchlists refreshed from approved TI sources.
- **Avoid as a production hard dependency:** the live `externaldata()` DDNS CSV fallback. It is retained from the legacy source for portability, but a cached watchlist is more deterministic and reviewable.

## Time behaviour

The endpoint and click detections default to a 1-hour lookback. The click rule
joins up to 7 days of email context. Tune schedule/lookback together so overlap
and ingestion delay are intentional rather than accidental.

## Output and decision use

Outputs identify the affected device/user, DDNS host/domain or remote IP,
initiating process/path, connection or click evidence, and lightweight severity
context. A match should drive investigation or alert enrichment; DDNS use alone
is not proof of compromise.

## Known inherited gaps

- `ddns-bulletproof-infra.kql` contains placeholder fallback CIDRs; it must use a current, reviewed range feed before deployment.
- the provider-domain candidates use a public CSV fallback and intentionally exclude the large `afraid.org` tier to reduce false positives.
- `non-browser-to-ddns.kql` retains a duplicated `ddns_all` materialisation block from the legacy source. That duplication is preserved in this structural migration and should be removed during the queued query-quality/tuning work, not silently changed here.
- none of these migrated candidates currently ships analytic-rule YAML or fixture-backed tuning evidence.

## Validation

All runnable files now use `.kql` and carry the v2 metadata header. The repository
smoke test validates grammar only; workspace schema, watchlist availability,
false-positive rate, and runtime cost still require live validation before a
candidate is promoted to production.
