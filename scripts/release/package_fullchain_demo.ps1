param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$templateRoot = Join-Path $PSScriptRoot "fullchain_demo"
$prototypeSourceRoot = Join-Path $RepoRoot "design\prototypes\html\full-chain-demo"
$distRoot = Join-Path $RepoRoot "prototype\fullchain_demo"
$webRoot = Join-Path $distRoot "web"
$docsRoot = Join-Path $distRoot "docs"
$designRoot = Join-Path $distRoot "design"

$webFiles = @(
    "world-mysteries-full-chain.html",
    "world-mysteries-full-chain.js",
    "world-mysteries-full-chain-head.htm",
    "world-mysteries-explore-dice.html",
    "newspaper-fill-lab.html"
)

if (Test-Path $distRoot) {
    Remove-Item $distRoot -Recurse -Force
}

New-Item -ItemType Directory -Force $distRoot, $webRoot, $docsRoot, $designRoot | Out-Null

foreach ($file in $webFiles) {
    Copy-Item (Join-Path $prototypeSourceRoot $file) (Join-Path $webRoot $file) -Force
}

Copy-Item (Join-Path $prototypeSourceRoot "Assets") $webRoot -Recurse -Force

Copy-Item (Join-Path $RepoRoot "docs\*") $docsRoot -Recurse -Force
Copy-Item (Join-Path $RepoRoot "design\gdd") (Join-Path $designRoot "gdd") -Recurse -Force
Copy-Item (Join-Path $RepoRoot "design\systems") (Join-Path $designRoot "systems") -Recurse -Force

Copy-Item (Join-Path $templateRoot "index.template.html") (Join-Path $distRoot "index.html") -Force
Copy-Item (Join-Path $templateRoot "README.template.md") (Join-Path $distRoot "README.md") -Force

$cscCandidates = @(
    "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
    "C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
)
$csc = $cscCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $csc) {
    throw "csc.exe not found. Cannot build the launcher EXE."
}

$launcherSource = Join-Path $templateRoot "FullChainDemoLauncher.cs"
$launcherExe = Join-Path $distRoot "Run FullChain Demo.exe"

& $csc /nologo /target:winexe /out:$launcherExe /reference:System.Windows.Forms.dll $launcherSource

if (-not (Test-Path $launcherExe)) {
    throw "Launcher EXE build failed."
}

Write-Host "Full Chain Demo package created at: $distRoot"
Write-Host "Launcher EXE: $launcherExe"

