# KQL validation: preflight and live release gate

Validation has two separate layers. Offline preflight catches grammar and known
static hazards. The release gate requires a successful live execution of the
exact final content in its declared query surface.

## What offline preflight checks

- **Syntax and grammar.** Each `.kql` file is parsed by the
  `Microsoft.Azure.Kusto.Language` library (the same parser used by
  the Sentinel / Azure Data Explorer editor). If the file is not
  well-formed Kusto, it fails.
- **Known runtime-sensitive literals.** Unsupported
  `format_datetime()` tokens fail the static gate.
- **Executable contract headers.** Every changed active query must declare all
  required header fields and a supported execution surface.
- **Known execution-surface mismatches.** Sentinel investigation KQL that uses
  Defender Advanced Hunting `Timestamp` instead of `TimeGenerated` fails.
- **Known output-schema hazards.** A mismatched `SortOrder:int` union seed
  fails because the operational queries require one `long` sort column.
- **Invalid multi-key top clauses.** `top` accepts one ordering expression.
  Use `order by` for all ordering keys, then `take` the required row count.
- **Unsafe conditional distinct counts.** Investigation queries must not use
  `dcountif()`, which can fail when all or no rows satisfy its predicate.
  Deduplicate the stable key first, then use `countif()`.
- **Sibling alias dependencies.** A calculated column is not available to
  another expression in the same `extend`. Dependent calculations must use a
  later `extend` operator.
- The contract header (`// name:`, `// purpose:`, …) is just KQL
  line comments; the parser accepts them transparently.

## What offline preflight does not check

These checks remain **schema-blind** outside the explicitly guarded patterns.
They do not validate any of the following:

- **Table existence.** Every reference to `SigninLogs`, `AuditLogs`,
  `OfficeActivity`, `DeviceProcessEvents`, etc. is accepted without
  question because there is no live workspace attached.
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
deliberately out of scope because it would couple this repo to a specific
tenant and would not work as an offline / CI check.

## Offline preflight

```bash
pwsh ./scripts/test-kql.ps1
python3 ./scripts/lint-kql-runtime-literals.py .
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
KQL smoke test: root: /home/user/KQL
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

## Exact-content live gate

Offline success never establishes operational readiness. For every new or
changed active KQL file:

1. Freeze the final text and calculate its Git blob SHA.
2. Run the complete file in the declared execution surface.
3. For investigation KQL, the required surface is the Microsoft Sentinel Log
   Analytics blade.
4. Run the unchanged source once to bind execution to `source_sha256`.
5. Run a representative incident case with only declared analyst inputs
   populated.
6. Confirm both executions complete without a semantic or runtime error and
   that the expected output columns are present.
7. Add a sanitized `passed` receipt to
   `validation/sentinel-live.json` for that exact Git blob SHA.
8. Run:

```bash
python3 ./scripts/check-sentinel-live-validation.py . --files path/to/query.kql
```

The checker fails when a receipt is missing, pending, failed, malformed, or
bound to different content. Any byte change creates a different Git blob SHA
and invalidates the prior receipt.

Pull requests and main-branch pushes evaluate changed active KQL. Manual
workflow runs evaluate every active KQL file. A red gate is a release block,
not an advisory warning.

Branch protection must require both `Parse and lint every .kql` and
`KQL / live validation`. Changes to the workflow, gate scripts, or validation
records require code-owner review.

Where Azure OIDC and Log Analytics query diagnostics are available, the
stronger target is to match the SHA256 of `LAQueryLogs.QueryText` to the CI
artifact and require `ResponseCode == 200`. Until that integration exists,
the manifest requires a named analyst attestation and sanitized evidence.

## Current operational status

The manifest is authoritative. As of 2026-08-22, every active file is pending
or failed. None may be represented as incident-ready until its exact SHA has a
passed record.

## What's excluded

The harness skips:

- `scratchpad/`: exempt from the family contract by design, may
  contain rough / in-progress queries.
- `bin/`, `obj/`, `.git/`, `node_modules/`: never source.

## Where it lives

- `tests/kql-smoke/`: the .NET console tool.
- `scripts/test-kql.ps1`: PowerShell wrapper.
- `.github/workflows/kql-smoke.yml`: CI runner.

## Updating the parser version

The parser library is `Microsoft.Azure.Kusto.Language`, pinned in
`tests/kql-smoke/KqlSmoke.csproj`. Bump the `<PackageReference>`
version and re-run the harness to refresh.
