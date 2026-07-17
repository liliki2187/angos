# WMW 功能结构稿 Delivery Manifest

> **A228 追加修订**：本文件中的 369×207 双回执和全高右侧载体已被用户进一步否决。当前交付真值见 `2026-07-17-world-map-wmw-functional-density-v2-delivery-manifest.md`。

## 交付结论

已交付精确 1920×1080 黑白功能结构稿，证明三栏职责、主要组件坐标、双动作分离、默认折叠态和左右下角闭合关系成立。该稿是 `structure_wireframe`，不证明美术通过，也不证明推进日已经在 runtime 中实现。

## 产物

- 结构稿 PNG：`docs/prototypes/world-map-wmw-black-white-structure/black-white-function-structure-v1.png`
- 可编辑结构页：`docs/prototypes/world-map-wmw-black-white-structure/black-white-function-structure-v1.html`
- 确定性渲染脚本：`docs/prototypes/world-map-wmw-black-white-structure/render_wireframe.py`
- 几何与语义审计：`docs/prototypes/world-map-wmw-black-white-structure/black-white-function-structure-v1-audit.json`
- Router Card：`2026-07-17-world-map-wmw-functional-structure-router-card.md`
- 双 Agent 复核：`2026-07-17-world-map-wmw-functional-structure-review.md`
- Loop Log：`2026-07-17-world-map-wmw-visual-closure-before-functional-structure-loop-log.md`

## 几何合同

| 区域 | 1920×1080 坐标 `[x,y,w,h]` | 结果 |
| --- | --- | --- |
| 左栏 | `[36,24,342,1032]` | 通过 |
| 中栏 | `[402,24,972,1032]` | 通过 |
| 右栏 | `[1398,24,480,1032]` | 通过 |
| B2.12 卡 1 | `[66,36,306,240]` | 通过 |
| B2.12 卡 2 | `[66,294,306,240]` | 通过 |
| B2.12 卡 3 | `[66,552,306,240]` | 通过 |
| 左下全局日程器 | `[36,810,342,246]` | 通过 |
| 世界地图主舞台 | `[426,96,924,696]` | 通过 |
| 红线预警回执 | `[432,837,369,207]` | 通过 |
| 深链动向回执 | `[836,837,369,207]` | 通过 |
| 右侧全高载体 | `[1398,24,480,1032]` | 通过 |
| A5.1 | `[1398,45,480,780]` | 通过 |
| A5.1 照片 | `[1431,192,414,264]` | 通过 |
| A5.1 任务情报 | `[1425,630,426,66]` | 通过 |
| A5.1 主 CTA | `[1425,711,426,75]` | 通过 |

## 功能合同

| 玩家问题 / 动作 | 唯一主人 | 结构结果 |
| --- | --- | --- |
| 当前第几天、还剩几天 | 左下全局日程器 | 单一主人，通过 |
| 推进到下一天 | 左下全局日程器 | 存在；首次点击确认；后果预览 |
| 选择地区 | 左卡 / 地图针脚 | 同一选区链 |
| 当前地区说明 | A5.1 | 存在 |
| 查看任务情报 | A5.1 disclosure | 默认收起 |
| 进入地区任务台 | A5.1 主 CTA | 全屏唯一最强动作；进入不耗天 |
| 世界变化回执 | 中下两张回执 | 只读；最多两张 |

## Gate

- 画布尺寸：1920×1080，通过。
- 三栏与关键组件坐标：审计 JSON 已记录，通过。
- 推进日 / 进入地区双动作分离：通过。
- 顶部剩余天数重复：0，通过。
- 中下第三回执：0，通过。
- 右下文字 / 图标 / hit rect：0，通过。
- A5.1 默认展开：否；`collapsed`，通过。
- runtime 独立推进日命令：未实现，不通过也未宣称通过。

## 评审

- UX 老哥：现状 P0=1（目标动作缺失且存在视觉承诺 / runtime 命令缺口）；结构稿修正后，该缺口被显式标注，不再伪装为已实现。P1 为 frozen 几何漂移、空白 / 重复中下卡、时间事实双主人和日程器材质错误。
- UI Designer：接受 UX 的操作链与层级，给出精确 1920×1080 元素表；父级只对“顶部是否重复剩余天数”做了冲突裁决，采用 UX 的单一主人方案。
- 完整正文：`2026-07-17-world-map-wmw-functional-structure-review.md`。

## 能证明 / 不能证明

可以证明：功能分区、主要尺寸、动作层级、默认态、四角承重、结构容量。

不能证明：最终纸张材质、低多边形美术质量、中文生图精度、真实 hover / confirming 动效、Godot 运行状态、推进日状态机、生产资产可切图。

## 状态

`structure_wireframe_pass / filled_state_text_mock_allowed / runtime_advance_day_blocked_until_command_exists`
