# Model Routing

Use this file whenever you need to choose a model, normalize size parameters, or reject an invalid request.

## Supported Routes

| Route | Backend | Use For | Notes |
| --- | --- | --- | --- |
| `gpt-5-image` | `openai/gpt-5-image` | Transparent PNG/WebP assets, clean cutout assets, precise isolated game objects | The only OpenRouter path in this skill |
| `built-in-imagegen-opaque` | built-in `image_gen` tool | Non-transparent textures, concepts, posters, UI banners, portraits, environments, and other opaque outputs | Default opaque path; does not require OpenRouter config |

## Hard Routing Rule

- `background=transparent` -> only `openai/gpt-5-image`
- `background=opaque` -> only built-in `image_gen`

## Legacy Terms

- `nano-banana`
- `nano-banana-2`

Treat those as legacy user phrasing only. They should still resolve to this skill, but the actual opaque execution path must be built-in `image_gen`, not a third-party OpenRouter image model.

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

## Opaque Request Handling

For opaque requests in this skill:

- do not call `scripts/openrouter_image_gen.py`
- do not require `config.env`
- do not mention or choose Nano Banana / Nano Banana 2
- use built-in `image_gen`
- express size or framing needs in the prompt bundle instead of OpenRouter `image_config`
- if the result is project-bound, copy the selected built-in output into workspace `image_gen/YYYY-MM-DD/` and write a sidecar JSON

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

- transparent-background GPT Image fields
- provider-specific transparent-image options

## Storage Contract

- Output root: workspace `image_gen/`
- Date partition: `YYYY-MM-DD`
- File pattern: `YYYYMMDD-HHMMSS_slug_01.png`
- Sidecar pattern: `YYYYMMDD-HHMMSS_slug_01.json`
- For built-in opaque requests, include the original `$CODEX_HOME/generated_images/...` source path in the JSON metadata.
