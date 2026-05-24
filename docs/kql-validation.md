# KQL validation — local smoke test

A small .NET console tool that parses every `.kql` file in the repo
and reports any grammar / parse errors. Used as a pre-commit / pre-PR
sanity check so a broken file cannot land silently.

## What it checks

- **Syntax / grammar only.** Each `.kql` file is parsed by the
  `Microsoft.Azure.Kusto.Language` library (the same parser used by
  the Sentinel / Azure Data Explorer editor). If the file is not
  well-formed Kusto, it fails.
- The contract header (`// name:`, `// purpose:`, …) is just KQL
  line comments — the parser accepts them transparently.

## What it does NOT check

This harness is intentionally **schema-blind**. It does not, and
cannot, validate any of the following:

- **Table existence.** Every reference to `SigninLogs`, `AuditLogs`,
  `OfficeActivity`, `DeviceProcessEvents`, etc. is accepted without
  question — there is no live workspace attached.
- **Column existence.** Every reference to a column on those tables
  is accepted without question.
- **Type correctness.** Joins, summarises, projects, and case
  expressions are not type-checked against any schema.
- **Unbound `let` variables.** Every query in this repo opens with a
  `let`-block of analyst-supplied placeholders (`UserIdentityCheck`,
  `AlertTime`, `ActorToCheck`, …). The harness ignores the fact that
  these are empty strings or future-dated defaults.
- **Runtime semantics.** A query that parses successfully here may
  still produce zero rows or runtime errors against a real workspace.
  That is a different category of test and lives outside this repo.

If you need true semantic validation you would have to point the
parser at a `GlobalState` populated with the tenant's schema. That is
deliberately out of scope — it would couple this repo to a specific
tenant and would not work as an offline / CI check.

## How to run it

```bash
pwsh ./scripts/test-kql.ps1
```

or, directly with `dotnet`:

```bash
dotnet run --project tests/kql-smoke -- /path/to/repo/root
```

If no path is supplied, the tool walks upward from its own binary
looking for `repo-contract.md` to locate the repo root, so it works
from any working directory inside the tree.

## Reading the output

```
KQL smoke test — root: /home/user/KQL
Files: 21 (scratchpad/ excluded)
------------------------------------------------------------------------
PASS  01-sign-in/deep-dive.kql
PASS  01-sign-in/narrative-gen.kql
...
FAIL  05-endpoint/process/quick-dive.kql
      line 169, col 30: Expected: )
      line 169, col 30: The incomplete fragment is unexpected.
------------------------------------------------------------------------
Total: 21   Pass: 20   Fail: 1
```

- One `PASS` or `FAIL` line per file.
- On `FAIL`, every error diagnostic is indented under the file with
  its line, column, and message.
- Exit code `0` = all pass. Exit code `1` = at least one fail. Exit
  code `2` = harness misconfiguration (missing repo root, no `.kql`
  files found, etc.).

## What's excluded

The harness skips:

- `scratchpad/` — exempt from the family contract by design, may
  contain rough / in-progress queries.
- `bin/`, `obj/`, `.git/`, `node_modules/` — never source.

## Where it lives

- `tests/kql-smoke/` — the .NET console tool.
- `scripts/test-kql.ps1` — PowerShell wrapper.
- `.github/workflows/kql-smoke.yml` — optional CI runner.

## Updating the parser version

The parser library is `Microsoft.Azure.Kusto.Language`, pinned in
`tests/kql-smoke/KqlSmoke.csproj`. Bump the `<PackageReference>`
version and re-run the harness to refresh.
