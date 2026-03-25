param(
  [Parameter(Mandatory = $true)]
  [string]$InputSvg,

  [string]$OutputPng = "",

  [int]$Width = 0,

  [int]$Height = 0
)

$ErrorActionPreference = "Stop"

function Get-EdgePath {
  $candidates = @(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
  )

  foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate) {
      return $candidate
    }
  }

  throw "Microsoft Edge not found in common install paths."
}

function Resolve-OutputPath([string]$InputPath, [string]$RequestedOutput) {
  if ([string]::IsNullOrWhiteSpace($RequestedOutput)) {
    return [System.IO.Path]::ChangeExtension($InputPath, ".png")
  }

  if ([System.IO.Path]::IsPathRooted($RequestedOutput)) {
    return $RequestedOutput
  }

  return [System.IO.Path]::GetFullPath((Join-Path -Path (Get-Location) -ChildPath $RequestedOutput))
}

function Get-SvgNumber([string]$SvgText, [string]$AttributeName) {
  $pattern = $AttributeName + '\s*=\s*"([0-9]+(?:\.[0-9]+)?)(?:px)?"'
  $match = [System.Text.RegularExpressions.Regex]::Match($SvgText, $pattern)
  if ($match.Success) {
    return [double]$match.Groups[1].Value
  }

  return $null
}

function Get-CanvasSize([string]$SvgPath, [int]$RequestedWidth, [int]$RequestedHeight) {
  if ($RequestedWidth -gt 0 -and $RequestedHeight -gt 0) {
    return @{
      Width = $RequestedWidth
      Height = $RequestedHeight
    }
  }

  $svgText = Get-Content -LiteralPath $SvgPath -Raw -Encoding UTF8
  $parsedWidth = Get-SvgNumber -SvgText $svgText -AttributeName "width"
  $parsedHeight = Get-SvgNumber -SvgText $svgText -AttributeName "height"

  if ($parsedWidth -and $parsedHeight) {
    return @{
      Width = [int][Math]::Ceiling($parsedWidth)
      Height = [int][Math]::Ceiling($parsedHeight)
    }
  }

  $viewBoxMatch = [System.Text.RegularExpressions.Regex]::Match(
    $svgText,
    'viewBox\s*=\s*"[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)"'
  )

  if ($viewBoxMatch.Success) {
    return @{
      Width = [int][Math]::Ceiling([double]$viewBoxMatch.Groups[1].Value)
      Height = [int][Math]::Ceiling([double]$viewBoxMatch.Groups[2].Value)
    }
  }

  return @{
    Width = 1600
    Height = 900
  }
}

$resolvedInput = (Resolve-Path -LiteralPath $InputSvg).Path
$resolvedOutput = Resolve-OutputPath -InputPath $resolvedInput -RequestedOutput $OutputPng
$outputDir = Split-Path -Parent $resolvedOutput

if (-not (Test-Path -LiteralPath $outputDir)) {
  New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$edgePath = Get-EdgePath
$canvas = Get-CanvasSize -SvgPath $resolvedInput -RequestedWidth $Width -RequestedHeight $Height
$inputUri = ([System.Uri]$resolvedInput).AbsoluteUri
$stdoutPath = [System.IO.Path]::GetTempFileName()
$stderrPath = [System.IO.Path]::GetTempFileName()

if (Test-Path -LiteralPath $resolvedOutput) {
  Remove-Item -LiteralPath $resolvedOutput -Force
}

try {
  $process = Start-Process `
    -FilePath $edgePath `
    -ArgumentList @(
      "--headless",
      "--disable-gpu",
      "--hide-scrollbars",
      "--run-all-compositor-stages-before-draw",
      "--window-size=$($canvas.Width),$($canvas.Height)",
      "--screenshot=$resolvedOutput",
      $inputUri
    ) `
    -Wait `
    -PassThru `
    -NoNewWindow `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath

  if ($process.ExitCode -ne 0 -and -not (Test-Path -LiteralPath $resolvedOutput)) {
    throw "PNG export failed with exit code $($process.ExitCode)."
  }
}
finally {
  Remove-Item -LiteralPath $stdoutPath -Force -ErrorAction SilentlyContinue
  Remove-Item -LiteralPath $stderrPath -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path -LiteralPath $resolvedOutput)) {
  throw "PNG export failed: output file was not created."
}

Write-Output "OK"
Write-Output ("output=" + $resolvedOutput)
Write-Output ("size=" + $canvas.Width + "x" + $canvas.Height)
