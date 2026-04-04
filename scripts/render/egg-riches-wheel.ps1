param(
  [string]$HtmlPath = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
if (-not $HtmlPath) {
  $HtmlPath = Join-Path $repoRoot "design\prototypes\html\egg-riches-wheel-prototype.html"
}

$resolvedHtml = (Resolve-Path $HtmlPath).Path
$outputDir = Join-Path $repoRoot "artifacts\egg-riches-wheel"

$browserCandidates = @(
  "C:\Program Files\Google\Chrome\Application\chrome.exe",
  "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
  "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

$browserPath = $browserCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $browserPath) {
  throw "No Chrome/Edge browser found for headless capture."
}

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$fileUrl = "file:///" + ($resolvedHtml -replace "\\", "/")
$staticOutput = Join-Path $outputDir "static.png"
$autoplayOutput = Join-Path $outputDir "autoplay.png"

function Invoke-Capture {
  param(
    [string]$OutputPath,
    [string]$Url,
    [int]$VirtualTimeBudget = 0
  )

  $args = @(
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--run-all-compositor-stages-before-draw",
    "--window-size=430,900",
    "--default-background-color=ffffff",
    "--screenshot=$OutputPath"
  )

  if ($VirtualTimeBudget -gt 0) {
    $args += "--virtual-time-budget=$VirtualTimeBudget"
  }

  $args += $Url
  & $browserPath @args

  Start-Sleep -Milliseconds 300
  if (-not (Test-Path $OutputPath)) {
    throw "Capture failed for $OutputPath"
  }
}

Invoke-Capture -OutputPath $staticOutput -Url $fileUrl
Invoke-Capture -OutputPath $autoplayOutput -Url ($fileUrl + "?autoplay=1&target=7&loops=5") -VirtualTimeBudget 12000

Write-Output "BROWSER=$browserPath"
Write-Output "STATIC=$staticOutput"
Write-Output "AUTOPLAY=$autoplayOutput"
