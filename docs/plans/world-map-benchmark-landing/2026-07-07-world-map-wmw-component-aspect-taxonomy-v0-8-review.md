# WMW World Map Component Aspect Taxonomy v0.8 Review

Date: 2026-07-07

## Artifact Type

`component_aspect_taxonomy / upstream_classification / not final class contract / not sprite atlas / not runtime proof`

This pass answers one upstream question only: **what shape families the world-map UI actually uses before we rebuild assets.**

It does not approve final UI art, does not approve text fitting, and does not provide slice-ready sprites.

## Output Files

- Taxonomy overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/345-world-map-wmw-v0-8-component-aspect-taxonomy-overlay.png`
- Taxonomy matrix: `docs/screenshots/2026-06-24-world-map-benchmark-landing/346-world-map-wmw-v0-8-component-aspect-taxonomy-matrix.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/347-world-map-wmw-v0-8-component-aspect-taxonomy-manifest.json`
- Generator script: `tmp/wmw_v08_component_aspect_taxonomy.py`
- Source reference: `.codex-remote-attachments/019ef3f7-be2f-70d3-ae57-7df7fa181048/285fb7d4-37f0-4a98-86f4-c1652013a1d1/1-Photo-1.jpg`

## Result

**v0.8 is ready for user review as an upstream taxonomy, but it is not a production asset contract.**

The important correction is that the accepted world-map reference is not built from one square card component. Its main carriers are different rectangular families:

| Class | Role | Approx ratio | Square allowed | Production implication |
| --- | --- | ---: | --- | --- |
| `region_list_card` | left-side region summary | `1.20-1.35` | no | compact landscape card, not square tile |
| `region_photo_slot` | image inside region card | `2.3-3.4` | no | preserve image-slot contract, no squeeze |
| `map_panel` | central world map board | `1.25-1.35` | no | large square-on interaction board |
| `detail_dossier_page` | right selected-region paper | `0.60-0.70` | no | vertical dossier container |
| `right_action_lane` | CTA rows | `5.6-6.2` | no | long horizontal button lane |
| `bottom_receipt_card` | bottom status receipt | `1.75-1.90` | no | wide receipt card, not region-card geometry |
| `icon_badge` | sticker / badge / glyph | `0.9-1.15` | yes | square/circle assets only live here |
| `top_status_strip` | global HUD strip | `20+` | no | low-density horizontal strip |

## Key Decision

Do not use square or near-square imagegen cards as the main production source for the world-map UI.

Square assets are valid for `icon_badge`, stickers, glyph plates, and symbol-only affordances. They must not define the geometry of region cards, right-side CTA lanes, bottom receipts, the dossier page, or the map panel.

## Assetization Route Status

| Ring | Current formal artifact | Status | Blocking issue |
| --- | --- | --- | --- |
| 1. Style benchmark understanding | WMW branch analysis and accepted visual direction notes | usable | Style is understood, but style understanding is not a component contract |
| 2. Page structure / responsibilities | Reference screenshot exists | incomplete | Full formal structure spec for left / center / right / bottom is not locked |
| 3. Real-content filled mock | Several failed iterations | not passed | Typography, slots, and text/resource fit need class contracts first |
| 4. Component aspect taxonomy | This v0.8 pass | pending user review | Current key gate |
| 5. Class geometry contracts | v0.6.9 has useful uniformity rule only | must rewrite | The aspect and slot family are wrong for production |
| 6. No-text clean sprite brief | v0.6.8 / v0.6.9 | blocked | Built on wrong upstream ratios, must be restarted |
| 7. Imagegen candidate sheet | v0.7.1 | visual reference only | Cannot slice directly; class sizes are not validated |
| 8. Atlas / manifest | none | not started | Requires class contracts and clean sprites |
| 9. Runtime refill proof | v0.6.5 / v0.6.7 | temporary proof | Proves assembly method, not final resources |
| 10. Godot screenshot pass | none | not complete | Wait for atlas / manifest / runtime states |

## What This Blocks

- Blocks v0.6.9 left-region-card aspect from production use.
- Keeps only one useful v0.6.9 lesson: same `component_class` states must share geometry.
- Blocks v0.7.1 imagegen sheet from direct sprite slicing.
- Requires rewriting clean-sprite briefs after rectangular class ratios are confirmed.

## Loop Log - Missing Aspect Taxonomy Gate

- Trigger source: User pointed out that the current component set had become mostly square, while the accepted world-map reference clearly uses long rectangular cards, strips, receipts, and a vertical dossier.
- Original issue: The request was to correct benchmark components and preserve the reference's working UI grammar. My intermediate assetization path over-focused on clean component sheets and same-class uniformity before first classifying the source reference's real aspect families.
- Failure attribution: I treated "consistent component class" as enough. That was incomplete: consistency only works after the correct class family is chosen. A consistent square card is still wrong if the benchmark needs a compact landscape region card, long CTA lane, or wide receipt.
- Current handling: v0.8 inserts a dedicated `component_aspect_taxonomy` gate before class contracts, clean-sprite briefs, imagegen packs, atlas, or runtime integration.
- Recurrence protection: Any future assetized UI task must first classify the benchmark into role-based shape families, then decide which classes can be square. Symbol assets may be square; information carriers default to rectangular unless the source and information capacity prove otherwise.
- Captured: Yes. This review records the gate and `docs/onboarding/assetized-ui-production-chain.md` adds the rule.

## Next Gate

If v0.8 taxonomy is accepted, produce `v0.8.1 component class contracts`:

- exact `class_id`
- export size
- target ratio
- 9-slice / stretch policy
- `photo_slot`
- `label_plate`
- `content_rects`
- `hit_rects`
- icon禁入区
- state matrix
- long-text stress values

Do not proceed to clean sprites, imagegen atlas sheets, Godot runtime integration, or final screenshot replacement until this contract exists.
