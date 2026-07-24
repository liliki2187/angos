# WMW 完整整屏 benchmark Art Pass v0.5 Production Brief

## 状态

- `artifact_type = fullscreen_benchmark_art_identity_pass_candidate`
- `canvas = 1920x1080`
- `state = default`
- `status = executed_parent_three_up_benchmark_identity_iterate_pending_user_decision`
- `layout_truth = v0.4 rects accepted by user`
- `art_identity_truth = benchmark-board-01 / benchmark-board-02`
- `v0.4_permission = geometry_and_content_mask_only`

本轮执行 A248：不重开三栏版面，只重建美术身份。v0.4 的倒角框、按钮、纸色、阴影、材质与组件皮肤全部禁止继承。

## 六维 Style Lock

| 维度 | 硬要求 |
| --- | --- |
| 形状 | 裁切卡纸、装裱照片、平面印刷标签、短硬纸影与克制套印边；主体载体本身必须成立，禁止角落贴纸式修补 |
| 色彩 | 深海军蓝主场；品牌黄绿选中；teal / slate 次级；mustard 与 rust 小面积；纸面为清洁中性暖纸 |
| 材质 | 哑光卡纸、无涂布纸、照片纸、轻印刷齿；禁止棕灰档案、金属、玻璃、辉光和旧报纸 |
| 字体 | 后置粗窄刊头、几何中文标题、清晰正文、窄 metadata 与表格数字；不再使用同一通用字号体系覆盖所有层级 |
| 异常选片 | 三张地区照片必须有清晰异常主体；左北美与右 hero 同事件、不同编辑裁切；禁止普通风景缩略图和细碎三角滤镜 |
| 品牌符号 | 允许少量 globe seal、issue mark、照片角、登记线、胶带或夹具；全部非交互且只在既有 carrier 边缘 |

## 生成前 UX 安全句

- 装饰物与既有真实字段重叠必须为 0。
- 贴纸、胶带、夹具和品牌图形不得拥有可读文字、数字、箭头、状态色、按钮边框或工具栏排列。
- 禁止新增路线、图例、筛选器、额外 pin、warning stamp、“红线升温”、世界新闻、快捷按钮、抽屉或任务动作。
- 中央选区第一、右档案第二、右下 CTA 唯一最强；左日程动作次级；任务状态为信息标签，不得读成四个按钮。

## 生成记录

- 模式：Codex 内置 `imagegen`，`ui-mockup`。
- 参考 1：`benchmark-board-01.png`，艺术身份第一真值。
- 参考 2：`benchmark-board-02.png`，艺术身份第一真值。
- 参考 3：`wmw-fullscreen-default-art-pass-filled-v0-4.png`，仅 geometry / content mask。
- 原始生成位置：`C:\Users\gzfangyue\.codex\generated_images\019f7e73-ca4d-76a2-9cd3-ef38d3c490cc\exec-3f492a16-ed7e-4634-a2ae-c6d607a3ee97.png`。
- 工作区源：`wmw-fullscreen-default-art-pass-imagegen-source-v0-5.png`。
- 装配脚本：`render_wmw_fullscreen_benchmark_art_pass_v0_5.py`。
- 完整候选：`wmw-fullscreen-default-benchmark-art-pass-filled-v0-5.png`。

## 最终执行 Prompt

```text
Use case: ui-mockup
Asset type: complete 1920x1080 desktop game UI visual-style art pass
Primary request: Create one cohesive no-text player-facing WORLD MYSTERIES WEEKLY world-map screen whose artistic identity unmistakably belongs to the same modern mystery-weekly editorial family as Images 1 and 2, while preserving only the functional geometry and content capacity of Image 3.

Reference priority:
- Image 1 and Image 2 are the sole artistic-identity truth. Inherit their modern editorial collage, strong publication graphics, matte cardstock, mounted photo prints, controlled paper layering, registration details, graphic color blocks, deep navy negative space, vivid olive-yellow green, cool teal/slate, mustard and restrained rust.
- Image 3 is geometry and content-capacity reference only. Preserve its three-column layout and carrier locations, but do not inherit any frame, bevel, button, paper color, shadow, material, typography or component skin from Image 3.

Fixed composition:
- Landscape 16:9, full screen, front-facing orthographic UI, no desk scene.
- Left: three aligned 348x240 region cards beginning near x30 with 18px vertical gaps, then one aligned 348x246 weekly schedule insert. Preserve their exact outer locations and content capacity.
- Center: dominant deep-navy world-map stage, first visual focus, with broad printed/cut-paper continent shapes. North America is the vivid brand-olive focal region; other continents use cool teal and slate. No routes, legends, event network, radar or GIS treatment.
- Right: one continuous full-height warm-neutral editorial feature sheet, second visual focus, with one headline zone, one mounted North America anomaly hero photo, one calm story-copy zone, one mission section header, four information rows, and one bottom olive CTA strip. No rear page, folder, bag, second shell or extra control.
- The bottom-right CTA strip is the single strongest action. The left schedule action is visible but clearly secondary.

Six-dimensional style lock:
1. Shape language: die-cut editorial cardstock, mounted photo prints, flat printed labels, short hard paper shadows, restrained registration-offset edges. The main carriers themselves must embody the collage language; never keep generic panels and merely add stickers to corners.
2. Color roles: board navy #071721 to #0D222C; clean paper light #D4CAB3; paper mid #BCA985; brand olive #879C36 with dark olive #56672B; teal #2E5B60; slate #3C535C; mustard #C49A3D; deadline rust #8B4E32 only for the true timed-task accent.
3. Materials: clean modern matte cardstock, uncoated editorial paper, mounted photo paper, subtle print tooth, broad low-poly value planes and short crisp shadows. No parchment, cardboard grime, metal, glass or glow.
4. Typography-safe art: reserve calm orthogonal writable areas for a later bold condensed masthead, heavy geometric Chinese headings, clean body text, condensed metadata and tabular numerals. Render no readable text now.
5. Anomaly imagery: the three left photos are clear editorial anomaly subjects with distinct color identities, not ordinary landscape thumbnails. The selected North America radome image and the right hero photo share the same event identity at different editorial crops. Use coarse readable low-poly shapes, not dense triangle filters.
6. Brand graphics: allow restrained abstract globe seals, issue marks, photo corners, registration lines, tape or small clips as non-interactive publication decoration within existing carriers.

Left region cards:
- Each is one clean die-cut editorial card with one mounted anomaly photo and one printed caption/footer.
- Selected uses vivid olive as integrated paper/print treatment.
- Locked cards use cool blue-gray, never brown-gray.
- Status carriers are flat printed tags, never raised buttons.
- All three share one coherent construction language without repeated chamfered HUD shells.

Schedule:
- Treat the whole module as a weekly issue insert.
- Light paper date strip, dark olive printed action band and two calm consequence lines.
- No bevel, metal well, console styling or luminous border.

Right feature page:
- One continuous clean warm-neutral editorial sheet.
- One mounted hero photograph, strong feature-headline area, calm article copy, one publication rule, four information rows, one bottom olive CTA.
- Mission status carriers are printed labels, not four buttons.
- Allow at most one restrained publication seal and one photo attachment treatment.

Interaction safety:
- Preserve every existing functional and content rectangle exactly.
- Decorative collage elements may overlap only non-content outer margins and frame corners; zero overlap with region titles, state labels, map labels or pins, schedule date/action/consequence fields, dossier text, task rows, disclosure summary or main CTA.
- Stickers, tape, clips and brand graphics are non-interactive physical decoration only: no readable words, numbers, arrows, chevrons, progress marks, status colors, button borders, repeated equal-sized icons, or alignment resembling a toolbar, filter, tab, badge, toggle or secondary CTA.
- Do not invent routes, legends, filters, extra pins, warning stamps, redline-warning badges, world-news strips, shortcut buttons, drawers, extra task actions or any control not present in Image 3.
- Maintain fixed visual priority: central selected map region first, right dossier second, bottom-right CTA only dominant action. Left schedule secondary; task status labels read as flat information, never buttons.
- Keep all writing surfaces orthogonal, clean and visually quiet. Texture, shadows, paper edges, tape and print tooth never cross writable areas.

Hard negatives:
no generic dashboard, no military archive software, no strategy HUD, no gray-brown parchment dominance, no sepia, no old newspaper, no metal bevels, no embossed frames, no inner glow, no soft luminous borders, no glossy UI, no repeated chamfered buttons, no sticker-only retrofit over unchanged panels, no fake text, no pseudo-text, no fake UI, no extra modules, no route lines, no GIS, no radar, no desk scene, no perspective room, no isometric environment, no uncontrolled clutter outside existing carriers, no watermark.

Output intent: a polished shippable visual-style proposal, not concept art, not an asset sheet, not a component board. Even with all future text hidden and viewed at 25% scale, it must still read immediately as a modern colorful mystery-weekly editorial collage from the same visual family as Images 1 and 2.
```

## 边界

- 本轮不改 Godot、正式合同、compact A5.1、B2.12 或三栏职责。
- 默认态获用户认可前，不生成 confirming、atlas 或拆件。
- 只向用户展示最终完整玩家视图；无字源、补片与 QA 不单独作为审阅项。
