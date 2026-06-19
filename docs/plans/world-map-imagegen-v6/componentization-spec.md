# World Map v6g Assetized UI Componentization Spec

> Status: 2026-06-16 component candidate pass, formal UI quality not yet passed.  
> Source artboard: `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/wm-fullscreen-artboard-v6g-pixel-strong.png`.  
> Rule: v6g is the current user-selected strong-pixel expansion source. The fullscreen artboard is never wired directly as an interactive UI.

## Production Flow

1. Treat v6g as the approved style and layout source for this pass.
2. Derive component candidates by crop / resize / transparent padding only.
3. Register each candidate in `world_map_imagegen_manifest.json` with `runtime_rect`, `dynamic_text_rects`, `forbidden_zones`, state contract, and hit contract where applicable.
4. Generate `review-overlays` before any Godot replacement.
5. Use component crops only as validation candidates. For final shipped UI, regenerate high-risk interactive pieces as independent Image 2 / human-art-tool assets, especially CTA, card states, pins, and selected/locked overlays.
6. Godot owns all Chinese text, numbers, region names, countdowns, state labels, pin semantics, hover, selected, disabled, pressed, and click logic.

## Component Ownership

| Asset id | Role | Source | Dynamic ownership |
| --- | --- | --- | --- |
| `wm_map_board_v6g_component_candidate` | Central static world-map board | v6g crop | Godot owns pins, routes, selected rings, labels |
| `wm_left_index_stack_v6g_component_candidate` | Left region index stack and four blank slots | v6g crop | Godot owns region names, counts, status, selection |
| `wm_right_dossier_body_v6g_component_candidate` | Selected-region dossier body, excluding CTA | v6g crop | Godot owns title, preview status, details, lock reason |
| `wm_cta_plate_v6g_default_candidate` | Main enter/dispatch CTA default frame | v6g crop | Godot owns label and button state; final needs state atlas |
| `wm_bottom_ticker_v6g_component_candidate` | Bottom channel ticker strips | v6g crop | Godot owns channel summaries and alert counts |
| `wm_side_tab_rail_v6g_component_candidate` | Right icon tab rail | v6g crop | Godot owns tab hit state; no text on rail |

## Safe-Zone Lessons Applied

- Control rect is not content rect. Text must fit inside declared `dynamic_text_rects`, not merely inside the visual card.
- Colored tabs, ribbons, screws, dense halftone corners, crop marks, and warning stripes are `forbidden_zones`.
- The CTA is independent from the right dossier. It must support `default / hover / pressed / disabled / loading`.
- Left index cards may be clicked as slots, but their long-term shipped form should use card state frames or a clean runtime selected overlay.
- Map pins are not part of the map board. They need a separate atlas with `normal / hover / selected / locked / urgent / completed`.

## Visual Acceptance Checklist

- v6g strong pixel language remains visible at 100% scale.
- Dynamic text zones stay calm enough for Chinese labels and two-line meta.
- No text zone touches a ribbon, screw, border, warning stripe, dense halftone, or colored tab.
- Fullscreen artboard, component crops, and overlay screenshots are reviewed together.
- Any component that looks cropped because it was cut from the mother artboard must be regenerated as an independent art asset before final Godot replacement.
- Safe-zone passing is not enough. Text must look absorbed by paper, dossier fields, ticker strips, map markings, or the CTA object, not pasted over the bitmap.
- Font, state, selection, and CTA semantics must be reviewed as a single UI system before live replacement.

## 2026-06-16 Quality Gap Review

User feedback on the v6g Godot preview: the result is still far from shipped-game quality. The main issue is not only position or overflow. Image, text, and function do not yet work as one system; the text reads like a Godot label layer placed over strong bitmap art, and the font stack is not yet an Angus UI system.

Cross-agent diagnosis:

- SIA: v6g currently reads as high-quality style art plus development text, not a finished game interface. Mature references such as `Papers, Please`, `Inscryption`, `Into the Breach`, `World of Horror`, `Citizen Sleeper`, `DREDGE`, and `Dave the Diver` show that strong UI polish comes from object action, state clarity, and type treatment sharing one system.
- Angus art director: the central map direction has potential, but CTA, pin, route, and text layers are not yet fully absorbed into the modern abnormal-weekly / editorial-object language. Current pins still risk generic glossy map-icon language.
- UX: the pipeline treated safe rectangles as semantic rectangles. Current selected region, red/cyan route state, right dossier, bottom ticker, and CTA do not yet form one decision package.
- UI Designer: next pass should not expand all regions. Build one single-state mock first: `North America quarantine zone selected + red-line heating + enterable`.

Formal UI candidate gate:

1. Define font tokens before more asset work: current-region title, section title, body, meta/status, CTA, and numbers.
2. Add `content_role` for each dynamic text zone: `region_title`, `status_badge`, `route_summary`, `cta_label`, `ticker_broadcast`, etc.
3. Unify state tokens across pin, left index card, right dossier, ticker, and CTA: `normal / hover / selected / locked / urgent / completed / disabled / loading`.
4. Make selected region linkage visible across left card, map pin, right dossier header, and CTA.
5. Regenerate or tighten `wm_pin_icon_v6g_atlas` so pins read as Angus editorial marks / printed map pins, not generic navigation icons.
6. Rework CTA as an editorial action object such as dispatch signoff, channel cut-in, or investigation approval; a centered label on a plate is not enough.
7. Validate with whole-screen, safe-zone, and 100% local crops for left card, map pin, right dossier, CTA, and ticker.
8. Do not promote v6g preview to live replacement until this gate passes.

## First Candidate Pass

Generated from `postprocess-mapping.v6g-components-candidate.json`:

- `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-map-board-v6g-component.png`
- `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-left-index-stack-v6g-component.png`
- `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-right-dossier-body-v6g-component.png`
- `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-cta-plate-v6g-default.png`
- `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-bottom-ticker-v6g-component.png`
- `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-side-tab-rail-v6g-component.png`

Validation additions:

- `validate-manifest` now fails if any `dynamic_text_rects` overlap `forbidden_zones`.
- `validate-manifest` now validates `hit_rect` and `hit_rects`.
- `review-overlays` now draws `hit_rect` / `hit_rects` in yellow in addition to green text zones, red forbidden zones, and cyan frames.

Current overlay summary:

- `docs/screenshots/2026-06-15-world-map-imagegen-v6-review/wm_v6g_component_candidate_safe_zones_summary.png`

## Next Production Assets

The first crop pass validates layout and manifest structure. The next true art-production pass should generate:

1. `wm_cta_plate_v6g_state_atlas`: `default / hover / pressed / disabled / loading`.
2. `wm_index_card_v6g_state_atlas`: `normal / hover / selected / locked / completed`.
3. `wm_pin_icon_v6g_atlas`: `normal / hover / selected / locked / urgent / completed`.
4. `wm_route_node_v6g_atlas`: red/cyan nodes and route endpoints.
5. `wm_story_preview_frame_v6g`: blank story image frame or per-region story preview family.

## Image 2 Component Outputs

Generated and staged with Codex built-in Image 2:

- CTA state atlas source: `image_gen/codex_image2_sources/2026-06-15/20260615-194428_angus-world-map-v6g-cta-state-atlas.png`
- CTA final atlas: `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-cta-plate-v6g-state-atlas.png`
- Pin/icon clean chroma source, rejected for being too generic/glossy: `image_gen/codex_image2_sources/2026-06-15/20260615-201358_angus-world-map-v6g-pin-icon-atlas-clean.png`
- Pin/icon editorial mark chroma source, current preview candidate: `image_gen/codex_image2_sources/2026-06-16/20260616-112622_angus-world-map-v6g-pin-icon-atlas-editorial-candidate.png`
- Pin/icon final transparent atlas: `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-pin-icon-v6g-atlas.png`
- Previous glossy atlas backup: `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-pin-icon-v6g-atlas-20260615-glossy-backup.png`

Repro commands:

```powershell
python scripts/art/world_map_imagegen_pipeline.py postprocess --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json --mapping docs/plans/world-map-imagegen-v6/postprocess-mapping.v6g-cta-state-atlas-candidate.json
python scripts/art/world_map_imagegen_pipeline.py extract-chromakey-atlas --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json --asset wm_pin_icon_v6g_atlas_candidate --source image_gen/codex_image2_sources/2026-06-15/20260615-201358_angus-world-map-v6g-pin-icon-atlas-clean.png --key-color "#ff00ff" --tolerance 90 --expected-frames 8 --max-frame-fill 58 --min-column-pixels 5 --group-gap 1
python scripts/art/world_map_imagegen_pipeline.py extract-chromakey-atlas --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json --asset wm_pin_icon_v6g_atlas_candidate --source image_gen/codex_image2_sources/2026-06-16/20260616-112622_angus-world-map-v6g-pin-icon-atlas-editorial-candidate.png --key-color "#ff00ff" --tolerance 90 --expected-frames 8 --max-frame-fill 58 --min-column-pixels 5 --group-gap 1
```

QA previews:

- Safety overlay summary: `docs/screenshots/2026-06-15-world-map-imagegen-v6-review/wm_v6g_component_candidate_safe_zones_summary.png`
- Asset preview board: `docs/screenshots/2026-06-15-world-map-imagegen-v6-review/wm_v6g_component_asset_preview_board.png`

## Godot Preview Assembly

Status: preview assembled on 2026-06-15, then revised into a single-state quality mock on 2026-06-16. This is not a replacement for the live `WeeklyRunGame` world map.

Project files:

- `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapV6gPreview.gd`
- `gd_project/tests/capture_world_map_v6g_preview.gd`
- `gd_project/tests/test_world_map_imagegen_v6_manifest.gd`

Runtime scope:

- The preview reads the v6 manifest through `WeeklyRunWorldMapAssetManifest.load_manifest_v6()`.
- Component `TextureRect` placement uses manifest `runtime_rect`.
- Dynamic Chinese labels use manifest `dynamic_text_rects`; no label is placed by visual guessing.
- The central map board remains static art. Runtime route lines, pin atlas frames, CTA label, index text, dossier text, and ticker text are Godot layers.
- `texture_filter` is set to nearest on the preview textures to avoid smoothing the strong-pixel material.

Screenshots:

- Clean Godot preview: `docs/screenshots/2026-06-15-world-map-v6g-godot-preview/01-v6g-godot-preview-clean.png`
- Godot safe-zone preview: `docs/screenshots/2026-06-15-world-map-v6g-godot-preview/02-v6g-godot-preview-safe-zones.png`
- Single-state quality mock clean preview: `docs/screenshots/2026-06-16-world-map-v6g-single-state-mock/01-v6g-single-state-mock-clean.png`
- Single-state quality mock safe-zone preview: `docs/screenshots/2026-06-16-world-map-v6g-single-state-mock/02-v6g-single-state-mock-safe-zones.png`

Single-state mock changes:

- Focuses the preview on `North America quarantine zone selected + red-line heating + enterable`.
- Adds a runtime font stack based on the title/editorial-office screens: `Microsoft YaHei`, `Noto Sans CJK SC`, `Noto Sans SC`, `SimHei`, `Arial Unicode MS`.
- Demotes non-current index cards and non-current pins.
- Adds selected-region linkage across left index card, central pin halo, right dossier title/status, bottom ticker, and CTA.
- Rewrites the right dossier into status badges, short clue summary, action consequence, and CTA path.
- Replaces the generic glossy pin atlas preview with an editorial-marker atlas: tack, seal, lock tag, urgent tag, completed stamp, and route nodes.
- Offsets and resizes non-current map markers so they remain readable without covering the red/cyan route structure.
- Adds runtime typography treatments so text reads as paper fields and print marks instead of plain Labels: selected card corner brackets, title rules, subtle ink shadow / red-cyan misregistration layers, section underline, and CTA stamp rails.
- Keeps all text dynamic in Godot; no new baked Chinese text or fake state was added to PNG assets.

Verification:

```powershell
python scripts/art/world_map_imagegen_pipeline.py validate-manifest --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json
python scripts/art/world_map_imagegen_pipeline.py validate-final-assets --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json
python scripts/art/world_map_imagegen_pipeline.py review-overlays --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json --out-dir docs/screenshots/2026-06-15-world-map-imagegen-v6-review
godot --headless --path gd_project -s res://tests/test_world_map_imagegen_manifest.gd
godot --headless --path gd_project -s res://tests/test_world_map_imagegen_v6_manifest.gd
godot --path gd_project --resolution 1920x1080 --windowed --audio-driver Dummy --rendering-driver opengl3 -s res://tests/capture_world_map_v6g_preview.gd
```

2026-06-16 verified:

- `python scripts/art/world_map_imagegen_pipeline.py validate-manifest --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json` passed with 16 assets, 0 errors, 0 warnings.
- `python scripts/art/world_map_imagegen_pipeline.py validate-final-assets --manifest gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json` passed with no missing final assets.
- `godot --headless --path gd_project -s res://tests/test_world_map_imagegen_v6_manifest.gd` passed.
- `godot --path gd_project --resolution 1920x1080 --windowed --audio-driver Dummy --rendering-driver opengl3 -s res://tests/capture_world_map_v6g_preview.gd` generated the single-state mock screenshots listed above.
- 100% crops checked for selected left card, right header/body, CTA, bottom ticker, and adjusted map markers under `docs/screenshots/2026-06-16-world-map-v6g-single-state-mock/crops/`.

Known risks before live replacement:

- `wm_pin_icon_v6g_atlas_candidate` now reads closer to Angus editorial map objects than the rejected glossy pin pass, but it is still a preview candidate. Before production promotion, re-review selected/urgent/locked/completed states against a real gameplay state matrix.
- `wm_cta_plate_v6g_state_atlas_candidate` is acceptable for state validation, but should be regenerated or tightened as a production atlas before live replacement.
- Index card state frames are not yet independent production assets; current crop validates layout and text zones only.
- Runtime typography is improved, but formal UI still needs a real type token pass: production font choice, weight rules, numeric alignment, hover/selected text state, and fallback behavior for machines without the preferred CJK font.
- This preview validates 1920x1080 first. Before live replacement, rerun screenshots or scale checks for the manifest desktop 16:9 targets.
