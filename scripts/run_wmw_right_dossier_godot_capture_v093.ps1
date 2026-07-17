param(
    [string]$GodotPath = ''
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$defaultGodot = Join-Path $repoRoot 'tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64_console.exe'
$captureScript = 'res://tests/capture_world_map_wmw_right_dossier_runtime_v093.gd'
$outDir = Join-Path $repoRoot 'docs\screenshots\2026-06-24-world-map-benchmark-landing'

function Resolve-GodotPath {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        $resolved = (Resolve-Path -LiteralPath $RequestedPath).Path
        if ($resolved -notlike '*4.6.2-stable*') {
            throw "WMW UI capture is pinned to Godot 4.6.2-stable, got: $resolved"
        }
        return $resolved
    }
    if (Test-Path -LiteralPath $defaultGodot) {
        return (Resolve-Path -LiteralPath $defaultGodot).Path
    }
    throw 'Pinned Godot 4.6.2-stable executable not found.'
}

$godot = Resolve-GodotPath -RequestedPath $GodotPath
Write-Host ("Using Godot executable: {0}" -f $godot)
Write-Host 'Running WMW v0.9.3 right-dossier candidate A3 capture (windowed opengl3)...'
& $godot --path $projectPath --resolution 1920x1080 --windowed --audio-driver Dummy --rendering-driver opengl3 -s $captureScript
if ($LASTEXITCODE -ne 0) {
    throw 'WMW v0.9.3 right-dossier candidate A3 Godot capture failed.'
}

$expected = @(
    '608-world-map-wmw-v0-9-3-right-dossier-candidate-a3-godot-runtime.png',
    '609-world-map-wmw-v0-9-3-right-dossier-candidate-a3-godot-runtime-qa.png'
)
foreach ($name in $expected) {
    $path = Join-Path $outDir $name
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Expected screenshot missing: $path"
    }
    if ((Get-Item -LiteralPath $path).Length -lt 10000) {
        throw "Screenshot is suspiciously small: $path"
    }
}

Write-Host 'WMW v0.9.3 right-dossier candidate A3 Godot capture passed.'
