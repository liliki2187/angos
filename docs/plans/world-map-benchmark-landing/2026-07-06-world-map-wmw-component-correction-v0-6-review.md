# WMW World Map Component Correction v0.6 Review

Date: 2026-07-06

## Artifact Type

`component_correction_candidate / no-text shell sheet / filled text validation / not atlas / not final art`

This pass converts the previous geometry gates into an independent component correction sheet. It is not cropped from the full-screen mock and does not rely on the overlapped right dossier / bottom receipt composition.

## Output Files

- No-text component sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/294-world-map-wmw-v0-6-component-correction-no-text-sheet.png`
- Filled text validation sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/295-world-map-wmw-v0-6-component-correction-filled-sheet.png`
- QA overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/296-world-map-wmw-v0-6-component-correction-qa.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/297-world-map-wmw-v0-6-component-correction-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/298-world-map-wmw-v0-6-component-correction-manifest.json`
- Generator script: `tmp/wmw_v06_component_correction_sheet.py`

## Result

Downgraded after user review. This pass is useful as a component-grammar sketch, but it is not a valid component correction candidate because the left-card thumbnail images are visibly vertically compressed.

- Components represented: 4 left region cards, 3 bottom receipts, 3 right CTA rows.
- Manifest rects: 61
- CTA rows preserve the v0.4.1 clean-button rule: no spike-like internal facets, no protruding false arrows, clean label plates.
- Bottom receipts are rebuilt as independent components, avoiding the full-screen overlap issue found in v0.5.1.
- All dynamic text is filled after no-text shells are drawn.
- Failure: left-card snapshot slots use non-uniform resize, compressing source images into a too-wide / too-short photo lane.

## What This Proves

- The world-map component families can be represented as reusable orthogonal shells instead of a single full-screen bitmap.
- Left cards can support the four current state roles: selected, available, warning, locked.
- Receipts can support independent green / blue / red variants without being hidden under the right dossier stack.
- Right CTA style can be reused as a clean component family.

## What This Does Not Prove

- It is not final art. It still uses deterministic proof styling and source-cropped snapshots.
- It is not an atlas. The sheet contains labels and layout context; slicing should use a later atlas-specific export.
- It does not yet run longest-string, hover / pressed / selected / disabled, or locked-state stress tests.
- It does not prove final WMW paper material fidelity. The next pass must reapply the paper material and color contract.

## Self-Check Notes

- The current left-card and receipt layout is intentionally conservative: text is small enough to fit, but final font weights and hierarchy still need a typography stress pass.
- The no-text shells avoid sharp low-poly spikes in functional carriers. Large block facets remain only as calm material value planes.
- The card thumbnails are static content art and may be replaced by final generated snapshot assets later.
- The sheet is a component grammar board; it should not be treated as a finished in-game screen.

## Loop Log - Thumbnail Aspect Ratio Compression

- Trigger source: user pointed out that the left-card image is obviously flattened.
- Original issue: the v0.6 component sheet presented region-card thumbnails as if they were valid component previews, but the thumbnail art was visibly compressed.
- Failure attribution: the generator used `crop_photo(...).resize(size)` and forced source crops into a `262x75` target slot. That target aspect ratio is about `3.49:1`, while the selected source crop is about `1.74:1`. I optimized for fitting four cards on one sheet and preserving text/action geometry, but failed to preserve static image aspect ratio. This is the same class of mistake as earlier text/shell false passes: one layer passed while another visible layer failed.
- Current handling: v0.6 is downgraded. It may only be referenced for rough component grammar, not for visual approval, atlas slicing, or final UI style judgment.
- Recurrence protection: any `photo_rect`, `snapshot_rect`, portrait, icon art, map thumbnail, character portrait, item image, or generated still must pass `image_aspect_pass` before visual review. Static art cannot be non-uniformly scaled to fit a UI slot. The allowed fixes are aspect-preserving cover crop, aspect-preserving contain with intentional matte, or resizing the component slot to match the art ratio.
- Whether captured: captured here. The next pass must be v0.6.1 with aspect-preserving thumbnails or revised card proportions before typography stress or atlas export.

## Next Gate

1. Rebuild v0.6.1 with image aspect preserved:
   - no non-uniform thumbnail scaling
   - use cover crop or slot redesign
   - compare each thumbnail against the accepted full-screen source crop
2. Then run a text stress sheet:
   - longest region name
   - longest status/meta line
   - two-digit day count
   - locked / disabled CTA reason
3. Produce atlas-export layout:
   - one row per component state
   - no section labels
   - transparent or documented matte background
   - exact `target_size` per component
4. Build a Godot manifest draft from the corrected v0.6.1 rects.
5. Recompose one world-map screenshot from the independent components and compare against the accepted v0.4.1 / v0.5.1 visual target.
