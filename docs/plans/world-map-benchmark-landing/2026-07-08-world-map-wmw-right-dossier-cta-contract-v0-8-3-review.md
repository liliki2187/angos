# WMW Right Dossier + CTA Contract v0.8.3 Review

Date: 2026-07-08

## Artifact Type

`component_class_contract_candidate / right_dossier_page / right_action_lane / full-screen QA / not final art / not atlas`

This pass locks the right selected-region paper and its three CTA rows before no-text clean sprite work.

## Output Files

- Source measurement audit: `docs/screenshots/2026-06-24-world-map-benchmark-landing/359-world-map-wmw-v0-8-3-right-dossier-cta-source-audit.png`
- Contract candidate board: `docs/screenshots/2026-06-24-world-map-benchmark-landing/360-world-map-wmw-v0-8-3-right-dossier-cta-contract.png`
- Full-screen QA reinsert: `docs/screenshots/2026-06-24-world-map-benchmark-landing/361-world-map-wmw-v0-8-3-right-dossier-cta-reinsert-qa.png`
- 100% crops: `docs/screenshots/2026-06-24-world-map-benchmark-landing/362-world-map-wmw-v0-8-3-right-dossier-cta-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/363-world-map-wmw-v0-8-3-right-dossier-cta-manifest.json`
- Generator script: `tmp/wmw_v083_right_dossier_cta_contract.py`

## Source Measurement Result

The source reference is visually close, but not production-exact.

| Source object | Measurement |
| --- | ---: |
| `right_dossier_page` | `317 x 513` |
| CTA row 1 | `283 x 48` |
| CTA row 2 | `282 x 47` |
| CTA row 3 | `282 x 49` |

This means the current art reference can guide style and approximate placement, but production must normalize the right-side components into exact classes.

## Contract Candidate

Recommended classes:

| Class | Value |
| --- | --- |
| `right_dossier_page` | `320 x 520` |
| `right_action_lane` | `284 x 50` |
| CTA row gap | `5 px` |
| `photo_slot` | `276 x 176` |
| `title_slot` | `160 x 34` |
| `status_stamp` | `58 x 58` |
| CTA `left_icon_zone` | `34 x 34` |
| CTA `label_plate` | `170 x 32` |
| CTA `right_action_badge` | `42 x 40` |
| CTA `hit_rect` | full `284 x 50` |

## v0.8.4 Text Stress Note

The `320 x 520` dossier and `284 x 50` CTA contract passes normal and stress text-capacity checks in v0.8.4. This approves capacity only; final typography, final font choice, and final art texture still need later review.

## What Is Validated

- The right-side page can be normalized to a `320 x 520` component without breaking the full-screen composition.
- Three CTA rows can share one `284 x 50` class.
- Green / blue / red CTA rows can differ by skin and icon, not geometry.
- The right action badge remains fixed across CTA states.
- The page, photo, header, stamp, meta area, CTA stack, CTA label plate, and CTA hit rect all remain square-on.

## What Is Not Validated

- Final art quality.
- Final WMW color / texture matching.
- Final Chinese typography and long-string stress.
- Full state matrix including hover / pressed / disabled.
- No-text source sprite quality.
- Godot runtime assembly.

## One-Vote Fails

The right-side contract fails if:

- CTA rows use different heights by state;
- green / blue / red rows shift the right button badge;
- the warning row narrows its label plate to accommodate art;
- the right paper tilts while runtime text remains horizontal;
- decorative tabs, clip, back pages, or shadow move content rects;
- photo slot ratio changes without re-authoring the image content;
- a row looks good as art but no longer matches `284 x 50`.

## Production Decision

Use the source reference to preserve WMW paper / low-poly / dossier language, but use the contract values above for production.

The page and CTA rows should proceed as:

1. `right_dossier_page = 320 x 520`
2. `right_action_lane = 284 x 50`
3. three CTA states share identical slots
4. decoration can vary outside functional slots
5. no dynamic text is baked into the no-text asset

## Loop Log - Right-Side Near-Uniform Source Is Still Not a Contract

- Trigger source: Continuing the assetization route after the left-card reinsert proof; the next highest-risk component is the right selected-region paper and its CTA stack.
- Original issue: The source art's CTA rows are close enough by eye that they can look uniform, but exact measurement shows `283x48 / 282x47 / 282x49`. If accepted directly, runtime text and hit rects may drift by state.
- Failure attribution: Previous iterations repeatedly treated "visually close" as "production-compatible", which caused later text, hit rect, and art-shell alignment failures.
- Current handling: v0.8.3 normalizes the page and CTA rows into exact classes, then overlays them back onto the full screen.
- Recurrence protection: Any component family that repeats in a UI must pass exact same-class measurement, even when the source art looks visually consistent.
- Captured: Yes. This review records the right-side class contract and the broader production chain now includes a full-screen reinsert gate before freezing major class contracts.

## Next Gate

After user review:

1. Accept or adjust `right_dossier_page = 320 x 520`.
2. Accept or adjust `right_action_lane = 284 x 50`.
3. Run long-string text stress for:
   - title;
   - status stamp;
   - meta line;
   - three CTA labels;
   - disabled / blocked reason.
4. Produce no-text clean sprite brief for right-side components.
