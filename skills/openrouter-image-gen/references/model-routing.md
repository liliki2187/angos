# Model Routing

Use this file whenever you need to choose a model, normalize size parameters, or reject an invalid request.

## Supported Models

| Alias | Model ID | Use For | Notes |
| --- | --- | --- | --- |
| `gpt-5-image` | `openai/gpt-5-image` | Transparent PNG/WebP assets, clean cutout assets, precise isolated game objects | Required for transparent background in this skill |
| `nano-banana` | `google/gemini-2.5-flash-image` | Fast opaque generation, simple icons, props, portraits, basic concepts, lower composition complexity | Supports `image_config.aspect_ratio` |
| `nano-banana-2` | `google/gemini-3.1-flash-image-preview` | Opaque generation with more subjects, more references, more layout complexity, heavier text/logo demands, extended aspect ratios | Supports extended aspect ratios and `0.5K` |

## Hard Routing Rule

- `background=transparent` -> only `openai/gpt-5-image`
- `background=opaque` -> choose between `nano-banana` and `nano-banana-2`

## Complexity Heuristic For Opaque Images

Prefer `nano-banana` when the request is mostly one of these:

- single icon or item
- isolated prop
- single portrait
- simple environment mood frame
- quick exploration thumbnails

Prefer `nano-banana-2` when one or more of these apply:

- multi-subject composition
- complex scene storytelling
- poster / key art / marketing composition
- UI banners or hero banners
- text must render clearly in-image
- more than one reference image
- extended aspect ratios (`1:4`, `4:1`, `1:8`, `8:1`)
- the user explicitly asks for cleaner layout control or more faithful reference-driven edits

## Supported Count Range

This skill supports `count` values from `1` to `8`.

Generation count is orchestrated client-side as repeated single-image requests so the skill does not depend on provider-specific multi-image semantics.

## Transparent Request Validation

For `openai/gpt-5-image` in this skill:

- Allowed literal `resolution` values:
  - `1024x1024`
  - `1536x1024`
  - `1024x1536`
  - `auto`
- Allowed `background` values:
  - `transparent`
  - `opaque`
  - `auto`
- If `background=transparent`, the script forces:
  - `model=openai/gpt-5-image`
  - `output_format=png` unless the user explicitly asks for `webp`
- Reject non-square panoramic transparent requests that cannot map cleanly to the supported GPT Image sizes.

## Opaque Request Validation

For Gemini image models in this skill, prefer OpenRouter's documented `image_config` fields instead of arbitrary pixel sizes.

### Allowed aspect ratios

- `1:1`
- `2:3`
- `3:2`
- `3:4`
- `4:3`
- `4:5`
- `5:4`
- `9:16`
- `16:9`
- `21:9`

Additional aspect ratios supported only by `nano-banana-2`:

- `1:4`
- `4:1`
- `1:8`
- `8:1`

### Allowed image sizes

For `nano-banana`:

- `1K`
- `2K`
- `4K`

For `nano-banana-2`:

- `0.5K`
- `1K`
- `2K`
- `4K`

### Allowed literal resolutions for Gemini fallback mapping

Only accept these literal resolutions for Gemini requests. Convert them to `aspect_ratio` plus default `1K`.

| Resolution | Aspect Ratio |
| --- | --- |
| `1024x1024` | `1:1` |
| `832x1248` | `2:3` |
| `1248x832` | `3:2` |
| `864x1184` | `3:4` |
| `1184x864` | `4:3` |
| `896x1152` | `4:5` |
| `1152x896` | `5:4` |
| `768x1344` | `9:16` |
| `1344x768` | `16:9` |
| `1536x672` | `21:9` |

Reject other literal Gemini resolutions early and ask the user to switch to:

- an allowed literal resolution above, or
- `aspect_ratio` plus `image_size`

## Reference Images

- Accept up to `4` local reference images in this skill.
- Supported file types:
  - `png`
  - `jpg`
  - `jpeg`
  - `webp`
  - `gif`
- Reference images are sent through `messages[].content[]` entries with `type=image_url`.
- The script uses base64 data URLs for local files.

## Provider Routing

Set:

- `provider.require_parameters=true`

This asks OpenRouter to route only to providers that support the parameters in the request, which is especially important when using:

- `image_config`
- transparent-background GPT Image fields
- provider-specific image options

## Storage Contract

- Output root: workspace `image_gen/`
- Date partition: `YYYY-MM-DD`
- File pattern: `YYYYMMDD-HHMMSS_slug_01.png`
- Sidecar pattern: `YYYYMMDD-HHMMSS_slug_01.json`
