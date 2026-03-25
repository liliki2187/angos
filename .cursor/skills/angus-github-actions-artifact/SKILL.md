---
name: angus-github-actions-artifact
description: Checks GitHub Actions for this Angus repository after push, waits for completion, and downloads build artifacts on success. Use when the user asks to verify CI status, inspect a workflow run, or fetch artifacts after pushing code in this project.
---

# Angus GitHub Actions Artifact Flow

Use this skill only for this repository: `https://github.com/daydreamerguan/angus`.

## What this skill does

1. Confirms current repo is `daydreamerguan/angus`.
2. Finds the latest run of workflow `Godot Build` for current branch.
3. If latest run is still running/queued, waits until it completes.
4. If latest run failed, reports latest run failure and stops.
5. If latest run succeeded, downloads artifact `Build-Windows`.
6. Saves to a timestamped output directory and zip filename.
7. Keeps extracted filenames unchanged (do not rename executables).
8. Reports run URL, conclusion, and local artifact path.

## Preconditions

- Token has at least repository read access and Actions read access.
- Token is available in either:
  - `GITHUB_TOKEN` environment variable, or
  - project-local `.env.local` file.
- User already pushed changes, or explicitly asked to run checks after push.

## Commands

Run these commands in sequence.

```powershell
# 1) Guard: only run in target repo
$remoteUrl = git remote get-url origin
if ($remoteUrl -notmatch 'github\.com[:/]+daydreamerguan/angus(\.git)?$') {
  throw "This skill is only for daydreamerguan/angus"
}

# 2) Resolve token (env first, then .env.local)
if (-not $env:GITHUB_TOKEN) {
  $envFile = ".env.local"
  if (Test-Path $envFile) {
    $line = Get-Content $envFile | Where-Object { $_ -match '^GITHUB_TOKEN=' } | Select-Object -First 1
    if ($line) {
      $env:GITHUB_TOKEN = $line.Substring("GITHUB_TOKEN=".Length).Trim()
    }
  }
}
if (-not $env:GITHUB_TOKEN) {
  throw "GITHUB_TOKEN not found in env or .env.local"
}
$owner = "daydreamerguan"
$repo = "angus"
$workflowFile = "godot-build.yml"
$headers = @{
  Authorization = "Bearer $($env:GITHUB_TOKEN)"
  Accept = "application/vnd.github+json"
  "X-GitHub-Api-Version" = "2022-11-28"
}

# 3) Find latest run for current branch
$branch = git rev-parse --abbrev-ref HEAD
$runsUrl = "https://api.github.com/repos/$owner/$repo/actions/workflows/$workflowFile/runs?branch=$branch&per_page=1"
$runsResp = Invoke-RestMethod -Method Get -Uri $runsUrl -Headers $headers
$runs = $runsResp.workflow_runs
$run = $runs | Select-Object -First 1
if (-not $run) { throw "No workflow run found for branch $branch" }
$runId = $run.id

# 4) Poll until completion
while ($true) {
  $runUrl = "https://api.github.com/repos/$owner/$repo/actions/runs/$runId"
  $runInfo = Invoke-RestMethod -Method Get -Uri $runUrl -Headers $headers
  if ($runInfo.status -eq "completed") { break }
  Start-Sleep -Seconds 8
}

$conclusion = $runInfo.conclusion
$htmlUrl = $runInfo.html_url
Write-Output "Run URL: $htmlUrl"
Write-Output "Status: $($runInfo.status)"
Write-Output "Conclusion: $conclusion"

# 5) Download artifact only on success
if ($conclusion -ne "success") {
  throw "Latest run failed or not successful. status=$($runInfo.status), conclusion=$conclusion, url=$htmlUrl"
}

# 6) Find artifact
$artifactsUrl = "https://api.github.com/repos/$owner/$repo/actions/runs/$runId/artifacts"
$artResp = Invoke-RestMethod -Method Get -Uri $artifactsUrl -Headers $headers
$artifact = $artResp.artifacts | Where-Object { $_.name -eq "Build-Windows" } | Select-Object -First 1
if (-not $artifact) { throw "Artifact Build-Windows not found in run $runId" }

# 7) Download and extract artifact (timestamped directory, keep extracted names)
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$outDir = "artifacts/Build-Windows-$runId-$timestamp"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$zipPath = Join-Path $outDir "Build-Windows-$timestamp.zip"
Invoke-WebRequest -Method Get -Uri $artifact.archive_download_url -Headers $headers -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $outDir -Force

# 8) Show downloaded files
Write-Output "Artifact path: $outDir"
Get-ChildItem -Path $outDir -Recurse -File | Select-Object FullName
```

## Notes

- If artifact name changes, list available artifact names with:

```powershell
$artifactsUrl = "https://api.github.com/repos/$owner/$repo/actions/runs/$runId/artifacts"
(Invoke-RestMethod -Method Get -Uri $artifactsUrl -Headers $headers).artifacts | Select-Object name,size_in_bytes,expired
```
