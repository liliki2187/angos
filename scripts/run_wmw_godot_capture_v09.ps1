param(
    [string]$GodotPath = '',
    [switch]$SkipRepro
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$defaultGodot = Join-Path $repoRoot 'tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64_console.exe'
$captureScript = 'res://tests/capture_world_map_wmw_left_card_runtime_v09.gd'
$reproScript = 'res://tests/godot_capture_minimal_repro.gd'
$outDir = Join-Path $repoRoot 'docs\screenshots\2026-06-24-world-map-benchmark-landing'

function Resolve-GodotPath {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        return (Resolve-Path -LiteralPath $RequestedPath).Path
    }
    if (Test-Path -LiteralPath $defaultGodot) {
        return (Resolve-Path -LiteralPath $defaultGodot).Path
    }

    $localConsoles = Get-ChildItem -Path (Join-Path $repoRoot 'tools\godot') -Recurse -File -Filter 'Godot*_console.exe' -ErrorAction SilentlyContinue
    if ($localConsoles) {
        $preferred = $localConsoles | Where-Object { $_.FullName -like '*4.6.2-stable*' } | Select-Object -First 1
        if ($preferred) {
            return $preferred.FullName
        }
        return ($localConsoles | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1).FullName
    }

    foreach ($candidate in @('godot4', 'godot')) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            return $command.Source
        }
    }

    throw 'Godot executable not found. Pass -GodotPath or install tools/godot/4.6.2-stable/.'
}

$godot = Resolve-GodotPath -RequestedPath $GodotPath
Write-Host ("Using Godot executable: {0}" -f $godot)

if (-not $SkipRepro) {
    Write-Host 'Running minimal repro (headless)...'
    & $godot --headless --path $projectPath -s $reproScript
    if ($LASTEXITCODE -ne 0) {
        throw 'Minimal repro failed unexpectedly in headless mode.'
    }

    Write-Host 'Running minimal repro (windowed opengl3)...'
    & $godot --path $projectPath --resolution 640x360 --windowed --audio-driver Dummy --rendering-driver opengl3 -s $reproScript
    if ($LASTEXITCODE -ne 0) {
        throw 'Minimal repro failed in windowed mode.'
    }
}

Write-Host 'Running v0.9.14 B2.8 left-card capture (windowed opengl3)...'
& $godot --path $projectPath --resolution 1920x1080 --windowed --audio-driver Dummy --rendering-driver opengl3 -s $captureScript
if ($LASTEXITCODE -ne 0) {
    throw 'v0.9.14 B2.8 left-card Godot capture failed.'
}

$expected = @(
    '517-world-map-wmw-v0-9-14-left-card-b2-8-godot-single-component.png',
    '518-world-map-wmw-v0-9-14-left-card-b2-8-godot-single-component-qa.png'
)
foreach ($name in $expected) {
    $path = Join-Path $outDir $name
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Expected screenshot missing: $path"
    }
}

Write-Host 'WMW v0.9.14 B2.8 Godot capture passed.'
