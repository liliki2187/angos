# PSD UI Import

This project now has a PSD-to-Godot UI verification path built around two pieces:

1. `Importality`, the Godot add-on used to recognize PSD files as importable image assets through an external command.
2. Project-local Python scripts that flatten PSD files and export visible layers into a generated `Control` + `TextureRect` scene.

## Why this route

The older Godot PSD importer from asset library entry `555` is deleted, Godot `3.2` only, and Windows-only.
`Importality` is the current Godot `4.x` path that still supports importing other graphic formats as regular images through CLI utilities.

Sources:

- https://godotengine.org/asset-library/asset/555
- https://godotengine.org/asset-library/asset/2025
- https://github.com/nklbdev/godot-4-importality

## What was added

- `addons/nklbdev.importality`
- `scripts/psd_to_png.py`
- `scripts/psd_to_godot_ui.py`
- `scripts/configure_importality_psd.py`
- `Assets/ui/psd_samples/golden_ui/source/golden_ui.psd`
- `Assets/ui/psd_samples/golden_ui/generated/...`
- `scenes/dev/GoldenUiImportedPreview.tscn`

## Preferred entry point

Use the high-level wrapper when the goal is "take this PSD and make a reusable Godot UI bundle":

```powershell
python scripts/build_psd_ui_bundle.py path\\to\\mockup.psd
```

By default this creates:

- `Assets/ui/imported/<slug>/source/<file>.psd`
- `Assets/ui/imported/<slug>/generated/...`
- `scenes/ui/imported/<Slug>Ui.tscn`
- `generated/bundle.json`

For validation-only output:

```powershell
python scripts/build_psd_ui_bundle.py path\\to\\mockup.psd --mode preview
```

This writes to `Assets/ui/psd_samples/<slug>/...` and `scenes/dev/<Slug>ImportedPreview.tscn`.

## Configure Godot editor settings

The add-on uses Godot Editor Settings, not project settings, for external conversion rules.

Run:

```powershell
python scripts/configure_importality_psd.py
```

This updates `editor_settings-4.3.tres` with:

- `importality/temporary_files_directory_path`
- `importality/command_building_rules_for_custom_image_loader`

The PSD rule points to:

```text
python scripts/psd_to_png.py {in_path} {out_path}
```

## Rebuild a PSD UI scene

```powershell
python scripts/psd_to_godot_ui.py `
  Assets/ui/psd_samples/golden_ui/source/golden_ui.psd `
  --output-dir Assets/ui/psd_samples/golden_ui/generated `
  --scene scenes/dev/GoldenUiImportedPreview.tscn `
  --root-name GoldenUiImportedPreview
```

Outputs:

- `preview/<name>_flat.png`: flattened PSD preview
- `layers/...`: visible raster layers as PNGs
- `manifest.json`: layer hierarchy and bounds
- `.tscn`: a Godot UI preview scene built from `TextureRect` nodes

## Current limitation

This path imports PSD artwork as raster UI, not semantic Godot widgets.
Buttons, labels, containers, and theme logic are not inferred from Photoshop automatically.
Use the generated scene as a layout and art baseline, then replace key parts with real Godot UI controls where needed.
