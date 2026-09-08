# 世界地图粗概括 filled-state 视觉方向候选 v1 交付清单

## 交付结论

已完成一张 `1920×1080`、有真实内容的完整世界地图 filled-state 视觉方向候选。它采用“粗概括夜班剪版台”：顶部品牌锁、左侧地区简报、中央宽块面世界地图、单张地图样张、UFO 便签、右侧主稿和被动 Schedule 共享冷石板灰综合色基底。

当前状态：`filled_state_visual_direction_candidate_pending_user`。

本交付不进入 atlas、资产 manifest、Godot 或 `WeeklyRunGame`，也不声称生产冻结。

## 主审图

- `image_gen/2026-08-18/world-map-rough-abstraction-filled-target-v1/10-final-filled-state-visual-target-1920x1080.png`
- 尺寸：`1920×1080`
- SHA-256：`0157E846F772F68AB34291F6FC1D258D6CFB88399D008DC70D8F4C1749B92D7C`

## 真实生图来源与职责

1. `01-filled-state-rough-abstraction-imagegen-raw.png`：从空白画布生成的整屏 ImageGen 原件；负责顶部、地图、右稿、Schedule、综合色、照明与整体编辑部氛围。
2. `02-filled-state-rough-abstraction-1920x1080.png`：仅做无裁切规格化；因 RegionCard 状态改变尺寸而未升格。
3. `03 / 04` 与 `06 / 07`：两轮 ImageGen 定向编辑诊断；证明 selected / warning 可分轨，但整屏模型不能可靠保证重复组件 exact geometry。
4. `05-region-card-blank-master-imagegen.png`：首张共享卡壳真实生图；因表头 / 双栏 / footer 读成后台表格而淘汰。
5. `09-region-card-simple-paper-master-imagegen.png`：最终共享无字卡壳真实生图；只包含连续暖灰纸面与单层综合色背纸。
6. `00-canonical-story-content-reference.png`：三张新闻母图的程序拼版参考，只用于向 ImageGen 说明内容锁定，不替代美术生成。

## 参考图职责

- `benchmark-board-01.png`、`benchmark-board-02.png`：唯一正向美术真值，约束粗轮廓、少量宽块面、现代低彩度纸物件和趣味度。
- A291：只约束顶部 / 左栏 / 中央地图 / 右稿的三栏职责与整屏平衡，不作为纸材画法真值。
- 抽象灰度差距板：负向细节预算参考，阻止多层纸堆、微型版号、条码、准星和完整制造件回流。
- 三张 `1104×704` canonical 新闻母图：只允许完整等比复用，不裁切、不拉伸、不另做缩略图。

## 程序允许范围

脚本：`scripts/art/compose_world_map_rough_abstraction_contract_target_v1.py`。

程序只负责：

- 连通浅色背景转透明；
- 将 ImageGen 共享卡壳等比缩放为统一 `480×244`；
- 在固定位置复制三次；
- 将三张 canonical 母图等比缩至 `207×132 / 69:44`；
- 回填真实中文、selected / locked / warning 和 footer；
- 保证三卡同构、文字安全区和最终 `1920×1080` 输出。

程序没有重画顶部、地图、纸材纹理、右稿、Schedule、CTA、Disclosure、地图照片或 UFO 便签。

## 功能合同回归

| 项目 | 结果 |
| --- | --- |
| 桌面 `1920×1080`、三栏结构 | 保持 |
| 三张 RegionCard 同宽同高 | 通过，三实例均 `480×244` |
| 三张左卡统一图片槽 | 通过，均为 `207×132 / 69:44` |
| canonical 新闻母图 | 通过，`1104×704 → 207×132`，只等比缩放 |
| selected / warning 分轨 | 通过，蓝色“已选择”与锈红警示分离 |
| locked 同位 | 通过，02/03 使用与 selected 同位状态签 |
| Schedule passive | 通过，无箭头、展开或 hover 暗示 |
| 地图照片 / UFO 便签 | 保持 NO-HIT 视觉，不新增假控件 |
| Dossier / Disclosure / CTA | 位置与层级保持 |
| 功能面 `0°` | 保持 |

## 最终卡壳 ImageGen 提示词

> Create a replacement blank RegionCard material master. This is a single reusable art asset, not a UI screen. Image 1 is a negative structure reference: do not repeat its header band, image cell, right data cells or footer bar. Image 2 provides the cool night-newsroom screen context. Images 3 and 4 are the positive clean-low-poly-weekly style truth. Output one large front-facing landscape paper card on a transparent background, about 1.97:1, 0° orthographic. Use exactly two visible layers: one restrained desaturated cool-cobalt/slate backing sheet visible only as a 6–8 px irregular edge, and one warm-neutral editorial paper front sheet with a single hand-cut contour. The front sheet is one continuous surface with only subtle broad low-poly facets. Remove all internal panels, placeholders, rules, grids, nested borders, footer bars, clips, tape, pins and manufacturing detail. Contemporary, playful and rough-abstract; not CRM, SCP, GIS or old archive.

完整整屏空白起稿提示词与后续定向修图提示词保留在本轮 Codex 工具调用记录；最终可复现资产以主审图、共享母版和合成脚本为准。

## 双审

- UX 老哥：`P0=0 / P1=0 / P2=2 / PASS`。后台表格感、warning 假按钮和 footer 贴边均已关闭；P2 为运行时最长中文与 CTA disabled 误读防护。
- UI Designer：`P0=0 / P1=0 / P2=2 / PASS`。三卡读作同族编辑部简报纸，综合色跨三栏成立，不应再以增加装饰或字段提升完成度。

## 下一步

等待用户只裁决美术方向：是否认可这套“粗概括夜班剪版台”作为下一阶段视觉目标。认可前不拆资产、不制作正式壳、不进入 Godot。
