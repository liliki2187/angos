# 区域任务 dossier 同源叠印拆分试验 v1｜交付清单

> 日期：2026-07-22  
> 当前状态：`overlay_stitch_probe_v1_go_pending_user_visual_freeze`  
> 交付性质：单例真实拆分 / Godot 1× 回填证明；不是正式生产接入

## 本轮回答的问题

用户希望确认“一体式、没有明确框体的右侧 dossier 是否适合拼接”，并要求实际试装，而不是继续看抽象结构说明。

结论：**适合。** 前提不是把每个分区切成完整卡片，而是保留一张完整底纸，把摘要竖线、青色 metadata 和锈色 risk 作为同源透明印刷层，CTA 继续作为独立交互资源。

## 拆分结果

| 层 | 资产 | 运行职责 |
| --- | --- | --- |
| 完整底纸 | `rt-dossier-base-shell-probe-v1-2x.png` | 单独关闭所有叠印后仍是完整 dossier，不依赖其他层补轮廓 |
| 摘要竖线 | `rt-dossier-summary-accent-probe-v1-2x.png` | 只保留深青编辑竖线，不把中性纸纹切成补丁 |
| 青色信息叠印 | `rt-dossier-metadata-wash-probe-v1-2x.png` | 地点 / 耗时 / 需求的低饱和青色语义区，无边框、阴影和独立纸边 |
| 锈色风险叠印 | `rt-dossier-risk-wash-probe-v1-2x.png` | 风险等级 / 依据 / 建议的锈色语义区；美术向上出血 `10px@1×`，消除两区间白缝 |
| CTA | `rt-dossier-cta-probe-v1-2x.png` | 沿用既有独立交互资源，保持唯一高权重操作终点 |

Godot 试装资源暂存于：

`gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_overlay_probe_v1/`

这些文件未登记进正式 manifest。

## 主要视觉证据

- 拆分爆炸图：`design/art-direction/region-task-board/dossier-overlay-stitch-probe-v1/review/01-dossier-overlay-exploded-v1.png`
- 2× 无字重组：`design/art-direction/region-task-board/dossier-overlay-stitch-probe-v1/review/02-dossier-overlay-recomposed-2x-v1.png`
- Godot 4.6.3 真实 1× 对照：`docs/screenshots/2026-07-22-region-task-dossier-overlay-stitch-probe-v1/05-dossier-overlay-stitch-probe-1x-v3.png`
- Godot 4.6.3 真实 1× 局部：`docs/screenshots/2026-07-22-region-task-dossier-overlay-stitch-probe-v1/06-final-dossier-with-runtime-text-1x-v3.png`

Godot 使用真实中文运行文字验证：任务标题、七行摘要、地点、耗时、需求、风险等级、风险依据、建议以及 CTA 均未进入美术贴图。

## 复核结果

### UI Designer

- 结论：`GO`。
- 最终严重度：`P0=0 / P1=0 / P2=1`。
- 初审指出 `当前任务 / 依据 / 建议 / 任务已就绪` 在 1× 接近最小可读阈值；四处各提升 `1px` 后 P1 关闭。
- 非阻断 P2：浅锈底色面积略大、视觉重量接近 CTA。若正式接入，可轻降饱和度，但不得退回中性 NinePatch。

### UX 老哥

- 结论：`GO`。
- 最终严重度：`P0=0 / P1=0 / P2=1`。
- 扫读链成立：`任务身份 → 摘要 → 地点/耗时/需求 → 风险等级 → 依据 → 建议 → 送至签批台`。
- 青 / 锈叠印共用底纸轮廓且无独立边框、阴影，不读成组件套娃；CTA 仍是唯一实体按钮和视线终点。
- 非阻断 P2：四处辅助小字需要在 `1600×900`、`1366×768` 或字体代理变化下补真实字体回归。

## 运行与环境证据

- 图层审计：`design/art-direction/region-task-board/dossier-overlay-stitch-probe-v1/audit.json`
- Godot：`4.6.3.stable.official.7d41c59c4`
- 渲染：OpenGL 3.3 Compatibility，NVIDIA GeForce GTX 1060 6GB
- 成功命令：使用仓库内最小截图工程、`--windowed --resolution 1920x1080 --audio-driver Dummy --rendering-driver opengl3`。
- 主项目与最小工程的 headless 启动在受限环境中先因默认 `user://logs` 无写权限 / dummy 渲染初始化触发 signal 11；显式写入仓库日志并使用 windowed OpenGL 后成功。该问题属于执行环境，不是资产或 GDScript 断言失败。

## 保持冻结的内容

- 未修改 `dossier_contract.json`。
- 未修改 component inventory 或 `region_task_asset_manifest_v2.json`。
- 未替换 `WeeklyRunRegionTaskBoardV2.gd` 的正式 dossier 实现。
- 未修改 pin v7、密集避让、cluster、clamp、动态文字合同或 event card。
- 未重开 A / B / C 路线，也没有批量铺开状态矩阵。

## 当前需要用户判断

只判断两件事：

1. 这套“完整底纸 + 同源透明叠印 + 独立 CTA”的拆分，在真实 1× 组合后是否仍然像一体式美术，而不是程序组件拼接。
2. 风险区当前的浅锈面积是否可以作为正式资产化起点；若认为偏重，下一轮只做一次降饱和 / 收权重的定向修正，不改变分区、文字、CTA 与几何。

用户确认后，才进入正式资产角色命名、合同升版草案、多分辨率与 CTA 状态矩阵；当前不得把试验资产直接标记为 production frozen。

