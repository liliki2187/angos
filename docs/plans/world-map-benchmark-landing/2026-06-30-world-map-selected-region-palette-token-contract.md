# World Map Selected Region Palette Token Contract

Status: branch experiment, not formal project-wide art source.

## Purpose

This contract records the local palette-token correction for the selected region in the world-map benchmark branch.

The current generated screen candidate is:

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/95-world-map-imagegen-color-recorrected-v0-51.png`

The local implementation proof is:

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/103-world-map-v051-local-olive-grade-proof-v2.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/104-world-map-v051-local-olive-proof-v2-color-check.png`

## Rule

Do not continue full-screen regeneration just to fix the selected-region yellow-green cast.

Use v0.51 as the generated screen candidate and fix selected-region yellow-green through local palette tokens or a local LUT pass.

## Token Family

Selected region olive:

- `selected_region_olive`: `#606548`
- `selected_region_olive_dark`: `#5B5E3E`
- `selected_region_olive_light`: `#807E50`

Use these as a low-chroma moss-olive family. They should replace the previous gold/yellow-green selection language while preserving the same perceived lightness.

## Acceptance

For a local correction proof:

- `global L` must not drop more than `3` from v0.51.
- `median L` should remain close to v0.51.
- `dark %` should remain close to v0.51.
- High-saturation `yellowgreen %` should decrease from v0.51.
- The selected region must remain recognizable as the active region.
- The correction must not introduce extra grunge, scratches, halos, or route lines.

Proof v2 result:

- `global L`: preserved at about `66.4`.
- `median L`: preserved at about `47.5`.
- high-saturation `yellowgreen %`: reduced from about `2.8` to near `0.0`.
- changed pixels: about `7.9%`, confirming this is a local correction, not a full-screen retone.

## Implementation Guidance

Runtime-drawn selected-state overlays should use the token family directly:

- selection halo / corner brackets: `selected_region_olive_light`
- selected overlay wash: `selected_region_olive`
- deep selected material / shadow: `selected_region_olive_dark`

Texture-baked selected landmass colors should not be fixed by re-generating the full screen. Use one of:

- a no-text component asset pass with the selected landmass already in the token family
- a localized LUT / hue-saturation pass masked to the selected landmass
- a runtime overlay only if it does not read as a flat programmatic tint

## Non-Goals

- This contract does not approve the old v6g runtime preview as the new benchmark style.
- This contract does not replace v0.51 as the generated screen candidate.
- This contract does not authorize blanking text fields or increasing paper area to match old first-version metrics.
