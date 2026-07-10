# WMW Runtime Assembly Validation v0.6.5 Review

Date: 2026-07-07

## Artifact Type

`deterministic runtime-composition proof / not final atlas / not Godot capture`

This pass tests whether the left region cards can be rebuilt from the v0.6.4 source-aware slices without changing the accepted card/photo pairing. It overlays no-text card composites and dynamic title/meta text onto the accepted full screen reference, then measures text boxes separately from the visual shell rectangles.

## Output Files

- Clean composition: `docs/screenshots/2026-06-24-world-map-benchmark-landing/317-world-map-wmw-v0-6-5-runtime-assembly-validation.png`
- QA overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/318-world-map-wmw-v0-6-5-runtime-assembly-validation-qa.png`
- 100% crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/319-world-map-wmw-v0-6-5-runtime-assembly-validation-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/320-world-map-wmw-v0-6-5-runtime-assembly-validation-manifest.json`
- Generator: `tmp/wmw_v06_5_runtime_assembly_validation.py`

## Result

`PASS as composition validation; NOT final runtime-ready.`

- The four left cards are restored from v0.6.4 `card_composite_no_text` slices.
- Card, photo, label, and action rects remain source-locked.
- No per-card or per-photo resize is used.
- Runtime title/meta text is fit against explicit title/meta boxes.
- All measured text boxes pass fit in the generated manifest.

## Godot Capture Status

`BLOCKED`

A temporary Godot capture script was attempted first, but Godot 4.6.2 crashed with signal 11 while running the script. The unverified script was removed instead of retained as a project test.

This means v0.6.5 does not validate:

- Godot `Label` font metrics.
- Godot imported texture alpha or mask behavior.
- Hover, pressed, focused, selected, disabled, or locked state frames.
- Actual in-project node hierarchy or theme interaction.

## What This Fixes

- Prevents the earlier false route of resizing snapshots to fit a changed card shell.
- Keeps the source image slot contract visible in QA.
- Separates visual shell fit from text fit.
- Makes text fit measurable instead of relying on visual guesswork.

## Remaining Limits

- Small meta text is only fit-validated, not final readability-approved.
- The right dossier still reflects the older source reference and is not part of this pass.
- The left-card no-text composites are still proof carriers from source cleanup, not final clean transparent sprites.
- Final atlas production still needs clean art exports, alpha masks, and state frames.

## Next Gate

Before production atlas:

1. Convert the v0.6.4/v0.6.5 source contracts into clean transparent sprite requests.
2. Produce actual clean left-card state sprites with the same rects.
3. Re-run this composition check with the clean sprites.
4. Reattempt Godot capture from a minimal isolated scene.
5. Only then call the left-card atlas runtime-ready.
