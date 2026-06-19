# World Map v7 Filled Content Mock V1

> Date: 2026-06-18  
> Status: filled-state content validation mock, not an art source and not a no-text production PNG.  
> Purpose: verify the current world-map information contract with real Chinese content before Image 2 style drafting and component splitting.

## Screenshot Artifacts

- Full screen filled mock: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/01-world-map-v7-filled-content-mock.png`
- Right dossier 100% crop: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/02-right-dossier-filled-content-100pct.png`
- Bottom ticker warning detail open: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/03-bottom-ticker-warning-detail-open.png`
- Bottom ticker 100% crop: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/04-bottom-ticker-100pct.png`
- Editable source: `docs/prototypes/world-map-v7/filled-content-mock-v1.html`

## Validated State

```text
Selected region: 北美禁区带
Availability: 可进入
Urgent state: 红线升温
Week state: 探索周 01 / 剩余 7 天
World metrics: 公信 42 / 诡名 18 / 声望 31 / 守序 26 / 狂性 11
Primary action: 进入选定地区
```

## Current Layout Decisions

- The production-review annotation row from the earlier structure wireframe is removed. The game-facing top area now contains only the real top status strip.
- The right dossier body contains one continuous selected-region introduction paragraph only.
- `地区情报 / 档案更新 / 地区预警` are implemented as clickable bottom ticker entrances.
- The task-pool preview remains a secondary ticket under the red state strip: `查看任务情报 · 3`.
- The bottom ticker detail layer opens as a read-only popover over the map area, not over the right dossier CTA.
- The primary CTA keeps a fixed label: `进入选定地区`; it does not include the selected region name.

## QA Notes

- Right dossier crop confirms the CTA fills the intended content width and is not squeezed by the side tab decoration.
- The prose body does not contain task counts, task names, material lists, file updates, or warning detail cards.
- The bottom ticker detail open state does not reflow the right dossier and does not cover the primary CTA.
- Central map art remains placeholder-level in this mock. It validates occupied space and state relationships only; the approved v6g low-poly paper map language should be retained or retranslated in the next style draft.

## Next Step

Use this filled-state mock as the field and capacity source for the next Image 2 style draft. The style draft should visually approach the accepted v7/fusion B direction, but must preserve these content slots and should not bake final Chinese text into production PNG components.
