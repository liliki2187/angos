# Loop Log：右 dossier A3 QA 截图局部基线丢失假通过

> **结论**：A3 第一次 609 QA 截图丢失了右侧整块说明内容，但旧 runner 仍因“文件存在、全图非黑、颜色数量足够”返回 PASS；该截图已作废并重截，不进入复审证据。
> **影响**：608 运行图本身有效，第一次 609 无法证明 QA 覆盖没有破坏基线内容；在重截和局部保留率 gate 通过前，A3 不得 finalize。
> **下一步**：复用同一个 SubViewport 场景生成 baseline / QA，并新增右侧说明区亮像素保留率检查；重截 608/609 后再生成 610 与 611。

## 触发与归因

- **触发来源**：父级肉眼自检失败。
- **原始问题**：第一次 609 只剩左侧 dossier 与 QA 框，右侧标题、说明段落和动作语法文本全部消失；runner 却显示 PASS。
- **失败归因**：证据 gate 漏洞。旧 capture 为 baseline 和 QA 分别新建 SubViewport；第二个场景发生局部内容未绘制时，全图非黑与颜色多样性仍能由左侧复杂图片满足。
- **复发判定**：F1“验证等级冒充”第 16 次以上复发。它不是新错误家族，而是“全局统计代替目标区域内容完整性”的同族换皮。
- **本轮处理**：第一次 609 降级作废；capture 改为同一场景先存 baseline、再叠 QA；正式 608/609 重跑并由肉眼复核。

## 防复发实现

1. `capture_world_map_wmw_right_dossier_runtime_v093.gd` 不再为 QA 重建第二套场景；QA 只在 baseline 场景上追加 overlay。
2. capture 内新增右侧说明区 `[650,40,1820,900]` 亮像素计数，QA 保留率低于 baseline 的 `85%` 直接退出码 1。
3. 611 manifest 再用 Python 独立计算同一区域保留率，避免 runner 自证。
4. `frame_post_draw` 双等待、全黑拒绝、颜色多样性与原相对基线检查继续保留；局部 gate 是补充，不替代肉眼。

## 最终证据

- 沙箱内最小复现：headless / windowed 均出现 `signal 11`；不据此判断 Godot 环境损坏。
- 沙箱外固定 `4.6.2-stable` windowed 最小复现：`root.get_texture()` 与 `SubViewport` 均 PASS。
- 重截 609：右侧说明区完整，且与 608 共用同一场景。
- 611：记录右侧区域 baseline / QA 亮像素与保留率；未达到阈值不得写通过。
