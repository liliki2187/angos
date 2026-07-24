# WMW v5.1 默认态完整整屏视觉风格稿复核

## 结论

`wmw-fullscreen-default-filled-style-v0-1.png` 是 A242 后第一张 1920×1080 完整默认态玩家视图。UI Designer 与 UX 老哥曾在交付前判 PASS，但用户复核发现左栏复用了 imagegen 源的占位载体后又叠加真实载体，产生双底板、残留横条与套框。v0.1 因此撤回视觉候选身份，仅保留为失败证据；详见 `2026-07-21-world-map-wmw-fullscreen-left-column-double-carrier-loop-log.md`。

- UI Designer：`PASS，P0=0 / P1=0 / P2=0`。
- UX 老哥：`PASS，P0=0 / P1=0 / P2=2`；父级逐项复核后保留 1 个观感 P2，排除 1 个误读 P2。
- 用户状态：`v0_1_rejected_left_column_double_carrier`。

## v0.2 左栏纠偏

用户确认图 1 左栏混乱后，UX 老哥诊断 v0.1 为 `ITERATE，P0=0 / P1=2 / P2=1`：三卡存在双 carrier 与已退役 meta 残影，日程器把 placeholder 与真实操作层叠在一起。UI Designer 随后给出只改左栏的精确施工表。

v0.2 不重新调用 imagegen，只复用三张照片 RGB；三张源卡的 footer、占位横条、占位状态块、外框和阴影全部停止复用。每张卡重建为单外框、单照片窗、单 footer、单状态块；日程器重建为日期头、动作区、后果区三层。

- UI Designer 最终：`PASS，P0=0 / P1=0 / P2=0`。
- UX 老哥最终：`PASS，P0=0 / P1=0 / P2=0`。
- `placeholder_carrier_reuse_count=0`。
- v0.2 相对 v0.1 的 `x>=402` 区域差异像素为 0，中央与右栏未改变。
- v0.2 SHA-256：`ac351af37889c728a7996573ec65659e20e4a5b540e3d877b43ba1892f29f23b`；连续两次渲染一致。
- 当前唯一用户审阅入口：`wmw-fullscreen-default-filled-style-v0-2.png`。
- 用户状态：`v0_2_pending_style_decision`。

## v0.3 共轴纠偏

用户继续复核 v0.2 后指出三卡与左下日程器不同轴：三卡为 `[66,y,306,240]`，日程器仍为 `[36,810,342,246]`。该问题属于正常观看比例即可发现的基础 P1，v0.2 的 PASS 因此撤回。

v0.3 按 A244 只修订日程器：外框改为 `[66,810,306,246]`，与三卡共享 `left=66 / right=372 / center=219`；三段垂直间距均为 18px。日期头、动作区、图标井与两条后果按新宽度缩排，功能文字不减项。

- UI Designer：`PASS，P0=0 / P1=0 / P2=0`。
- UX 老哥：`PASS，P0=0 / P1=0 / P2=0`。
- 对齐硬 Gate：0px 容差通过。
- v0.3 相对 v0.2：三张卡差异 0，中央与右栏差异 0；变化只在旧 / 新日程器及其阴影包络。
- v0.3 SHA-256：`6e5d7aa71953636032127f9af5c0fbf679bc66f26cef2d1c4bac4a73a7c9bb13`；连续两次渲染一致。
- 当前唯一用户审阅入口：`wmw-fullscreen-default-filled-style-v0-3.png`。
- 用户状态：`v0_3_pending_style_decision`。

## v0.3 美术身份降级

用户进一步复核后指出：v0.3 的按钮、状态块和纸面仍有明显程序矩形粗糙感，左栏虽然内部共轴，但整组 `x=66,w=306` 相对标杆过度内缩。v0.3 因此降级为 `filled-state functional assembly / geometry and real-content evidence`，不再等待美术采纳。

UX 老哥判 `P0=0 / P1=2 / P2=0`：一项是程序装配不能代表正式美术完成度，另一项是左栏组与画布边缘的关系未关闭。UI Designer 已将下一完整 art pass 候选收敛为四外壳 `[30,y,348,h]`，并保持三段 18px 间距；中央和右栏职责 / rect 不变。

下一用户审阅入口改为按 `2026-07-21-world-map-wmw-fullscreen-art-pass-v0-4-production-brief.md` 生成的完整 1920×1080 真实中文效果图。

## 这张图解决什么

此前的 `schedule_gate` 只证明局部状态分层与拆图技术，不能证明 WMW 整屏美术成立。本稿把 v5.1 冻结三栏、真实默认态中文内容与 benchmark-board-01/02 的 modern clean-low-poly weekly 视觉基因合并到同一张玩家视图中，让用户能够直接判断：

1. 中央地图是否是真正主场；
2. 右侧地区档案是否形成第二阅读层；
3. 左卡、日程、地图、纸页与 CTA 是否属于同一个 WMW；
4. 右下 CTA 是否为唯一主动作；
5. 是否可以把该整屏方向作为后续组件资产化的视觉基准。

## 生成与装配

- built-in imagegen 已真实调用，最终 prompt 记录在 `2026-07-21-world-map-wmw-fullscreen-visual-style-default-production-brief.md`。
- imagegen 源：`docs/prototypes/world-map-wmw-fullscreen-visual-style-default/wmw-fullscreen-default-imagegen-source-v0-1.png`，只提供无字整屏色重、材质、地图与照片气质，不是几何真源，也不是用户审阅入口。
- 程序装配：`render_wmw_fullscreen_default_style_v0_1.py`，负责按 v5.1 rect 重建全部 carrier、后置真实中文、pin、锁、任务和 CTA，并输出审计。
- 最终玩家视图：`wmw-fullscreen-default-filled-style-v0-1.png`。

## UI Designer 最终意见

`PASS，P0=0 / P1=0 / P2=0`。中央地图已成为第一视觉中心，右档案稳定在第二层级，右下 CTA 是全屏唯一最强动作；左卡、日程、地图和右纸已统一为同一套 clean-low-poly weekly 材质语言。三栏 rect、四任务容量与默认态内容稳定，未见路线、红线章、额外功能、假字或阻断性的生成痕迹。

## UX 老哥最终意见与父级裁决

`PASS，P0=0 / P1=0 / P2=2`。玩家可以先读北美选区，再由右侧同名档案承接，并在底部找到唯一主 CTA；日程器次级但可发现，四角职责闭合，无假按钮、隐藏控制、路线、红线章或伪 runtime 差量。

两个原始 P2：

1. 右侧暖纸与中央选区权重接近，用户需重点判断右栏是否抢地图主场。该项保留为用户观感裁决，不阻断交付。
2. UX 目读第四条任务为“未班车”。父级对照脚本与 UTF-8 审计，二者均为内容真源规定的 `M330 末班车空白段`，排除该误读，不修改图像。

因此父级归一化记录为 `PASS，P0=0 / P1=0 / P2=1`。

## 审计结果

- 真实 PNG：`1920×1080`。
- SHA-256：`9481b63ad626fc91e50182a0394d5e15b09f4217d11a065d4fec71a8895efb59`。
- 文字安全区：44 / 44 通过。
- 地图 pin：3；任务行：4；主 CTA：1；路线：0；新增模块：0。
- 连续两次渲染 hash 相同，确定性复现通过。
- “红线升温”状态章不存在；限时信息只保留在任务摘要与具体任务行。

## 边界

- 本稿是静态 filled-state visual style mock，不证明 runtime 已实现。
- 未生成 confirming、组件 atlas 或其他组件状态。
- 未修改 Godot、正式组件合同、compact A5.1、B2.12 或三栏结构。
- 用户确认前继续暂停组件扩产。
