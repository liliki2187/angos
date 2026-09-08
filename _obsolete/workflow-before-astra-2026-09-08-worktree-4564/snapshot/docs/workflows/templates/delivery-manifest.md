# Delivery Manifest

## 决策条 / Decision Strip

- **结论**：通过 / 部分通过 / 不通过 / 需要你裁决。
- **影响**：这次交付能证明什么、不能证明什么，会挡住什么。
- **下一步**：下一轮具体做什么。

## 详情 / Human Brief

- **一句话结论**：这次交付能证明什么；不能证明什么；当前是继续、降级、返工还是需要裁决。
- **我实际做了什么**：
- **现在卡在哪里**：无阻断 / 产物类型不足 / 阶段跳转过早 / 验收对象不一致 / 缺截图 / 缺复审 / 其它。
- **为什么不能跳过**：
- **下一步怎么验证**：
- **本轮不要做**：

> 第一屏只保留三行决策条；这 6 行是第二层解释。术语最多放括号里，完整标签、gate 和证据路径放到下面术语版。

## 术语版 / Manifest

- **交付对象**：
- **产物类型**：structure_wireframe / problem_overlay / interaction_fix_sketch / safe_zone_capacity_validation / logic_smoke / visual_style_reference / color_locked_style_draft / no_text_style_draft / filled_state_text_mock / no_text_asset_master / runtime_skeleton / runtime_state_preview / production_candidate
- **风险等级**：
- **它能证明**：
- **它不能证明**：
- **对照真源 / 标杆**：
- **截图 / 文件路径**：
- **几何 / 正交检查**：未触发 / 自动触发-已裁切核心组件 / 自动触发-已画水平垂直参考线 / 未通过 / 未验证不得宣称通过
- **几何触发原因**：风格稿 / 生图稿 / 有字 mock / 无字资产母版 / 运行预览 / 生产候选 / 宣称可继续 / 用户反馈提到倾斜 / 其它
- **已过 gate**：
- **未过 / 待确认 gate**：
- **反向读法检查**：
- **已调用 agent / 复审**：
- **未调用 agent 与原因**：
- **文档 / 实现 drift 检查**：
- **下一步允许做**：
- **下一步禁止跳到**：

## 降级判断

如果出现以下任一项，必须降级产物类型：

- 逻辑烟测截图被当成视觉验收。
- safe-zone / rect 通过被当成正式 UI 质量通过。
- 程序叠字像默认 Label，仍声称 `filled_state_text_mock`。
- 无字底图未通过真实内容填充预览，却要进入 atlas / manifest。
- 可写纸面、按钮底板、CTA 文本槽、任务卡内框或右侧票据倾斜，却声称正交 / 可落地通过。
- 只看整屏图，没有核心组件裁切和水平 / 垂直参考线，却声称几何通过。
- 触发 `ui_geometry_gate` 的任务没有给几何证据，却把产物推进到有字 mock、无字资产母版、manifest、runtime 或生产候选。
- 目标截图与运行截图页面职责或功能分区不一致。
- 用户指出肉眼不成立，而 manifest 只给流程通过。
