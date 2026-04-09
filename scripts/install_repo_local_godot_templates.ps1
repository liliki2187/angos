param(
    [string]$Version = '4.6.2.stable'
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$sourceRoot = Join-Path $repoRoot 'tools\godot\4.6.2-stable\export_templates\templates'
$targetRoot = Join-Path $env:APPDATA ("Godot\export_templates\{0}" -f $Version)

if (-not (Test-Path $sourceRoot)) {
    Write-Error ('Repo-local export templates not found: {0}' -f $sourceRoot)
    exit 1
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
Copy-Item -Path (Join-Path $sourceRoot '*') -Destination $targetRoot -Recurse -Force

Write-Host ('Installed Godot export templates {0} to {1}' -f $Version, $targetRoot)
