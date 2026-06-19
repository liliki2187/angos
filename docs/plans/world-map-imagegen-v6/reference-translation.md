# World Map Imagegen V6 Reference Translation

> Status: v6 candidate direction. Do not replace the current v5 runtime UI until the artboard and component assets pass art, UI, and UX review.

## User-Approved Direction

The new reference direction should be treated as a style target for the next world-map asset pass:

- Brighter warm paper: closer to clean ivory editorial stock, not yellowed archive paper.
- Cleaner printed material: folds, crop marks, binder clips, tabs, and paper shadows should feel intentional and premium.
- Low-poly paper world map: the map should be recognizable but abstracted, with faceted polygon shapes, paper grain, and restrained printed texture.
- Deep navy engineering board: the dark base remains Angus, but it should support clean contrast instead of swallowing text and cards.
- Controlled red and cyan: red marks deadline/anomaly energy; cyan marks tracking/signal. They should be sparse and structural.
- Strong usable blank zones: paper areas must leave quiet content rectangles for Godot-rendered text, numbers, labels, states, and CTA copy.

## What To Keep From Angus

- Modern supernatural weekly magazine / global channel identity.
- Deep navy, vivid red-orange, warm paper, restrained cyan.
- Printed matter materiality: crop marks, halftone dots, registration marks, misregistration, paper layering.
- Pixel material as deliberate 2-4px block clusters and halftone structure, not retro 8-bit UI.
- Dynamic text and state ownership remains in Godot.

## What To Avoid

- Old newspaper, yellowed archive, parchment, historical case-file mood.
- Photographic paper noise, dirty mold speckles, muddy gray-blue detail.
- Cyberpunk glass, neon holograms, SaaS panels, generic mobile-game buttons.
- Baked Chinese text, baked numbers, fake pins, fake task states, fake button labels.
- Dense geography detail that competes with runtime pins and selection feedback.

## V6 Artboard Acceptance

- At 1920x1080, the central map reads as premium low-poly paper geography, not a noisy old map.
- Left and right paper zones are brighter than v5 and have obvious clean writing areas.
- The central map remains the dominant object; side panels feel like working editorial objects.
- No baked UI text, region names, numbers, countdowns, labels, fake task cards, or fake buttons.
- The design can be split into runtime components without needing Pillow or GDScript to paint missing art.
