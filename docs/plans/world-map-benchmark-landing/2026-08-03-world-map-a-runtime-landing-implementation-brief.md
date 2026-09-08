# 世界地图 A 版真实功能界面落地规格 v0.1

> 状态修订（2026-08-03）：本文记录的是 A279 之前的旧“目标图先行 / 组件资产化”路线。用户否决“旧骨架换皮”和“A 完成构图贴真实文字”后，当前执行真源已切换为 A280 的 `真实行为组件 + 新布局合同 + A 视觉语法`；首个可见检查点见 `2026-08-03-world-map-integrated-functional-skeleton-delivery-manifest.md`。本文保留供审计，不得继续作为当前布局母体。

## 一句话方案

保留现有世界地图的功能几何和数据闭环，把 A 版拆成无字组件资产、动态内容层与真实交互层；先以北美选中态做可玩的单状态纵切片，再补锁定与展开状态。

## 阶段 0：先交付真实内容目标图

2026-08-03 用户指出，进入组件拆分和 Godot 实现前，应先看到真实内容界面长什么样。该纠偏优先于下文所有组件工作：

1. 先制作一张完整 `1920×1080 filled-state visual target`；
2. 使用当前正式中文、地区、状态、任务概况和 CTA；
3. 以世界地图 A 的构图主语、物件关系和情绪为视觉母体；黑白功能稿只校验功能事实与交互边界，不约束精确三栏几何；
4. 用户确认整屏观感后，再执行下文无字组件与运行时纵切片；
5. 未通过前不得把任何新位图接入 Godot 或升格组件合同。

本次阶段误判与回正记录见 `2026-08-03-world-map-runtime-filled-state-first-loop-log.md`。

首张真实内容目标稿因沿用旧界面骨架、仅迁移 A 色材而被用户否决，已降级为偏差案例。下文组件清单在新版 A 母体整屏目标稿通过前继续冻结。

## 为什么不能直接铺 A 版整图

A 版同时烘焙了地区卡、编号、selected 标签、地图 pin、圈选、新闻照片、右侧正文、CTA 与 `DAY 1` 物件。直接作为背景会产生两套互相冲突的界面：玩家看到的按钮与程序真正的 hit rect 不一致，地区切换后背景里的旧状态也不会更新。

正确层级：

```text
L0  深夜背景与无交互环境层
L1  无字地图板 / 地区卡壳 / dossier / 回条 / CTA 位图
L2  动态地区照片与内容图像
L3  路线、selected 圈、状态 overlay
L4  原生中文、期号、周数、剩余天数、任务预览
L5  Button hit、focus、hover、pressed、disabled、transition lock
L6  无字夹子、贴纸、纸影等 no-text / no-hit 装饰
L7  debug / safe-zone 验收层
```

任何位图若同时包含“地图底图 + pin + 中文”或“dossier 壳 + 状态文字 + CTA 文案”，均不得进入运行资源。

## 冻结布局

沿用 `1280×720` 参考画布并在 `1920×1080` 下等比乘 `1.5`：

| 区域 | 参考坐标 | 1920×1080 |
| --- | --- | --- |
| 左栏 | `[24,16,228,688]` | `[36,24,342,1032]` |
| 中央 | `[268,16,648,688]` | `[402,24,972,1032]` |
| 右栏 | `[932,16,320,688]` | `[1398,24,480,1032]` |
| 中央地图 | `[284,64,616,464]` | `[426,96,924,696]` |
| 右 dossier | `[932,30,320,520]` | `[1398,45,480,780]` |
| 中央回条 | `[284,544,616,144]` | `[426,816,924,216]` |

第一轮不按 A 图的像素坐标重排责任区，也不升 `locked_candidate` 合同几何。

## 组件映射

| 功能组件 | 美术资产 | 运行时内容 / 行为 |
| --- | --- | --- |
| 左地区卡 | 无字纸壳、状态徽记、独立地区照片 | 整卡 Button；地区名、selected / locked / warning 动态 |
| 中央地图 | 无字夜班石板蓝地图纸、大块大陆剪影 | pin Button、中文标签、短路线、selected 圈动态 |
| 右 dossier | 无字暖纸壳、背页、夹子、主照框 | 地区名、状态章、简介、任务概况、两条只读预览动态 |
| 任务情报 | 文档图标与分隔线 | 整行 disclosure；collapsed / expanded 原位切换 |
| 主 CTA | 橄榄纸质动作条状态 atlas | `进入地区任务台 / 暂不可进入`；唯一跨层动作 |
| 中央回条 | 无字横向票据壳 | 当前地区摘要、提示、0 天规则；首轮保留 |
| `DAY 1` 机器 | 首轮不装配 | 未接真实日程信号前不得表现为按钮 |

## 第一轮可玩状态

```text
北美禁区带 selected
  ├─ 地图与左卡共同高亮
  ├─ 右侧状态：红线升温
  ├─ 任务情报 collapsed，可展开两条只读预览
  ├─ CTA：进入地区任务台
  └─ 进入前后 remaining_days 不变
```

同期保留东亚 / 太平洋 locked 入口，用于下一刀验证“可选择查看、不可进入”。

## 状态语法

- `available`：可 hover / pressed / focus，但不提前修改右侧内容。
- `selected`：左卡、地图 pin、地区标签和 dossier 同帧更新。
- `warning`：锈红只进入短页签、pin 刻度或状态章；不整页染红，不禁用 CTA。
- `locked`：仍可被选中查看缺口；降低进入邀请感，CTA 为 `暂不可进入`。
- `expanded`：只把 dossier 既有正文区切成两条只读任务，CTA 与纸张零位移。
- `confirming`：首轮仅作为 CTA 的短 transition lock，防止重复触发；不新增二次确认流程。

## 首轮资产清单

1. `world_map_base_night_slate_no_text`。
2. `left_region_card_shell` 与 selected / available / warning / locked 状态层。
3. 每地区照片资源；左卡照片与右 dossier 主照分别遵守现有槽位比例。
4. `map_pin` 五态 atlas。
5. `right_dossier_shell_no_text`。
6. `right_dossier_photo`，严格 `69:44`。
7. `primary_enter_cta` default / hover / pressed / locked_disabled atlas。
8. globe / document / arrow 图标。
9. `center_summary_receipt_no_text`。
10. 最多一枚 no-hit 手绘异常贴纸，作为幽默与品牌证据。

## 验收场景

1. 5 秒看出当前地区、地区状态、剩余天数与唯一主动作。
2. 点击左卡和点击地图 pin 得到相同的四端点状态。
3. 选择锁定地区后右侧出现真实缺口，CTA 禁用但详情可读。
4. warning 不等于 disabled；北美红线升温仍可进入。
5. expanded 只显示两条任务并完整写出 `耗时 N 天`，任务行无按钮反馈。
6. 进入地区前后 `remaining_days` 完全相同。
7. 所有具有按钮感的物件都存在真实回调；装饰物无 hover、手型、发光和完整按钮框。
8. 动态文字与 hit rect 不进入夹子、纸边、折角、状态签和照片边框禁入区。

## 当前边界

- 本规格授权制作 `runtime_testbed / local_proof`，不把 A 自动升级为 production benchmark。
- 左卡 Control 原点、可见纸壳边与 `transparent_bleed` 的坐标口径需在 debug overlay 中显式分开。
- `bottom_receipt_card` 合同与当前 `CenterLowerBand` 存在实现分叉；首轮继续使用中央回条，不并存两套底部系统。
- 若后续要求完整采用 A 的左列宽度、编号标签、`DAY 1` 机器或 loose-object 布局，必须单独升版 world-map frozen contracts。
