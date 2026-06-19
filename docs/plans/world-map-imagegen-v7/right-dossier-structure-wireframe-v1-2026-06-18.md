# World Map v7 Right Dossier Structure Wireframe V1

> Date: 2026-06-18  
> Status: structure direction accepted by user on 2026-06-18; still not an approved art source.  
> Purpose: recover from the A80 legacy-container failure by proving the right dossier can physically hold the new function set before generating no-text PNG components.

## Screenshot Artifacts

- Full screen structure wireframe: `docs/screenshots/2026-06-18-world-map-v7-right-dossier-structure/01-world-map-v7-right-dossier-structure-wireframe.png`
- Right dossier 100% crop: `docs/screenshots/2026-06-18-world-map-v7-right-dossier-structure/02-right-dossier-structure-100pct-crop.png`
- Editable source: `docs/prototypes/world-map-v7/right-dossier-structure-wireframe.html`

## Layout Decision Under Test

The old `432w` right dossier is rejected for this function set. V1 tests a wider `560w` right dossier and shifts the main desktop layout to:

```text
Canvas 1920x1080

Top strip     [40,104,1840,64]
Left index    [40,188,360,750]
Map board     [420,188,880,750]
Right dossier [1320,188,560,750]
Bottom ticker [40,952,1840,88]
```

This preserves a large central map while giving the selected-region dossier enough physical area for media, risk, task preview entry, prose, footer, and CTA.

## Right Dossier Internal Structure

Outer dossier: `560x750`.

Reserved side decoration / no-text area:

```text
right_side_tabs / binder trim [498,0,62,750]
```

Dynamic content column:

```text
content column [28,18,470,714]

header             [0,0,470,88]
media_viewport     [0,104,470,170]
alert_ribbon       [0,290,470,44]
task_intel_ticket  [42,348,386,52]
air_gap            [0,412,470,18]
prose_body         [0,442,470,150]
footer_hint        [0,604,470,38]
primary_cta        [0,654,470,60]
```

## Content Capacity

| Slot | Capacity | Runtime content | Production PNG may include |
| --- | --- | --- | --- |
| Header | title 8-10 chars, 2 compact badges | fixed label, region name, difficulty, recommendation | paper section, empty badge frames |
| Media viewport | one clipped image, no text overlay | region preview image loaded / masked at runtime or baked per-region if stable | media frame, mask, crop marks |
| Alert ribbon | 1 line, 16-18 chars | red-line / lock / urgent warning | empty red ribbon / alert frame |
| Task intel ticket | `查看任务情报 · N`, one right action cue | task count, hover / pressed / open state | ticket shell, arrow slot, state atlas |
| Prose body | one 70-110 char paragraph | single selected-region introduction only | clean paper area, optional region-type chip frame |
| Footer hint | 1 low-weight rule line | entry consequence / disabled reason | footnote strip |
| Primary CTA | 4-6 chars, fixed action | `进入选定地区` / disabled / loading | CTA atlas frames |
| Bottom ticker item | type 4 chars + title 10-14 chars + action cue | clickable `地区情报 / 档案更新 / 地区预警` detail entrances | ticker shell, empty type chip, arrow/action zone |

## Compatibility Gates

This structure passes the first-order checks that A80 failed:

- The region image is inside a fixed media viewport and cannot visually fly into side tabs.
- The red alert ribbon and cyan task-intel ticket each have their own physical slot.
- The task-intel ticket is inset and separated from prose by an 18px air gap.
- The prose body contains only a single region introduction, not task counts, action controls, region-intel tiles, file-update rows, or warning details.
- The primary CTA is not inside the media image and does not compete with the task-intel ticket.
- The right-side label / binder trim is explicitly marked as `no_text_rect`.
- `地区情报 / 档案更新 / 地区预警` are moved to clickable bottom ticker items. Their detail content must open from the ticker item and must not flow back into the right prose body.

## Known Non-Art Limitations

- This is a low-fidelity structure wireframe, not a style draft.
- It uses CSS blocks and text to verify capacity; it should not be used as a visual target.
- It does not yet solve final art style, pixel texture, paper material, CTA pressed animation, or media-frame ornament language.
- It does not yet include locked / disabled / empty variants or open ticker-detail popovers. Those belong to the next state wireframe pass after this default layout is accepted.

## Next Step If Approved

1. Generate a no-text style draft using this structure, keeping v6g's central low-poly paper map direction.
2. Create `wm_right_dossier_base_v7b`, `wm_region_media_frame_v7b`, `wm_alert_ribbon_v7b`, `wm_task_intel_ticket_atlas_v7b`, and `wm_cta_enter_region_atlas_v7b`.
3. Update the v7 manifest draft with the rects above.
4. Produce a filled-state text mock using the same content to verify final visual fusion.
5. Only then integrate in Godot.
