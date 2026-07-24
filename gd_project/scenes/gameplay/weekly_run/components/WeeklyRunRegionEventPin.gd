extends Button

signal hover_changed(task_id: String, hovering: bool)

const ManifestV2 = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd")

const INK := Color("17252a")
const DISABLED_TINT := Color(0.70, 0.70, 0.66, 1.0)
const HOVER_FADE_SECONDS := 0.10
const SELECT_FADE_SECONDS := 0.096
const DESELECT_FADE_SECONDS := 0.08
const KIND_ORDER := ["permanent", "chain", "hidden", "temp"]

var task_id := ""
var _kind := "permanent"
var _state := "available"
var _selected := false
var _hovered := false
var _external_hover := false
var _enabled := true
var _map_ratio_x := 0.5
var _caption_left := false
var _visual_tween: Tween

var _pin_shell: TextureRect
var _compound_underlay: TextureRect
var _compound_hover: TextureRect
var _compound_selected: TextureRect
var _compound_focus: TextureRect
var _kind_icon_atlas: Texture2D
var _symbol_icon: TextureRect
var _state_badge_atlas: Texture2D
var _state_badge: TextureRect
var _caption_panel: Control
var _caption_title: Label
var _caption_meta: Label

var _right_hover_atlas: Texture2D
var _left_hover_atlas: Texture2D
var _right_selected_atlas: Texture2D
var _left_selected_atlas: Texture2D
var _right_underlay_atlas: Texture2D
var _left_underlay_atlas: Texture2D
var _right_focus_atlas: Texture2D
var _left_focus_atlas: Texture2D


func _ready() -> void:
	flat = true
	focus_mode = Control.FOCUS_ALL
	add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	custom_minimum_size = Vector2(72.0, 80.0)
	clip_contents = false

	_right_hover_atlas = ManifestV2.load_asset_texture("rt2_task_compound_right_hover_v7")
	_left_hover_atlas = ManifestV2.load_asset_texture("rt2_task_compound_left_hover_v7")
	_right_selected_atlas = ManifestV2.load_asset_texture("rt2_task_compound_right_selected_v7")
	_left_selected_atlas = ManifestV2.load_asset_texture("rt2_task_compound_left_selected_v7")
	_right_underlay_atlas = ManifestV2.load_asset_texture("rt2_task_compound_right_selected_underlay_v7")
	_left_underlay_atlas = ManifestV2.load_asset_texture("rt2_task_compound_left_selected_underlay_v7")
	_right_focus_atlas = ManifestV2.load_asset_texture("rt2_task_compound_right_focus_v7")
	_left_focus_atlas = ManifestV2.load_asset_texture("rt2_task_compound_left_focus_v7")

	_compound_underlay = _make_texture_layer("SelectedArtUnderlay", 0)
	_compound_hover = _make_texture_layer("HoverArtCompound", 1)
	_compound_selected = _make_texture_layer("SelectedArtCompound", 2)
	_compound_focus = _make_texture_layer("FocusArtCompound", 3)

	_pin_shell = TextureRect.new()
	_pin_shell.name = "IdleArtPinShell"
	_pin_shell.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pin_shell.position = Vector2(4.0, 0.0)
	_pin_shell.size = Vector2(64.0, 80.0)
	_pin_shell.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_pin_shell.stretch_mode = TextureRect.STRETCH_SCALE
	_pin_shell.texture = ManifestV2.load_asset_texture("rt2_task_pin_b_closed_v7")
	_pin_shell.z_index = 4
	add_child(_pin_shell)

	_kind_icon_atlas = ManifestV2.load_asset_texture("rt2_task_pin_kind_icons_v3")
	_symbol_icon = TextureRect.new()
	_symbol_icon.name = "RuntimeKindIcon"
	_symbol_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_symbol_icon.position = Vector2(22.0, 14.0)
	_symbol_icon.size = Vector2(28.0, 28.0)
	_symbol_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_symbol_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_symbol_icon.z_index = 5
	add_child(_symbol_icon)

	_state_badge_atlas = ManifestV2.load_asset_texture("rt2_task_state_badges_v7")
	_state_badge = TextureRect.new()
	_state_badge.name = "ArtStateBadge"
	_state_badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_state_badge.position = Vector2(48.0, 4.0)
	_state_badge.size = Vector2(24.0, 24.0)
	_state_badge.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_state_badge.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_state_badge.z_index = 7
	add_child(_state_badge)

	_caption_panel = Control.new()
	_caption_panel.name = "RuntimeCompoundText"
	_caption_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_caption_panel.position = Vector2(78.0, 4.0)
	_caption_panel.size = Vector2(200.0, 72.0)
	_caption_panel.z_index = 6
	add_child(_caption_panel)
	_caption_title = _make_label(_caption_panel, "RuntimeTitle", Rect2(14, 8, 166, 28), 15, INK)
	_caption_meta = _make_label(_caption_panel, "RuntimeMeta", Rect2(14, 36, 166, 22), 12, Color("405157"))

	mouse_entered.connect(_on_mouse_entered)
	mouse_exited.connect(_on_mouse_exited)
	focus_entered.connect(func() -> void: _refresh_visual_state(true, HOVER_FADE_SECONDS))
	focus_exited.connect(func() -> void: _refresh_visual_state(true, HOVER_FADE_SECONDS))
	_refresh_visual_state(false)


func configure(data: Dictionary, selected: bool) -> void:
	task_id = str(data.get("id", ""))
	_kind = _normalized_kind(str(data.get("kind", "permanent")))
	_state = str(data.get("state", "available"))
	_selected = selected
	_enabled = bool(data.get("enabled", true))
	if not _enabled and _state == "available":
		_state = "locked"
	elif str(data.get("tone", "normal")) == "deadline" and _state == "available":
		_state = "urgent"
	_map_ratio_x = clampf(float(data.get("map_pos", {}).get("x", 0.5)), 0.0, 1.0)
	_caption_left = _map_ratio_x > 0.72
	set_meta("task_id", task_id)
	set_meta("source", "payload.nodes")
	disabled = not _enabled
	mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND if _enabled else Control.CURSOR_ARROW

	_symbol_icon.texture = _icon_texture_for_kind(_kind)
	_caption_title.text = str(data.get("name", data.get("label", "未命名任务")))
	_caption_meta.text = "%s · %d天" % [_kind_label(_kind), int(data.get("days", 0))]
	_caption_panel.position.x = -208.0 if _caption_left else 78.0
	_update_compound_textures()
	_update_state_badge()
	_refresh_visual_state(false)


func set_selected(value: bool, animate: bool = true) -> void:
	if _selected == value:
		return
	_selected = value
	var duration := SELECT_FADE_SECONDS if value else DESELECT_FADE_SECONDS
	_refresh_visual_state(animate, duration)


func set_external_hover(value: bool) -> void:
	if _external_hover == value:
		return
	_external_hover = value
	_refresh_visual_state(true, HOVER_FADE_SECONDS)


func is_caption_visible() -> bool:
	return visible and is_instance_valid(_caption_panel) and _caption_panel.visible


func get_caption_rect_in_pin() -> Rect2:
	if not is_instance_valid(_caption_panel):
		return Rect2()
	return Rect2(_caption_panel.position, _caption_panel.size)


func get_selected_visual_alpha() -> float:
	return _compound_selected.modulate.a if is_instance_valid(_compound_selected) else 0.0


func get_compound_orientation() -> String:
	return "left" if _caption_left else "right"


func is_using_assetized_state_badge() -> bool:
	return is_instance_valid(_state_badge) and _state_badge_atlas != null


func _on_mouse_entered() -> void:
	_hovered = true
	hover_changed.emit(task_id, true)
	_refresh_visual_state(true, HOVER_FADE_SECONDS)


func _on_mouse_exited() -> void:
	_hovered = false
	hover_changed.emit(task_id, false)
	_refresh_visual_state(true, HOVER_FADE_SECONDS)


func _refresh_visual_state(animate: bool, duration: float = 0.0) -> void:
	if _caption_panel == null:
		return
	var hover_active := _hovered or _external_hover
	var focus_active := has_focus() and not hover_active and not _selected
	var caption_active := _selected or hover_active or focus_active
	_caption_panel.visible = caption_active
	_caption_panel.modulate = Color.WHITE if _enabled else Color(0.78, 0.78, 0.74, 0.88)
	_symbol_icon.modulate = Color.WHITE if _enabled else Color(0.68, 0.68, 0.64, 0.82)
	_state_badge.modulate = Color.WHITE if _enabled else Color(0.82, 0.82, 0.78, 0.92)
	_set_layer_rgb_tint(DISABLED_TINT if not _enabled else Color.WHITE)

	var pin_alpha := 0.0 if caption_active else 1.0
	var hover_alpha := 1.0 if caption_active and not _selected and not focus_active else 0.0
	var selected_alpha := 1.0 if _selected else 0.0
	var underlay_alpha := selected_alpha
	var focus_alpha := 1.0 if focus_active else 0.0
	_apply_layer_targets(pin_alpha, hover_alpha, selected_alpha, underlay_alpha, focus_alpha, duration if animate else 0.0)
	z_index = 6 if caption_active else 2


func _apply_layer_targets(pin_alpha: float, hover_alpha: float, selected_alpha: float, underlay_alpha: float, focus_alpha: float, duration: float) -> void:
	if is_instance_valid(_visual_tween):
		_visual_tween.kill()
	if duration <= 0.0:
		_set_alpha(_pin_shell, pin_alpha)
		_set_alpha(_compound_hover, hover_alpha)
		_set_alpha(_compound_selected, selected_alpha)
		_set_alpha(_compound_underlay, underlay_alpha)
		_set_alpha(_compound_focus, focus_alpha)
		return
	_visual_tween = create_tween().set_parallel(true).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	_visual_tween.tween_property(_pin_shell, "modulate:a", pin_alpha, duration)
	_visual_tween.tween_property(_compound_hover, "modulate:a", hover_alpha, duration)
	_visual_tween.tween_property(_compound_selected, "modulate:a", selected_alpha, duration)
	_visual_tween.tween_property(_compound_underlay, "modulate:a", underlay_alpha, duration)
	_visual_tween.tween_property(_compound_focus, "modulate:a", focus_alpha, duration)


func _set_layer_rgb_tint(tint: Color) -> void:
	for layer_value in [_pin_shell, _compound_hover, _compound_selected, _compound_underlay, _compound_focus]:
		var layer: TextureRect = layer_value
		var color: Color = layer.modulate
		color.r = tint.r
		color.g = tint.g
		color.b = tint.b
		layer.modulate = color


func _set_alpha(item: CanvasItem, alpha: float) -> void:
	var color := item.modulate
	color.a = clampf(alpha, 0.0, 1.0)
	item.modulate = color


func _update_compound_textures() -> void:
	var index := _kind_index(_kind)
	var frame_width := 840 if _caption_left else 834
	var source_height := 240
	var runtime_size := Vector2(280.0, 80.0) if _caption_left else Vector2(278.0, 80.0)
	var runtime_position := Vector2(-208.0, 0.0) if _caption_left else Vector2.ZERO
	var hover_atlas := _left_hover_atlas if _caption_left else _right_hover_atlas
	var selected_atlas := _left_selected_atlas if _caption_left else _right_selected_atlas
	var underlay_atlas := _left_underlay_atlas if _caption_left else _right_underlay_atlas
	var focus_atlas := _left_focus_atlas if _caption_left else _right_focus_atlas
	for layer_value in [_compound_underlay, _compound_hover, _compound_selected, _compound_focus]:
		var layer: TextureRect = layer_value
		layer.position = runtime_position
		layer.size = runtime_size
	_compound_hover.texture = _atlas_frame(hover_atlas, index, frame_width, source_height)
	_compound_selected.texture = _atlas_frame(selected_atlas, index, frame_width, source_height)
	_compound_underlay.texture = _atlas_frame(underlay_atlas, index, frame_width, source_height)
	_compound_focus.texture = _atlas_frame(focus_atlas, index, frame_width, source_height)


func _update_state_badge() -> void:
	var badge_index := -1
	match _state:
		"assigned":
			badge_index = 0
		"urgent":
			badge_index = 1
		"locked", "disabled":
			badge_index = 2
	_state_badge.visible = badge_index >= 0
	_state_badge.texture = _atlas_frame(_state_badge_atlas, badge_index, 72, 72) if badge_index >= 0 else null


func _make_texture_layer(layer_name: String, z: int) -> TextureRect:
	var layer := TextureRect.new()
	layer.name = layer_name
	layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.position = Vector2.ZERO
	layer.size = Vector2(278.0, 80.0)
	layer.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	layer.stretch_mode = TextureRect.STRETCH_SCALE
	layer.z_index = z
	add_child(layer)
	return layer


func _make_label(parent: Control, label_name: String, rect: Rect2, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.name = label_name
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.position = rect.position
	label.size = rect.size
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	parent.add_child(label)
	return label


func _atlas_frame(source: Texture2D, index: int, frame_width: int, frame_height: int) -> Texture2D:
	if source == null or index < 0:
		return null
	var frame := AtlasTexture.new()
	frame.atlas = source
	frame.region = Rect2(float(index * frame_width), 0.0, float(frame_width), float(frame_height))
	return frame


func _icon_texture_for_kind(kind: String) -> Texture2D:
	return _atlas_frame(_kind_icon_atlas, _kind_index(kind), 84, 84)


func _normalized_kind(kind: String) -> String:
	return kind if kind in KIND_ORDER else "permanent"


func _kind_index(kind: String) -> int:
	var index := KIND_ORDER.find(_normalized_kind(kind))
	return index if index >= 0 else 0


func _kind_label(kind: String) -> String:
	match kind:
		"temp":
			return "限时截稿"
		"chain":
			return "连续追踪"
		"hidden":
			return "灵视异常"
		_:
			return "常驻调查"
