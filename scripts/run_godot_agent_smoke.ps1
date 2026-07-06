param(
    [string]$GodotPath = '',
    [string]$PythonPath = '',
    [string[]]$ExtraValidateScript = @(),
    [switch]$SkipGda,
    [switch]$GdaOffline
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$godotAppData = Join-Path $repoRoot 'tmp\godot-agent-smoke-appdata'
$uvCacheDir = Join-Path $repoRoot 'tmp\uv-cache'
$uvToolDir = Join-Path $repoRoot 'tmp\uv-tools'
$uvToolBinDir = Join-Path $repoRoot 'tmp\uv-tool-bin'

function Find-Godot {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        return (Resolve-Path -LiteralPath $RequestedPath).Path
    }

    $localGodotRoot = Join-Path $repoRoot 'tools\godot'
    $localConsoles = Get-ChildItem -Path $localGodotRoot -Recurse -File -Filter 'Godot*_console.exe' -ErrorAction SilentlyContinue
    if ($localConsoles) {
        $projectConfig = Join-Path $repoRoot 'gd_project\project.godot'
        $featureVersion = ''
        if (Test-Path -LiteralPath $projectConfig) {
            $featureLine = Select-String -LiteralPath $projectConfig -Pattern 'config/features=PackedStringArray\("([^"]+)"\)' -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($featureLine) {
                $featureVersion = $featureLine.Matches[0].Groups[1].Value
            }
        }

        if ($featureVersion) {
            $featureMatch = $localConsoles |
                Where-Object { $_.FullName -like "*$featureVersion*" } |
                Sort-Object FullName -Descending |
                Select-Object -First 1
            if ($featureMatch) {
                return $featureMatch.FullName
            }
        }

        $latestLocal = $localConsoles |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1
        return $latestLocal.FullName
    }

    foreach ($candidate in @('godot4', 'godot', 'Godot_v4.6.2-stable_win64_console.exe', 'Godot_v4.6.2-stable_win64.exe')) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            return $command.Source
        }
    }

    throw 'Godot executable not found. Pass -GodotPath, place a repo-local build under tools/godot/, or add godot4/godot to PATH.'
}

function Resolve-GdaCommand {
    $globalGda = Get-Command 'gda' -ErrorAction SilentlyContinue
    if ($globalGda) {
        return @{
            Exe = $globalGda.Source
            PrefixArgs = @()
            Label = $globalGda.Source
        }
    }

    $uvx = Get-Command 'uvx' -ErrorAction SilentlyContinue
    if (-not $uvx) {
        throw 'gda was not found on PATH, and uvx was not found either. Install gda with `uv tool install gda`, or install uv.'
    }

    if (-not (Test-Path -LiteralPath $uvCacheDir)) {
        New-Item -ItemType Directory -Force -Path $uvCacheDir | Out-Null
    }
    if (-not (Test-Path -LiteralPath $uvToolDir)) {
        New-Item -ItemType Directory -Force -Path $uvToolDir | Out-Null
    }
    if (-not (Test-Path -LiteralPath $uvToolBinDir)) {
        New-Item -ItemType Directory -Force -Path $uvToolBinDir | Out-Null
    }

    $env:UV_TOOL_DIR = $uvToolDir
    $env:UV_TOOL_BIN_DIR = $uvToolBinDir

    $prefix = @('--cache-dir', $uvCacheDir)
    if ($GdaOffline) {
        $prefix += '--offline'
    }
    if ($PythonPath) {
        $prefix += @('--python', (Resolve-Path -LiteralPath $PythonPath).Path)
    }
    $prefix += @('--from', 'gda', 'gda')

    return @{
        Exe = $uvx.Source
        PrefixArgs = $prefix
        Label = ('{0} {1}' -f $uvx.Source, ($prefix -join ' '))
    }
}

function Invoke-GdaScriptValidate {
    param(
        [hashtable]$Gda,
        [string]$RelativePath
    )

    $args = @()
    $args += $Gda.PrefixArgs
    $args += @('script', 'validate', $RelativePath, '--json')

    $previousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $output = & $Gda.Exe @args 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $previousErrorActionPreference
    $lines = @($output | ForEach-Object { $_.ToString() })
    $jsonLine = $lines | Where-Object { $_.TrimStart().StartsWith('{') } | Select-Object -First 1

    if (-not $jsonLine) {
        Write-Host ($lines -join [Environment]::NewLine)
        throw "gda did not return JSON while validating $RelativePath."
    }

    $result = $jsonLine | ConvertFrom-Json
    if ($exitCode -ne 0) {
        Write-Host ($lines -join [Environment]::NewLine)
        throw "gda exited with code $exitCode while validating $RelativePath."
    }
    if (-not $result.valid) {
        Write-Host ($lines -join [Environment]::NewLine)
        throw "gda script validate failed for $RelativePath."
    }

    Write-Host ("PASS gda validate: {0}" -f $RelativePath)
}

$GodotPath = Find-Godot -RequestedPath $GodotPath
Write-Host ('Using Godot executable: {0}' -f $GodotPath)

if (-not (Test-Path -LiteralPath $godotAppData)) {
    New-Item -ItemType Directory -Force -Path $godotAppData | Out-Null
}
$env:APPDATA = $godotAppData
$env:GDA_GODOT = $GodotPath
$env:GDA_PROJECT = $projectPath

if (-not $SkipGda) {
    $gda = Resolve-GdaCommand
    Write-Host ('Using gda command: {0}' -f $gda.Label)

    $scriptsToValidate = @(
        'scenes/gameplay/weekly_run/WeeklyRunGame.gd',
        'tests/gda_angus_weekly_run_smoke.gd'
    )
    $scriptsToValidate += $ExtraValidateScript

    foreach ($scriptPath in $scriptsToValidate) {
        Invoke-GdaScriptValidate -Gda $gda -RelativePath $scriptPath
    }
}
else {
    Write-Host 'Skipping gda script validation.'
}

Write-Host 'Running Godot headless smoke: res://tests/gda_angus_weekly_run_smoke.gd'
& $GodotPath --headless --no-header --path $projectPath -s 'res://tests/gda_angus_weekly_run_smoke.gd'
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host 'Godot agent smoke passed.'
