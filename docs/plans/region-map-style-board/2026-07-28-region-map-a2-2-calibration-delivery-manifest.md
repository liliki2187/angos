# 区域地图 A2.2 色彩与纸张校准交付清单

## 决策条

- **结论**：A2.2 已完成；地图不再由低饱和浅灰蓝主导，主纸也从原 A2 偏暗与 A2.1 过白之间回到接近世界地图 A 的暖灰白区间。
- **影响**：A2 的本地岩盘结构与事件链保持，跨屏综合色域更接近世界地图 A；当前仍是待用户确认的风格参考。
- **下一步**：用户判断 A2.2 是否解决灰土与纸暗；未确认前不替换正式母版。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = regional_map_a2_2_color_paper_calibration`
- `status = pending_user_review`
- `production_candidate = false`
- `runtime_implemented = false`
- `scope_invariant = visually_close_but_pixel_unverified`

## 产物

- A2.1 中间稿：`image_gen/2026-07-28/region-map-map-variants-v1/07-a2-1-color-paper-calibrated.png`
- A2.2 当前稿：`image_gen/2026-07-28/region-map-map-variants-v1/09-a2-2-paper-balanced.png`
- 世界 A / 原 A2 / A2.2 对照：`image_gen/2026-07-28/region-map-map-variants-v1/10-world-a-region-a2-a2-2-comparison.png`
- A2.2 25%：`image_gen/2026-07-28/region-map-map-variants-v1/11-a2-2-paper-balanced-25pct.png`
- 世界 A / A2.2 25%：`image_gen/2026-07-28/region-map-map-variants-v1/12-world-a-region-a2-2-25pct.png`

`image_gen/` 被 `.gitignore` 忽略；图片已落入工作区，但不进入 Git 追踪。

## 角色意见

### UX 老哥

- `P0 = 0`；`P1` 为跨屏层级断层。
- 地图建议饱和 `38–46%`，禁止全局压暗与玩具青；`R-21`、线路和河道保持清楚的明度差。
- 纸张必须分主纸、次卡、回执 / 背板三档，禁止所有纸同亮或纯白软件面板。
- 25% 下阅读链应为地图 → `R-21 / 线路` → 右卷宗 / CTA。

### UI Designer

- 主纸只包括地图外框、选中票据与右 `CASE FILE`；未选票据和小媒介属于次卡；底部票据和背板维持更深层。
- 地图色彩以冷青主地形、夜板岩蓝和低饱和灰蓝构成，锈红只做极小节点信号。
- 仅保留地图右下“人扒天线”的破纸便签，不新增笑点。

## 近似取样

以下为对照 ROI 的近似 HSV 平均，不是正式 palette token：

| 对象 | 饱和度 | 明度 |
| --- | ---: | ---: |
| 世界地图 A 地图主体 | `57.5%` | `27.1%` |
| 原区域 A2 地图主体 | `28.7%` | `43.2%` |
| 区域 A2.2 地图主体 | `44.4%` | `45.2%` |
| 世界地图 A 主案卷纸 | `15.8%` | `76.2%` |
| 原区域 A2 主案卷纸 | `16.5%` | `73.5%` |
| A2.1 主案卷纸 | `12.2%` | `87.8%` |
| 区域 A2.2 主案卷纸 | `14.7%` | `79.5%` |

## Gate

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 真实生图 | `pass` | A2.1 与 A2.2 均来自内置 `imagegen` |
| A2 结构保留 | `pass_visual` | 地图拓扑、事件节点与 `R-21` 选中链保持 |
| 灰土修正 | `pass_visual` | 地图饱和度从约 `28.7%` 提至约 `44.4%` |
| 地图明度目标 | `watch_item` | 最终近似明度 `45.2%`，高于 UX 探针建议；25% 可读但仍需用户主观判断 |
| 纸张偏暗修正 | `pass_visual` | 主案卷纸从约 `73.5%` 提至约 `79.5%` |
| 防纯白纸 | `pass_after_revision` | A2.1 约 `87.8%` 过白；A2.2 已回调 |
| 纸张角色分层 | `directional_pass` | 主纸 / 次卡 / 回执背板肉眼可分；未做角色级 mask/token 校验 |
| 25% 阅读链 | `pass_visual` | 地图、选中链、右案卷和 CTA 层级仍成立 |
| 外层冻结 | `visual_close` | 内置 imagegen 无 mask，不能证明 ROI 外逐像素不变 |
| 生产候选 | `blocked` | 未经用户确认且没有资产合同、状态矩阵或 runtime 验收 |

## 原始生成输出

- A2.1：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_JhvXd5YmwonfNQmMFVStRfEo.png`
- A2.2：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_2TDpOUyUsmxY74ldXt2y2qbd.png`
