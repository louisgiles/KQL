# Playbooks

Multi-step investigation paths for specific incident classes. Where a family
in `01-sign-in/` to `06-email/` answers "what happened on this table", a
playbook answers "what do I need to decide on this incident type, in order".

Each query carries the header block from `../repo-contract.md`, keeps analyst
inputs in a top `let` block and uses a bounded time window.

| Playbook | Shape | Purpose |
| --- | --- | --- |
| [`device-code-auth/`](device-code-auth/) | Four small, ordered queries | Sign-in deep dive, user precedent, tenant prevalence and a 24-hour audit sweep. Stop at the first step that supports a decision. |
| [`device-code-scope/`](device-code-scope/) | Three larger modules | A one-row rapid decision, post-authentication scope and exact-IP campaign scope for a confirmed or suspected device-code compromise. |

Both cover device-code authentication from different angles: `device-code-auth`
is the fast funnel, `device-code-scope` is the blast-radius work once the
funnel says it is real.

## Run principle

Steps are numbered in run order, but every step runs on its own. Stop at the
first output that supports containment, closure or a named follow-on question.

## Validation status

Both playbooks target Sentinel Log Analytics (`TimeGenerated`). They pass the
repository parser, but neither has a recorded run against a live workspace
yet. Treat them as candidates until each has been run against a known-benign,
an ambiguous and a known-suspicious case.
