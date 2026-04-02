param(
    [string]$SourceClaudeRoot = (Join-Path $PSScriptRoot '..\tmp_download\Claude-Code-Game-Studios-main\.claude'),
    [string]$TargetSkillsRoot = (Join-Path $PSScriptRoot '..\skills')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Normalize-AsciiText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text
    )

    $replacements = [ordered]@{
        [char]0x00A0 = ' '
        [char]0x2013 = '-'
        [char]0x2014 = '--'
        [char]0x2018 = "'"
        [char]0x2019 = "'"
        [char]0x201C = '"'
        [char]0x201D = '"'
        [char]0x2026 = '...'
        [char]0x2190 = '<-'
        [char]0x2192 = '->'
        [char]0x2264 = '<='
        [char]0x2265 = '>='
    }

    foreach ($entry in $replacements.GetEnumerator()) {
        $Text = $Text.Replace([string]$entry.Key, $entry.Value)
    }

    return ($Text -replace "`r?`n", "`r`n").Trim() + "`r`n"
}

function Get-FrontmatterValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Frontmatter,
        [Parameter(Mandatory = $true)]
        [string]$Key
    )

    $line = ($Frontmatter -split "`r?`n" | Where-Object { $_ -match "^\s*$([regex]::Escape($Key))\s*:" } | Select-Object -First 1)
    if (-not $line) {
        throw "Missing frontmatter key '$Key'."
    }

    $value = $line -replace "^\s*$([regex]::Escape($Key))\s*:\s*", ''
    $value = $value.Trim()

    if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
        $value = $value.Substring(1, $value.Length - 2)
    }

    return $value
}

function Convert-SkillNameToDisplayName {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillName
    )

    $acronyms = @{
        'ui' = 'UI'
        'qa' = 'QA'
        'vfx' = 'VFX'
        'adr' = 'ADR'
    }

    return (($SkillName -split '-') | ForEach-Object {
            $segment = $_.ToLowerInvariant()
            if ($acronyms.ContainsKey($segment)) {
                $acronyms[$segment]
            }
            elseif ($segment.Length -le 1) {
                $segment.ToUpperInvariant()
            }
            else {
                $segment.Substring(0, 1).ToUpperInvariant() + $segment.Substring(1)
            }
        }) -join ' '
}

function Convert-FrontmatterDescription {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Description
    )

    $Description = $Description.Replace('CLAUDE.md', 'project docs')
    return Normalize-AsciiText -Text $Description
}

function Escape-DoubleQuotedScalar {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    return $Value.Replace('\', '\\').Replace('"', '\"')
}

function Convert-Body {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Body,
        [Parameter(Mandatory = $true)]
        [string[]]$SkillNames
    )

    $converted = Normalize-AsciiText -Text $Body
    $converted = $converted.Replace('.claude/docs/templates/', '../_game-studio-shared/templates/')
    $converted = $converted.Replace('.claude/docs/technical-preferences.md', 'docs/technical-preferences.md')
    $converted = $converted.Replace('CLAUDE.md', 'AGENTS.md')
    $converted = $converted.Replace('AskUserQuestion', 'a concise direct user question')
    $converted = $converted.Replace('subagent_type:', 'role:')
    $converted = $converted.Replace("agent's prompt", 'subagent prompt')
    $converted = $converted.Replace('agent prompts', 'subagent prompts')
    $converted = $converted.Replace("subagent's proposals", 'draft proposals')
    $converted = $converted.Replace("Write the agent's full analysis", 'Write the full analysis')
    $converted = $converted.Replace("Write the agent's", 'Write the')
    $converted = $converted.Replace('Use the Task tool to spawn each team member as a subagent:', 'If the user explicitly wants delegation, map each team member below to a suitable generic Codex subagent:')
    $converted = $converted.Replace('use the Task tool to delegate to', 'delegate a bounded subtask to a suitable generic Codex subagent for')
    $converted = $converted.Replace('via the Task tool', 'via a suitable generic Codex subagent')
    $converted = $converted.Replace('When delegating via Task tool', 'When delegating with generic Codex subagents')
    $converted = $converted.Replace('Use the Task tool to request sign-off:', 'If the user explicitly wants delegation, request sign-off with bounded generic Codex subagent tasks:')

    $converted = [regex]::Replace(
        $converted,
        '(?m)^Spawn the `([^`]+)` agent to:',
        'If the user explicitly wants delegation, spawn a suitable generic Codex subagent for the `$1` pass to:'
    )

    $converted = [regex]::Replace(
        $converted,
        '(?m)^Delegate to \*\*([^\*]+)\*\*:',
        'Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **$1** pass:'
    )

    $skillPattern = ($SkillNames | ForEach-Object { [regex]::Escape($_) }) -join '|'
    $converted = [regex]::Replace(
        $converted,
        "/($skillPattern)(?=[^a-z-]|$)",
        '$$$1'
    )

    return $converted.Trim() + "`r`n"
}

function Write-Utf8File {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    $directory = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Write-NormalizedCopy {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,
        [Parameter(Mandatory = $true)]
        [string]$TargetPath
    )

    $raw = [System.IO.File]::ReadAllText($SourcePath, [System.Text.Encoding]::UTF8)
    Write-Utf8File -Path $TargetPath -Content (Normalize-AsciiText -Text $raw)
}

if (-not (Test-Path -LiteralPath $SourceClaudeRoot)) {
    throw "Source Claude directory not found: $SourceClaudeRoot"
}

$sourceSkillsRoot = Join-Path $SourceClaudeRoot 'skills'
if (-not (Test-Path -LiteralPath $sourceSkillsRoot)) {
    throw "Source skills directory not found: $sourceSkillsRoot"
}

$skillDirectories = Get-ChildItem -LiteralPath $sourceSkillsRoot -Directory | Sort-Object Name
$skillNames = $skillDirectories.Name

$sharedRoot = Join-Path $TargetSkillsRoot '_game-studio-shared'
$sharedTemplatesRoot = Join-Path $sharedRoot 'templates'

$sharedFiles = @(
    @{ Source = Join-Path $SourceClaudeRoot 'docs\templates\game-concept.md'; Target = Join-Path $sharedTemplatesRoot 'game-concept.md' },
    @{ Source = Join-Path $SourceClaudeRoot 'docs\templates\game-design-document.md'; Target = Join-Path $sharedTemplatesRoot 'game-design-document.md' },
    @{ Source = Join-Path $SourceClaudeRoot 'docs\templates\project-stage-report.md'; Target = Join-Path $sharedTemplatesRoot 'project-stage-report.md' },
    @{ Source = Join-Path $SourceClaudeRoot 'docs\templates\systems-index.md'; Target = Join-Path $sharedTemplatesRoot 'systems-index.md' },
    @{ Source = Join-Path $SourceClaudeRoot 'docs\technical-preferences.md'; Target = Join-Path $sharedTemplatesRoot 'technical-preferences.md' }
)

foreach ($sharedFile in $sharedFiles) {
    Write-NormalizedCopy -SourcePath $sharedFile.Source -TargetPath $sharedFile.Target
}

foreach ($skillDirectory in $skillDirectories) {
    $skillName = $skillDirectory.Name
    $rawSkill = [System.IO.File]::ReadAllText((Join-Path $skillDirectory.FullName 'SKILL.md'), [System.Text.Encoding]::UTF8)
    $match = [regex]::Match(
        $rawSkill,
        '(?s)\A---\r?\n(?<frontmatter>.*?)\r?\n---\r?\n(?<body>.*)\z'
    )

    if (-not $match.Success) {
        throw "Skill file is missing valid frontmatter: $skillName"
    }

    $frontmatter = $match.Groups['frontmatter'].Value
    $body = $match.Groups['body'].Value

    $description = Convert-FrontmatterDescription -Description (Get-FrontmatterValue -Frontmatter $frontmatter -Key 'description')
    $convertedBody = Convert-Body -Body $body -SkillNames $skillNames
    $displayName = Convert-SkillNameToDisplayName -SkillName $skillName
    $selfSkillReference = '$' + $skillName
    $escapedDescription = Escape-DoubleQuotedScalar -Value $description.Trim()
    $escapedDisplayName = Escape-DoubleQuotedScalar -Value $displayName

    $skillContent = @"
---
name: $skillName
description: "$escapedDescription"
---

## Codex Notes

- Treat references like /$skillName or /other-skill as Codex skill names. For example, use $selfSkillReference for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

$convertedBody
"@

    $openAiYaml = @"
interface:
  display_name: "$escapedDisplayName"
  short_description: "$escapedDescription"
  default_prompt: "Use $selfSkillReference to run the $displayName workflow in this Codex project."
"@

    $targetSkillRoot = Join-Path $TargetSkillsRoot $skillName
    Write-Utf8File -Path (Join-Path $targetSkillRoot 'SKILL.md') -Content (Normalize-AsciiText -Text $skillContent)
    Write-Utf8File -Path (Join-Path $targetSkillRoot 'agents\openai.yaml') -Content (Normalize-AsciiText -Text $openAiYaml)
}

Write-Host ("Imported {0} skills into {1}" -f $skillDirectories.Count, $TargetSkillsRoot)
