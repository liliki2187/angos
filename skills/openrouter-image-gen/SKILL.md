---
name: openrouter-image-gen
description: Generate, edit, or plan game-ready images through OpenRouter image models, including OpenAI GPT-5 Image transparency workflows and Google Nano Banana / Nano Banana 2 opaque workflows. Use when the user asks for OpenRouter image generation, openrouter image gen, openrouter 生图, Nano Banana, Nano Banana 2, GPT-5 Image transparent PNGs, reference-image image-to-image generation, game textures, icons, key art, splash art, posters, UI banners, decals, portraits, environment art, props, sprites, or similar visual asset generation tasks.
---

# OpenRouter Image Gen

Use this skill to plan and run OpenRouter-based image generation for game production assets.

## Quick Workflow

1. Read `references/model-routing.md` before choosing a model or validating user-provided size/background constraints.
2. Read `references/prompt-planning.md` before writing the final prompt bundle.
3. Check `config.env` in this skill folder. If it does not exist, ask the user to copy `config.env.example` to `config.env` and fill in the API key.
4. Normalize the request into:
   - `asset_type`
   - `background`
   - `count`
   - `model`
   - `resolution` or `aspect_ratio` plus `image_size`
   - `reference_image` paths if any
   - `slug`
   - positive prompt
   - negative constraints
5. Validate parameters before sending any API request. If the request is outside the supported matrix, stop immediately and explain what must change.
6. Run the Python script in this folder.
7. Return the saved image paths and metadata JSON paths to the user.

## Routing Rules

- If the user wants a transparent background, route to `openai/gpt-5-image` only.
- If the user wants a non-transparent image, choose between:
  - `google/gemini-2.5-flash-image` for simpler and faster tasks
  - `google/gemini-3.1-flash-image-preview` for more complex composition, heavier text/layout demands, more references, or extended aspect ratios
- If the user explicitly names one of the supported models, honor it only if the rest of the request is valid for that model.
- Treat reference-image generation as a normal path for all supported models, but keep the request conservative and validate local file existence first.

## Common Asset Types

Use the prompt planner to infer defaults for at least these common game-production targets:

- `icon`
- `item`
- `prop`
- `sprite`
- `vfx`
- `decal`
- `texture`
- `tileable-texture`
- `portrait`
- `character-concept`
- `creature-concept`
- `environment-concept`
- `background`
- `key-art`
- `poster`
- `ui-screen`
- `ui-banner`
- `logo-mark`
- `card-art`
- `isometric-asset`

If the user does not provide an asset type, infer the closest one from their request and record that inference in the metadata JSON.

## Prompt Rules

- Treat the user request as production intent, not as a raw final prompt.
- Expand the prompt into a game-ready generation prompt that clarifies:
  - subject
  - camera/framing
  - rendering style
  - material/lighting
  - silhouette readability
  - intended in-game use
  - background requirement
  - reference-image role if present
- Always include negative constraints from `references/prompt-planning.md`.
- Do not rely on a dedicated negative prompt parameter. The script compiles negative constraints into the final prompt text.

## Validation Rules

- Stop before calling OpenRouter if:
  - the user requests transparent output on a non-GPT-5 Image model
  - the user requests an unsupported literal resolution
  - the user requests an unsupported aspect ratio / image size pair
  - `count` is outside the supported range
  - reference image files do not exist or use unsupported formats
- Prefer explicit correction over silent fallback.
- Record every fallback or inference in the metadata JSON.

## Commands

Use these commands from the repository root:

```powershell
python ".\skills\openrouter-image-gen\scripts\openrouter_image_gen.py" doctor
```

```powershell
python ".\skills\openrouter-image-gen\scripts\openrouter_image_gen.py" generate `
  --prompt "Angus occult newspaper front page key art with a field board and printroom glow" `
  --asset-type key-art `
  --background opaque `
  --count 2 `
  --aspect-ratio 3:4 `
  --image-size 2K `
  --slug angus-key-art
```

```powershell
python ".\skills\openrouter-image-gen\scripts\openrouter_image_gen.py" generate `
  --prompt "Clean in-game relic icon, brass sigil, readable silhouette" `
  --asset-type icon `
  --background transparent `
  --count 1 `
  --resolution 1024x1024 `
  --slug relic-icon
```

Add one or more reference images like this:

```powershell
python ".\skills\openrouter-image-gen\scripts\openrouter_image_gen.py" generate `
  --prompt "Refine this scene into a cleaner production-ready environment concept" `
  --asset-type environment-concept `
  --background opaque `
  --model nano-banana-2 `
  --count 1 `
  --aspect-ratio 16:9 `
  --image-size 2K `
  --reference-image ".\path\to\ref-01.png" `
  --reference-image ".\path\to\ref-02.png" `
  --slug refinery-yard
```

## Output Rules

- Save generated files under the workspace root in `image_gen/YYYY-MM-DD/`.
- Prefix every filename with a local timestamp.
- Include a descriptive slug in every filename.
- Save a sidecar JSON next to each image with:
  - original user request
  - inferred asset type
  - chosen model and why
  - normalized size/background/count
  - final prompt
  - negative constraints
  - reference image list
  - OpenRouter response identifiers and usage if available
  - output file paths
  - warnings / assumptions / fallbacks

## Files To Read

- `references/model-routing.md`
- `references/prompt-planning.md`
- `config.env.example`
