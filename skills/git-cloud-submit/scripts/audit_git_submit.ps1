#Requires -Version 5.1

[CmdletBinding()]
param(
    [string]$Repository = ".",
    [ValidateSet("Text", "Json")]
    [string]$Format = "Json",
    [ValidateSet("WorkingTree", "Staged")]
    [string]$Scope = "WorkingTree",
    [long]$WarnFileBytes = 10MB,
    [long]$BlockFileBytes = 100MB
)

$ErrorActionPreference = "Stop"

function Invoke-GitCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [switch]$AllowFailure
    )

    $output = @(& git @Arguments 2>&1 | ForEach-Object { "$_" })
    $exitCode = $LASTEXITCODE
    if (-not $AllowFailure -and $exitCode -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code ${exitCode}: $($output -join [Environment]::NewLine)"
    }

    [pscustomobject]@{
        ExitCode = $exitCode
        Lines = $output
    }
}

function Convert-GitPath {
    param([string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return $Path
    }

    $trimmed = $Path.Trim()
    if ($trimmed.StartsWith('"') -and $trimmed.EndsWith('"')) {
        try {
            return ($trimmed | ConvertFrom-Json)
        }
        catch {
            return $trimmed.Trim('"')
        }
    }
    return $trimmed
}

function Get-SafeRemoteUrl {
    param([string]$Url)

    if ([string]::IsNullOrWhiteSpace($Url)) {
        return $null
    }
    return [regex]::Replace($Url, '(?i)(https?://)([^/@]+)@', '$1***@')
}

function Get-ExistingFileInfo {
    param([string[]]$Paths)

    $items = @()
    foreach ($path in @($Paths | Sort-Object -Unique)) {
        if ([string]::IsNullOrWhiteSpace($path)) {
            continue
        }
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            $item = Get-Item -LiteralPath $path
            $items += [pscustomobject]@{
                Path = ($path -replace '\\', '/')
                Bytes = [long]$item.Length
                Extension = $item.Extension.ToLowerInvariant()
            }
        }
    }
    return $items
}

$originalLocation = Get-Location
try {
    Set-Location -LiteralPath (Resolve-Path -LiteralPath $Repository)
    $rootResult = Invoke-GitCommand -Arguments @("rev-parse", "--show-toplevel")
    $repoRoot = $rootResult.Lines[0]
    Set-Location -LiteralPath $repoRoot

    $statusResult = Invoke-GitCommand -Arguments @("-c", "core.quotepath=false", "status", "--porcelain=v1", "--untracked-files=all")
    $statusEntries = @()
    foreach ($line in $statusResult.Lines) {
        if ($line.Length -lt 3) {
            continue
        }
        $code = $line.Substring(0, 2)
        $rawPath = $line.Substring(3)
        if ($rawPath.Contains(" -> ")) {
            $rawPath = ($rawPath -split " -> ")[-1]
        }
        $statusEntries += [pscustomobject]@{
            Code = $code
            Path = Convert-GitPath -Path $rawPath
        }
    }

    $untrackedResult = Invoke-GitCommand -Arguments @("-c", "core.quotepath=false", "ls-files", "--others", "--exclude-standard")
    $untrackedPaths = @($untrackedResult.Lines | ForEach-Object { Convert-GitPath -Path $_ } | Where-Object { $_ })

    $stagedResult = Invoke-GitCommand -Arguments @("-c", "core.quotepath=false", "diff", "--cached", "--name-only")
    $stagedPaths = @($stagedResult.Lines | ForEach-Object { Convert-GitPath -Path $_ } | Where-Object { $_ })

    if ($Scope -eq "Staged") {
        $candidatePaths = $stagedPaths
    }
    else {
        $candidatePaths = @($statusEntries.Path | Where-Object { $_ })
    }
    $fileItems = @(Get-ExistingFileInfo -Paths $candidatePaths)

    $binaryExtensions = @(
        ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff",
        ".wav", ".mp3", ".ogg", ".flac", ".mp4", ".webm", ".mov",
        ".glb", ".gltf", ".fbx", ".blend", ".psd", ".zip", ".7z", ".rar",
        ".pdf", ".docx", ".xlsx", ".pptx"
    )
    $binaryItems = @($fileItems | Where-Object { $binaryExtensions -contains $_.Extension })
    $largeWarnings = @($fileItems | Where-Object { $_.Bytes -ge $WarnFileBytes } | Sort-Object Bytes -Descending)
    $largeBlocks = @($fileItems | Where-Object { $_.Bytes -ge $BlockFileBytes } | Sort-Object Bytes -Descending)

    $sensitivePattern = '(?i)(^|/)(\.env($|\.)|[^/]*\.(pem|p12|pfx|key)$|id_(rsa|ed25519)(\.|$)|credentials?([^/]*\.|$)|secrets?([^/]*\.|$)|tokens?([^/]*\.|$)|auth[^/]*\.json$)'
    $safeExamplePattern = '(?i)(example|sample|template|placeholder|\.dist($|\.))'
    $sensitiveCandidates = @(
        $candidatePaths |
            ForEach-Object { ($_ -replace '\\', '/') } |
            Where-Object { $_ -match $sensitivePattern -and $_ -notmatch $safeExamplePattern } |
            Sort-Object -Unique
    )

    $generatedPattern = '(?i)(^|/)(tmp|temp|logs?|\.cache|\.godot|\.import|node_modules|__pycache__)(/|$)|\.(log|tmp|bak|swp)$'
    $generatedCandidates = @(
        $candidatePaths |
            ForEach-Object { ($_ -replace '\\', '/') } |
            Where-Object { $_ -match $generatedPattern } |
            Sort-Object -Unique
    )

    if ($Scope -eq "Staged") {
        $scopeEntries = @($statusEntries | Where-Object {
            $_.Code -ne "??" -and $_.Code.Substring(0, 1) -ne " "
        })
        $scopeUntrackedCount = 0
    }
    else {
        $scopeEntries = $statusEntries
        $scopeUntrackedCount = $untrackedPaths.Count
    }

    $conflictCodes = @("DD", "AU", "UD", "UA", "DU", "AA", "UU")
    $conflicts = @($statusEntries | Where-Object { $conflictCodes -contains $_.Code })
    $deletions = @($scopeEntries | Where-Object { $_.Code.Contains("D") })
    $renames = @($scopeEntries | Where-Object { $_.Code.Contains("R") })

    $branchResult = Invoke-GitCommand -Arguments @("branch", "--show-current")
    $branch = if ($branchResult.Lines.Count -gt 0) { $branchResult.Lines[0] } else { $null }
    $upstreamResult = Invoke-GitCommand -Arguments @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}") -AllowFailure
    $upstream = if ($upstreamResult.ExitCode -eq 0 -and $upstreamResult.Lines.Count -gt 0) { $upstreamResult.Lines[0] } else { $null }

    $ahead = $null
    $behind = $null
    if ($upstream) {
        $distanceResult = Invoke-GitCommand -Arguments @("rev-list", "--left-right", "--count", "HEAD...@{u}") -AllowFailure
        if ($distanceResult.ExitCode -eq 0 -and $distanceResult.Lines.Count -gt 0) {
            $parts = $distanceResult.Lines[0] -split "\s+"
            if ($parts.Count -ge 2) {
                $ahead = [int]$parts[0]
                $behind = [int]$parts[1]
            }
        }
    }

    $remoteResult = Invoke-GitCommand -Arguments @("remote", "get-url", "origin") -AllowFailure
    $originUrl = if ($remoteResult.ExitCode -eq 0 -and $remoteResult.Lines.Count -gt 0) { Get-SafeRemoteUrl -Url $remoteResult.Lines[0] } else { $null }

    $attributesPath = Join-Path $repoRoot ".gitattributes"
    $hasAttributes = Test-Path -LiteralPath $attributesPath -PathType Leaf
    $hasLfsRules = $false
    if ($hasAttributes) {
        $hasLfsRules = [bool](Select-String -LiteralPath $attributesPath -Pattern 'filter=lfs' -Quiet)
    }
    $lfsVersionResult = Invoke-GitCommand -Arguments @("lfs", "version") -AllowFailure
    $lfsAvailable = $lfsVersionResult.ExitCode -eq 0

    $topLevel = @(
        $candidatePaths |
            ForEach-Object {
                $normalized = $_ -replace '\\', '/'
                if ($normalized.Contains('/')) { $normalized.Split('/')[0] } else { "(root)" }
            } |
            Group-Object |
            Sort-Object Count -Descending |
            ForEach-Object { [pscustomobject]@{ Name = $_.Name; Count = $_.Count } }
    )

    $counts = [ordered]@{
        entries = $scopeEntries.Count
        untracked = $scopeUntrackedCount
        staged_paths = $stagedPaths.Count
        working_tree_entries = $statusEntries.Count
        working_tree_untracked = $untrackedPaths.Count
        deletions = $deletions.Count
        renames = $renames.Count
        conflicts = $conflicts.Count
    }

    $totalBytes = [long](($fileItems | Measure-Object -Property Bytes -Sum).Sum)
    $binaryBytes = [long](($binaryItems | Measure-Object -Property Bytes -Sum).Sum)
    $flags = @()
    if ($conflicts.Count -gt 0) {
        $flags += [pscustomobject]@{ Level = "block"; Code = "UNMERGED"; Message = "Unmerged or conflicted paths exist." }
    }
    if ($sensitiveCandidates.Count -gt 0) {
        $flags += [pscustomobject]@{ Level = "block"; Code = "SENSITIVE_NAME"; Message = "Potential key, certificate, credential, or token filename found; contents were not read." }
    }
    if ($largeBlocks.Count -gt 0) {
        $flags += [pscustomobject]@{ Level = "block"; Code = "FILE_SIZE_BLOCK"; Message = "At least one file meets the blocking size threshold." }
    }
    if (-not $branch) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "DETACHED_HEAD"; Message = "The repository may be in detached HEAD state." }
    }
    if (-not $upstream) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "NO_UPSTREAM"; Message = "The current branch has no verifiable upstream." }
    }
    if ($behind -ne $null -and $behind -gt 0) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "UPSTREAM_BEHIND"; Message = "HEAD is behind upstream; do not pull or rebase silently." }
    }
    if ($deletions.Count -gt 0) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "DELETIONS"; Message = "The candidate set includes deletions that require intent confirmation." }
    }
    if ($Scope -eq "WorkingTree" -and $untrackedPaths.Count -ge 100) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "MANY_UNTRACKED"; Message = "At least 100 untracked files exist; freeze include and exclude paths by theme." }
    }
    if ($binaryBytes -ge 50MB -and -not $hasLfsRules) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "BINARY_WITHOUT_LFS"; Message = "Binary candidates total at least 50 MiB and no LFS rule was found." }
    }
    if ($largeWarnings.Count -gt 0) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "LARGE_FILES"; Message = "At least one file meets the warning size threshold." }
    }
    if ($generatedCandidates.Count -gt 0) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "GENERATED_PATHS"; Message = "Candidates include common temp, cache, log, or generated paths." }
    }
    if ($topLevel.Count -ge 6) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "MIXED_TOP_LEVEL"; Message = "Candidates span at least six top-level paths; check for unrelated work." }
    }
    if ($branch -in @("main", "master")) {
        $flags += [pscustomobject]@{ Level = "review"; Code = "PRIMARY_BRANCH"; Message = "The current branch is a primary branch candidate; recheck remote and branch before push." }
    }

    $report = [ordered]@{
        schema_version = "1.0"
        generated_at = (Get-Date).ToString("o")
        read_only = $true
        repository = $repoRoot
        scope = $Scope
        git = [ordered]@{
            branch = $branch
            upstream = $upstream
            ahead = $ahead
            behind = $behind
            origin_url = $originUrl
        }
        counts = $counts
        sizes = [ordered]@{
            candidate_existing_bytes = $totalBytes
            binary_bytes = $binaryBytes
            warn_file_bytes = $WarnFileBytes
            block_file_bytes = $BlockFileBytes
        }
        lfs = [ordered]@{
            command_available = $lfsAvailable
            gitattributes_present = $hasAttributes
            lfs_rules_present = $hasLfsRules
        }
        top_level = $topLevel
        largest_files = @($fileItems | Sort-Object Bytes -Descending | Select-Object -First 12)
        sensitive_name_candidates = $sensitiveCandidates
        generated_path_candidates = @($generatedCandidates | Select-Object -First 50)
        flags = $flags
        blocked = [bool]($flags | Where-Object { $_.Level -eq "block" })
        requires_review = [bool]($flags | Where-Object { $_.Level -eq "review" })
    }

    if ($Format -eq "Json") {
        $report | ConvertTo-Json -Depth 8
    }
    else {
        "Git cloud submit read-only audit"
        "Repository: $repoRoot"
        "Branch: $branch | upstream: $upstream | ahead/behind: $ahead/$behind"
        "Status: entries=$($counts.entries), untracked=$($counts.untracked), staged_paths=$($counts.staged_paths), deletions=$($counts.deletions), conflicts=$($counts.conflicts)"
        "Candidate existing size: $([Math]::Round($totalBytes / 1MB, 2)) MiB | binary: $([Math]::Round($binaryBytes / 1MB, 2)) MiB"
        "LFS: command=$lfsAvailable, .gitattributes=$hasAttributes, rules=$hasLfsRules"
        if ($flags.Count -eq 0) {
            "Risk flags: none"
        }
        else {
            "Risk flags:"
            foreach ($flag in $flags) {
                "- [$($flag.Level)] $($flag.Code): $($flag.Message)"
            }
        }
        if ($fileItems.Count -gt 0) {
            "Largest files:"
            $fileItems | Sort-Object Bytes -Descending | Select-Object -First 12 | ForEach-Object {
                "- $([Math]::Round($_.Bytes / 1MB, 2)) MiB  $($_.Path)"
            }
        }
        if ($sensitiveCandidates.Count -gt 0) {
            "Potentially sensitive filenames (contents not read):"
            $sensitiveCandidates | ForEach-Object { "- $_" }
        }
    }
}
finally {
    Set-Location -LiteralPath $originalLocation
}
