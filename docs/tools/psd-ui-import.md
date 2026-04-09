# PSD UI 导入说明

本项目目前已经建立一条 PSD 到 Godot UI 的验证链路，核心由两部分组成：

1. `Importality`：Godot 插件。它通过外部命令识别 PSD 文件，并把它们当成可导入图像资产。
2. 项目本地 Python 脚本：负责将 PSD 扁平化，并把可见图层导出为生成式 `Control` + `TextureRect` 场景。

## 为什么选择这条路径

旧版 Godot PSD 导入器（资产库条目 `555`）已经失效，只支持 Godot `3.2`，而且仅限 Windows。
`Importality` 是 Godot `4.x` 下目前仍可行的路径，它支持通过 CLI 工具把其他图形格式导入为常规图片资源。

参考来源：

- https://godotengine.org/asset-library/asset/555
- https://godotengine.org/asset-library/asset/2025
- https://github.com/nklbdev/godot-4-importality

## 已新增内容

- `gd_project/addons/nklbdev.importality`
- `scripts/import/psd_to_png.py`
- `scripts/import/psd_to_godot_ui.py`
- `scripts/import/configure_importality_psd.py`
- `gd_project/Assets/ui/psd_samples/golden_ui/source/golden_ui.psd`
- `gd_project/Assets/ui/psd_samples/golden_ui/generated/...`
- `gd_project/scenes/dev/GoldenUiImportedPreview.tscn`

## 推荐入口

当目标是“把这份 PSD 变成一个可复用的 Godot UI 资产包”时，请使用高层封装脚本：

```powershell
python scripts/import/build_psd_ui_bundle.py path\\to\\mockup.psd
```

默认会生成：

- `gd_project/Assets/ui/imported/<slug>/source/<file>.psd`
- `gd_project/Assets/ui/imported/<slug>/generated/...`
- `gd_project/scenes/ui/imported/<Slug>Ui.tscn`
- `generated/bundle.json`

如果只需要验证输出：

```powershell
python scripts/import/build_psd_ui_bundle.py path\\to\\mockup.psd --mode preview
```

该模式会写入 `gd_project/Assets/ui/psd_samples/<slug>/...` 和 `gd_project/scenes/dev/<Slug>ImportedPreview.tscn`。

## 配置 Godot 编辑器设置

这个插件使用的是 Godot Editor Settings，而不是项目设置，来配置外部转换规则。

运行：

```powershell
python scripts/import/configure_importality_psd.py
```

它会把以下字段写入 `editor_settings-4.3.tres`：

- `importality/temporary_files_directory_path`
- `importality/command_building_rules_for_custom_image_loader`

PSD 规则会指向：

```text
python scripts/import/psd_to_png.py {in_path} {out_path}
```

## 重建一个 PSD UI 场景

```powershell
python scripts/import/psd_to_godot_ui.py `
  gd_project/Assets/ui/psd_samples/golden_ui/source/golden_ui.psd `
  --output-dir gd_project/Assets/ui/psd_samples/golden_ui/generated `
  --scene gd_project/scenes/dev/GoldenUiImportedPreview.tscn `
  --root-name GoldenUiImportedPreview
```

输出内容：

- `preview/<name>_flat.png`：扁平化 PSD 预览图
- `layers/...`：可见栅格图层 PNG
- `manifest.json`：图层层级与边界信息
- `.tscn`：由 `TextureRect` 节点搭建出的 Godot UI 预览场景

## 当前限制

这条链路导入的是“栅格化 UI 美术”，不是“语义化 Godot 控件”。
按钮、文本、容器和主题逻辑都不会从 Photoshop 自动推断出来。
因此应把生成场景视为布局和美术基线，再按需要把关键部分替换成真正的 Godot UI 控件。
