---
name: psd-to-godot-ui
description: |
  Convert a Photoshop PSD in this Godot project into a reusable UI bundle:
  a copied source PSD under project assets, generated layer PNGs, a flattened
  preview PNG, manifest metadata, and a `Control`-rooted `.tscn` scene made
  of nested `Control` groups plus `TextureRect` leaves. Use when the user
  wants to import a PSD mockup, validate that a PSD can become a Godot UI
  scene, regenerate the scene after PSD changes, or prepare a PSD-designed
  interface for later integration into the game.
---

# PSD To Godot UI

Treat "project-usable UI scene" as a reusable Godot asset bundle with these outputs:

- a source PSD stored inside the repo
- generated PNG textures for visible PSD layers
- `generated/manifest.json` describing the exported hierarchy
- a flattened preview PNG for quick inspection
- a `.tscn` scene rooted at `Control`, with group layers mapped to `Control` nodes and visible raster layers mapped to `TextureRect` nodes

This pipeline creates raster UI scaffolding, not semantic Godot widgets.
Do not claim that buttons, labels, containers, or theme logic were inferred automatically.
Use the generated scene as a reviewable layout/art baseline that can later be integrated or replaced with native Godot controls.

## Default workflow

1. Use `python scripts/import/build_psd_ui_bundle.py <psd_path>` as the default entry point.
2. Use `reusable` mode unless the user clearly asks for a throwaway validation build.
3. Let the wrapper:
   - copy the PSD into the repo
   - configure Importality editor settings
   - generate the asset bundle
   - emit `bundle.json` with the important output paths
4. Read `generated/bundle.json` and report the exact scene path, asset folder, preview PNG, and manifest path.
5. Summarize what the user can do next: instantiate the generated `.tscn` into a gameplay scene, keep it as a preview scene, or replace selected raster nodes with native Godot UI controls.

## Output conventions

Use these defaults unless the user asks for a different layout:

- `reusable` mode:
  - `gd_project/Assets/ui/imported/<slug>/source/<file>.psd`
  - `gd_project/Assets/ui/imported/<slug>/generated/...`
  - `gd_project/scenes/ui/imported/<Slug>Ui.tscn`
- `preview` mode:
  - `gd_project/Assets/ui/psd_samples/<slug>/source/<file>.psd`
  - `gd_project/Assets/ui/psd_samples/<slug>/generated/...`
  - `gd_project/scenes/dev/<Slug>ImportedPreview.tscn`

Use `preview` mode for proving the pipeline works.
Use `reusable` mode for assets the team may later wire into the game.

## Commands

Preferred high-level command:

```powershell
python scripts/import/build_psd_ui_bundle.py "<absolute-or-relative-psd-path>"
```

Validation-only build:

```powershell
python scripts/import/build_psd_ui_bundle.py "<absolute-or-relative-psd-path>" --mode preview
```

Lower-level commands only when debugging or changing the pipeline:

```powershell
python scripts/import/configure_importality_psd.py
python scripts/import/psd_to_godot_ui.py "<input.psd>" --output-dir "<generated-dir>" --scene "<scene.tscn>" --root-name "<SceneRootName>"
```

## Integration boundary

By default, stop after generating the reusable scene bundle and reporting the paths.
Only modify existing gameplay scenes when the user explicitly asks to hook the generated UI into the game.

When the user does ask for integration:

1. Find the target Godot scene.
2. Instance the generated `.tscn` into an appropriate `Control`-based parent.
3. Preserve the generated scene as a separate reusable asset instead of flattening it into the gameplay scene unless the user asks otherwise.
4. Call out any remaining manual follow-up, especially replacing raster-only elements with real interactive controls.

## References

Read `docs/tools/psd-ui-import.md` only when you need to debug the pipeline, adjust conventions, or explain the tooling in more depth.
