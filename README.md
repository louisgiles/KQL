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
(current as of 29/03/2026. Further additions to come.)

### Identity:

- sign-in-abnormality
- failed-auth-pattern
- mfa-bypass
- anomalous-token-replay
- privileged-account-activity
- service-principal-auth-tracker
- sign-in-investigation-narrative-gen
- sign-in-triage-plus-risk-scoring-engine


### Usage:
Each file is a standalone query to be used within your sentinel logs blade. Some queries reference specific tables.
Comments at the top of each file for the pre-requisites and table dependencies.

### Note:
This is a personal reference library, not an open-source project. All work is my own.
Contributions are not accepted but feel free to fork and adapt for your own environment.
Reach out to me on LinkedIn if you make any adjustments or additions, I'd love to hear what other people are engaged in.
https://www.linkedin.com/in/louis-giles/
