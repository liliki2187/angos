# 世界地图 v4 夹层收口与一图复用交付清单

**结论**：v4 已完成两项局部返工：左索引与 DAY 之间的无职责夹层由 `106px` 收紧为 `16px`；左地区卡与右 dossier 改为引用同一个 `69:44` canonical 地区资源，并按 `138×88 → 414×264` 严格三倍等比显示。

**影响**：不对称三责任区、`960×700` 地图、三个 beacon、右侧唯一 CTA、collapsed / expanded 与 selected / warning / locked 语法不变。当前产物仍是 `runtime_skeleton / runtime_state_preview`，不能据此宣称正式地区美术完成。

**下一步**：用户先复核 v4 真实截图；若结构与复用方式通过，再把当前 SVG 功能占位资源替换为同合同的正式 `1104×704` 地区美术母图。

## 变更合同

- `RegionIndex=[36,174,372,650]`，结束于 `y824`。
- `ReadOnlyTimeStrip=[36,840,372,86]`，与索引间隔 `16px`。
- canonical source：每地区唯一 `1104×704 / 69:44`。
- 左卡 display：`138×88`。
- 右 dossier display：`414×264`。
- 变换：完整 UV、宽高严格 `3×`、禁止裁切、禁止非等比拉伸。
- 状态：locked 只做运行时低饱和调制；selected / warning / locked 不烘焙进图片。
- 右 dossier：外框不变；图片增高后 disclosure、preview、cost 与 CTA 固定下移，collapsed / expanded 不推动 CTA。

## 运行证据

- `gda script validate`：本轮修改的五个原型脚本与两个测试脚本全部 PASS。
- 正式 Godot agent smoke：`Godot agent smoke passed.`。
- 独立原型 headless 状态测试：`test_world_map_integrated_prototype.gd OK`。
- 重定向 Godot 用户缓存后的窗口化 OpenGL 状态测试：`test_world_map_integrated_prototype.gd OK`。
- 真实截图脚本：`capture_world_map_integrated_prototype.gd OK`。
- 首次未重定向用户缓存的窗口化测试发生 Godot 4.6.3 原生 signal 11；按故障卡 006 分流后，项目 smoke、headless 与重定向缓存的同版本 GUI / OpenGL 路径均通过，因此不归因于本轮 GDScript。

## 截图证据

目录：`docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/`

- `21-clean-no-gap-shared-image-v4.png`：collapsed 首帧与左栏 16px 收口。
- `22-hit-rect-review-v4.png`：地图、三卡、beacon、disclosure、CTA 与只读 DAY 热区证据。
- `23-locked-feedback-v4.png`：锁定阻断不替换 selected / dossier。
- `24-mission-expanded-v4.png`：三行只读预览展开，CTA 不移动。
- `25-interaction-state-sequence-v4.gif`：真实运行状态短序列。
- `26-shared-region-image-proof-v4.png`：左图按 3× 放大与右图完整画幅并排。

## 阶段边界

- 能证明：夹层空洞已收紧；同一地区左右节点引用同一资源；显示比例、完整画幅与交互状态成立。
- 不能证明：SVG 占位图达到正式美术标杆；其它地区正式图片已生图；完整状态 atlas 或正式 `WeeklyRunGame` 接线完成。
- 允许：继续用户视觉裁决；按同一 canonical 合同替换正式美术。
- 禁止：把当前 SVG 称为生产美术；为左卡另做不同裁切的 thumbnail；重新把 DAY 固定回底部制造夹层。

## 双审收口

- UX 终审：夹层空洞、DAY 下方外缘负空间、同源图识别、collapsed / expanded 容量与主操作链 PASS；初审仅保留 disclosure 可发现性 P2。
- UI Designer 首次终审：核心合同通过，但发现 CTA 与前层纸页可见底边贴合、disclosure 无方向符号两个 P1；父级采用更严格口径局部修正。
- 修正后 UI Designer 最终复核：`PASS / P0=0 / P1=0 / P2=0`。前层纸页完整覆盖 `468×842`，CTA 下方恢复约 `16px` 暖纸边；同一 Button 内 `⌄/⌃` 可见，热区数与功能 rect 均未变化。
- 修正后 UX 最终复核：`PASS / P0=0 / P1=0 / P2=0`，原 disclosure 可发现性 P2 已关闭，七类冲突扫描无新增问题。

## 反向读法

- 左栏 5 秒读法应是“地区列表结束后紧接只读 DAY”，而不是“少了第四张卡”。
- 图片 5 秒读法应是“左边这张小图就是右边同一张图放大”，而不是“同题材的两张图”。
