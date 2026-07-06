# World Map WMW Layered All-Functional v0.95 Review

Date: 2026-07-03

## Artifact Type

`layered UI proof / geometry pass / visual not final`

This supersedes v0.94 for typography scale and overlay roughness. It is still not a final art asset, not a no-text atlas, and not a Godot runtime implementation.

## Output Files

- Full proof: `docs/screenshots/2026-06-24-world-map-benchmark-landing/254-world-map-wmw-v0-95-layered-all-functional-proof.png`
- Geometry QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/255-world-map-wmw-v0-95-layered-all-functional-geometry-qa.png`
- Crop contact sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/256-world-map-wmw-v0-95-functional-crops-contact-sheet.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/257-world-map-wmw-v0-95-layered-all-functional-proof.json`

## Result

**Geometry pass by construction. Visual polish not final.**

The proof converts the main text-bearing and state-bearing functional areas into deterministic axis-aligned coordinate layers:

- right header title/status/stamp;
- right CTA rows, label plates, and action boxes;
- left card title/meta plates;
- bottom receipt title/value/progress lanes.

The manifest records `27` functional components. All are coordinate-locked and marked `axis_aligned: true`, with top/bottom angles `0.0 deg`.

## What Improved From v0.94

- Text scale is reduced and no longer dominates the whole card.
- Right CTA proof remains orthogonal but reads less like a debug overlay.
- Bottom receipt lanes are more compact and closer to the source component scale.
- The contact sheet no longer overlaps proof crops.

## Remaining Visual Issues

- This is still visibly a deterministic overlay, not a finished WMW component atlas.
- The left card labels and receipt lanes need better paper/token blending, edge softness, and low-poly value planes.
- Final typography should be tuned as a style decision, not just a readable system font pass.
- Icon boxes and CTA borders need a custom atlas pass to recover the benchmark's hand-drawn sticker/weekly-paper character.

## Production Implication

The next valid route is:

1. Keep imagegen for no-text background mood, low-poly thumbnails, paper sheets, decorative tabs, stickers, clips, shadows, and surface color.
2. Move all text, CTA labels, hit rects, status rows, and progress/state lanes into a measured runtime / atlas layer.
3. Build a WMW component atlas from the v0.89 carrier contract and paper material contract.
4. Re-run geometry QA before any user-facing candidate.
5. Then run visual/style QA for color, texture, typography, icon quality, and benchmark fidelity.

Do not return to full-screen text-baked prompt-only generation for functional UI.
