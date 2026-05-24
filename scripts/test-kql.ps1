#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run the KQL smoke-test harness against this repository.

.DESCRIPTION
    Builds and runs the .NET console tool under tests/kql-smoke/ which parses
    every .kql file (except scratchpad/) and reports syntax-level diagnostics.
    The harness is syntax-only — it does NOT validate against a live Sentinel,
    Defender, or Azure schema. See docs/kql-validation.md for details.

.PARAMETER RepoRoot
    Override the repo root. Defaults to the parent of this script directory.

.PARAMETER Configuration
    Build configuration. Defaults to Release.

.EXAMPLE
    pwsh ./scripts/test-kql.ps1
    Run from the repo root.

.EXAMPLE
    pwsh ./scripts/test-kql.ps1 -Configuration Debug
    Run with Debug-built binaries.
#>

[CmdletBinding()]
param(
    [string] $RepoRoot,
    [string] $Configuration = 'Release'
)

$ErrorActionPreference = 'Stop'

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
}

$toolDir = Join-Path $RepoRoot 'tests/kql-smoke'
if (-not (Test-Path $toolDir)) {
    Write-Error "KQL smoke tool not found at $toolDir"
    exit 2
}

Write-Host "Building harness ($Configuration)..." -ForegroundColor Cyan
dotnet build $toolDir --configuration $Configuration --nologo --verbosity quiet
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed."
    exit $LASTEXITCODE
}

Write-Host "Running harness against $RepoRoot..." -ForegroundColor Cyan
dotnet run --project $toolDir --configuration $Configuration --no-build --no-restore -- $RepoRoot
exit $LASTEXITCODE
