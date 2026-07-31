# 区域地图 A2.4 趣味密度校准交付清单

## 决策条

- **结论**：A2.4 已完成并通过当前视觉 Gate；相较 A2.2，趣味从一个孤立黄便签扩展为三层同源异常证据，25% 下仍不抢主任务链。
- **影响**：区域地图与世界地图 A 的趣味剂量已经明显接近，但区域地图继续保持“本地外勤案卷台”的严肃工作原型，没有复制世界地图的贴纸构图。
- **下一步**：等待用户判断是否达到“和世界地图差不多”的趣味度。当前尺寸和像素冻结均未通过，不得升格为生产候选。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = regional_map_a2_4_humor_linked`
- `status = pending_user_review`
- `production_candidate = false`
- `runtime_implemented = false`
- `scope_invariant = failed_exact_size_and_pixel_unverified`

## 产物

- A2.2 编辑母版：`image_gen/2026-07-28/region-map-map-variants-v1/09-a2-2-paper-balanced.png`
- A2.3 诊断稿：`image_gen/2026-07-28/region-map-map-variants-v1/13-a2-3-humor-balanced.png`
- A2.3 与世界 A 并排：`image_gen/2026-07-28/region-map-map-variants-v1/14-world-a-region-a2-3-humor-comparison.png`
- A2.3 25%：`image_gen/2026-07-28/region-map-map-variants-v1/15-world-a-region-a2-3-25pct.png`
- A2.4 当前候选：`image_gen/2026-07-28/region-map-map-variants-v1/17-a2-4-humor-linked.png`
- 世界 A / A2.4 整屏并排：`image_gen/2026-07-28/region-map-map-variants-v1/18-world-a-region-a2-4-humor-comparison.png`
- 世界 A / A2.4 25%：`image_gen/2026-07-28/region-map-map-variants-v1/19-world-a-region-a2-4-25pct.png`
- A2.2 / A2.4 三锚点裁切：`image_gen/2026-07-28/region-map-map-variants-v1/20-a2-2-a2-4-humor-anchors.png`

`image_gen/` 被 `.gitignore` 忽略；图片已落入工作区，但不进入 Git 追踪。

## 三个趣味锚点

| 层级 | 位置 | 作用 |
| --- | --- | --- |
| 主笑点 | 中央地图右下黄便签 | 一本正经的测量行为与鱼形灯塔投影形成“方向错了”的冷面反差 |
| 隐藏证据 | 左 `R-21` 缩略图 + 右案卷灯塔照片 | 同一条锈红圈高空鱼跨栏重复，说明这不是装饰，而是同一案件证据 |
| 制度余味 | 底部交通票据 | 路线终点变成两道水波，像行政系统平静记录了“抵达错误地点” |

## 双 Agent 意见

### UX 老哥

- `P0 = 0`，`P1 = 0`。
- A2.2 只有一个明显趣味锚点，世界地图 A 约有三层；区域地图可补三处二读异常，但不得破坏 `R-21` 与 CTA 的首读。
- 建议锚点为黄便签主笑点、案卷照片隐蔽证据和交通票据制度余味。
- 5 秒测试：先读出 `R-21` 主链与 CTA，再能指出至少两处克制怪异。

### UI Designer

- 三处锚点应共同讲述“方向错了 → 高度错了 → 目的地也错了”，而不是三张无关贴纸。
- 黄便签使用手绘主笑点；案卷照片使用粗颗粒低多边形证据；交通票据使用机构印刷式收尾。
- 冻结 A2.2 的布局、颜色、纸张、文字、地图和功能链，只开放紧贴对象的局部区域。

## Gate

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 真实生图 | `pass` | A2.3、A2.4 均来自内置 `imagegen` |
| 三处趣味锚点 | `pass_visual` | 主笑点、隐蔽证据和制度余味均可辨认 |
| 同一案件证据链 | `pass_visual` | 锈红圈高空鱼在已选缩略图与右案卷照片中重复 |
| 25% 首读 | `pass_visual` | 地图、`R-21`、案卷与 CTA 仍先于小笑点被读到 |
| 与世界 A 趣味剂量 | `conditional_pass` | 差距明显缩小；最终“是否同量级”交用户主观裁决 |
| 防贴纸轰炸 | `pass_visual` | 没有新增彩色徽章、旅行纪念品、表情或大面积状态色 |
| 对象—画法合同 | `pass_visual` | 便签偏手绘、证据偏粗低多边形、票据偏机构印刷 |
| 精确尺寸冻结 | `fail` | A2.2 为 `1672×941`；A2.3 为 `1662×946`；A2.4 为 `1663×946` |
| 区外逐像素冻结 | `unverified` | 无 mask 编辑，不能证明未开放区域逐像素不变 |
| 生产候选 | `blocked` | 待用户确认，且尺寸 / mask / 资产合同 / runtime 均未通过 |

## 原始生图输出

- A2.3：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_jf75f9VaO3v6jv4QT8KoKegY.png`
- A2.4：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_7sHJpUlGdkuAHOnAoC7vEH9M.png`

## 用户复核后的状态修订（2026-07-29）

- 用户指出左侧四张任务配图不够抽象概括：放在标杆式多边形背景中尚可，单独放在暖纸票据上会明显读成写实的低多边形建筑模型。
- 上表“对象—画法合同 `pass_visual`”自此撤回，修订为 `fail_component_illustration`；A2.4 整体状态降为 `direction_retained_component_illustration_rework_required`。
- 趣味证据链、综合色盘、地图、纸张和功能层级继续保留；下一轮只开放四张任务配图 ROI。
- 详细根因与转换合同见 `docs/plans/region-map-style-board/2026-07-29-region-map-a2-4-micro-diorama-realism-loop-log.md`。

## 世界地图 A 并排后：R-21 内容纵切片

- 用户进一步指出，区域页即使配图颗粒度接近后，整屏仍比世界地图 A 更严肃、更无趣。
- 双 Agent 复核将问题定位为：趣味只集中在边角，左卡、地图和案卷没有组成持续证据链；右案卷三块同构空表格又把内容高潮压成待填写模板。
- 本轮不再增加泛贴纸，只为 R-21 构建“左卡目击 → 地图定位 → 右案卷复核”的单案纵切片。

### 新增产物

- 真实生图证据正文：`image_gen/2026-07-29/region-map-r21-vertical-slice-v1/01-r21-evidence-body-imagegen.png`
- R-21 整屏纵切片：`image_gen/2026-07-29/region-map-r21-vertical-slice-v1/02-region-map-a2-r21-evidence-chain-preview.png`
- 世界 A / R-21 纵切片并排：`image_gen/2026-07-29/region-map-r21-vertical-slice-v1/03-world-a-region-r21-side-by-side.png`
- 世界 A / R-21 纵切片 `25%`：`image_gen/2026-07-29/region-map-r21-vertical-slice-v1/04-world-a-region-r21-side-by-side-25pct.png`

### 工具与拼版边界

- 核心证据正文由内置 `imagegen` 真实生成；提示词要求继承世界地图 A 的夜班石板蓝、暖白纸、橄榄与克制锈红，并将“鱼游进灯塔光束”做成严肃调查与荒谬对象的冷面反差。
- 程序只负责从生图素材裁切摘要、两张证据票条和关系图，回填到既有案卷槽位；同时保护三栏、标题、状态、地图拓扑、任务坐标和底部功能区。
- 当前回填是视觉风格稿，不声明已进入 Godot、已冻结热区或已完成生产资产切分。

| 新增 Gate | 结果 | 说明 |
| --- | --- | --- |
| 真实生图 | `pass` | 证据正文来自内置 `imagegen` |
| R-21 三段证据链 | `pass_visual` | 左卡复核圈、地图位置层和右案卷内容形成同源关系 |
| 右案卷内容高潮 | `pass_visual` | 三块空表单被摘要、票条和关系图替代 |
| 25% 主链 | `pass_visual` | `R-21`、地图节点和案卷仍先于二读笑点 |
| 防旅游 / 防贴纸轰炸 | `pass_visual` | 未新增旅行物件、纪念章集合或无关道具 |
| 全屏趣味分布 | `partial` | 仅关闭 R-21；其余三案仍待分配独立异常节奏 |
| 用户裁决 | `pending` | 等待用户判断本轮趣味剂量是否进入目标区间 |
| 生产候选 | `blocked` | 未完成全案扩展、资产合同和 runtime 落地 |
