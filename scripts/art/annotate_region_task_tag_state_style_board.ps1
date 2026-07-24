param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

function New-CenteredFormat {
    $format = [System.Drawing.StringFormat]::new()
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    return $format
}

function ConvertFrom-HexCodePoints {
    param([string]$HexValues)

    return -join ($HexValues.Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries) | ForEach-Object {
        [char][Convert]::ToInt32($_, 16)
    })
}

$source = [System.Drawing.Image]::FromFile($InputPath)
$bitmap = [System.Drawing.Bitmap]::new($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

try {
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.DrawImageUnscaled($source, 0, 0)

    $warmPaper = [System.Drawing.ColorTranslator]::FromHtml('#E8DDC9')
    $mutedInk = [System.Drawing.ColorTranslator]::FromHtml('#AAB5B2')
    $accent = [System.Drawing.ColorTranslator]::FromHtml('#C2B483')

    $titleFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 20, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $subtitleFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 12, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $rowFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 18, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $cellFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 15, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)

    $warmBrush = [System.Drawing.SolidBrush]::new($warmPaper)
    $mutedBrush = [System.Drawing.SolidBrush]::new($mutedInk)
    $accentBrush = [System.Drawing.SolidBrush]::new($accent)
    $center = New-CenteredFormat

    $taskType = ConvertFrom-HexCodePoints '4EFB 52A1 7C7B 578B'
    $interactionState = ConvertFrom-HexCodePoints '4EA4 4E92 72B6 6001'
    $processState = ConvertFrom-HexCodePoints '6D41 7A0B 72B6 6001'
    $combinedState = ConvertFrom-HexCodePoints '7EC4 5408 72B6 6001'
    $title = ConvertFrom-HexCodePoints '533A 57DF 4EFB 52A1 77ED 7B7E 0020 007C 0020 7C7B 578B 4E0E 72B6 6001 5BA1 6838 6807 6CE8'
    $subtitle = ConvertFrom-HexCodePoints '4E2D 5FC3 56FE 6807 003D 4EFB 52A1 7C7B 578B 0020 00B7 0020 53F3 4E0A 89D2 7B7E 003D 6D41 7A0B 72B6 6001 0020 00B7 0020 5916 7F18 002F 80CC 677F 003D 4EA4 4E92 72B6 6001'

    $graphics.DrawString($title, $titleFont, $warmBrush, [System.Drawing.RectangleF]::new(20, 14, 1632, 26), $center)
    $graphics.DrawString($subtitle, $subtitleFont, $mutedBrush, [System.Drawing.RectangleF]::new(20, 40, 1632, 16), $center)

    $rowLabels = @(
        @{ Text = (ConvertFrom-HexCodePoints '4EFB 52A1') + [Environment]::NewLine + (ConvertFrom-HexCodePoints '7C7B 578B'); Y = 145 },
        @{ Text = (ConvertFrom-HexCodePoints '4EA4 4E92') + [Environment]::NewLine + (ConvertFrom-HexCodePoints '72B6 6001'); Y = 335 },
        @{ Text = (ConvertFrom-HexCodePoints '6D41 7A0B') + [Environment]::NewLine + (ConvertFrom-HexCodePoints '72B6 6001'); Y = 532 },
        @{ Text = (ConvertFrom-HexCodePoints '7EC4 5408') + [Environment]::NewLine + (ConvertFrom-HexCodePoints '72B6 6001'); Y = 742 }
    )

    foreach ($row in $rowLabels) {
        $graphics.DrawString($row.Text, $rowFont, $accentBrush, [System.Drawing.RectangleF]::new(38, $row.Y, 105, 97), $center)
    }

    $xPositions = @(210, 559, 929, 1288)
    $widths = @(257, 271, 277, 260)
    $yPositions = @(85, 282, 483, 683)
    $permanent = ConvertFrom-HexCodePoints '5E38 9A7B 4EFB 52A1'
    $temporary = ConvertFrom-HexCodePoints '9650 65F6 4EFB 52A1'
    $chain = ConvertFrom-HexCodePoints '8FDE 7EED 4EFB 52A1'
    $hidden = ConvertFrom-HexCodePoints '9690 85CF 4EFB 52A1'
    $default = ConvertFrom-HexCodePoints '9ED8 8BA4'
    $available = ConvertFrom-HexCodePoints '53EF 7528'
    $hover = ConvertFrom-HexCodePoints '60AC 505C'
    $selected = ConvertFrom-HexCodePoints '9009 4E2D'
    $focus = ConvertFrom-HexCodePoints '7126 70B9'
    $assigned = ConvertFrom-HexCodePoints '5DF2 6D3E 9063'
    $urgent = ConvertFrom-HexCodePoints '7D27 6025'
    $locked = ConvertFrom-HexCodePoints '9501 5B9A'
    $disabled = ConvertFrom-HexCodePoints '7981 7528'
    $rightFlip = ConvertFrom-HexCodePoints '53F3 4FA7 7FFB 7B7E'
    $divider = ' | '

    $labels = @(
        ($permanent + $divider + $default)
        ($temporary + $divider + $default)
        ($chain + $divider + $default)
        ($hidden + $divider + $default)
        ($permanent + $divider + $available)
        ($permanent + $divider + $hover)
        ($permanent + $divider + $selected)
        ($permanent + $divider + $focus)
        ($permanent + $divider + $assigned)
        ($permanent + $divider + $urgent)
        ($permanent + $divider + $locked)
        ($permanent + $divider + $disabled)
        ($temporary + $divider + $urgent)
        ($chain + $divider + $assigned)
        ($hidden + $divider + $selected)
        ($permanent + $divider + $rightFlip)
    )

    for ($rowIndex = 0; $rowIndex -lt 4; $rowIndex++) {
        for ($columnIndex = 0; $columnIndex -lt 4; $columnIndex++) {
            $rect = [System.Drawing.RectangleF]::new(
                $xPositions[$columnIndex],
                $yPositions[$rowIndex],
                $widths[$columnIndex],
                34
            )
            $labelIndex = ($rowIndex * 4) + $columnIndex
            $graphics.DrawString($labels[$labelIndex], $cellFont, $warmBrush, $rect, $center)
        }
    }

    $outputDirectory = Split-Path -Parent $OutputPath
    if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }
    $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    foreach ($resource in @($center, $accentBrush, $mutedBrush, $warmBrush, $cellFont, $rowFont, $subtitleFont, $titleFont, $graphics, $bitmap, $source)) {
        if ($null -ne $resource) {
            $resource.Dispose()
        }
    }
}
