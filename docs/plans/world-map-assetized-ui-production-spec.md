# 世界地图界面资产化生产规格

> 状态：2026-06-12 v5 生产链修正中；Codex 内置 Image 2 / 人工美术工具作为主生图入口，OpenRouter 仅作为可选脚本化后端；v4 只作为临时运行版和失败样本复盘，不再作为美术生产方式。  
> 目标：世界地图界面的视觉质感必须来自真实 bitmap 美术资源，GDScript 只承载动态文字、数值、点击、选中/禁用状态，不再用程序绘制来模拟风格稿效果。

## 1. 风格基准

- 主基准：`docs/screenshots/2026-06-11-world-map-ui-style-sheet/03-world-map-ui-style-sheet-v3-textless-modern-pixel.png`
- 局部颗粒参考：`docs/screenshots/2026-06-11-world-map-ui-style-sheet/04-world-map-ui-style-sheet-v4-micro-pixel-compare.png`
- 运行截图：`docs/screenshots/2026-06-11-world-map-assetized-v4-godot/01-world-map-assetized.png`
- 正式风格关键词：高清微像素、现代编辑部全球频道、深蓝/纸白/信号红/青色、印刷半调、轻微套印偏移、非旧档案、非羊皮纸、非纯程序扁平 UI。
- 2026-06-11 返工结论：风格稿不是“纹理参考”，而是一整套物件系统。落地时若仍保留旧列表、旧纸条 callout、旧白色日志卡，即使局部贴图资产化，也视为未通过。
- 2026-06-12 生产链修正：Pillow / GDScript 不得承担美术生产。它们只能做裁切、缩放、打包、manifest 校验和安全区 overlay；底板、按钮、pin、票据、贴纸、故事图必须由生图 / 美术工具生成，并经 `@像素艺术` 复审。

## 2. P0 资源包

当前资源放在：

```text
gd_project/Assets/ui/angus_packaging/world_map/assetized/
```

该目录暂时放置 `.gdignore`，避免 Godot 4.6.2 在导入新 PNG 时触发 native crash。运行时由 `WeeklyRunUiStyle.load_world_map_texture()` 通过 `Image.load_from_file()` 读取真实 PNG。

| 资源 | 当前文件 | 用途 | 动态层 |
| --- | --- | --- | --- |
| 世界地图底图 | `wm-world-board-v3-base.png` | 中央世界地图板、地图颗粒、扫描楔形、路线底纹 | pin、选中反馈 |
| 左索引面板壳 | `wm-panel-left-index-v4.png` | 左侧频道索引背景，只提供壳和微像素底纹，不烘入假地区行 | 标题、地区频道条、统计 |
| 右详情纸面板 | `wm-panel-right-detail-v4.png` | 右侧选区档案夹、标签页、报告图槽和 CTA 区 | 标题、正文、票据文字、按钮文字 |
| 底部频道 ticker | `wm-bottom-log-strip-v4.png` | 底部行动反馈总壳，设备条 / 电报码语法 | 日志 chip 文案 |
| 地区频道条 | `wm-region-strip-red-v4.png` / `wm-region-strip-cyan-v4.png` / `wm-region-strip-locked-v4.png` | 左侧地区条底材、色条、状态块 | 编号、地区名、线报数 |
| 票据 | `wm-ticket-deadline-v4.png` / `wm-ticket-chain-v4.png` | 红条截稿 / 青条追踪票据底材 | 票据标题、数量、说明 |
| 地图符号 pin | `wm-pin-symbol-red-v4.png` / `wm-pin-symbol-cyan-v4.png` / `wm-pin-symbol-gold-v4.png` / `wm-pin-symbol-normal-v4.png` / `wm-pin-symbol-locked-v4.png` | 中央地图可点击点。默认只显示符号，不再使用纸条 callout | 仅选中/锁定短标签 |
| 底部日志 chip | `wm-log-chip-red-v4.png` / `wm-log-chip-cyan-v4.png` / `wm-log-chip-gold-v4.png` / `wm-log-chip-next-v4.png` | 截稿、追踪、当前选区、下一步反馈底材 | chip 标题与正文 |
| 进入按钮底板 | `wm-cta-enter-region-v4.png` | 右侧主行动按钮底材 | 按钮文字、enabled/disabled |
| 故事预览图 | `wm-story-preview-v4.png` | 右侧像素异常报告图，红眼 / 城市剪影 / 半调 | 后续可替换为地区专属图 |

## 3. 接入规则

1. 纹理、纸张、色条、章圈、地图颗粒、半调、边框、按钮底板必须来自 PNG。
2. 中文文案、地区名、线报数、倒计时、宏观数值、可进入/锁定状态必须由控件动态渲染，不得烘进贴图。
3. 新贴图不得包含会被误读成真实内容的假文字、假数字、假 pin、假任务状态；装饰性状态块必须避开动态文字安全区。
4. 地图底图不得包含固定 pin 或固定中文标签，避免与真实地图状态冲突。
5. `WorldMapCanvas` 在 world 模式只保留动态选择反馈，不再绘制程序 overprint。
6. 资源接入优先使用 `StyleBoxTexture` 或运行时 `ImageTexture`；`StyleBoxFlat` 只可作为 fallback，不作为风格生产手段。
7. 地图默认 pin 必须是大号语义符号；地区名和解释文字只在左索引 / 右档案 / 选中短标签中出现，不得回退成地图纸条 tooltip。

## 4. 下一批资源

- P1：右侧故事预览按地区生成真实小图，替代当前统一红眼报告图。
- P1：左侧地区卡 hover / selected / disabled 三态单独出图，减少运行时 modulate。
- P2：顶部 header 壳、宏观状态 badge、返回主菜单按钮底图。
- P2：区域地图界面同规格资产包，不能沿用 world board。

## 5. 验收清单

- 1920x1080 截图中不能出现贴图假文字线与动态文字重叠。
- 可进入、已选、锁定三类地图点都必须可读、可点区清楚。
- 左侧地区卡、右侧票据、底部日志 chip 的文字必须落在低噪声区域。
- 新图生成后必须先交 `@像素艺术` 看风格，再交 `@UI设计` 看切片可生产性，最后交 `@UX老哥` 看可读性和状态理解。

## 6. v5 正式生产链

v5 的核心改动是：先生成整屏美术母版，再从母版派生组件 atlas，最后由 Godot 装配动态层。不得再先用程序画一套 PNG，再让程序 PNG 反过来充当风格源。

### 6.1 生产顺序

1. `ui_designer` / `ux_laoge` 确定世界层职责：只选地区，不选任务；右侧只做从属详情；主 CTA 只进入区域，不消耗天数。
2. `@像素艺术` 确认 prompt 和参考图：现代异常周刊、深海军蓝、红橙异常、暖纸、克制青色、高清微像素、半调、套印错位；禁止旧档案、旧报纸、泛黄纸、低清像素、SaaS 面板。
3. 使用 Codex 内置 Image 2 先生成 `wm_fullscreen_artboard_v5`，作为整屏母版和风格源；母版未通过，不进入组件生产。OpenRouter / 其它 API 只作为可选自动化后端，不是唯一生产入口。
4. 将被用户和 `@像素艺术` 认可的 Codex Image 2 输出图保存到本地稳定路径，再用 `stage-source` 登记到 `image_gen/codex_image2_sources/YYYY-MM-DD/`。登记只复制原图并写 metadata，不做任何美术修补。
5. 使用已批准母版作为参考，继续用 Codex Image 2 / 人工美术工具生成透明 PNG 组件和不透明底图：地图底板、左索引册、右档案夹、底部 ticker、地区条 atlas、pin atlas、票据 atlas、CTA atlas、徽记 atlas、地区故事图。透明组件若由 Codex Image 2 输出，应优先要求干净可抠的纯色背景或由人工工具导出透明 PNG；本地处理只允许抠除纯色背景、裁切、缩放和补透明留白，不得重画边框、颗粒、半调或符号。
6. 用 `scripts/art/world_map_imagegen_pipeline.py postprocess` 只做裁切、缩放、透明留白和尺寸落位，生成 manifest 指定的最终 PNG。
7. 用 `review-overlays` 生成安全区 / 禁入区 / 状态帧 overlay，交 `@像素艺术`、`@UI设计`、`@UX老哥` 复审。
8. Godot 只按 manifest 装配：`TextureRect` / `NinePatchRect` / `TextureButton` + 子 `Label` / 热区；不再用 `StyleBoxFlat` 或程序绘制模拟正式视觉效果。

### 6.1.1 视觉可使用区域先行

世界地图 v5/v6 之后的每个资产化 UI 组件，必须先定义视觉可使用区域，再进入 Godot 动态层装配。控件矩形不等于可写区域；PNG 内的书签、折角、螺丝、箭头、色条主体、强半调、纸边和装饰凸起都可能是 `no_text_rects`。

每个会承载动态文字的 asset / atlas frame 必须在生产记录或 manifest 中明确：

- `content_rects`：标题、正文、计数、状态、CTA 文案、ticker 文案的可写区。
- `no_text_rects`：禁止放动态文字的装饰区。
- `ninepatch_margin`：允许拉伸的边界，不能把装饰结构拉变形。
- `max_text`：最长汉字数、数字位数、是否允许换行和省略策略。
- `state_frames`：normal / hover / selected / disabled / locked 下文字安全区是否一致。

交付截图必须包含整屏图和关键 100% 局部裁切：右侧 CTA、红/青票据、正文框、左侧索引顶部 / 底部、底部 ticker。若文字只是在 Control 内没越界，但视觉上压到禁入装饰或贴近按钮下沿，仍判定为未通过。

### 6.1.2 v6g 当前拓展状态

2026-06-15 用户明确选择 `wm_fullscreen_artboard_v6g_pixel_strong` 作为当前强像素拓展源。v6g 不直接替换运行界面，而是按资产化链路拆成组件候选：

> 2026-06-30 分支覆盖规则：在 World Mystery Weekly 干净低多边形周刊支线中，v6g 已降级为历史 runtime-token / 资产化测试床，不再作为当前视觉标杆、组件扩展源或 crop-validation 真源。当前支线以 `docs/screenshots/2026-06-24-world-map-benchmark-landing/95-world-map-imagegen-color-recorrected-v0-51.png` 作为生图候选，以 proof v2 和 `2026-06-30-world-map-selected-region-palette-token-contract.md` 作为局部选区色号合同。

- 中央地图底板：只承载地图材质、网格、低多边形纸质大陆；pin、路线、选中圈和标签由 Godot / atlas 负责。
- 左索引栈：保留四张强像素纸卡和装订结构；每张卡的标题 / meta 文字进入 manifest 文字安全区，热区覆盖整张卡。
- 右选区档案正文：只承载预览 / 正文纸面和夹具；CTA 从右档案中拆出独立按钮组件。
- 主 CTA：独立 `TextureButton` 候选，后续必须补 `default / hover / pressed / disabled / loading` 状态 atlas。
- 底部 ticker 与右侧 tab rail：只承载无文字底材、图标语法和热区；状态文案与 tab 选择由 Godot 动态层负责。

本轮同步增强 `scripts/art/world_map_imagegen_pipeline.py`：`validate-manifest` 现在会把 `dynamic_text_rects` 与 `forbidden_zones` 的相交判为 error，并校验 `hit_rect` / `hit_rects`；`review-overlays` 会显示文字安全区、禁入区、状态帧和热区。这条校验必须在 Godot 接入前通过。

### 6.1.3 v7 功能容量合同

2026-06-16 用户确认：世界地图当前大致风格没有问题，尤其中央世界地图底图、强像素、明亮纸面和低多边形纸质地图方向应保留；下一轮问题重点是信息容量、功能分区、文字与框体贴合。后续不得继续先生成“好看的大概风格稿”，再把世界地图真实字段硬塞进去。

v7 前置合同见：

```text
docs/plans/world-map-imagegen-v7/functional-layout-contract.md
docs/plans/world-map-imagegen-v7/style-draft-prompt.md
```

v7 页面职责收窄为：选择取材地区、理解当前选中地区是否可进入 / 有何紧急状态、进入选中地区。世界地图层不得承载完整任务列表、员工 / 骰池、达标率、下一天、派遣签批或长日志。组件尺寸、`content_rects / no_text_rects / hit_rects`、字段容量和状态矩阵必须先按 v7 合同冻结，再进入下一轮 Image 2 风格稿和组件生产。

v7 允许在无文字结构稿之后额外生成一张“有字效果预览稿 / filled-state text mock”，用真实中文测试图文融合和目标截图感。该图只能指导 Godot 字体 token、字号、层级、颜色和密度，不得作为生产 PNG、切图母版或 runtime 底图。当前字段合同已按 A77 / A79 / A80 / A85 修订：顶部去掉 `阶段：取材`，左侧 `探索周 / 剩余天数` 保持周时钟纸票据，右侧五维宏观属性改为独立 `世界状态` 徽记轨 / 仪表轨，不再和左侧同框；左侧地区卡回归地区级选择建议，显示 `难度 / 推荐 / 短原因或锁定缺口`，不得显示 `目标 / 限时 / 线索 / 深链` 任务池计数；右侧选定地区标题区可重复 `难度 / 推荐` 作为选中确认；右侧大正文纸面只承载一段连续的选定地区文本简介，不再拆成 `地区特征 / 本周异变 / 可带回素材 / 地区预警` 等正文内模块，不得写入任务摘要、任务数量、任务名或任务预览行；任务池信息只通过地区图像下方、红色状态条下方的青色独立次级票据打开只读 popover，标准按钮文案为 `查看任务情报 · N`，按钮应包含当前已知可预览任务总数，如 `查看任务情报 · 3`，且必须左右缩进、与正文纸面留 12-16px 空气层、具备箭头 / 查看动作区 / hover / pressed / open 状态，不得做成贴在正文纸面上沿的满宽蓝色标题栏；popover 最多显示 2-3 条任务缩略预览，不得包含任务选择、派遣、员工、骰池、达标率、成功率或完整任务详情；主 CTA 在 ready state 固定为 `进入选定地区`，在 blocked state 固定为 `暂不可进入`；底部三格改为低权重且可点击的详情入口 `地区情报 / 档案更新 / 地区预警`，不再使用 `任务小结` 作为第二个任务指标显示位。其中 `地区预警` 用来承载进入该地区可能带来的惩罚、debuff、封锁、异常污染或其它行动影响。当前 A77 目标截图为 A79 / A80 前的参考，后续需按 A80 / A85 重新出目标稿：

```text
docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/03-world-map-v7-difficulty-rating-task-intel-popover.png
```

P0/P1 ready / blocked 目标截图 `01-world-map-v7-p0p1-real-info-text-mock.png` 与 `02-world-map-v7-p0p1-blocked-state-text-mock.png` 只作为“选中地区闭环 / 锁定地区闭环”的历史参考；其中左卡和右侧摘要里的任务池计数已被 A77 覆盖，不得作为当前字段合同。

v4 图 `05-world-map-v7-filled-state-text-mock-v4.png` 只作为“顶部五维 / CTA / ticker 方向正确但功能等价不足”的中间稿：它缺少清晰的旧网页版四项区域摘要、锁定缺口完整语法和真实地区情报预览，不得作为最终字段合同参考。

v1 图 `02-world-map-v7-filled-state-text-mock.png` 只能作为错误字段案例：它缺少地区简介、顶部缺五维、CTA 拼接动态地区名、底部像功能条，不得作为后续组件或 Godot 字段合同参考。

### 6.2 机器可读文件

```text
gd_project/Assets/ui/angus_packaging/world_map/imagegen_v5/world_map_imagegen_manifest.json
docs/plans/world-map-imagegen-v5/prompt-bundle.json
docs/plans/world-map-imagegen-v5/postprocess-mapping.example.json
gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json
docs/plans/world-map-imagegen-v6/prompt-bundle.json
docs/plans/world-map-imagegen-v6/componentization-spec.md
docs/plans/world-map-imagegen-v6/postprocess-mapping.v6g-components-candidate.json
docs/plans/world-map-imagegen-v7/functional-layout-contract.md
docs/plans/world-map-imagegen-v7/style-draft-prompt.md
docs/plans/world-map-imagegen-v7/filled-state-text-mock-prompt.md
docs/plans/world-map-imagegen-v7/filled-state-text-mock-blocked-prompt.md
docs/plans/world-map-imagegen-v7/filled-state-text-mock-review-2026-06-16.md
docs/plans/world-map-imagegen-v7/filled-state-text-mock-v2-review-2026-06-16.md
docs/plans/world-map-imagegen-v7/filled-state-text-mock-v3-review-2026-06-16.md
docs/plans/world-map-imagegen-v7/filled-state-text-mock-v4-review-2026-06-16.md
docs/plans/world-map-imagegen-v7/filled-state-text-mock-p0p1-review-2026-06-17.md
docs/plans/world-map-imagegen-v7/difficulty-rating-task-intel-popover-prompt.md
docs/plans/world-map-imagegen-v7/difficulty-rating-task-intel-popover-review-2026-06-17.md
docs/plans/world-map-imagegen-v7/right-prose-task-count-button-prompt.md
docs/plans/world-map-imagegen-v7/a80-task-intel-button-affordance-review-2026-06-17.md
scripts/art/world_map_imagegen_pipeline.py
gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssetManifest.gd
```

`world_map_imagegen_manifest.json` 是 v5 资产契约：每个资源必须声明最终尺寸、背景透明 / 不透明、推荐模型、Godot 节点类型、运行时 rect、九宫格边距、状态帧、文字安全区、禁入区、地图热区和复审 gate。

`prompt-bundle.json` 是生图计划：第一阶段只跑整屏母版；母版经用户和 `@像素艺术` 通过后，才把母版路径填入 `APPROVED_ARTBOARD` 继续跑组件。当前主路径是把 prompt 交给 Codex 内置 Image 2 生成；文件里的 `model` 字段保留为可脚本化后端的建议，不代表必须走 OpenRouter。

`postprocess-mapping.example.json` 是裁切映射模板：把已批准的 Codex Image 2 / 人工美术工具 / OpenRouter 输出图映射到 manifest 中的最终 PNG。后处理只能裁切 / 缩放 / 补透明，不得画边框、噪点、半调、符号或文字。

`imagegen_v5/.gdignore` 是临时导入保护：Godot 4.6.2 之前导入新 PNG 时出现过 native crash，因此 v5 资源默认先由运行时 `Image.load_from_file()` 路径读取；确认导入链稳定前，不把新图直接交给 Godot importer。

`WeeklyRunWorldMapAssetManifest.gd` 是后续接入 Godot 的统一读取口：按 manifest 的 `asset_id` 找最终 PNG、运行时加载纹理、读取运行时 rect 与文字安全区。当前文件只提供入口，不替换现有 world 层画面。

### 6.3 工具命令

校验 manifest：

```powershell
python scripts/art/world_map_imagegen_pipeline.py validate-manifest
```

输出 Codex Image 2 生图 prompt 包：

```powershell
python scripts/art/world_map_imagegen_pipeline.py codex-prompt --job 01_fullscreen_artboard
```

将 Codex Image 2 / 人工美术工具输出登记进仓库源图目录：

```powershell
python scripts/art/world_map_imagegen_pipeline.py stage-source --asset wm_fullscreen_artboard_v5 --job 01_fullscreen_artboard --source "C:\path\to\selected-image.png" --slug approved-angus-world-map-v5-artboard
```

输出 OpenRouter 整屏母版 dry-run 命令（可选脚本化后端）：

```powershell
python scripts/art/world_map_imagegen_pipeline.py emit-commands --stage artboard --dry-run
```

直接执行 OpenRouter 整屏母版 job（可选脚本化后端，需要已配置 OpenRouter key，且模型在当前区域可用）：

```powershell
python scripts/art/world_map_imagegen_pipeline.py run-job --job 01_fullscreen_artboard
```

母版通过后，输出 OpenRouter 组件 dry-run 命令（可选脚本化后端）：

```powershell
python scripts/art/world_map_imagegen_pipeline.py emit-commands --approved-artboard "image_gen/YYYY-MM-DD/APPROVED_angus-world-map-v5-artboard.png" --dry-run
```

母版通过后，执行单个 OpenRouter 组件 job（可选脚本化后端）：

```powershell
python scripts/art/world_map_imagegen_pipeline.py run-job --job 08_pin_atlas --approved-artboard "image_gen/YYYY-MM-DD/APPROVED_angus-world-map-v5-artboard.png"
```

裁切已批准生成图：

```powershell
python scripts/art/world_map_imagegen_pipeline.py postprocess --mapping docs/plans/world-map-imagegen-v5/postprocess-mapping.example.json
```

校验最终 PNG 是否满足 manifest 尺寸 / 透明度：

```powershell
python scripts/art/world_map_imagegen_pipeline.py validate-final-assets
```

生成安全区复审 overlay：

```powershell
python scripts/art/world_map_imagegen_pipeline.py review-overlays
```

### 6.4 当前阻塞

OpenRouter 在当前环境中已不作为主路径。若后续仍要使用 OpenRouter 自动化后端，需要保证 `skills/openrouter-image-gen/config.env` 存在且 `OPENROUTER_API_KEY` 有效，并确认目标图像模型在当前账号 / 区域可用。主路径改为 Codex 内置 Image 2：由 Codex 生图，人选通过后用 `stage-source` 纳入同一套 postprocess / validate / overlay / Godot manifest 管线。

### 6.5 v5 P0 验收

- 生图资产不能包含中文正文、地区名、倒计时、材料数、任务标题、按钮文案、假 pin、假状态条或假任务卡。
- 地图 pin、左索引、右档案三处的已选 / 可进入 / 锁定 / 截稿 / 追踪状态必须一致。
- 视觉 pin、热区、反馈锚点必须来自同一份 manifest；锁定区可以预览但不可进入时，不能使用主可点击语法。
- 动态文字安全区必须为低噪声区域，半调、折痕、红青错位和纸纹不得穿过正文、数字和 CTA 文案。
- 右侧必须读作“选中地区从属详情 / 档案夹”，不得读作可点击任务列表。
- 截图验收覆盖 1920x1080、1600x900、1366x768 三个桌面 16:9；默认可进入、选中锁定、hover/selected/disabled 状态都要截。

### 6.6 v7 P0/P1 Godot 运行层落地

2026-06-17 已把 P0/P1 信息合同接入当前 Godot 世界地图动态层，截图：

- `docs/screenshots/2026-06-17-world-map-p0p1-godot/01-world-map-p0p1-ready.png`
- `docs/screenshots/2026-06-17-world-map-p0p1-godot/02-world-map-p0p1-locked.png`
- A80 functional split preview:
  - `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/01-world-map-a80-functional-preview.png`
  - `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/02-world-map-a80-task-popover-open.png`
  - `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/03-world-map-a80-safe-zones.png`

已落地范围：

- CTA 固定为 `进入选定地区` / `暂不可进入`，不再拼接地区名。
- 左侧地区卡、地图 pin、右侧档案、CTA、底部 ticker 共享同一个选定地区状态。
- 右侧大正文纸面只渲染一段连续的选定地区文本简介；`地区情报 / 档案更新 / 地区预警` 不在正文里拆成多块，`目标 / 限时 / 线索 / 深链` 等任务池信息也不再出现在左卡或正文，只能通过红色状态条下方的次级 `查看任务情报 · N` 独立票据入口打开只读预览。该票据必须左右缩进、带动作提示和状态反馈，不得贴成正文纸面的蓝色标题栏。
- 底部三条固定承担 `地区情报 / 档案更新 / 地区预警` 的可点击详情入口，不再做教程提示、当前地区重复显示或任务指标复读。
- 锁定地区可被选中预览缺口，但入口按钮保持 disabled，进入逻辑仍由 Godot 检查。
- A80 预览把当前风格稿拆成更接近最终组件职责的运行态：左侧地区索引、中央地图、右侧档案、状态票据、任务情报票据 / 弹窗、CTA、底部反馈条。该预览用于锁定功能分区、文字容量和交互边界。

未完成范围：

- 这不是正式 v7 无字 PNG 组件替换；当前仍复用现有 assetized world-map 底材。
- 后续必须按 `docs/plans/world-map-imagegen-v7/functional-layout-contract.md` 生产无字组件、状态 atlas、content rect、hit rect 和安全区 overlay，再替换 Godot 资源入口。
- 当前安全区截图同时暴露 legacy v6g manifest 与 A80 新动态区的差异；正式 v7 拆图必须重新写 manifest，不应直接沿用 v6g 安全区作为验收真源。

### 6.7 v7 A80 兼容性失败复盘

2026-06-18 用户复审指出 A80 Godot 预览存在明显问题：旧右侧版面与新设计不兼容，地区图样飞出纸面，按钮和状态条没有稳定承载槽位。该截图不得继续作为世界地图目标 UI 或生产拆图母版，只能作为“旧底板硬贴新功能”的失败样本。

复盘结论：

- 旧右侧纸面 / 档案底板不是万能容器。它的夹子、书签、边栏、点阵、纸边和侧标签已经烘焙了原有功能结构，不能自动承载新的大图、状态条、任务票据和 CTA。
- `Control rect` 能放下不等于视觉可用区能承载。任何动态图 / 字 / 按钮都必须先通过 `content_rects / no_text_rects / hit_rects` 和 100% 裁切检查。
- 有字效果稿、运行骨架图、no-text 生产组件必须分开命名和验收。不能把旧底图上叠 Label / Button 的截图当作资产化落地完成。
- 下一轮世界地图 v7 必须先做右侧地区档案的新结构验证稿，冻结 header、media viewport、alert strip、task-intel ticket、single region intro prose body、CTA / footer 的尺寸和容量，再进入无字组件生图。`地区情报 / 档案更新 / 地区预警` 不再塞入右侧正文纸面，改由底部 clickable ticker 作为详情入口承载。

新增硬 Gate：

- `legacy_container_compatibility_gate`：复用旧组件前，逐项检查新功能槽是否被旧装饰、边栏、夹子、纸边、相框、半调、标签挤占。若任一关键槽必须浮在旧图上或压进装饰区，旧组件直接判失败。
- `100_percent_crop_gate`：整屏图通过不算通过；必须附右侧档案、地区图槽、红色状态条、任务情报票据、CTA 的 100% 裁切并逐项确认没有飞图、贴边、遮挡、浮层错位。
- `component_contract_gate`：正式拆图前必须已有 fresh manifest 草案，包括 `media_viewport` mask、按钮状态 atlas、文本容量、长文案溢出策略和 disabled / hover / pressed / open 状态。
- `ticker_detail_gate`：底部 `地区情报 / 档案更新 / 地区预警` 必须读作可点击详情入口，具备 type chip、短标题、动作箭头、hover / open 状态；点击后只打开只读详情，不进入任务选择、派遣、骰池或成功率页面。

后续结构验证稿 V1 已生成；其右侧单简介 + 底部详情入口方向已被用户接受，后续不作为美术源，只作为容量与结构合同：

- `docs/screenshots/2026-06-18-world-map-v7-right-dossier-structure/01-world-map-v7-right-dossier-structure-wireframe.png`
- `docs/screenshots/2026-06-18-world-map-v7-right-dossier-structure/02-right-dossier-structure-100pct-crop.png`
- `docs/plans/world-map-imagegen-v7/right-dossier-structure-wireframe-v1-2026-06-18.md`

真实内容填充稿 V1 已生成，用于进入 Image 2 风格稿前检查字段容量、中文长度和点击详情层；它不是生产美术资源，也不是 no-text PNG：

- `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/01-world-map-v7-filled-content-mock.png`
- `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/02-right-dossier-filled-content-100pct.png`
- `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/03-bottom-ticker-warning-detail-open.png`
- `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/04-bottom-ticker-100pct.png`
- `docs/plans/world-map-imagegen-v7/filled-content-mock-v1-2026-06-18.md`

### 6.8 v7 现代纸品体积感与可点击 Gate

2026-06-18 用户明确要求：世界地图后续可以继续向参考图的现代印刷纸品、高级概括地图和干净色系靠拢，但各功能分区、特殊区域和可点击按钮必须保留明确体积感与功能可见性；不能为了扁平、清爽或高级感，把按钮做成不可辨认的静态纸片。

资产与风格稿必须同时满足：

- `modern_print_material_gate`：整体读作现代异常周刊 / 现代印刷纸品，而不是旧档案、审批表、旧办公资料夹、泛黄旧报纸或金属 HUD。
- `paper_volume_gate`：按钮、地图 pin、左侧 selected 卡、底部 ticker 可点击项和主 CTA 的体积感来自纸层抬升、短投影、纸边厚度、压印、裁切、套印错位和 pressed 下压，不来自写实金属、锈蚀螺丝、厚重旧机器或手游 3D bevel。
- `clickability_gate`：所有可点击对象必须比只读纸面更像可操作物件，至少定义 `default / hover / pressed / selected / disabled / locked` 中适用状态；只读纸面、书签、折角、半调点阵和装饰夹具不得共享按钮语法。
- `scope_separation_gate`：当前任务 CTA 与全局推进动作继续保持空间、颜色、材质、atlas、hit rect 和确认态分离；不得因为重新包装而再次相邻或同托盘化。
- `safe_zone_gate`：体积阴影、纸边、箭头、压印和半调不能压入 `content_rects`；100% 裁切必须检查主 CTA、左卡、地图 selected pin、右侧标题 / 正文、底部 ticker 详情入口。

下一轮 Image 2 prompt 应把“tactile clickable paper buttons / raised paper CTA / lifted paper tabs / clear hover pressed state design”列入正向词，同时把 “no old archive paper / no bureaucratic approval form / no realistic metal gradient / no generic mobile game buttons / no glossy capsule buttons” 列入负面约束。任何视觉稿若只解决老旧感，却让玩家看不出哪里可点，应标为交互失败稿，不进入拆图。
