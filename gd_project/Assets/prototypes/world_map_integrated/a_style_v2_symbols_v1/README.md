# 世界地图 A 风格运行时符号包 v1

## 身份

- `runtime_state_preview_symbol_replacement_v1`
- 可见图形全部来自 Codex 内置 ImageGen 的真实位图生成。
- 本地程序只执行色键去背、透明裁边、等比缩放、四象限切片和 manifest 校验，没有重画 UFO、眼睛、纸边、三窗或海平线。

## 资产

- `ufo_note_228x256.png`：无字芥末 UFO 便签，运行时显示 `114×128`；中文由 Godot `Label` 承担。
- `three_window_event_224x84.png`：无字三窗共享海线事件牌，运行时显示 `112×42`，不得承载文字或热区。
- `eye_default_144.png`：默认 open-eye 状态。
- `eye_selected_144.png`：selected 蓝色背纸与不闭合手画圈状态。
- `eye_selected_warning_144.png`：selected 与 warning 叠加状态。
- `eye_locked_144.png`：独立 locked 半闭眼状态，不通过灰度染色生成。
- `world_map_a_symbol_pack_v1_manifest.json`：尺寸、alpha bbox、透明角与 provenance。

## 运行时边界

Godot 继续控制编号、地区名、状态文字、机构细连接线、hover/focus/blocked 反馈、显隐、焦点和 hit rect。Godot 不再用 `draw_polygon / draw_arc / draw_circle / draw_polyline` 绘制品牌符号终稿。

## 源与处理

- 生图源：`image_gen/2026-08-06/world-map-runtime-symbol-pack-v1/sources/`
- 色键去背：`imagegen` 技能自带 `remove_chroma_key.py`
- 派生脚本：`scripts/ui-contracts/wmw/prepare_world_map_a_symbol_pack_v1.py`
- 视觉母体：`image_gen/2026-08-05/world-map-a-style-real-ui-v2-thick-sticker-ink/01-world-map-a-style-real-ui-v2-thick-sticker-ink.png`
