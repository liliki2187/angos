# 区域任务短签选中背板拆图交付清单

> 日期：2026-07-21  
> 阶段：`split_strategy_rejected`  
> 范围：拆分与落地预检，不改生产 Godot、正式合同或 manifest

> 复核结论：本清单中的七层微拆被用户反馈与后续技术核查共同否决，只保留为失败证据。问题包括：微型色片无法保留效果稿的纸沿与压合关系、文字安全区超出真实纸面并碰撞端帽、左右翻签行为不一致，以及多个状态小构件仍由 Godot 程序绘制。不得按本清单接入生产。

## 主审图

- `design/art-direction/region-task-board/2026-07-21-region-task-pin-layer-exploded-sheet-v1.png`
- 对话截图副本：`docs/screenshots/2026-07-21-region-task-pin-runtime-preflight/03-layer-exploded-sheet.png`

主审图展示真实透明资源的合成关系，不是概念示意：

1. `selected_backplate`：选中时才显示的美术背板，四类预着色 frame，共用相同 alpha 轮廓。
2. `neutral_pin_shell`：中性图钉主体，默认状态复用。
3. `pin_type_accent`：只覆盖图钉下方尖端的类型色件。
4. `kind_icon`：复用现有四类任务图标 atlas。
5. `neutral_label_base`：中性短签底纸。
6. `label_type_accent`：只覆盖短签右端帽的类型色件。
7. `dynamic_text`：标题与 meta 保持 Godot 动态文字，不烘进 PNG。

## 透明资源

- Atlas：
  - `design/art-direction/region-task-board/runtime-preflight-v1/rt-task-pin-selected-backplates-v1-atlas-3x.png`
  - `design/art-direction/region-task-board/runtime-preflight-v1/rt-task-pin-type-accents-v1-atlas-3x.png`
  - `design/art-direction/region-task-board/runtime-preflight-v1/rt-task-label-type-accents-v1-atlas-2x.png`
- 独立 frame：`design/art-direction/region-task-board/runtime-preflight-v1/frames/`
- 预检元数据：`design/art-direction/region-task-board/runtime-preflight-v1/runtime-preflight-assets-v1.json`

## 本轮需要用户判断

1. 七层拆分是否足够直观、便于后续维护；是否有层需要合并或继续拆开。
2. `selected_backplate` 相对 64×80 图钉的 72×80 体量是否过大或过厚。
3. 类型色只进入背板、图钉尖端和短签右端帽，是否符合期望。

## 尚未执行

- 未替换 `WeeklyRunRegionEventPin.gd` 的运行时派生绘制。
- 未更新 `event_pin_contract.json` 与正式资源 manifest。
- 未改变尺寸、alpha、锚点、文字层、密集避让、cluster 或 clamp 合同。
- Godot 4.6.3 本轮在最小退出脚本也触发 `signal 11`，因此正式引擎截图留到环境恢复后；当前主审材料由已导出的真实透明层按合同尺寸确定性合成。
