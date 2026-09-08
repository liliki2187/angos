extends Control

const PAPER := Color("eee8d7")
const PAPER_BACK := Color("c7c3aa")
const INK := Color("17252b")
const MUTED := Color("596468")
const COBALT := Color("356783")
const OLIVE := Color("70795b")
const RUST := Color("9a4a36")
const PAPER_WARM_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_warm_ivory_512.png")

var _font: Font
var _advance_panel: Panel


func configure(font: Font) -> void:
	_font = font


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	focus_mode = Control.FOCUS_NONE
	_build_children()
	_disable_input_tree(self)
	queue_redraw()


func get_state_snapshot() -> Dictionary:
	return {
		"state": "disabled_runtime_unavailable",
		"advance_enabled": false,
		"advance_rect": [16, 72, 340, 94],
		"interactive_button_names": [],
		"root_mouse_filter": mouse_filter,
		"pointer_consuming_descendant_count": _count_pointer_consuming_descendants(self),
		"focusable_descendant_count": _count_focusable_descendants(self),
	}


func _build_children() -> void:
	var kicker := _make_label("ScheduleKicker", Rect2(16, 8, 220, 18), 11, MUTED)
	kicker.text = "GLOBAL SCHEDULE / 全局日程"

	var day := _make_label("CurrentDay", Rect2(16, 28, 156, 34), 23, INK)
	day.text = "当前第 1 天"
	var remaining := _make_label("RemainingDays", Rect2(188, 30, 168, 30), 16, COBALT)
	remaining.text = "剩余 7 天"
	remaining.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT

	_advance_panel = Panel.new()
	_advance_panel.name = "AdvanceDayUnavailable"
	_advance_panel.position = Vector2(16, 72)
	_advance_panel.size = Vector2(340, 94)
	_advance_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_advance_panel.add_theme_stylebox_override("panel", _panel_style(Color("d7d3c3"), Color(OLIVE, 0.45), 1))
	add_child(_advance_panel)

	var icon_plate := Panel.new()
	icon_plate.name = "AdvanceIconPlate"
	icon_plate.position = Vector2(12, 12)
	icon_plate.size = Vector2(70, 70)
	icon_plate.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var icon_style := StyleBoxFlat.new()
	icon_style.bg_color = Color("c9c8ba")
	icon_style.border_color = Color(0.24, 0.29, 0.27, 0.34)
	icon_style.border_width_left = 1
	icon_style.border_width_top = 1
	icon_style.border_width_right = 1
	icon_style.border_width_bottom = 1
	icon_plate.add_theme_stylebox_override("panel", icon_style)
	_advance_panel.add_child(icon_plate)
	var arrow := _make_label_in(icon_plate, "Arrow", Rect2(0, 0, 70, 70), 30, INK)
	arrow.text = "—"
	arrow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

	var action_title := _make_label_in(_advance_panel, "AdvanceTitle", Rect2(100, 12, 220, 34), 19, INK)
	action_title.text = "日程推进暂未开放"
	var action_note := _make_label_in(_advance_panel, "AdvanceNote", Rect2(100, 48, 220, 28), 13, MUTED)
	action_note.text = "当前版本不可操作"

	var consequence := _make_label("CurrentImpact", Rect2(16, 176, 340, 24), 13, INK)
	consequence.text = "当前：无任务到期"
	var zero_day := _make_label("ZeroDayImpact", Rect2(16, 206, 340, 24), 13, RUST)
	zero_day.text = "日程归零：进入编辑部阶段"


func _draw() -> void:
	draw_rect(Rect2(Vector2(6, 6), size - Vector2(2, 2)), Color(0.01, 0.05, 0.07, 0.42), true)
	draw_polygon(PackedVector2Array([
		Vector2(0, 4), Vector2(size.x - 22, 0), Vector2(size.x, 20), Vector2(size.x - 5, size.y), Vector2(7, size.y - 2), Vector2(0, size.y - 18),
	]), [Color("273b43")])
	draw_rect(Rect2(9, 8, 354, 229), PAPER, true)
	draw_texture_rect(PAPER_WARM_TEXTURE, Rect2(9, 8, 354, 229), false, Color(1, 1, 1, 0.68))
	draw_rect(Rect2(9, 8, 354, 229), Color(0.12, 0.18, 0.17, 0.52), false, 1.0)
	draw_rect(Rect2(12, 68, 348, 102), Color(OLIVE, 0.12), true)
	draw_line(Vector2(16, 202), Vector2(356, 202), Color(0.20, 0.27, 0.25, 0.20), 1.0)
	draw_polygon(PackedVector2Array([Vector2(330, 8), Vector2(363, 8), Vector2(363, 40)]), [Color(OLIVE, 0.82)])


func _panel_style(fill: Color, border: Color, width: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = border
	style.border_width_left = width
	style.border_width_top = width
	style.border_width_right = width
	style.border_width_bottom = width
	return style


func _make_label(node_name: String, rect: Rect2, font_size: int, color: Color) -> Label:
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
	add_child(label)
	return label


func _make_label_in(parent: Control, node_name: String, rect: Rect2, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("font", _font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	parent.add_child(label)
	return label


func _disable_input_tree(node: Node) -> void:
	if node is Control:
		var control := node as Control
		control.mouse_filter = Control.MOUSE_FILTER_IGNORE
		control.focus_mode = Control.FOCUS_NONE
	for child in node.get_children():
		_disable_input_tree(child)


func _count_focusable_descendants(node: Node) -> int:
	var count := 0
	for child in node.get_children():
		if child is Control and (child as Control).focus_mode != Control.FOCUS_NONE:
			count += 1
		count += _count_focusable_descendants(child)
	return count


func _count_pointer_consuming_descendants(node: Node) -> int:
	var count := 0
	for child in node.get_children():
		if child is Control and (child as Control).mouse_filter != Control.MOUSE_FILTER_IGNORE:
			count += 1
		count += _count_pointer_consuming_descendants(child)
	return count
