# WMW 右 dossier 候选 A 复审记录（v0.9.0）

> **产物类型**：单 class 生产候选复审材料，不是冻结生产资源。
> **当前状态**：程序构造、Python 回填、Godot 4.6.2 windowed 截图与双 agent 复核均已完成；等待用户视觉裁决。
> **设计采纳**：A199，主 CTA 常态采用低饱和橄榄绿；任务情报入口保持青蓝；锈红与中性灰只服务风险 / 禁用状态。

## 1. 本轮范围

本轮只生产以下三类的首张纵向切片候选：

- `right_dossier_page`：中性 parent hollow shell；
- `right_mission_intel_button`：青蓝 secondary child；
- `right_action_lane`：橄榄绿 primary child。

未生产其它 class，未修改 `design/ui-contracts/world-map/` 中任何 frozen 字段。文字、数字、状态语义图标和后续 hover / pressed / locked 反馈仍归运行时层。

## 2. 真实生图与构造

- 579：parent 真实 imagegen 源；
- 580：mission secondary 真实 imagegen 源；
- 581：primary olive 真实 imagegen 源；
- 582：无字三母版与几何 / alpha 证据板；
- 583 / 584：Python 运行时回填与 QA；
- 585 / 586：Godot 4.6.2 windowed OpenGL3 运行截图与 QA；
- 587：benchmark / Godot runtime / child close-up 复审板；
- 588：Delivery Manifest。

三个生图源先去除 `#FF00FF` 色键，再按合同做分块几何构造；没有整体拉伸去凑合同。parent 照片窗被构造为精确 alpha 洞，照片在下、parent 壳在上、两个 child 独立叠加，文字与共享 PNG 图标最后由运行时绘制。

## 3. 程序证据

| 检查项 | 结果 | 可核验依据 |
| --- | --- | --- |
| export geometry | PASS | parent `640x1040`；mission `568x88`；primary `568x100` |
| parent photo alpha | PASS | `194304/194304` 透明像素 |
| photo bezel continuity | PASS | alpha 结构破损 `0`；只把 `alpha <= 8` 视为洞，抗锯齿半透明不误判 |
| chroma residue | PASS | 三母版均为 `0` |
| A196 可见主体对齐 | PASS | mission `[0,0,568,86]`；primary `[0,0,568,98]`；左右 / 宽度差 `0/0/0` |
| shadow 独立量测 | PASS | mission `[5,86,567,88]`；primary `[6,98,567,100]` |
| runtime text bbox | PASS | 实际 raster alpha bbox `8/8` 在槽内 |
| shared runtime icons | PASS | Python 与 Godot 共用 globe / document / arrow / check PNG，不再使用 Unicode 临时替代 |
| Godot UI capture | PASS | 4.6.2-stable、windowed OpenGL3；585/586 颜色采样 `3789/3856`；非黑采样均 `32400` |

## 4. UX 老哥复核原文

> 结论：**可进入用户视觉复审，不要求先返工。** 本轮判定为 **P0=0、P1=0、P2=3**。A196、A199 均有真实运行时证据支撑；但候选仍不应冻结，hover / pressed / locked 等动态状态尚未验收。
>
> A196 通过：两个合同槽可见主体同为 284px、中心均为 `x=160`，588 实测 `left/right/width diff = 0/0/0`，阴影单独量测。因此不是“合同框对齐但成品不齐”的假通过。
>
> A199 通过：次级入口稳定为青蓝，主 CTA 为低饱和橄榄绿，`高危`继续使用锈红；父 dossier 没有被状态色污染。青蓝饱和度略高，但尚未推翻高度、位置和动作语义形成的主次关系，适合交给用户最终裁决。
>
> P2-1 是 Python / Godot 图标 token 不一致；本项已在复核后修复，当前 583-587 与 588 均使用同一组 PNG 配料。
>
> P2-2 是“推荐12”缺少正式计量单位，可能与“12项”短暂串读。P2-3 是双端圆环可能被理解为多个小按钮；动态实现必须以整条为唯一 hit rect，并统一 hover / pressed / disabled 反馈。

UX 最终意见：静态默认态可以交用户复审；用户观感通过且动态状态补证后，再讨论生产冻结。

## 5. UI Designer 复核原文

> 结论：可直接进入用户视觉裁决。视觉侧未发现需要预先返工的 P0/P1；A196/A199 成立，未新增视觉 P2。
>
> 582/585/587 保留了 clean low-poly weekly 的核心语言：深海军蓝与暖灰米纸形成主对比；大块低多边形明暗面进入照片、纸面和动作条；橄榄绿、青蓝、锈红维持语义分工；纸边、套页、裁角、背页和克制阴影形成编辑部档案物件感，没有滑向旧报纸、军事终端或扁平 SaaS 面板。
>
> parent / photo / child 图层完整；照片窗 alpha、父壳、两个独立 child 与运行时文字图标的顺序成立。主纸面占主体，锈红只属于高危与警戒背页；两条动作栈同宽共中心，primary 约高 14%，橄榄绿只属于底部推进性动作。
>
> 父壳在运行时稍偏亮，但仍在标杆允许范围，不上升为返工项；可由用户直接判断是否偏好更亮、更干净的 dossier。

UI Designer 最终意见：候选 A 已形成完整、可解释且接近标杆的视觉系统，无需在用户裁决前预返工。

## 6. 当前裁决点

请基于 585 与 587 选择：

1. **采纳候选 A 方向**：进入 default / hover / pressed / warning / locked 状态派生与动态验收；
2. **局部微调**：只调整纸张亮度、青蓝 / 橄榄色权重或运行时文案，不重开三母版结构；
3. **不采纳**：候选保持归档，不启动其它 class。

无论选择哪一项，`推荐12` 的正式单位与 locked / warning 行为仍需在动态状态轮明确；当前 588 的结论严格保持 `evidence_ready_user_visual_review_pending`。
