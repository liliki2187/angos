# 世界地图「夜班四色套印选题台」v1 交付清单

## 结论

`01-night-press-color-key-desk-1920x1080.png` 是第一张只按宏观组件家族、综合色块、地图载体和氛围光重构的方向候选。UX 老哥与 UI Designer 均判宏观风格 Gate 通过，可交用户判断“大风格是否成立”；状态为 `macro_style_direction_candidate / pending_user_visual_decision`。

它不是功能合同通过稿、production visual target、asset master 或 Godot landing 许可。

## 交付物

- `image_gen/2026-08-17/world-map-night-press-color-key-desk-v1/01-night-press-color-key-desk-1920x1080.png`
  - Codex 内置 ImageGen 从空白画布生成。
  - 原始 `1672×941`，程序只做高质量无裁切规格化为 `1920×1080`。
- `image_gen/2026-08-17/world-map-night-press-color-key-desk-v1/02-macro-style-before-after-board-1920x620.png`
  - 程序仅负责把 02 与新候选等比并排、加标题，用于宏观差异 QA；不替代生图。

## 核心提示词

```text
Create a brand-new 1920×1080 filled-state desktop game UI for World Mystery Weekly in the unique direction “Night Press Color-Key Desk”. Image 02 is only a negative macro-silhouette and functional-position guide; do not inherit its three white cards, uniform dark GIS board, giant continuous white dossier or white Schedule.

Keep the three-column responsibilities and frozen image / text / Disclosure / CTA regions, but completely redesign the visible component families: three same-size cobalt / olive / mustard regional pitch jackets on the left; a large cobalt / muted-teal screen-printed world proof with only 4–6 broad continent groups in the center; a two-tone cobalt editor’s jacket with an upper warm-white lead proof and lower blue-gray / olive review tray on the right; a mustard / olive physical deadline calendar dock below the left cards.

Allocate roughly 42% midnight navy, 35% combined cobalt/teal/olive/mustard midtones, no more than 24–28% warm-white paper, and about 3% rust red. The redesign must remain obvious at 480×270 after hiding all text, notes and objects smaller than 80×80. Use modern pressboard, crisp die-cut paper, broad low-poly planes and restrained print tooth. Avoid white paper walls, dense triangle maps, SCP, radar, target rings, eye emblems, locks, military hardware, CASE FILE, antique archives, dirty grunge, photorealism, pixel art and halftone.
```

## 宏观 QA

- `480×270 + 12px Gaussian blur` 后，显著明度变化粗测：全屏 `43.7%`。
- 分区变化：左 `29.9%`、中 `35.7%`、右 `71.0%`。
- 近白纸代理阈值粗测约 `8.2–13.5%`；该值不是 CIE Lab 精确面积，只用于确认没有回到左右白纸墙。
- 遮字后仍可读：蓝 / 绿 / 芥末选题夹、世界套印版样、双色主编稿夹、综合色日历器。

## 双审

- UX 老哥：宏观 Gate 通过，`P0=0 / P1=2 / P2=3`。P1 为 locked 静态事实仍需运行语义证明，以及 Schedule 黄色 FrontCarrier / 橄榄 BackDecor 分层不清；两项不阻断本轮大风格判断。
- UI Designer：宏观组件家族、综合色和 clean low-poly 均通过；两个视觉 P1 为地图 02 / 03 同心圆 pin 仍像靶标，以及夹壳 / CTA 铆钉与卡扣偏工业设备，需要回到现代压纹纸板。

## 继续阻断

- 用户确认大风格前不做局部清稿、组件拆分或状态矩阵。
- 不从整屏回裁生产组件。
- 不进入 atlas、manifest、Godot 或 `WeeklyRunGame`。
