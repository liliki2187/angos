# 世界地图风格板 v4 蓝色层级试改交付清单

## 决策条

- **结论**：蓝色扎眼问题获得方向性修正，当前为用户审阅候选。
- **影响**：大面积钴蓝已经退成墨蓝与低饱和石板蓝，暖纸、橄榄和芥末重新成为品牌记忆；`SELECTED 02` 仍由文字、编号、圈选和少量状态蓝共同识别。
- **下一步**：由用户判断这一版是否恰当，尤其确认状态蓝是否压得过低。用户确认前不升格生产标杆。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = color_only_blue_hierarchy_revision`
- `status = blue_hierarchy_visual_candidate_pending_user_review`
- `production_candidate = false`
- `runtime_implemented = false`
- `scope_invariant = unverified`

本产物只验证蓝色面积、饱和度与信息层级，不验证 runtime 状态矩阵、正式色彩 token、atlas 或严格局部像素替换。

## 用户审阅入口

- 完整 v4：`image_gen/2026-07-28/world-map-interface-style-board-v4-blue-hierarchy/01-world-map-interface-style-board-v4-blue-hierarchy.png`
- 25% 缩略：`image_gen/2026-07-28/world-map-interface-style-board-v4-blue-hierarchy/02-world-map-interface-style-board-v4-25pct.png`
- v3 / v4 缩略对照：`image_gen/2026-07-28/world-map-interface-style-board-v4-blue-hierarchy/03-world-map-interface-style-board-v3-v4-color-comparison.png`
- 说明：`image_gen/` 被 `.gitignore` 忽略，以上图片已落工作区但未进入 Git 追踪。

## 输入与生成链

- 编辑目标：`image_gen/2026-07-28/world-map-interface-style-board-v3-component-language/01-world-map-interface-style-board-v3-component-language.png`
- 直接标杆：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- 生图方式：Codex 内置 `imagegen`，真实位图编辑。
- 原始生成输出：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_pbzkMzmFJjcrcmP7J7tQRHsR.png`
- 最终尺寸：`1672×941`，RGB。
- 完整 v4 SHA-256：`4ce8d9c283de33bd82e8a3fa6408662ffce3d553ae56bf4ef0e3f0fba0edb5fc`
- 25% 缩略 SHA-256：`d93c26b087baaf4e09bdecad98b4ee4fa259107e29a66c45bb457368e3790be`
- 对照图 SHA-256：`221bead836322fe4a5654dcd7db1073ad6d291c7bd85b59c8fa2255c6caa4341`
- 程序只用于缩放、对照拼版和色彩面积粗测，没有替代真实生图。

## 颜色 brief

| 层级 | 视觉职责 | 本轮目标 |
| --- | --- | --- |
| B0 深海军蓝 | 工作台负空间、地图底 | 维持大面积、低明度，不提亮 |
| B1 结构蓝 | 右侧文件夹背板、selected 卡背层、右下文件夹、非关键连接件 | 低饱和石板蓝 / 旧牛仔蓝，约 `#263851`、`#40566A`、`#465C6A` |
| B2 状态蓝 | `SELECTED`、`02`、圈选节点和必要连接节点 | 少量、清晰但不电光，约 `#334E77` 到 `#3E6790` |

冻结不变：

- 全部布局、构图、组件数量、轮廓、低多边形颗粒、文字、尺寸、位置和遮挡。
- 纸张颜色、纸纹、边缘、夹子、回形针、胶带和阴影。
- 地图拓扑、大陆形状、圈选位置与连接线几何。
- 青色事件光束、橙色 `?!`、芥末便签、橄榄标签、暖纸、灰紫锁定卡和黑色墨线。
- 塔楼、建筑、站台、UFO、符号条与 `DAY 1` 的对象画法。

## UX 老哥结论

UX 老哥判定 `P0=0，P1=2，P2=1`：

- P1：状态色泛滥。高能钴蓝同时承担 selected 与非状态结构底衬，削弱状态色独占性。
- P1：蓝色走廊贯穿左、中、右，面积与强度共同抢走事件图和 `NEWS LEAD` 焦点。
- P2：大面积高纯度蓝使纸件滑向科技塑料与控制台感。
- 推荐保守方案 A：降低右侧背板、selected 多层卡背和非关键连接件；保留 `SELECTED + 02 + 圈选节点` 的少量状态蓝。
- 25% 标准：先读中央地图、塔楼事件图和右侧新闻纸，5 秒内仍能指出 `SELECTED 02`。
- 100% 标准：非蓝元素保持原样，结构蓝不与背景黏成一片，换色边缘无污染。

## UI Designer 等价 brief

UI Designer 子 agent 在读取阶段异常卡住并被中断。父级读取 `skills/ui-designer/SKILL.md` 与必需 system prompt 后执行等价流程：

- 元素表只包含 B0 背景、B1 结构背板和 B2 状态锚点，没有新增任何 UI 元素。
- 桌面 16:9 布局与 v3 完全沿用，不出新 wireframe。
- 色彩注意力顺序：暖纸 / 地图事件图 / `NEWS LEAD` → `SELECTED 02` → B1 文件夹结构 → B0 负空间。
- 无新增资产需求；本轮只是现有蓝色职责重分配。
- 所有文字安全区与现有组件安全区保持不变。

## Gate 结果

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 直接标杆对照 | `directional_pass` | 蓝色从纯钴蓝退回标杆式墨蓝、石板蓝与旧牛仔蓝 |
| 25% 焦点顺序 | `pass_visual` | 中央地图、塔楼事件图和右侧新闻纸先于背板被读取 |
| `SELECTED 02` 识别 | `pass_visual` | 文字、编号、圈选和连接关系仍提供双重以上编码 |
| 非蓝色冻结 | `pass_visual` | 青光、橙黄、橄榄、暖纸和灰紫在肉眼对照中保持原职责 |
| 高能蓝面积 | `very_low_pending_user_decision` | 粗测阈值下由 v3 的约 `4.06%` 降至 v4 的约 `0.05%`；阈值只用于相对比较，提示状态蓝可能压得偏低 |
| `scope_invariant` | `unverified` | 内置 imagegen 没有 mask / ROI 外像素锁定，不能证明严格 color-only 像素替换 |
| UI 双 agent | `exception_recorded` | UX 老哥完成；UI Designer 卡住，父级执行等价 brief |
| 生产标杆 | `blocked` | 用户尚未审阅，且正式 B2 状态色面积尚未裁决 |

## 禁止跳步

- 用户确认前不更新正式美术真源或设计采纳记录。
- 不切 atlas、不接 Godot、不修改正式 UI 合同或 runtime 状态色。
- 若用户认为状态蓝过低，下一轮只允许针对 B2 状态锚点做一次小范围增强，不得恢复大面积钴蓝。
