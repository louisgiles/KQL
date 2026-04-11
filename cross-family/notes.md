# cross-family

Investigations that don't sit cleanly in one family. Pivots that start
in one data domain and end in another — e.g. an email click that leads
to a sign-in anomaly that leads to an endpoint process chain.

## Use case

An analyst has two or more signals from different families that may
relate to the same incident. Cross-family queries stitch those signals
together on shared keys (UPN, IP, device name, timestamp window).

## Starting entities

- Any combination of: UPN, IP, device name, NetworkMessageId,
  CorrelationId, time window.

## Queries in this family

None yet. This folder exists to satisfy the contract's folder layout
and to give future multi-family pivots a home.

## Data dependencies

Per-query. A cross-family query may touch any table listed as
**Required** or **Optional enrichment** in any family `notes.md`.
It must never elevate an **Avoid as hard dependency** table into a
hard filter — the rule applies across families, not just within.

## Done criteria

A cross-family triage is finished when every family involved has been
driven to its own `done_criteria` and a single closure bucket has been
chosen for the incident as a whole.

## Closure language

Same four buckets as the per-family contract. The incident takes the
**highest severity** bucket of any contributing family — a benign
email finding does not downgrade a suspicious sign-in finding.

## Validation — test cases

To be authored alongside the first cross-family query.

## Contract compliance notes

- Folder placeholder only. No queries yet.
- When the first cross-family query is added, it must carry the full
  contract header block and a top-of-file `let` block like any
  single-family query.
