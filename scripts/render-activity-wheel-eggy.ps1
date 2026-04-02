param(
  [string]$HtmlPath = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $HtmlPath) {
  $HtmlPath = Join-Path $repoRoot "design\htmls\activity_wheel_eggy\activity-wheel-eggy.html"
}

$resolvedHtml = (Resolve-Path $HtmlPath).Path
$outputDir = Join-Path $repoRoot "artifacts\activity-wheel-eggy"

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
$rawOutput = Join-Path $outputDir "raw.png"
$previewOutput = Join-Path $outputDir "preview.png"

$args = @(
  "--headless=new",
  "--disable-gpu",
  "--hide-scrollbars",
  "--run-all-compositor-stages-before-draw",
  "--window-size=430,900",
  "--default-background-color=ffffff",
  "--screenshot=$rawOutput",
  $fileUrl
)

& $browserPath @args
Start-Sleep -Milliseconds 1000

if (-not (Test-Path $rawOutput)) {
  throw "Capture failed for $rawOutput"
}

Add-Type -AssemblyName System.Drawing
$rawImage = [System.Drawing.Bitmap]::FromFile($rawOutput)
$cropRect = New-Object System.Drawing.Rectangle(47, 0, 375, 840)
$cropped = $rawImage.Clone($cropRect, $rawImage.PixelFormat)
$cropped.Save($previewOutput, [System.Drawing.Imaging.ImageFormat]::Png)
$cropped.Dispose()
$rawImage.Dispose()

Write-Output "BROWSER=$browserPath"
Write-Output "PREVIEW=$previewOutput"
