extends RefCounted
class_name WeeklyRunUiStyle

const WorldMapImagegenManifest := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssetManifest.gd")
const RegionTaskAssetManifest := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskAssetManifest.gd")

const WM_ASSET_DIR := "res://Assets/ui/angus_packaging/world_map/assetized"
const WM_PANEL_LEFT_INDEX := "wm-panel-left-index-v4.png"
const WM_PANEL_RIGHT_DETAIL := "wm-panel-right-detail-v4.png"
const WM_BOTTOM_LOG_STRIP := "wm-bottom-log-strip-v4.png"
const WM_REGION_CARD_RED := "wm-region-strip-red-v4.png"
const WM_REGION_CARD_CYAN := "wm-region-strip-cyan-v4.png"
const WM_REGION_CARD_LOCKED := "wm-region-strip-locked-v4.png"
const WM_TICKET_DEADLINE := "wm-ticket-deadline-v4.png"
const WM_TICKET_CHAIN := "wm-ticket-chain-v4.png"
const WM_CTA_ENTER := "wm-cta-enter-region-v4.png"
const WM_LOG_CHIP_RED := "wm-log-chip-red-v4.png"
const WM_LOG_CHIP_CYAN := "wm-log-chip-cyan-v4.png"
const WM_LOG_CHIP_GOLD := "wm-log-chip-gold-v4.png"
const WM_LOG_CHIP_NEXT := "wm-log-chip-next-v4.png"
const WM_PIN_SYMBOL_RED := "wm-pin-symbol-red-v4.png"
const WM_PIN_SYMBOL_CYAN := "wm-pin-symbol-cyan-v4.png"
const WM_PIN_SYMBOL_GOLD := "wm-pin-symbol-gold-v4.png"
const WM_PIN_SYMBOL_NORMAL := "wm-pin-symbol-normal-v4.png"
const WM_PIN_SYMBOL_LOCKED := "wm-pin-symbol-locked-v4.png"
const REGION_TASK_ASSET_DIR := "res://Assets/ui/angus_packaging/region_task"
const DISPATCH_SIGNOFF_CTA_ATLAS := "res://Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-cta-signoff-atlas.png"

static var _runtime_texture_cache := {}

static func apply_panel_style(panel: Control, bg: Color = Color(0.08, 0.11, 0.16, 0.97), border: Color = Color(0.20, 0.25, 0.31, 1.0), radius: int = 14) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	style.content_margin_left = 12
	style.content_margin_top = 12
	style.content_margin_right = 12
	style.content_margin_bottom = 12
	panel.add_theme_stylebox_override("panel", style)

static func apply_paper_panel_style(panel: Control) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.895, 0.855, 0.775, 1.0)
	style.border_color = Color(0.18, 0.20, 0.16, 1.0)
	style.set_border_width_all(2)
	style.corner_radius_top_left = 3
	style.corner_radius_top_right = 3
	style.corner_radius_bottom_left = 3
	style.corner_radius_bottom_right = 3
	style.content_margin_left = 28
	style.content_margin_top = 26
	style.content_margin_right = 28
	style.content_margin_bottom = 24
	panel.add_theme_stylebox_override("panel", style)

static func apply_texture_panel_style(panel: Control, texture: Texture2D, margin: int = 32, content_margin: int = 18) -> void:
	var style := _make_texture_style(texture, margin, content_margin, content_margin, content_margin, content_margin)
	panel.add_theme_stylebox_override("panel", style)

static func apply_texture_panel_style_as_overlay(panel: Control, texture: Texture2D, margin: int = 32, content_margin: int = 18, tint: Color = Color.WHITE) -> void:
	apply_texture_panel_style(panel, texture, margin, content_margin)
	panel.modulate = tint

static func apply_world_imagegen_panel_style(
	panel: Control,
	asset_id: String,
	texture_margin: int = 24,
	content_left: int = 18,
	content_top: int = 18,
	content_right: int = 18,
	content_bottom: int = 18
) -> bool:
	var texture := WorldMapImagegenManifest.load_asset_texture(asset_id)
	if texture == null:
		return false
	var style := _make_texture_style(texture, texture_margin, content_left, content_top, content_right, content_bottom)
	panel.add_theme_stylebox_override("panel", style)
	return true

static func load_world_imagegen_texture(asset_id: String) -> Texture2D:
	return WorldMapImagegenManifest.load_asset_texture(asset_id)

static func load_world_imagegen_atlas_frame(asset_id: String, frame_id: String) -> Texture2D:
	return WorldMapImagegenManifest.load_asset_frame_texture(asset_id, frame_id)

static func has_world_imagegen_v5_runtime_assets() -> bool:
	var required_assets: Array[String] = [
		"wm_bg_shell",
		"wm_world_board_base",
		"wm_left_index_panel",
		"wm_right_story_folder",
		"wm_bottom_ticker",
		"wm_story_preview_north_america",
	]
	for asset_id in required_assets:
		if load_world_imagegen_texture(asset_id) == null:
			return false
	var required_frames := {
		"wm_region_strip_atlas": ["available", "hover", "selected", "locked", "disabled"],
		"wm_pin_atlas": ["normal", "deadline", "chain", "selected", "locked"],
		"wm_ticket_atlas": ["deadline_red", "chain_cyan", "info_neutral", "locked_gray"],
		"wm_cta_enter_region_atlas": ["normal", "hover", "pressed", "disabled", "focus"],
	}
	for asset_id in required_frames.keys():
		for frame_id in required_frames[asset_id]:
			if load_world_imagegen_atlas_frame(str(asset_id), str(frame_id)) == null:
				return false
	return true

static func load_region_task_asset_texture(asset_id: String) -> Texture2D:
	return RegionTaskAssetManifest.load_asset_texture(asset_id)

static func load_region_task_asset_atlas_frame(asset_id: String, frame_id: String) -> Texture2D:
	return RegionTaskAssetManifest.load_asset_frame_texture(asset_id, frame_id)

static func has_region_task_asset(asset_id: String) -> bool:
	var manifest := RegionTaskAssetManifest.load_manifest()
	return RegionTaskAssetManifest.has_asset(asset_id, manifest)

static func has_region_task_artboard_v3_runtime_assets() -> bool:
	var manifest := RegionTaskAssetManifest.load_manifest()
	if manifest.is_empty():
		return false
	if not RegionTaskAssetManifest.has_asset("rt_artboard_full", manifest):
		return false
	return RegionTaskAssetManifest.asset_runtime_file_exists("rt_artboard_full", manifest)

static func has_region_task_assetized_contract() -> bool:
	var manifest := RegionTaskAssetManifest.load_manifest()
	if manifest.is_empty():
		return false
	var required_assets: Array[String] = [
		"rt_board_shell",
		"rt_map_base_clean",
		"rt_map_route_layer",
		"rt_pin_atlas",
		"rt_pin_label_atlas",
		"rt_task_card_atlas",
		"rt_filter_tab_atlas",
		"rt_detail_sheet_base",
		"rt_cta_dispatch_atlas",
		"rt_advance_day_atlas",
		"rt_hud_strip",
	]
	for asset_id in required_assets:
		if not RegionTaskAssetManifest.has_asset(asset_id, manifest):
			return false
	var required_frames := {
		"rt_pin_atlas": ["normal", "hover", "selected", "locked", "completed", "urgent"],
		"rt_pin_label_atlas": ["hover", "selected", "disabled"],
		"rt_task_card_atlas": ["normal", "hover", "selected", "unavailable", "assigned", "deadline"],
		"rt_filter_tab_atlas": ["default", "hover", "selected", "disabled"],
		"rt_cta_dispatch_atlas": ["default", "hover", "pressed", "disabled", "focus", "loading"],
		"rt_advance_day_atlas": ["default", "hover", "pressed", "disabled", "focus", "confirming"],
	}
	for asset_id in required_frames.keys():
		for frame_id in required_frames[asset_id]:
			if not RegionTaskAssetManifest.has_frame(str(asset_id), str(frame_id), manifest):
				return false
	return true

static func has_region_task_assetized_runtime_assets() -> bool:
	if not has_region_task_assetized_contract():
		return false
	var manifest := RegionTaskAssetManifest.load_manifest()
	for asset in manifest.get("assets", []):
		if typeof(asset) == TYPE_DICTIONARY:
			var asset_id := str(asset.get("id", ""))
			if not RegionTaskAssetManifest.asset_runtime_file_exists(asset_id, manifest):
				return false
	return true

static func apply_region_task_assetized_panel_style(
	panel: Control,
	asset_id: String,
	texture_margin: int = 24,
	content_left: int = 18,
	content_top: int = 18,
	content_right: int = 18,
	content_bottom: int = 18
) -> bool:
	var texture := load_region_task_asset_texture(asset_id)
	if texture == null:
		return false
	panel.add_theme_stylebox_override("panel", _make_texture_style(texture, texture_margin, content_left, content_top, content_right, content_bottom))
	return true

static func apply_region_task_assetized_layout_panel_style(panel: Control, area: String) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.0, 0.0, 0.0, 0.0)
	style.border_color = Color(0.0, 0.0, 0.0, 0.0)
	style.set_border_width_all(0)
	if area == "left":
		style.content_margin_left = 24
		style.content_margin_top = 38
		style.content_margin_right = 24
		style.content_margin_bottom = 18
	elif area == "right":
		style.content_margin_left = 34
		style.content_margin_top = 54
		style.content_margin_right = 34
		style.content_margin_bottom = 54
	else:
		style.content_margin_left = 0
		style.content_margin_top = 0
		style.content_margin_right = 0
		style.content_margin_bottom = 0
	panel.add_theme_stylebox_override("panel", style)

static func apply_region_task_artboard_v3_layout_panel_style(panel: Control, area: String) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.0, 0.0, 0.0, 0.0)
	style.border_color = Color(0.0, 0.0, 0.0, 0.0)
	style.set_border_width_all(0)
	if area == "left":
		style.content_margin_left = 88
		style.content_margin_top = 50
		style.content_margin_right = 34
		style.content_margin_bottom = 18
	elif area == "right":
		style.content_margin_left = 52
		style.content_margin_top = 82
		style.content_margin_right = 54
		style.content_margin_bottom = 76
	else:
		style.content_margin_left = 0
		style.content_margin_top = 0
		style.content_margin_right = 0
		style.content_margin_bottom = 0
	panel.add_theme_stylebox_override("panel", style)

static func _make_region_task_artboard_v3_hotspot_style(
	content_left: int,
	content_top: int,
	content_right: int,
	content_bottom: int,
	highlight: Color = Color(0.0, 0.0, 0.0, 0.0)
) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = highlight
	style.border_color = Color(0.0, 0.0, 0.0, 0.0)
	style.set_border_width_all(0)
	style.content_margin_left = content_left
	style.content_margin_top = content_top
	style.content_margin_right = content_right
	style.content_margin_bottom = content_bottom
	return style

static func apply_region_task_artboard_v3_task_button(button: Button, selected: bool, enabled: bool = true) -> void:
	var normal_highlight := Color(0.0, 0.0, 0.0, 0.0)
	var hover_highlight := Color(0.97, 0.80, 0.42, 0.07) if enabled else Color(0.0, 0.0, 0.0, 0.0)
	var selected_highlight := Color(0.98, 0.72, 0.24, 0.055)
	var normal_style := _make_region_task_artboard_v3_hotspot_style(74, 18, 34, 12, selected_highlight if selected else normal_highlight)
	var hover_style := _make_region_task_artboard_v3_hotspot_style(74, 18, 34, 12, selected_highlight if selected else hover_highlight)
	var pressed_style := _make_region_task_artboard_v3_hotspot_style(74, 20, 34, 10, selected_highlight if enabled else normal_highlight)
	button.add_theme_stylebox_override("normal", normal_style)
	button.add_theme_stylebox_override("hover", hover_style)
	button.add_theme_stylebox_override("pressed", pressed_style)
	button.add_theme_stylebox_override("disabled", normal_style)
	button.add_theme_color_override("font_color", Color(0.10, 0.14, 0.12, 1.0))
	button.add_theme_color_override("font_hover_color", Color(0.07, 0.10, 0.09, 1.0))
	button.add_theme_color_override("font_pressed_color", Color(0.06, 0.09, 0.08, 1.0))
	button.add_theme_color_override("font_disabled_color", Color(0.44, 0.45, 0.40, 1.0))
	button.add_theme_font_size_override("font_size", 15)
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled

static func apply_region_task_artboard_v3_cta_button(button: Button, enabled: bool = true) -> void:
	var normal_style := _make_region_task_artboard_v3_hotspot_style(44, 10, 56, 10)
	var hover_style := _make_region_task_artboard_v3_hotspot_style(44, 10, 56, 10, Color(1.0, 0.88, 0.54, 0.11) if enabled else Color(0.0, 0.0, 0.0, 0.0))
	var pressed_style := _make_region_task_artboard_v3_hotspot_style(44, 12, 56, 8, Color(0.12, 0.02, 0.01, 0.12) if enabled else Color(0.0, 0.0, 0.0, 0.0))
	button.add_theme_stylebox_override("normal", normal_style)
	button.add_theme_stylebox_override("hover", hover_style)
	button.add_theme_stylebox_override("pressed", pressed_style)
	button.add_theme_stylebox_override("disabled", normal_style)
	var font_color := Color(0.98, 0.96, 0.84, 1.0) if enabled else Color(0.74, 0.70, 0.62, 0.92)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_font_size_override("font_size", 18)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.86))
	button.disabled = not enabled

static func apply_region_task_artboard_v3_invisible_hotspot(button: Button, enabled: bool = true) -> void:
	var style := _make_region_task_artboard_v3_hotspot_style(0, 0, 0, 0)
	var hover_style := _make_region_task_artboard_v3_hotspot_style(0, 0, 0, 0, Color(1.0, 0.86, 0.40, 0.08) if enabled else Color(0.0, 0.0, 0.0, 0.0))
	button.add_theme_stylebox_override("normal", style)
	button.add_theme_stylebox_override("hover", hover_style)
	button.add_theme_stylebox_override("pressed", hover_style)
	button.add_theme_stylebox_override("disabled", style)
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled

static func apply_region_task_assetized_task_card_button(button: Button, state: String, enabled: bool = true) -> bool:
	var normal_id := state if state in ["normal", "selected", "unavailable", "assigned", "deadline"] else "normal"
	if not enabled:
		normal_id = "unavailable"
	var normal_texture := load_region_task_asset_atlas_frame("rt_task_card_atlas", normal_id)
	var hover_texture := load_region_task_asset_atlas_frame("rt_task_card_atlas", "hover" if enabled else normal_id)
	var pressed_texture := load_region_task_asset_atlas_frame("rt_task_card_atlas", "selected" if enabled else normal_id)
	if normal_texture == null or hover_texture == null or pressed_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 20, 72, 14, 46, 14))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 20, 72, 14, 46, 14))
	button.add_theme_stylebox_override("pressed", _make_texture_style(pressed_texture, 20, 72, 16, 46, 12))
	button.add_theme_stylebox_override("disabled", _make_texture_style(normal_texture, 20, 72, 14, 46, 14))
	button.add_theme_color_override("font_color", Color(0.12, 0.15, 0.13, 1.0))
	button.add_theme_color_override("font_hover_color", Color(0.09, 0.12, 0.10, 1.0))
	button.add_theme_color_override("font_pressed_color", Color(0.08, 0.11, 0.09, 1.0))
	button.add_theme_color_override("font_disabled_color", Color(0.44, 0.45, 0.40, 1.0))
	button.add_theme_font_size_override("font_size", 14)
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled
	return true

static func apply_region_task_assetized_pin_button(button: Button, selected: bool, enabled: bool, tone: String = "normal") -> bool:
	var normal_id := "normal"
	if not enabled:
		normal_id = "locked"
	elif selected:
		normal_id = "selected"
	elif tone == "deadline":
		normal_id = "urgent"
	elif tone == "chain":
		normal_id = "completed"
	var normal_texture := load_region_task_asset_atlas_frame("rt_pin_atlas", normal_id)
	var hover_texture := load_region_task_asset_atlas_frame("rt_pin_atlas", "hover" if enabled and not selected else normal_id)
	var pressed_texture := load_region_task_asset_atlas_frame("rt_pin_atlas", "selected" if enabled else normal_id)
	if normal_texture == null or hover_texture == null or pressed_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 0, 0, 0, 0, 0))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 0, 0, 0, 0, 0))
	button.add_theme_stylebox_override("pressed", _make_texture_style(pressed_texture, 0, 0, 0, 0, 0))
	button.add_theme_stylebox_override("disabled", _make_texture_style(normal_texture, 0, 0, 0, 0, 0))
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled
	return true

static func apply_region_task_assetized_filter_button(button: Button, selected: bool, enabled: bool = true) -> bool:
	var normal_id := "selected" if selected else "default"
	if not enabled:
		normal_id = "disabled"
	var normal_texture := load_region_task_asset_atlas_frame("rt_filter_tab_atlas", normal_id)
	var hover_texture := load_region_task_asset_atlas_frame("rt_filter_tab_atlas", "hover" if enabled and not selected else normal_id)
	var pressed_texture := load_region_task_asset_atlas_frame("rt_filter_tab_atlas", "selected" if enabled else normal_id)
	if normal_texture == null or hover_texture == null or pressed_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 12, 16, 8, 16, 8))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 12, 16, 8, 16, 8))
	button.add_theme_stylebox_override("pressed", _make_texture_style(pressed_texture, 12, 16, 9, 16, 7))
	button.add_theme_stylebox_override("disabled", _make_texture_style(normal_texture, 12, 16, 8, 16, 8))
	var font_color := Color(0.10, 0.14, 0.12, 1.0) if selected else Color(0.88, 0.93, 0.88, 1.0)
	if not enabled:
		font_color = Color(0.52, 0.54, 0.48, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_font_size_override("font_size", 14)
	button.add_theme_constant_override("outline_size", 0 if selected else 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.86))
	button.disabled = not enabled
	return true

static func apply_region_task_assetized_cta_button(button: Button, enabled: bool = true, loading: bool = false) -> bool:
	var normal_id := "loading" if loading else "default"
	if not enabled:
		normal_id = "disabled"
	var normal_texture := load_region_task_asset_atlas_frame("rt_cta_dispatch_atlas", normal_id)
	var hover_texture := load_region_task_asset_atlas_frame("rt_cta_dispatch_atlas", "hover" if enabled and not loading else normal_id)
	var pressed_texture := load_region_task_asset_atlas_frame("rt_cta_dispatch_atlas", "pressed" if enabled and not loading else normal_id)
	var disabled_texture := load_region_task_asset_atlas_frame("rt_cta_dispatch_atlas", "disabled")
	var focus_texture := load_region_task_asset_atlas_frame("rt_cta_dispatch_atlas", "focus")
	if normal_texture == null or hover_texture == null or pressed_texture == null or disabled_texture == null or focus_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 18, 44, 10, 62, 12))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 18, 44, 10, 62, 12))
	button.add_theme_stylebox_override("pressed", _make_texture_style(pressed_texture, 18, 44, 12, 62, 10))
	button.add_theme_stylebox_override("disabled", _make_texture_style(disabled_texture, 18, 44, 10, 62, 12))
	button.add_theme_stylebox_override("focus", _make_texture_style(focus_texture, 18, 44, 10, 62, 12))
	var font_color := Color(0.98, 0.96, 0.82, 1.0) if enabled else Color(0.70, 0.68, 0.60, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", Color(0.70, 0.68, 0.60, 1.0))
	button.add_theme_font_size_override("font_size", 18)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.88))
	button.disabled = not enabled
	return true

static func apply_world_imagegen_v5_index_panel_style(panel: Control) -> bool:
	return apply_world_imagegen_panel_style(panel, "wm_left_index_panel", 30, 42, 64, 26, 34)

static func apply_world_imagegen_v5_detail_panel_style(panel: Control) -> bool:
	return apply_world_imagegen_panel_style(panel, "wm_right_story_folder", 34, 34, 34, 78, 28)

static func apply_world_imagegen_v5_log_strip_style(panel: Control) -> bool:
	return apply_world_imagegen_panel_style(panel, "wm_bottom_ticker", 24, 18, 14, 18, 14)

static func apply_world_imagegen_v5_cta_button(button: Button, enabled: bool = true) -> bool:
	var normal_texture := load_world_imagegen_atlas_frame("wm_cta_enter_region_atlas", "normal")
	var hover_texture := load_world_imagegen_atlas_frame("wm_cta_enter_region_atlas", "hover")
	var pressed_texture := load_world_imagegen_atlas_frame("wm_cta_enter_region_atlas", "pressed")
	var disabled_texture := load_world_imagegen_atlas_frame("wm_cta_enter_region_atlas", "disabled")
	var focus_texture := load_world_imagegen_atlas_frame("wm_cta_enter_region_atlas", "focus")
	if normal_texture == null or hover_texture == null or pressed_texture == null or disabled_texture == null or focus_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 18, 24, 6, 92, 18))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 18, 24, 6, 92, 18))
	button.add_theme_stylebox_override("pressed", _make_texture_style(pressed_texture, 18, 24, 6, 92, 18))
	button.add_theme_stylebox_override("disabled", _make_texture_style(disabled_texture, 18, 24, 2, 92, 22))
	button.add_theme_stylebox_override("focus", _make_texture_style(focus_texture, 18, 24, 6, 92, 18))
	var disabled_font_color := Color(0.90, 0.87, 0.74, 1.0)
	var font_color := Color(0.98, 0.96, 0.82, 1.0) if enabled else disabled_font_color
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", disabled_font_color)
	button.add_theme_font_size_override("font_size", 18)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.86))
	button.disabled = not enabled
	return true

static func apply_world_imagegen_v5_action_item_style(button: Button, visual_style: String, emphasis: bool, enabled: bool = true) -> bool:
	if not visual_style.begins_with("region_"):
		return false
	var locked_preview := visual_style == "region_locked_file"
	var locked_selected := locked_preview and emphasis
	var normal_id := "available"
	if not enabled:
		normal_id = "locked" if visual_style == "region_locked_file" else "disabled"
	elif emphasis:
		normal_id = "selected"
	var normal_texture := load_world_imagegen_atlas_frame("wm_region_strip_atlas", normal_id)
	var hover_texture := load_world_imagegen_atlas_frame("wm_region_strip_atlas", "hover" if enabled and not emphasis else normal_id)
	var pressed_texture := load_world_imagegen_atlas_frame("wm_region_strip_atlas", "selected" if enabled else normal_id)
	var disabled_texture := load_world_imagegen_atlas_frame("wm_region_strip_atlas", "disabled")
	if normal_texture == null or hover_texture == null or pressed_texture == null or disabled_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 22, 62, 12, 20, 12))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 22, 62, 12, 20, 12))
	button.add_theme_stylebox_override("pressed", _make_texture_style(pressed_texture, 22, 62, 12, 20, 12))
	button.add_theme_stylebox_override("disabled", _make_texture_style(disabled_texture, 22, 62, 12, 20, 12))
	var font_color := Color(0.12, 0.15, 0.14, 1.0)
	if not enabled:
		font_color = Color(0.24, 0.27, 0.23, 1.0)
	if locked_selected:
		font_color = Color(0.20, 0.16, 0.10, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color if locked_selected else Color(0.48, 0.50, 0.45, 1.0))
	button.add_theme_font_size_override("font_size", 14)
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled and not locked_preview
	if locked_selected:
		button.modulate = Color(1.17, 1.08, 0.88, 1.0)
	elif emphasis and enabled:
		button.modulate = Color(1.06, 1.02, 0.92, 1.0)
	else:
		button.modulate = Color.WHITE
	return true

static func apply_world_imagegen_v5_ticket_label_style(label: Label, variant: String) -> bool:
	var frame_id := "info_neutral"
	if variant == "deadline":
		frame_id = "deadline_red"
	elif variant == "chain":
		frame_id = "chain_cyan"
	elif variant == "locked":
		frame_id = "locked_gray"
	var texture := load_world_imagegen_atlas_frame("wm_ticket_atlas", frame_id)
	if texture == null:
		return false
	label.add_theme_stylebox_override("normal", _make_texture_style(texture, 18, 112, 8, 66, 8))
	return true

static func apply_world_imagegen_v5_pin_style(button: Button, selected: bool, enabled: bool, tone: String = "normal") -> bool:
	var preview_locked := tone == "locked"
	var locked_selected := selected and preview_locked
	var frame_id := "normal"
	if not enabled or preview_locked:
		frame_id = "locked"
	elif selected:
		frame_id = "selected"
	elif tone == "deadline":
		frame_id = "deadline"
	elif tone == "chain":
		frame_id = "chain"
	var normal_texture := load_world_imagegen_atlas_frame("wm_pin_atlas", frame_id)
	var hover_texture := load_world_imagegen_atlas_frame("wm_pin_atlas", "selected" if enabled and not preview_locked else frame_id)
	if normal_texture == null or hover_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 0, 0, 0, 0, 0))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 0, 0, 0, 0, 0))
	button.add_theme_stylebox_override("pressed", _make_texture_style(hover_texture, 0, 0, 0, 0, 0))
	button.add_theme_stylebox_override("disabled", _make_texture_style(normal_texture, 0, 0, 0, 0, 0))
	button.add_theme_color_override("font_color", Color(0.98, 0.92, 0.72, 1.0))
	button.add_theme_color_override("font_hover_color", Color(0.98, 0.92, 0.72, 1.0))
	button.add_theme_color_override("font_pressed_color", Color(0.98, 0.92, 0.72, 1.0))
	button.add_theme_color_override("font_disabled_color", Color(0.72, 0.72, 0.64, 0.58))
	button.add_theme_constant_override("outline_size", 0)
	if locked_selected:
		button.modulate = Color(1.25, 1.10, 0.82, 1.0)
	elif selected and enabled:
		button.modulate = Color(1.08, 1.04, 0.92, 1.0)
	else:
		button.modulate = Color.WHITE
	button.disabled = not enabled and not preview_locked
	return true

static func apply_world_index_panel_style(panel: Control) -> void:
	apply_texture_panel_style(panel, load_world_map_texture(WM_PANEL_LEFT_INDEX), 18, 14)

static func apply_world_detail_panel_style(panel: Control) -> void:
	apply_texture_panel_style(panel, load_world_map_texture(WM_PANEL_RIGHT_DETAIL), 24, 18)

static func apply_world_log_strip_style(panel: Control) -> void:
	apply_texture_panel_style(panel, load_world_map_texture(WM_BOTTOM_LOG_STRIP), 18, 14)

static func apply_world_story_ticket_style(label: Label, variant: String) -> void:
	if apply_world_imagegen_v5_ticket_label_style(label, variant):
		return
	var texture := load_world_map_texture(WM_TICKET_CHAIN if variant == "chain" else WM_TICKET_DEADLINE)
	var style := _make_texture_style(texture, 16, 34, 8, 16, 8)
	label.add_theme_stylebox_override("normal", style)

static func apply_world_log_chip_texture_style(label: Label, variant: String) -> void:
	var frame_id := "info_neutral"
	if variant == "deadline":
		frame_id = "deadline_red"
	elif variant == "chain":
		frame_id = "chain_cyan"
	elif variant == "locked":
		frame_id = "locked_gray"
	var imagegen_texture := load_world_imagegen_atlas_frame("wm_ticket_atlas", frame_id)
	if imagegen_texture != null:
		label.add_theme_stylebox_override("normal", _make_texture_style(imagegen_texture, 18, 132, 12, 48, 10))
		return
	var texture := load_world_map_texture(WM_LOG_CHIP_RED)
	if variant == "next":
		texture = load_world_map_texture(WM_LOG_CHIP_NEXT)
	elif variant == "chain":
		texture = load_world_map_texture(WM_LOG_CHIP_CYAN)
	elif variant == "selected":
		texture = load_world_map_texture(WM_LOG_CHIP_GOLD)
	var style := _make_texture_style(texture, 18, 52, 9, 14, 9)
	label.add_theme_stylebox_override("normal", style)

static func apply_world_cta_button(button: Button, enabled: bool = true) -> void:
	var style := _make_texture_style(load_world_map_texture(WM_CTA_ENTER), 18, 18, 9, 18, 9)
	button.add_theme_stylebox_override("normal", style)
	button.add_theme_stylebox_override("hover", style.duplicate())
	button.add_theme_stylebox_override("pressed", style.duplicate())
	button.add_theme_stylebox_override("disabled", style.duplicate())
	var font_color := Color(0.98, 0.96, 0.82, 1.0) if enabled else Color(0.55, 0.60, 0.58, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.86))
	button.disabled = not enabled

static func load_world_map_texture(file_name: String) -> Texture2D:
	var res_path := "%s/%s" % [WM_ASSET_DIR, file_name]
	if _runtime_texture_cache.has(res_path):
		return _runtime_texture_cache[res_path]
	var image := Image.load_from_file(ProjectSettings.globalize_path(res_path))
	if image == null or image.is_empty():
		push_warning("World map runtime asset failed to load: %s" % res_path)
		return null
	var texture := ImageTexture.create_from_image(image)
	_runtime_texture_cache[res_path] = texture
	return texture

static func load_region_task_texture(file_name: String) -> Texture2D:
	var res_path := "%s/%s" % [REGION_TASK_ASSET_DIR, file_name]
	if _runtime_texture_cache.has(res_path):
		return _runtime_texture_cache[res_path]
	var image := Image.load_from_file(ProjectSettings.globalize_path(res_path))
	if image == null or image.is_empty():
		push_warning("Region task runtime asset failed to load: %s" % res_path)
		return null
	var texture := ImageTexture.create_from_image(image)
	_runtime_texture_cache[res_path] = texture
	return texture

static func load_dispatch_signoff_cta_frame(frame_id: String) -> Texture2D:
	var normalized_id := frame_id
	if normalized_id == "stamped":
		normalized_id = "pressed"
	var region := _dispatch_signoff_cta_frame_rect(normalized_id)
	if region.size == Vector2.ZERO:
		normalized_id = "default"
		region = _dispatch_signoff_cta_frame_rect(normalized_id)
	var cache_key := "%s::%s" % [DISPATCH_SIGNOFF_CTA_ATLAS, normalized_id]
	if _runtime_texture_cache.has(cache_key):
		return _runtime_texture_cache[cache_key]
	var atlas := _load_runtime_texture(DISPATCH_SIGNOFF_CTA_ATLAS, "Dispatch signoff CTA atlas")
	if atlas == null:
		return null
	var texture := AtlasTexture.new()
	texture.atlas = atlas
	texture.region = region
	_runtime_texture_cache[cache_key] = texture
	return texture

static func apply_dispatch_signoff_cta_button(button: Button, enabled: bool = true, execute_state: String = "idle") -> bool:
	var state := execute_state
	var normal_id := "default"
	if state == "loading":
		normal_id = "loading"
	elif state == "stamped":
		normal_id = "stamped"
	elif not enabled:
		normal_id = "disabled"
	var normal_texture := load_dispatch_signoff_cta_frame(normal_id)
	var hover_texture := load_dispatch_signoff_cta_frame("hover" if enabled and state == "idle" else normal_id)
	var pressed_texture := load_dispatch_signoff_cta_frame("pressed" if enabled and state == "idle" else normal_id)
	var force_disabled_frame := ["loading", "stamped"].has(state)
	var disabled_texture := load_dispatch_signoff_cta_frame(normal_id if force_disabled_frame else "disabled")
	var focus_texture := load_dispatch_signoff_cta_frame("focus" if enabled and state == "idle" else normal_id)
	if normal_texture == null or hover_texture == null or pressed_texture == null or disabled_texture == null or focus_texture == null:
		return false
	button.add_theme_stylebox_override("normal", _make_texture_style(normal_texture, 18, 16, 8, 16, 10))
	button.add_theme_stylebox_override("hover", _make_texture_style(hover_texture, 18, 16, 8, 16, 10))
	button.add_theme_stylebox_override("pressed", _make_texture_style(pressed_texture, 18, 16, 11, 16, 7))
	button.add_theme_stylebox_override("disabled", _make_texture_style(disabled_texture, 18, 16, 8, 16, 10))
	button.add_theme_stylebox_override("focus", _make_texture_style(focus_texture, 18, 16, 8, 16, 10))
	var font_color := Color(0.98, 0.94, 0.76, 1.0)
	if normal_id == "disabled":
		font_color = Color(0.72, 0.70, 0.62, 1.0)
	elif state == "loading":
		font_color = Color(1.0, 0.90, 0.60, 1.0)
	elif state == "stamped":
		font_color = Color(0.78, 0.95, 0.70, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_font_size_override("font_size", 18)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.88))
	button.disabled = (not enabled) or force_disabled_frame
	return true

static func _dispatch_signoff_cta_frame_rect(frame_id: String) -> Rect2:
	match frame_id:
		"default":
			return Rect2(0, 0, 174, 92)
		"hover":
			return Rect2(174, 0, 174, 92)
		"pressed", "stamped":
			return Rect2(348, 0, 174, 92)
		"disabled":
			return Rect2(522, 0, 174, 92)
		"focus":
			return Rect2(696, 0, 174, 92)
		"loading":
			return Rect2(870, 0, 174, 92)
		_:
			return Rect2()

static func _load_runtime_texture(res_path: String, label: String) -> Texture2D:
	if _runtime_texture_cache.has(res_path):
		return _runtime_texture_cache[res_path]
	var image := Image.load_from_file(ProjectSettings.globalize_path(res_path))
	if image == null or image.is_empty():
		push_warning("%s failed to load: %s" % [label, res_path])
		return null
	var texture := ImageTexture.create_from_image(image)
	_runtime_texture_cache[res_path] = texture
	return texture

static func _make_texture_style(
	texture: Texture2D,
	texture_margin: int,
	content_left: int,
	content_top: int,
	content_right: int,
	content_bottom: int
) -> StyleBoxTexture:
	var style := StyleBoxTexture.new()
	style.texture = texture
	style.texture_margin_left = texture_margin
	style.texture_margin_top = texture_margin
	style.texture_margin_right = texture_margin
	style.texture_margin_bottom = texture_margin
	style.content_margin_left = content_left
	style.content_margin_top = content_top
	style.content_margin_right = content_right
	style.content_margin_bottom = content_bottom
	return style

static func apply_button_style(button: Button, emphasis: bool, enabled: bool = true) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.09, 0.12, 0.18, 1.0)
	normal.border_color = Color(0.28, 0.34, 0.42, 1.0)
	if emphasis:
		normal.bg_color = Color(0.22, 0.18, 0.08, 1.0)
		normal.border_color = Color(0.80, 0.64, 0.33, 1.0)
	normal.set_border_width_all(1)
	normal.corner_radius_top_left = 10
	normal.corner_radius_top_right = 10
	normal.corner_radius_bottom_left = 10
	normal.corner_radius_bottom_right = 10
	normal.content_margin_left = 10
	normal.content_margin_right = 10
	normal.content_margin_top = 8
	normal.content_margin_bottom = 8
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", normal.duplicate())
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.95, 0.96, 0.98, 1.0)
	if emphasis:
		font_color = Color(0.95, 0.88, 0.72, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", Color(0.57, 0.61, 0.67, 1.0))
	button.disabled = not enabled

static func apply_channel_shell_style(panel: Control, emphasis: bool = false) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.020, 0.032, 0.036, 0.72)
	style.border_color = Color(0.17, 0.58, 0.62, 0.34)
	if emphasis:
		style.border_color = Color(0.90, 0.27, 0.20, 0.58)
	style.set_border_width_all(1)
	style.corner_radius_top_left = 3
	style.corner_radius_top_right = 3
	style.corner_radius_bottom_left = 3
	style.corner_radius_bottom_right = 3
	style.content_margin_left = 12
	style.content_margin_top = 10
	style.content_margin_right = 12
	style.content_margin_bottom = 10
	panel.add_theme_stylebox_override("panel", style)

static func apply_wall_map_shell_style(panel: Control) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.0, 0.0, 0.0, 0.0)
	style.border_color = Color(0.0, 0.0, 0.0, 0.0)
	style.set_border_width_all(0)
	style.corner_radius_top_left = 0
	style.corner_radius_top_right = 0
	style.corner_radius_bottom_left = 0
	style.corner_radius_bottom_right = 0
	style.content_margin_left = 0
	style.content_margin_top = 0
	style.content_margin_right = 0
	style.content_margin_bottom = 0
	panel.add_theme_stylebox_override("panel", style)

static func apply_dossier_panel_style(panel: Control, variant: String = "dark") -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.030, 0.044, 0.046, 0.96)
	style.border_color = Color(0.26, 0.70, 0.72, 0.42)
	if variant == "cyan":
		style.bg_color = Color(0.032, 0.052, 0.056, 0.96)
		style.border_color = Color(0.18, 0.65, 0.68, 0.42)
	elif variant == "red":
		style.bg_color = Color(0.064, 0.040, 0.038, 0.96)
		style.border_color = Color(0.84, 0.22, 0.18, 0.58)
	style.set_border_width_all(1)
	style.border_width_top = 3
	style.border_width_left = 3
	style.corner_radius_top_left = 3
	style.corner_radius_top_right = 3
	style.corner_radius_bottom_left = 3
	style.corner_radius_bottom_right = 3
	style.content_margin_left = 14
	style.content_margin_top = 14
	style.content_margin_right = 14
	style.content_margin_bottom = 14
	panel.add_theme_stylebox_override("panel", style)

static func apply_editor_note_panel_style(panel: Control, variant: String = "dark") -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.050, 0.060, 0.052, 0.94)
	style.border_color = Color(0.74, 0.64, 0.38, 0.58)
	if variant == "cyan":
		style.bg_color = Color(0.034, 0.055, 0.058, 0.94)
		style.border_color = Color(0.25, 0.78, 0.82, 0.48)
	elif variant == "red":
		style.bg_color = Color(0.070, 0.038, 0.036, 0.94)
		style.border_color = Color(0.86, 0.24, 0.18, 0.62)
	style.set_border_width_all(1)
	style.border_width_top = 3
	style.border_width_left = 3
	style.corner_radius_top_left = 2
	style.corner_radius_top_right = 2
	style.corner_radius_bottom_left = 2
	style.corner_radius_bottom_right = 2
	style.content_margin_left = 18
	style.content_margin_top = 16
	style.content_margin_right = 18
	style.content_margin_bottom = 16
	panel.add_theme_stylebox_override("panel", style)

static func apply_magazine_clip_panel_style(panel: Control) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.953, 0.925, 0.850, 0.99)
	style.border_color = Color(0.095, 0.115, 0.105, 0.88)
	style.set_border_width_all(1)
	style.border_width_top = 6
	style.border_width_left = 3
	style.corner_radius_top_left = 2
	style.corner_radius_top_right = 2
	style.corner_radius_bottom_left = 2
	style.corner_radius_bottom_right = 2
	style.content_margin_left = 18
	style.content_margin_top = 15
	style.content_margin_right = 18
	style.content_margin_bottom = 16
	style.shadow_color = Color(0.01, 0.015, 0.012, 0.24)
	style.shadow_size = 5
	style.shadow_offset = Vector2(3.0, 3.0)
	panel.add_theme_stylebox_override("panel", style)

static func apply_primary_channel_button(button: Button, enabled: bool = true) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.08, 0.54, 0.61, 1.0)
	normal.border_color = Color(0.94, 0.88, 0.66, 0.86)
	if not enabled:
		normal.bg_color = Color(0.055, 0.070, 0.075, 0.92)
		normal.border_color = Color(0.24, 0.29, 0.30, 0.80)
	normal.set_border_width_all(1)
	normal.border_width_left = 5
	normal.border_width_bottom = 3
	normal.corner_radius_top_left = 3
	normal.corner_radius_top_right = 3
	normal.corner_radius_bottom_left = 3
	normal.corner_radius_bottom_right = 3
	normal.content_margin_left = 12
	normal.content_margin_right = 12
	normal.content_margin_top = 9
	normal.content_margin_bottom = 9
	normal.shadow_color = Color(0.01, 0.015, 0.012, 0.28)
	normal.shadow_size = 4
	normal.shadow_offset = Vector2(3.0, 3.0)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = normal.bg_color.lightened(0.08)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.98, 0.96, 0.82, 1.0) if enabled else Color(0.55, 0.60, 0.58, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.86))
	button.disabled = not enabled

static func apply_region_task_v2_panel_style(panel: Control, area: String) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.0, 0.0, 0.0, 0.0)
	style.border_color = Color(0.0, 0.0, 0.0, 0.0)
	style.set_border_width_all(0)
	style.corner_radius_top_left = 0
	style.corner_radius_top_right = 0
	style.corner_radius_bottom_left = 0
	style.corner_radius_bottom_right = 0
	if area == "left":
		style.content_margin_left = 38
		style.content_margin_top = 0
		style.content_margin_right = 32
		style.content_margin_bottom = 6
	elif area == "right":
		style.content_margin_left = 64
		style.content_margin_top = 96
		style.content_margin_right = 54
		style.content_margin_bottom = 118
	else:
		style.content_margin_left = 0
		style.content_margin_top = 0
		style.content_margin_right = 0
		style.content_margin_bottom = 0
	panel.add_theme_stylebox_override("panel", style)

static func apply_region_task_v2_small_button(button: Button) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.020, 0.040, 0.050, 0.74)
	normal.border_color = Color(0.10, 0.45, 0.50, 0.70)
	normal.set_border_width_all(1)
	normal.border_width_left = 4
	normal.corner_radius_top_left = 3
	normal.corner_radius_top_right = 3
	normal.corner_radius_bottom_left = 3
	normal.corner_radius_bottom_right = 3
	normal.content_margin_left = 12
	normal.content_margin_top = 7
	normal.content_margin_right = 12
	normal.content_margin_bottom = 7
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = Color(0.035, 0.070, 0.080, 0.84)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	button.add_theme_color_override("font_color", Color(0.90, 0.96, 0.88, 1.0))
	button.add_theme_color_override("font_hover_color", Color(0.98, 0.96, 0.82, 1.0))
	button.add_theme_color_override("font_pressed_color", Color(0.90, 0.96, 0.88, 1.0))
	button.add_theme_font_size_override("font_size", 15)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.82))

static func apply_region_task_v2_filter_button(button: Button, selected: bool) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.94, 0.90, 0.80, 0.72) if selected else Color(0.96, 0.93, 0.84, 0.18)
	normal.border_color = Color(0.70, 0.16, 0.12, 0.72) if selected else Color(0.14, 0.18, 0.16, 0.14)
	normal.set_border_width_all(0)
	normal.border_width_bottom = 2 if selected else 1
	normal.corner_radius_top_left = 2
	normal.corner_radius_top_right = 2
	normal.corner_radius_bottom_left = 2
	normal.corner_radius_bottom_right = 2
	normal.content_margin_left = 8
	normal.content_margin_top = 5
	normal.content_margin_right = 8
	normal.content_margin_bottom = 5
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = normal.bg_color.lightened(0.06)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.10, 0.14, 0.13, 1.0) if selected else Color(0.88, 0.94, 0.90, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_font_size_override("font_size", 14)
	button.add_theme_constant_override("outline_size", 0 if selected else 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.86))
	button.disabled = false

static func apply_region_task_v2_anchor_pin_style(button: Button, enabled: bool, tone: String = "normal") -> void:
	var normal := StyleBoxFlat.new()
	var color := Color(0.90, 0.86, 0.72, 0.92)
	var border := Color(0.16, 0.20, 0.18, 0.72)
	if tone == "deadline":
		color = Color(0.86, 0.20, 0.12, 0.94)
		border = Color(0.98, 0.72, 0.52, 0.78)
	elif tone == "chain":
		color = Color(0.08, 0.58, 0.62, 0.92)
		border = Color(0.62, 0.96, 0.96, 0.66)
	if not enabled:
		color = Color(0.42, 0.42, 0.36, 0.72)
		border = Color(0.26, 0.28, 0.25, 0.70)
	normal.bg_color = color
	normal.border_color = border
	normal.set_border_width_all(2)
	normal.corner_radius_top_left = 12
	normal.corner_radius_top_right = 12
	normal.corner_radius_bottom_left = 12
	normal.corner_radius_bottom_right = 12
	normal.shadow_color = Color(0.01, 0.015, 0.012, 0.26)
	normal.shadow_size = 3
	normal.shadow_offset = Vector2(2.0, 2.0)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = normal.bg_color.lightened(0.10)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled

static func apply_region_task_v2_cta_button(button: Button, enabled: bool = true) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.070, 0.170, 0.180, 0.96) if enabled else Color(0.16, 0.13, 0.11, 0.78)
	normal.border_color = Color(0.92, 0.45, 0.22, 0.86) if enabled else Color(0.34, 0.30, 0.26, 0.72)
	normal.set_border_width_all(1)
	normal.border_width_left = 6
	normal.border_width_bottom = 2
	normal.corner_radius_top_left = 3
	normal.corner_radius_top_right = 3
	normal.corner_radius_bottom_left = 3
	normal.corner_radius_bottom_right = 3
	normal.content_margin_left = 18
	normal.content_margin_top = 10
	normal.content_margin_right = 18
	normal.content_margin_bottom = 10
	normal.shadow_color = Color(0.01, 0.015, 0.012, 0.24)
	normal.shadow_size = 4
	normal.shadow_offset = Vector2(3.0, 3.0)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = normal.bg_color.lightened(0.08)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.98, 0.96, 0.82, 1.0) if enabled else Color(0.72, 0.70, 0.62, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_font_size_override("font_size", 18)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.88))
	button.disabled = not enabled

static func apply_region_task_v2_pin_style(button: Button, selected: bool, enabled: bool, tone: String = "normal") -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.96, 0.93, 0.84, 0.92)
	normal.border_color = Color(0.14, 0.18, 0.17, 0.58)
	if tone == "deadline":
		normal.border_color = Color(0.80, 0.12, 0.09, 0.88)
	elif tone == "chain":
		normal.border_color = Color(0.05, 0.52, 0.58, 0.88)
	if selected:
		normal.bg_color = Color(0.98, 0.88, 0.56, 0.96)
		normal.border_color = Color(0.96, 0.55, 0.14, 0.95)
	if not enabled:
		normal.bg_color = Color(0.58, 0.58, 0.52, 0.66)
		normal.border_color = Color(0.36, 0.36, 0.32, 0.64)
	normal.set_border_width_all(1)
	normal.border_width_left = 5
	normal.corner_radius_top_left = 2
	normal.corner_radius_top_right = 2
	normal.corner_radius_bottom_left = 2
	normal.corner_radius_bottom_right = 2
	normal.content_margin_left = 10
	normal.content_margin_top = 7
	normal.content_margin_right = 10
	normal.content_margin_bottom = 7
	normal.shadow_color = Color(0.01, 0.015, 0.012, 0.18)
	normal.shadow_size = 3
	normal.shadow_offset = Vector2(2.0, 2.0)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = normal.bg_color.lightened(0.06)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.10, 0.14, 0.13, 1.0) if enabled else Color(0.36, 0.38, 0.34, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_font_size_override("font_size", 13)
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled

static func apply_map_pin_style(button: Button, selected: bool, enabled: bool, tone: String = "normal") -> void:
	var texture_name := WM_PIN_SYMBOL_NORMAL
	var font := Color(0.98, 0.92, 0.72, 1.0)
	if tone == "deadline":
		texture_name = WM_PIN_SYMBOL_RED
	elif tone == "chain":
		texture_name = WM_PIN_SYMBOL_CYAN
	elif tone == "locked":
		texture_name = WM_PIN_SYMBOL_LOCKED
		font = Color(0.72, 0.72, 0.64, 0.82)
	elif selected:
		texture_name = WM_PIN_SYMBOL_GOLD
	var texture := load_world_map_texture(texture_name)
	var style := _make_texture_style(texture, 0, 0, 0, 0, 0)
	button.add_theme_stylebox_override("normal", style)
	var hover := style.duplicate()
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", style.duplicate())
	button.add_theme_stylebox_override("disabled", style.duplicate())
	button.add_theme_color_override("font_color", font)
	button.add_theme_color_override("font_hover_color", font)
	button.add_theme_color_override("font_pressed_color", font)
	button.add_theme_color_override("font_disabled_color", Color(font.r, font.g, font.b, 0.58))
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.88))
	button.add_theme_font_size_override("font_size", 10)
	button.modulate = Color(1.12, 1.08, 0.95, 1.0) if selected and enabled else Color.WHITE
	button.disabled = not enabled

static func apply_action_item_style(button: Button, visual_style: String, emphasis: bool, enabled: bool = true) -> void:
	if visual_style.begins_with("staff_card"):
		var blocked_full := visual_style == "staff_card_blocked_full"
		var style := StyleBoxFlat.new()
		style.bg_color = Color(0.075, 0.100, 0.108, 0.98)
		style.border_color = Color(0.22, 0.34, 0.36, 1.0)
		if emphasis:
			style.bg_color = Color(0.16, 0.135, 0.072, 0.98)
			style.border_color = Color(0.90, 0.67, 0.30, 1.0)
		elif blocked_full:
			style.bg_color = Color(0.090, 0.082, 0.062, 0.98)
			style.border_color = Color(0.62, 0.42, 0.22, 1.0)
		style.set_border_width_all(1)
		style.corner_radius_top_left = 5
		style.corner_radius_top_right = 5
		style.corner_radius_bottom_left = 5
		style.corner_radius_bottom_right = 5
		style.content_margin_left = 12
		style.content_margin_top = 10
		style.content_margin_right = 12
		style.content_margin_bottom = 10
		button.add_theme_stylebox_override("normal", style)
		var hover := style.duplicate()
		hover.bg_color = style.bg_color.lightened(0.06)
		if blocked_full:
			hover.border_color = Color(0.95, 0.58, 0.30, 1.0)
		var pressed := style.duplicate()
		pressed.bg_color = style.bg_color.darkened(0.08)
		button.add_theme_stylebox_override("hover", hover)
		button.add_theme_stylebox_override("pressed", pressed)
		button.add_theme_stylebox_override("disabled", style.duplicate())
		var color := Color(0.93, 0.91, 0.76, 1.0)
		if emphasis:
			color = Color(1.0, 0.82, 0.46, 1.0)
		elif blocked_full:
			color = Color(0.78, 0.70, 0.54, 1.0)
		button.add_theme_color_override("font_color", color)
		button.add_theme_color_override("font_hover_color", color)
		button.add_theme_color_override("font_pressed_color", color)
		button.add_theme_color_override("font_disabled_color", Color(0.58, 0.60, 0.56, 1.0))
		button.add_theme_constant_override("outline_size", 2)
		button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.85))
		button.disabled = not enabled
		return

	if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"]:
		var texture_name := WM_REGION_CARD_RED
		var font_color := Color(0.92, 0.88, 0.70, 1.0)
		if visual_style == "region_file_cyan":
			texture_name = WM_REGION_CARD_CYAN
		elif visual_style == "region_locked_file":
			texture_name = WM_REGION_CARD_LOCKED
			font_color = Color(0.66, 0.68, 0.62, 1.0)
		if emphasis and visual_style != "region_locked_file":
			font_color = Color(1.0, 0.90, 0.55, 1.0)
		var texture := load_world_map_texture(texture_name)
		var normal := _make_texture_style(texture, 18, 64, 9, 86, 8)
		button.add_theme_stylebox_override("normal", normal)
		button.add_theme_stylebox_override("hover", normal.duplicate())
		button.add_theme_stylebox_override("pressed", normal.duplicate())
		button.add_theme_stylebox_override("disabled", normal.duplicate())
		button.add_theme_color_override("font_color", font_color)
		button.add_theme_color_override("font_hover_color", font_color)
		button.add_theme_color_override("font_pressed_color", font_color)
		button.add_theme_color_override("font_disabled_color", Color(0.56, 0.59, 0.58, 1.0))
		button.add_theme_font_size_override("font_size", 12)
		button.add_theme_constant_override("outline_size", 2)
		button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.88))
		button.disabled = not enabled
		button.modulate = Color(1.12, 1.05, 0.88, 1.0) if emphasis and enabled else Color.WHITE
		return

	var bg := Color(0.10, 0.13, 0.16, 1.0)
	var border := Color(0.26, 0.34, 0.36, 1.0)
	var font_color := Color(0.94, 0.94, 0.86, 1.0)
	var paper_node_style := visual_style in ["node_deadline", "node_chain", "node_file"]
	if visual_style in ["region_file", "region_file_red", "region_file_cyan"]:
		bg = Color(0.953, 0.925, 0.850, 0.99)
		border = Color(0.19, 0.21, 0.18, 0.58)
		font_color = Color(0.14, 0.17, 0.15, 1.0)
	elif visual_style == "region_locked_file":
		bg = Color(0.54, 0.54, 0.49, 0.54)
		border = Color(0.41, 0.39, 0.33, 0.54)
		font_color = Color(0.70, 0.71, 0.65, 1.0)
	elif visual_style == "node_deadline":
		bg = Color(0.960, 0.916, 0.845, 0.99)
		border = Color(0.79, 0.14, 0.10, 0.74)
		font_color = Color(0.16, 0.18, 0.15, 1.0)
	elif visual_style == "node_chain":
		bg = Color(0.905, 0.948, 0.924, 0.99)
		border = Color(0.08, 0.58, 0.64, 0.74)
		font_color = Color(0.13, 0.18, 0.17, 1.0)
	elif visual_style == "node_file":
		bg = Color(0.962, 0.932, 0.850, 0.99)
		border = Color(0.70, 0.55, 0.24, 0.66)
		font_color = Color(0.16, 0.18, 0.15, 1.0)
	if emphasis:
		border = Color(0.86, 0.62, 0.20, 0.82)
		bg = Color(0.980, 0.948, 0.805, 0.99) if visual_style in ["region_file", "region_file_red", "region_file_cyan"] else bg.lightened(0.10)
		if visual_style in ["region_file", "region_file_red", "region_file_cyan"] or paper_node_style:
			font_color = Color(0.12, 0.14, 0.12, 1.0)
		else:
			font_color = Color(1.0, 0.88, 0.48, 1.0)

	var normal := StyleBoxFlat.new()
	normal.bg_color = bg
	normal.border_color = border
	normal.set_border_width_all(1 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] or paper_node_style else 2)
	normal.border_width_left = 7 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] else 6 if paper_node_style else 2
	normal.border_width_top = 2 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] or paper_node_style else normal.border_width_top
	normal.border_width_bottom = 1 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] or paper_node_style else normal.border_width_bottom
	if paper_node_style:
		normal.set_border_width_all(0)
		normal.border_width_left = 6
	if visual_style == "region_file_red":
		normal.border_color = Color(0.62, 0.12, 0.10, 0.76)
	elif visual_style == "region_file_cyan":
		normal.border_color = Color(0.04, 0.48, 0.54, 0.76)
	elif visual_style == "region_locked_file":
		normal.border_color = Color(0.40, 0.34, 0.23, 0.50)
	if emphasis and visual_style in ["region_file", "region_file_red", "region_file_cyan"]:
		normal.border_color = Color(0.78, 0.52, 0.15, 0.80)
	normal.corner_radius_top_left = 3
	normal.corner_radius_top_right = 3
	normal.corner_radius_bottom_left = 3
	normal.corner_radius_bottom_right = 3
	normal.content_margin_left = 66 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] else 18 if paper_node_style else 14
	normal.content_margin_right = 94 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] else 16 if paper_node_style else 12
	normal.content_margin_top = 12 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] else 11 if paper_node_style else 10
	normal.content_margin_bottom = 11 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] else 11 if paper_node_style else 10
	normal.shadow_color = Color(0.01, 0.015, 0.012, 0.18 if visual_style != "region_locked_file" else 0.08)
	normal.shadow_size = 3 if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] or paper_node_style else 0
	normal.shadow_offset = Vector2(3.0, 3.0)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = bg.lightened(0.04)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", Color(0.56, 0.59, 0.58, 1.0))
	if visual_style in ["region_file", "region_file_red", "region_file_cyan", "region_locked_file"] or paper_node_style:
		button.add_theme_font_size_override("font_size", 14 if not paper_node_style else 13)
		button.add_theme_constant_override("outline_size", 0)
	else:
		button.add_theme_constant_override("outline_size", 1)
		button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.78))
	button.disabled = not enabled

static func apply_region_task_v2_action_item_style(button: Button, visual_style: String, emphasis: bool, enabled: bool = true) -> bool:
	if not visual_style.begins_with("node_"):
		return false
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.98, 0.95, 0.86, 0.04)
	normal.border_color = Color(0.0, 0.0, 0.0, 0.0)
	if emphasis:
		normal.bg_color = Color(0.98, 0.88, 0.54, 0.18)
		normal.border_color = Color(0.96, 0.56, 0.14, 0.68)
	elif visual_style == "node_deadline":
		normal.border_color = Color(0.78, 0.10, 0.07, 0.34)
	elif visual_style == "node_chain":
		normal.border_color = Color(0.04, 0.50, 0.56, 0.34)
	normal.set_border_width_all(0)
	normal.border_width_left = 4 if emphasis or visual_style != "node_file" else 0
	normal.corner_radius_top_left = 2
	normal.corner_radius_top_right = 2
	normal.corner_radius_bottom_left = 2
	normal.corner_radius_bottom_right = 2
	normal.content_margin_left = 24
	normal.content_margin_top = 15
	normal.content_margin_right = 56
	normal.content_margin_bottom = 12
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = normal.bg_color.lightened(0.05)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.11, 0.15, 0.13, 1.0) if enabled else Color(0.50, 0.52, 0.47, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_font_size_override("font_size", 14)
	button.add_theme_constant_override("outline_size", 0)
	button.disabled = not enabled
	return true
