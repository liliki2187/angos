# 派遣签批台 V14 真实内容风格稿 Prompt

> 状态：待生成  
> 目的：生成真正的 `filled-state text mock / 真实内容风格稿`，美术效果应接近正式截图，并能作为后续无字组件拆图与 asset manifest 的目标依据。  
> 重要纠偏：`docs/screenshots/2026-06-18-dispatch-signoff-packaging-v13-filled/01-dispatch-signoff-filled-content-style-v13.png` 只算真实内容结构填充稿，不算真实内容风格稿。

## 参考图角色

- 用户现代参考图：控制 Angus 当前视觉年龄、深蓝主场、红青高能状态色、现代印刷质感、半调 / 套印 / 裁切标记语言。
- V13 结构填充稿：只控制功能分区、真实信息容量、角色 / 道具 / 签批关系，不控制最终美术完成度。

## 正向 Prompt

```text
High-fidelity production art target for a 1920x1080 desktop 16:9 game UI screen, a modern midnight editorial dispatch signoff desk for the Angus supernatural weekly magazine.

Use the modern Angus reference as the visual benchmark: layered deep-sea navy as the dominant field, not black-gray and not blue-green mud. The navy field should have clear value layers through map-like planes, editorial geometry, halftone fields, and restrained grid structure. Clean ivory printed paper appears only as physical work objects. Vivid red-orange creates high-energy collision for danger, route pins, approval and CTA. Cyan appears only as restrained tracking/signal, not as full-screen panel outlines. Use structured halftone dots, crop marks, red-cyan print misregistration, micro-pixel texture, premium printed matter, and clean contemporary editorial design.

Use the V13 structure mock only for functional structure and real content placement: left task dossier, dominant central dispatch board with five selected employee ID cards clipped onto one action rail, one equipment receipt for 匿名热线录音 under the crew, verification ruler for effective points / 人脉 / 洞察 / 缺口 / 达标率 / 失败后果, lower candidate employee badge-card drawer, bottom equipment requisition tray, compact right red approval receipt / stamp board with a physical stamp CTA.

This must look like a complete finished in-game UI screenshot and a future asset-slicing art target, not a wireframe, not a PIL mock, not a programmer UI, not simple rectangular panels.

Keep the same functional meanings: selected crew are already committed and removed from candidates; item is part of current dispatch and does not occupy crew slots; candidate employee drawer is visible by default; equipment tray is visible but secondary; approval ticket is the final decision object.

Include integrated representative Chinese UI content such as M330 未班车空白段, 深度调查 1/4, 可签批 · 队伍 5/5, 盖章签批, 候命员工作证抽屉, 器材领用托盘, 匿名热线录音. It is acceptable if exact text is not perfect for runtime, but it must feel naturally printed into the art and all text-safe zones must be clean, orthographic, rectangular, and replaceable by runtime UI later.

Make boundaries come from graphicized physical objects: dark coated dispatch board, a few functional card clips, paper layers, ticket perforations, drawer lips, red rubber stamp slot, crop marks, short color tabs. Reduce literal office-object realism by at least 30 percent. Clips, rings, holes, rivets, stacked papers, drawer parts and labels should be abstracted into flat editorial cut shapes, print layers, overprint edges or halftone structures. Do not rely on equal thick rectangular panel frames.

Make role cards and candidate cards feel like the same card-size family with polished high-definition micro-pixel character portraits. Central dispatch board must be the visual anchor, with cool layered deep navy negative space and structural route/signal graphics behind the cards. The whole screen should have only one or two dominant visual objects: the central dispatch board and the compact right approval ticket.
```

## 负向约束

```text
Avoid old archive, yellowed paper, dirty paper speckles, coffee stains, torn parchment, warm wood desk, nostalgic office, old newspaper, Sultan palace ornament, gold filigree, SaaS dashboard, generic admin panel, KPI cards, glassmorphism, mobile UI, standard web form fields, programmer wireframe, simple PIL/Canvas rectangles, debug labels, red annotation boxes, explanatory arrows, watermark, excessive grunge, low-resolution 8-bit UI, black-gray muddy navy, blue-green muddy background, full-screen cyan engineering outlines, CAD grid feeling, overly literal office props, realistic binder holes everywhere, excessive clips, rivets, stacked papers or drawer mechanics.
```

## 生成参数建议

- `asset_type`: `ui-screen`
- `background`: `opaque`
- `model`: `nano-banana-2`
- `aspect_ratio`: `16:9`
- `image_size`: `2K`
- `count`: `1`
- `slug`: `dispatch-signoff-real-content-style-v14`

## 通过标准

- 第一眼像现代 Angus，而不是旧档案、后台表单或老报社派工系统。
- 蓝色必须是有层次的深海军蓝，不是黑灰、蓝绿黑或全屏 CAD 网格。
- 中央调度板是主视觉，不被右侧票据或底部候选区抢走。
- 五张已选员工卡、一个随队道具、候选员工抽屉、器材托盘、签批票据的功能关系清楚。
- 纸面是干净象牙白，纹理不穿过标题、数字、CTA 和角色名。
- 红橙只用于危险、签批、主 CTA；青色只用于追踪 / 信号 / 信息。
- 拟物细节比 V13 减少至少 30%，办公物件必须被图形化、印刷化、像素概括化。
- 图文融合像同一轮美术精修，不像程序 Label 贴在底图上。
- 后续可以拆出：`desk_backdrop`、`task_dossier`、`dispatch_board_base`、`selected_staff_card_frame`、`item_receipt`、`coverage_ruler`、`candidate_drawer_base`、`equipment_tray_base`、`approval_ticket_base`、`approval_cta_plate`。

## 当前阻塞

使用 OpenRouter 参考图生图会上传本地用户参考图和项目 V13 图到外部服务。需要用户明确同意后才能执行该生成步骤。
