param(
  [string]$Branch = "main",
  [switch]$DryRun,
  [switch]$SkipOrigin,
  [switch]$SkipDaydreamer
)

$ErrorActionPreference = "Stop"

function Run-Git([string]$cmd) {
  Write-Host ">> git $cmd" -ForegroundColor Cyan
  & git $cmd.Split(" ")
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed: git $cmd"
  }
}

Write-Host "=== Dual Remote Sync ===" -ForegroundColor Yellow

# 1) Ensure we're in a git repo
& git rev-parse --is-inside-work-tree | Out-Null
if ($LASTEXITCODE -ne 0) {
  throw "Current directory is not a git repository."
}

# 2) Ensure remotes exist
$remotes = (& git remote).Trim().Split([Environment]::NewLine) | Where-Object { $_ -ne "" }
if (-not ($remotes -contains "origin")) {
  throw "Remote 'origin' not found."
}
if (-not ($remotes -contains "daydreamer")) {
  throw "Remote 'daydreamer' not found. Please run: git remote add daydreamer https://github.com/daydreamerguan/angus.git"
}

# 3) Show status context (non-blocking)
Write-Host "`n[Status]" -ForegroundColor Yellow
& git status --short

# 4) Ensure local branch exists and checkout
Write-Host "`n[Checkout $Branch]" -ForegroundColor Yellow
& git checkout $Branch
if ($LASTEXITCODE -ne 0) { throw "Failed to checkout branch: $Branch" }

# 5) Push sequence
if ($DryRun) {
  Write-Host "`n[DryRun] planned push targets:" -ForegroundColor Yellow
  if (-not $SkipOrigin) { Run-Git "push --dry-run origin ${Branch}:${Branch}" }
  if (-not $SkipDaydreamer) { Run-Git "push --dry-run daydreamer ${Branch}:${Branch}" }
  Write-Host "`nDry run completed." -ForegroundColor Green
  exit 0
}

if (-not $SkipOrigin) {
  Write-Host "`n[Push origin]" -ForegroundColor Yellow
  Run-Git "push origin ${Branch}:${Branch}"
}

if (-not $SkipDaydreamer) {
  Write-Host "`n[Push daydreamer]" -ForegroundColor Yellow
  Run-Git "push daydreamer ${Branch}:${Branch}"
}

Write-Host "`nSync completed successfully: origin + daydreamer" -ForegroundColor Green

