# Threat hunts

Each hunt states the behaviour being tested, the population and window, the
expected benign noise, telemetry limits and the result that warrants an
investigation.

| Hunt | Surface | What it looks for |
| --- | --- | --- |
| [`endpoint/cloudflare-tunnel/`](endpoint/cloudflare-tunnel/) | Sentinel Log Analytics | Cloudflare Tunnel (`cloudflared`) deployment and execution, with preserved triage notes. |
| [`endpoint/high-volume-url-file-pull/`](endpoint/high-volume-url-file-pull/) | Defender Advanced Hunting | Scored high-volume pulls from a target service, joined to file origin and execution. |
| [`identity/babbler-novelty/`](identity/babbler-novelty/) | Sentinel Log Analytics | Tenant-wide per-actor sign-in novelty using the Babbler Good-Turing engine. |

A hunt that keeps finding real things is a detection candidate. Promotion into
`../detections/` is a separate, reviewed change.
