# World Map WMW Benchmark Component Resource Contract v0.2

Date: 2026-07-03

## Status

`resource contract / benchmark shell alignment / not final art`

This contract answers the user's concern: v0.95's layered proof must not become the art source. The benchmark image defines the visual component shell; the runtime / functional layer defines only the orthogonal content, hit, and state rects.

## Artifacts

- Benchmark shell reference: `docs/screenshots/2026-06-24-world-map-benchmark-landing/258-world-map-wmw-benchmark-shell-reference-v0-1.png`
- Full overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/262-world-map-wmw-benchmark-component-resource-contract-v0-2-overlay.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/263-world-map-wmw-benchmark-component-resource-contract-v0-2-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/264-world-map-wmw-benchmark-component-resource-contract-v0-2.json`

## Core Rule

Do **not** slice v0.95 temporary proof as art.

Use this split:

| Layer | Source | Can slant? | Can carry dynamic text? |
| --- | --- | --- | --- |
| Visual shell | Benchmark-style no-text bitmap resource | outer edge may use cut corners / bevel / tabs; main functional face stays front-on | No |
| Decorative art | clips, tabs, paper edges, shadows, thumbnails, low-poly photo, backing pages | Yes, if it carries no function | No |
| Static glyph art | globe, warning, document, target, check, hand stickers | No for hit / state boxes; hand-drawn shape can be irregular inside rect | Usually no; state variants allowed |
| Runtime content | title, status, button label, receipt title/value, progress fill | No | Yes |
| Runtime interaction | hit rect, hover, pressed, disabled, selected | No | No text itself, but must align with content |

## Component Coverage

The v0.2 manifest covers 11 benchmark-aligned components:

| Component | Visual shell source | Runtime/function rects |
| --- | --- | --- |
| right_dossier_sheet | right paper dossier, photo frame, clip, backing tabs | title lane, status lane, photo caption, stamp slot |
| cta_primary | green benchmark CTA shell | left icon, label plate, right action icon, button hit rect |
| cta_secondary | teal benchmark CTA shell | left icon, label plate, right action icon, button hit rect |
| cta_warning | rust benchmark CTA shell | left icon, label plate, right action icon, button hit rect |
| left_na | selected North America region card shell | title/meta plate, global icon, state/action icon, card hit rect |
| left_eu | Europe available card shell | title/meta plate, global icon, state/action icon, card hit rect |
| left_af | Africa warning card shell | title plate, global icon, state/action icon, card hit rect |
| left_sa | South America locked card shell | title plate, global icon, lock/action icon, card hit rect |
| receipt_action | bottom action receipt shell | receipt title, value, progress bar |
| receipt_info | bottom intel receipt shell | receipt title, value, progress bar |
| receipt_redline | bottom redline receipt shell | receipt title, value, progress bar |

## Production Implication

The next resource pass should generate or paint **no-text benchmark shells**, not a new full-screen text-baked mock:

1. Produce no-text shells for the 11 components above, preserving the benchmark's bevel, low-poly planes, paper tone, icon character, and color modules.
2. Keep all dynamic text out of the bitmap.
3. Rebuild runtime text/status/hit rects from the manifest.
4. Run geometry QA against the runtime rects and 100% crop QA against each component.
5. Only after this, build a filled-state preview to check whether the real UI text and real resource shell still feel like the benchmark.

## Known Caveat

The current shell reference is a text-baked visual target, so it is not a cuttable production source. It is only used to define silhouette, density, material, and component proportion. A production atlas needs either a no-text regeneration/inpaint pass or a hand-cleaned no-text component atlas.
