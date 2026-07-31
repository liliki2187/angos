param(
    [string]$GodotPath = ''
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$defaultGodot = Join-Path $repoRoot 'tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64_console.exe'
$captureScript = 'res://tests/capture_godot_visual_feedback_smoke.gd'
$outDir = Join-Path $repoRoot 'docs\screenshots\2026-07-29-godot-visual-feedback-smoke'

function Resolve-GodotPath {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        return (Resolve-Path -LiteralPath $RequestedPath).Path
    }
    if (Test-Path -LiteralPath $defaultGodot) {
        return (Resolve-Path -LiteralPath $defaultGodot).Path
    }
    throw 'Pinned Godot 4.6.2 console executable not found. Pass -GodotPath or install tools/godot/4.6.2-stable/.'
}

$godot = Resolve-GodotPath -RequestedPath $GodotPath
Write-Host ("Using Godot executable: {0}" -f $godot)
Write-Host 'Capturing WeeklyRunGame visual feedback states (windowed opengl3)...'

& $godot --path $projectPath --resolution 1920x1080 --windowed --audio-driver Dummy --rendering-driver opengl3 -s $captureScript
if ($LASTEXITCODE -ne 0) {
    throw 'Godot visual feedback smoke failed.'
}

$expectedPngs = @(
    '01-world-map-region-ready.png',
    '02-region-task-m330-selected.png',
    '03-dispatch-m330-no-staff.png',
    '04-dispatch-m330-staff-selected.png'
)
foreach ($name in $expectedPngs) {
    $path = Join-Path $outDir $name
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Expected screenshot missing: $path"
    }
    $item = Get-Item -LiteralPath $path
    if ($item.Length -lt 10000) {
        throw "Screenshot is suspiciously small: $path"
    }
}

$manifest = Join-Path $outDir 'capture-manifest.json'
if (-not (Test-Path -LiteralPath $manifest)) {
    throw "Expected manifest missing: $manifest"
}

Write-Host 'Godot visual feedback smoke passed.'
Write-Host ("Screenshots: {0}" -f $outDir)
