# WMW `right_dossier_page` v0.8.6 无字 clean-sprite brief

> 日期：2026-07-14
> 产物类型：`production brief delta / structure board / not production art / not atlas / not Godot runtime`
> 设计采纳：A196
> `contract_v0_8_6`：`pass`
> `brief_landing`：`conditional_pass`
> `imagegen_execution`：`ready_for_single_class_vertical_slice`（A199：橄榄绿）

## 1. 本版作用

本 brief 显式取代 v0.8.5 的动作栈几何，其余 parent / child 像素所有权、三母版、照片镂空层、无字边界、状态派生与 QA 要求继续继承：

`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-clean-sprite-brief-v0-8-5.md`

本 brief 初版不调用 imagegen、不生产 atlas、不改 Godot、不启动其它 class。A199 已解除颜色阻塞，当前只允许启动本 brief 覆盖的三母版单类纵向切片。

## 2. A196 几何修订

v0.8.5 的两条功能条并未真正共中心：次级条中心 `160`、主 CTA 中心 `158`；主 CTA 左右留白又是 `16/20px`。该几何撤销，不得继续作为 clean-sprite 输入。

| 元素 | v0.8.5 | v0.8.6 | 结果 |
| --- | --- | --- | --- |
| `mission_intel_button` | `[22,390,276,44]` | `[18,390,284,44]` | 左右各 `18px`，中心 `160` |
| `primary_enter_cta` | `[16,444,284,50]` | `[18,444,284,50]` | 左右各 `18px`，中心 `160` |
| mission child | `276x44 @ (954,420)` | `284x44 @ (950,420)` | export / hit rect 同步扩宽 |
| primary child | `284x50 @ (948,474)` | `284x50 @ (950,474)` | 仅修正父页中心 |

两条主体固定满足：`left_edge_diff=0`、`right_edge_diff=0`、`center_x_diff=0`、`width_diff=0`。高度继续保持 `44/50px`。

## 3. 可见轮廓与阴影分离

生产候选不能只报 export rect。每个 child 必须独立记录：

- `visible_body_bbox`：不含阴影的外框 / 背板主轮廓；这是双边对齐的唯一判定对象；
- `shadow_bbox`：局部纸影与 pressed 前后变化范围；只承担抬升，不参与主体宽度；
- `hit_rect`：与合同 export 同尺寸，hover / pressed / disabled 时不得移动。

首张 clean-sprite 候选必须在 200%-300% 对齐板上同时画出两种 bbox，并程序断言两条 `visible_body_bbox` 的左右边缘与中心差均为 `0`。禁止用相同 PNG 宽度、相同 export rect 或单边对齐冒充视觉双边对齐。

## 4. 主次层级

任务情报条与主 CTA 同宽后，主次差异只由以下变量承担：

- 次级：`44px` 高、安静底色、较轻边框、较浅阴影、信息型图标和较弱 hover；
- 主 CTA：`50px` 高、较强内板对比、明确纸厚、较强字重、进入箭头、抬升和 pressed 下压；
- locked 页面中任务情报仍是 `locked_context_enabled`，只有主 CTA 是 `locked_disabled`。

禁止重新加入 2-8px 宽差、偏心、单边毛边或移动 hit rect 来制造层级。

## 5. 未改变范围

- dossier `320x520 @ (932,30)`、上半部、照片槽、正文与事实条不动；
- 两个 child 的内部 `left_icon_zone / label_plate / right_action_badge` 本轮不动；
- parent hollow shell + 两个独立 child master + runtime 文字 / 数字 / 状态图标的 z 序不动；
- 所有无字、无假字、无烘焙状态语义和一类一母版规则不动；
- locked 次级文案 / 回调、warning 二次确认与任务耗时术语继续 provisional。

## 6. 本版证据与 gate

- 573：v0.8.5 错位与 v0.8.6 同宽对比、WARNING 光栅文字回填、对齐判据；
- 574：default / warning / locked 三状态实际 raster alpha glyph bbox 压力；
- 575：1280x720 组件同屏回填 / 尺度与对齐审计；2026-07-16 已明确降级为 `component_reinsert_review_board`，不得作为页面结构或功能必要性真源；
- 576：更新后的三母版 clean-sprite 结构板；
- 577：合同、文字、对齐、范围与下一阻塞 manifest。

硬 gate：

1. 三份合同版本均为 v0.8.6；
2. 两条 slot / child export 宽度均为 `284px`，父页中心均为 `160`；
3. 两个 child 绝对位置分别为 `(950,420)`、`(950,474)`；
4. 下半部槽位交叠 `0`，上半部与两个 child 内部槽位无改动；
5. 三状态 raster glyph bbox 全部位于 carrier 内；
6. 首个生产候选补跑 `visible_body_bbox` 与 `shadow_bbox` 分离 gate；
7. A199 已裁决主 CTA 常态橄榄绿；只允许本三母版纵向切片启动 imagegen，禁止扩到其它 class。

## 7. A199 颜色语义与当前入口

用户已选择橄榄绿：主 CTA default / hover / pressed 使用橄榄绿；次级任务情报保持青蓝；warning 锈红只用于风险状态层；locked_disabled 使用中性灰。颜色只归 child / 状态皮肤，parent 不整体染色，label plate 保持安静无字。

当前状态为 `ready_for_single_class_vertical_slice`，不是批量生产授权。首张候选必须依次通过：三个独立母版、无字 / 无假字、正交功能面、父子接缝、照片窗 alpha、两 child `visible_body_bbox` 同宽共线、`shadow_bbox` 独立、Python 回填、Godot 4.6.2 windowed 截图与用户视觉复审。
