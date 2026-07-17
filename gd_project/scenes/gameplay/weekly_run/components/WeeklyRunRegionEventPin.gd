extends Button

signal hover_changed(task_id: String, hovering: bool)

const ManifestV2 = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd")

const INK := Color("17252a")
const PAPER := Color("e8dfc8")
const PAPER_LIGHT := Color("f2ead6")
const OLIVE := Color("87964f")
const RUST := Color("ad4f36")
const TEAL := Color("34767a")
const MUTED := Color("8c8a79")

var task_id := ""
var _tone := "normal"
var _state := "available"
var _selected := false
var _hovered := false
var _external_hover := false
var _enabled := true
var _map_ratio_x := 0.5
var _pin_shell: TextureRect
var _kind_icon_atlas: Texture2D
var _symbol_icon: TextureRect
var _state_tab: Polygon2D
var _state_mark_primary: Line2D
var _state_mark_secondary: Line2D
var _caption_panel: Control
var _caption_texture: TextureRect
var _caption_state_spine: Polygon2D
var _caption_title: Label
var _caption_meta: Label
var _disabled_slash: Line2D

func _ready() -> void:
	flat = true
	focus_mode = Control.FOCUS_ALL
	add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	custom_minimum_size = Vector2(72.0, 80.0)
	clip_contents = false
	_pin_shell = TextureRect.new()
	_pin_shell.name = "GeneratedPinShell"
	_pin_shell.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pin_shell.position = Vector2(4.0, 0.0)
	_pin_shell.size = Vector2(64.0, 80.0)
	_pin_shell.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_pin_shell.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_pin_shell.texture = ManifestV2.load_asset_texture("rt2_task_pin_shell_v2")
	_pin_shell.z_index = 1
	add_child(_pin_shell)

	_kind_icon_atlas = ManifestV2.load_asset_texture("rt2_task_pin_kind_icons_v3")
	_symbol_icon = TextureRect.new()
	_symbol_icon.name = "RuntimeKindIcon"
	_symbol_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_symbol_icon.position = Vector2(22.0, 14.0)
	_symbol_icon.size = Vector2(28.0, 28.0)
	_symbol_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_symbol_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_symbol_icon.z_index = 2
	add_child(_symbol_icon)

	_state_tab = Polygon2D.new()
	_state_tab.name = "RuntimeStateCarrier"
	_state_tab.polygon = PackedVector2Array([
		Vector2(49.0, 7.0), Vector2(67.0, 10.0), Vector2(66.0, 25.0), Vector2(51.0, 22.0),
	])
	_state_tab.z_index = 5
	add_child(_state_tab)
	_state_mark_primary = _make_state_line("RuntimeStateMarkPrimary")
	_state_mark_secondary = _make_state_line("RuntimeStateMarkSecondary")

	_disabled_slash = Line2D.new()
	_disabled_slash.name = "RuntimeDisabledSlash"
	_disabled_slash.points = PackedVector2Array([Vector2(18, 18), Vector2(54, 46)])
	_disabled_slash.width = 4.0
	_disabled_slash.default_color = Color("6e5f58")
	_disabled_slash.antialiased = true
	_disabled_slash.z_index = 3
	add_child(_disabled_slash)

	_caption_panel = Control.new()
	_caption_panel.name = "GeneratedShortLabel"
	_caption_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_caption_panel.position = Vector2(78.0, 4.0)
	_caption_panel.size = Vector2(200.0, 72.0)
	_caption_panel.z_index = 4
	add_child(_caption_panel)
	_caption_texture = TextureRect.new()
	_caption_texture.name = "GeneratedShortLabelTexture"
	_caption_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_caption_texture.size = Vector2(200.0, 72.0)
	_caption_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_caption_texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_caption_texture.texture = ManifestV2.load_asset_texture("rt2_task_pin_label_v2")
	_caption_panel.add_child(_caption_texture)
	_caption_state_spine = Polygon2D.new()
	_caption_state_spine.name = "RuntimeLabelStateSpine"
	_caption_state_spine.polygon = PackedVector2Array([
		Vector2(180.0, 10.0), Vector2(197.0, 15.0), Vector2(197.0, 57.0), Vector2(182.0, 62.0),
	])
	_caption_state_spine.z_index = 1
	_caption_panel.add_child(_caption_state_spine)
	_caption_title = Label.new()
	_caption_title.name = "RuntimeTitle"
	_caption_title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_caption_title.position = Vector2(14.0, 8.0)
	_caption_title.size = Vector2(166.0, 28.0)
	_caption_title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	_caption_title.add_theme_font_size_override("font_size", 15)
	_caption_title.add_theme_color_override("font_color", INK)
	_caption_title.z_index = 2
	_caption_panel.add_child(_caption_title)
	_caption_meta = Label.new()
	_caption_meta.name = "RuntimeMeta"
	_caption_meta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_caption_meta.position = Vector2(14.0, 36.0)
	_caption_meta.size = Vector2(166.0, 22.0)
	_caption_meta.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	_caption_meta.add_theme_font_size_override("font_size", 12)
	_caption_meta.add_theme_color_override("font_color", Color("405157"))
	_caption_meta.z_index = 2
	_caption_panel.add_child(_caption_meta)

	mouse_entered.connect(_on_mouse_entered)
	mouse_exited.connect(_on_mouse_exited)
	focus_entered.connect(func() -> void:
		_refresh_visual_state()
	)
	focus_exited.connect(func() -> void:
		_refresh_visual_state()
	)
	_refresh_visual_state()

func configure(data: Dictionary, selected: bool) -> void:
	task_id = str(data.get("id", ""))
	_tone = str(data.get("tone", "normal"))
	_state = str(data.get("state", "available"))
	_selected = selected
	_enabled = bool(data.get("enabled", true))
	if not _enabled and _state == "available":
		_state = "locked"
	elif _tone == "deadline" and _state == "available":
		_state = "urgent"
	_map_ratio_x = clampf(float(data.get("map_pos", {}).get("x", 0.5)), 0.0, 1.0)
	set_meta("task_id", task_id)
	set_meta("source", "payload.nodes")
	disabled = not _enabled
	mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND if _enabled else Control.CURSOR_ARROW
	var kind := str(data.get("kind", "permanent"))
	var kind_label := _kind_label(kind)
	_symbol_icon.texture = _icon_texture_for_kind(kind)
	_caption_title.text = str(data.get("name", data.get("label", "未命名任务")))
	_caption_meta.text = "%s · %d天" % [kind_label, int(data.get("days", 0))]
	_caption_panel.position.x = -208.0 if _map_ratio_x > 0.72 else 78.0
	_disabled_slash.visible = _state == "disabled"
	_update_state_carrier()
	_refresh_visual_state()

func set_selected(value: bool) -> void:
	_selected = value
	_refresh_visual_state()

func set_external_hover(value: bool) -> void:
	_external_hover = value
	_refresh_visual_state()

func is_caption_visible() -> bool:
	return visible and is_instance_valid(_caption_panel) and _caption_panel.visible

func get_caption_rect_in_pin() -> Rect2:
	if not is_instance_valid(_caption_panel):
		return Rect2()
	return Rect2(_caption_panel.position, _caption_panel.size)

func _on_mouse_entered() -> void:
	_hovered = true
	hover_changed.emit(task_id, true)
	_refresh_visual_state()

func _on_mouse_exited() -> void:
	_hovered = false
	hover_changed.emit(task_id, false)
	_refresh_visual_state()

func _refresh_visual_state() -> void:
	if _caption_panel == null:
		return
	var active := _selected or _hovered or _external_hover or has_focus()
	_caption_panel.visible = active
	_caption_panel.modulate = Color.WHITE if _enabled else Color(0.78, 0.78, 0.74, 0.88)
	_pin_shell.modulate = Color.WHITE if _enabled else Color(0.70, 0.70, 0.66, 0.88)
	_symbol_icon.modulate = Color.WHITE if _enabled else Color(0.68, 0.68, 0.64, 0.82)
	_caption_state_spine.color = Color(INK if has_focus() and not (_selected or _hovered or _external_hover) else _accent_color(), 0.94 if _selected or has_focus() else 0.72)
	z_index = 6 if active else 2
	queue_redraw()

func _draw() -> void:
	var hover_active := _hovered or _external_hover
	var accent := _accent_color()
	if _selected:
		var backplate := PackedVector2Array([
			Vector2(6.0, 5.0), Vector2(58.0, 2.0), Vector2(69.0, 13.0), Vector2(66.0, 53.0),
			Vector2(52.0, 64.0), Vector2(14.0, 60.0), Vector2(4.0, 47.0), Vector2(5.0, 16.0),
		])
		draw_colored_polygon(backplate, Color(accent.lightened(0.16), 0.95))
		draw_polyline(PackedVector2Array([backplate[0], backplate[1], backplate[2], backplate[3]]), Color(PAPER_LIGHT, 0.62), 1.2, true)
		draw_arc(Vector2(36.0, 31.0), 32.0, -2.78, -0.72, 14, Color(accent, 0.96), 2.7, true)
	elif hover_active:
		draw_arc(Vector2(36.0, 31.0), 31.0, -2.68, 0.34, 16, Color(accent, 0.92), 2.4, true)
	elif has_focus():
		draw_arc(Vector2(36.0, 31.0), 31.0, -2.70, -1.46, 8, Color(INK, 0.96), 2.4, true)
		draw_arc(Vector2(36.0, 31.0), 31.0, 0.34, 1.48, 8, Color(OLIVE, 0.94), 2.4, true)
		draw_line(Vector2(16.0, 61.0), Vector2(31.0, 64.0), Color(INK, 0.96), 2.2, true)

func _accent_color() -> Color:
	match _tone:
		"deadline":
			return RUST
		"chain":
			return TEAL
		"locked":
			return MUTED
		_:
			return OLIVE

func _make_state_line(line_name: String) -> Line2D:
	var line := Line2D.new()
	line.name = line_name
	line.width = 2.0
	line.default_color = PAPER_LIGHT
	line.antialiased = true
	line.z_index = 6
	add_child(line)
	return line

func _update_state_carrier() -> void:
	var carrier_visible := _state in ["assigned", "urgent", "locked"]
	_state_tab.visible = carrier_visible
	_state_mark_primary.visible = carrier_visible
	_state_mark_secondary.visible = carrier_visible
	_state_mark_primary.points = PackedVector2Array()
	_state_mark_secondary.points = PackedVector2Array()
	match _state:
		"assigned":
			_state_tab.color = TEAL
			_state_mark_primary.points = PackedVector2Array([Vector2(54, 16), Vector2(58, 20), Vector2(65, 11)])
		"urgent":
			_state_tab.color = RUST
			_state_mark_primary.points = PackedVector2Array([Vector2(55, 20), Vector2(59, 10), Vector2(62, 18), Vector2(67, 12)])
			_state_mark_secondary.points = PackedVector2Array([Vector2(64, 22), Vector2(68, 19)])
		"locked":
			_state_tab.color = MUTED
			_state_mark_primary.points = PackedVector2Array([Vector2(55, 16), Vector2(55, 23), Vector2(66, 23), Vector2(66, 16), Vector2(55, 16)])
			_state_mark_secondary.points = PackedVector2Array([Vector2(58, 16), Vector2(58, 11), Vector2(63, 11), Vector2(63, 16)])

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

func _icon_texture_for_kind(kind: String) -> Texture2D:
	if _kind_icon_atlas == null:
		return null
	var atlas_texture := AtlasTexture.new()
	atlas_texture.atlas = _kind_icon_atlas
	atlas_texture.region = Rect2(float(_kind_icon_index(kind) * 84), 0.0, 84.0, 84.0)
	return atlas_texture

func _kind_icon_index(kind: String) -> int:
	match kind:
		"chain":
			return 1
		"hidden":
			return 2
		"temp":
			return 3
		_:
			return 0
