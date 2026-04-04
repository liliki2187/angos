param(
  [string]$ImagePath = "",
  [string]$Title = "Egg Riches Wheel Prototype",
  [string]$Caption = "Built from the replied reference image. The button uses slot-style running light and glow effects."
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
if (-not $ImagePath) {
  $ImagePath = Join-Path $repoRoot "artifacts\egg-riches-wheel\autoplay.png"
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
