param(
    [string]$GodotPath = ''
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$tests = @(
    (Resolve-Path (Join-Path $repoRoot 'tests\godot\weekly_run\test_phase_flow.gd')).Path,
    (Resolve-Path (Join-Path $repoRoot 'tests\godot\weekly_run\test_settlement_result.gd')).Path
)

if (-not $GodotPath) {
    $localGodotRoot = Join-Path $repoRoot 'tools\godot'
    $localConsole = Get-ChildItem -Path $localGodotRoot -Recurse -File -Filter 'Godot*_console.exe' -ErrorAction SilentlyContinue |
        Sort-Object FullName -Descending |
        Select-Object -First 1
    if ($localConsole) {
        $GodotPath = $localConsole.FullName
    }
}

if (-not $GodotPath) {
    foreach ($candidate in @('godot4', 'godot', 'Godot_v4.6.2-stable_win64_console.exe', 'Godot_v4.6.2-stable_win64.exe')) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            $GodotPath = $command.Source
            break
        }
    }
}

if (-not $GodotPath) {
    Write-Error 'Godot executable not found. Pass -GodotPath, or place a repo-local build under tools/godot/, or add godot4/godot to PATH.'
    exit 1
}

Write-Host ('Using Godot executable: {0}' -f $GodotPath)

foreach ($testScript in $tests) {
    Write-Host ('Running {0}' -f $testScript)
    & $GodotPath --headless --path $projectPath -s $testScript
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Write-Host 'Weekly run smoke tests passed.'
