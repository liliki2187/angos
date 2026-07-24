# 区域任务短签一体接合 v3 交付清单

> 日期：2026-07-21  
> 阶段：`rejected_by_user / negative_join_evidence`  
> 范围：只修复 pin / label 一体接合；尚未替换 Godot 生产实现

## 用户复核结论（2026-07-21）

用户否决本候选：红框区域仍同时暴露完整 pin 右边线、绿色竖背板、横条左端切角和上下凹口，说明它只是两个完整组件发生重叠，并没有成为真正共用轮廓的一体组件。此前美术 / UI / UX GO 全部撤回；本清单及截图只保留为反例和技术管线证据，不得冻结或接入 Godot。

## 原技术结论（已降级）

v2 中右挂约 10px、左挂约 12px 的贯穿暗缝已经消除。v3 将 pin 与 label 的纸质关系烘焙为同一 compound background：横条内肩埋入 pin 下方，pin 前壳压在横条上方；没有新增程序连接色块，也没有移动逻辑 anchor。

## 主审证据

- 修正前后局部对照：`docs/screenshots/2026-07-21-region-task-pin-integrated-join-v3/01-v2-v3-integrated-join-comparison.png`
- 四类型、左右挂与状态压力真实 1×：`docs/screenshots/2026-07-21-region-task-pin-integrated-join-v3/02-native-1x-integrated-join-evidence-v3.png`
- 真实生图接合源板：`design/art-direction/region-task-board/runtime-preflight-v3/01-integrated-pin-label-source-v3-alpha.png`
- 最终生图提示词：`design/art-direction/region-task-board/2026-07-21-region-task-integrated-join-v3-imagegen-prompt.md`

## 美术资源

- 16 个独立 compound frame：`design/art-direction/region-task-board/runtime-preflight-v3/frames/`
- 右挂 default / selected atlas：`rt-task-compound-right-default-v3-atlas-3x.png`、`rt-task-compound-right-selected-v3-atlas-3x.png`
- 左挂 default / selected atlas：`rt-task-compound-left-default-v3-atlas-3x.png`、`rt-task-compound-left-selected-v3-atlas-3x.png`
- 预检元数据：`design/art-direction/region-task-board/runtime-preflight-v3/runtime-preflight-assets-v3.json`
- 生成与回填脚本：`scripts/art/build_region_task_integrated_join_preflight_v3.py`

## 不变量

- hit：`72×80`
- pin：`64×80`
- anchor in hit：`[36,76]`
- 右 caption rect：`[78,4,200,72]`
- 左 caption rect：`[-208,4,200,72]`
- 动态文字区：`[14,12,158,48]`
- 右 compound footprint：`278×80`
- 左 compound footprint：`280×80`
- dense、cluster、clamp 与 hover → selected 的逻辑合同不变

## 接合合同

- 右挂美术 underlap：`12px`
- 左挂美术 underlap：`10px`
- 层级：`compound paper < kind icon / dynamic text < state badge`
- 16 个 frame 在 `alpha > 24` 下均为单一主要连通体
- 接合处不允许贯穿地图底色、双描边、纯色色块桥或第二状态色

## 程序后处理边界

程序只负责：

- 色键透明化；
- 九宫格延展横条中央空白纸面；
- 精确裁切、尺寸归一、atlas 拼装；
- 动态图标、标题、meta 与状态签回填；
- alpha 连通性与尺寸 QA。

程序没有重画 pin、纸张材质、selected 背板、类型色、端帽或接合补丁。

## 复核结果

- 美术指导：PASS；上下短凹口属于合理裁纸肩，不建议继续加工。
- UI Designer：`P0=0 / P1=0 / GO`。
- UX 老哥：`P0=0 / P1=0 / P2=1 / GO`。
- 保留 P2：常驻橄榄绿与隐藏蓝灰 selected 的外围增量弱于限时 / 连续；与本轮接合无关，不阻断。

## 尚未执行

- 未替换 `WeeklyRunRegionEventPin.gd` 或 Godot 正式资源。
- 未修改 `event_pin_contract.json`、正式 manifest 或 label anchor。
- 未重跑五点 dense、cluster 收拢 / 展开、右边缘 clamp 与 hover → selected 动图。
- event card 继续冻结。

## 当前需要用户判断

本候选已被用户否决，不再要求继续判断。下一轮改为先审核“共享外轮廓 compound”大比例无字结构稿；通过后才制作四类型与运行时 1×回填。
