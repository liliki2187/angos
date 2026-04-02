param(
    [switch]$Link
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$SkillName = "claude-to-im"
$SourceDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$CodexSkillsDir = Join-Path $env:USERPROFILE ".codex\skills"
$TargetDir = Join-Path $CodexSkillsDir $SkillName

Write-Host "Installing $SkillName skill for Codex..."

if (-not (Test-Path (Join-Path $SourceDir "SKILL.md"))) {
    throw "SKILL.md not found in $SourceDir"
}

New-Item -ItemType Directory -Path $CodexSkillsDir -Force | Out-Null

if (Test-Path $TargetDir) {
    $existing = Get-Item -LiteralPath $TargetDir -Force
    if ($existing.LinkType) {
        Write-Host "Already installed as $($existing.LinkType): $TargetDir"
    } else {
        Write-Host "Already installed at $TargetDir"
    }
    Write-Host "Remove it first if you want to reinstall."
    exit 0
}

if ($Link) {
    New-Item -ItemType Junction -Path $TargetDir -Target $SourceDir | Out-Null
    Write-Host "Linked $TargetDir -> $SourceDir"
} else {
    Copy-Item -LiteralPath $SourceDir -Destination $TargetDir -Recurse
    Write-Host "Copied to $TargetDir"
}

if ($Link) {
    Write-Host "Link mode: using the workspace copy as-is."
} else {
    $HasCodexSdk = Test-Path (Join-Path $TargetDir "node_modules\@openai\codex-sdk")
    $HasNodeModules = Test-Path (Join-Path $TargetDir "node_modules")

    if (-not $HasNodeModules -or -not $HasCodexSdk) {
        Write-Host "Installing dependencies..."
        npm install --prefix $TargetDir
    }

    if (-not (Test-Path (Join-Path $TargetDir "dist\daemon.mjs"))) {
        Write-Host "Building daemon bundle..."
        npm run build --prefix $TargetDir
    }

    Write-Host "Pruning dev dependencies..."
    npm prune --production --prefix $TargetDir
}

Write-Host ""
Write-Host "Done. Start a new Codex session and use:"
Write-Host "  claude-to-im setup"
Write-Host "  claude-to-im start"
Write-Host "  claude-to-im doctor"
