# WMW Left Region Card Class Contract v0.8.1 Review

Date: 2026-07-07

## Artifact Type

`component_class_contract_candidate / left_region_card / geometry lock / not final art / not atlas`

This pass answers the user's concern: whether the left-side cards in the art draft have consistent width, height, image slot, and functional regions.

## Output Files

- Current source uniformity audit: `docs/screenshots/2026-06-24-world-map-benchmark-landing/348-world-map-wmw-v0-8-1-left-card-current-uniformity-audit.png`
- Class contract candidate: `docs/screenshots/2026-06-24-world-map-benchmark-landing/349-world-map-wmw-v0-8-1-left-card-class-contract.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/350-world-map-wmw-v0-8-1-left-card-class-contract-manifest.json`
- Generator script: `tmp/wmw_v081_left_region_card_contract.py`

## Source Measurement Result

The current art reference does **not** have consistent left-card geometry.

| State | Source card size | Source card ratio | Source photo size | Source photo ratio | Production status |
| --- | ---: | ---: | ---: | ---: | --- |
| selected | `202 x 168` | `1.20` | `175 x 73` | `2.40` | fail: geometry drift |
| available | `203 x 170` | `1.19` | `174 x 75` | `2.32` | fail: geometry drift |
| warning | `203 x 149` | `1.36` | `174 x 53` | `3.28` | fail: geometry drift |
| locked | `204 x 149` | `1.37` | `174 x 51` | `3.41` | fail: geometry drift |

The left-card source is therefore a **visual reference**, not a slice-ready same-class production source.

## v0.8.2 Revision Note

The `204 x 150` contract below was the first measurable candidate, not the recommended final size. Full-screen reinsert testing in v0.8.2 recommends revising the next `left_region_card` contract candidate to `204 x 160` before clean-sprite brief work.

## Contract Candidate

`class_id`: `left_region_card`

All states share the same production geometry:

| Field | Value |
| --- | --- |
| `export_size` | `204 x 150` at 1280x720 reference scale |
| `transparent_bleed` | `6 px`, fixed and not counted as layout size |
| `photo_slot` | `174 x 58`, same in all states |
| `label_plate` | `114 x 32`, same in all states |
| `meta_line` | `96 x 10`, same in all states |
| `icon_badge` | `32 x 32`, same in all states |
| `action_badge` | `38 x 38`, same in all states |
| `hit_rect` | full `204 x 150` card bounds |

State differences may only change:

- color skin
- low-poly facet tint
- lock / warning / target / check glyph
- selected glow
- paper shadow opacity inside fixed bleed

State differences may not change:

- export width or height
- photo slot size or y position
- label plate size or y position
- action badge position
- hit rect
- stack spacing contract
- photo aspect handling

## One-Vote Fails

The left-card class fails if:

- selected state becomes taller or wider than other region cards;
- warning / locked state uses a shorter photo slot;
- a photo is squeezed to fit a new slot;
- paper shadow, lock, warning triangle, check mark, or glow expands the runtime export box;
- an AI-generated state has a good appearance but changes functional geometry.

## Production Decision

Use the accepted art draft to preserve style language, not source dimensions.

For production, `selected / available / warning / locked` must be skins of one `left_region_card` component class. If design later wants a larger selected card, it must be declared as a separate class such as `left_region_card_expanded`, and the whole left-list layout must be redesigned around that class instead of mixing it into the same state matrix.

## Loop Log - Art Beauty Versus Component Uniformity

- Trigger source: User asked whether the left-side art components have identical width and height, and stated they do not want art polish to create inconsistent components that later fail during functional implementation.
- Original issue: Earlier iterations let source-art variation and imagegen composition influence component dimensions. This risked turning visual differences into runtime geometry differences.
- Failure attribution: I had separated "same-class state uniformity" as a rule, but had not yet applied it directly to the accepted left-side card source measurements.
- Current handling: v0.8.1 measures the source cards, marks the current art as non-uniform, and proposes a fixed `left_region_card` production contract.
- Recurrence protection: Any future card-class asset must compare all states against one `export_size`, one `photo_slot`, one `label_plate`, one `action_badge`, and one `hit_rect` before entering clean sprite brief or atlas production.
- Captured: Yes. This review records the left-card-specific rule and uses the broader `component_class_uniformity_gate` already added to `docs/onboarding/assetized-ui-production-chain.md`.

## Next Gate

After user review:

1. Decide whether `204 x 150` is the accepted production size at 1280x720 reference scale.
2. If accepted, produce v0.8.2 clean-sprite brief for `left_region_card` using this contract.
3. If not accepted, adjust the class size once, then rerun the same uniformity audit.
4. Do not create per-state sprites until the class contract is approved.
