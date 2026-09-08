extends Button

signal region_activated(region_id: String)
signal locked_region_activated(region_id: String)

const AbstractImageScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedAbstractImage.gd")
const PAPER := Color("eee8d7")
const PAPER_DIM := Color("d3d2c4")
const INK := Color("17252b")
const MUTED := Color("596469")
const COBALT := Color("356783")
const OLIVE := Color("70795b")
const RUST := Color("9a4a36")
const LOCKED := Color("777f76")
const PAPER_WARM_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_warm_ivory_512.png")
const PAPER_LOCKED_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_cool_locked_512.png")
const PAPER_STEEL_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_steel_blue_512.png")
const PAPER_OLIVE_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_olive_ticket_512.png")

var region_id := ""
var display_name := ""
var status_text := ""
var secondary_text := ""
var thumbnail_variant := "north_america"
var paper_offset := 0.0
var is_selected := false
var is_locked := false
var has_warning := false
var disabled_feedback := false
var _hovered := false
var _font: Font
var _content_root: Control
var _number_label: Label
var _title_label: Label
var _state_label: Label
var _availability_label: Label
var _secondary_label: Label
var _thumbnail: Control


func configure(data: Dictionary, font: Font, next_paper_offset: float = 0.0) -> void:
	region_id = str(data.get("region_id", ""))
	display_name = str(data.get("display_name", ""))
	status_text = str(data.get("status_text", ""))
	secondary_text = str(data.get("secondary_text", ""))
	thumbnail_variant = str(data.get("thumbnail_variant", region_id))
	is_locked = bool(data.get("locked", false))
	has_warning = bool(data.get("warning", false))
	paper_offset = next_paper_offset
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
	clip_contents = false
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
	_build_children()
	_apply_content()


func _build_children() -> void:
	_content_root = Control.new()
	_content_root.name = "PaperContent"
	_content_root.position = Vector2(paper_offset, 0)
	_content_root.size = Vector2(size.x - paper_offset, size.y)
	_content_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_content_root)

	_thumbnail = AbstractImageScript.new()
	_thumbnail.name = "Thumbnail"
	_thumbnail.position = Vector2(16, 56)
	_thumbnail.size = Vector2(138, 88)
	_thumbnail.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_content_root.add_child(_thumbnail)

	_number_label = _make_label("IndexNumber", Rect2(42, 10, 34, 32), 18, INK, true)
	_title_label = _make_label("RegionTitle", Rect2(80, 8, 160, 38), 21, INK, true)
	_state_label = _make_label("SelectionState", Rect2(244, 10, 80, 30), 14, MUTED, true)
	_state_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_availability_label = _make_label("Availability", Rect2(168, 58, 156, 24), 15, MUTED, true)
	_secondary_label = _make_label("Secondary", Rect2(168, 84, 156, 62), 14, MUTED, false)
	_secondary_label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_secondary_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART


func _apply_content() -> void:
	if not is_instance_valid(_title_label):
		return
	var number_text: String = str({"north_america": "01", "east_asia": "02", "pacific": "03"}.get(region_id, "--"))
	_number_label.text = number_text
	_title_label.text = display_name
	_state_label.text = "锁定" if is_locked else ("已选择" if is_selected else "可用")
	_availability_label.text = "暂不可进入" if is_locked else "可进入"
	_secondary_label.text = secondary_text
	var main_color := LOCKED if is_locked else INK
	_number_label.add_theme_color_override("font_color", COBALT if is_selected else (LOCKED if is_locked else OLIVE))
	_title_label.add_theme_color_override("font_color", main_color)
	_state_label.add_theme_color_override("font_color", PAPER if is_locked or is_selected else MUTED)
	_availability_label.add_theme_color_override("font_color", LOCKED if is_locked else COBALT)
	_secondary_label.add_theme_color_override("font_color", RUST if has_warning or disabled_feedback else (LOCKED if is_locked else MUTED))
	_thumbnail.configure(thumbnail_variant, is_locked)


func _draw() -> void:
	var paper_rect := Rect2(Vector2(paper_offset, 0), Vector2(size.x - paper_offset, size.y))
	var paper := PAPER_DIM if is_locked else PAPER
	var cut := PackedVector2Array([
		paper_rect.position + Vector2(0, 2),
		paper_rect.position + Vector2(paper_rect.size.x - 18, 0),
		paper_rect.position + Vector2(paper_rect.size.x, 18),
		paper_rect.position + Vector2(paper_rect.size.x - 2, paper_rect.size.y),
		paper_rect.position + Vector2(10, paper_rect.size.y - 1),
		paper_rect.position + Vector2(0, paper_rect.size.y - 12),
	])
	if is_selected:
		var backer := PackedVector2Array()
		for point in cut:
			backer.append(point + Vector2(-5, 5))
		draw_polygon(backer, [Color("405e75")])
		draw_texture_rect(PAPER_STEEL_TEXTURE, Rect2(paper_rect.position + Vector2(-5, 5), paper_rect.size), false, Color(1, 1, 1, 0.72))
	elif is_locked:
		var locked_backer := PackedVector2Array()
		var locked_offset := Vector2(-4, 4) if region_id == "east_asia" else Vector2(5, 5)
		for point in cut:
			locked_backer.append(point + locked_offset)
		draw_polygon(locked_backer, [Color("40536a") if region_id == "east_asia" else Color("697252")])
		draw_texture_rect(
			PAPER_STEEL_TEXTURE if region_id == "east_asia" else PAPER_OLIVE_TEXTURE,
			Rect2(paper_rect.position + locked_offset, paper_rect.size),
			false,
			Color(1, 1, 1, 0.58)
		)
	draw_rect(Rect2(paper_rect.position + Vector2(7, 8), paper_rect.size - Vector2(8, 8)), Color(0.01, 0.06, 0.08, 0.28), true)
	draw_polygon(cut, [paper])
	draw_texture_rect(PAPER_LOCKED_TEXTURE if is_locked else PAPER_WARM_TEXTURE, paper_rect, false, Color(1, 1, 1, 0.62))
	draw_polyline(cut, Color(0.16, 0.22, 0.22, 0.48), 1.2, true)
	_draw_hand_eye(paper_rect.position + Vector2(25, 25), COBALT if is_selected else (LOCKED if is_locked else OLIVE))
	draw_rect(Rect2(paper_rect.position + Vector2(13, 53), Vector2(144, 94)), Color("10242d"), true)
	draw_rect(Rect2(paper_rect.position + Vector2(14, 54), Vector2(142, 92)), Color(0.75, 0.77, 0.69, 0.42), false, 1.0)
	if is_selected:
		draw_polygon(PackedVector2Array([
			paper_rect.position + Vector2(paper_rect.size.x - 72, -2),
			paper_rect.position + Vector2(paper_rect.size.x, 2),
			paper_rect.position + Vector2(paper_rect.size.x - 2, 42),
			paper_rect.position + Vector2(paper_rect.size.x - 76, 38),
		]), [Color("405e75")])
	if has_warning:
		var right := paper_rect.end.x
		draw_polygon(PackedVector2Array([Vector2(right - 16, 0), Vector2(right, 0), Vector2(right, 16)]), [RUST])
	if is_locked:
		draw_polygon(PackedVector2Array([
			paper_rect.position + Vector2(paper_rect.size.x - 72, -2),
			paper_rect.position + Vector2(paper_rect.size.x, 2),
			paper_rect.position + Vector2(paper_rect.size.x - 2, 42),
			paper_rect.position + Vector2(paper_rect.size.x - 76, 38),
		]), [Color("747a5c")])
		_draw_paperclip(paper_rect.position + Vector2(paper_rect.size.x - 16, 78))
	if disabled_feedback:
		draw_rect(Rect2(paper_rect.position + Vector2(8, paper_rect.size.y - 8), Vector2(paper_rect.size.x - 16, 5)), RUST, true)
	if _hovered or has_focus():
		draw_line(paper_rect.position + Vector2(168, 51), paper_rect.position + Vector2(322, 51), COBALT if not is_locked else OLIVE, 2.0)


func _draw_hand_eye(center: Vector2, color: Color) -> void:
	var outline := PackedVector2Array([
		center + Vector2(-13, 0), center + Vector2(-7, -7), center + Vector2(1, -9),
		center + Vector2(10, -5), center + Vector2(14, 1), center + Vector2(7, 7),
		center + Vector2(-2, 9), center + Vector2(-10, 5), center + Vector2(-13, 0),
	])
	draw_polyline(outline, color, 3.5, false)
	draw_circle(center + Vector2(1, 0), 4.0, color)


func _draw_paperclip(anchor: Vector2) -> void:
	var wire := Color("6e7068")
	draw_arc(anchor, 8.0, -1.2, 1.9, 16, wire, 2.0)
	draw_line(anchor + Vector2(3, -7), anchor + Vector2(-2, 14), wire, 2.0)


func get_image_contract_snapshot() -> Dictionary:
	return _thumbnail.get_source_contract() if is_instance_valid(_thumbnail) else {}


func _on_pressed() -> void:
	if is_locked:
		locked_region_activated.emit(region_id)
	else:
		region_activated.emit(region_id)


func _make_label(node_name: String, rect: Rect2, font_size: int, color: Color, bold: bool) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("font", _font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	_content_root.add_child(label)
	return label
