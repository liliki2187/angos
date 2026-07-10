# WMW Clean Resource Request v0.6.6 Review

Date: 2026-07-07

## Artifact Type

`production resource request / coordinate contract / not final atlas`

This pass converts the v0.6.4 and v0.6.5 source-aware validation into a clean resource request. It is not a new visual style mock. It defines what must be exported or regenerated before the left region cards can become production UI assets.

## Output Files

- Clean resource request sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/321-world-map-wmw-v0-6-6-clean-resource-request-sheet.png`
- Coordinate contract sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/322-world-map-wmw-v0-6-6-coordinate-contract-sheet.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/323-world-map-wmw-v0-6-6-clean-resource-request-manifest.json`
- Generator: `tmp/wmw_v06_6_clean_resource_request.py`

## Result

`PASS as production request; NOT atlas-ready.`

- Each left-card state keeps its own card size and photo ratio.
- The sheet separates accepted filled reference, current proof carrier, clean export target, runtime text boxes, and required final sprites.
- The coordinate sheet records both source pixel rects and 1920x1080 runtime rects.
- The manifest stores per-state local rects for `photo_slot`, `label_plate`, `action_button`, `title_text_box`, and `meta_text_box`.

## Required Clean Sprites

For each state:

- `card_shell_clean_no_dynamic_text`
- `photo_clip_mask_or_clean_photo_slot`
- `label_plate_blank`
- `action_button_state`

Runtime-only:

- Region title.
- Region meta/status.
- Hover/focus text color changes.

## Hard Rules Preserved

- Do not use v0.6.4 proof carriers as final atlas sprites.
- Do not bake dynamic text into final card resources.
- Do not change photo ratios without re-authoring snapshot art.
- Do not non-uniformly scale card photos or cards.
- Functional carriers must remain 0-degree orthogonal.
- Decorative tape, paperclips, and backing pages may tilt only if they do not carry functional text or click targets.

## Why This Matters

The earlier failures came from trying to correct an already-accepted style image by changing component geometry. That caused photo compression, crop loss, mismatched text plates, and false QA passes. v0.6.6 changes the workflow: the accepted reference becomes a contract, and new clean resources must conform to that contract instead of replacing it with a visually similar but structurally different component.

## Next Gate

Generate or export clean transparent sprites from this request, then rerun:

1. v0.6.5 composition validation with the clean sprites.
2. A minimal Godot capture scene.
3. 100% crop review for left cards.
4. `card_shell_pass`, `image_slot_contract_pass`, `text_action_contract_pass`, and `orthogonal_function_component_pass`.
