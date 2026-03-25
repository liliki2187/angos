$ErrorActionPreference = "Stop"

# Ensure git is on PATH (common install locations)
$gitPaths = @(
  "C:\Program Files\Git\bin",
  "C:\Program Files (x86)\Git\bin",
  $env:LOCALAPPDATA + "\Programs\Git\bin"
)
foreach ($p in $gitPaths) {
  if (Test-Path (Join-Path $p "git.exe")) {
    $env:Path = $p + ";" + $env:Path
    break
  }
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Error "Git not found. Please install Git for Windows and ensure it is in PATH, then re-run this script."
  exit 1
}

$repoUrl = "https://github.com/daydreamerguan/angus.git"
$owner = "daydreamerguan"
$repo = "angus"
$branch = "main"
$workflowFile = "godot-build.yml"
$artifactName = "Build-Windows"

$baseDir = Join-Path $env:USERPROFILE "source\repos"
$repoDir = Join-Path $baseDir "angus"
New-Item -ItemType Directory -Force -Path $baseDir | Out-Null

function Test-AngusRepo($path) {
  if (-not (Test-Path (Join-Path $path ".git"))) { return $false }
  try {
    $remote = git -C $path remote get-url origin 2>$null
    return ($remote -like "*github.com*daydreamerguan/angus*")
  } catch {
    return $false
  }
}

$currentDir = (Get-Location).Path
if (Test-AngusRepo $currentDir) {
  $repoDir = $currentDir
  Write-Output "Using current directory as angus repo: $repoDir"
} elseif (-not (Test-Path $repoDir)) {
  Write-Output "Cloning $repoUrl into $repoDir"
  git clone $repoUrl $repoDir
} elseif (-not (Test-AngusRepo $repoDir)) {
  throw "Target path exists but is not daydreamerguan/angus: $repoDir"
} else {
  Write-Output "Using existing repo: $repoDir"
}

$skillPath = Join-Path $repoDir ".cursor\skills\angus-github-actions-artifact\SKILL.md"
if (Test-Path $skillPath) {
  Write-Output "Reference skill found: $skillPath"
}

Write-Output "Fetching and pulling latest main..."
git -C $repoDir fetch --all --prune
git -C $repoDir checkout $branch
git -C $repoDir pull --ff-only origin $branch

if (-not $env:GITHUB_TOKEN) {
  throw "GITHUB_TOKEN is not available. Please set GITHUB_TOKEN in your environment before running this script."
}
if (-not $env:GH_TOKEN) {
  $env:GH_TOKEN = $env:GITHUB_TOKEN
}

$headers = @{
  Authorization = "Bearer $($env:GITHUB_TOKEN)"
  Accept = "application/vnd.github+json"
  "X-GitHub-Api-Version" = "2022-11-28"
}

$runsUrl = "https://api.github.com/repos/$owner/$repo/actions/workflows/$workflowFile/runs?branch=$branch&per_page=1"
Write-Output "Querying latest workflow run..."
$runsResp = Invoke-RestMethod -Method Get -Uri $runsUrl -Headers $headers
$run = $runsResp.workflow_runs | Select-Object -First 1
if (-not $run) {
  throw "No workflow run found for workflow $workflowFile on branch $branch"
}
$runId = $run.id
Write-Output "Latest run ID: $runId"

$runApiUrl = "https://api.github.com/repos/$owner/$repo/actions/runs/$runId"
while ($true) {
  $runInfo = Invoke-RestMethod -Method Get -Uri $runApiUrl -Headers $headers
  if ($runInfo.status -eq "completed") { break }
  Write-Output "Waiting for run $runId ... status=$($runInfo.status)"
  Start-Sleep -Seconds 8
}

$conclusion = $runInfo.conclusion
$htmlUrl = $runInfo.html_url
Write-Output "Run URL: $htmlUrl"
Write-Output "Conclusion: $conclusion"

if ($conclusion -ne "success") {
  throw "Latest run is not successful. conclusion=$conclusion, url=$htmlUrl"
}

$artifactsUrl = "https://api.github.com/repos/$owner/$repo/actions/runs/$runId/artifacts"
$artResp = Invoke-RestMethod -Method Get -Uri $artifactsUrl -Headers $headers
$artifact = $artResp.artifacts | Where-Object { $_.name -eq $artifactName } | Select-Object -First 1
if (-not $artifact) {
  Write-Output "Available artifacts:"
  $artResp.artifacts | ForEach-Object { Write-Output "  - $($_.name)" }
  throw "Artifact $artifactName not found in run $runId"
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$outDir = Join-Path $repoDir "artifacts\Build-Windows-$runId-$timestamp"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$zipPath = Join-Path $outDir "Build-Windows-$timestamp.zip"
Write-Output "Downloading artifact to $zipPath"
Invoke-WebRequest -Method Get -Uri $artifact.archive_download_url -Headers $headers -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $outDir -Force

$headCommit = git -C $repoDir rev-parse HEAD
Write-Output ""
Write-Output "=== FINAL SUMMARY ==="
Write-Output "Repo path: $repoDir"
Write-Output "Branch: $branch"
Write-Output "HEAD: $headCommit"
Write-Output "Run URL: $htmlUrl"
Write-Output "Artifact zip: $zipPath"
Write-Output "Artifact dir: $outDir"
Write-Output "Key files:"
Get-ChildItem -Path $outDir -Recurse -File | Where-Object {
  $_.Name -match "Angus(\.console)?\.exe" -or $_.Extension -eq ".zip"
} | ForEach-Object { Write-Output "  $($_.FullName)" }
