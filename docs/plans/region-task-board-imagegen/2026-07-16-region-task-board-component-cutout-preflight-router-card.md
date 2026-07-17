# Router Card：区域任务台组件裁切准入

> 日期：2026-07-16

- **用户明示目标**：在继续生产前，确认所有功能组件的裁切难度与落地方式；每个需要裁切的组件必须先确定，避免先追求整屏美观再做污染裁切。
- **当前阶段**：`production_preflight / component_aspect_taxonomy`。
- **本轮必要补全**：唯一 `asset_id`、生产路线、母版数、尺寸状态、倍率、alpha / padding、阴影所有权、允许 / 禁止烘焙内容、状态派生和首条纵向切片。
- **本轮不做**：不生图、不裁 E2、不接入运行时、不做批量 atlas、不升格 production candidate。
- **真源顺序**：A204 / A208 / A210 → 1920×1080 页面合同 → E 暖灰色调基底 A219 → clean-lowpoly 标杆与支线规范 → E2 组合气质参考。
- **协作链**：现有 UI 改进按 `ux_laoge` 先诊断、`ui_designer` 后冻结资产分类；`clean low-poly weekly` 临时例外不调用旧像素坐标系的 `angus_art_director`。
- **Gate**：所有 class 必须进入机器 inventory；从 E2 直接裁切数必须为 0；首轮只允许 pin + 短签，真实 Godot 回插前禁止扩产。
