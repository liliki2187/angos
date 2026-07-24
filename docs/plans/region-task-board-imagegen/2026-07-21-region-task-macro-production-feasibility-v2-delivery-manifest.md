# 区域任务短签宏观组合件 v2 生产可行性交付清单

> 日期：2026-07-21  
> 阶段：`pin_label_connection_p1_reopened`  
> 范围：美术资源与精确尺寸预检，不改生产 Godot、正式合同或正式 manifest

> 用户复核更新：原 UI / UX GO 已撤回。用户指出图钉与名称横条在 v2 中实际分离，没有继承效果稿的压合连接。当前主审图保留为问题证据，不得作为冻结依据。

## 主审图

- `design/art-direction/region-task-board/2026-07-21-region-task-macro-production-feasibility-v2.png`
- 真实 1×读回：`docs/screenshots/2026-07-21-region-task-pin-runtime-preflight-v2/02-native-1x-truth-strip-v2.png`

主审图同时覆盖：

1. 四类任务 default / selected 的真实 1×中文回填。
2. selected pin、左右 label、类型图标与动态文字的宏观组合件拆分。
3. 最长隐藏任务标题的右挂 / 左挂。
4. `temp selected + urgent` 的类型 / 流程状态组合。

## 美术源与透明候选

- 生图提示：`design/art-direction/region-task-board/2026-07-21-region-task-macro-asset-sources-v2-prompts.md`
- 透明源目录：`design/art-direction/region-task-board/runtime-preflight-v2/`
- 独立 frame：`design/art-direction/region-task-board/runtime-preflight-v2/frames/`
- 预检元数据：`design/art-direction/region-task-board/runtime-preflight-v2/runtime-preflight-assets-v2.json`
- 精确合成脚本：`scripts/art/build_region_task_macro_preflight_v2.py`

候选 atlas：

- `rt-task-pin-default-macro-v2-atlas-3x.png`
- `rt-task-pin-selected-macro-v2-atlas-3x.png`
- `rt-task-label-right-macro-v2-atlas-2x.png`
- `rt-task-label-left-macro-v2-atlas-2x.png`
- `rt-task-state-badges-macro-v2-atlas-3x.png`
- `rt-task-pin-kind-icons-v4-candidate-atlas-3x.png`

## 资产所有权

美术组合件：

- default pin：前壳、内框、连接肩、类型尖端。
- selected pin：选中纸背、前壳、连接肩、类型尖端。
- right / left label：纸面、切角、远端类型帽。
- assigned / urgent / locked：纸签底与状态图形。

继续动态：

- 任务类型图标 atlas。
- 标题、meta 与省略。
- 外部投影、锚点、dense、cluster、clamp。

## 合同状态

保持：

- hit `72×80`
- pin `64×80`
- visual offset `[4,0]`
- anchor `[36,76]`
- label `200×72`
- label anchors `[78,4] / [-208,4]`

待用户确认后再升正式合同：

- 文字安全区 `[14,12,158,48]`
- title `[14,12,158,25]`
- meta `[14,39,158,20]`
- 状态小纸签候选尺寸 `24×24`
- 程序派生 selected / 状态签改为美术资源所有权

## 复核结论

- UI Designer：`P0=0 / P1=0 / P2=1 / GO`
- UX 老哥：`P0=0 / P1=0 / P2=1 / GO`
- 共同 P2：低饱和类型的 selected 外围增量或 meta 灰度在复杂地图上可能略弱；正式运行接入后只检查明度 / 墨色，不增加新描边、光环或第二状态色。

## 已重开的 P1

- 右挂 pin / label 约有 10px 暗缝，左挂约有 12px 暗缝。
- 生产 Godot 的 label z-order 高于 pin，与“图钉压住横条”的目标相反。
- 下一轮只修 overlap、z-order 与接合肩；其余已通过项保持。

## 当前需要用户判断

1. 当前宏观组合件是否终于保留了效果稿的小纸沿、压合与纸层感。
2. 短签两行文字与 `200×72` 框体是否匹配。
3. selected 背板是否足够明确但不过厚。
4. 左右短签与 urgent 小纸签是否可以冻结进入正式接入。

## 尚未执行

- 未修改 `WeeklyRunRegionEventPin.gd`。
- 未替换 Godot 正式资源或 manifest。
- 未修改 `event_pin_contract.json`。
- 未重跑 Godot 状态矩阵、密集避让、cluster、clamp 或 hover → selected 动效；这些留在用户确认后的正式接入阶段。
