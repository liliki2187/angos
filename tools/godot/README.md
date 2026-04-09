# Godot 本地工具目录

本目录用于放置 **仓库内固定版本的 Godot 二进制与导出模板**。

- 当前锁定版本：`4.6.2-stable`
- 推荐解压位置：`tools/godot/4.6.2-stable/`
- Export templates 解压后保留 `tools/godot/4.6.2-stable/export_templates/templates/`
- 详细工作流文档：`docs/tools/godot-local-engine-workflow.md`

说明：

- `tools/godot/` 下的实际引擎文件默认不进入 Git。
- 如果需要升级版本，先更新：
  - `docs/engine-reference/godot/`
  - `docs/technical-preferences.md`
  - `docs/tools/godot-local-engine-workflow.md`
  - `.github/workflows/godot-build.yml`
