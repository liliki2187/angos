extends Control
class_name WeeklyRunWorldMap

signal filter_pressed(tag)
signal region_pressed(region_id)
signal node_pressed(node_id)

const FILTER_LABELS := {
	"sci": "科学纪实",
	"occult": "神秘玄学",
	"pop": "大众热度",
}

const REGION_POSITIONS := {
	"us": Vector2(0.27, 0.58),
	"east_asia": Vector2(0.74, 0.40),
}

const NODE_POSITIONS := {
	"n51": Vector2(0.24, 0.50),
	"skin": Vector2(0.38, 0.62),
	"temp_ufo": Vector2(0.48, 0.42),
	"hidden_gate": Vector2(0.62, 0.69),
	"harbor_echo": Vector2(0.72, 0.49),
	"mountain_signal": Vector2(0.83, 0.33),
}

const ROUTE_IDS := [
	"n51",
	"skin",
	"temp_ufo",
	"hidden_gate",
	"harbor_echo",
	"mountain_signal",
]

var _regions: Array = []
var _nodes: Array = []
var _filters := {"sci": true, "occult": true, "pop": true}
var _selected_region_id := ""
var _selected_node_id := ""
var _region_hint := ""
var _week := 1
var _remaining_days := 7
var _week_days := 7
var _filter_buttons := {}
var _region_buttons := {}
var _node_buttons := {}

func _ready() -> void:
	clip_contents = true
	mouse_filter = Control.MOUSE_FILTER_PASS
	resized.connect(_layout_dynamic_buttons)

func bind(payload: Dictionary) -> void:
	_regions = payload.get("regions", [])
	_nodes = payload.get("nodes", [])
	_filters = payload.get("filters", {"sci": true, "occult": true, "pop": true})
	_selected_region_id = str(payload.get("selected_region_id", ""))
	_selected_node_id = str(payload.get("selected_node_id", ""))
	_region_hint = str(payload.get("region_hint", ""))
	_week = int(payload.get("week", 1))
	_remaining_days = int(payload.get("remaining_days", 7))
	_week_days = int(payload.get("week_days", 7))
	_rebuild_dynamic_buttons()
	queue_redraw()

func _draw() -> void:
	var map_rect := _map_rect()
	_draw_map_base(map_rect)
	_draw_routes(map_rect)
	_draw_locations(map_rect)
	_draw_overlay_text(map_rect)
	_draw_day_compass(map_rect)

func _map_rect() -> Rect2:
	var margin := Vector2(14.0, 14.0)
	var rect_size := Vector2(maxf(1.0, size.x - margin.x * 2.0), maxf(1.0, size.y - margin.y * 2.0))
	return Rect2(margin, rect_size)

func _draw_map_base(map_rect: Rect2) -> void:
	draw_rect(map_rect, Color(0.24, 0.055, 0.035, 1.0), true)
	draw_rect(Rect2(map_rect.position + Vector2(map_rect.size.x * 0.68, 0.0), Vector2(map_rect.size.x * 0.32, map_rect.size.y)), Color(0.16, 0.075, 0.045, 0.88), true)
	draw_rect(Rect2(map_rect.position, Vector2(map_rect.size.x, 58.0)), Color(0.055, 0.060, 0.055, 0.94), true)
	draw_rect(Rect2(map_rect.position + Vector2(0.0, map_rect.size.y - 52.0), Vector2(map_rect.size.x, 52.0)), Color(0.035, 0.045, 0.045, 0.92), true)
	draw_rect(map_rect, Color(0.82, 0.63, 0.30, 0.80), false, 2.0)
	draw_rect(Rect2(map_rect.position + Vector2(8.0, 8.0), map_rect.size - Vector2(16.0, 16.0)), Color(0.40, 0.29, 0.17, 0.65), false, 1.0)

	var fold_x := map_rect.position.x + map_rect.size.x * 0.70
	draw_line(Vector2(fold_x, map_rect.position.y + 58.0), Vector2(fold_x - 28.0, map_rect.end.y - 52.0), Color(0.06, 0.035, 0.028, 0.52), 3.0)
	draw_line(Vector2(fold_x + 14.0, map_rect.position.y + 58.0), Vector2(fold_x - 18.0, map_rect.end.y - 52.0), Color(0.63, 0.40, 0.18, 0.22), 1.0)

	for x_index in range(7):
		for y_index in range(4):
			var motif_pos := map_rect.position + Vector2(70.0 + x_index * 86.0, 94.0 + y_index * 78.0)
			if motif_pos.x > map_rect.end.x - 40.0 or motif_pos.y > map_rect.end.y - 70.0:
				continue
			_draw_map_motif(motif_pos)

func _draw_map_motif(center: Vector2) -> void:
	var color := Color(0.78, 0.55, 0.25, 0.12)
	draw_circle(center, 3.0, color)
	draw_line(center + Vector2(-8.0, 0.0), center + Vector2(8.0, 0.0), color, 1.0)
	draw_line(center + Vector2(0.0, -8.0), center + Vector2(0.0, 8.0), color, 1.0)
	draw_arc(center, 11.0, 0.0, TAU, 12, color, 1.0)

func _draw_routes(map_rect: Rect2) -> void:
	for index in range(ROUTE_IDS.size() - 1):
		var start := _position_for_node(ROUTE_IDS[index], index, map_rect)
		var end := _position_for_node(ROUTE_IDS[index + 1], index + 1, map_rect)
		_draw_dotted_line(start, end, Color(0.80, 0.69, 0.48, 0.42), 3.0, 9.0, 6.0)

func _draw_dotted_line(start: Vector2, end: Vector2, color: Color, width: float, dash: float, gap: float) -> void:
	var delta := end - start
	var distance := delta.length()
	if distance <= 0.1:
		return
	var direction := delta / distance
	var cursor := 0.0
	while cursor < distance:
		var segment_end := minf(cursor + dash, distance)
		draw_line(start + direction * cursor, start + direction * segment_end, color, width)
		cursor += dash + gap

func _draw_locations(map_rect: Rect2) -> void:
	for index in range(_nodes.size()):
		var node := _nodes[index] as Dictionary
		var node_id := str(node.get("id", ""))
		var position := _position_for_node(node_id, index, map_rect)
		var accent := _accent_for_type(str(node.get("type", "")))
		var selected := _selected_node_id == node_id
		var dispatch_enabled := bool(node.get("enabled", false))
		_draw_location_marker(position, accent, selected, dispatch_enabled)

func _draw_location_marker(position: Vector2, accent: Color, selected: bool, dispatch_enabled: bool) -> void:
	var base_color := accent
	if not dispatch_enabled:
		base_color = accent.darkened(0.42)
	var radius := 10.0 if selected else 7.0
	draw_circle(position + Vector2(0.0, 4.0), radius + 4.0, Color(0.02, 0.02, 0.018, 0.62))
	draw_circle(position, radius + 4.0, Color(0.86, 0.66, 0.26, 0.45))
	draw_circle(position, radius, base_color)
	draw_rect(Rect2(position + Vector2(-16.0, -31.0), Vector2(32.0, 16.0)), Color(0.05, 0.10, 0.11, 0.82), true)
	draw_rect(Rect2(position + Vector2(-10.0, -42.0), Vector2(20.0, 12.0)), Color(0.07, 0.13, 0.14, 0.78), true)
	draw_line(position + Vector2(-22.0, -15.0), position + Vector2(22.0, -15.0), Color(0.74, 0.52, 0.22, 0.45), 2.0)
	if selected:
		draw_arc(position, radius + 10.0, 0.0, TAU, 48, Color(0.96, 0.82, 0.42, 0.92), 2.0)

func _draw_overlay_text(map_rect: Rect2) -> void:
	var font := get_theme_default_font()
	var title_color := Color(0.94, 0.82, 0.56, 1.0)
	var body_color := Color(0.79, 0.72, 0.58, 0.94)
	draw_string(font, map_rect.position + Vector2(18.0, 32.0), "世界探索地图", HORIZONTAL_ALIGNMENT_LEFT, -1.0, 20, title_color)
	draw_string(font, map_rect.position + Vector2(190.0, 32.0), "第 %d 周 · 剩余 %d / %d 天" % [_week, _remaining_days, _week_days], HORIZONTAL_ALIGNMENT_LEFT, -1.0, 16, body_color)
	var hint := _region_hint
	if hint.length() > 42:
		hint = hint.substr(0, 42) + "..."
	draw_string(font, map_rect.position + Vector2(18.0, map_rect.size.y - 20.0), hint, HORIZONTAL_ALIGNMENT_LEFT, -1.0, 15, body_color)

func _draw_day_compass(map_rect: Rect2) -> void:
	var center := map_rect.end - Vector2(74.0, 74.0)
	draw_circle(center, 48.0, Color(0.035, 0.050, 0.046, 0.88))
	draw_circle(center, 40.0, Color(0.68, 0.50, 0.22, 0.35))
	draw_arc(center, 41.0, 0.0, TAU, 56, Color(0.88, 0.69, 0.32, 0.75), 2.0)
	draw_line(center + Vector2(-26.0, 0.0), center + Vector2(26.0, 0.0), Color(0.83, 0.66, 0.33, 0.85), 2.0)
	draw_line(center + Vector2(0.0, -26.0), center + Vector2(0.0, 26.0), Color(0.83, 0.66, 0.33, 0.55), 1.0)
	var font := get_theme_default_font()
	draw_string(font, center + Vector2(-25.0, 6.0), "%d 天" % _remaining_days, HORIZONTAL_ALIGNMENT_CENTER, 50.0, 18, Color(0.96, 0.86, 0.55, 1.0))

func _rebuild_dynamic_buttons() -> void:
	for child in get_children():
		remove_child(child)
		child.queue_free()
	_filter_buttons.clear()
	_region_buttons.clear()
	_node_buttons.clear()
	_build_filter_buttons()
	_build_region_buttons()
	_build_node_buttons()
	_layout_dynamic_buttons()

func _build_filter_buttons() -> void:
	for tag in FILTER_LABELS.keys():
		var button := Button.new()
		button.text = str(FILTER_LABELS[tag])
		button.focus_mode = Control.FOCUS_ALL
		button.z_index = 10
		button.pressed.connect(_on_filter_button_pressed.bind(str(tag)))
		add_child(button)
		_filter_buttons[str(tag)] = button
		_apply_map_button_style(button, bool(_filters.get(str(tag), true)), true, Color(0.86, 0.68, 0.34, 1.0))

func _build_region_buttons() -> void:
	for region in _regions:
		var item := region as Dictionary
		var region_id := str(item.get("id", ""))
		var button := Button.new()
		button.text = str(item.get("name", region_id))
		button.focus_mode = Control.FOCUS_ALL
		button.z_index = 11
		button.disabled = not bool(item.get("enabled", true))
		button.pressed.connect(_on_region_button_pressed.bind(region_id))
		add_child(button)
		_region_buttons[region_id] = button
		_apply_map_button_style(button, _selected_region_id == region_id, not button.disabled, Color(0.57, 0.76, 0.70, 1.0))

func _build_node_buttons() -> void:
	for node in _nodes:
		var item := node as Dictionary
		var node_id := str(item.get("id", ""))
		var label := "%s\n%d 天 · %s" % [str(item.get("name", node_id)), int(item.get("days", 0)), str(item.get("difficulty", ""))]
		var button := Button.new()
		button.text = label
		button.alignment = HORIZONTAL_ALIGNMENT_CENTER
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.focus_mode = Control.FOCUS_ALL
		button.z_index = 12
		button.disabled = not bool(item.get("selectable", true))
		button.pressed.connect(_on_node_button_pressed.bind(node_id))
		add_child(button)
		_node_buttons[node_id] = button
		_apply_map_button_style(button, _selected_node_id == node_id, not button.disabled, _accent_for_type(str(item.get("type", ""))))

func _layout_dynamic_buttons() -> void:
	var map_rect := _map_rect()
	var filter_size := Vector2(104.0, 30.0)
	var filter_x := map_rect.position.x + 18.0
	for tag in FILTER_LABELS.keys():
		if not _filter_buttons.has(str(tag)):
			continue
		var button := _filter_buttons[str(tag)] as Button
		button.custom_minimum_size = filter_size
		button.size = filter_size
		button.position = Vector2(filter_x, map_rect.position.y + 48.0)
		filter_x += filter_size.x + 8.0

	var region_size := Vector2(minf(maxf(size.x * 0.22, 132.0), 190.0), 34.0)
	for index in range(_regions.size()):
		var item := _regions[index] as Dictionary
		var region_id := str(item.get("id", ""))
		if not _region_buttons.has(region_id):
			continue
		var button := _region_buttons[region_id] as Button
		var local_position := _position_for_region(region_id, index, map_rect)
		button.custom_minimum_size = region_size
		button.size = region_size
		button.position = local_position - region_size * 0.5 + Vector2(0.0, 36.0)

	var node_size := Vector2(minf(maxf(size.x * 0.20, 122.0), 180.0), 44.0)
	for index in range(_nodes.size()):
		var item := _nodes[index] as Dictionary
		var node_id := str(item.get("id", ""))
		if not _node_buttons.has(node_id):
			continue
		var button := _node_buttons[node_id] as Button
		var local_position := _position_for_node(node_id, index, map_rect)
		button.custom_minimum_size = node_size
		button.size = node_size
		button.position = local_position - node_size * 0.5 + Vector2(0.0, 44.0)

func _position_for_region(region_id: String, index: int, map_rect: Rect2) -> Vector2:
	var normalized: Vector2 = REGION_POSITIONS.get(region_id, Vector2(0.24 + float(index) * 0.28, 0.58)) as Vector2
	return map_rect.position + Vector2(map_rect.size.x * normalized.x, map_rect.size.y * normalized.y)

func _position_for_node(node_id: String, index: int, map_rect: Rect2) -> Vector2:
	var fallback := Vector2(0.18 + float(index % 4) * 0.18, 0.35 + float(index / 4) * 0.22)
	var normalized: Vector2 = NODE_POSITIONS.get(node_id, fallback) as Vector2
	return map_rect.position + Vector2(map_rect.size.x * normalized.x, map_rect.size.y * normalized.y)

func _accent_for_type(type_id: String) -> Color:
	match type_id:
		"sci":
			return Color(0.46, 0.76, 0.84, 1.0)
		"occult":
			return Color(0.70, 0.56, 0.88, 1.0)
		"pop":
			return Color(0.88, 0.64, 0.34, 1.0)
		_:
			return Color(0.82, 0.70, 0.42, 1.0)

func _apply_map_button_style(button: Button, selected: bool, enabled: bool, accent: Color) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.045, 0.055, 0.050, 0.92)
	normal.border_color = accent.darkened(0.22)
	if selected:
		normal.bg_color = Color(0.24, 0.17, 0.08, 0.96)
		normal.border_color = Color(0.96, 0.78, 0.34, 1.0)
	if not enabled:
		normal.bg_color = Color(0.045, 0.045, 0.042, 0.78)
		normal.border_color = Color(0.28, 0.26, 0.22, 0.72)
	normal.set_border_width_all(1)
	normal.corner_radius_top_left = 9
	normal.corner_radius_top_right = 9
	normal.corner_radius_bottom_left = 9
	normal.corner_radius_bottom_right = 9
	normal.content_margin_left = 8
	normal.content_margin_right = 8
	normal.content_margin_top = 5
	normal.content_margin_bottom = 5
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", normal.duplicate())
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.95, 0.87, 0.66, 1.0) if selected else Color(0.86, 0.78, 0.60, 1.0)
	if not enabled:
		font_color = Color(0.52, 0.50, 0.44, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color.lightened(0.08))
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)

func _on_filter_button_pressed(tag: String) -> void:
	filter_pressed.emit(tag)

func _on_region_button_pressed(region_id: String) -> void:
	region_pressed.emit(region_id)

func _on_node_button_pressed(node_id: String) -> void:
	node_pressed.emit(node_id)
