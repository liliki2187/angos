# World Map WMW Pseudo No-Text Runtime Fill v0.3 Review

Date: 2026-07-06

## Artifact Type

`runtime text fill proof / pseudo no-text shell / not production atlas`

This pass uses the v0.2 semantic contract to fill real Chinese runtime text back into the benchmark-like world map shell.

## Output Files

- Preview: `docs/screenshots/2026-06-24-world-map-benchmark-landing/274-world-map-wmw-v0-3-pseudo-no-text-runtime-fill-preview.png`
- QA overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/275-world-map-wmw-v0-3-pseudo-no-text-runtime-fill-qa.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/276-world-map-wmw-v0-3-pseudo-no-text-runtime-fill-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/277-world-map-wmw-v0-3-pseudo-no-text-runtime-fill-manifest.json`

## Result

**Downgraded after user review: text-layer fit passes, but the functional art shell fails. This is not a production pass.**

Automated fit summary:

- Text items checked: 22
- Fit issues: 0
- Fit pass: true

Important correction: this automated fit only proves that runtime text fits inside authored rectangles. It does **not** prove that the underlying bitmap frame is orthogonal. User review identified that the right dossier header and CTA shells still have visible slant / perspective while the runtime text layer is straight. That mismatch fails the "functional components must be orthogonal" rule.

## What This Proves

- Runtime Chinese text can be rendered into the v0.2 `ink_safe_rect` boxes without overflow.
- CTA rows keep separate visual module, text plate, ink safe, right glyph, and hit rect layers.
- Left cards can hold title + status/meta without reintroducing the earlier top/bottom drift.
- Bottom receipts can hold title + value while preserving the progress-strip area.
- Font fallback is now explicit: Chinese strings are encoded with Unicode escapes and rendered through Microsoft YaHei / SimHei / NotoSansSC fallback. Question-mark or tofu fallback is not allowed.

## What This Does Not Prove

- The pseudo no-text fill is not final art. It is a local plate-fill simulation over a text-baked benchmark screenshot.
- Paper texture, edge cleanup, polygonal tone blocks, and true no-text plate quality still need art generation or painting.
- This pass tests current representative text, not the longest possible future strings.
- It does not prove that the visual shell itself is straight. v0.3 used a benchmark-like bitmap shell whose functional frames still contain imagegen perspective / slant.

## User Review Failure - Functional Art Shell Slant

The core problem is not the top runtime text layer. The runtime text is straight, but the paper header, CTA rows, and some label plates underneath are not straight enough to serve as functional UI carriers.

This creates a visual contradiction:

- Runtime layer: orthogonal and readable.
- Art shell: slightly tilted / perspective-warped.
- Result: the player sees the text floating over a misaligned physical frame.

Therefore v0.3 must not be used as a no-text atlas basis.

## Notes From This Pass

- The first attempt rendered Chinese as question marks due to command-pipe encoding loss.
- The second attempt rendered tofu boxes because the bold font chain selected a font without the needed Chinese glyphs.
- The final pass fixes both by using Unicode-escaped strings and a validated CJK fallback chain.
- Right header residual baked text required a slightly larger pseudo cleanup area; final no-text art should not rely on this workaround.
- The deeper miss was validating authored rectangles rather than validating the actual bitmap edge geometry of each functional carrier.

## Loop Log - Functional Art Shell Orthogonality Failure

- Trigger source: user highlighted that the top text layer is straight while the underlying functional art frame is visibly slanted.
- Original issue: v0.3 treated text fit and authored rectangle geometry as enough to continue.
- Failure attribution: I reused a benchmark-like full bitmap shell as if it were an atlas-ready UI shell. The benchmark collage style contains perspective and hand-placed paper/card slant, which is acceptable for decoration but not for functional carriers. The QA script only checked `ink_safe_rect` nesting and text overflow, not the real pixel edges of the frame.
- Current handling: v0.3 is downgraded. It is only evidence that runtime text can fit inside the proposed rectangles; it is not evidence that the visual resource is usable.
- Recurrence protection: every functional component now needs two passes before atlas work: `text_geometry_pass` and `art_shell_geometry_pass`. `art_shell_geometry_pass` must inspect the visible carrier edges themselves: header plates, CTA rows, label plates, receipt fields, and action panels must be 0-degree orthogonal. Decorative paper sheets, clips, tape, and background pages may tilt, but no text-bearing or click-bearing surface may tilt.
- Whether captured: captured here. The next artifact must be an orthogonal no-text shell proof, not another runtime text refill over the slanted shell.

## Next Gate

1. Produce an orthogonal no-text shell proof for the right dossier header and three CTA rows first.
2. The shell proof must preserve benchmark color / low-poly paper texture, but rebuild functional carrier edges as 0-degree surfaces.
3. Run an art-shell geometry QA crop before any text refill.
4. Reapply the v0.2 manifest and v0.3 runtime text fill only after the art shell geometry passes.
5. Then run longest-string and multi-state stress tests.
6. Only after those pass, slice atlas and integrate in Godot.
