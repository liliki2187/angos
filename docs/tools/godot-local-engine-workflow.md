# Godot 本地工具链工作流

## 目的

把 Angus 的 Godot 运行环境从“依赖外部全局目录”改成“仓库内固定版本工具链”，保证本地开发、smoke test 与 CI 使用同一版本。

## 当前锁定版本

- **引擎**：Godot `4.6.2 stable`
- **包类型**：Standard（非 .NET）
- **目标平台**：Windows x86_64 开发环境

## 官方下载来源

- Windows 下载页：
  - `https://godotengine.org/download/windows/`
- 版本归档页：
  - `https://godotengine.org/download/archive/4.6.2-stable/`
- Windows Standard 包：
  - `https://downloads.godotengine.org/?version=4.6.2&flavor=stable&slug=win64.exe.zip&platform=windows.64`
- Export Templates：
  - `https://downloads.godotengine.org/?version=4.6.2&flavor=stable&slug=export_templates.tpz&platform=templates`

## 项目内目录约定

```text
tools/
  godot/
    README.md
    4.6.2-stable/
      Godot_v4.6.2-stable_win64.exe
      Godot_v4.6.2-stable_win64_console.exe
      export_templates/
        templates/
```

## 安装规则

1. 只下载 **Godot 4.6.2 stable Standard**，不要混用 `.NET` 包。
2. Windows 包下载后直接解压到 `tools/godot/4.6.2-stable/`。
3. Export Templates 解压到 `tools/godot/4.6.2-stable/export_templates/`，保留 Godot 官方自带的 `templates/` 子目录。
4. `tools/godot/` 下的实际二进制与模板文件不纳入 Git；只保留说明文档。

## 运行规则

### 打开编辑器

```powershell
tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64.exe
```

### 运行 smoke test

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_weekly_run_smoke_tests.ps1
```

默认情况下，runner 会优先搜索 `tools/godot/` 下的 `*_console.exe`。

### 安装本地导出模板到 Godot 用户目录

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_repo_local_godot_templates.ps1
```

该脚本会把仓库内 `tools/godot/4.6.2-stable/export_templates/templates/` 的内容复制到：

```text
%APPDATA%\Godot\export_templates\4.6.2.stable\
```

### 显式指定 Godot

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_weekly_run_smoke_tests.ps1 `
  -GodotPath tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe
```

## 禁止事项

- 不要把 `E:\angus\tools\godot-4.3` 这类外部目录继续当作默认运行时真源。
- 不要在项目里同时维持多个“默认 Godot 版本”。
- 不要因为升级到 4.6.2 就重新引入 `Array[Array[String]]` 这类不受支持的嵌套 typed collections。

## 首次运行后的正常副作用

- 第一次用 Godot 4.6.2 打开、导出或扫描项目时，可能会生成一批新的 `.uid` 文件。
- `gd_project/.godot/` 下的缓存、导出中间文件和导入产物会刷新；这些本来就不应进入 Git。
