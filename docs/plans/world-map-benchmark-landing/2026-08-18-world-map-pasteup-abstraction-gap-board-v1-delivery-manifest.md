# 世界地图「粗概括 vs 过度精制」差距板 v1 交付清单

> 日期：2026-08-18  
> 产物类型：`problem_overlay / diagnostic_constraint_board`  
> 状态：`dual_review_pass / ready_as_next_imagegen_visual_reduction_attachment`  
> 边界：不是生图目标、不是功能合同、不是资产母件、不是 Godot runtime 证据。

## 1. 交付物

- 标注板：`image_gen/2026-08-18/world-map-pasteup-abstraction-gap-board-v1/01-benchmark-vs-current-abstraction-grayness-gap-board-1920x1080.png`
- 可复现排版脚本：`scripts/art/annotate_world_map_pasteup_abstraction_gap_v1.py`

用户提供的四个 benchmark 裁切已保存为：

- `reference-crop-01-masthead-folder.png`
- `reference-crop-02-folder-family.png`
- `reference-crop-03-weekly-folder.png`
- `reference-crop-04-documents.png`

当前反例为：

- `image_gen/2026-08-18/world-map-pasteup-internal-variants-v1/02-color-separation-proof-1920x1080.png`

## 2. 制作方式

本板由程序读取真实 benchmark 裁切与当前 02 全屏图，只做裁切、等比缩放、红框、编号、中文说明和方向性色块排版。程序没有生成或替代美术内容。板上色块只表达“保留色相、降低色度、共享冷石板灰”的关系，不是正式色值或生产 token。

## 3. 板上结论

### 标杆完成度

- 一个主轮廓统领纸层；
- 每件以 `3–6` 个宽明度 / 综合色块表达；
- 一张背纸或一件夹具足以说明接触；
- 蓝、青、橄榄、芥末和暖纸共享低彩度冷石板灰底；
- 完成度集中在大形、综合色与压叠关系，不集中在微型工艺数量。

### 当前 02 的五处超量

1. 左卡三次重复完整壳、双框、独立底栏、重复状态装饰与独立投影；
2. 地图仍是密三角与完整套印描边；
3. 右稿同时存在纸堆、夹子、色样轨、准星、细框与微型版号；
4. Schedule 的环装、铆钉、条码与内框共同形成假控件；
5. 品牌锁组后又接工具图标、准星与条码，重新形成机构状态栏。

## 4. 并列 Gate

### 冻结不减

- 桌面三栏职责；
- 三张等高 RegionCard；
- 统一 `69:44` 图窗；
- selected / locked；
- 地图轮廓、相对位置与地区定位；
- 右稿动态槽；
- Disclosure；
- CTA；
- Schedule `passive`；
- 功能承载面 `0°`。

正式 ImageGen prompt 必须把 `69:44` 展开为：同一张 `1104×704` canonical 母图仅等比缩放，不裁切、不拉伸、不另做缩略图。`可见载体层级 ≤2` 也必须展开为“每个组件最多两层可见载体”，不能让模型理解成整屏只有两层。

### 主动降级

- 每个组件最多两层可见载体；
- 每张卡只保留一个显式状态主承载位；
- 每个组件最多一张明显背纸；
- 右稿只保留一个夹具；
- 地图每个主要大陆先读 `3–6` 个主明度 / 综合色质量块，同时保持轮廓与定位可辨；
- 顶部工具图标、准星、条码、色样最多保留一个弱化的非交互印刷提示；
- CTA / Disclosure 本身不可删除，只削减外围厚底板、铆钉和重复阴影。

## 5. 双审

### UX 老哥

初审发现三项 P1：缺少 frozen 功能白名单；状态签 / CTA 有误删歧义；“每洲 3–6 面”可能损伤地图导航。板已全部修正。快速回归为 `P0=0 / P1=0 / P2=2 / PASS`。两个 P2 均已写入本清单的正式 prompt 提醒：展开 canonical 母图复用措辞；灰化综合色不能只依赖板上小字。

### UI Designer

初审确认 benchmark 拆解和五个红框方向正确，要求把“纸层少”改为“一个主轮廓统领纸层”，并把共同灰底解释为保留色相、降低色度。修订后判定可作为下一张 ImageGen prompt 的视觉减法附件。正式 prompt 仍须同时附 frozen 功能合同、地图先行宏观构图和完整负面词。

## 6. 下一步

若用户确认继续生成，下一张必须从空白画布重新生成完整 `1920×1080` filled-state visual target；不能编辑 02 继续减纹理，也不能把 02 当构图母版。输入应同时包含：

1. 两张正式 benchmark，负责正向塑造真值；
2. 本差距板，负责抽象度和微工艺减法；
3. A305 / A306 frozen 功能合同文字；
4. A310 地图先行宏观构图；
5. A311 综合色共同灰底与防泛黄约束。

