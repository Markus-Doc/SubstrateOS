<#
.SYNOPSIS
    SubstrateOS installer for Windows PowerShell (ADR-026).

.DESCRIPTION
    Installs the `labctl` + `subos` console scripts so `subos claude` works from
    any directory in a fresh shell. Idempotent: re-running upgrades in place.
    pipx-first (isolated, user-scope, on PATH via `pipx ensurepath`); falls back
    to a managed virtualenv + shim when pipx is unavailable. Pins no model and
    adds no API billing — it just installs the launcher.

.PARAMETER FullAutoDefault
    Opt in to the full-auto posture by default (user-scope env var). Never bakes
    privilege into the public Base (ADR-019).

.EXAMPLE
    .\install.ps1
.EXAMPLE
    .\install.ps1 -FullAutoDefault
#>
[CmdletBinding()]
param(
    [switch]$FullAutoDefault
)

$ErrorActionPreference = "Stop"

function Write-Info { param([string]$Message) Write-Host "==> $Message" -ForegroundColor Cyan }
function Write-Warn { param([string]$Message) Write-Host "[!] $Message" -ForegroundColor Yellow }
function Write-Err  { param([string]$Message) Write-Host "[x] $Message" -ForegroundColor Red }

# Resolve the repo root (this script lives at the repo root) and the package dir.
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PkgDir = Join-Path $RepoRoot "scripts"
if (-not (Test-Path -LiteralPath $PkgDir)) {
    Write-Err "package directory not found at $PkgDir — run this from a SubstrateOS clone"
    exit 1
}

# 1. Python >= 3.11 (prefer the `py` launcher).
$python = $null
$pyArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    $python = "py"; $pyArgs = @("-3")
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $python = "python"
} else {
    Write-Err "Python 3 not found. Install Python >= 3.11 from https://www.python.org/downloads/ (tick 'Add to PATH')."
    exit 1
}
& $python @pyArgs -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
if ($LASTEXITCODE -ne 0) {
    $ver = (& $python @pyArgs -c "import sys; print('%d.%d.%d' % sys.version_info[:3])")
    Write-Err "Python >= 3.11 required, found $ver. Please upgrade Python."
    exit 1
}
$ver = (& $python @pyArgs -c "import sys; print('%d.%d.%d' % sys.version_info[:3])")
Write-Info "Python OK ($ver)"

# 2. Install via pipx (preferred) or a managed venv fallback.
# $pipxCmd is the executable; $pipxBase are the leading args (empty for a bare
# `pipx` on PATH, or `-3 -m pipx` when invoking pipx through the Python launcher).
$pipxCmd = $null
$pipxBase = @()
if (Get-Command pipx -ErrorAction SilentlyContinue) {
    $pipxCmd = "pipx"
} else {
    & $python @pyArgs -m pipx --version *> $null
    if ($LASTEXITCODE -eq 0) { $pipxCmd = $python; $pipxBase = $pyArgs + @("-m", "pipx") }
}

if (-not $pipxCmd) {
    Write-Info "pipx not found — installing it (user scope)"
    & $python @pyArgs -m pip install --user pipx
    if ($LASTEXITCODE -eq 0) {
        & $python @pyArgs -m pipx ensurepath *> $null
        $pipxCmd = $python; $pipxBase = $pyArgs + @("-m", "pipx")
    } else {
        Write-Warn "could not install pipx; falling back to a managed virtualenv"
    }
}

$binHint = Join-Path $env:USERPROFILE ".local\bin"
if ($pipxCmd) {
    Write-Info "Installing SubstrateOS with pipx (idempotent)"
    & $pipxCmd @pipxBase install --force $PkgDir
    & $pipxCmd @pipxBase ensurepath *> $null
} else {
    $venv = Join-Path $env:LOCALAPPDATA "SubstrateOS\venv"
    Write-Info "Installing SubstrateOS into a managed virtualenv ($venv)"
    & $python @pyArgs -m venv $venv
    & (Join-Path $venv "Scripts\python.exe") -m pip install --upgrade pip *> $null
    & (Join-Path $venv "Scripts\python.exe") -m pip install $PkgDir
    $binHint = Join-Path $venv "Scripts"
    Write-Warn "Add this directory to PATH to use subos/labctl: $binHint"
}

# 3. Optional opt-in to the full-auto posture (user-scope; never the public Base).
if ($FullAutoDefault) {
    [Environment]::SetEnvironmentVariable("SUBSTRATEOS_FULL_AUTO", "1", "User")
    $env:SUBSTRATEOS_FULL_AUTO = "1"
    Write-Warn "Full-auto posture enabled for new shells (SUBSTRATEOS_FULL_AUTO=1, user environment)."
}

# 4. Verify.
Write-Info "Verifying the installation"
$subos = Get-Command subos -ErrorAction SilentlyContinue
if ($subos) {
    & subos --version
    & labctl doctor
    Write-Info "Done. Try:  subos claude --dry-run"
} else {
    Write-Warn "subos is installed but not on PATH in THIS terminal."
    Write-Warn "Open a NEW PowerShell window (PATH refreshes there), then run:  subos --version"
    Write-Warn "If scripts are blocked, first run:  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
    Write-Warn "Bin directory: $binHint"
}
