# Delivery Manifest：区域任务台组件裁切准入

> 日期：2026-07-16
> 产物类型：`production_preflight / component_contract`，不是可见 UI 改动或生产美术资产。

## 交付内容

1. `component_cutout_inventory_v1.json`：18 个唯一 class；经首条切片验证后修订为 10 类独立透明母版、5 类矩形 NinePatch、2 类不透明底图 / tile、1 类程序组件。短签固定 200×72，不再走未经验证的拉伸路线。
2. `2026-07-16-region-task-board-component-cutout-preflight-v2.md`：人工可读的完整功能、交互、裁切和首轮生产评估。
3. `event_card / event_pin / dossier / schedule / page` 合同增补：状态矩阵、尺寸、alpha、阴影、摘要溢出和直接裁切禁令。
4. `region_task_asset_manifest_v2.json`：引用裁切 inventory，增加 1366×768 回归目标和完整 pin 状态。
5. `validate_component_cutout_inventory.py`：校验唯一 ID、路线计数、必需字段、首条切片和 manifest 合同引用。
6. `STATUS.md`、Loop Log 与 A212 修订：保存当前 Gate 和防复发规则。

## Gate 结果

| 项目 | 结果 |
| --- | --- |
| E2 继续作为综合色调 / 组合气质参考 | PASS |
| 从 E2 直接裁正式组件 | BLOCKED，数量冻结为 0 |
| 全部正式 class 已登记 | PASS，18 / 18 |
| 生产路线完整 | PASS，`10 / 5 / 2 / 1` |
| 首条纵向切片 | PASS，冻结为 pin + 短签 |
| 批量任务卡 / dossier / atlas 生产 | BLOCKED |
| 真实 Godot 回插 | 2026-07-16 后续 PASS；Godot 4.6.3 已完成 manifest、0 / 1 / N、密集、cluster、clamp、状态矩阵与主流程验证。4.6.2 的 `signal 11` 作为环境差异保留。 |

## 验证证据

- `python scripts/ui-contracts/region-task-board/validate_component_cutout_inventory.py`：通过。
- JSON 解析：inventory、page、event card、event pin、dossier、schedule 与 manifest 均有效。
- `git diff --check`：本轮相关文本无空白错误。
- `test_region_task_manifest_v2.gd`：连续两次在 Godot 4.6.2 启动阶段崩溃，未进入断言；明确记录为未通过，而不是功能失败或成功。

## 下一步

只为 `rt_task_pin_shell_mother` 与 `rt_task_pin_label_mother` 制作单件、无字、自带透明通道的候选资产。候选必须经过 alpha probe、300% 边缘检查、3x 缩小、anchor / hit rect、0 / 1 / N / 密集避让、状态矩阵和真实 Godot 回插；任一证据不通过，不进入事件卡生产。
