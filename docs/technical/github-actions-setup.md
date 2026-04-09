# GitHub Actions 与 Godot 构建配置指南

## 概述

仓库当前锁定 Godot `4.6.2 stable`，CI 与本地工作流都应围绕这一版本对齐。为了避免第三方容器镜像滞后于官方稳定版，CI 直接从 Godot 官方下载页拉取对应版本的引擎与导出模板。

## 当前真源

- 工作流文件：`.github/workflows/godot-build.yml`
- Godot 项目根：`gd_project/project.godot`
- 本地锁定版本说明：`docs/engine-reference/godot/VERSION.md`
- 本地工具链放置规范：`docs/tools/godot-local-engine-workflow.md`

## 触发条件

- 推送到 `main` 分支
- 向 `main` 发起 Pull Request
- 在 GitHub Actions 页面手动触发

## 当前 CI 版本策略

- **引擎版本**：Godot `4.6.2 stable`
- **下载来源**：Godot 官方 `downloads.godotengine.org`
- **Linux 构建二进制**：`linux.x86_64.zip`
- **导出模板**：`export_templates.tpz`
- **导出目标**：Windows Desktop

## 本地构建

### 前置要求

1. 使用仓库内工具链 `tools/godot/4.6.2-stable/`
2. 确保同版本 export templates 已准备好
3. 不再把外部全局 Godot 目录视为默认真源

### 常用命令

```powershell
# 安装 repo-local export templates
powershell -ExecutionPolicy Bypass -File scripts/install_repo_local_godot_templates.ps1

# Smoke test（默认优先吃仓库内 tools/godot）
powershell -ExecutionPolicy Bypass -File scripts/run_weekly_run_smoke_tests.ps1

# 指定 Godot 可执行文件
powershell -ExecutionPolicy Bypass -File scripts/run_weekly_run_smoke_tests.ps1 `
  -GodotPath tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe
```

如需手工导出：

```powershell
tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe `
  --headless --path gd_project --export-release "Windows Desktop" gd_project/build/release/Angus.exe
```

## 版本升级时要改哪些地方

当项目锁定版本升级时，需要同步检查这些位置：

1. `.github/workflows/godot-build.yml`
2. `docs/technical-preferences.md`
3. `docs/engine-reference/godot/`
4. `docs/tools/godot-local-engine-workflow.md`
5. `scripts/run_weekly_run_smoke_tests.ps1`

## 常见问题

### Q：CI 提示 `Export template not found`

A：先确认 workflow 下载的是与锁定版本完全一致的 `export_templates.tpz`，再确认安装目录版本号与引擎版本一致。

### Q：本地和 CI 用的不是同一版本怎么办

A：视为配置错误。先修版本锁定文档与 workflow，再继续开发。

### Q：为什么不继续依赖外部全局安装

A：因为那会让项目状态依赖机器环境，无法保证 smoke test、导出和他人复现时使用的是同一引擎版本。

## 参考资源

- [Godot 官方下载页](https://godotengine.org/download/windows/)
- [Godot 官方导出文档](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)
