# 区域地图界面风格板 v1 交付清单

## 决策条

- **结论**：首轮区域地图风格板达到“有条件通过”，可交给用户判断原型与氛围方向；尚不能升格为生产标杆。
- **影响**：世界地图与区域地图已从“同图两级缩放”拉开为“全球选题总台”与“本地事件作业图”；中央地图、事件票据、任务案卷和日程 / 签批家族已经在同一张板上建立。
- **下一步**：用户先判断综合色调、严肃度和黑色幽默剂量；方向确认后，再严格套入黑白功能稿生成完整区域地图有字风格稿。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = regional_event_map_component_style_board_v1`
- `status = conditional_pass_pending_user_review`
- `production_candidate = false`
- `runtime_implemented = false`
- `scope_invariant = unverified`

本产物是一张区域地图组件美术语言板，不是完整游戏界面、真实运行截图、无字资产母版、状态 atlas 或正式美术真源。

## 用户主审入口

- 完整风格板：`image_gen/2026-07-28/region-map-interface-style-board-v1/01-region-map-interface-style-board-v1.png`
- 25% 缩略：`image_gen/2026-07-28/region-map-interface-style-board-v1/02-region-map-interface-style-board-v1-25pct.png`
- 世界地图 A / 区域地图 v1 对照：`image_gen/2026-07-28/region-map-interface-style-board-v1/03-world-a-region-v1-comparison.png`
- Mapness / 对象语言 QA：`image_gen/2026-07-28/region-map-interface-style-board-v1/04-region-map-interface-style-board-v1-qa.png`
- 生图 Prompt：`docs/plans/region-map-style-board/2026-07-28-region-map-style-board-v1-prompts.md`

`image_gen/` 当前被 `.gitignore` 忽略；图片已经落入工作区，但没有进入 Git 追踪。

## 生成链

- 生图方式：Codex 内置 `imagegen`。
- 首轮：根据区域黑白功能稿、世界地图 A 和两张直接标杆生成区域组件风格板。
- 定向修正：只纠正中央地图颗粒 / 道路密度、手工幽默符号、`DAY 01` 拟物重量、重复 globe 和证据媒介色相。
- 程序只用于 25% 缩放、世界 / 区域对照排版和 QA 裁切，不替代真实生图。

原始生成输出：

- 首轮：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_ShzX4dGaopRER2y2yc39VQKt.png`
- 最终修正：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_RIP5Ws39CosUlJMkAcNArppK.png`

## 视觉主语

- 世界地图：`region-centric` 全球选题总台，少量地区入口、全景、开阔。
- 区域地图：`event-centric` 本地事件作业图，同一区可有 `0–N` 个事件坐标、近景、正在工作。
- 三处选中联动：左侧 `R-21` 事件票据 → 中央 `R-21` 地图坐标 → 右侧 `R-21` 任务案卷。

## UI Designer 原始结论

- 桌面 16:9 组件风格板采用：左事件票据、中部主地图、右任务案卷、底部日程与签批。
- 资产覆盖区域地图底纸、事件坐标族、事件短签、事件票据、现场证据、任务案卷、日程组件和派遣 CTA。
- 综合色彩以深海军 / 石板蓝为家族底，区域页比世界页增加暖纸与橄榄，不变成旅行手账。
- 地图使用大低多边形块面和少量制图线，现场图不用摄影，纸件拟物但动态文字面保持正交。
- 黑色幽默只藏在现场批注、盖章和小贴纸中。
- 25% 必须读成“被事件、证据和派遣手续占据的本地外勤工作桌”。

## UX 老哥原始结论

- `P0 = 0`。
- `P1`：若左票据、右证据、底部五项同时精做，会把地图压成 Dashboard；因此底部压为两组，证据只留 `1–2` 件。
- `P1`：若仍为完整平面地图加少数圆点，会读成世界地图二级缩放；因此必须保留局部地貌、现场圈注和同区 `0–N` 事件。
- `P2`：品牌贴纸与证据平均散布会互抢；黑色幽默集中到选中事件附近，非功能贴纸数量低于世界页。
- 与世界地图共享 A 配色、纸张、CTA 和标签语法，符合跨屏视觉一致性（KB-X-2）。
- 进入区域时必须继承世界页选中的地区上下文（KB-X-3），并以“打开地区案卷”而不是普通缩放表达转场（KB-X-8）。
- 结论：有条件 GO；首图必须通过 25% 缩略复核。

## Gate 结果

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 真实生图 | `pass` | 首轮与定向修正均来自内置 imagegen |
| 直接标杆方向 | `directional_pass` | 现代周刊拼贴、哑光色块、薄纸层与尺度错落基本成立 |
| 世界 / 区域原型区分 | `pass_visual` | 25% 对照下，世界页先读全球地图，区域页先读本地事件作业图 |
| Mapness | `pass_visual` | 遮住任务文字后仍能凭陆水关系、地区、铁路 / 主路和地标读成区域地图 |
| `event-centric` | `pass_visual` | 地图存在多事件坐标，同一区不只一个固定入口 |
| 低多边形颗粒 | `pass_after_revision` | 二轮压缩道路与小切面后，大块地貌 / 水域结构先于微细节被读取 |
| A 配色同族 | `directional_pass` | 深海军、石板蓝、暖纸、橄榄、芥末和少量状态蓝保持同族；尚未逐像素抽取正式 token |
| 纸张合同 | `directional_pass_only` | 纸张较干净、薄、现代；未做角色级纸材 mask 与精确 token 归一 |
| 黑色幽默 | `pass_with_watch_item` | 天线批注已从标准禁令牌改为手工便签，但笑点仍较克制，需用户判断剂量 |
| 严肃度 | `pass_with_watch_item` | 怪异事件与媒介变化已成立，但 `CASE FILE` 和底部正式票据仍保留较强机构感 |
| 正交 / 安全区 | `unverified` | 肉眼看功能面正交，但本轮未做几何测量、中文填充或最长文案测试 |
| `scope_invariant` | `unverified` | 内置 imagegen 没有 mask，不能证明定向修正的 ROI 外像素逐像素不变 |
| 生产标杆 | `blocked` | 未经用户确认，且没有有字界面、状态矩阵、运行截图与直接标杆最终复审 |

## 25% 反向读法

- 不是世界地图放大版：没有 globe / 大陆 / 全球网格，主语是本地海岸、铁路、工业地标和多事件坐标。
- 不是旅行社：没有目的地明信片、导航路线、罗盘或自然和谐色盘。
- 不是军事 / 情报台：没有雷达、准星、扫描线、SECTOR 大章或战术路径。
- 不是犯罪证据板：没有警徽、警戒带、红线关系网或法证照片。
- 不是纯软件 Dashboard：中央地图面积和纸面对象仍是第一阅读层。

## 尺寸与哈希

| 文件 | 尺寸 | SHA-256 |
| --- | --- | --- |
| 完整风格板 | `1672×941` | `231fc9b186f3b02ed19598fbabd02425fb0f080d5d2fa77631844db695ab63e7` |
| 25% 缩略 | `418×235` | `3887cdc9885578bc9677c8a326f9c056c32d4b421885f2f603887eff37977122` |
| 世界 / 区域对照 | `1690×524` | `079f1649fb0bc6ad94e4ea05d359423c3efbfe20ecc42f7a3a6d4867fecb6161` |
| QA 图 | `1220×720` | `a7b9dc2512bb254eed71f50625e1dd64cc51005e239fcbf02e8f01e32bec582c` |

## 允许下一步

- 用户确认或定向调整区域地图的综合色调、严肃度、黑色幽默剂量和组件家族。
- 方向确认后，严格按照区域地图黑白功能稿生成一张完整有字风格稿。

## 禁止跳步

- 不切 atlas、不接 Godot、不写正式 runtime token。
- 不把当前英文文字、图钉、纸件直接当作可复用生产资产。
- 不把当前板称为 Angus 正式全局美术真源、生产标杆或资源标杆。
- 不在用户确认前登记为新的正式美术采纳项。
