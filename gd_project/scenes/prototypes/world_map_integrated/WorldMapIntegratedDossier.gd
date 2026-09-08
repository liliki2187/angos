extends Control

signal mission_intel_toggled(expanded: bool)
signal enter_region_requested(region_id: String)

const AbstractImageScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedAbstractImage.gd")
const PAPER := Color("eee8d7")
const PAPER_BACK := Color("c8c5ad")
const INK := Color("17252b")
const MUTED := Color("596468")
const COBALT := Color("356783")
const OLIVE := Color("70795b")
const RUST := Color("9a4a36")
const PAPER_WARM_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_warm_ivory_512.png")
const PAPER_OLIVE_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_olive_ticket_512.png")
const PAPER_STEEL_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/paper_steel_blue_512.png")

var _font: Font
var _region_id := "north_america"
var _expanded := false
var _title_label: Label
var _status_label: Label
var _headline_label: Label
var _summary_label: Label
var _mission_button: Button
var _disclosure_symbol_label: Label
var _preview_root: Control
var _preview_label: Label
var _cost_label: Label
var _cta_button: Button
var _lead_image: Control
var _cta_hovered := false
var _cta_pressed := false


func configure(font: Font) -> void:
	_font = font


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_PASS
	clip_contents = false
	_build_children()
	render_region({
		"region_id": "north_america",
		"display_name": "北美禁区带",
		"status_text": "红线升温",
		"summary": "都市传说与军事封锁交叠。\n红线稿需在 7 天内处理。",
		"mission_facts": "限时 1 · 线索 2 · 深链 1",
	})


func render_region(data: Dictionary) -> void:
	_region_id = str(data.get("region_id", "north_america"))
	if not is_instance_valid(_title_label):
		return
	_title_label.text = str(data.get("display_name", "北美禁区带"))
	_status_label.text = str(data.get("status_text", "红线升温"))
	_headline_label.text = str(data.get("headline", "洗衣店里出现了一片海"))
	_summary_label.text = str(data.get("summary", ""))
	_mission_button.text = "任务情报    %s" % str(data.get("mission_facts", ""))
	_lead_image.configure(_region_id, false)
	_update_expanded_state()
	queue_redraw()


func set_mission_expanded(value: bool) -> void:
	_expanded = value
	_update_expanded_state()
	queue_redraw()


func is_mission_expanded() -> bool:
	return _expanded


func get_state_snapshot() -> Dictionary:
	return {
		"region_id": _region_id,
		"title": _title_label.text if is_instance_valid(_title_label) else "",
		"status": _status_label.text if is_instance_valid(_status_label) else "",
		"expanded": _expanded,
		"mission_rect": [27, 572, 414, 56],
		"primary_cta_rect": [27, 932, 414, 76],
		"lead_image": _lead_image.get_source_contract() if is_instance_valid(_lead_image) else {},
		"interactive_button_names": ["MissionDisclosure", "PrimaryEnterCta"],
	}


func activate_mission_for_test() -> void:
	_on_mission_pressed()


func activate_primary_for_test() -> void:
	_on_primary_pressed()


func _build_children() -> void:
	var kicker := _make_label("Kicker", Rect2(27, 24, 414, 24), 13, MUTED, HORIZONTAL_ALIGNMENT_LEFT)
	kicker.text = "NEWS LEAD · 01 / 今夜校样"
	_title_label = _make_label("RegionTitle", Rect2(27, 58, 286, 76), 34, INK, HORIZONTAL_ALIGNMENT_LEFT)
	_title_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_status_label = _make_label("RegionStatus", Rect2(325, 60, 116, 42), 17, RUST, HORIZONTAL_ALIGNMENT_CENTER)

	_lead_image = AbstractImageScript.new()
	_lead_image.name = "LeadImage"
	_lead_image.position = Vector2(27, 150)
	_lead_image.size = Vector2(414, 264)
	_lead_image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_lead_image)

	_headline_label = _make_label("StoryHeadline", Rect2(27, 426, 414, 40), 25, INK, HORIZONTAL_ALIGNMENT_LEFT)
	_headline_label.text = "洗衣店里出现了一片海"
	_summary_label = _make_label("RegionSummary", Rect2(27, 472, 414, 84), 17, INK, HORIZONTAL_ALIGNMENT_LEFT)
	_summary_label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_summary_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_summary_label.max_lines_visible = 4
	_mission_button = _make_button("MissionDisclosure", Rect2(27, 572, 414, 56), 16, INK, PAPER, Color("d9d8c7"), COBALT)
	_mission_button.alignment = HORIZONTAL_ALIGNMENT_LEFT
	_mission_button.pressed.connect(_on_mission_pressed)
	_disclosure_symbol_label = Label.new()
	_disclosure_symbol_label.name = "DisclosureStateSymbol"
	_disclosure_symbol_label.position = Vector2(366, 0)
	_disclosure_symbol_label.size = Vector2(48, 56)
	_disclosure_symbol_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_disclosure_symbol_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_disclosure_symbol_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_disclosure_symbol_label.add_theme_font_override("font", _font)
	_disclosure_symbol_label.add_theme_font_size_override("font_size", 18)
	_disclosure_symbol_label.add_theme_color_override("font_color", Color(MUTED, 0.78))
	_mission_button.add_child(_disclosure_symbol_label)

	_preview_root = Control.new()
	_preview_root.name = "MissionPreviewCapacity"
	_preview_root.position = Vector2(27, 640)
	_preview_root.size = Vector2(414, 248)
	_preview_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_preview_root)
	_preview_label = Label.new()
	_preview_label.name = "MissionPreviewRows"
	_preview_label.position = Vector2(12, 10)
	_preview_label.size = Vector2(390, 228)
	_preview_label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_preview_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_preview_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_preview_label.add_theme_font_override("font", _font)
	_preview_label.add_theme_font_size_override("font_size", 16)
	_preview_label.add_theme_color_override("font_color", INK)
	_preview_label.text = "4 项已知任务\n\n常驻 2 · 限时 1 · 深链 1\n最早截止：第 4 天\n\n展开查看完整任务列表"
	_preview_root.add_child(_preview_label)

	_cost_label = _make_label("ActionCost", Rect2(27, 898, 414, 22), 15, MUTED, HORIZONTAL_ALIGNMENT_RIGHT)
	_cost_label.text = "本次进入：0 天"
	_cta_button = _make_button("PrimaryEnterCta", Rect2(27, 932, 414, 76), 21, Color("f2ecd8"), OLIVE, Color("7d8565"), COBALT)
	_cta_button.text = "进入地区任务台  →"
	for state_name in ["normal", "hover", "pressed", "focus", "disabled"]:
		_cta_button.add_theme_stylebox_override(state_name, StyleBoxEmpty.new())
	_cta_button.mouse_entered.connect(func() -> void:
		_cta_hovered = true
		queue_redraw()
	)
	_cta_button.mouse_exited.connect(func() -> void:
		_cta_hovered = false
		_cta_pressed = false
		queue_redraw()
	)
	_cta_button.button_down.connect(func() -> void:
		_cta_pressed = true
		queue_redraw()
	)
	_cta_button.button_up.connect(func() -> void:
		_cta_pressed = false
		queue_redraw()
	)
	_cta_button.pressed.connect(_on_primary_pressed)


func _draw() -> void:
	draw_rect(Rect2(Vector2(13, 10), size - Vector2(2, 2)), Color(0.01, 0.05, 0.07, 0.42), true)
	draw_polygon(PackedVector2Array([
		Vector2(8, 8), Vector2(size.x - 18, 2), Vector2(size.x, 20), Vector2(size.x - 3, size.y), Vector2(10, size.y - 4),
	]), [Color("344e5d")])
	draw_texture_rect(PAPER_STEEL_TEXTURE, Rect2(8, 8, size.x - 8, size.y - 8), false, Color(1, 1, 1, 0.72))
	draw_polygon(PackedVector2Array([
		Vector2(3, 5), Vector2(size.x - 28, 0), Vector2(size.x - 3, 25), Vector2(size.x - 7, size.y - 5), Vector2(0, size.y),
	]), [PAPER_BACK])
	draw_polygon(PackedVector2Array([
		Vector2(0, 2), Vector2(size.x - 20, 4), Vector2(size.x, 24), Vector2(size.x - 4, size.y - 2), Vector2(6, size.y), Vector2(1, size.y - 18),
	]), [PAPER])
	draw_texture_rect(PAPER_WARM_TEXTURE, Rect2(0, 2, size.x - 4, size.y - 4), false, Color(1, 1, 1, 0.70))
	draw_rect(Rect2(Vector2(1, 3), size - Vector2(7, 5)), Color(0.12, 0.18, 0.17, 0.44), false, 1.0)
	_draw_binder_clip(Vector2(size.x * 0.5, 9))
	draw_rect(Rect2(325, 60, 116, 42), Color(RUST, 0.10), true)
	draw_rect(Rect2(325, 60, 116, 42), RUST, false, 2.0)
	draw_line(Vector2(24, 138), Vector2(444, 138), Color(0.20, 0.27, 0.25, 0.26), 1.0)
	draw_rect(Rect2(23, 146, 422, 272), Color("142932"), true)
	draw_rect(Rect2(26, 149, 416, 266), Color(0.12, 0.18, 0.17, 0.58), false, 1.0)
	draw_rect(Rect2(27, 572, 7, 56), COBALT if _expanded else OLIVE, true)
	if _expanded:
		draw_rect(Rect2(27, 640, 414, 248), Color(0.26, 0.33, 0.30, 0.06), true)
		draw_rect(Rect2(27, 640, 414, 248), Color(0.26, 0.33, 0.30, 0.22), false, 1.0)
		var row_y := [650.0, 700.0, 750.0, 800.0]
		var row_colors := [COBALT, OLIVE, RUST, Color("596f72")]
		for index in range(row_y.size()):
			draw_rect(Rect2(35, row_y[index], 6, 34), Color(row_colors[index], 0.76), true)
			draw_line(Vector2(47, row_y[index] + 38), Vector2(429, row_y[index] + 38), Color(0.24, 0.30, 0.28, 0.16), 1.0)
	else:
		draw_line(Vector2(39, 704), Vector2(429, 704), Color(0.26, 0.33, 0.30, 0.16), 1.0)
		draw_line(Vector2(39, 792), Vector2(429, 792), Color(0.26, 0.33, 0.30, 0.10), 1.0)
	var ticket_color := Color("7d8565") if _cta_hovered else OLIVE
	if _cta_pressed:
		ticket_color = ticket_color.darkened(0.10)
	var ticket := PackedVector2Array([
		Vector2(27, 932), Vector2(425, 932), Vector2(441, 946), Vector2(441, 994),
		Vector2(426, 1008), Vector2(27, 1008),
	])
	draw_polygon(ticket, [ticket_color])
	draw_texture_rect(PAPER_OLIVE_TEXTURE, Rect2(35, 936, 398, 68), false, Color(1, 1, 1, 0.66))
	draw_rect(Rect2(27, 932, 7, 76), RUST, true)
	draw_circle(Vector2(27, 970), 8.0, PAPER)
	draw_circle(Vector2(441, 970), 8.0, PAPER)
	if _cta_hovered or _cta_button.has_focus():
		draw_line(Vector2(56, 998), Vector2(412, 998), Color("d9d3c4"), 2.0)


func _draw_binder_clip(center: Vector2) -> void:
	var metal := Color("151a1b")
	draw_rect(Rect2(center + Vector2(-26, -8), Vector2(52, 28)), metal, true)
	draw_rect(Rect2(center + Vector2(-22, -5), Vector2(44, 20)), Color("292b2a"), true)
	draw_arc(center + Vector2(-14, -6), 12.0, PI, TAU, 18, Color("aaa89c"), 2.5)
	draw_arc(center + Vector2(14, -6), 12.0, PI, TAU, 18, Color("aaa89c"), 2.5)


func _update_expanded_state() -> void:
	if not is_instance_valid(_preview_root):
		return
	_preview_root.visible = true
	_mission_button.text = "任务情报    收起" if _expanded else "任务情报    限时 1 · 线索 2 · 深链 1"
	_disclosure_symbol_label.text = "－" if _expanded else "＋"
	_preview_label.text = (
		"01  51 区外圈公路｜科学纪实｜2 天｜常驻\n\n"
		+ "02  罗斯威尔档案残页｜科学纪实｜1 天｜常驻\n\n"
		+ "03  雷达异常光点｜大众热度｜2 天｜限时第 4 天\n\n"
		+ "04  M330 末班车空白段｜神秘玄学｜2 天｜深链"
	) if _expanded else (
		"4 项已知任务\n\n常驻 2 · 限时 1 · 深链 1\n最早截止：第 4 天\n\n展开查看完整任务列表"
	)


func _on_mission_pressed() -> void:
	set_mission_expanded(not _expanded)
	mission_intel_toggled.emit(_expanded)


func _on_primary_pressed() -> void:
	enter_region_requested.emit(_region_id)


func _make_label(node_name: String, rect: Rect2, font_size: int, color: Color, alignment: HorizontalAlignment) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.horizontal_alignment = alignment
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("font", _font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	add_child(label)
	return label


func _make_button(node_name: String, rect: Rect2, font_size: int, font_color: Color, normal_color: Color, hover_color: Color, focus_color: Color) -> Button:
	var button := Button.new()
	button.name = node_name
	button.position = rect.position
	button.size = rect.size
	button.focus_mode = Control.FOCUS_ALL
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	button.add_theme_font_override("font", _font)
	button.add_theme_font_size_override("font_size", font_size)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_stylebox_override("normal", _button_style(normal_color, Color(0.24, 0.30, 0.28, 0.48), 1))
	button.add_theme_stylebox_override("hover", _button_style(hover_color, focus_color, 2))
	button.add_theme_stylebox_override("pressed", _button_style(normal_color.darkened(0.08), focus_color, 3))
	button.add_theme_stylebox_override("focus", _button_style(Color(0, 0, 0, 0), focus_color, 2))
	add_child(button)
	return button


func _button_style(fill: Color, border: Color, width: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = border
	style.border_width_left = width
	style.border_width_top = width
	style.border_width_right = width
	style.border_width_bottom = width
	style.content_margin_left = 18
	style.content_margin_right = 18
	return style
