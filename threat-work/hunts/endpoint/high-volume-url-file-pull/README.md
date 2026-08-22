# High-volume URL file-pull endpoint hunt

## Hypothesis

A device repeatedly connecting to a target file-hosting or web service is more
concerning when endpoint evidence shows a file came from that service,
especially when the same file was then executed.

This is a hypothesis-led hunt. Volume alone is not a malicious verdict.

## Starting entities and variables

Set `TargetUrlToken` to one bare registrable-domain token without a scheme.
The query does not run a meaningful hunt while this value is empty.

Optional tuning:

- `HuntEnd`: fixed upper boundary for a repeatable run.
- `Lookback`: 30 days by default.
- `ProximityWindow`: maximum gap between a target connection and nearby file
  creation.
- `AdwareUrlExclusions`: known benign or adware URL tokens to remove.
- `AdwareProcExclusions`: known PUP or adware process names to remove.
- `Browsers`: process names excluded from the non-browser agency signal.
- `W_*`: explicit scoring weights.

## Dependencies

- **Required:** `DeviceNetworkEvents`, `DeviceFileEvents`, and
  `DeviceProcessEvents`.
- **Optional enrichment:** none.
- **Avoid as a hard dependency:** browser history, proxy-only attribution, or
  URL reputation. These can support triage but cannot replace endpoint origin
  and execution evidence.

If any required Defender table is unavailable, the query cannot provide a
complete score. An empty result is not proof that the target was unused.

## Time behaviour

The query uses one fixed `HuntEnd` and a bounded `Lookback`. Every table
uses `[HuntEnd - Lookback, HuntEnd)`. Shorten the window for rapid triage or
extend it only within available retention.

## Signal and noise model

Signals are additive:

- network volume to the target;
- a nearby file creation on the same device;
- file origin or referrer matching the target;
- a non-browser process initiating target connections;
- execution of a file matched to the target by SHA-256, falling back to exact
  folder and file name only when a hash is missing.

File-origin and execution evidence force the result into the high band.
Browser chatter, sanctioned package repositories, software deployment tooling,
adware, and PUP traffic are expected benign-noise sources.

## Output and decision use

The query returns one row per device with:

- connection volume and initiators;
- origin file count, paths, hashes, URLs, and first/last timestamps;
- proximity count and closest observed time gap;
- non-browser initiators;
- executed file paths, hashes, count, and first/last timestamps;
- score and triage band.

Review high-band devices first. Validate the target service, file hash, signer,
prevalence, process ancestry, user intent, and business owner before deciding.

## Done criteria

Close the hunt for a device when the target, downloaded files, execution, user,
and owner are confirmed as authorised and consistent.

Escalate when origin or execution evidence is unauthorised, the file is
malicious or unknown, non-browser agency is unexplained, or the owner and user
intent cannot be resolved.

## Coverage limits

- URL matching uses KQL token matching against a bare domain token. Validate the
  observed `OriginUrls` before treating the match as exact-host attribution.
- File-origin fields can be sparse.
- Path and file-name matching is used only when either execution or origin hash
  is missing. It is weaker than a SHA-256 match.
- Endpoint telemetry cannot prove actions that occurred only on the remote
  service.
- The score prioritises review. It is not a calibrated probability or detection
  severity.

## Validation

The logic is ported from preserved KQL PR #13 head
`dd59661489f68d29079c71237eac36d16347ad43`. The new module adds v2 metadata,
a fixed run boundary, decisive evidence fields, and a safer hash-first
execution join.

Run `pwsh ./scripts/test-kql.ps1` and validate known-benign, ambiguous, and
known-suspicious examples in the target workspace before operational use.
