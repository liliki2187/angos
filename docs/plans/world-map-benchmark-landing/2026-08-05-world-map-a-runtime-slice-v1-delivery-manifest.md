# 世界地图 A 风格真实运行纵切片 v1 交付清单

## 结论

世界地图 A 风格第一次进入 A282 的真实 Godot 功能层。当前结果不是整屏背景贴图：中央地图、北美新闻母图和四类纸材由无字 imagegen 资产承担；动态中文、地区状态、三态 beacon、任务展开、CTA、热区与焦点继续由 Godot 原生层承担。

> **2026-08-06 用户视觉 Gate 修订**：上述表述把“状态由 Godot 控制”与“符号美术由 Godot primitive 绘制”混为一谈。UFO 便签、三窗事件牌与 eye beacon 的可见图形实际由 GDScript 程序绘制，并非 imagegen 正式美术；用户已明确否决其粗糙度。当前纵切片降为 `runtime_state_preview / user_visual_gate_failed_programmatic_symbol_assets`，此前 UI / UX PASS 只保留为功能与布局证据。

## 产物身份

- `runtime_state_preview`
- 可以证明：A 风格母体可与 A282 精确责任区共存；北美同图三倍复用、8 个交互节点、Schedule 禁用输入、locked 不改选区和 disclosure 原位展开仍成立。
- 不能证明：三地区新闻图均已生产完成、完整 `WeeklyRunGame` 导航已接通、当前北美新闻图已升格生产母版、hover / pressed 动画节奏已冻结。

## 本轮落地

1. M0 输入合同：`ScheduleGate` 根节点与全部子 Control 均为 `MOUSE_FILTER_IGNORE / FOCUS_NONE`，自动测试断言焦点后代数与指针消费后代数均为 0。
2. M1 无字资产：
   - `1104×704` 北美新闻母图；
   - `960×902` 无字世界地图板；
   - 暖纸、锁定纸、橄榄票据与钢蓝背纸四张无字表面纹理；
   - 生成原始源已保存到 `image_gen/2026-08-05/world-map-a-runtime-slice-v1/sources/`。
3. M2 北美 selected 纵切片：左卡、地图 beacon、右 dossier 与 CTA 共享 `selected_region_id`；地图使用粗墨撕纸眼睛，selected 使用钢蓝错位背纸与不闭合手画圈，locked 使用同轮廓半闭眼睑。
4. 视觉职责：芥末便签只作为北美异常附件；机构分隔线保持细线；主 CTA 使用橄榄撕票结构；纸纹不承载动态文字。
5. P1 收口：东亚与太平洋锁定卡使用不同错位背纸；任务展开区加入编辑清样式编号色条与分隔；北美异常簇加入“三滚筒窗共用一条海平线”的无字事件附件；locked 点击反馈压缩为单行状态确认，完整解锁条件只由地区卡承载。

## 自动 Gate

- `button_count = 8`
- 8 个交互节点名称逐一断言为 3 卡、3 beacon、disclosure 与 CTA
- Schedule `advance_enabled=false`
- Schedule `root_mouse_filter=MOUSE_FILTER_IGNORE`
- Schedule `pointer_consuming_descendant_count=0`
- Schedule `focusable_descendant_count=0`
- 北美 source `1104×704`
- 左卡 `138×88`、右档案 `414×264`、同一 `resource_path`
- 左右图片均为 `STRETCH_KEEP_ASPECT_CENTERED`
- 地图板 source / display 均为 `960×902`，beacon 与文字由 runtime overlay 拥有
- 三责任区与 CTA / disclosure exact rect 无漂移
- disclosure 展开前后 CTA 的实际 `global_rect` 完全一致
- locked 点击后的单行反馈、选区与 dossier 不变均有断言

## 双终审

- UI Designer：`PASS`（仅限 `runtime_state_preview`），`P0=0 / P1=0`。剩余 P2 为 dossier 顶部夹子略像占位符、Schedule 的 `DAY 1` 器物感偏弱、locked beacon 小尺寸下略像灰横杠；均不阻塞本纵切片结束。
- UX 老哥：`PASS`（`runtime_state_preview`），`P0=0 / P1=0 / P2=0`。locked 文本安全、主操作链、GIF 状态序列、8 节点、Schedule 输入隔离、CTA 零位移与同图 stretch 合同均通过。
- 综合结论：结束纵切片内部迭代，进入用户视觉 Gate；不得将本结论扩大为生产美术冻结。

### 2026-08-06 用户视觉裁决

- 用户视觉 Gate 未通过：程序绘制的 UFO、三窗事件牌和 eye beacon 与 A 风格稿的手绘贴纸完成度不一致。
- 撤回“纵切片视觉 P1 已清零”的扩大解释；结构、交互与文本 P1 仍保留通过。
- 下一步只替换上述符号的可见美术层；在真实生图透明资产接入并重拍前，不扩产东亚 / 太平洋，不接正式宿主。

### 2026-08-06 修复去向

真实符号资产替换、逐态测试与新截图已转入 `2026-08-06-world-map-a-runtime-symbol-pack-v1-delivery-manifest.md`。本 v1 清单继续保留为程序符号失败证据，不再代表最新视觉状态。

## 真实证据

目录：`docs/screenshots/2026-08-05-world-map-a-runtime-slice-v1/`

- `01-selected-collapsed.png`
- `02-locked-feedback.png`
- `03-selected-expanded.png`
- `04-hit-rect-review.png`
- `05-interaction-state-sequence.gif`
- `index.html`

## 下一 Gate

先以真实生图透明资产替换程序符号层并重新提交用户视觉 Gate，再决定是否：

1. 把北美新闻图从当前中等偏高密度候选继续压到 A285 的中间颗粒真值；
2. 为东亚 / 太平洋按同一 `69:44` 管线生产正式母图；
3. 把当前隔离 prototype 接入正式 `WeeklyRunGame` 世界地图入口。

用户视觉通过前，不批量扩产三地区，不把本轮资源标成 `production_frozen`。
