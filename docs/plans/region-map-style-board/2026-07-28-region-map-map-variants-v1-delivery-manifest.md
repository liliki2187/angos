# 区域地图中央地图变量 v1 交付清单

## 决策条

- **结论**：用户已从 3 个中央地图候选中正式选择 A2「冷青岩盘」作为区域地图当前视觉方向。
- **影响**：后续区域地图的中央地图以偏蓝低饱和冷青灰岩盘、墨蓝水域和石板蓝选中链为基准；A1 / A3 只保留为氛围与误读边界参考。
- **下一步**：等待用户授权后，以 A2 为地图方向并严格套入区域地图黑白功能稿生成完整有字风格稿；本轮不进入生产资产。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = regional_map_internal_colorway_exploration_v1`
- `status = user_selected_a2_cool_teal_terrain`
- `production_candidate = false`
- `runtime_implemented = false`
- `scope_invariant = visually_close_but_pixel_unverified`

## 产物

- `01-a1-night-blue-tidal.png`：夜蓝潮汐层。
- `02-a2-cool-teal-terrain.png`：冷青岩盘。
- `03-a3-lead-blue-clipping.png`：铅蓝剪报图。
- `04-region-map-variants-comparison.png`：地图局部 + 整屏综合色温对照。
- `05-region-map-variants-25pct.png`：三版 25% 整屏对照。

目录：`image_gen/2026-07-28/region-map-map-variants-v1/`

`image_gen/` 被 `.gitignore` 忽略；图片已落入工作区，但不进入 Git 追踪。

## 角色意见

### UI Designer

- `A1` 最稳定地继承世界地图 A 的夜班蓝；主要风险是暗部吞掉普通节点。
- `A2` 地貌识别最强；主要风险是冷青偏绿后滑向军图。
- `A3` 编辑部剪报拟物最强；主要风险是浅陆地与道路过多后像旅行地图。
- 生成前推荐：`A1 > A2 > A3`。

### UX 老哥

- 25% 下 `A1 / A2` 可能收敛成相似冷暗地图，`A3` 差异最大但最易跑题。
- `A1` 必须禁止发光、扫描感潮汐圈，并保护 `R-21` 链对比。
- `A2` 的节点 / 地图可读性最稳，但必须禁止准星、荧光边和等距网格。
- `A3` 的水陆与选中链最易分辨，但道路必须降权，剪报不得压过节点。
- 生成前推荐：`A2 > A1 > A3`。

## 生成后父级复核

- `A1`：综合色温最接近世界地图 A，夜班 / 潮湿氛围最完整；地图整体最暗，但节点与 `R-21` 链仍可辨。
- `A2`：地图内部最清醒、冷青层次最丰富，25% 下中央地图主语最强；冷青已保持偏蓝，未读成军事地图。
- `A3`：综合色温最中性，水陆分界最清楚，剪报笑点明确；也是最接近“文档地图 / 旅行图”误读边界的一版。

## 用户裁决

- 2026-07-28：用户明确回复“那就 A2 吧。”
- 已登记为设计采纳条目 `A275`。
- 选择的是区域地图视觉参考方向，不等于正式 palette token、无字资产母版、atlas 或 runtime 冻结。

## Gate

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 真实生图 | `pass` | 3 张候选均来自内置 `imagegen` |
| 同母版独立变量 | `pass` | 3 版均以区域地图 v1 为编辑目标，未串联生成 |
| 中央地图偏黄修正 | `pass_visual` | 3 版地图主体均由夜蓝 / 冷青灰 / 铅蓝替代卡其橄榄 |
| 25% 地图主语 | `pass_visual` | 3 版均仍先读为本地事件地图 |
| 事件链延续 | `pass_visual` | 左 `R-21` → 地图 `R-21` 选中链均保留 |
| 非旅行 / 非世界地图 | `pass_with_watch_item` | `A3` 浅色与交通骨架最接近误读边界 |
| 非军事 / 非雷达 | `pass_visual` | 无准星、扫描线、发光 HUD；潮汐圈仍为纸面等值圈 |
| 低多边形颗粒 | `directional_pass` | 大块面成立，但三版仍属于风格参考，不是可拆地图资产 |
| 外层 UI 冻结 | `visual_close` | 肉眼保持同一母版；内置 imagegen 无 mask，不能证明 ROI 外逐像素不变 |
| 生产候选 | `blocked` | 未经用户选择，且没有资产合同、状态矩阵或 runtime 验收 |

## 反向读法

- `A1` 不能被读成雷达：没有荧光、扫描线、准星；但后续若强化潮汐圈必须继续防守。
- `A2` 不能被读成军事图：节点仍是纸面事件签，冷青只服务地貌大面。
- `A3` 不能被读成旅行图：没有目的地串联、箭头和观光照片；但浅色面积与道路权重不宜继续增加。

## 原始生成输出

- `A1`：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_FPLKrZkvdUZixIedrOszHPjk.png`
- `A2`：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_ZGz8m02qpVpaXrn82zuBhiz5.png`
- `A3`：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_AXIkWxX8l0hX671Vk6mhoY5Q.png`
