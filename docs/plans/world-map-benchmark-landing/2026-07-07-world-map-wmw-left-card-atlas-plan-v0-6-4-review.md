# WMW Left Card Atlas Plan v0.6.4 Review

Date: 2026-07-07

## Artifact Type

`atlas plan / slice contact sheet / layer-stack proof / not final atlas / not final art`

This pass continues from v0.6.3. It does not repaint or normalize the left-card art. It proves how the accepted source cards should be split before any runtime atlas work: preserve each source card/photo pairing, isolate dynamic text carriers, and keep state buttons as separate runtime carriers.

## Output Files

- Atlas plan sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/313-world-map-wmw-v0-6-4-left-card-atlas-plan-sheet.png`
- Layer-stack proof: `docs/screenshots/2026-06-24-world-map-benchmark-landing/314-world-map-wmw-v0-6-4-left-card-layer-stack-proof.png`
- Slice contact sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/315-world-map-wmw-v0-6-4-left-card-slice-contact-sheet.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/316-world-map-wmw-v0-6-4-left-card-atlas-plan-manifest.json`
- Slice directory: `docs/screenshots/2026-06-24-world-map-benchmark-landing/wmw-v0-6-4-left-card-slices/`
- Generator: `tmp/wmw_v06_4_left_card_atlas_plan.py`

## Result

`PASS as atlas plan; NOT final atlas-ready.`

- Card shells and photo references are inherited from the accepted v0.6.3 source-aware proof.
- Photo reference slices stay at 1x source scale and are not non-uniformly resized.
- Dynamic title/meta text is placed only on `label_plate_blank` carriers.
- Action icons are separated as `action_button_state` slices.
- The output intentionally keeps state-specific card heights and visible photo ratios instead of forcing a universal left-card image slot.

## Self-Correction In This Pass

The first v0.6.4 export accidentally treated a source photo area with baked label overlap as a clean final photo slice. This was corrected by renaming the slice role to `visible_photo_reference` and adding `photo_visible_rect_overrides` in the manifest.

The resulting rule is:

- A source screenshot crop can prove visual composition.
- It cannot be used as final photo art when the source UI has baked overlap between the photo, label plate, or action button.
- Final atlas production needs clean art exports, masks, or state-specific re-authored snapshot art for those areas.

## Production Rules Locked

- Do not solve photo-slot mismatch with cover crop.
- Do not use non-uniform image resize.
- Do not normalize all left-card state variants into one photo ratio unless the snapshot art is re-authored for that ratio.
- Treat `card_composite_no_text` as a proof carrier, not a final separated shell.
- Treat `visible_photo_reference` as a source composition reference, not a clean atlas sprite.
- Runtime text must sit on locked label plates, not float over arbitrary colored areas.

## Remaining Limits

- The sheet is still generated from accepted source crops, not from clean transparent UI sprites.
- It does not include hover, pressed, focused, selected, disabled, or locked runtime state frames.
- It does not include alpha/mask validation.
- It does not yet recompose a real Godot runtime screenshot.
- Warning and locked cards expose state-specific photo ratios; these require either preserved state-specific slots or re-authored snapshot art.

## Next Gate

Build v0.6.5 as a real runtime-assembly validation pass:

1. Produce or request clean no-text UI sprites for each left-card state.
2. Keep the v0.6.4 state-specific photo and label contracts.
3. Assemble the four left cards in Godot with runtime text, icon, and image nodes.
4. Capture a real 16:9 desktop screenshot plus 100% crops.
5. Pass `card_shell_pass`, `image_slot_contract_pass`, `text_action_contract_pass`, and `orthogonal_function_component_pass` before calling the atlas production-ready.
