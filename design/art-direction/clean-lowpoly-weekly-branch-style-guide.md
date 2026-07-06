# Clean Low-Poly Weekly Branch Style Guide

> 状态：支线风格验证，不是 Angus 全项目正式美术真源。  
> 创建日期：2026-06-24  
> 当前应用范围：优先服务世界地图、地区卡、右侧 dossier、票条 / sticker / icon atlas 的 UI 落地验证。  
> 转正条件：只有当世界地图、地区界面、任务派遣等多界面铺量验证通过，并经 `@像素艺术` 生成后复审通过，才考虑并入 `angus-visual-style-guide.md`。

## 1. 为什么另开支线

这组标杆和项目之前的像素艺术记录差异较大：它不是角色高清微像素，也不是早期重纸纹、重半调、旧档案感的资产化 UI。它更像一套**干净现代周刊编辑部 + 大块低多边形图形设计 + 轻纸品物件**的 UI 视觉语言。

因此当前只作为世界地图视觉落地支线推进。不得因为局部效果成立，就直接覆盖角色美术、全局像素颗粒、正式 UI 真源或既有美术规范。

## 2. 归档参考

原始标杆：

- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`

纸张材质合同：

- `design/art-direction/clean-lowpoly-weekly-paper-material-contract.md`
- `docs/screenshots/2026-07-01-wmw-component-correction/13-wmw-paper-material-truth-board-v0-3.png`
- `docs/screenshots/2026-07-01-wmw-component-correction/14-wmw-paper-material-truth-samples-v0-3.json`

关键问题裁切：

- `design/art-direction/references/clean-lowpoly-weekly-branch/sticker-reference-crop.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/ticket-flat-problem-crop.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/icon-too-regular-problem-crop.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/premium-sticker-reference-crop.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/v0-5-too-dark-muddy-problem-crop.png`

本轮阶段样本：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/04-world-map-ui-v0-3-colorblock-draft.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/05-right-dossier-base-v0-4.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/08-right-dossier-validation-contact-sheet-v0-4.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/09-world-map-1920-dossier-v0-4-validation.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/10-ticket-symbol-atlas-v0-5-handdrawn.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/11-ticket-symbol-atlas-v0-6-premium-light.png`
- `docs/screenshots/2026-07-01-wmw-component-correction/01-wmw-component-correction-sheet-v0-1.png`
- `docs/screenshots/2026-07-01-wmw-component-correction/02-wmw-component-correction-sheet-v0-2-no-text.png`

## 3. 核心理解

这条支线的关键词不是“质感丰富”，而是**图形概括准确**。

标杆的视觉力量来自：

- 大块低多边形色块的明度变化。
- 清晰剪影、硬边阴影和少量冷暖色块。
- 现代周刊版式、大标题、色票、标签、文件夹和纸件叠层。
- 轻微手绘 / 裁纸感的不规则边缘。
- 干净但不空洞的纸面。
- 贴纸式、概括式、轻微歪斜的符号系统。

标杆不依赖：

- 重纸纹、污渍、旧档案黄、旧报纸脏感。
- 摄影噪声、雾气、刮痕、随机颗粒。
- 密集三角网、GIS 终端纹理、过细海岸线。
- 规则软件 icon、统一线宽矢量图标、通用游戏按钮 bevel。

## 4. 低多边形规则

低多边形必须是“大块概括”，不是“细密三角网”。

通过标准：

- 一个主体先读出大剪影，再用 3-8 个主要明暗面塑造体积。
- 场景 / 快照在缩到 25% 时先读出大色块和主物体，不读成纹理。
- 天空、山体、地图大陆、异常物件优先使用大三角、大梯形、大斜四边形。
- 轮廓可以有手绘式轻微不规则，但不要写实细边。

失败表现：

- 全图被均匀三角面切满。
- 大陆、小岛、海岸线过细，读成 GIS / 雷达底图。
- 快照像照片加 low-poly 滤镜，而不是编辑部重绘的图形插图。
- 为了“高级感”增加雾、纸纹、颗粒、刮痕。

## 5. 纸件和票条规则

纸件应是现代周刊工作物件，不是旧档案。

票条和 CTA 的正确方向：

- 中心 `content_rect` 必须干净，能承载动态中文。
- 但中心区域不应纯平空白，可保留极轻的 4-7 个大块色面或印刷压层。
- 彩色框体内应有低多边形明度变化，避免变成 SaaS 表单条。
- 票条边缘应像纸签 / 印刷切片 / sticker-cut，轻微不规则。
- 红橙只给 danger、alert、primary CTA。

票条和 CTA 的失败方向：

- 完全纯平矩形，失去标杆色块起伏。
- 过度 bevel、高光、阴影，读成通用手游按钮。
- 孔洞、条码、短刻度、细线、点阵全部堆在一个组件里。
- 斜纹、箭头、角切、描边、高光同时出现，导致图形过忙。

## 6. 符号和贴纸规则

图标不应是标准软件 icon，而应像标杆贴纸区的图形符号。

正确方向：

- 厚线、概括轮廓、手绘不完全规整。
- 白色剪纸边、贴纸边、少量套印错位。
- globe、eye、warning、hand、arrow、document 等符号可以轻微歪斜。
- 小图标里也可以有大块低多边形色块，但不要细碎。

失败方向：

- 完美圆、完美三角、统一线宽、规则矢量图标。
- 图标像系统工具栏，而不是周刊贴纸。
- 为了“手绘”增加太多脏边、毛刺或随机噪点。

## 7. 已踩坑记录

1. **把标杆误读成重质感。**  
   结果会加纸纹、污渍、摄影颗粒和刮痕。正确做法是用低多边形色块明度塑造质感。

2. **把低多边形做成细密三角网。**  
   世界地图、快照和地区卡会变成 GIS / 雷达终端，而不是周刊图形设计。

3. **为了 UI 可读性把票条做成纯平表单。**  
   文字区变安全了，但标杆味丢失。正确做法是文字区干净但仍有极轻的大块色面压层。

4. **把图标做成规整软件 icon。**  
   规则图标削弱标杆的贴纸、手绘、周刊物件感。

5. **直接生成整屏概念图。**  
   整屏图容易好看但不可落地。必须拆成无字底图、动态文字、安全区 overlay、状态 atlas 和 1920 截图验证。

6. **右栏尺寸未先验证。**  
   右侧 dossier 单独好看，但放入 1920x1080 后会压中央地图。正式布局需要右栏固定列或缩窄到约 520-580px。

7. **小组件变土、变暗、变厚。**  
   v0.5 找回了手绘贴纸和低多边形色块，但纸边太厚、暗部太黑、颜色偏泥、整体像土黄色手工贴纸，缺少远标杆里的干净高级感。正确方向应更轻、更清透、更现代：纸边薄而白、阴影克制、暗部不死黑、橄榄和青绿更干净、红橙更清爽，保留概括手绘但不要滑向民俗 / 手账 / craft paper。

8. **整屏验证时又回到低多边形渲染。**  
   v0.17 把 v0.16 小组件放回世界地图后，票条语言能成立，但中心地图、右侧快照和左侧缩略图又出现细碎三角、场景插画和 GIS 感。整屏验证不能只看“有 low-poly”，必须继续检查块面颗粒度：标杆是大块剪纸式概括，不是低多边形 3D 渲染或细密三角网。

9. **信息承载面被纸件感带斜。**  
   v0.18 虽然减少了碎三角和微细节，但右侧 dossier、左侧地区卡、底部票据整体倾斜，违反“承载信息的 UI 面必须正交”的硬规则。后续 prompt 和验收必须先锁定：凡有动态文字、可点击热区、缩略图框、状态条、按钮文案或真实中文填充的正面区域，一律 0 度水平 / 垂直；斜切、胶带、夹子、背后纸张露边只能存在于 no-text 装饰层。

10. **为了修正交把风格修平。**  
    v0.54 这类正交约束稿虽然改善了功能面倾斜，但中央世界地图多边形变成更碎的细密三角网，左侧卡片、右侧 dossier、CTA 和底部票据上的低多边形平面色块被抹平，结果从“低多边形周刊纸品”滑向“干净软件 UI”。后续必须双闸门验收：先看功能面是否正交，再看同一批功能面是否仍保留大块平面色块、4-8 个主要明度块面、块状阴影和手绘贴纸张力。不能用扁平空白矩形解决文字安全区。

11. **把色块误写成褶皱。**  
    v0.55 的 prompt 把标杆文字组件上的平面明度色块误写为 `folds / 褶皱 / 折痕`，导致文本槽出现纸张折起感。原标杆的文字组件不是折纸纹理：它们只有低对比、平面的低多边形色块和明度块面，不应有明显 crease / wrinkle 线穿过可写区。后续 prompt 必须写 `flat low-poly color-value blocks`，并负向排除 `creases / wrinkles across text slots`。

12. **右侧 dossier 轻斜仍然一票否决。**  
    v0.55 虽然找回了一部分大色块，但右侧 dossier / CTA stack 仍有可见倾斜。该图降级为“色块恢复但正交失败”的偏差样本，不得作为生产候选或下一步切图源。后续生成后必须先裁切右侧 dossier、CTA stack、底部 receipt 并叠水平 / 垂直参考线；只看整屏观感或说“基本正”都不算验收。

13. **QA 框不能替代真实边线。**  
    v0.56 暴露两个复发问题：底部 receipt 右侧出现高对比白色折角 / 撕裂状痕迹，仍然把“平面低多边形色块”误生成为纸张 fold / tear；右侧 CTA stack 的真实生成边线仍有可见倾斜。`111-world-map-wmw-flat-color-orthogonal-v0-56-qa.png` 与 `112-world-map-wmw-flat-color-orthogonal-v0-56-right-qa-crop.png` 只能证明手动画的参考框是正的，不能证明图本身正交。后续 QA 线必须贴住真实生成边缘；只要真实边缘斜，即使参考框水平也失败。

14. **把组件校正误扩成整屏重生。**  
    用户的原始诉求是把标杆中的组件改成能承载真实游戏 UI 的组件语言，而不是持续重生整张世界地图。整屏生图每次都会重新解释地图、配色、纸张、按钮、材质和构图，导致旧优点被冲掉、新问题不断出现。后续应先做组件校正板：地区卡、右侧 dossier、CTA、底部 receipt、贴纸图标、标题条等逐类转译；只修正正交、可写区、状态矩阵和符号嵌合问题，其它标杆味道尽量不动。组件板通过后，再把组件放回世界地图做单状态验证。

15. **不能靠 prompt 形容词复刻纸张。**  
    纸张是这条支线的基础材质，不能每轮让生图模型重新理解 `warm beige / advanced gray / paper texture`。后续必须先引用 `clean-lowpoly-weekly-paper-material-contract.md`：从标杆裁切 token 锁定纸色和纸纹，再做组件形状、生图、后处理或回填验证。v0.5 只能作为色彩方向候选，不是纸张材质真源；纸张真源来自标杆 crop board。

## 7.5 高级感 / 舒适度闸门

小组件必须同时满足“手绘概括”和“干净高级”。不能只因为符号不规整、色块回来了，就放行。

通过标准：

- 纸边是干净暖白 / 象牙白，不是厚黄纸板。
- 色彩清透，橄榄绿、青绿、红橙之间有层级，不灰、不脏、不糊。
- 暗部用深海军蓝 / 深墨绿控制，不大面积死黑。
- 阴影轻，只表达叠层，不制造笨重贴纸块。
- 符号粗犷但自信，像现代周刊贴纸，不像廉价手账贴纸。
- 留白充足，组件之间有空气感。

失败表现：

- 整体偏土黄、偏棕、偏脏绿、偏黑。
- 纸边过厚，像硬纸板或手工剪贴。
- 组件阴影厚重，显得笨、沉、廉价。
- 为了手绘感把图标画得幼稚、民俗或低龄。
- 票条虽然有低多边形，但低对比泥色让画面发闷。

v0.6 方向样本：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/11-ticket-symbol-atlas-v0-6-premium-light.png`

v0.6 修正了 v0.5 的“土暗厚”，但不能作为色彩通过样本：纸边 / 高亮纸面被推到 `#F3E8D9`，明显高于标杆贴纸裁图约 `#C2BAAC`；橄榄绿也从标杆约 `#4E623D` 漂到 `#747945`；警示红橙从低饱和锈色漂到 `#BD4F26`。下一轮不能整体压暗或整体提亮，必须按 token 色号回到标杆，同时重新加入更像 `premium-sticker-reference-crop.png` 的概括、歪斜和黑色图形张力。

## 7.6 小组件色彩合同 v0.1

详见：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/12-ticket-symbol-color-contract-v0-1.md`

v0.7 的临时色彩目标：

- `paper_high`：目标 `#C2BAAC`，允许约 `#BEB5A6` - `#C9C0B0`；禁止 v0.6 的亮白 `#F3E8D9`。
- `paper_mid`：目标 `#B2AB9B` - `#BCB4A5`，可写区不能惨白。
- `olive_mid`：目标 `#4E623D` - `#5B6A37`；禁止偏黄偏亮的 `#747945`。
- `olive_dark`：目标 `#3F4C2D` - `#435737`。
- `warning_rust`：目标低饱和锈红 / 红棕 `#6D462D` - `#8A4E32`；禁止鲜红橙 `#BD4F26`。
- `teal_blue`：目标 `#384946` / `#293C41`；不能因为修正亮度而继续压黑。
- `ink_dark`：目标 `#191E1F` - `#272A2B`；避免 v0.5 的死黑 `#080F19`。

## 8. 落地验证链

每个组件进入生产候选前，至少通过以下验证：

1. **无字底图**：没有烘死中文、数字、按钮文案和任务数据。
2. **安全区 overlay**：明确 `content_rects / no_text_rects / hit_rects`。
3. **真实中文填充**：使用当前游戏字段，不用占位假字。
4. **状态 atlas**：至少 default / hover / selected / locked / warning。
5. **1920x1080 截图**：确认在真实桌面界面比例中可读、可点、风格不掉。
6. **像素艺术复审**：若要升级为生产标杆 / 真源候选，必须复审通过。

## 9. 当前阶段结论

已阶段性成立：

- v0.3 的“色块塑形”方向大致对。
- v0.4 右侧 dossier 单组件能承载真实中文。
- v0.5 票条 / 符号方向修正了“过平”和“过规整”的问题。
- v0.6 票条 / 符号方向修正了“土暗厚”的问题，但颜色过亮、过白，不能作为色彩通过样本；下一轮必须按 `12-ticket-symbol-color-contract-v0-1.md` 复采样。
- v0.8 票条 / 符号候选解决了 v0.6 的过亮白和 v0.5 的泥厚问题，可进入小范围真实 UI 验证。
- v0.16 是当前较干净的小组件候选，适合进入真实 UI 验证，但仍不是 exact 色号通过。
- v0.18 在“大块色面、低微细节”上比 v0.17 有进步，但因信息面倾斜，降级为偏差样本。
- v0.19 是当前世界地图局部落地验证候选：在保持 v0.18 大块面方向的同时，恢复了信息承载面的正交硬规则。
- 2026-07-01 的 `02-wmw-component-correction-sheet-v0-2-no-text.png` 是组件转译候选：相比继续整屏重生，它更符合“先修可复用组件、其它不动”的流程；但尚未经过真实中文填充、逐组件安全区、色号复采样和像素艺术复审，不能升级为生产候选。
- 2026-07-01 的 `07-wmw-component-correction-sheet-v0-5-balanced-advanced-gray.png` 是当前“高级灰但不土”的色彩方向候选：比 v0.3 少黄褐土味，比 v0.4 少旧档案感。它仍不是生产候选；warning / rust 的饱和度和纸面高光还需在真实世界地图单状态里继续压测。

仍未通过：

- 中央世界地图 v0.18 已明显减少碎片，但正式底图仍需继续删小岛、删细海岸、删密集切面。
- 快照和缩略图仍略偏场景插画 / low-poly render，不够手绘概括。
- 右侧 dossier 放进 1920x1080 后偏大，需要布局列约束。
- 小组件还没有完成真实中文填充、状态 atlas 和可点击热区验证；当前只是整屏视觉局部验证通过一轮。
- 小组件颜色还需在真实中文填充里复核，尤其 `ink_dark`、`background_dark`、`teal_blue` 偏暗，以及 `paper_mid` 是否压字。
- 尚未完成左侧地区卡、任务派遣、地区界面的铺量验证。

## 10. 转正条件

这条支线只有满足以下条件，才可考虑并入正式 Angus 美术风格：

- 世界地图：右侧 dossier、左侧地区卡、中央地图、底部票条、pin / sticker atlas 全部通过真实界面验证。
- 地区界面：能保持同样的色块塑形和手绘贴纸符号，不退回普通面板。
- 任务派遣：角色、任务卡、签批票条、CTA 不与当前角色高清微像素方向冲突。
- 多屏截图放在一起时，仍像同一套游戏，而不是一张独立漂亮风格稿。
- `@像素艺术` 复审确认它继承标杆，且没有滑向旧档案、重纸纹、纯科幻终端或通用手游 UI。

在转正前，所有相关稿件统一称为：

```text
clean low-poly weekly branch
```

不要称为：

```text
Angus 正式全局美术真源
生产标杆
资源标杆
```
