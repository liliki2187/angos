# WMW World Map v0.58 Color Contract

Status: temporary color correction contract for the next imagegen pass. This is a sampled analysis aid, not a global art source.

## Source Images

- Benchmark reference 1: `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- Benchmark reference 2: `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- Current user-feedback image: `C:/Users/GZFANG~1/AppData/Local/Temp/codex-clipboard-b7276f30-40dc-4746-9ec5-674da47cc0df.png`

## Key Samples

| token | benchmark / target sample | current sample | reading |
| --- | --- | --- | --- |
| clean dark board | `#152429`, also current map ocean `#091A2B` is acceptable | top strip `#171E1E` | dark base is not the main problem; avoid turning it gray or dusty |
| paper body | target range `#BEB5A6` to `#C9C0B0`, with mid paper around `#AFA591` | right paper `#B1A390`, gray bar `#CEBEAA` | paper is too gray-beige in large areas, and gray placeholder bars are too dominant |
| olive / selected green | benchmark swatches `#6E8047`, `#798545`, `#666D3C` | selected land `#4C5948`, CTA green frame `#817F6B` | current green is too low-saturation and too beige/gray, causing muddy military/cardboard feel |
| teal / blue-green | benchmark swatches around `#2F4A49`, `#3E515F` | current blue/teal components often collapse toward gray | restore cool teal identity; do not let teal become neutral gray |
| rusty warning red | target `#6D462D` to `#8A4E32` | current red ranges between muted brown and red-brown | keep rusty red-orange, but separate it from paper brown with clearer hue contrast |
| world land gray | current land `#3A4145` | n/a | gray landmass area is visually large; avoid letting it dominate the whole screen as a mid-gray blanket |

## v0.58 Prompt Targets

- Do not globally brighten or globally darken.
- Keep the dark navy board clean and deep, close to `#091A2B` / `#152429`, not smoky gray.
- Paper should read as clean warm ivory: high `#C2BAAC`, mid `#B8AD9A`, shadow `#9C927F`; avoid broad dull gray bars and muddy beige fields.
- Selected olive and green UI frames should move toward `#63713A` / `#666D3C` / `#6E8047`, not `#4C5948` or `#817F6B`.
- Teal-blue UI frames should move toward `#2F4A49` / `#3E515F`, not neutral gray.
- Warning rust should stay in `#6D462D` - `#8A4E32`, with less brown-paper blending.
- Reduce gray placeholder bars, perforation dots, and coupon/ticket literal details.
- Preserve hard orthogonal functional faces and no fold / tear / crease marks in functional components.

## Failure Boundaries

- Fail if the screen reads as gray-beige tickets on a dark UI rather than modern weekly editorial paper collage.
- Fail if green UI areas sample near low-saturation gray-green (`S < 0.25`) or beige olive.
- Fail if teal components become neutral gray.
- Fail if paper dominates the screen with gray placeholder strips.
- Fail if correcting color reintroduces slanted functional components, folded-corner scars, dense GIS mesh, or old archive grime.

## Candidate Resampling

### v0.58

- Image: `docs/screenshots/2026-06-24-world-map-benchmark-landing/123-world-map-wmw-color-contract-v0-58.png`
- Result: direction improved but not enough. Paper sampled `#B5A590`, CTA green `#6A684C`, teal frame `#505F5E`, selected land `#3A462B`.
- Reading: gray / muddy feeling was reduced, but green and teal still retained too much beige-gray; selected land was still dark and not folder-olive enough.

### v0.59

- Image: `docs/screenshots/2026-06-24-world-map-benchmark-landing/124-world-map-wmw-color-contract-v0-59.png`
- Resampled tokens:
  - dark map ocean: `#001524`, acceptable deep navy.
  - right paper: `#BAAC95`, close to clean ivory target and less gray than current feedback image.
  - gray/header bar: `#A39681`, less bright and less dead-gray than previous gray strips.
  - CTA green frame: `#7D8055`, cleaner and more saturated than v0.58, but slightly yellow-bright versus ideal `#63713A` / `#666D3C`.
  - CTA blue frame: `#536F71`, improved separation from gray, still slightly lighter than ideal `#2F4A49` / `#3E515F`.
  - CTA red frame: `#91684F`, clearer rust, slightly bright versus ideal upper bound `#8A4E32`.
  - selected land: `#3A492A`, saturated enough but still dark; should mix more `#5B6338` / `#63713A` planes if promoted.
- Reading: v0.59 fixes the gray/muddy direction better than v0.58, but introduces a new risk of looking too clean / too atlas-like and the world map low-poly facets remain somewhat regular.

## Texture Retention Addendum For v0.60

User feedback after v0.59: the gray / muddy color issue improved, but valuable surface texture and material character from the previous image were washed out.

This should not be solved by returning to dirty archive texture. Split texture into allowed and forbidden categories:

Allowed benchmark texture:

- broad low-poly value blocks on card shells, CTA bodies, bottom receipts, and dossier paper bodies;
- subtle printed-paper tooth and mottling below text readability threshold;
- slight ink / screen-print unevenness on colored frames;
- bevel-like cut-paper thickness on outer frames and icon wells;
- dark board grid, faint blueprint lines, and edge wear;
- controlled shadow layering between stacked paper objects;
- low-poly scene/image texture inside thumbnails and the dossier snapshot.

Forbidden texture:

- visible fold / tear / crease / wrinkle lines across functional components;
- bright diagonal folded-corner scars;
- old archive grime, tea stains, parchment yellow, dirty newspaper;
- dense barcode / perforation / tiny-hole clutter;
- photographic grain or random noise over text slots;
- full-screen gray filter or muddy beige wash.

v0.60 should preserve the v0.59 color correction direction while restoring allowed benchmark texture. It should not become a smooth vector atlas, flat software UI, or sterile clean mock.

### v0.60

- Image: `docs/screenshots/2026-06-24-world-map-benchmark-landing/125-world-map-wmw-texture-retention-v0-60.png`
- Result: texture returned, but too much dirt / old-paper tendency returned with it.
- Resampled tokens:
  - right paper: `#AF9C82`, dirtier and darker than v0.59 `#BAAC95`.
  - gray/header bar: `#948268`, too brown / old-paper.
  - CTA green frame: `#6B6546`, acceptable saturation but beige-yellow.
  - CTA blue frame: `#515A55`, collapsed toward low-saturation gray-green.
  - CTA red frame: `#835A40`, within rust family.
  - selected land: `#3F452D`, dark olive.
- Reading: useful as a boundary sample for "texture restored but paper becomes old / dirty".

### v0.61

- Image: `docs/screenshots/2026-06-24-world-map-benchmark-landing/126-world-map-wmw-balanced-texture-v0-61.png`
- Result: better balance than v0.60. Paper texture and component value blocks return, while old-paper dirt is reduced. Still not final.
- Resampled tokens:
  - right paper: `#B6A48B`, cleaner than v0.60, still darker / warmer than v0.59.
  - gray/header bar: `#9B8971`, improved versus v0.60 but still brown-gray.
  - CTA green frame: `#6B6745`, textured and saturated, still slightly dark / yellow.
  - CTA blue frame: `#505B55`, still too neutral; teal identity needs another pass if v0.61 is used as base.
  - CTA red frame: `#7E523D`, good controlled rust.
  - selected land: `#3B432D`, dark olive, acceptable as shadow plane but needs some lighter olive planes.
- Reading: v0.61 is the current best compromise for "color no longer gray/muddy + texture not erased", but the teal/blue token and selected land need correction before promotion.

### v0.62

- Image: `docs/screenshots/2026-06-24-world-map-benchmark-landing/127-world-map-wmw-benchmark-diff-correction-v0-62.png`
- Intent: correct benchmark differences called out after v0.61: restore clearer green / teal identity, keep clean paper, reduce coupon feeling, and push map planes larger / more editorial.
- Resampled tokens:
  - right paper: `#B1A18A`, acceptable but slightly darker / warmer than v0.59.
  - gray/header bar: `#BAA78C`, less dead-gray, but still a large form-like strip.
  - CTA green frame: `#857D5B`, too yellow / beige versus target olive.
  - CTA blue frame: `#495757`, still too low-saturation and gray versus target teal.
  - CTA red frame: `#88573E`, good controlled rust.
  - selected land: `#434727`, saturated but dark and yellow-olive.
  - map gray land: `#454647`, very low saturation; the landmass still reads as a broad gray UI map rather than a designed editorial object.
- Reading: v0.62 improves overall cleanliness and reduces coupon/ticket literalism. It still misses the benchmark mainly in teal identity, olive hue, large-plane map treatment, and dossier/status-card editorial looseness.
