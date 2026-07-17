# 区域任务图钉 C 混合竖切片 v3 交付清单

> 日期：2026-07-17
> 阶段：`runtime_candidate_pending_user_visual_review`
> 结论：实际 Godot 效果与定向逻辑已通过；等待用户视觉确认，暂不解锁事件卡。

## 这版采用什么

- 图钉与短签：C 切角楔面为主，保留 B 的安静内容区和 A 的单侧灰蓝纸脊。
- 四类图标：常驻调查、连续追踪、灵视异常、限时截稿使用同一深蓝粗线编辑符号，不再使用默认 Unicode 字符。
- 选中：程序纸背板贴住图钉本体，并只保留一段局部印刷弧；不再使用脱离图钉的完整同心圆。
- 状态：assigned / urgent / locked 使用贴在右上边缘的青蓝 / 锈红 / 灰色状态签；disabled 另用禁用斜线。
- 聚类：保留动态数量，收拢 / 展开用非对称切角纸章的填色与描边变化，不再用圆章和减号替代数量。

## 资产与实现

- 生成后透明资产：`image_gen/2026-07-17/region-task-production-slice-v3/`
- 生产规格与 alpha 指标：`image_gen/2026-07-17/region-task-production-slice-v3/prepared/region-task-pin-slice-v3-alpha-metrics.json`
- Godot 资产目录：`gd_project/Assets/ui/angus_packaging/region_task/v2/pin_slice/`
- 运行时代码：`gd_project/scenes/gameplay/weekly_run/components/WeeklyRunRegionEventPin.gd`
- 聚类样式：`gd_project/scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd`
- manifest：`gd_project/Assets/ui/angus_packaging/region_task/region_task_asset_manifest_v2.json` v4
- 合同：`design/ui-contracts/region-task-board/event_pin_contract.json` v5

## 真实证据

- `01-five-dense-selected.png`：五点密集、选中短签与相邻图钉净空。
- `02-cluster-collapsed.png` / `03-cluster-expanded.png`：八点聚类收拢与展开。
- `04-right-edge-label-clamp.png`：右岸事件的短签自动翻到左侧。
- `05-runtime-state-matrix.png`：available / hover / selected / disabled / assigned / urgent / locked / focus 八态。
- `06-hover-select-runtime-demo.gif`：真实 hover → selected 运行演示。
- 目录：`docs/screenshots/2026-07-17-region-task-pin-slice-v3/`

## 验证

- `test_region_task_manifest_v2.gd`：Godot 4.6.3 通过；三类 v3 资产均可从 manifest 加载。
- `test_region_task_board_v2.gd`：Godot 4.6.3 通过；0 / 1 / N、共享 task_id、选中标签唯一性、密集避让、cluster 与 7–9 行摘要均无回归。
- alpha 指标：pin、label、icon atlas 的可见洋红抠图残留均为 0。
- 沙箱内 Godot 4.3 / 4.6.x 仍会发生 `signal 11`；在真实用户运行环境中复跑通过，属于环境路径问题，不是脚本断言失败。

## UI / UX 最终复核

- UX 初审唯一 P1 为 hover / focus 同构；修正为 hover 单段橄榄弧，focus 深墨短底线 + 两段错位印刷弧 + 深墨标签脊后复核 `PASS`，当前无阻断项。
- UI 同意上述修法；复截后复核 `PASS`。C 切角、安静内容面、单侧纸脊、深蓝图标、状态签与标签色脊已形成同一视觉家族。
- cluster 的切角感与展开色差仍可加强，但双方均判为 P2，不阻断本轮交付，也不需要为此重做 alpha 或结构。

## 尚未放行

- 用户尚未对真实运行候选做视觉确认。
- `rt_event_card_mother`、dossier、CTA 与批量组件生产继续冻结。
- `推进一天` 仍没有玩法命令，不得伪装为可用状态。
