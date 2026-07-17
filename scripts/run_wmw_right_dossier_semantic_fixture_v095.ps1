param(
    [string]$GodotPath = ''
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$defaultGodot = Join-Path $repoRoot 'tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64_console.exe'
$exportScript = 'res://tests/export_world_map_wmw_right_dossier_runtime_fixture_v095.gd'
$fixturePath = Join-Path $repoRoot 'gd_project\Assets\ui\angus_packaging\world_map\wmw_v095_right_dossier_candidate_a5\right_dossier_candidate_a5_runtime_fixture.json'

function Resolve-GodotPath {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        $resolved = (Resolve-Path -LiteralPath $RequestedPath).Path
        if ($resolved -notlike '*4.6.2-stable*') {
            throw "WMW semantic export is pinned to Godot 4.6.2-stable, got: $resolved"
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
Write-Host 'Exporting WMW v0.9.5 right-dossier production runtime fixture (logic-only headless)...'
& $godot --headless --path $projectPath -s $exportScript
if ($LASTEXITCODE -ne 0) {
    throw 'WMW v0.9.5 right-dossier semantic fixture export failed.'
}
if (-not (Test-Path -LiteralPath $fixturePath)) {
    throw "Expected runtime fixture missing: $fixturePath"
}

$fixture = Get-Content -LiteralPath $fixturePath -Encoding utf8 -Raw | ConvertFrom-Json
if ($fixture.provenance -ne 'production_runtime_export' -or -not $fixture.generated_from_production_data) {
    throw 'Runtime fixture provenance check failed.'
}
Write-Host 'WMW v0.9.5 right-dossier production runtime fixture passed.'
