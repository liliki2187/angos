---
name: svg-to-png
description: |
  Convert a local SVG file into a PNG image on Windows by rendering it with
  Microsoft Edge headless mode. Use when Codex needs to export, rasterize, or
  preview a project SVG as PNG for sharing, design review, docs delivery, or IM
  posting. Supports explicit output path and optional width/height overrides.
---

# SVG To PNG

Use this skill to rasterize local SVG files into PNG files inside the Angus workspace.

## Workflow

1. Resolve the SVG path to an absolute local file.
2. Choose the output PNG path.
   If the user does not specify one, write the PNG next to the SVG with the same basename.
3. Run the bundled wrapper:

```cmd
E:\angus\angus\skills\svg-to-png\scripts\export-svg-to-png.cmd "<input.svg>" ["<output.png>"] [width] [height]
```

Examples:

```cmd
E:\angus\angus\skills\svg-to-png\scripts\export-svg-to-png.cmd "E:\angus\angus\design\references\diagrams\game-overall-flow.svg"
E:\angus\angus\skills\svg-to-png\scripts\export-svg-to-png.cmd "E:\angus\angus\design\references\diagrams\game-overall-flow.svg" "E:\angus\angus\design\references\diagrams\game-overall-flow@2x.png" 2600 1750
```

## Behavior

- The script detects Microsoft Edge from common Windows install paths.
- If width/height are omitted, it reads `width` and `height` from the SVG first, then falls back to `viewBox`, then to `1600x900`.
- It renders the SVG directly through Edge headless screenshot mode.
- It creates the output directory if needed.

## Reporting

Report only the useful result:

- success or failure
- output PNG path
- raster size used

If Edge is missing or the SVG path is invalid, say so briefly and stop.
