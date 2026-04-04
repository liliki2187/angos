param(
  [string]$ImagePath = "",
  [string]$Title = "Eggy Jump Joy Reconstruction",
  [string]$Caption = "Rebuilt from activity_wheel_eggy assets and the replied reference image."
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
if (-not $ImagePath) {
  $ImagePath = Join-Path $repoRoot "artifacts\activity-wheel-eggy\preview.png"
}

$resolvedImage = (Resolve-Path $ImagePath).Path
$sendScript = Join-Path $repoRoot "skills\claude-to-im\scripts\send-feishu-images-post.mjs"

$nodeCandidates = @(
  "C:\Program Files\nodejs\node.exe",
  "C:\Users\guanmx\AppData\Local\Programs\nodejs\node.exe"
)

$nodePath = $nodeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $nodePath) {
  throw "No node.exe found for Feishu send script."
}

& $nodePath $sendScript --title $Title --caption $Caption $resolvedImage

if ($LASTEXITCODE -ne 0) {
  throw "Feishu image post failed."
}
