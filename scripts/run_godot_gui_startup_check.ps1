param(
    [string]$GodotPath = '',
    [ValidateSet('RunProject', 'Editor', 'ProjectManager')]
    [string]$Mode = 'RunProject',
    [int]$QuitAfterFrames = 180,
    [int]$TimeoutSeconds = 30,
    [string]$RenderingDriver = 'opengl3',
    [string]$DisplayDriver = 'windows',
    [string]$AudioDriver = 'Dummy',
    [string]$Resolution = '1280x720',
    [switch]$RecoveryMode,
    [switch]$SurviveOnly
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = (Resolve-Path (Join-Path $repoRoot 'gd_project')).Path
$logDir = Join-Path $repoRoot 'tmp\godot-gui-startup-check'

function Find-GodotGui {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        return (Resolve-Path -LiteralPath $RequestedPath).Path
    }

    $localGodotRoot = Join-Path $repoRoot 'tools\godot'
    $localExes = Get-ChildItem -Path $localGodotRoot -Recurse -File -Filter 'Godot*.exe' -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notlike '*_console.exe' }
    if ($localExes) {
        $projectConfig = Join-Path $projectPath 'project.godot'
        $featureVersion = ''
        if (Test-Path -LiteralPath $projectConfig) {
            $featureLine = Select-String -LiteralPath $projectConfig -Pattern 'config/features=PackedStringArray\("([^"]+)"\)' -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($featureLine) {
                $featureVersion = $featureLine.Matches[0].Groups[1].Value
            }
        }

        if ($featureVersion) {
            $featureMatch = $localExes |
                Where-Object { $_.FullName -like "*$featureVersion*" } |
                Sort-Object FullName -Descending |
                Select-Object -First 1
            if ($featureMatch) {
                return $featureMatch.FullName
            }
        }

        $latestLocal = $localExes |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1
        return $latestLocal.FullName
    }

    foreach ($candidate in @('godot4', 'godot', 'Godot_v4.6.3-stable_win64.exe', 'Godot_v4.6.2-stable_win64.exe')) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            return $command.Source
        }
    }

    throw 'Godot GUI executable not found. Pass -GodotPath, place a repo-local GUI build under tools/godot/, or add godot4/godot to PATH.'
}

if ($TimeoutSeconds -lt 5) {
    throw '-TimeoutSeconds must be at least 5.'
}
if ($QuitAfterFrames -lt 1 -and -not $SurviveOnly) {
    throw '-QuitAfterFrames must be at least 1 unless -SurviveOnly is used.'
}

if (-not (Test-Path -LiteralPath $logDir)) {
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
}

$GodotPath = Find-GodotGui -RequestedPath $GodotPath
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$logFile = Join-Path $logDir ("godot-gui-startup-{0}.log" -f $timestamp)

$args = @('--path', $projectPath)

switch ($Mode) {
    'RunProject' { }
    'Editor' {
        $args += '--editor'
        if ($RecoveryMode) {
            $args += '--recovery-mode'
        }
    }
    'ProjectManager' {
        $args = @('--project-manager')
    }
}

if (-not $SurviveOnly) {
    $args += @('--quit-after', $QuitAfterFrames)
}
$args += @(
    '--display-driver', $DisplayDriver,
    '--rendering-driver', $RenderingDriver,
    '--audio-driver', $AudioDriver,
    '--windowed',
    '--resolution', $Resolution,
    '--log-file', $logFile
)

Write-Host ('Using Godot GUI executable: {0}' -f $GodotPath)
Write-Host ('Mode: {0}' -f $Mode)
Write-Host ('Project path: {0}' -f $projectPath)
Write-Host ('Log file: {0}' -f $logFile)
Write-Host ('Arguments: {0}' -f ($args -join ' '))

$process = Start-Process -FilePath $GodotPath -ArgumentList $args -WorkingDirectory $projectPath -PassThru
$exited = $process.WaitForExit($TimeoutSeconds * 1000)

if ($SurviveOnly) {
    if (-not $exited) {
        Write-Host ('Godot GUI survived for {0} seconds.' -f $TimeoutSeconds)
        $closed = $process.CloseMainWindow()
        Start-Sleep -Milliseconds 800
        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
        Write-Host 'Godot GUI startup check passed in survive-only mode.'
        exit 0
    }

    if ($process.ExitCode -eq 0) {
        Write-Host 'Godot GUI exited cleanly before the survive window ended.'
        Write-Host 'Godot GUI startup check passed in survive-only mode.'
        exit 0
    }

    throw "Godot GUI exited early with code $($process.ExitCode). See log: $logFile"
}

if (-not $exited) {
    try {
        $closed = $process.CloseMainWindow()
        Start-Sleep -Milliseconds 800
        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
    }
    finally {
        throw "Godot GUI did not exit within $TimeoutSeconds seconds. This can mean a hang, a modal crash dialog, or --quit-after not being honored. See log: $logFile"
    }
}

if ($process.ExitCode -ne 0) {
    throw "Godot GUI exited with code $($process.ExitCode). See log: $logFile"
}

Write-Host 'Godot GUI startup check passed.'
