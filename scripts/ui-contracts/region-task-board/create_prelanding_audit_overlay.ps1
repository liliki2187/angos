param(
    [string]$InputPath = "image_gen/2026-07-15/20260715-wmw-region-task-board-filled-style-v3.png",
    [string]$OutputPath = "docs/screenshots/2026-07-15-region-task-prelanding-audit/01-component-geometry-audit-overlay.png"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$inputFullPath = (Resolve-Path -LiteralPath $InputPath).Path
$outputFullPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputPath))
$outputDirectory = [System.IO.Path]::GetDirectoryName($outputFullPath)
[System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null

$source = [System.Drawing.Image]::FromFile($inputFullPath)
$bitmap = New-Object System.Drawing.Bitmap($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.DrawImage($source, 0, 0, $source.Width, $source.Height)

$scaleX = $source.Width / 1920.0
$scaleY = $source.Height / 1080.0
$font = New-Object System.Drawing.Font("Segoe UI", 13, [System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Regular)
$labelBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 9, 15, 24))
$textBrush = [System.Drawing.Brushes]::White

function Convert-Rect([int[]]$rect) {
    return [System.Drawing.RectangleF]::new(
        [single]($rect[0] * $scaleX),
        [single]($rect[1] * $scaleY),
        [single]($rect[2] * $scaleX),
        [single]($rect[3] * $scaleY)
    )
}

function Draw-AuditRect([int[]]$rect, [string]$label, [System.Drawing.Color]$color, [float]$width = 3.0) {
    $scaled = Convert-Rect $rect
    $pen = New-Object System.Drawing.Pen($color, $width)
    $pen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
    $graphics.DrawRectangle($pen, $scaled.X, $scaled.Y, $scaled.Width, $scaled.Height)
    $size = $graphics.MeasureString($label, $font)
    $labelRect = [System.Drawing.RectangleF]::new(
        [single]($scaled.X + 5),
        [single]($scaled.Y + 5),
        [single]($size.Width + 10),
        [single]($size.Height + 4)
    )
    $graphics.FillRectangle($labelBrush, $labelRect)
    $graphics.DrawString($label, $font, $textBrush, $labelRect.X + 5, $labelRect.Y + 2)
    $pen.Dispose()
}

$banner = [System.Drawing.RectangleF]::new(270, 8, 1080, 34)
$graphics.FillRectangle($labelBrush, $banner)
$graphics.DrawString(
    "FROZEN 1920x1080 GEOMETRY SCALED INTO 1672x941 PREVIEW - VISIBLE DRIFT MEANS NO DIRECT CROP",
    $smallFont,
    $textBrush,
    $banner.X + 10,
    $banner.Y + 8
)

Draw-AuditRect @(0, 0, 1920, 72) "HUD - NATIVE GODOT" ([System.Drawing.Color]::FromArgb(255, 87, 214, 141))
Draw-AuditRect @(24, 96, 380, 804) "LEFT INDEX - REBUILD SHELL" ([System.Drawing.Color]::FromArgb(255, 255, 176, 64))
Draw-AuditRect @(420, 96, 1040, 804) "MAP - REUSE ORIGINAL" ([System.Drawing.Color]::FromArgb(255, 56, 205, 255))
Draw-AuditRect @(1484, 96, 412, 960) "DOSSIER - REBUILD SHELL" ([System.Drawing.Color]::FromArgb(255, 235, 92, 255))
Draw-AuditRect @(24, 916, 1436, 140) "SCHEDULE - NATIVE + NINEPATCH" ([System.Drawing.Color]::FromArgb(255, 255, 225, 72))

Draw-AuditRect @(1508, 248, 364, 316) "SUMMARY 7-8 / STRESS 9" ([System.Drawing.Color]::FromArgb(255, 255, 255, 255)) 2
Draw-AuditRect @(1512, 916, 356, 112) "PRIMARY CTA - MASTER" ([System.Drawing.Color]::FromArgb(255, 255, 86, 86)) 2
Draw-AuditRect @(52, 938, 318, 100) "DAY GATE - DISTINCT MASTER" ([System.Drawing.Color]::FromArgb(255, 110, 154, 255)) 2

$warning = [System.Drawing.RectangleF]::new(715, 300, 420, 54)
$warningBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 122, 37, 31))
$graphics.FillRectangle($warningBrush, $warning)
$graphics.DrawString("PIN SET MUST MATCH LEFT task_id SET - LANDMARKS CANNOT USE TASK-PIN SILHOUETTE", $smallFont, $textBrush, $warning.X + 10, $warning.Y + 10)

$bitmap.Save($outputFullPath, [System.Drawing.Imaging.ImageFormat]::Png)

$warningBrush.Dispose()
$labelBrush.Dispose()
$font.Dispose()
$smallFont.Dispose()
$graphics.Dispose()
$bitmap.Dispose()
$source.Dispose()

Write-Output $outputFullPath
