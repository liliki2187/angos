param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

function ConvertFrom-HexCodePoints {
    param([string]$HexValues)

    return -join ($HexValues.Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries) | ForEach-Object {
        [char][Convert]::ToInt32($_, 16)
    })
}

function New-CenteredFormat {
    $format = [System.Drawing.StringFormat]::new()
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    return $format
}

$source = [System.Drawing.Image]::FromFile($InputPath)
$bitmap = [System.Drawing.Bitmap]::new($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

try {
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.DrawImageUnscaled($source, 0, 0)

    $scaleX = $source.Width / 1672.0
    $scaleY = $source.Height / 941.0
    $scale = [Math]::Min($scaleX, $scaleY)

    $ink = [System.Drawing.ColorTranslator]::FromHtml('#17252A')
    $mutedInk = [System.Drawing.ColorTranslator]::FromHtml('#44545A')
    $olive = [System.Drawing.ColorTranslator]::FromHtml('#606733')
    $ochre = [System.Drawing.ColorTranslator]::FromHtml('#886A40')
    $teal = [System.Drawing.ColorTranslator]::FromHtml('#34767A')
    $slate = [System.Drawing.ColorTranslator]::FromHtml('#445967')

    $titleFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 28 * $scale, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $subtitleFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 16 * $scale, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $columnFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 22 * $scale, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $rowFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 21 * $scale, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $colorFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 14 * $scale, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)

    $inkBrush = [System.Drawing.SolidBrush]::new($ink)
    $mutedBrush = [System.Drawing.SolidBrush]::new($mutedInk)
    $rowBrushes = @(
        [System.Drawing.SolidBrush]::new($olive),
        [System.Drawing.SolidBrush]::new($ochre),
        [System.Drawing.SolidBrush]::new($teal),
        [System.Drawing.SolidBrush]::new($slate)
    )
    $center = New-CenteredFormat

    $title = ConvertFrom-HexCodePoints '533A 57DF 4EFB 52A1 77ED 7B7E 0020 007C 0020 7C7B 578B 8272 4E0E 9009 4E2D 80CC 677F'
    $subtitle = ConvertFrom-HexCodePoints '5DE6 FF1A 9ED8 8BA4 3000 53F3 FF1A 9009 4E2D FF1B 9009 4E2D 80CC 677F 7EE7 627F 4EFB 52A1 7C7B 578B 8272'
    $default = ConvertFrom-HexCodePoints '9ED8 8BA4'
    $selected = ConvertFrom-HexCodePoints '9009 4E2D'

    $graphics.DrawString($title, $titleFont, $inkBrush, [System.Drawing.RectangleF]::new(130 * $scaleX, 58 * $scaleY, 1412 * $scaleX, 36 * $scaleY), $center)
    $graphics.DrawString($subtitle, $subtitleFont, $mutedBrush, [System.Drawing.RectangleF]::new(130 * $scaleX, 98 * $scaleY, 1412 * $scaleX, 24 * $scaleY), $center)

    $graphics.DrawString($default, $columnFont, $inkBrush, [System.Drawing.RectangleF]::new(445 * $scaleX, 174 * $scaleY, 414 * $scaleX, 58 * $scaleY), $center)
    $graphics.DrawString($selected, $columnFont, $inkBrush, [System.Drawing.RectangleF]::new(978 * $scaleX, 174 * $scaleY, 410 * $scaleX, 58 * $scaleY), $center)

    $rowNames = @(
        (ConvertFrom-HexCodePoints '5E38 9A7B 4EFB 52A1'),
        (ConvertFrom-HexCodePoints '9650 65F6 4EFB 52A1'),
        (ConvertFrom-HexCodePoints '8FDE 7EED 4EFB 52A1'),
        (ConvertFrom-HexCodePoints '9690 85CF 4EFB 52A1')
    )
    $colorNames = @(
        (ConvertFrom-HexCodePoints '6A44 6984 7EFF'),
        (ConvertFrom-HexCodePoints '8D6D 9EC4'),
        (ConvertFrom-HexCodePoints '9752 7EFF'),
        (ConvertFrom-HexCodePoints '84DD 7070')
    )
    $rowY = @(278, 443, 609, 773)

    for ($index = 0; $index -lt 4; $index++) {
        $graphics.DrawString($rowNames[$index], $rowFont, $inkBrush, [System.Drawing.RectangleF]::new(98 * $scaleX, ($rowY[$index] + 17) * $scaleY, 238 * $scaleX, 34 * $scaleY), $center)
        $graphics.DrawString($colorNames[$index], $colorFont, $rowBrushes[$index], [System.Drawing.RectangleF]::new(98 * $scaleX, ($rowY[$index] + 52) * $scaleY, 238 * $scaleX, 24 * $scaleY), $center)
    }

    $outputDirectory = Split-Path -Parent $OutputPath
    if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }
    $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    foreach ($resource in @($center, $rowBrushes[0], $rowBrushes[1], $rowBrushes[2], $rowBrushes[3], $mutedBrush, $inkBrush, $colorFont, $rowFont, $columnFont, $subtitleFont, $titleFont, $graphics, $bitmap, $source)) {
        if ($null -ne $resource) {
            $resource.Dispose()
        }
    }
}
