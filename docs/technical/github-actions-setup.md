# GitHub Actions Godot 构建配置指南

## 概述

已配置 GitHub Actions 自动构建 Godot 项目，每次推送到 main 分支会自动触发构建。支持 Linux / Windows / macOS / HTML5 导出。

## CI 工作流

```
.github/workflows/godot-build.yml
```

### 触发条件

- 推送到 `main` 分支（自动）
- 创建 Pull Request 到 `main`（自动）
- 手动触发（Actions 页面 → Run workflow）

### 构建平台

| 选项 | 输出 |
|------|------|
| linux | Angus.x86_64 |
| windows | Angus.exe |
| mac | Angus.zip |
| web | build/web/ |

### 容器镜像

使用 `barichello/godot-ci:4.3`（Godot 4.3 + 导出模板预装）。

## 本地构建

### 前置要求

1. 安装 [Godot 4.3](https://godotengine.org/download)
2. 下载对应的 [Export Templates](https://godotengine.org/download)

### 导出命令

```bash
# Linux
godot --headless --export-release "Linux/X11" build/Angus.x86_64

# Windows
godot --headless --export-release "Windows Desktop" build/Angus.exe

# macOS
godot --headless --export-release "macOS" build/Angus.zip

# HTML5
godot --headless --export-release "HTML5" build/web/index.html
```

或使用脚本：

```bash
chmod +x scripts/release/export.sh
./scripts/release/export.sh "Windows Desktop" build/Angus.exe
```

## 自定义配置

### 修改 Godot 版本

编辑 `.github/workflows/godot-build.yml` 中的：
- `image: barichello/godot-ci:4.3`（CI 容器）
- `Godot_v4.3-stable_export_templates.tpz`（导出模板下载链接）

### 添加新场景

编辑 `project.godot` 中的 `run/main_scene`，或使用 Godot Editor 设置。

### 修改窗口分辨率

编辑 `project.godot` 中的 `[display]` 部分。

## 常见问题

### Q: 构建失败 "Export template not found"
A: 检查 CI 中 export templates 下载链接是否正确

### Q: 本地导出缺少模板
A: Godot Editor → Editor → Manage Export Templates → Download

### Q: 如何添加新导出平台
A: 编辑 `export_presets.cfg` 添加新 preset，同步更新 workflow

## 参考资源

- [Godot 官方文档](https://docs.godotengine.org)
- [Godot CI GitHub Action](https://github.com/barichello/godot-ci)
- [Godot 导出指南](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)
