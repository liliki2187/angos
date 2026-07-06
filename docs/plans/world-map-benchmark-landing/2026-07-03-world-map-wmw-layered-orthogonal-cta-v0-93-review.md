# World Map WMW Layered Orthogonal CTA v0.93 Review

Date: 2026-07-03

## Artifact Type

`layered UI proof / geometry pass / visual not final`

This is a workflow proof after v0.92 failed the text-bearing slant rule. It is not a final art asset and not a production atlas.

## Output Files

- Full proof: `docs/screenshots/2026-06-24-world-map-benchmark-landing/246-world-map-wmw-v0-93-layered-orthogonal-cta-proof.png`
- Right CTA crop: `docs/screenshots/2026-06-24-world-map-benchmark-landing/247-world-map-wmw-v0-93-right-cta-layered-crop.png`
- Geometry QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/248-world-map-wmw-v0-93-right-cta-geometry-qa.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/249-world-map-wmw-v0-93-layered-orthogonal-cta-proof.json`

## Result

**Geometry method pass. Visual polish not final.**

The v0.93 CTA rows are rebuilt as deterministic, coordinate-locked functional UI layers:

- primary CTA top/bottom: `0.0 deg`
- secondary CTA top/bottom: `0.0 deg`
- warning CTA top/bottom: `0.0 deg`

This solves the hard failure from v0.91 and v0.92: text-bearing functional rows are no longer controlled by image-model perspective.

## What This Proves

- The correct production path is **not** full-screen text-baked image generation.
- Image generation can still provide mood, paper, low-poly thumbnails, stickers, backing sheets, shadows, and decorative objects.
- CTA label plates, text slots, button hit rects, status rows, and other dynamic UI must be rebuilt as orthogonal runtime / atlas layers.
- Geometry QA can now be exact because the functional boxes are generated from coordinates, not inferred from a painted perspective image.

## Remaining Visual Issues

- The rebuilt CTA layer is still too mechanical compared with the benchmark; it needs a proper WMW component atlas pass.
- Typography is readable and inside the frames, but final font weight, color, and edge softness still need a typography/component pass.
- The row separators and icon boxes are proof-level. A final asset should use the v0.89 carrier contract and WMW paper/material atlas more faithfully.
- Only the right CTA area was converted. Left cards, bottom receipts, right header lanes, stamp slots, and title/status lanes still need the same layered treatment.

## Next Gate

Before another user-facing full-screen candidate:

1. Convert all text-bearing functional areas to the same layered method.
2. Keep no-text imagegen art only under/around those layers.
3. Run geometry QA on at least right CTA, left card meta, bottom receipts, and right header lanes.
4. Then run style QA: paper token, low-poly planes, icon hand-drawn quality, typography hierarchy, and WMW color contract.
