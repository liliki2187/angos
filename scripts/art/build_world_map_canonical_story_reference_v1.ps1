param(
    [string]$OutputPath = "D:\angos\image_gen\2026-08-18\world-map-rough-abstraction-filled-target-v1\00-canonical-story-content-reference.png"
)

Add-Type -AssemblyName System.Drawing

$sources = @(
    @{ Label = "01 NORTH AMERICA — FULL 1104×704 / 69:44"; Path = "D:\angos\gd_project\Assets\prototypes\world_map_integrated\a_style_v2_runtime\north_america_story_1104x704.png" },
    @{ Label = "02 EAST ASIA — FULL 1104×704 / 69:44"; Path = "D:\angos\gd_project\Assets\prototypes\world_map_integrated\a_style_v2_runtime\east_asia_story_1104x704.png" },
    @{ Label = "03 PACIFIC — FULL 1104×704 / 69:44"; Path = "D:\angos\gd_project\Assets\prototypes\world_map_integrated\a_style_v2_runtime\pacific_story_1104x704.png" }
)

$outputDirectory = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

$canvas = New-Object System.Drawing.Bitmap 1800, 760
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$graphics.Clear([System.Drawing.Color]::FromArgb(20, 32, 40))
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAlias

$titleFont = New-Object System.Drawing.Font("Arial", 28, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$noteFont = New-Object System.Drawing.Font("Arial", 14)
$whiteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(235, 232, 218))
$mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(160, 176, 178))
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(160, 176, 178), 2)

$graphics.DrawString("CANONICAL STORY CONTENT — COMPOSITION LOCK ONLY", $titleFont, $whiteBrush, 44, 28)
$graphics.DrawString("Use the complete frame. No crop, no stretch, no alternate thumbnail.", $noteFont, $mutedBrush, 48, 76)

$panelWidth = 552
$panelHeight = 352
$startX = 48
$gap = 24
$imageY = 150

for ($index = 0; $index -lt $sources.Count; $index++) {
    $item = $sources[$index]
    $x = $startX + (($panelWidth + $gap) * $index)
    $graphics.DrawString($item.Label, $labelFont, $whiteBrush, $x, 116)
    $image = [System.Drawing.Image]::FromFile($item.Path)
    try {
        $graphics.DrawImage($image, $x, $imageY, $panelWidth, $panelHeight)
        $graphics.DrawRectangle($borderPen, $x, $imageY, $panelWidth, $panelHeight)
    }
    finally {
        $image.Dispose()
    }
}

$graphics.DrawString("Same North America source must reappear whole in left card and right dossier.", $noteFont, $mutedBrush, 48, 540)
$graphics.DrawString("East Asia and Pacific use the same identical slot geometry; state never changes image size.", $noteFont, $mutedBrush, 48, 575)

$canvas.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$borderPen.Dispose()
$whiteBrush.Dispose()
$mutedBrush.Dispose()
$titleFont.Dispose()
$labelFont.Dispose()
$noteFont.Dispose()
$graphics.Dispose()
$canvas.Dispose()

Write-Output $OutputPath
