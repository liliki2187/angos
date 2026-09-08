extends Button

signal region_activated(region_id: String)
signal locked_region_activated(region_id: String)

const PAPER := Color("eee8d7")
const COBALT := Color("356783")
const OLIVE := Color("70795b")
const RUST := Color("9a4a36")
const LOCKED := Color("858c81")
const EYE_DEFAULT_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_default_144.png")
const EYE_SELECTED_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_selected_144.png")
const EYE_SELECTED_WARNING_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_selected_warning_144.png")
const EYE_LOCKED_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_locked_144.png")

var region_id := ""
var display_name := ""
var is_selected := false
var is_locked := false
var has_warning := false
var disabled_feedback := false
var core_position := Vector2(28, 38)
var label_rect := Rect2(62, 10, 140, 52)
var _hovered := false
var _font: Font
var _art_texture: TextureRect
var _name_label: Label
var _state_label: Label


func configure(data: Dictionary, font: Font, next_core: Vector2, next_label_rect: Rect2) -> void:
	region_id = str(data.get("region_id", ""))
	display_name = str(data.get("display_name", ""))
	is_locked = bool(data.get("locked", false))
	has_warning = bool(data.get("warning", false))
	core_position = next_core
	label_rect = next_label_rect
	_font = font
	if is_inside_tree():
		_apply_content()
	queue_redraw()


func set_state(selected: bool, warning: bool, blocked: bool = false) -> void:
	is_selected = selected
	has_warning = warning
	disabled_feedback = blocked
	_apply_content()
	queue_redraw()


func _ready() -> void:
	flat = true
	text = ""
	focus_mode = Control.FOCUS_ALL
	mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	for state_name in ["normal", "hover", "pressed", "focus", "disabled"]:
		add_theme_stylebox_override(state_name, StyleBoxEmpty.new())
	pressed.connect(_on_pressed)
	mouse_entered.connect(func() -> void:
		_hovered = true
		queue_redraw()
	)
	mouse_exited.connect(func() -> void:
		_hovered = false
		queue_redraw()
	)
	_art_texture = TextureRect.new()
	_art_texture.name = "BeaconArt"
	_art_texture.position = core_position - Vector2(36, 36)
	_art_texture.size = Vector2(72, 72)
	_art_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_art_texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_art_texture.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	_art_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_art_texture)
	_name_label = _make_label("RegionName", Rect2(label_rect.position, Vector2(label_rect.size.x, 30)), 16)
	_state_label = _make_label("RegionState", Rect2(label_rect.position + Vector2(0, 28), Vector2(label_rect.size.x, 22)), 12)
	_apply_content()


func _apply_content() -> void:
	if not is_instance_valid(_name_label):
		return
	var number_text: String = str({"north_america": "01", "east_asia": "02", "pacific": "03"}.get(region_id, "--"))
	_name_label.text = "%s  %s" % [number_text, display_name]
	_state_label.text = "锁定" if is_locked else ("红线升温" if has_warning else "可进入")
	_name_label.add_theme_color_override("font_color", PAPER if not is_locked else Color("aeb3a8"))
	_state_label.add_theme_color_override("font_color", RUST if has_warning else (LOCKED if is_locked else Color("b9c5bd")))
	if is_instance_valid(_art_texture):
		_art_texture.position = core_position - Vector2(36, 36)
		_art_texture.texture = _resolve_art_texture()


func _draw() -> void:
	var ring := LOCKED if is_locked else (COBALT if is_selected else OLIVE)
	var label_edge_x := label_rect.position.x if label_rect.position.x > core_position.x else label_rect.end.x
	draw_line(core_position + Vector2(26 if label_rect.position.x > core_position.x else -26, 0), Vector2(label_edge_x, core_position.y), Color(ring, 0.48), 1.0)
	if _hovered or has_focus():
		draw_line(Vector2(label_rect.position.x, label_rect.end.y), Vector2(label_rect.end.x, label_rect.end.y), ring, 2.0)
	if disabled_feedback:
		draw_line(Vector2(label_rect.position.x, label_rect.end.y - 2), Vector2(label_rect.end.x, label_rect.end.y - 2), RUST, 4.0)


func get_asset_contract_snapshot() -> Dictionary:
	var active_texture: Texture2D = _art_texture.texture if is_instance_valid(_art_texture) else null
	return {
		"state": _resolve_art_state(),
		"resource_path": active_texture.resource_path if active_texture != null else "",
		"source_size": [active_texture.get_width(), active_texture.get_height()] if active_texture != null else [0, 0],
		"display_size": [72, 72],
		"stretch_mode": _art_texture.stretch_mode if is_instance_valid(_art_texture) else -1,
		"mouse_filter": _art_texture.mouse_filter if is_instance_valid(_art_texture) else -1,
		"programmatic_final_art": false,
	}


func _resolve_art_state() -> String:
	if is_locked:
		return "locked"
	if is_selected and has_warning:
		return "selected_warning"
	if is_selected:
		return "selected"
	return "default"


func _resolve_art_texture() -> Texture2D:
	match _resolve_art_state():
		"locked":
			return EYE_LOCKED_TEXTURE
		"selected_warning":
			return EYE_SELECTED_WARNING_TEXTURE
		"selected":
			return EYE_SELECTED_TEXTURE
		_:
			return EYE_DEFAULT_TEXTURE


func _on_pressed() -> void:
	if is_locked:
		locked_region_activated.emit(region_id)
	else:
		region_activated.emit(region_id)


func _make_label(node_name: String, rect: Rect2, font_size: int) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("font", _font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", PAPER)
	add_child(label)
	return label
