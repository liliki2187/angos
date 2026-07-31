# 世界地图六版配色候选 v1 交付清单

## 决策条

- **结论**：六版完整配色候选已生成，可进入用户横向选择；尚无主方案。
- **影响**：A–C 用于比较相近蓝色的色号、灰度与明度；D–F 用于比较标杆体系内的青蓝、烟灰靛和橄榄主导扩展。
- **下一步**：用户选择一个主方案，或指定“以某版为主、吸收另一版的状态色”。选择前不冻结正式 palette。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = six_colorway_comparison`
- `status = colorway_set_v1_pending_user_selection`
- `production_candidate = false`
- `runtime_implemented = false`
- `scope_invariant = unverified`

六版均为桌面 16:9 世界地图风格板的综合色彩候选，只用于判断色彩气质、信息层级与状态色面积，不代表正式 token、runtime 状态矩阵、atlas 或其他界面已经同步。

## 用户主审入口

- 六版 3×2 对照板：`image_gen/2026-07-28/world-map-colorways-v1/07-world-map-colorways-v1-review-board.png`
- 三处 100% 裁切 QA：`image_gen/2026-07-28/world-map-colorways-v1/08-world-map-colorways-v1-100pct-qa.png`
- 六张完整大图：
  - A：`01-a-night-slate-blue.png`
  - B：`02-b-faded-old-denim-blue.png`
  - C：`03-c-deep-ink-navy.png`
  - D：`04-d-petrol-teal-blue.png`
  - E：`05-e-smoky-indigo-gray.png`
  - F：`06-f-olive-led-gray-blue.png`
- 上述文件统一位于：`image_gen/2026-07-28/world-map-colorways-v1/`
- `image_gen/` 当前被 `.gitignore` 忽略；图片已落工作区但未进入 Git 追踪。

## 共同输入与生成方式

- 唯一编辑基线：`image_gen/2026-07-28/world-map-interface-style-board-v3-component-language/01-world-map-interface-style-board-v3-component-language.png`
- 直接标杆：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- 生成方式：Codex 内置 `imagegen`；每个方案一次独立真实位图编辑，不互相套娃。
- E 首轮误洗橄榄大陆，未进入最终目录；最终 E 以一次定向真实 imagegen 编辑恢复橄榄、芥末与暖纸。
- 程序只负责 25% 缩放、3×2 对照排版、色卡文字与 100% 裁切，没有替代生图。

## 六版 palette brief

| 方案 | 气质 | B0 背景 | B1 结构层 | B2 状态锚点 | 主要风险 |
| --- | --- | --- | --- | --- | --- |
| A 夜班石板蓝 | 最均衡、最接近默认标杆 | `#071923` | `#40566A` | `#426E96` | 个性相对保守 |
| B 旧牛仔蓝 | 褪色办公文件夹、略暖 | `#0A1823` | `#495D74` | `#5E82A7` | 蓝纸面积比 A 稍显眼 |
| C 深墨海军蓝 | 最深、最悬疑 | `#05151E` | `#2C424D` | `#426C83` | 暗部层次可能偏紧 |
| D 煤油青蓝 | 夜班冷光、偏青绿 | `#06191D` | `#355A59` | `#477D8C` | 需防止与事件青光混为一类 |
| E 烟灰靛蓝 | 更古怪、冷灰、轻微偏靛 | `#101622` | `#4A5066` | `#66718F` | 与锁定灰紫的距离较小 |
| F 橄榄主导·灰蓝状态 | 最接近标杆 01 的品牌比例 | `#0A1818` | `#596247` | `#587E90` | 状态蓝最克制，可能需要微抬 |

色号是目标区间与对照标签，不是对生图结果逐像素取样后的正式 token。用户选定主方案后才能进入正式 palette 抽取与合同化。

## 共同冻结项

- 画布、布局、构图、组件数量、组件轮廓、文字、字号、位置、地图拓扑、圈选与连接线几何。
- 新闻图、三处塔、低多边形颗粒、UFO、符号试条、`DAY 1` 的对象画法。
- 暖纸、纸边、纸纹、夹子、回形针、胶带、阴影和黑色墨线。
- `WORLD MYSTERY WEEKLY`、`ISSUE 01`、`REGION INDEX`、`DEFAULT/SELECTED/LOCKED`、`NEWS LEAD`、`01/02/03`、`WMW` 与 `DAY 1` 的身份。
- 不新增按钮、路线、图例、玩法、信息或装饰物。

## 视觉验收

### 25% 对照

- 六版第一层均保持中央地图、塔楼事件图和右侧 `NEWS LEAD`，没有恢复大面积钴蓝走廊。
- 六版均能依靠颜色、`SELECTED` 文字、`02` 编号、圈选和连接关系识别当前对象。
- A–C 差异主要是灰度、明度和冷暖；D–F 的综合色彩身份在缩略图中可辨。

### 100% 裁切

- `SELECTED CARD`：六版状态标签、`02` 与纸背层次均清晰。
- `MAP 02`：六版 selected 填色、圈线、编号与相邻橄榄大陆没有合并。
- `DOSSIER BACKS`：六版右侧纸堆仍读作哑光文件夹，不读成高亮塑料外壳。
- E 最终版已恢复非蓝色橄榄 / 芥末 / 暖纸；F 保持青色事件照片与橄榄结构分工。

## 产物哈希

| 文件 | SHA-256 |
| --- | --- |
| A | `b0838a549e200f5b04d43874d7f804b5b1b55fe5462b42f6387018aeaee13050` |
| B | `75e02e4f1e98697706ccdba2019eda3134fac078d853976122b74d10049ca6d1` |
| C | `1826ee32b74a618bad314cb0fcfe980b064e5e459e77212b5137b9e880f626be` |
| D | `711fce32b3a53ef74bd9438a91b0601c05ef76ab4805e386898b5a01a83db84f` |
| E | `84f86ad406d003db9e0a2020710ae28f7e928f75b132c7ebe377837f3ea46612` |
| F | `3bd19a6a8a773e58bb0a65b7cf29aa5512e1c22785092df46c3ca8e6763d3abb` |
| 3×2 对照板 | `5cc8c7312d6cded912ace229290071d0707b6cac4783746fd0de839e871b89f1` |
| 100% QA | `29fce7ba4a0e10d284a941926413de911c461c91a997e5fed15d4a56fcfa676e` |

## Gate 结果

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 真实生图 | `pass` | 六版底图均来自内置 imagegen；程序只做排版与 QA |
| 直接标杆约束 | `pass_directionally` | 均保持深色编辑部、哑光纸件、暖纸 / 橄榄 / 芥末与低饱和冷色 |
| 25% 可比性 | `pass` | 六版身份清晰且 `SELECTED 02` 可辨 |
| 100% 状态 / 纸背层次 | `pass_visual` | 三处裁切未见文字身份丢失或结构层黏连 |
| 非蓝元素冻结 | `pass_visual` | E 的首轮偏差已定向返修；最终六版肉眼通过 |
| `scope_invariant` | `unverified` | 内置 imagegen 没有 mask / ROI 外像素锁定，不能证明逐像素只改色 |
| 主方案选择 | `pending_user_selection` | 未经用户裁决，不冻结正式色板 |
| 生产标杆 | `blocked` | 当前仍是综合色彩比较稿 |

## 禁止跳步

- 用户没有选择主方案前，不把任何一版登记为正式美术真源或设计采纳。
- 不把六张图直接切 atlas、接 Godot 或转换成 runtime 状态色。
- 若用户要求合并方案，只允许先明确“哪一版为母版、吸收哪一版的哪个颜色层级”，不得继续无边界混色。

## 用户裁决（2026-07-28）

- 用户明确选择 A「夜班石板蓝」。
- A 已登记为 A274，身份为后续同族界面风格稿的当前配色锚点。
- B–F 停止并行扩展，保留为备查与偏差边界。
- 本次选择不把 A 自动升级为正式 runtime token、生产标杆、atlas 或 Godot 资源。
