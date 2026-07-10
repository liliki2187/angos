# WMW World Map Component Correction v0.6.1 Review

Date: 2026-07-06

## Artifact Type

`component_correction_candidate / aspect-safe thumbnail pass / no-text shell sheet / filled text validation / not atlas / not final art`

This pass replaces the downgraded v0.6 component sheet. The main correction is image aspect safety for left-card snapshots.

## Output Files

- No-text component sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/299-world-map-wmw-v0-6-1-aspect-safe-component-no-text-sheet.png`
- Filled text validation sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/300-world-map-wmw-v0-6-1-aspect-safe-component-filled-sheet.png`
- QA overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/301-world-map-wmw-v0-6-1-aspect-safe-component-qa.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/302-world-map-wmw-v0-6-1-aspect-safe-component-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/303-world-map-wmw-v0-6-1-aspect-safe-component-manifest.json`
- Generator script: `tmp/wmw_v06_component_correction_sheet.py`

## Result

Downgraded after user review. v0.6.1 fixed non-uniform thumbnail compression, but it broke the accepted source image / component slot pairing on the left region cards.

- Component families represented: 4 left region cards, 3 bottom receipts, 3 right CTA rows.
- Manifest rects: 61
- Left-card photo slots changed from a flattened `262x75` lane to a single `262x150` lane.
- Thumbnail placement now uses aspect-preserving cover crop instead of non-uniform resize, but this is not enough when the slot ratio itself is wrong.
- CTA rows preserve the v0.4.1 clean-button rule: no spike-like internal facets, no protruding false arrows, clean label plates.
- Bottom receipts remain independent components, not cropped from the overlapped full-screen mock.

## What This Fixes

- Removes the visible vertical compression in left-card snapshots.
- Prevents image assets from passing component QA just because text and shells are correct.
- Establishes `image_aspect_pass` as a required peer to `text_geometry_pass` and `art_shell_geometry_pass`.
- Exposes a missing gate: `image_slot_contract_pass`. Accepted component/photo pairings must keep their original slot ratio and composition unless the snapshot art is re-authored to the new ratio.

## Remaining Limits

- This is still not final art and not atlas output.
- The third region image uses aspect-preserving cover from a narrow source crop, so it reads as visibly zoomed/cropped. This is not acceptable for a component correction pass.
- The left region cards are no longer valid as component candidates in this artifact. CTA and receipt studies may still be referenced separately, but v0.6.1 must not be used as a left-card source for atlas or runtime assembly.
- Font hierarchy is still conservative and needs a later typography stress pass.
- Final WMW paper material and color contract still need to be reapplied.

## Production Rule

For `photo_rect`, `snapshot_rect`, `portrait_rect`, `icon_art_rect`, map inset, evidence image, or any static visual content:

- Do not use non-uniform resize.
- Use aspect-preserving cover crop when the slot must be filled and the source/slot ratio mismatch is minor.
- Use aspect-preserving contain with intentional matte when the full image must remain visible.
- Or resize the component slot to match the art.
- If the image looks compressed even though the shell and text pass, the component fails.
- If a previously accepted UI already had a good component/photo pairing, preserve that pairing as `image_slot_contract_pass`. Do not change the component slot ratio and hide the mismatch with cover crop.

## Loop Log - Source Slot Contract Failure

- Trigger source: User pointed out that v0.6.1 shows obvious image cropping, and asked why the original UI component and image fit well without compression but became mismatched after my changes.
- Original issue: The original left-card UI had card shell, photo window, image composition, and text area working as one visual contract. My v0.6/v0.6.1 revisions rebuilt the card shell and photo lane independently, so the old snapshots no longer matched the new component proportions.
- Failure attribution: I treated `image_aspect_pass` as sufficient. In v0.6 the image was non-uniformly squeezed; in v0.6.1 I fixed the squeezing by using cover crop, but I kept a single new `262x150` photo slot for multiple card states. For a narrow source crop, cover crop preserved aspect ratio but cut away the intended composition. This changed the accepted component/image relationship instead of preserving it.
- Current handling: v0.6.1 is downgraded for left-card assetization. It can only be used as a diagnostic example for aspect safety and source-slot mismatch, not as a left-card production candidate.
- Recurrence protection: Add `image_slot_contract_pass` alongside `image_aspect_pass`: before rebuilding any existing component, measure and lock the accepted source `snapshot_rect` ratio, target slot ratio, safe crop window, and visible subject margins. If the component slot ratio changes, the image must be re-authored to that ratio, or the slot must be reverted.
- Captured: Yes. The rule is added to `docs/onboarding/ui-interaction-guidelines.md` and `docs/onboarding/assetized-ui-production-chain.md`, and this review now records the downgrade.

## Next Gate

1. Run a text stress sheet on v0.6.1:
   - longest region name
   - longest status/meta line
   - two-digit day count
   - locked / disabled CTA reason
2. Rebuild the left-card correction as v0.6.2 using source-aware photo slot contracts:
   - either preserve each accepted card's original photo slot ratio;
   - or generate / crop new snapshot art to the new slot ratio before composing the card.
3. Produce atlas-export layout after stress passes.
4. Recompose one world-map screenshot from independent components and compare against the accepted full-screen target.
