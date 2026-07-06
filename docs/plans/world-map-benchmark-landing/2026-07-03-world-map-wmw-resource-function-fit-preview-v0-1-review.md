# World Map WMW Resource-Function Fit Preview v0.1 Review

Date: 2026-07-03

## Artifact Type

`resource-function fit preview / dry-run / not production atlas`

This preview answers whether the benchmark-like visual shells can work with real runtime text and functional zones before producing a no-text atlas.

## Output Files

- Fit preview: `docs/screenshots/2026-06-24-world-map-benchmark-landing/265-world-map-wmw-resource-function-fit-preview-v0-1.png`
- Fit QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/266-world-map-wmw-resource-function-fit-qa-v0-1.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/267-world-map-wmw-resource-function-fit-crops-v0-1.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/268-world-map-wmw-resource-function-fit-preview-v0-1.json`

## Result

**Fit route is valid enough to continue, but this v0.1 QA overlay is not a pass. Not final art.**

This dry-run keeps the benchmark shell visible and simulates runtime text/status layers inside the v0.2 contract rects. It shows:

- Right dossier title/status/stamp and CTA labels can fit without slanting.
- Left region card labels can fit inside the benchmark bottom label plates.
- Bottom receipt title/value/progress lanes can fit the benchmark receipt shells.
- The visual shell still reads closer to the benchmark than the v0.95 temporary overlay, because v0.95 is no longer the art source.

## Why This Stage Helps

This is the checkpoint before atlas work:

1. The art shell is still benchmark-like.
2. Runtime text is rendered separately, so we can see font, weight, padding, and hierarchy.
3. QA overlay proves the content rects are where the runtime will write.
4. If text feels too cramped or too small here, we resize the shell or rewrite copy before no-text atlas production.

## Known Issues

- The fit preview is a dry-run over a text-baked benchmark image; it is not a true no-text shell.
- Some old baked text / plate color ghosts may remain where the script covered text areas.
- The contact sheet crops the bottom receipt group tightly; the full preview is the primary visual check.
- It only tests one state: `北美禁区带 / 红线升温 / 可进入`. Multi-state pressure is still required.

## Next Gate

Before no-text atlas production:

1. Make a state stress sheet with selected / available / warning / locked / disabled and longest likely Chinese strings.
2. Check 100% crops for right CTA, left card, bottom receipt, and right header.
3. If all fit, generate or paint no-text benchmark shells for the 11 components from the resource contract.
4. Rebuild the same runtime text/status layer on top of those no-text shells.
5. Only then move toward atlas slicing and Godot integration.

## Loop Log - Overlay / Visual Module Mismatch

- Trigger source: user pointed out that the red CTA area and other regions do not overlap with the real component zones in `266-world-map-wmw-resource-function-fit-qa-v0-1.png`.
- Original issue: the overlay appears to certify fit, but some boxes do not sit on the visual module they are meant to validate.
- Failure attribution: v0.1 collapsed four different concepts into generic boxes: `visual_shell_rect`, `content_rect`, `ink_safe_rect`, and `hit_rect`. The generator checked text fit inside self-authored coordinates, but did not check whether those coordinates match the real color plate / button module in the benchmark asset.
- Current handling: downgrade v0.1 QA overlay to "directional dry-run only"; do not use it as an atlas contract pass.
- Recurrence protection: v0.2 must draw and validate four separately named layers: `visual_module_rect`, `text_plate_rect`, `ink_safe_rect`, and `hit_rect`. The right CTA must split `right_action_icon_hit` into `action_visual_plate`, `action_glyph_rect`, and `action_hit_rect`.
- Whether captured: captured in this review. Next manifest must include 100% crops for each role, and pass/fail must be based on matching the real colored/paper module, not only on text fitting inside authored coordinates.
