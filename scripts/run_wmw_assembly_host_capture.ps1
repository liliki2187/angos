param(
    [string]$GodotPath = '',
    [string]$PythonPath = ''
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$defaultGodot = Join-Path $repoRoot 'tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64_console.exe'
$defaultPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$captureScript = 'res://tests/capture_world_map_wmw_assembly_host.gd'
$evidenceScript = Join-Path $repoRoot 'scripts\ui-contracts\wmw\wmw_assembly_host_evidence.py'
$outDir = Join-Path $repoRoot 'docs\screenshots\2026-06-24-world-map-benchmark-landing'

function Resolve-GodotPath {
    param([string]$RequestedPath)
    $candidate = $defaultGodot
    if ($RequestedPath) {
        $candidate = $RequestedPath
    }
    $resolved = (Resolve-Path -LiteralPath $candidate).Path
    if ($resolved -notlike '*4.6.2-stable*') {
        throw "WMW UI capture is pinned to Godot 4.6.2-stable, got: $resolved"
    }
    return $resolved
}

function Resolve-PythonPath {
    param([string]$RequestedPath)
    if ($RequestedPath) {
        return (Resolve-Path -LiteralPath $RequestedPath).Path
    }
    if (Test-Path -LiteralPath $defaultPython) {
        return (Resolve-Path -LiteralPath $defaultPython).Path
    }
    throw 'Bundled Python with Pillow was not found. Pass -PythonPath explicitly.'
}

$godot = Resolve-GodotPath -RequestedPath $GodotPath
$python = Resolve-PythonPath -RequestedPath $PythonPath
Write-Host ("Using Godot executable: {0}" -f $godot)
Write-Host 'Capturing the independent WMW assembly host from WeeklyRunGame (windowed opengl3)...'
& $godot --path $projectPath --resolution 1920x1080 --windowed --audio-driver Dummy --rendering-driver opengl3 -s $captureScript
if ($LASTEXITCODE -ne 0) {
    throw 'WMW assembly-host Godot capture failed.'
}

$expectedPngs = @(
    '645-world-map-wmw-assembly-host-collapsed.png',
    '646-world-map-wmw-assembly-host-expanded.png',
    '647-world-map-wmw-assembly-host-locked.png',
    '648-world-map-wmw-assembly-host-geometry-qa.png'
)
foreach ($name in $expectedPngs) {
    $path = Join-Path $outDir $name
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Expected screenshot missing: $path"
    }
    if ((Get-Item -LiteralPath $path).Length -lt 10000) {
        throw "Screenshot is suspiciously small: $path"
    }
}

& $python $evidenceScript
if ($LASTEXITCODE -ne 0) {
    throw 'WMW assembly-host evidence generation failed.'
}

foreach ($name in @(
    '644-world-map-wmw-assembly-host-dual-reference-board.png',
    '649-world-map-wmw-assembly-host-state-cycle.gif',
    '650-world-map-wmw-assembly-host-integration-manifest.json'
)) {
    if (-not (Test-Path -LiteralPath (Join-Path $outDir $name))) {
        throw "Expected evidence missing: $name"
    }
}

Write-Host 'WMW assembly-host capture and evidence passed.'
