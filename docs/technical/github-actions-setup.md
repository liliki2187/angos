# GitHub Actions 与 Godot 构建配置指南

## 概述

仓库已配置 GitHub Actions 自动构建 Godot 项目。每次推送到 `main` 分支时会自动触发构建，支持 Linux / Windows / macOS / HTML5 导出。

## CI 工作流

```text
.github/workflows/godot-build.yml
```

Godot 项目根目录：

```text
gd_project/project.godot
```

### 触发条件

- 推送到 `main` 分支（自动）
- 向 `main` 发起 Pull Request（自动）
- 手动触发（Actions 页面 -> `Run workflow`）

### 构建平台

| 选项 | 输出 |
|------|------|
| `linux` | `Angus.x86_64` |
| `windows` | `Angus.exe` |
| `mac` | `Angus.zip` |
| `web` | `build/web/` |

### 容器镜像

使用 `barichello/godot-ci:4.3`，其中已预装 Godot 4.3 与导出模板。

## 本地构建

### 前置要求

1. 安装 [Godot 4.3](https://godotengine.org/download)
2. 下载对应的 [Export Templates](https://godotengine.org/download)

### 导出命令

```bash
# Linux
godot --headless --path gd_project --export-release "Linux/X11" build/Angus.x86_64

# Windows
godot --headless --path gd_project --export-release "Windows Desktop" build/Angus.exe

# macOS
godot --headless --path gd_project --export-release "macOS" build/Angus.zip

# HTML5
godot --headless --path gd_project --export-release "HTML5" build/web/index.html
```

也可以使用脚本：

```bash
chmod +x scripts/release/export.sh
./scripts/release/export.sh "Windows Desktop" build/Angus.exe
```

## 自定义配置

### 修改 Godot 版本

编辑 `.github/workflows/godot-build.yml` 中的以下字段：

- `image: barichello/godot-ci:4.3`（CI 容器）
- `Godot_v4.3-stable_export_templates.tpz`（导出模板下载链接）

### 添加新场景

编辑 `gd_project/project.godot` 中的 `run/main_scene`，或直接通过 Godot 编辑器设置。

### 修改窗口分辨率

编辑 `gd_project/project.godot` 中的 `[display]` 部分。

## 常见问题

### Q：构建失败，提示 `Export template not found`

A：检查 CI 中的导出模板下载链接是否正确。

### Q：本地导出提示缺少模板

A：打开 Godot Editor -> Editor -> Manage Export Templates -> Download。

### Q：如何添加新的导出平台？

A：编辑 `gd_project/export_presets.cfg`，添加新的 preset，并同步更新 workflow。

## 参考资源

- [Godot 官方文档](https://docs.godotengine.org)
- [Godot CI GitHub Action](https://github.com/barichello/godot-ci)
- [Godot 导出指南](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)
