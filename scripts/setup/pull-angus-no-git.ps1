$ErrorActionPreference = "Stop"
$repo = "daydreamerguan/angus"
$branch = "main"
$baseDir = Join-Path $env:USERPROFILE "source\repos"
$repoDir = Join-Path $baseDir "angus"
New-Item -ItemType Directory -Force -Path $baseDir | Out-Null

# 0) Token first (needed for private repo zip)
if (-not $env:GITHUB_TOKEN) {
  throw "GITHUB_TOKEN is not available. Please set GITHUB_TOKEN in your environment before running this script."
}
$headers = @{
  Authorization = "Bearer $($env:GITHUB_TOKEN)"
  Accept = "application/vnd.github+json"
  "X-GitHub-Api-Version" = "2022-11-28"
}

# 1) Download source ZIP (use API zipball for private repo)
$zipUrl = "https://api.github.com/repos/$repo/zipball/$branch"
$zipPath = Join-Path $baseDir "angus-main.zip"
Write-Output "Downloading repository source..."
Invoke-WebRequest -Uri $zipUrl -Headers $headers -OutFile $zipPath -UseBasicParsing

# 2) Extract (zipball creates daydreamerguan-angus-<sha>)
if (Test-Path $repoDir) { Remove-Item $repoDir -Recurse -Force }
Expand-Archive -Path $zipPath -DestinationPath $baseDir -Force
$got = Get-ChildItem -Path $baseDir -Directory | Where-Object { $_.Name -like "daydreamerguan-angus-*" } | Select-Object -First 1
if ($got) { Rename-Item $got.FullName $repoDir } else { New-Item -ItemType Directory -Force -Path $repoDir | Out-Null }
Write-Output "Source extracted to: $repoDir"

# 3) Get latest workflow run + artifact
$owner = "daydreamerguan"
$repoName = "angus"
$workflowFile = "godot-build.yml"
$artifactName = "Build-Windows"

$runsUrl = "https://api.github.com/repos/$owner/$repoName/actions/workflows/$workflowFile/runs?branch=$branch&per_page=1"
Write-Output "Querying latest workflow run..."
$runsResp = Invoke-RestMethod -Method Get -Uri $runsUrl -Headers $headers
$run = $runsResp.workflow_runs | Select-Object -First 1
if (-not $run) { throw "No workflow run found for $workflowFile on $branch" }
$runId = $run.id

$runApiUrl = "https://api.github.com/repos/$owner/$repoName/actions/runs/$runId"
do {
  $runInfo = Invoke-RestMethod -Method Get -Uri $runApiUrl -Headers $headers
  if ($runInfo.status -eq "completed") { break }
  Write-Output "Waiting for run $runId ... status=$($runInfo.status)"
  Start-Sleep -Seconds 8
} while ($true)

if ($runInfo.conclusion -ne "success") {
  Write-Output "Run not success: $($runInfo.conclusion). URL: $($runInfo.html_url)"
  exit 1
}

$artifactsUrl = "https://api.github.com/repos/$owner/$repoName/actions/runs/$runId/artifacts"
$artResp = Invoke-RestMethod -Method Get -Uri $artifactsUrl -Headers $headers
$artifact = $artResp.artifacts | Where-Object { $_.name -eq $artifactName } | Select-Object -First 1
if (-not $artifact) {
  Write-Output "Available: $(($artResp.artifacts | ForEach-Object { $_.name }) -join ', ')"
  throw "Artifact $artifactName not found"
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$outDir = Join-Path $repoDir "artifacts\Build-Windows-$runId-$timestamp"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$zipPath = Join-Path $outDir "Build-Windows.zip"
Write-Output "Downloading artifact to $zipPath"
Invoke-WebRequest -Method Get -Uri $artifact.archive_download_url -Headers $headers -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $outDir -Force

Write-Output ""
Write-Output "=== DONE ==="
Write-Output "Repo (source): $repoDir"
Write-Output "Run URL: $($runInfo.html_url)"
Write-Output "Artifact dir: $outDir"
$exes = Get-ChildItem -Path $outDir -Recurse -Filter "*.exe" -ErrorAction SilentlyContinue
$exes | ForEach-Object { Write-Output "  EXE: $($_.FullName)" }
