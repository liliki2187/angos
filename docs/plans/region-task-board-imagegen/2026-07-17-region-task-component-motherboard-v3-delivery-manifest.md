# 区域任务组件形态 / 材质母版 v3 交付清单

> 日期：2026-07-17
> 阶段：`component_motherboard_v3 / pending_user_variant_selection`
> 结论：可交用户做 A/B/C 选型；不可裁生产资产，不可接 Godot，不解锁事件卡。

## 本轮范围

- 使用真实生图生成同一视觉语法下的三种受控结构变量：
  - 左：A 侧脊型；
  - 中：B 错层型；
  - 右：C 切角楔面型。
- 保留既有 pin、label、cluster 的冻结比例和运行时职责，不修改代码或正式 UI 合同。
- 底部使用深海军蓝、彩色低多边形地图块、浅暖纸三种背景的 `3 × 3` 缩略矩阵检查 25% 识别。
- 将报告、连续链、隐藏线索、临时紧急四类符号改为非 Unicode 的同家族 pictogram，并装入 pin 做实际重心检查。

## 交付物

- 母版：[`20260717-154802_region-task-component-motherboard-abc-v3_01.png`](../../../image_gen/2026-07-17/region-task-component-motherboard/20260717-154802_region-task-component-motherboard-abc-v3_01.png)
- 生图元数据：[`20260717-154802_region-task-component-motherboard-abc-v3_01.json`](../../../image_gen/2026-07-17/region-task-component-motherboard/20260717-154802_region-task-component-motherboard-abc-v3_01.json)
- 过程稿 v1 / v2 保留在同目录，用于审计首版背景矩阵缺失与第二版 overlay 差距，不作为当前选型图。

## 直接标杆复核

- `benchmark-board-01/02`：已恢复大形面、受控异色纸层、薄边与现代平面 editorial collage；未回到旧像素 / 半调坐标系。
- E2：组件不再只有米白轮廓；状态色进入角签 / 侧脊，四类 kind icon 形成统一系列。
- 100%：三种变量和 pictogram 重心可辨。
- 25%：C 的切角身份保留最稳，A 次之；B 在浅底仍最保守。

## UI / UX 复核裁决

- UX：v2 为 `CONDITIONAL PASS`，实证改荐 C 为主，吸收 B 的安静内容面与 A 的单侧纸脊。
- UI：同意改荐 C；上轮 A 首选是理论判断，本轮 25% 实证优先。
- v3 已按共同阻断项做唯一一轮定向修正：kind icon 入钉、状态收回边界、删除外置长条、降低压纹 / 双框 / 厚阴影。

## 仍未放行

- 用户尚未选择左 / 中 / 右方案。
- 选中载体在最终生产前仍需单独证明附着于 pin；不得复用引擎式闭合虚线环。
- 当前图不能直接裁成透明 alpha，也不能替换 `rt_event_pin_shell`、`rt_event_label_shell`、icon atlas 或 cluster 程序样式。
- `rt_event_card_mother` 继续冻结。

## 用户选型后的下一步

只对用户选定方案进入正式生产：先输出透明 pin / label clean master 与独立 icon / status / selected 叠层，再按既有尺寸、锚点与 100% / 25% Gate 接回单类 Godot vertical slice。未获选择前不得继续自发生图。
