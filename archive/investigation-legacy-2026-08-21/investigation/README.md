# Investigation

The active home for reusable queries used during a live security incident.
Navigation should begin with the analyst's objective and starting entity, not
with a data table or arbitrary family number.

## Include

- rapid actor, device, IP, session, process, message, and resource pivots;
- compact timelines and cross-domain evidence correlation;
- incident playbooks and queries whose outputs drive containment or closure.

## Exclude

- population-wide threat hunts (`../threat-work/hunts/`);
- source research (`../threat-work/research/`);
- deployable detection logic (`../threat-work/detections/`);
- Babbler or agentic one-shot pipeline stages (the separate
  [`louisgiles/oneshots`](https://github.com/louisgiles/oneshots) repository).

Any query-bearing module must follow the
[`repository contract`](../repo-contract.md), including a local README,
declared inputs and tables, a bounded time window, decision-oriented output,
and explicit done criteria.

This is a scaffold only. The queued investigation-structure task will define
the objective-led modules and migrate reviewed legacy content; nothing was
silently copied here.
