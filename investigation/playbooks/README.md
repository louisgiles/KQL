# Playbooks

Ordered investigation sequences that compose small, independently runnable
queries into a decision funnel. Each step follows `../../repo-contract.md`:
declared header, parameters in a top `let` block, bounded time windows, and
decision-oriented output.

A playbook differs from a rapid-decision module. A rapid-decision module
(for example [`../identity/device-code/`](../identity/device-code/)) computes
one determination row inside a single large query. A playbook keeps each
question in its own small query so the analyst can stop as soon as the
evidence supports a decision, and so any step can be run alone.

## Active playbooks

| Playbook | Purpose |
| --- | --- |
| [`device-code-auth/`](device-code-auth/) | Four-step triage of device-code authentication: sign-in deep dive, user precedent, tenant prevalence, and a 24-hour audit-log sweep. |

## Run principle

Steps are numbered in run order, but every step is independently usable.
Stop at the first step whose output supports containment, closure, or a
specific named follow-on question. Escalate into the relevant deep module
rather than widening a playbook step.
