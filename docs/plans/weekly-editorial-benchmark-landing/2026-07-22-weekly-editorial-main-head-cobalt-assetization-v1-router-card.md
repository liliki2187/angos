# 发刊编辑主头版钴蓝资产化预演 v1 Router Card

## 目标

验证方案 1 的钴蓝配色和物件语言能否在不改变 `main_head_slot 442×374` 合同的前提下，拆成可由 Godot 原生控件拼装的分层资源。

## 真值

- 几何：`design/ui-contracts/weekly-editorial/main_head_slot.json`。
- 运行位置：`[459,276,442,374]`。
- 美术：方案 1 钴蓝风格稿、两张 clean-lowpoly-weekly benchmark 与本轮真实生图源。
- 动态内容：现有 M330 报道图、中文标题、meta 和唯一 `44×44` 换稿按钮。

## 允许范围

- 新增 2× 纸面底图、固定装饰、合法 / 悬停 / 聚焦状态 overlay 和换稿按钮皮肤。
- 新增独立 Godot 捕获脚本和整屏位置合成证据。
- 只写 preflight 目录，不替换正式 asset manifest，不修改正式发刊场景。

## Gate

- 四态根节点始终为 `442×374`、旋转为 `0°`。
- 标题、报道图、meta、换稿按钮在所有状态零漂移。
- 所有视觉 overlay 忽略鼠标输入；只有真实 Button 承担 `44×44` 命中。
- 放回现行整屏合同布局后只改变合同矩形内像素。
- 用户确认前不推广到候选卡或正式 Godot 界面。
