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

### 7.16 全字体 / 艺术字生图大标杆 v0.28

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/44-art-lettering-full-typography-imagegen-board-v0-28.png`

生成目标：

- 回应“上一张涵盖太少”的反馈，改为覆盖 Angus 当前高频界面与功能标题，而不是只做右侧 dossier 示例。
- 使用生图软件一次性生成大尺寸字体 / 艺术字风格稿，验证哪些文字适合变成固定艺术字资产，哪些文字应保留运行时清晰印刷字。
- 词表来自当前三界面结构稿与运行时代码，覆盖世界地图、区域任务台、派遣签批台、编辑部 / 发刊、角色 / 骰池、状态章、票据按钮、正文短句和数值徽章。

覆盖层级：

| 层级 | 示例 | 当前判断 |
| --- | --- | --- |
| 品牌主标识 | `世界秘闻周刊` / `WMW` | 固定生图艺术字资产，可做刊头和风格板标识 |
| 页面 / 屏幕标题 | `世界地图`、`区域任务台`、`派遣签批台`、`发刊前报道板`、`发刊回响`、`角色档案` | 适合生图艺术字，但每个固定页面名需单独校对 / 抠图 |
| 地区 / dossier 标题 | `北美禁区`、`北美禁区带` | 适合生图艺术字；若地区名动态扩展，需要按地区名单逐个生成 |
| 模块 / 分区标题 | `地区简介`、`地区预警`、`进入条件`、`任务情报`、`候选队员`、`本周骰池`、`主编复核` | 更适合轻艺术化印刷字，不建议全做贴纸字 |
| 状态贴纸 / 章印短词 | `高危`、`红线`、`锁定`、`绝密`、`可进入`、`已派遣`、`未就绪`、`可签批` | 适合固定 sticker / stamp atlas |
| 文件夹 / 分类标签 | `档案`、`情报`、`报道`、`秘密`、`证据`、`线索` | 适合固定 folder tab atlas，字形应比状态章更规整 |
| 任务标题 | `罗斯威尔档案残页`、`突发雷达异常光点`、`废弃雷达站夜访`、`封存录音的三秒空白` | 中型标题处理即可，不建议每条任务都做重艺术字 |
| CTA / ticket 文案 | `进入选定地区`、`消耗1天进入`、`任务情报3`、`送至签批台`、`签批外勤`、`推进一天` | 保持清晰运行时 UI 字体，底图和端帽承担风格 |
| 正文短句 | `本周取材区已打开`、`进入后再选择具体线报`、`本页不消耗天数` | 必须是运行时正文 / 印刷字，不做艺术字 |
| 数值徽章 | `推荐2`、`余4天`、`有效点13/8`、`覆盖2/2`、`压力+2` | 运行时字体 + 徽章底图；数字不能生图固定死 |

阶段判断：

- v0.28 比 v0.27 更适合指导 UI 替换，因为它按真实功能用字分层，不只是展示几组好看的艺术字。
- 整体风格保留了标杆的深色周刊板、暖纸面、橄榄 / 青蓝 / 暗红、剪纸白边、低微细节和手绘贴纸感。
- 文字承载面基本保持正交，符合“功能页信息面不能斜”的硬规则。
- 票据按钮与状态章的差异比较清楚：按钮文案更像印刷 UI 字，状态章更像生图贴纸。

不能直接生产的原因：

- 生图中文字仍需逐词校对，不能用“看起来差不多”进入 production atlas。
- 这是一张风格总表，不是透明 PNG 字库；下一步要按单词 / 单组件重生、抠图、清边、缩放验证。
- 动态文本、数字、任务列表和正文必须由运行时字体渲染，不能从这张图裁字拼接。
- 若后续要做正式字体规范，需要把 v0.28 拆成两条线：`固定艺术字资产清单` 与 `runtime font token`。

下一步建议：

1. 从 v0.28 中选 6 类固定资产做单词级生图：品牌刊头、页面标题、地区标题、状态章、文件夹标签、少量任务标题。
2. 同步确定 runtime font token：标题下方小字、正文、CTA、数字徽章继续用清晰中文字体，不用艺术字。
3. 先在世界地图右侧 dossier 做真实嵌入：`北美禁区` 艺术字 + `高危 / 红线` 状态章 + 运行时正文 / CTA。
4. 通过 1920x1080 crop 后，再扩展到左侧地区卡和派遣签批台。

### 7.17 竞品字体气质汇总稿 v0.29

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/45-competitor-typography-comparison-imagegen-board-v0-29.png`

参考来源：

- `Strange Horticulture` Steam 页面：`https://store.steampowered.com/app/1574580/Strange_Horticulture/`
- `Cultist Simulator` Steam 页面：`https://store.steampowered.com/app/718670/Cultist_Simulator/`
- `The Case of the Golden Idol` Steam 页面：`https://store.steampowered.com/app/1677770/The_Case_of_the_Golden_Idol/`
- `Papers, Please` Steam 页面：`https://store.steampowered.com/app/239030/Papers_Please/`
- `Return of the Obra Dinn` Steam 页面：`https://store.steampowered.com/app/653530/Return_of_the_Obra_Dinn/`
- `Orwell: Keeping an Eye On You` Steam 页面：`https://store.steampowered.com/app/491950/Orwell_Keeping_an_Eye_On_You/`

生成目标：

- 回应 v0.28 “字体太死板”的反馈，不继续在单一 Angus 字形里硬调，而是先把相邻游戏的字体气质转成中文对照稿。
- 同一套测试文案重复展示：`北美禁区`、`派遣签批台`、`高危`、`进入选定地区`、`本周取材区已打开`、`余4天`，便于比较标题、按钮、正文、数字的适配性。
- 仅参考竞品字体气质，不复刻商标 logo 或官方字形。

竞品气质判断：

| 行 | 气质 | 可学 | Angus 风险 |
| --- | --- | --- | --- |
| 01 植物志衬线 | 类 Strange Horticulture 的书册 / 植物志衬线 | 标题有纸面高级感 | 容易变旧书、旧手册、安静 |
| 02 仪式卡牌 | 类 Cultist Simulator 的神秘 serif | 短标题和章印有仪式感 | 过度使用会变宗教 / 神秘学卡牌，不像现代周刊 |
| 03 侦探手写 | 类 Golden Idol 的侦探手写 / 粗糙标题 | 有生命力，不死板 | 容易低龄、漫画化、廉价手账 |
| 04 官僚块字 | 类 Papers, Please 的权威块字 | 状态章、封条、阻断标签有力 | 主标题太硬，压迫感强，像审查窗口 |
| 05 保险刻印 | 类 Obra Dinn 的历史刻印感 | 可用于特殊旧档案或历史副本 | 历史感过强，违背“不是旧档案” |
| 06 监控无衬线 | 类 Orwell 的冷静系统字 | 正文和数字可读性强 | 太冷、太软件、缺少周刊纸面味 |
| 07 Angus 混合推荐 | 现代周刊 + 轻微手工切字 + 清晰印刷字 | 当前最接近可继续方向 | 仍略硬，需要再吸收 03 的松动笔势 |

阶段判断：

- v0.29 说明 v0.28 的问题不是“字不够花”，而是主标题缺少人手切纸 / 印刷不规则带来的活性。
- 不建议采用 01 / 02 / 05 作为主 UI 字体方向，它们会把当前支线拖回旧书、神秘仪式或历史档案。
- 不建议采用 04 作为主标题方向，它适合 `封锁 / 禁止 / 已驳回 / 未就绪` 这类压迫状态，不适合 `北美禁区` 常态标题。
- 06 可作为 runtime 字体的可读性下限参考，但不能承担主视觉。
- 07 可继续作为 Angus 主方向，但需要下一轮明确加入：轻微不规则笔画、手工剪纸边、压印墨色变化、标题和正文分工。

下一步建议：

1. 做一张 `v0.30 Angus 专用字体提案`，不再放竞品全排，而是只合成 3 个可用候选：`07 稳定版`、`07+03 松动版`、`07+06 可读版`。
2. 每个候选只验证三层：页面标题 `北美禁区`，模块标题 `派遣签批台`，正文 / CTA `进入选定地区 / 本周取材区已打开`。
3. 若用户倾向更有生命力，优先选 `07+03 松动版`，但正文仍必须使用清晰 runtime 字体。

### 7.18 完整世界地图真实内容字体 A/B：07 vs 04

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/48-world-map-real-fill-font07-angus-hybrid-v0-32.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/49-world-map-real-fill-font04-bureaucratic-block-v0-33.png`

修正原因：

- 用户指出验证对象应是完整世界地图界面，而不是右侧 dossier 单组件。
- 本轮改用图库里的同源完整界面 `25-world-map-local-validation-v0-19-orthogonal-info-surfaces.png` 作为结构参考：左侧地区卡、中央世界地图、右侧 dossier、底部回执和右下贴纸全保留。
- 两版只比较字体气质与少量字面包装，不重排界面结构。

真实内容填充范围：

- 左侧地区卡：`北美禁区带`、`东亚神秘地带`、`太平洋失航带`、`黑色方尖碑回声`。
- 右侧 dossier：`北美禁区带`、`高危`、`推荐2`、`红线升温`、`消耗1天进入`、`任务情报·3`、`进入选定地区`。
- 底部回执：`地区异动 / 红线1 青线1`、`地区预警 / 进入后再选择线报`、`最近变化 / 锁定档案保留`。
- 地图状态：`已选`、`锁定`、`红线`。

v0.32 / 07 Angus 混合推荐判断：

- 优点：整体仍保留现代周刊感，标题、卡片和右侧 dossier 不会过度官僚化；与低多边形纸件、贴纸、色块标杆更融洽。
- 优点：适合常态页面标题、地区名、CTA、运行时 UI 文本的主方向。
- 问题：生图小字仍有误写，例如锁定条件存在变形；不能直接裁字生产。
- 问题：标题仍略偏规整，若用户觉得死板，下一轮应在 07 基础上加入 03 的轻微手工剪纸笔势，而不是转向 04 全局使用。

v0.33 / 04 官僚块字判断：

- 优点：`锁定`、`红线`、`进入选定地区`、`高危` 的权威感更强，危险 / 审批 / 封锁语义清楚。
- 优点：适合局部状态章、不可逆动作、签批回执、封条和锁定卡。
- 问题：全屏使用时会把世界地图读成通行证 / 审查窗口 / 管理系统，削弱标杆里的现代周刊和神秘编辑感。
- 问题：标题和正文都变硬后，信息密度看似清楚，但舒适度下降，玩家会更容易觉得界面“重”和“压”。

阶段结论：

- 主 UI 不建议全局采用 04。04 应降级为状态 / 审批 / 锁定专用字体气质。
- 常态页面与地区标题仍建议以 07 为底，但需要做 `07+03 松动版`：保持 07 的现代周刊结构和可读性，加入更明显的手工剪纸 / 印刷边缘不规则。
- 正文、数字和长按钮文案仍应由 runtime 字体渲染；生图只用于固定短词和标题资产候选。

下一步建议：

1. 做完整世界地图 v0.34：`07+03 松动版`，只强化标题和地区卡名称，正文 / CTA 保持 07 的清晰印刷字。
2. 同屏保留少量 04：只用于 `锁定`、`红线`、`高危` 和 `签批` 一类短状态章。
3. 通过后再转为生产测试：固定艺术字资产清单 + runtime font token，而不是继续让生图整屏写所有动态字。

### 7.19 完整世界地图字体层级修正版 v0.34

路径：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/50-world-map-real-fill-font-hierarchy-07-03-v0-34.png`

修正目标：

- 回应“字体大小、粗细没有区分，小组件字太粗”的反馈。
- 按 UX 诊断建立层级：主标题 > 模块标题 > 状态章 > CTA > 正文 / 辅助说明 > 数字徽章。
- 主 UI 采用 07 Angus 混合推荐为底，主标题和地区名加入少量 03 的手工剪纸松动感；04 只保留在 `锁定 / 红线 / 高危 / 已选` 等短状态章和 CTA 强调上。

v0.34 观察：

- 改善：相较 v0.32 / v0.33，状态章不再和 CTA 同等大，小组件正文整体降重，底部三张回执不再全部像一级标题。
- 改善：右侧 dossier 的 `北美禁区带`、三条票据和底部回执之间有了更明确的字重梯度。
- 保留问题：生图仍会误写小字，例如锁定条件中的 `罗斯威尔残页` 字形不稳定；这类文字不能直接作为生产字图。
- 保留问题：底部卡标题仍略重，下一轮若继续，应再把底部标题降半级，并把正文降到更接近 400 / 500 的印刷字。

阶段结论：

- v0.34 可以作为“字体层级方向通过”的风格稿，而不是生产 atlas。
- 正式落地应拆为两套：固定短词艺术字 / 章印资产，以及运行时字体 token。动态内容、长条件、数字和正文必须由 runtime 字体渲染。
- 目前更稳的方案是：`07+03` 负责标题和地区名，`04` 负责短状态章和主 CTA 强化，小组件正文走轻字重印刷体。

下一步建议：

1. 若继续生图：出 v0.35，只微调底部三卡和左侧卡的次级说明，不再改整体结构。
2. 若进入生产验证：先做一张真实 runtime overlay mock，把动态文字用可控字体压回 `content_rects`，生图只保留无字底图与固定状态贴纸。

### 7.20 v0.34 字体问题三方诊断

触发反馈：

- 用户指出：很多文字比较怪，有些像被压瘦成长条，字体效果组合不好，不像正式上线游戏的字体文字和界面配合度。

三方结论：

- `ux_laoge`：存在 P0 风险。右侧绿色 `消耗1天进入`、蓝色 `任务情报·3`、红色 `进入选定地区` 同屏争夺主动作，红色条视觉最强，可能劫持 CTA。中文横向压缩和全屏粗字也造成 P1 层级坍塌。
- `ui_designer`：正式字体系统不应走“生图艺术字 + 后贴 Label”混合路线。动态中文必须 runtime overlay；底图只负责纸件、章底、按钮底、照片、图标和纹理。禁止横向压缩、伪粗体、描边堆叠。
- `angus_art_director`：v0.34 不能作为正式上线视觉标杆。底图接近 Angus，但字体像后贴 UI label，并有 AI 烘焙文字感。下一版必须让底图只提供空白文字槽和灰条占位，真实中文由稳定字体渲染。

共识修正方向：

1. 不再让生图负责所有真实中文；地区名、任务名、计数、耗时、CTA、底部说明全部转为 runtime 字体。
2. 生图 / PNG 只保留无字底图、章底毛边、低多边形照片、地图陆块、图标外形、胶带、夹子、阴影、套印偏移和按钮底板。
3. 建立固定字体 token，中文 `scale_x = 1.0`，不允许压瘦；放不下时改安全区、缩短文案或换行。
4. 主 CTA 单一化：将 `进入` 与 `消耗 1 天` 合并到一个主动作，避免绿色进入条和红色进入条互相竞争。
5. 状态章只放 2-3 字短词：`锁定 / 红线 / 高危 / 已选 / 隐藏`；不承载长说明。

建议字体栈：

| Token | 用途 | 字体 |
| --- | --- | --- |
| `font.display` | 右侧地区名、重要标题 | `Noto Serif SC` / 思源宋体 Heavy 或 Black |
| `font.ui` | CTA、状态章、地区卡标题、正文 | `Noto Sans SC` / 思源黑体 |
| `font.number` | 数字徽章、计数、天数 | 稳定无衬线数字；中文回退 `font.ui` |

建议字号层级：

| Token | 用途 | 1920x1080 基准 |
| --- | --- | --- |
| `type.map.title` | 右侧地区名 | 48px / 800-900 |
| `type.card.title` | 左侧地区卡标题 | 32px / 700-800 |
| `type.cta.primary` | 主 CTA | 30px / 800 |
| `type.cta.secondary` | 次级按钮 | 26px / 700 |
| `type.badge.status` | 状态章 | 24px / 800 |
| `type.body.main` | 正文 / 回执正文 | 22px / 500-600 |
| `type.body.assist` | 辅助说明 | 18px / 400-500 |
| `type.number.badge` | 数字徽章 | 28px / 700 |

下一步执行建议：

- 不继续用生图整屏写真实中文。
- 先使用 `25-world-map-local-validation-v0-19-orthogonal-info-surfaces.png` 或后续无字底图作为 bitmap 底，做一张可控字体 overlay mock。
- 产出必须包含整屏图和 100% 裁切：左侧地区卡、右侧纸夹、CTA、底部回执、地图章字。

### 7.21 Runtime overlay 字体验证稿 v0.35 / v0.36

产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/51-world-map-runtime-overlay-font-system-v0-35.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/52-world-map-runtime-overlay-font-system-v0-35-crops.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/53-world-map-runtime-overlay-font-system-v0-36.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/54-world-map-runtime-overlay-font-system-v0-36-crops.png`

实现方式：

- 以 `25-world-map-local-validation-v0-19-orthogonal-info-surfaces.png` 作为无字 / 少字风格底图。
- 使用本机 `NotoSansSC-VF.ttf`、`NotoSerifSC-VF.ttf` 做真实中文 overlay。
- 不对中文做水平缩放；放不下时只能降字号、缩短文案或换文字安全区。

v0.35 观察：

- 解决了上一轮生图文字被压瘦、变成长条的问题。
- 主 CTA 合并为 `进入北美禁区 1天`，红色条降为 `红线截止 4天` 状态，减少动作冲突。
- 问题：整体字重仍偏硬，左侧卡和底部回执像“白纸标签贴上去”；按钮右侧小角标文字继续增加噪声。

v0.36 修正：

- 全局降低 `Noto Sans SC` 字重：标题从强 Bold 降到 Medium / 轻 Bold，正文降到 Regular。
- 右侧地区名保留 `Noto Serif SC`，但从 Black 降到 Bold，避免标题过于沉重。
- 移除按钮图标里的 `确认 / 线报` 小字，只保留图标语义。
- 底部回执标题从大粗字降级，小正文使用 Regular，避免小组件像一级标题。

阶段结论：

- v0.36 更适合作为“字体 runtime overlay 方向验证稿”：它证明真实字体可以避免 AI 生图中文压缩问题。
- 但它还不是最终上线 UI：纸槽与文字的融合仍需进一步做图层级别处理，尤其是左侧地区卡和底部回执的文字底槽，后续应在美术底图里预留更自然的印刷安全区，而不是用半透明矩形覆盖。
- 当前仍按支线风格推进，不写入正式 `design/art-direction/angus-visual-style-guide.md`；等完整世界地图、地区界面、任务派遣三类界面铺量通过后，再决定是否升级为正式风格规则。

### 7.22 v0.36 三方复审

复审结论：

- `ux_laoge`：P0=0，可以继续作为支线验证，但只能验证 runtime overlay 字体方向，不能升为正式 UI 候选。
- `ui_designer`：字体压缩问题已明显缓解，但半透明灰条像开发态 Label，需要改成印刷标题底托、短色签或真实纸槽。
- `angus_art_director`：有条件通过。低多边形照片、纸件层、手绘概括图标和深蓝地图主场保住了；下一步要把“文字贴上去”推进成“文字有自己的印刷物件位置”。

必须修的 P1：

1. 红色 `红线截止 4 天` 仍带箭头和强红底，容易像第二 CTA。下一版应去箭头或改成不可点击倒计时章。
2. 底部回执标题后的灰条像调试占位 / 输入框。下一版改为短标签、刷痕、印刷标题底托，或取消整条底色。
3. 中央地图浮字压在光圈、路线和大陆纹理上。下一版应使用 pin callout / 小纸签，并避开光圈 16-24px。
4. 左侧地区卡副信息太淡，远看像脏纹理。下一版要么提高对比，要么减少副文，把副信息收回右侧详情。

下一版底图预留要求：

- 左侧地区卡：标题纸签更宽；右侧小状态单独给短槽，远离勾章 / 靶心 / 锁图标。
- 中央地图：选中地区名不裸压地图，改为小纸签或 pin callout。
- 右侧档案纸：顶部标题、风险章、推荐值、照片标签、三条 CTA 都建立稳定 `content_rects`。
- CTA：文字槽和右侧图标槽分开，动态文字不跨到勾、靶心、箭头区域。
- 底部票据：拆成 `大标题槽 / 小说明槽 / 色块条槽`，标题与正文至少 8px 行距。

### 7.23 v0.37 内容贴合修复诊断

触发反馈：

- 用户指出：目前仍有内容不贴合的情况；希望一边修复，一边用生图方式生成一张“界面效果 + 真实文字”的风格稿，要求文字和界面贴合很好，达到上线游戏标准。

三方补充诊断：

- `ux_laoge`：v0.36 新增 P0。当前选中对象是北美，但中央地图最强青色虚线指向澳洲，和右侧 `进入北美禁区` 主 CTA 冲突。玩家会怀疑按钮到底进入北美、追踪澳洲，还是从北美派线到澳洲。
- `ui_designer`：同屏不应再出现“半透明灰矩形 + 文字”的通用底条。凡是文字需要底，必须是纸签、印章、票根、caption 或地图铭牌。
- `angus_art_director`：生图 prompt 目标应从“低多边形世界地图 UI”改成“World Mystery Weekly 的一张已排版、已印刷、可点击的编辑部世界选题墙”。核心不是加纸纹，而是让文字、按钮、图标、纸件、地图都像同一套印刷物件系统。

v0.37 runtime 修复目标：

1. 北美必须是唯一选中 / 高亮地区；跨到澳洲的强路线必须移除或降到不可读装饰。
2. 底部票据降为全局周状态，不再重复右侧操作事实。
3. 灰色文字底条改为纸签 / 短槽 / callout。
4. 红色 `红线截止 4 天` 继续降为状态票根，不作为第二 CTA。

v0.37 产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/55-world-map-runtime-overlay-font-system-v0-37.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/56-world-map-runtime-overlay-font-system-v0-37-crops.png`

v0.37 结论：

- 作为工程 overlay 验证稿成立：证明可控字体、纸签槽位、CTA 层级可以继续拆到 runtime。
- 但不适合作为上线风格稿：原始底图里的跨洲路线只能通过局部 inpaint / 覆盖压弱，仍会留下雾化痕迹；底图没有真正为文字预留纸件结构时，runtime overlay 很难完全消除“贴上去”的感觉。

### 7.24 生图整屏文字嵌合稿 v0.38

产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/57-world-map-imagegen-text-integrated-v0-38.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/58-world-map-imagegen-text-integrated-v0-38-crops.png`

生图硬约束：

- 16:9 desktop game UI screenshot mockup。
- 左侧地区索引卡 / 中央世界取材地图 / 右侧北美禁区带 dossier / 底部低权重周状态票据。
- 北美是唯一选中 / 高亮地区；禁止亮线连到澳洲或任何非选中地区。
- 真实中文只能出现在纸签、标题栏、章印、按钮板、票据和 caption 内；禁止浮在地图、照片、夹子、折角、边框或半调纹理上。
- 主 CTA 只有一个绿色签批条；蓝色情报为次级；红色红线为状态票据，不带箭头、不做按钮语法。

指定真实文字：

- `世界取材地图`
- `探索周 03 / 余 6 天`
- `北美禁区带`
- `红线升温`
- `高危`
- `推荐 2`
- `进入北美禁区 · 消耗 1天`
- `查看任务情报 · 线报 3`
- `红线截止 · 4天`
- `本周行动 · 余 6 天`
- `情报余量 · 线报 3`
- `红线台账 · 4 天后升温`

v0.38 观察：

- 明显优于 v0.37 的地方：文字和纸件 / 按钮板 / 票据的嵌合更自然，不再像开发态 overlay；北美是唯一高亮，地图没有跨洲强路线，核心空间主语清楚。
- 仍需注意：生图中文虽整体可读，但生产落地仍不能直接烘焙所有动态字；后续应以 v0.38 作为“美术底图 + 文字槽位”参考，再拆成可替换 runtime 文本层。
- 当前定位：v0.38 是本支线目前的前排视觉参考，不是正式项目真源。必须等世界地图、地区界面、任务派遣三类界面都能按同一规则铺量后，再考虑升级到正式风格规范。

### 7.25 正交硬规则修复稿 v0.39

触发反馈：

- 用户指出 v0.38 右侧 dossier 又出现信息界面倾斜问题；该问题此前已作为硬规则，后续必须避免。

规则复核：

- 全局规则已存在于 `docs/onboarding/ui-interaction-guidelines.md` 与 `docs/onboarding/assetized-ui-production-chain.md`：凡承载动态文字、数字、头像状态、按钮文案、可点击热区或状态矩阵的正面区域，必须 square-on、axis-aligned、可测量。
- 本轮不新增全球规则，而是将 v0.38 标记为“文字嵌合通过但正交硬规则失败”的偏差样本。

v0.39 产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/59-world-map-imagegen-orthogonal-text-v0-39.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/60-world-map-imagegen-orthogonal-text-v0-39-crops.png`

v0.39 prompt 一票否决句：

```text
Every information-bearing front face must be perfectly square-on, axis-aligned, horizontal and vertical, 0 degree rotation. The right dossier paper front, left region cards, center map board, bottom receipts, CTA strips, title fields, photo frame, text fields and clickable button plates must all be orthographic rectangles parallel to the image edges. No tilted, rotated, skewed, trapezoid, perspective, photographed, angled, leaning, or diagonal writable UI faces. Decorative back sheets, clips, tabs, shadows, bevel cuts and paper edges may create depth, but only behind or outside no-text zones. If a surface carries text or a button label, it must be straight and measurable.
```

v0.39 观察：

- 通过：右侧主 dossier 正面、三条 CTA / 状态票据、左侧地区卡、底部票据均恢复 0 度正交。
- 通过：斜感只保留在夹子、背后叠页、露边、阴影和装饰纸层，不再进入动态文字区或按钮热区。
- 通过：北美仍是唯一高亮区域，地图没有重新出现跨洲强路线。
- 仍需注意：作为生图稿，少数字符和小图标仍只能作为风格参考；生产落地仍应拆为正交无字底图 + runtime 文本层。

阶段结论：

- v0.39 取代 v0.38，成为当前支线“世界地图整屏文字嵌合 + 正交硬规则”的前排参考。
- v0.38 仅保留为“文字嵌合较好但右侧信息面倾斜失败”的偏差样本。

### 7.26 v0.39 颜色 / 质感回归对照

对照产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/61-world-map-color-texture-compare-v039-v038-v036.png`

对照对象：

- `v0.39 orthogonal`：正交硬规则修复稿。
- `v0.38 imagegen`：文字嵌合较好但右侧信息面倾斜失败。
- `v0.36 runtime`：可控字体 overlay 验证稿。

观察：

- 整体色盘没有大幅跑偏：深海军蓝地图、橄榄绿、青蓝、红橙、米白纸仍在同一方向。
- v0.39 相比 v0.38 的变化主要来自“正交修复”：面板边缘更硬、更规整，纸件更像干净 UI 物件，手工剪贴松动感略下降。
- v0.39 的北美高亮更偏黄绿、更亮；相比 v0.38 的橄榄灰绿，略有“地图选择高亮 / 策略游戏占区”的倾向。
- v0.39 的地图陆块三角纹更明显，局部更像低多边形网格；后续应压低内部三角线 / 纹理密度，回到标杆“大块概括”的原则。
- v0.39 的右侧纸面与底部票据更干净、更正交，解决可用性问题；但纸纹和纸边的随机手工感弱于 v0.38。
- v0.39 的 CTA stack 比 v0.36 好：文字更嵌入按钮板，不再像 runtime label；但比 v0.38 略更规整，需保留外轮廓手绘 / 贴纸感，不能让可写区倾斜。

下一轮约束：

1. 保留 v0.39 的正交信息面，不回退到 v0.38 的倾斜纸面。
2. 把北美高亮从偏亮黄绿压回更灰、更橄榄的标杆色。
3. 降低地图陆块内部三角网和线痕密度，保留大块低多边形。
4. 恢复 v0.38 的纸边 / 贴纸外轮廓手工感，但只作用于 `no_text_rects`，不进入文字槽和按钮热区。

### 7.27 v0.40 正交 + 灰橄榄 + 手工纸边回调

三方输入：

- `ui_designer`：保留 v0.39 的正交信息面与信息层级；北美高亮从偏黄绿修回“脏橄榄金 / 旧荧光标记笔”，不要青柠 / 嫩黄绿；纸件恢复轻微裁切差、压层厚度和手工边，但文字区必须方正干净。
- `ux_laoge`：v0.40 应以 v0.39 为 UX 骨架，只回调 v0.38 / 少量 v0.36 的颜色、纸张和边框质感；不能牺牲主 CTA、正交承载面、地图主读区和底部资源语义。
- `angus_art_director`：v0.40 应是“v0.39 的正交可落地信息面 + v0.38 的手工纸边 / 贴纸外轮廓 + 标杆的干净低多边形质感”。

产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/62-world-map-imagegen-muted-olive-texture-v0-40.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/63-world-map-imagegen-muted-olive-texture-v0-40-crops.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/64-world-map-color-texture-compare-v040-v039-v038.png`

v0.40 prompt 关键约束：

- 使用 v0.39 的正交布局和文字安全区作为硬源。
- 使用 v0.38 / 标杆的纸边、贴纸外轮廓、手工裁切、低多边形大块面作为材质参考。
- 北美高亮从亮黄绿压回 muted grey olive / dusty olive green。
- 陆块内部三角纹降 40-60%，地图读作现代低多边形印刷地图，而不是 GIS 三角网。
- 所有承载文字、数字、状态和按钮文案的面保持 0 度正交。

观察：

- 通过：北美高亮明显从 v0.39 的亮黄绿压回灰橄榄，选中仍清楚但不再刺眼。
- 失败：右侧 dossier / CTA stack 在用户复核截图中仍可见整体倾斜，不能判定为正交通过。此前“仍保持正交”的判断是父级 Codex 的验收错误。
- 通过：纸边、票据、贴纸外轮廓比 v0.39 更有手工裁切和物件层次。
- 改善：地图没有跨洲强路线，空间主语仍是北美。
- 保留问题：地图大陆内部三角块仍略明显，下一轮若继续，应继续降低三角线 / 内部纹理密度。
- 保留问题：v0.40 的纸件和 CTA 整体略变亮，后续需防止滑向“干净亮纸 / 扁平 UI 纸片”。

颜色统计摘要：

- 北美高亮亮度：v0.39 `86.8` -> v0.40 `78.9`，已压低并更接近灰橄榄。
- 右侧纸面亮度：v0.39 `111.1` -> v0.40 `111.4`，基本持平。
- 底部纸面亮度：v0.39 `140.3` -> v0.40 `141.8`，略升。
- 红色状态亮度：v0.39 `117.4` -> v0.40 `125.9`，红色区域更亮，下一轮需确认是否过抢。

阶段结论：

- v0.40 不取代 v0.39，降级为“颜色 / 纸边回调有效，但正交硬规则失败”的偏差样本。
- 但仍不是生产真源：生产拆层还需要无字底图、content/no-text rect manifest、runtime 字体 token 和颜色采样闸门。

### 7.28 v0.40 正交验收失败与 v0.41 修复闸门

触发反馈：

- 用户指出 v0.40 仍然是斜的，并追问是否经过视觉校验。

复盘结论：

- v0.40 没有经过合格视觉校验。父级 Codex 只做了整图肉眼检查和局部裁切观察，未对信息承载面做几何测量。
- 生图 prompt 写入“0 度正交”不等于结果自动满足；凡是模型生成的拟物纸面，都必须在交付前通过截图 / 裁切 / 几何测量三步验收。
- 这次错误暴露的是执行闸门缺失，而不是规则缺失。全局规则已写明“功能承载页必须方正”，但本轮没有按规则阻断失败图。

新增产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/65-world-map-v040-user-tilt-feedback-crop.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/66-world-map-v040-orthogonal-failure-qa.png`

v0.40 QA 结果：

- 右侧信息纸面检测为 `ORTHOGONAL QA: FAIL`。
- 左边缘相对垂直约 `+0.90 deg`，顶部相对水平约 `+0.90 deg`；底部受遮挡影响更大，但也不是稳定水平。
- 对 Angus 功能界面而言，承载标题、状态、照片框、CTA 文案和按钮热区的正面只要可见倾斜，即降级为灵感图 / 偏差样本。

v0.41 交付闸门：

1. 先生成图，再裁切右侧 dossier、CTA stack、左侧地区卡、底部票据和中心地图板。
2. 对每个信息承载面的上 / 下 / 左 / 右边做像素级边缘检测；任一核心边角偏差超过 `0.5 deg`，不得交付为通过稿。
3. 允许纸边、夹子、背页、阴影、标签和装饰贴纸倾斜；不允许标题纸面、照片框、CTA 文本槽、状态票据、按钮热区倾斜。
4. 最终回复必须同时附“风格稿原图 + 正交 QA 图”，不再只附整图或凭肉眼判断。

v0.41 修复候选：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/67-world-map-imagegen-geometric-orthogonal-v0-41.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/72-world-map-v041-orthogonal-qa-edge-first.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/73-world-map-v041-orthogonal-qa-edge-first-crop.png`

v0.41 临时 QA 结果：

- 通过：三条 CTA 的文字槽均在 `0.5 deg` 阈值内；底部三张票据的顶部 / 底部承载线均在阈值内。
- 通过：右侧照片框顶部 / 底部与右边界在阈值内。
- 未完全自动通过：照片框左边界检测会被图像内塔架竖线干扰，临时脚本报出假失败；后续需要把检测脚本升级为“先指定 content edge，再测边线”，或保留人工复核项。
- 结论：v0.41 只作为“正交修复候选”，不升级为生产真源；v0.40 仍是明确失败样本。

### 7.29 v0.41 配色 / 质感漂移复盘

触发反馈：

- 用户要求检查 v0.41 的配色和质感是否与标杆一致，并反思为什么每次微调都会改动这些。

采样产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/74-world-map-v041-vs-benchmark-color-texture-sampling.png`

临时 RGB / 亮度采样结论：

- `paper_light`：标杆约 `#AEA495 / #B5A792`，v0.41 为 `#BCAA95`，亮度比标杆均值高约 `+5.8`，面积从标杆约 `9.6-12.8%` 增至 `19.0%`。问题不是单个纸色，而是纸面占比和明度一起上升。
- `red_orange`：标杆红橙面积约 `0.2-0.3%`，v0.41 增至 `2.8%`，且更偏高饱和砖红。红色从“少量危险信号”变成了“票据系统主色之一”。
- `olive_green`：标杆橄榄约 `#696D3F / #626843`，v0.41 平均为 `#555639`，更暗、更灰，且北美选中区域局部仍有高亮策略地图感。
- `neutral_gray_map`：v0.41 地图灰平均亮度比标杆低约 `-17.4`，大陆更沉、更数字地图化；与标杆大块手绘低多边形的轻重关系不一致。
- texture 临时指标：v0.41 的边缘高频 `p90` 低于标杆，说明它更干净、更规整；但局部票据孔、条码、规则框仍带来“UI 票据细节”，不是标杆的概括性低多边形 / 手绘贴纸细节。

美术判断：

- v0.41 不满足“配色和质感与标杆一致”。它是正交修复候选，但不是标杆风格通过稿。
- 它更像“干净、规整、可读的 dossier UI”，而标杆更像“深暗现代周刊风格板 + 大块低多边形图像 + 手绘概括图形 + 克制纸张物件”。

为什么每次微调都会漂：

1. 每轮 prompt 都重新描述整张图，模型会全局重绘，而不是只改一个变量。
2. 为了修正交和文字可读性，prompt 强调 `clean orthographic / readable / paper labels`，模型自然会增大米白纸面、提亮纸面、规整边框，并降低手工块面。
3. 没有在生成前冻结 `Color Contract v1` 和 `Texture Contract`；“muted / dusty / benchmark style”这类形容词无法阻止模型重染。
4. 文本嵌入会迫使模型提高文字底板明度和对比度，导致纸面更亮、更大、更像后台表单。
5. 负面约束里反复写 `no grunge / no old archive / no tilted`，模型会过度补偿成干净亮纸和硬边 UI。

后续避免方式：

- 每次生图前先冻结本轮 `Style Lock Contract`：唯一标杆图、固定 ROI、色号 token、纸面占比、暗部占比、红色面积、纹理高频范围、低多边形块面粒度。
- 每轮只允许移动一个变量。几何修复 prompt 必须写 `preserve sampled palette and texture; change geometry only`，不得重新描述颜色、纸感和材质。
- 生图后先复采样；若纸面亮度 / 面积、红色面积、暗部占比或纹理指标超阈值，即使正交修好了也降级为偏差样本。
- 将“整屏文字嵌合生图稿”和“生产可拆分底图”分开：文字稿用于看版式感，不能同时承担色彩 / 材质真源。

### 7.30 v0.42-v0.45 配色 / 质感修正

触发反馈：

- 用户要求“改一下”，即按 §7.29 的结论修正 v0.41 与标杆之间的配色、纸面占比、红色占比和质感偏差。

产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/75-world-map-imagegen-style-locked-v0-42.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/76-world-map-v042-vs-benchmark-color-texture-sampling.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/77-world-map-imagegen-style-locked-v0-43.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/78-world-map-v043-vs-benchmark-color-texture-sampling.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/79-world-map-imagegen-style-locked-v0-44.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/80-world-map-v044-vs-benchmark-color-texture-sampling.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/81-world-map-imagegen-style-locked-v0-45.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/82-world-map-v045-vs-benchmark-color-texture-sampling.png`

迭代观察：

- v0.42：深蓝和红色面积比 v0.41 明显回调，但错误带回了北美到澳洲的跨洲虚线，语义失败。
- v0.43：去掉跨洲线，保持暗底和正交，但仍保留大面积底部纸票据，纸面占比约 `18.1%`，无法真正回到标杆。
- v0.44：有效改法出现。将底部大白票据改为“彩色文件夹 / 票夹 + 小纸签”，纸面占比从 v0.41 的 `19.0%` 降到 `9.3%`，进入标杆范围。但整体被压得过暗，纸签偏脏灰，红褐文件夹被算法算作红色面积偏高。
- v0.45：保留 v0.44 的材质比例，适度提亮纸签并收敛红褐色。纸面占比约 `13.5%`，接近标杆上沿；深蓝占比 / 暗部占比更接近标杆 2；无跨洲路线。

当前判断：

- v0.45 是本轮相对最好的修正版，可作为“配色 / 质感修正候选”给用户看。
- v0.45 仍不是生产真源：整体亮度偏暗，地图灰与橄榄仍比标杆沉，红褐文件夹在临时采样中仍造成 `red_orange` 面积偏高。
- 真正可迁移的结论不是“调暗纸面”，而是“降低纸面承载面积，把大票据改为彩色文件夹 / 票夹主体 + 小纸签写字”。这是后续铺量时应保留的组件语法。

### 7.31 v0.46-v0.53 第一版色彩重新矫正

触发反馈：

- 用户指出当前图相比第一版“严重变暗，颜色也不对”，要求重新矫正。
- 本轮将用户提供的第一版世界地图图作为色彩 / 明度锚点，只参考其色彩与材质关系；不继承第一版的跨地图路线、空白占位字段或早期未填充内容结构。

归档产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/83-world-map-first-ref-vs-v045-color-target.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/84-world-map-imagegen-color-recorrected-v0-46.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/85-world-map-v046-vs-first-ref-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/86-world-map-imagegen-color-recorrected-v0-47.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/87-world-map-v047-vs-first-ref-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/88-world-map-imagegen-color-recorrected-v0-48.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/89-world-map-v048-vs-first-ref-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/90-world-map-imagegen-color-recorrected-v0-49.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/91-world-map-v049-vs-first-ref-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/92-world-map-first-version-color-reference.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/93-world-map-imagegen-color-recorrected-v0-50.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/94-world-map-v050-vs-first-ref-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/95-world-map-imagegen-color-recorrected-v0-51.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/96-world-map-v051-vs-first-ref-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/97-world-map-imagegen-color-recorrected-v0-52.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/98-world-map-v052-vs-first-ref-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/99-world-map-imagegen-color-recorrected-v0-53.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/100-world-map-v053-vs-first-ref-color-check.png`

第一版色彩锚点采样：

- `global L` 约 `69.6`，`median L` 约 `48.4`。
- `dark %` 约 `52.3%`，说明标杆不是亮图，而是深底 + 可读中间调，不应把整体压成黑泥。
- `paper %` 约 `18.1%`，但这是第一版含大量空白占位条的结构结果；真实内容版不应为了追纸面占比而把字段清空。
- 参考色相：深海军蓝 `#061520 / #0C1924`，纸面 `#B3A593`，橄榄 `#585B3B`，青蓝 `#344454`，地图灰 `#535454`。

版本判断：

- v0.46：首次把 v0.45 的暗沉问题明显拉回，`global L` 约 `64.1`，纸面和地图灰更接近第一版；但红褐面积与纹理压力偏高。
- v0.47：尝试压红色后整体又变暗，`global L` 约 `63.0`，纹理压力更高；淘汰。
- v0.48：红色压力下降，但右侧纸张和局部几何出现漂移，且 `global L` 仍约 `62.9`；淘汰。
- v0.49：局部纸张更暖，但全局压到 `59.6`，属于“视觉局部变好、整体又暗掉”的失败样本；淘汰。
- v0.50：几何和文字较稳，但 `global L` 约 `62.1`，仍未真正解决第一版亮度差；不作为候选。
- v0.51：本轮有效候选。`global L` 约 `66.4`，`median L` 约 `47.5`，`dark %` 约 `53.2%`，已经接近第一版的明度结构；几何与真实文字也保持较好。主要遗留问题是北美选区 / 橄榄面略偏黄绿。
- v0.52：肉眼看似压住黄绿，但 `global L` 掉到约 `61.3`，复发“变暗”问题；淘汰。
- v0.53：同明度换 hue 的 prompt 仍导致全局暗回约 `61.3`，不作为交付候选。

当前阶段结论：

- 当前给用户看的色彩矫正版应以 v0.51 为候选，而不是 v0.52 / v0.53。
- v0.51 的局部黄绿问题不应继续通过整屏生图解决；连续两轮证明模型会在“压黄绿 / 换 hue”时连带压低整体明度和纸面占比。
- 后续进入界面替换或生产化时，应把 v0.51 当整屏氛围候选，把第一版当色彩守门锚点；局部北美选区颜色应在实现侧用 palette token / 局部色阶调整，而不是整屏重生成。

新增硬规则：

1. “修局部颜色”不得重跑整屏作为唯一方案。若整屏生图用于探索，必须先过 `global L`、`dark %`、`paper %`、`yellowgreen %` 与几何门禁。
2. 若新图 `global L` 低于当前候选超过 `3`，即使局部颜色更舒服，也降级为失败样本。
3. 第一版可以作为色彩 / 明度锚点，但不能作为结构锚点；不得恢复跨地图路线、空白字段或早期未填充 UI。
4. 纸面占比指标要结合真实内容解释。真实内容版纸面占比低于第一版是可接受的，不能通过清空字段或扩大白纸来追指标。
5. 后续 prompt 中避免使用单独的 `desaturate` / `mute` 作为局部色彩修复主词；这会诱发模型把整屏压暗。应改为“保持同明度的 palette token 替换”，并优先在实现侧完成。

### 7.32 v0.51 局部橄榄 token proof 与运行时小改

触发：

- v0.51 解决了第一版对比下的整体变暗问题，但北美选区 / 橄榄面略偏黄绿。
- v0.52 / v0.53 连续证明：继续用整屏生图修“压黄绿”会把全图重新压暗。

新增产出：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/101-world-map-v051-local-olive-grade-proof.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/102-world-map-v051-local-olive-proof-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/103-world-map-v051-local-olive-grade-proof-v2.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/104-world-map-v051-local-olive-proof-v2-color-check.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/105-world-map-v6g-runtime-selected-olive-token-preview.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/106-world-map-v6g-runtime-selected-olive-token-safe-zones.png`
- `docs/plans/world-map-benchmark-landing/2026-06-30-world-map-selected-region-palette-token-contract.md`

proof 结果：

- proof v1 只证明了局部处理可以保住整体明度，但 `yellowgreen %` 没有下降，反而从 v0.51 的约 `2.8` 升到约 `3.4`；不作为 token 方案。
- proof v2 通过：`global L` 保持约 `66.4`，`median L` 保持约 `47.5`，`yellowgreen %` 从约 `2.8` 降到近似 `0.0`，改动像素约 `7.9%`。
- proof v2 说明：局部 palette token / LUT 可以解决北美黄绿问题，不需要继续整屏生图。

token 结论：

- `selected_region_olive`: `#606548`
- `selected_region_olive_dark`: `#5B5E3E`
- `selected_region_olive_light`: `#807E50`

运行时小改：

- `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapV6gPreview.gd` 已将运行时选中 halo、左侧选中 overlay、选中角标从金黄高亮抽换到上述橄榄 token。
- 该改动只验证运行时 token 可落地，不代表旧 v6g runtime 预览已成为本轮新 benchmark 风格稿。
- 贴图内的北美陆块颜色仍来自 baked texture；后续应通过无字组件资产、局部 LUT 或重切 map board 解决，而不是继续整屏重生图。

验收备注：

- 首次 headless Godot 截图崩溃；改用 `--windowed --audio-driver Dummy --rendering-driver opengl3` 成功生成预览截图。
- 旧 v6g 预览含路线、旧纸面比例和旧美术方向，仅用于技术验证 token，不用于判断本轮“World Mystery Weekly 低多边形纸品”风格是否通过。
