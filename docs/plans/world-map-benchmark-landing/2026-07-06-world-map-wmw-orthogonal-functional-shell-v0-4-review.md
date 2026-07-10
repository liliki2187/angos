# WMW World Map Orthogonal Functional Shell v0.4 Review

Date: 2026-07-06

## Artifact Type

`art_shell_geometry_proof / no-text shell proof / not final art / not atlas`

This pass is a scoped proof for the right dossier header and three CTA rows. It answers one production question only: can the visible functional art shell be rebuilt as 0-degree orthogonal surfaces before runtime text is refilled?

## Output Files

- No-text shell proof: `docs/screenshots/2026-06-24-world-map-benchmark-landing/278-world-map-wmw-v0-4-orthogonal-no-text-shell-proof.png`
- Geometry QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/279-world-map-wmw-v0-4-orthogonal-shell-geometry-qa.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/280-world-map-wmw-v0-4-orthogonal-shell-crops.png`
- Runtime text refill preview: `docs/screenshots/2026-06-24-world-map-benchmark-landing/281-world-map-wmw-v0-4-orthogonal-shell-text-refill-preview.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/282-world-map-wmw-v0-4-orthogonal-shell-manifest.json`
- Generator script: `tmp/wmw_v04_orthogonal_shell.py`

## Result

Scoped pass for the right dossier header and CTA rows as a geometry proof.

- Functional shell surfaces checked: 17
- Scope: right title lane, right status lane, right stamp, photo caption lane, three CTA shells, three label plates, three action plates, three hit rects.
- All functional carrier rectangles in this proof are authored as axis-aligned surfaces.
- Runtime Chinese text is refilled only after the no-text shell is rebuilt.

This is not a final WMW art pass. The paper tone, low-poly block finesse, icon polish, atlas slicing, hover / pressed / disabled states, left cards, center map, and bottom receipts still need separate passes.

## Post-Review Cleanup - CTA Sharp Protrusions

User review identified sharp colored / dark protrusions on the left side of the CTA stack. These were not part of the intended component grammar.

Cause:

- The deterministic proof reused an older full-screen source underneath the rebuilt shells, leaving source-image remnants just outside the paper edge.
- Some low-poly facets near CTA rows were too sharp and read as arrowheads / protruding geometry rather than internal material blocks.

Fix:

- Cleared the non-functional strip outside the left paper edge of the CTA stack.
- Constrained low-poly facets inside the button carrier so they no longer read as functional arrowheads.

Production rule:

- Low-poly blocks may add material variation inside a functional carrier, but they must not create protruding tips, route arrows, false affordances, or shapes that extend beyond the declared `visual_module_rect`.

## v0.4.1 Correction - No Spike-Like Internal Facets

User review clarified that the problem was not only the clipped outer tip. The CTA component still contained spike-like triangular facets inside the carrier, especially near the label plate. Those shapes did not always exceed the declared geometry, but they still read as arrows / teeth / protruding UI geometry and no longer matched the earlier cleaner CTA component style.

Correction outputs:

- No-text shell proof: `docs/screenshots/2026-06-24-world-map-benchmark-landing/283-world-map-wmw-v0-4-1-clean-cta-no-spikes-shell-proof.png`
- Geometry QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/284-world-map-wmw-v0-4-1-clean-cta-geometry-qa.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/285-world-map-wmw-v0-4-1-clean-cta-crops.png`
- Runtime text refill preview: `docs/screenshots/2026-06-24-world-map-benchmark-landing/286-world-map-wmw-v0-4-1-clean-cta-text-refill-preview.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/287-world-map-wmw-v0-4-1-clean-cta-manifest.json`

v0.4.1 changes:

- Removed triangular CTA material facets.
- Replaced them with broad horizontal pressure bands and quiet rectangular value blocks.
- Replaced CTA label plate paper with a cleaner text-plate material that avoids triangular low-poly facets.

Loop Log addendum:

- Trigger source: user compared v0.4 CTA rows against the earlier cleaner UI component style and pointed out that spike-like shapes were still present.
- Original issue: I treated the problem as "outer protrusion / tip cleanup" instead of recognizing that internal spike-like low-poly facets also change component semantics.
- Failure attribution: I over-applied low-poly style language to a functional button carrier. The benchmark uses large calm facets, but not every facet shape is suitable inside a CTA. Pointed triangles near text read as arrows / teeth / false affordances.
- Current handling: v0.4.1 cleans CTA material language while preserving orthogonal shells and runtime text fit.
- Recurrence protection: Functional carriers now reject spike-like internal facets even when they remain inside the measured rect. Low-poly style in CTA / receipt / label plates must prefer horizontal bands, wide value planes and low-contrast blocks.
- Whether captured: Captured here and added to `docs/onboarding/ui-interaction-guidelines.md`.

## What This Fixes

- The earlier false pass where straight runtime text sat on top of a slanted bitmap button shell.
- The mismatch between text safe zones and visible art modules.
- The temptation to continue prompt-only full-screen image generation after repeated functional slant failures.

## What This Does Not Fix

- It does not make the whole world map production-ready.
- It does not prove left region cards, bottom receipts, map labels, or future dispatch UI are straight.
- It does not preserve final benchmark-level paper material by itself. The paper / button material must still go through the existing WMW paper material contract and color contract.
- It does not replace imagegen. It is a geometry lock / proof layer that future no-text generated or painted art must obey.

## Loop Log

- Trigger source: User pointed out that the top runtime text was straight, but the underlying functional art frames remained visibly slanted.
- Original issue: The previous pass checked text overflow and safe-zone rectangles, but treated those checks as if the UI component had passed.
- Failure attribution: I validated authored overlay boxes instead of validating the real visible bitmap shell. This let a straight text layer mask a slanted art carrier. I also kept using full-screen imagegen outputs as if they could be repaired by safe zones, when the carrier geometry itself was the failing layer.
- Current handling: v0.3 is downgraded. v0.4 rebuilds the right dossier header and CTA shells as explicit no-text, axis-aligned functional carriers first, then refills text.
- Recurrence protection: All future assetized UI components that carry text, state or clicks require both `text_geometry_pass` and `art_shell_geometry_pass`. QA reference lines must attach to the visible bitmap shell, not just to an ideal overlay rectangle.
- Whether captured: Captured in this review and added to `docs/onboarding/ui-interaction-guidelines.md` plus `docs/onboarding/assetized-ui-production-chain.md`.

## Next Gate

1. Extend the same art-shell geometry gate to the left region cards and bottom receipt cards.
2. Replace deterministic proof styling with a cleaner no-text art shell that follows the benchmark paper token and low-poly material contract.
3. Refill real content only after every text-bearing shell passes visual edge QA.
4. Build a component correction sheet from the passed shells, not from the earlier slanted full-screen bitmap.
5. Only after component shells pass, proceed to atlas slicing / Godot manifest / runtime state screenshots.
