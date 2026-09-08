# 世界地图运行纵切片程序符号误当美术资产 Loop Log

## 决策条

- **结论**：芥末 UFO 便签、冷青三窗事件牌与 eye beacon 是 GDScript 程序绘制，不是生图软件生成的正式符号美术；撤回本纵切片的用户视觉通过口径。
- **影响**：当前截图仍可证明 A282 功能合同、状态同步、同图三倍复用和输入隔离，但不能证明贴纸 / beacon / 异常附件已达到 A 风格稿的手绘完成度。
- **下一步**：冻结布局与交互，使用真实生图工具生产同一套无字透明符号母版，替换程序可见层后重新截图审查。

## 详情

- **触发来源**：用户反馈。
- **原始问题**：用户圈出地图北美异常簇，指出“这些符号是啥，看起来很粗糙，不是用生图软件生的吧”。
- **事实核查**：`WorldMapIntegratedMapDecor.gd` 通过 `draw_polygon / draw_arc / draw_polyline / draw_line / draw_circle` 绘制 UFO 便签与三窗事件牌；`WorldMapIntegratedBeacon.gd` 通过相同 primitive 绘制撕纸眼睛、selected 圈和 locked 眼睑。只有纸张纹理、世界地图板和北美新闻母图来自 imagegen。
- **错误归因**：父级把“动态 overlay 应由 runtime 拥有”错误扩大成“overlay 的可见美术也可由程序临时绘制”，并在交付中把生图纸纹与程序符号合并表述为美术落地完成；这违反 A48 的资产 provenance 边界，也绕过了 A285 / A287 的符号画法 Gate。
- **为什么评审未拦住**：UI / UX 终审聚焦 P1 布局、状态链、文本安全、热区和同图合同，没有逐对象核对可见资产来源；父级也没有在 delivery manifest 中按对象列出 `imagegen / runtime text / runtime state / temporary debug drawing` 四类 provenance。
- **复发判定**：已知错误家族“程序化近似冒充美术资源”再次复发；不是新的审美分歧，而是既有硬规则未执行。

## 修复边界

- 保留 A282 exact rect、三栏职责、8 个交互节点、Schedule 输入隔离、locked 不改选区、disclosure 原位展开与 69:44 同图三倍复用。
- 不重做世界地图板、北美新闻母图、纸材、动态中文或功能数据。
- 只重做承担品牌画法的可见符号层：UFO / 问号 / 划叉、三窗共享海线事件牌、eye beacon default / selected / locked，以及必要的真实美术 selected / warning 覆盖层。
- 生图必须输出无字透明资产；程序只做裁切、尺寸整理、manifest、状态切换与位置装配。

## 交付前新增检查

1. delivery manifest 对每个可见对象列出 provenance；任何 `temporary_debug_drawing` 不得出现在用户视觉候选截图中。
2. 符号以 `96px / 48px` 双尺度和 1920×1080 整屏同时与 A 风格稿并排检查。
3. 先核对真实源文件 hash / 路径，再由代码证明 runtime 只切换资产，不重新用 primitive 描摹终稿。
4. UI / UX PASS 只覆盖各自职责；父级必须额外完成标杆画法与资产来源 Gate，不能再把两者的 PASS 扩大为美术通过。

## 当前产物身份

- `runtime_state_preview / user_visual_gate_failed_programmatic_symbol_assets`
- 可保留为功能与交互证据。
- 不可作为符号美术、完整视觉、生产资产或后续批量扩产真源。

## 修复结果（2026-08-06）

- 使用 Codex 内置 ImageGen、A 风格稿参考与纯 `#ff00ff` 色键，生成无字 UFO 便签、三窗事件牌和四态 eye 母版；`remove_chroma_key.py` 只负责去背，项目脚本只负责透明裁边、等比缩放、切片与 manifest。
- `WorldMapIntegratedMapDecor.gd` 与 `WorldMapIntegratedBeacon.gd` 已删除品牌图形的 `draw_polygon / draw_polyline / draw_arc / draw_circle`；动态文字、地区编号、机构细连接线、hover/focus/blocked 反馈继续由 runtime 控制。
- Godot 4.6.2 自动测试通过：8 个交互节点不变；UFO / 事件牌资源路径与 display rect 固定；eye 的 default / selected / selected_warning / locked 四态逐态验证路径、`144×144` source、`72×72` display、stretch 和 mouse-ignore。
- UI Designer 终审 `PASS / P0=0 / P1=0 / P2=2`，P2 只要求事件牌不得再缩小、UFO 文案保持两行；UX 老哥终审 `PASS / P0=0 / P1=0 / P2=1`，其四态矩阵 P2 已在终审后补齐并通过测试。
- 当前身份更新为 `runtime_state_preview_symbol_provenance_pass_pending_user_visual_gate`。错误家族已在实现与自动化层关闭，但仍等待用户对新截图作最终视觉判断。
