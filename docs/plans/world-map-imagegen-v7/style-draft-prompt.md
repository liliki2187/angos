# World Map v7 Functional Style Draft Prompt

Use case: ui-mockup  
Asset type: Angus world map style draft, desktop 16:9  
Primary request: create a production-oriented style draft based on the v7 functional layout contract, not a generic mood artboard.

Prompt:

```text
Create a desktop 16:9 production style draft for the Angus world map / global channel screen.

Functional intent:
- This screen only chooses a reporting region and enters the selected region.
- It does not select tasks, configure staff, show dice, advance the day, or display a full action log.
- Validate one real state only: North America quarantine zone selected + red-line heating + enterable.

Preserve approved visual direction:
- Keep the existing Angus v6g direction: bright modern ivory printed paper, strong stylized pixel-print texture, faceted low-poly paper world map, deep navy editorial board, red-orange anomaly/deadline marks, restrained cyan tracking/signal marks, modern supernatural weekly magazine identity.
- Do not redesign the central world map base into a different theme.
- The central map board should remain the main visual object, with a cool blue-gray faceted paper world map and high-end pixel-print material.

Required layout:
- Top low-weight status strip: left weekly clock tickets for week / days, plus a visually separate world-state badge rail for five macro attributes.
- Left region index: four clean horizontal card slots with separate blank areas for title, availability, difficulty, recommendation, and one short reason / lock gap.
- Central map board: the largest object, containing only the map material, grid, crop marks, paper facets, low-weight decorative print marks, and weak route atmosphere.
- Right selected-region dossier: a clean orthographic paper face with separate blank zones for title, difficulty / recommendation badges, region image, state ticket, secondary task-intel ticket, region body sections, and footer / blocker line.
- Task intel popover: reserve an optional no-text secondary popover shell anchored to the task-intel ticket for read-only task preview rows; it must not resemble a task selection board.
- Primary CTA plate: a separate editorial action object / channel cut-in / signoff plate beneath the dossier, with a clean center label area.
- Bottom ticker: one printed receipt / channel strip with three short blank receipt lanes.

Content safety:
- No readable text of any kind.
- No Chinese characters, no English UI labels, no letters, no numbers, no region names, no task names, no countdowns, no button labels, no fake tooltip, no fake status chip, no fake map pin label, no fake task card, no watermark, no signature.
- All future dynamic content must be rendered later by Godot inside explicit clean content_rects.
- Text-safe zones must be low-noise, orthographic, horizontal, and visually quiet.

No-text zones:
- Keep tabs, clips, screws, folds, bookmarks, side color strips, arrows, halftone clusters, crop marks, paper edges, strong borders, decorative protrusions, icon plates, warning stripes, and map texture outside future text zones.
- Strong pixelization should affect edges, shadows, outlines, map coasts, signal marks, and print artifacts, not the blank writing surfaces.

Interactive separation:
- Do not bake gameplay pins, selected rings, hover labels, lock icons, route nodes, CTA text, or UI states into the background.
- Pins, selected rings, hover labels, region card states, CTA states, ticker states, and tab states must read as later component layers or atlases.

Avoid:
- old newspaper, yellowed archive, parchment, historical case file, dirty paper speckles, tea stain, sepia, warm wood desk, coffee office, glass SaaS panels, cyberpunk hologram, generic mobile game UI, low-resolution retro 8-bit style, photographic paper noise.
```

Reference notes:

- Use `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/wm-fullscreen-artboard-v6g-pixel-strong.png` as the strongest pixel/material reference.
- Use `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/wm-fullscreen-artboard-v6h-pixel-strong-bright-paper.png` only as a paper-brightness reference if needed.
- Use `docs/plans/world-map-imagegen-v7/functional-layout-contract.md` as the layout and capacity source of truth.
