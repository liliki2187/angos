# 世界地图 · 标杆落地流程 v0.1

> 日期：2026-06-24  
> 状态：标杆落地试产，不是最终 UI，不是 Godot 落地稿。  
> 目标：用世界地图界面验证“先保标杆味，再拆组件，再替换运行时”的新流程。

## 1. 输入

### 1.1 当前世界地图结构来源

- 最新填充稿：`docs/screenshots/2026-06-23-world-map-clean-lowpoly-style-target/11-v2-1-filled-state-text-mock.png`
- 右侧 crop：`docs/screenshots/2026-06-23-world-map-clean-lowpoly-style-target/12-v2-1-filled-right-dossier-crop.png`
- 生产合同：`docs/screenshots/2026-06-23-world-map-clean-lowpoly-style-target/production-contract.md`

当前世界地图承担的玩家决策：

```text
选择地区 -> 看懂能否进入 / 是否值得进入 -> 进入选定地区
```

不承担：任务选择、员工派遣、骰池、成功率、任务详情列表。

### 1.2 标杆约束

世界地图不能只变成“更干净的策略地图 UI”。必须保留标杆 DNA：

- 高密度现代周刊资产板。
- 大纸件、dossier、文件夹叠层。
- 橄榄绿 / 芥末黄 / 蓝色文件夹和米白纸面。
- 贴纸、夹子、色票、条码、图标 atlas。
- 低多边形快照不只出现在地图上，也出现在组件样本里。
- 红橙只给危险和主 CTA。

## 2. 生成产物

### 2.1 世界地图组件母版

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/01-world-map-component-motherboard-v0.png`

用途：

- 验证“世界地图组件”能否贴近用户标杆。
- 统一世界地图页的组件词汇：地区文件夹、地图板、右侧 dossier、pin / sticker、ticker receipt、日程 dock、CTA atlas。
- 不作为最终可玩整屏 UI，不直接切图。

通过点：

- 标杆资产板密度和纸件叠层已经回来。
- 世界地图专属组件足够完整，不再是泛 moodboard。
- 左卡、地图、右 dossier、ticker、schedule、CTA 的组件身份清楚。

问题：

- 仍有少量英文标题 / 编号被模型生成出来。生产母版需要禁掉可读字。
- 右侧 dossier 的正文和票条还只是方向样本，未做精确安全区。
- 地图板偏像组件展示，不是运行时尺寸合同。
- 生成后复审新增问题：地图、地区卡和快照的低多边形颗粒度过碎，偏细三角网 / GIS 终端纹理，缺少标杆的大块概括和手绘裁纸感。
- 票据 / ticker / 横条组件微细节过多，孔洞、短线、条码、点阵和边缘缺口同时出现，读成票券素材包，而不是大块印刷物件。

结论：仅可作为“世界地图组件词汇方向草稿”，不可作为生产标杆；其中图像颗粒度和票据细节密度需按 §2.3 返工。

### 2.2 右侧地区 dossier 组件稿

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/02-right-dossier-component-sheet-v0.png`

用途：

- 抽世界地图 P0 组件：右侧选定地区 dossier。
- 作为下一步 `无字底图 -> 安全区 overlay -> 真实中文填充` 的视觉来源。

通过点：

- 结构接近世界地图合同：header、snapshot、red alert ticket、secondary task-intel ticket、prose body、footer、primary CTA。
- 可写区域基本正交，适合后续叠运行时中文。
- 红色主 CTA 与青色次级票条有明显层级。
- 纸张、夹子、文件夹、低多边形快照、贴纸的标杆味比旧世界地图右栏更强。

问题：

- 作为 sheet 有右侧状态样本和色票，不能直接当单组件 PNG。
- 主 dossier 内部还有少量伪文字条，需要生产版进一步清洁。
- CTA 与任务情报票条需要状态 atlas 分帧，而不是从 sheet 直接裁。
- 快照偏写实照片 / 雾状摄影质感，低多边形块面只在背景隐约出现；下一版应重画为大块概括低多边形插图。
- 红色 / 青色票条内部线框、缺口、斜纹和微线偏多；下一版应保留更少、更大的形状关系。

结论：可作为右侧 dossier 信息结构参考，不可直接进入 P0 组件拆分；下一步应先做“低细节、大块面”的右侧 dossier v0.2，再做三件套。

### 2.3 生成后复审：大块面返工要求

`@像素艺术` 复审结论：当前 5 个裁切都不能作为“世界地图组件生产标杆”，只能算方向草稿。核心偏差不是“不够低多边形”，而是低多边形执行成了密集细网格、高清照片纹理和票据微装饰。

返工规则：

| 对象 | 当前偏差 | v0.2 要求 |
| --- | --- | --- |
| 世界地图板 | 大陆海岸线、小岛、三角网、扫描点过密，偏 GIS / 雷达终端 | 大陆概括成更少的大块面；海岸线简化；删减小岛和微点；北美高亮用 6-10 个大块主面 |
| 地区文件夹卡 | 地图图形太小、太灰、太碎，图标比主图形抢 | 每张卡先成立大块文件夹色面；地图缩略图用大块剪影 / 大块多边形，不追求细节 |
| 横条 / CTA | 内部线框、边缘缺口、斜纹、细槽过多 | 每条只保留 1 个主形状 + 1 个状态装饰；文字槽保持干净 |
| ticker 票据 | 孔洞、条码、短线、点阵、阴影都在抢 | 去掉大多数孔洞和条码；每张票据只保留一个大图标、两三条大文本占位、少量结构半调 |
| dossier 快照 | 写实雷达、天空、雾气、照片颗粒过重 | 改为大块低多边形插图；主体用少量几何块表达，禁止摄影雾气和细雷达结构 |

下一轮 prompt 必须包含：

```text
large simplified low-poly planes, bold blocky polygon shapes, editorial cut-paper graphic design, slightly hand-drawn imperfect polygon edges, halftone as large structured patches, minimal micro-detail, strong negative space
```

下一轮 prompt 必须排除：

```text
no dense triangulation mesh, no tiny polygon web, no small holes, no barcode clutter, no scattered speckle noise, no photographic grain, no GIS terminal map detail, no overly detailed coastlines, no decorative micro-lines, no texture covering text areas
```

## 3. 右侧 dossier 三件套要求

### 3.1 无字 bitmap 底图

目标组件：

```text
wm_right_dossier_benchmark_base_v0
```

必须包含：

- 纸张叠层和文件夹标签。
- 顶部夹子 / 回形针，但不压标题区。
- 低多边形地区快照框。
- 红色 alert ticket 底。
- 青色 / 橄榄 task-intel ticket 底。
- 大块干净 prose paper。
- footer hint strip。
- 底部红橙 primary CTA ticket。

不得包含：

- 可读中文 / 英文 / 数字。
- 地区名、按钮文案、任务数量。
- 假任务列表、员工、骰子、成功率。
- 斜的正文纸面。

### 3.2 安全区 overlay

建议 rect：

| rect | 说明 |
| --- | --- |
| `header_title_rect` | 地区标题，1 行 |
| `header_badge_rects` | 难度 / 推荐 / 状态短 badge |
| `snapshot_rect` | 地区快照，无文字 |
| `alert_ticket_rect` | 红线 / 状态短句 |
| `task_intel_ticket_rect` | `查看任务情报 · N`，独立点击 |
| `prose_rect` | 单段地区介绍，70-110 中文字 |
| `footer_hint_rect` | 进入条件 / 后果 |
| `primary_cta_rect` | `进入选定地区` |

`no_text_rects`：

- top clip / paper clip。
- dossier 右侧 tabs。
- paper edges / folded corners。
- snapshot image area。
- CTA 右箭头 / stamp / cutout。
- strong halftone / barcode / sticker edges。

### 3.3 真实中文填充预览

必须用当前世界地图真实字段：

- 地区：北美禁区。
- 状态：红线升温。
- 难度：高。
- 推荐：3。
- 收益窗口：3 天。
- 进入消耗：1 天。
- 可见任务：3。
- CTA：进入选定地区。

验收：

- 100% crop 下中文不压纹理、不压夹子、不贴边。
- `查看任务情报 · 3` 像可点击票条，不像正文标题。
- CTA 是唯一红橙主动作。
- 右侧 dossier 仍像标杆纸件，不退回普通面板。

## 4. 世界地图替换顺序

1. 先做右侧 dossier 三件套。
2. 再做左侧 region folder card atlas。
3. 再做 primary CTA / task-intel ticket state atlas。
4. 再做 map pin / sticker atlas。
5. 再做 bottom ticker receipt lanes 和 schedule dock。
6. 最后才整合全屏背景和中央地图板。

不建议现在直接重生整屏可玩世界地图。整屏会再次稀释标杆，先让 P0 组件成立。

## 5. 当前判断

本轮已经完成：

- 功能骨架冻结：使用现有世界地图 v2.1 填充稿。
- 标杆组件母版：已生成 v0。
- P0 组件抽取：已生成右侧 dossier component sheet v0。

未完成：

- 右侧 dossier 无字单组件底图。
- 安全区 overlay。
- 真实中文填充预览。
- `@像素艺术` 生成后复审。

下一步建议（已根据生成后复审修订）：

```text
先重做右侧 dossier v0.2：大块低多边形快照 + 低微细节票条 + 干净文字安全区。
通过风格复审后，再做无字单组件底图 + overlay + 中文填充预览。
```

这一步过了，再开始左侧地区卡 atlas。

## 6. v0.3 色块塑形试稿阶段判断

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/04-world-map-ui-v0-3-colorblock-draft.png`

用户反馈：

```text
这个风格大致是对的。
```

阶段判断：

- v0.3 比 v0 / v0.2 更接近当前新标杆：视觉力量主要来自低多边形大色块、明暗面、硬边阴影和干净纸件，而不是纸纹、孔洞、噪声和微细节。
- 右侧 dossier、左侧地区卡、底部票据已经具备继续拆成组件的价值。
- 中央世界地图仍有偏碎问题，尤其小岛、海岸、内部切面和地图边框细节；不可直接作为最终地图底图。
- v0.3 是“阶段性方向稿”，不是生产标杆，也不是可直接切片使用的 UI 资产。

下一步验证链：

1. 右侧 dossier 单组件验证：生成无字底图，标出 `content_rects / no_text_rects / hit_rects`，用真实中文填充。
2. 左侧地区卡 atlas 验证：default / hover / selected / locked / warning 五态，使用同一色块塑形规则。
3. 中央世界地图底图验证：重做更概括的大陆剪影，删减小岛、海岸细节和密集切面。
4. Godot / HTML 真实界面验证：在 1920x1080 桌面画面中接入真实动态字段，截图检查可读性、点击边界和状态层级。
5. 生成后复审：若候选要升级为生产标杆，必须再交 `@像素艺术` 检查色块塑形、微细节密度、动态文字安全区和标杆继承。

## 7. 右侧 dossier v0.4 单组件承载验证

产物：

| 文件 | 用途 |
| --- | --- |
| `docs/screenshots/2026-06-24-world-map-benchmark-landing/05-right-dossier-base-v0-4.png` | 无字底图 |
| `docs/screenshots/2026-06-24-world-map-benchmark-landing/06-right-dossier-safe-zones-v0-4.png` | `content_rects / no_text_rects / hit_rects` 安全区 overlay |
| `docs/screenshots/2026-06-24-world-map-benchmark-landing/07-right-dossier-chinese-fill-v0-4.png` | 真实中文填充预览 |
| `docs/screenshots/2026-06-24-world-map-benchmark-landing/08-right-dossier-validation-contact-sheet-v0-4.png` | 三图对照表 |

验证结果：

- 通过：无字底图能承载真实中文；标题、状态、alert ticket、task-intel ticket、正文、footer、CTA 均有可写区，不需要把字压在纹理、斜纹、夹子或图像上。
- 通过：纸面整体较干净，视觉质感主要来自低多边形大色块、硬边阴影和纸件压层，不再靠孔洞、脏点、条码和微线堆叠。
- 通过：红橙主 CTA 与 alert ticket 层级清楚；青绿 task-intel ticket 能作为次级可点击入口。
- 待修：snapshot 仍偏规则三角面，天空和山体的切面数量偏多；下一版应更像手绘概括的大色块，而不是标准 low-poly 渲染。
- 待修：票条边缘仍略有通用游戏按钮 / bevel 感；下一版需要让它更像印刷纸签和套印压层，而不是按钮框。
- 待修：右侧 folder tabs 与纸边可保留，但真实界面中需要检查是否遮挡鼠标命中区或右栏边界。

结论：

`05-08` 可作为“右侧 dossier 真实承载验证通过稿”，但不是生产标杆。下一步应把 `07-right-dossier-chinese-fill-v0-4.png` 缩放接入 1920x1080 世界地图布局中，检查它和中央地图、左侧地区卡、底部状态条共同出现时是否仍保留 v0.3 的标杆方向。

### 7.1 1920x1080 尺度验证补充

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/09-world-map-1920-dossier-v0-4-validation.png`

验证结果：

- 通过：右侧中文在 1920x1080 桌面比例中仍能阅读，标题、alert、task-intel、正文和 CTA 层级清楚。
- 通过：右侧 dossier 与左侧地区卡、中央地图同屏时没有明显风格断裂，仍保留 v0.3 的色块塑形方向。
- 待修：当前右栏占屏偏大，压到中央地图右侧；正式布局应给右栏预留固定列，或把 dossier 缩到约 520-580px 宽。
- 待修：中央地图自身仍偏碎，尤其海岸、小岛和内部切面；不应因为右栏验证通过而直接放行中央地图。

结论：`05-09` 可作为右侧 dossier 的落地验证包；下一步进入左侧地区卡 atlas 五态验证，并同步为中央地图预留右栏安全列。若要把本 dossier 方向升级为生产候选，必须再交 `@像素艺术` 做生成后复审。

### 7.2 票条 / 符号 v0.5 纠偏样本

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/10-ticket-symbol-atlas-v0-5-handdrawn.png`

用户反馈来源：

- v0.4 票条框体内的细微色块 / 低多边形变化不足，显得过平。
- 按钮图样过于规整，符号应更接近标杆贴纸区：概括、手绘、剪纸、轻微歪斜。

v0.5 采用的修正：

- 票条彩色框体内恢复轻微大块低多边形明度变化，中心可写区也保留极轻的色块压层，不做纯平白框。
- 图标从标准 UI icon 改为贴纸式手绘符号：厚线、概括轮廓、剪纸白边、不规则色块。
- 保留大面积 `content_rect`，不让低多边形色块和符号进入动态文字区。

结论：v0.5 只保留为“手绘 / 色块找回”的局部方向样本；它仍有明显土、暗、厚、泥色问题，不能作为高级感通过样本或生产 atlas。下一步接入真实中文前，需要先通过小组件高级感 / 舒适度闸门，再验证轻微色块不会压低文字可读性。

### 7.3 票条 / 符号 v0.6 高级感纠偏样本

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/11-ticket-symbol-atlas-v0-6-premium-light.png`

用户反馈来源：

- v0.5 相比远标杆的小组件不够舒服、不够高级，整体显得土土暗暗。
- 问题不在于“细节不够”或“手绘不够”，而在于纸边过厚、暗部过死、阴影过重、橄榄 / 红色偏泥，整体滑向暗沉手工贴纸。

v0.6 采用的修正：

- 提亮纸边和可写区，让白边更薄、更干净。
- 降低厚重阴影和死黑暗部，保留纸层体积但减少手账 / craft paper 感。
- 让橄榄绿、青绿和红橙更清爽，避免土黄、棕黄、脏绿主导。
- 保留框体内轻微低多边形色块，不回到纯平按钮。

结论：v0.6 可以作为“修正土暗厚”的边界样本，但颜色未通过。它出现了过亮、过白、略规整的问题，尤其 `paper_high #F3E8D9` 明显高于标杆约 `#C2BAAC`，`olive_mid #747945` 高于标杆约 `#4E623D`，`warning_rust #BD4F26` 过鲜。下一轮应按色彩合同先把纸边、橄榄绿和警示红橙压回标杆，再把远标杆贴纸区的概括歪斜、黑色图形张力和怪异周刊味合并。

### 7.4 票条 / 符号色彩合同 v0.1

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/12-ticket-symbol-color-contract-v0-1.md`

关键目标：

- `paper_high`：标杆约 `#C2BAAC`，禁止 v0.6 的亮白 `#F3E8D9`。
- `paper_mid`：`#B2AB9B` - `#BCB4A5`，动态可写区不能惨白。
- `olive_mid`：`#4E623D` - `#5B6A37`，禁止偏黄偏亮的 `#747945`。
- `warning_rust`：`#6D462D` - `#8A4E32`，禁止鲜红橙 `#BD4F26`。
- `teal_blue`：约 `#384946` / `#293C41`，不要因整体压暗继续变黑。

结论：v0.7 不能用“整体暗一点”或“整体亮一点”调色，必须分 token 复采样。

### 7.5 票条 / 符号 v0.7-v0.8 迭代

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/13-ticket-symbol-atlas-v0-7-benchmark-palette.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/14-ticket-symbol-atlas-v0-8-color-corrected.png`

结论：

- v0.7 把纸边从 v0.6 的过亮白收回，但深墨、背景和青蓝被压得过黑。
- v0.8 保留了较好的纸边与红橙收敛，写字区比 v0.7 干净，整体更接近远标杆贴纸区的“现代周刊贴纸”。
- v0.8 仍不是生产 atlas：`ink_dark`、`background_dark`、`teal_blue` 自动采样仍偏暗；纸面 `paper_mid` 略亮，需要真实中文填充后检查。

下一步：不要继续只在单独 atlas 里打磨。应把 v0.8 作为候选塞回右侧 dossier / 左侧地区卡的小范围真实 UI 验证，看它在 1920x1080 世界地图里是否仍舒服、高级、可读。

### 7.6 票条 / 符号 v0.9 色彩复核

路径：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/15-ticket-symbol-atlas-v0-9-palette-match.png`

结论：

- v0.9 是目前色彩最接近标杆的小组件候选，但仍不能称为“色号一样”。
- 接近项：`paper_high #C1B6A2` 对标 `#C2BAAC`，`paper_mid #B5AB96` 对标 `#B2AB9B`，`olive_mid #515A36` 对标 `#4E623D`，`background_dark #131719` 对标 `#191C1E`。
- 未同色项：`red_orange #6D331D` 与标杆低饱和暗红棕仍有较大 RGB 距离；`ink_dark #131719` 仍比标杆 `#272A2B` 黑；`teal_blue #2F403E` 仍偏暗。

下一步：

- 若继续追色，只修 `ink_dark / teal_blue / red_orange` 三个 token，不再动纸色和橄榄。
- 若目标是完全同色，纯生图 prompt 不可靠，应转为固定 ROI + 后期调色 / LUT / 分层资源流程。

### 7.7 票条 / 符号 v0.10-v0.16 三 token 修色

当前候选：

`docs/screenshots/2026-06-24-world-map-benchmark-landing/22-ticket-symbol-atlas-v0-16-minimal-clean-color.png`

取舍：

- v0.10 是较稳的生图底稿。
- v0.11 / v0.12 没有有效修正墨色，且部分色块变暗。
- v0.13 / v0.14 尝试局部 LUT，数值改善但暗按钮和红按钮出现修色斑点。
- v0.15 数据最接近，但斑点明显，不采用。
- v0.16 保留 v0.10 的干净观感，同时让背景和青蓝更接近标杆；作为当前真实 UI 验证候选。

注意：

- v0.16 仍不是 exact 色号通过。`paper_high / paper_mid / background_dark / teal_blue` 已接近，`ink_dark` 和 `red_orange` 仍不能用全图自动 mask 判定通过。
- 后续如继续追色，必须改用固定 ROI 吸管点；否则大面积背景会污染 `ink_dark` 统计。

### 7.8 世界地图局部落地验证 v0.17-v0.19

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/23-world-map-local-validation-v0-17-v016-components.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/24-world-map-local-validation-v0-18-large-blocks.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/25-world-map-local-validation-v0-19-orthogonal-info-surfaces.png`

验证目标：

- 不再单独磨票条 atlas，而是把 v0.16 的票条 / 贴纸语言放回世界地图真实结构中观察。
- 覆盖中心世界地图、左侧地区卡、右侧 dossier、底部 ticker / receipt lane 四类高频组件。
- 仍属于“局部落地验证稿”，不是生产界面，也不是可切片运行时底图。

v0.17 结果：

- 通过：整体布局能读成世界地图界面，右侧 dossier、左侧地区卡和底部票据没有退回纯功能面板。
- 通过：票条基本保留 v0.16 的纸件 / 贴纸语言，颜色没有回到 v0.6 的过亮白。
- 未通过：中心地图和右侧快照仍偏密集低多边形渲染 / GIS 感，三角切面过多。
- 未通过：底部票据出现小孔、刻度和微细节，背离标杆“大块概括”的要求。

v0.18 修正：

- 把中心世界地图改成更少切面的大陆剪影，北美选中区用大块橄榄 / 青绿色面表达。
- 压掉票据小孔、条码、微线和散点，只保留大图标、大写字区和宽色块。
- 贴纸图标继续保持手绘、厚线、剪纸白边，而不是标准矢量 UI icon。
- 整体色调继续按 v0.16 收敛，不追求亮白高级感，也不回到土暗手账感。
- 失败：右侧 dossier、左侧地区卡和底部票据出现整体倾斜。凡承载动态信息 / 可点击热区 / 文字安全区的界面物件必须 0 度正交，v0.18 只能作为“大块面修正有效、正交规则失败”的偏差样本。

v0.19 修正：

- 所有承载信息的主面恢复 0 度正交：中心地图板、左侧地区卡、右侧 dossier、底部票据、缩略图框、写字区和票条均按水平 / 垂直网格组织。
- 斜切、夹子、背后文件夹露边、贴纸白边和阴影只保留在 no-text 装饰层，不再压到动态文字区或 hit area。
- 保留 v0.18 的大块低多边形方向与低微细节密度，避免回到 v0.17 的细碎三角网和票据微孔。

当前判断：

- v0.19 是当前可继续拆组件验证的候选；v0.18 不可继续使用，除非只作为“倾斜信息面失败”的反例。
- 仍需注意：右侧快照和左侧缩略图还略偏场景插画 / low-poly render，后续若进入生产资产，需要继续把它们压成更概括的周刊图像，而不是细场景图。
- 下一步不建议继续生成整屏大图。应抽出右侧 dossier、左侧地区卡、底部 ticker 三类组件，分别做 `content_rects / no_text_rects / hit_rects`，再接真实中文验证。

### 7.9 右侧 dossier v0.20 三件套验证

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/26-right-dossier-base-v0-20-orthogonal-no-text.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/27-right-dossier-safe-zones-v0-20.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/28-right-dossier-chinese-fill-v0-20.png`

验证目标：

- 只验证右侧 dossier 单组件，不再依赖整屏风格稿判断。
- 生图只负责无字底图；`safe-zone overlay` 和真实中文填充是验证层，不是美术成品。
- 检查标题、badge、快照、meta、三条 ticket / CTA 是否都有正交、干净、可落动态文字的区域。

通过项：

- 信息承载主面已恢复正交：主纸面、快照框、三条票条、写字区和按钮热区均为 0 度水平 / 垂直。
- 无字底图没有生成可读中英文或假 UI 文案，可作为后续 runtime overlay 的底图候选。
- 票条内部没有明显小孔、条码、刻度和密集微线，整体比 v0.17 更符合“大块色面 + 低微细节”。
- 真实中文字段能放入当前 `content_rects`，没有压到夹子、贴纸、右侧文件夹露边或票条图标区。

待修项：

- 快照仍偏低多边形场景渲染，塔、雷达和天空切面过细；生产版应继续压成更概括的周刊图像。
- 当前中文填充字体只是验证用，观感偏运行时 Label，不能视为最终字体 / 排版风格通过。
- 标题字号偏重，实际 UI 需要在 1920x1080 右栏尺寸里重新定 `font_size / weight / line_height`。
- 右侧 dossier 的正式生产仍需拆出状态 atlas：normal / hover / selected / disabled / warning，而不是从这张整组件图直接切片。

当前判断：

- v0.20 通过“右侧 dossier 无字底图 + 安全区 + 真实中文初填”第一轮验证。
- 下一步应先做 1920x1080 世界地图嵌入验证：把 v0.20 按右栏目标宽度放回 v0.19 世界地图结构，检查中文在真实比例下是否仍可读、右栏是否压中央地图。
- 若嵌入验证通过，再进入左侧地区卡五态 atlas；若嵌入后文字过大或右栏太宽，先回调版式尺寸和字体 token，不继续扩组件。

### 7.10 右侧 dossier v0.21 字体 / 墨色研究

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/29-right-dossier-base-v0-21-integrated-endcaps.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/30-right-dossier-font-study-a-noto-medium.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/31-right-dossier-font-study-b-yahei-soft.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/32-right-dossier-font-study-c-hanyi-strong.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/33-right-dossier-font-study-contact-sheet-v0-21.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/34-right-dossier-real-content-font-recommended-a2-v0-21.png`

修正目标：

- 解决 v0.20 中右侧对勾 / 靶心 / 箭头端区与票条框体嵌合不够的问题。
- 研究中文字体、字重、墨色如何适配低多边形纸件底图。
- 使用真实中文覆盖，不用生图生成中文；字体研究稿是排版验证层，不是最终 runtime UI。

底图修正：

- v0.21 将右侧动作端区改成与票条连续的 end-cap：共享外轮廓、颜色家族、阴影和纸缝，不再像后贴的小方按钮。
- 快照比 v0.20 略少细节，但仍偏 low-poly 场景插画；后续生产版还需继续压成更概括的周刊图像。

字体对比：

- A：`Noto Sans SC Medium / Black`，柔黑墨色。标题够硬、正文不抢、CTA 有重量，是当前推荐方向。
- B：`Microsoft YaHei UI`，偏灰墨色。清晰安全，但更像普通软件 UI，风格弱。
- C：`汉仪中黑 197` 标题，高对比深墨。第一眼更强，但容易压纸面、显土、破坏标杆的克制感。

v0.21 A2 临时建议：

- 标题：`Noto Sans SC Black`，柔黑 `#262823` 左右，避免纯黑。
- 正文 / ticket：`Noto Sans SC Medium`，正文约比标题低 1-2 个重量级，墨色同样用柔黑。
- 辅助状态：偏灰墨 `#545249` 左右，不要用低透明浅灰。
- 文案要短：`消耗 1 天进入` 优于 `进入条件：消耗 1 天`；`任务情报 · 3` 优于 `查看任务情报 · 3`。
- Badge 要短：`高危 / 推荐2` 比 `高风险 / 推荐 2` 更适合当前小区域。

当前判断：

- v0.21 A2 可以作为下一轮 1920x1080 右栏嵌入验证的字体候选。
- 暂不采用 B 作为风格方向，除非后续可读性压倒风格需求。
- 暂不采用 C 作为正文方向；若需要更强标题，可只在极少数封面 / 章节标题中试用，不能进入常规 UI 字体 token。

### 7.11 Steam 字体参照与 v0.22 真实比例嵌入

参照来源：

- `Strange Horticulture` Steam 页面：`https://store.steampowered.com/app/1574580/Strange_Horticulture/`
- `Cultist Simulator` Steam 页面：`https://store.steampowered.com/app/718670/Cultist_Simulator/`
- `The Case of the Golden Idol` Steam 页面：`https://store.steampowered.com/app/1677770/The_Case_of_the_Golden_Idol/`
- `Papers, Please` Steam 页面：`https://store.steampowered.com/app/239030/Papers_Please/`

字体共性判断：

- 这类 Steam 独游通常不让正文承担全部风格。正文更偏清晰、稳定、短句；风格主要由承载物、边框、图标、颜色和版式建立。
- 标题可以更有性格，但不会让所有 UI 字都变成装饰字。
- 按钮 / 行动文案通常短、强、可扫读；长解释文本放到正文区或详情层，不塞进按钮。
- 状态信息优先用短词、颜色、位置和图标共同表达，避免用一整句说明压在小块里。

v0.22 路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/35-world-map-1920-right-dossier-font-v0-22.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/36-world-map-right-dossier-font-v0-22-crop.png`

v0.22 采用：

- 字体：`Noto Sans SC Black` 标题 / CTA，`Noto Sans SC Medium` 正文与状态。
- 墨色：柔黑约 `#262823`，辅助灰墨约 `#545249`，不用纯黑和低透明浅灰。
- 文案：继续使用短句，保留 `消耗 1 天进入`、`任务情报 · 3`、`进入选定地区`。

v0.22 结论：

- 真实右栏比例下，A2 字体方向仍可读，中文没有明显漂浮成普通软件 label。
- 柔黑墨色比纯黑更适合当前暖纸面；标题和 CTA 有重量，但不把纸面压死。
- 端帽嵌合改善有效：对勾 / 靶心 / 箭头和票条共享轮廓与材质后，不再像外挂功能按钮。
- 问题转移到布局尺度：当前右栏略宽、略高，在 1920x1080 嵌入时压到底部 ticker，下一轮应先收右栏目标宽度 / 高度，再继续左侧卡 atlas。

下一步建议：

- 先把右栏目标尺寸定为 500-540px 宽、840-900px 高的范围，做一张不压底部 ticker 的嵌入版。
- 字体方向暂定为 v0.22：`Noto Sans SC` + 柔黑 + 短文案。
- 不继续扩左侧地区卡，直到右栏嵌入尺寸通过。

### 7.12 主题竞品字体气质对比 v0.23

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/37-right-dossier-competitor-font-comparison-v0-23.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/38-right-dossier-font-proposed-serif-title-sans-body-v0-23.png`

参照归类：

- `Strange Horticulture`：纸面 / 手册 / 植物志气质，标题和说明更偏书页印刷感。
- `Cultist Simulator`：神秘卡牌 / 仪式感，标题可更有古典或神秘感，正文仍短。
- `The Case of the Golden Idol`：手绘侦探 / 高识别，字形个性强，但移植到 Angus 容易变粗糙或土。
- `Papers, Please`：官僚档案 / 章印感，强主题但偏硬、旧、压迫，不适合当前现代周刊支线主 UI。

候选结论：

- 0 号“全无衬线黑体”对应 v0.22 当前方向，清楚但仍像软件 Label。
- 1 号“全宋 / 书页感”更有纸面气质，但会把界面推向旧书或植物志。
- 2 号“神秘卡牌”标题有气质，但容易过于仪式化。
- 3 号“手绘强识别”第一眼强，但容易变土、变低龄或廉价手账。
- 4 号“官僚档案”主题强，但会压掉标杆的现代周刊感。
- 5 号“Angus 折中建议”当前最适合继续：标题用 `Noto Serif SC SemiBold`，正文 / ticket 用 `Noto Sans SC Medium`，CTA 用 `Noto Sans SC Black`，墨色偏暖柔黑。

v0.23 临时字体 token：

- `region_title_font`: `Noto Serif SC SemiBold`
- `region_title_color`: 约 `#302B23`
- `ticket_body_font`: `Noto Sans SC Medium`
- `ticket_body_color`: 约 `#302B23`
- `primary_cta_font`: `Noto Sans SC Black`
- `secondary_color`: 约 `#585248`

注意：

- 这是字体气质候选，不是最终 runtime 字体规范。
- 竞品字体未按官方字体文件名判断，而是按 Steam 页面截图可见气质归类；后续若需要商业字体或授权字体，需单独做字体授权筛选。

### 7.13 标题艺术字处理 v0.24

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/39-right-dossier-title-art-treatment-comparison-v0-24.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/40-right-dossier-title-art-proposed-v0-24.png`

问题来源：

- v0.22 / v0.23 主要解决“字体气质”，但标题仍像普通文字，没有形成独立的 title treatment。
- 用户指出需要看“标题艺术字”，而不是只看正文和按钮字体。

对比结论：

- 0 当前粗黑体：清楚，但仍像软件 label。
- 1 书页 serif：纸面感强，但容易把界面推向旧书 / 旧档案。
- 2 档案章：主题强，但偏硬、偏旧。
- 3 剪纸贴标：贴纸感强，但容易低龄或廉价手账化。
- 4 神秘刊头：有神秘感，但容易过度装饰。
- 5 周刊压印：当前推荐。它不是换一款花字体，而是在 serif 标题上加极轻套印影和短下划线，让标题像印在纸面里的现代周刊刊头。

临时规则：

- 标题艺术字只用于地区名 / 页面主标题，不进入正文、按钮、状态、票条说明。
- 标题面仍必须正交，不做斜字、旋转字或透视字。
- 不使用手写体、纯像素字、过重描边、强章印噪声。
- 正文和按钮继续走 `Noto Sans SC` 清晰体系，避免整套 UI 都艺术字化。

下一步：

- 用 v0.24 的标题处理替换 v0.22 的右栏标题，再做一次 1920x1080 嵌入验证。
- 若嵌入后标题太轻，可先加深墨色或略增字重，不直接加粗黑体。

### 7.14 艺术字规格稿 v0.25-v0.26

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/41-art-lettering-spec-v0-25.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/42-art-lettering-spec-v0-26-clean.png`

目标：

- 回应“原标杆风格稿里有很多生图艺术字，效果更好”的反馈。
- 将艺术字从普通字体讨论中拆出来，定义它在 UI 中的使用位置、规格和资产层级。
- 避免两个极端：所有字都像软件 label，或所有字都变成不可维护的艺术字。

当前分层：

| 层级 | 用途 | 是否艺术字 | 备注 |
| --- | --- | --- | --- |
| 品牌 / 刊头 | 主界面标题、章节封面 | 是，固定大资产 | 可更夸张，类似周刊刊头 |
| 页面主标题 | 地区名 / 页面名 | 是，4-6 字优先 | 例：`北美禁区` |
| 贴纸 / 章印短词 | 高危、绝密、红线、锁定 | 是，固定 atlas | 可剪纸、章印、贴纸化 |
| 文件夹标签 | 档案、情报、报道、秘密 | 是，固定分类字 | 更规整，像文件夹印字 |
| 栏目小标题 | 地区情报、进入条件、可见任务 | 轻艺术化 | 可用短下划线、字距、颜色 |
| Runtime 正文字 | 数字、长句、按钮说明 | 否 | 使用清晰 UI 字体 |

落位判断：

- 右侧 dossier 中，`北美禁区` 应使用页面主标题艺术字。
- `高危 / 红线升温` 可使用贴纸 / 小标签艺术字。
- `消耗 1 天进入 / 任务情报 · 3 / 进入选定地区` 保持 UI 字，不做艺术字。
- CTA 可以加字重和墨色，但不使用装饰字形。

硬规则：

- 艺术字只做固定短词 / 主标题 atlas；动态长文本一律清晰 UI 字体。
- 所有信息面保持正交，不能为了艺术字倾斜、旋转或透视。
- 不使用整套手写体、纯像素字、过重描边或强章印噪声。
- 若使用生图艺术字，必须作为固定资产候选复审，不能直接进入 runtime 动态文字。

### 7.15 生图艺术字方向稿 v0.27

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/43-art-lettering-imagegen-style-sheet-v0-27.png`

修正原因：

- v0.25 / v0.26 是程序排版和图形模拟，用于说明层级，但没有回答“艺术字由生图软件生成，再抠出来用”的生产方式。
- 用户明确指出：原标杆风格稿中的生图艺术字效果更好，风格稿也应先用生图软件验证。

v0.27 结论：

- 方向成立。`北美禁区`、`高危 / 红线 / 锁定`、`档案 / 情报 / 报道 / 秘密`、`世界秘闻周刊` 都更接近“字本身就是纸件 / 贴纸 / 周刊刊头资产”的标杆气质。
- 与程序排版稿相比，v0.27 的优势在于笔画不规则、墨色边缘、剪纸白边、低多边形纸面压层和贴纸端角更自然。
- 缺点是它仍是风格稿，不是生产 atlas：后续必须做单词级抠图、透明边缘清理、字形校对和状态 / 缩放验证。

推荐进入抠图候选的资产类型：

- 页面主标题：`北美禁区`，用于右侧 dossier 地区名。
- 状态贴纸：`高危 / 红线 / 锁定`，用于短状态章。
- 文件夹标签：`档案 / 情报 / 报道 / 秘密`，用于固定分类 tab。
- 品牌刊头：`世界秘闻周刊`，用于主界面 / 风格板，不进入普通 UI 动态文字。

生产注意：

- 生图艺术字只适合固定词。若地区名未来可变，需要为每个固定地区名单独生成 / 校对 / 抠图，不能 runtime 拼字。
- 所有抠图资产需要保留正交朝向；不得用倾斜字面承载信息。
- 字形必须逐字校对，任何笔画错误都不能进入生产候选。
- 抠图后要在 1920x1080 右栏真实比例下验证，不能只看放大 atlas。
