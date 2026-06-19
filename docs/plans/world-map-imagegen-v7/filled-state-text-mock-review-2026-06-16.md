# World Map v7 Filled-State Text Mock Review

> Draft: `docs/screenshots/2026-06-16-world-map-v7-functional-style-draft/02-world-map-v7-filled-state-text-mock.png`  
> Prompt: `docs/plans/world-map-imagegen-v7/filled-state-text-mock-prompt.md`  
> Status: target screenshot / visual-density reference only. Not a production asset.

## What Works

- The screen reads more like a near-final game screenshot than the empty component draft.
- The v7 layout can carry the current North America state without immediately collapsing into overflow.
- Left index, selected map state, right dossier, CTA, and ticker form a clearer selected-region chain.
- The CTA reads better when the real action phrase is tested at full length.
- The bottom ticker density is acceptable when kept to one short line per lane.

## Problems To Watch

- Image-generated Chinese is good enough for a visual target, but it is still baked and not reliable enough for runtime.
- The generated text must be treated as a typography / hierarchy target, not as exact copy truth.
- Map selected ring / routes in this filled mock are visual guidance only. Production must use runtime layers or separate atlases.
- Right dossier content should remain a short region summary. Do not let it become a task operation list in Godot.
- Top-strip copy may need lower visual weight in runtime so the map remains the main object.

## Production Rule

Filled-state text mocks are allowed as a new middle step:

```text
functional contract -> empty style draft -> filled-state text mock -> component assets -> Godot dynamic reconstruction
```

The filled mock may guide typography, text hierarchy, information density, and target screenshot quality. It must not be cut into UI components, written to the production manifest as a runtime image, or used to bake dynamic Chinese text into PNG assets.
