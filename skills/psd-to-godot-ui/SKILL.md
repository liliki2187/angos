---
name: psd-to-godot-ui
description: "分析 PSD 导入 Godot 的可行性，或在用户要求时生成图层 PNG、布局场景与元数据。区分只读诊断、隔离预览和可复用导入，不自动接入正式游戏。"
---

# PSD 转 Godot UI

这条工具链生成栅格布局骨架，不会自动识别语义按钮、动态 Label、容器或业务逻辑。不能把导出的 TextureRect 场景称为已实现完整交互。

## 按请求执行

- 可行性/工作量分析：只读 PSD 结构、相关脚本与既有结果。不要运行会复制 PSD、改编辑器设置或生成场景的包装器。
- 用户要求验证导入：使用隔离 `preview` 输出，先检查目标是否已存在；默认传 `--skip-configure-editor`，需要修改编辑器设置时单独说明。
- 用户要求可复用导入：使用 `reusable`，生成源 PSD 副本、图层 PNG、flattened preview、manifest、bundle.json 与 Control 根场景。仍不自动修改主游戏场景。

当前包装器：
`python scripts/import/build_psd_ui_bundle.py "<PSD>" --mode preview --skip-configure-editor`

可复用导入将 mode 改为 `reusable`。参数与低层工具细节以 `scripts/import/build_psd_ui_bundle.py` 及 `docs/tools/psd-ui-import.md` 为准，需要调试或改约定时再读取。

## 验证和交付

读取实际生成的 bundle.json，核对资源路径、层级、透明、布局与预览；说明哪些仍是栅格、哪些需要真实文字/输入接线。给用户可用的场景和预览位置，不只说“成功”。

默认输出位于 `gd_project/Assets/ui/psd_samples/` 或 `gd_project/Assets/ui/imported/`，场景位于 `gd_project/scenes/dev/` 或 `gd_project/scenes/ui/imported/`；目标存在先核对归属，不能覆盖用户改动。只有用户要求集成才改具体游戏场景，保留独立资源与可恢复边界。
