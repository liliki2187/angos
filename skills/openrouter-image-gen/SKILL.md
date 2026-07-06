---
name: openrouter-image-gen
description: Plan and generate game-ready images with a hybrid workflow: OpenRouter GPT-5 Image for transparent PNG/WebP assets, and built-in imagegen for opaque textures, concepts, posters, UI banners, portraits, environments, and other non-transparent images. Use when the user asks for OpenRouter image generation, openrouter image gen, openrouter 生图, GPT-5 Image transparent PNGs, reference-image image-to-image generation, game textures, icons, key art, splash art, posters, UI banners, decals, portraits, environment art, props, sprites, or similar visual asset generation tasks. Legacy Nano Banana or Nano Banana 2 phrasing should still trigger this skill, but opaque requests must route to built-in imagegen instead of third-party models. If built-in imagegen / image_gen is unavailable, report that the request cannot be completed in the current session instead of using an OpenRouter opaque fallback.
---

# OpenRouter Image Gen

Use this skill to plan and run game production image generation with two execution paths:

- transparent assets -> OpenRouter `openai/gpt-5-image`
- opaque assets -> built-in `$imagegen`

## Quick Workflow

1. Read `references/model-routing.md` before choosing a model or validating user-provided size/background constraints.
2. Read `references/prompt-planning.md` before writing the final prompt bundle.
3. Normalize the request into:
   - `asset_type`
   - `background`
   - `count`
   - `route`
   - `resolution` or framing / aspect hints
   - `reference_image` paths if any
   - `slug`
   - positive prompt
   - negative constraints
4. Choose the execution path:
   - `background=transparent` -> OpenRouter helper script
   - `background=opaque` -> built-in `$imagegen`
   - `background=opaque` but built-in `image_gen` is unavailable -> fail with a clear explanation; do not use OpenRouter as a fallback
5. Only check `config.env` in this skill folder when the request routes to the OpenRouter helper script. Opaque requests must not be blocked on missing OpenRouter config because they do not use OpenRouter.
6. Validate parameters before sending any API request or tool call. If the request is outside the supported matrix, stop immediately and explain what must change.
7. Execute the selected path:
   - OpenRouter path: run the Python script in this folder
   - Built-in opaque path: call `image_gen`, then copy the selected output from `$CODEX_HOME/generated_images/...` into the workspace
8. Return the saved image paths and metadata JSON paths to the user.

## Claude-to-IM / IM Triggering

When this skill is triggered from a `claude-to-im` bridged Codex session, keep the same routing contract:

- If the IM user asks for an opaque game or project image and the actual tool list exposes built-in `image_gen`, use the built-in `$imagegen` path.
- If the bridged Codex SDK/CLI session does not expose built-in `image_gen`, fail directly and tell the user that `$imagegen` is unavailable in the current bridge session.
- Treat built-in `$imagegen` / `image_gen` as a conversation tool capability, not a shell executable. Do not search for an `image_gen` command on `PATH`.
- Do not run `scripts/openrouter_image_gen.py` for opaque requests, including bridge sessions where `$imagegen` is unavailable.
- Save project-bound outputs under `image_gen/YYYY-MM-DD/` and write the sidecar JSON metadata.
- After saving the image, report the workspace path. For Feishu delivery, the bridge can reuse the `claude-to-im send images` workflow or `skills/claude-to-im/scripts/send-feishu-images-post.mjs`.
- If the user asks for transparent output, keep using the transparent routing rules below unless the project explicitly changes that policy.

## Routing Rules

- If the user wants a transparent background, route to `openai/gpt-5-image` only.
- If the user wants a non-transparent image, route to built-in `$imagegen` only.
- If `image_gen` is unavailable, stop and report failure instead of using OpenRouter.
- If the user explicitly says `nano banana` or `nano banana 2`, treat that as legacy wording for an opaque request and still route to built-in `$imagegen`.
- If the user explicitly says `gpt-5-image` for a non-transparent request, explain that this skill uses built-in `$imagegen` for opaque outputs and cannot fall back to OpenRouter when `$imagegen` is unavailable.
- Treat reference-image generation as a normal path for both routes, but keep the request conservative and validate local file existence first.

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
- For built-in opaque requests, format the prompt bundle so it can be pasted directly into `$imagegen` as a single structured prompt.

## Validation Rules

- Stop before calling OpenRouter if:
  - the user requests transparent output on a non-GPT-5 Image model
  - the user requests an unsupported literal resolution
  - `count` is outside the supported range
  - reference image files do not exist or use unsupported formats
- Stop before using the OpenRouter helper script if the resolved background is `opaque`; opaque requests belong to built-in `$imagegen`, not this script.
- Prefer explicit correction over silent fallback.
- Record every fallback or inference in the metadata JSON.

## Commands

Use these commands from the repository root for the transparent OpenRouter path only:

```powershell
python ".\skills\openrouter-image-gen\scripts\openrouter_image_gen.py" doctor
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

Add one or more reference images to the transparent path like this:

```powershell
python ".\skills\openrouter-image-gen\scripts\openrouter_image_gen.py" generate `
  --prompt "Clean occult crest cutout with sharper silhouette and controlled metallic detail" `
  --asset-type logo-mark `
  --background transparent `
  --count 1 `
  --resolution 1024x1024 `
  --reference-image ".\path\to\ref-01.png" `
  --reference-image ".\path\to\ref-02.png" `
  --slug occult-crest
```

For opaque textures, concepts, posters, portraits, banners, and other non-transparent outputs:

- do not run `openrouter_image_gen.py`
- call built-in `$imagegen`
- if the result is for this project, copy the selected output from `$CODEX_HOME/generated_images/...` into `image_gen/YYYY-MM-DD/`
- write a sidecar JSON next to the copied image with the same metadata contract used by this skill, plus:
  - `execution_mode: "built-in-imagegen-opaque"`
  - `routing_reason`
  - `built_in_source_image`

If `$imagegen` / `image_gen` is unavailable in a bridge session, stop and report that opaque generation cannot be completed from that session. Do not use OpenRouter as an opaque fallback.

## Output Rules

- Save final generated files under the workspace root in `image_gen/YYYY-MM-DD/`.
- Prefix every filename with a local timestamp.
- Include a descriptive slug in every filename.
- Save a sidecar JSON next to each image with:
  - original user request
  - inferred asset type
  - chosen route and why
  - normalized size/background/count
  - final prompt
  - negative constraints
  - reference image list
  - OpenRouter response identifiers and usage if available for transparent requests
  - built-in source image path for opaque requests
  - output file paths
  - warnings / assumptions / fallbacks

## Files To Read

- `references/model-routing.md`
- `references/prompt-planning.md`
- `config.env.example`
