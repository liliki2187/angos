# Prompt Planning

Use this file when turning a user request into a production-ready image prompt.

## Core Prompt Shape

Build prompts in this order:

1. Asset identity
2. Intended game use
3. Subject description
4. Framing / camera / composition
5. Materials / lighting / rendering language
6. Background requirement
7. Reference-image role if present
8. Negative constraints

## Common Game Asset Defaults

| Asset Type | Default Background | Typical Shape | Prompt Additions |
| --- | --- | --- | --- |
| `icon` | transparent | square | centered object, clean silhouette, readable at small size |
| `item` | transparent | square | isolated prop, production-ready asset, readable at small size |
| `prop` | transparent | square or `3:2` | object-first composition, no scene clutter |
| `sprite` | transparent | square or portrait | 2D game sprite readability, clean outline, animation-friendly silhouette |
| `vfx` | transparent | square | emissive effect only, no mockup presentation |
| `decal` | transparent | square | flat readable graphic treatment, edge-safe cutout |
| `texture` | opaque | square | surface-first, material clarity, avoid scene composition |
| `tileable-texture` | opaque | square | seamless tiling, edge continuity, even coverage |
| `portrait` | opaque | `3:4` or `4:5` | bust or waist-up framing, facial readability |
| `character-concept` | opaque | `2:3`, `3:4`, or `4:5` | costume read, silhouette read, prop callouts only if asked |
| `creature-concept` | opaque | `2:3` or `16:9` | anatomy clarity, material hierarchy, threat read |
| `environment-concept` | opaque | `16:9` or `21:9` | world-building, depth layers, lighting story |
| `background` | opaque | `16:9` | gameplay-safe composition, horizon and focal structure |
| `key-art` | opaque | `3:4`, `4:5`, or `16:9` | hero composition, saleable mood, strong focal hierarchy |
| `poster` | opaque | `3:4` or `4:5` | title space planning, graphic hierarchy, publishable layout |
| `ui-screen` | opaque | `16:9` | full-screen interface mockup, panel hierarchy, interaction readability |
| `ui-banner` | opaque | `4:1`, `8:1`, or `16:9` | controlled empty space for UI overlay |
| `logo-mark` | transparent by default | square | vector-like clarity, bold read, minimal clutter |
| `card-art` | opaque | `3:4` | frame-aware focal placement |
| `isometric-asset` | transparent or opaque | square | clean volume read, consistent isometric angle |

## Negative Constraints

Always include a shared negative block unless the user explicitly asks otherwise.

Shared negative terms:

- watermark
- signature
- artist name
- copyright stamp
- frame border
- presentation mockup
- UI chrome
- drop shadow
- cropped subject
- cut off limbs
- duplicate objects
- extra fingers
- broken anatomy
- unreadable text
- muddy details
- jpeg artifacts
- oversaturated colors
- noisy background
- inconsistent lighting

Asset-specific negative additions:

- transparent assets:
  - background scene
  - floor shadow
  - environmental clutter
  - vignette
- textures:
  - seams
  - directional lighting hotspots
  - perspective scene elements
- UI banners / posters:
  - accidental logos
  - misspelled typography
  - random stickers
- portraits / characters:
  - asymmetrical eyes
  - malformed hands
  - fused accessories

Do not send negative constraints as a separate provider field. Fold them into the final prompt as a "Do not include" or "Avoid" clause.

## Reference Image Use

If reference images exist:

- Explain what each reference controls:
  - composition
  - costume
  - palette
  - material
  - silhouette
  - editing target
- Keep that intent in the metadata JSON.
- Do not say "copy this exactly" unless the user explicitly wants a faithful derivative and the request is legally safe.

## Quantity Heuristics

If the user does not specify `count`, use:

- `1` for most production assets
- `2` for look exploration, icon exploration, or character exploration
- `4` only when the user clearly wants options or variant exploration

Avoid defaulting to high counts because image generation is expensive and slower than text work.

## Transparency Heuristics

If the user does not specify background:

- Infer `transparent` for:
  - icon
  - item
  - prop
  - sprite
  - vfx
  - decal
  - logo-mark
- Infer `opaque` for:
  - texture
  - portrait
  - character-concept
  - creature-concept
  - environment-concept
  - background
  - key-art
  - poster
  - ui-screen
  - ui-banner
  - card-art

## Metadata Expectations

Record these fields in every sidecar JSON:

- original user request
- normalized asset type
- inferred or explicit background mode
- chosen model and model-selection reason
- requested size fields and normalized size fields
- count
- final prompt
- negative constraints
- reference-image list and roles
- warnings, assumptions, and fallbacks
- output paths
- response id, model, usage, and assistant text when available
