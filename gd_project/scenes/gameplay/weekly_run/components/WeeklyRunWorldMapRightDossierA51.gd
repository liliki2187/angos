extends Control
class_name WeeklyRunWorldMapRightDossierA51

signal enter_region_requested
signal mission_intel_toggled(expanded: bool)

const REFERENCE_SIZE := Vector2(320.0, 520.0)
const PREVIEW_LIMIT := 2

const PARENT_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v095_right_dossier_candidate_a5/ingredients/right_dossier_candidate_a5_parent_2x.png"
const PRIMARY_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v093_right_dossier_candidate_a3/ingredients/right_action_lane_candidate_a3_primary_olive_2x.png"
const PHOTO_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/right_dossier_north_america_photo_552x352.png"
const GLOBE_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_globe.png"
const DOCUMENT_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_document.png"
const ARROW_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_arrow.png"

const REGION_BODY_INNER := Rect2(34.0, 292.0, 252.0, 82.0)
const TASK_ROWS := [
	Rect2(34.0, 292.0, 252.0, 41.0),
	Rect2(34.0, 333.0, 252.0, 41.0),
]
const SLOTS := {
	"header_icon": Rect2(24.0, 38.0, 36.0, 36.0),
	"title_slot": Rect2(82.0, 42.0, 160.0, 34.0),
	"status_stamp": Rect2(246.0, 34.0, 58.0, 58.0),
	"photo_slot": Rect2(22.0, 98.0, 276.0, 176.0),
	"region_body": Rect2(22.0, 288.0, 276.0, 90.0),
	"mission_intel_button": Rect2(18.0, 390.0, 284.0, 44.0),
	"primary_enter_cta": Rect2(18.0, 444.0, 284.0, 50.0),
}
const MISSION_SLOTS := {
	"left_icon_zone": Rect2(10.0, 5.0, 28.0, 34.0),
	"title_label": Rect2(42.0, 6.0, 56.0, 32.0),
	"facts_label": Rect2(102.0, 6.0, 142.0, 32.0),
	"state_indicator": Rect2(252.0, 4.0, 20.0, 36.0),
}
const PRIMARY_SLOTS := {
	"label_plate": Rect2(62.0, 9.0, 170.0, 32.0),
	"right_action_badge": Rect2(238.0, 5.0, 42.0, 40.0),
}

const INK := Color("1c1e19")
const MUTED_INK := Color("4b5145")
const TEAL_INK := Color("3f6663")
const PAPER_INK := Color("eee5c9")
const RUST_INK := Color("8e3627")
const LOCKED_INK := Color("6f7068")

var _design_root: Control
var _ui_font: SystemFont
var _photo: TextureRect
var _photo_fallback: ColorRect
var _primary_texture: TextureRect
var _globe_icon: TextureRect
var _document_icon: TextureRect
var _arrow_icon: TextureRect
var _title_label: Label
var _status_label: Label
var _body_label: Label
var _mission_title_label: Label
var _mission_facts_label: Label
var _primary_label: Label
var _task_name_labels: Array[Label] = []
var _task_meta_labels: Array[Label] = []
var _task_divider: ColorRect
var _summary_divider: ColorRect
var _indicator_horizontal: ColorRect
var _indicator_vertical: ColorRect
var _summary_button: Button
var _primary_button: Button
var _debug_layer: Control

var _payload: Dictionary = {}
var _preview_rows: Array = []
var _preview_total := 0
var _region_id := ""
var _expanded := false
var _mission_available := false


static func has_runtime_assets() -> bool:
	for path in [PARENT_PATH, PRIMARY_PATH, PHOTO_PATH, GLOBE_ICON_PATH, DOCUMENT_ICON_PATH, ARROW_ICON_PATH]:
		if not ResourceLoader.exists(path):
			return false
	return true


func _ready() -> void:
	custom_minimum_size = REFERENCE_SIZE
	mouse_filter = Control.MOUSE_FILTER_PASS
	_setup_font()
	_build_interface()
	_update_design_transform()


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED and is_instance_valid(_design_root):
		_update_design_transform()


func render(payload: Dictionary) -> void:
	_payload = payload.duplicate(true)
	var next_region_id := str(payload.get("selected_region_id", ""))
	if next_region_id != _region_id:
		_region_id = next_region_id
		_expanded = false
	_preview_rows = payload.get("region_mission_preview", []).duplicate(true)
	_preview_total = int(payload.get("region_mission_preview_total", _preview_rows.size()))
	_mission_available = bool(payload.get("region_mission_intel_available", false)) and not _preview_rows.is_empty()
	if not _mission_available:
		_expanded = false
	_update_content()


func set_mission_intel_expanded(value: bool) -> void:
	var next_value := value and _mission_available
	if next_value == _expanded:
		return
	_expanded = next_value
	_update_state_visibility()
	mission_intel_toggled.emit(_expanded)


func is_mission_intel_expanded() -> bool:
	return _expanded


func set_debug_zones(visible: bool) -> void:
	if not is_instance_valid(_debug_layer):
		_build_debug_layer()
	_debug_layer.visible = visible


func activate_primary_for_test() -> void:
	if is_instance_valid(_primary_button) and not _primary_button.disabled:
		enter_region_requested.emit()


func get_state_snapshot() -> Dictionary:
	return {
		"region_id": _region_id,
		"title": _title_label.text if is_instance_valid(_title_label) else "",
		"expanded": _expanded,
		"mission_available": _mission_available,
		"mission_facts": _mission_facts_label.text if is_instance_valid(_mission_facts_label) else "",
		"preview_source_rows": _preview_rows.size(),
		"preview_rendered_rows": mini(PREVIEW_LIMIT, _preview_rows.size()) if _expanded else 0,
		"summary_disabled": _summary_button.disabled if is_instance_valid(_summary_button) else true,
		"primary_disabled": _primary_button.disabled if is_instance_valid(_primary_button) else true,
		"photo_placeholder_visible": is_instance_valid(_photo) and _photo.visible,
		"interactive_button_names": get_interactive_button_names(),
		"task_row_hit_rects": 0,
		"reference_size": [REFERENCE_SIZE.x, REFERENCE_SIZE.y],
		"region_body_rect": _rect_array(SLOTS["region_body"]),
		"mission_summary_rect": _rect_array(SLOTS["mission_intel_button"]),
		"primary_cta_rect": _rect_array(SLOTS["primary_enter_cta"]),
	}


func get_interactive_button_names() -> Array[String]:
	var names: Array[String] = []
	for node in find_children("*", "Button", true, false):
		names.append(str(node.name))
	names.sort()
	return names


func _setup_font() -> void:
	_ui_font = SystemFont.new()
	_ui_font.font_names = PackedStringArray([
		"Microsoft YaHei UI",
		"Microsoft YaHei",
		"Source Han Sans SC",
		"Noto Sans CJK SC",
		"Noto Sans SC",
		"DengXian",
		"SimHei",
	])


func _build_interface() -> void:
	_design_root = Control.new()
	_design_root.name = "DossierReferenceCanvas320x520"
	_design_root.size = REFERENCE_SIZE
	_design_root.clip_contents = true
	_design_root.mouse_filter = Control.MOUSE_FILTER_PASS
	add_child(_design_root)

	_photo_fallback = ColorRect.new()
	_photo_fallback.name = "PhotoFallback"
	_photo_fallback.position = SLOTS["photo_slot"].position
	_photo_fallback.size = SLOTS["photo_slot"].size
	_photo_fallback.color = Color("10242a")
	_photo_fallback.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_design_root.add_child(_photo_fallback)

	_photo = _make_texture("RegionPhotoPlaceholder", load(PHOTO_PATH), SLOTS["photo_slot"], TextureRect.STRETCH_KEEP_ASPECT_COVERED, 1)
	_make_texture("DossierPaperShell", load(PARENT_PATH), Rect2(Vector2.ZERO, REFERENCE_SIZE), TextureRect.STRETCH_SCALE, 2)
	_primary_texture = _make_texture("PrimaryCtaSkin", load(PRIMARY_PATH), SLOTS["primary_enter_cta"], TextureRect.STRETCH_SCALE, 3)

	var header_icon_rect: Rect2 = SLOTS["header_icon"]
	header_icon_rect.position.y += 3.0
	_globe_icon = _make_icon("HeaderGlobeIcon", load(GLOBE_ICON_PATH), header_icon_rect, Color("5d604e"), 0.86, 5)
	_document_icon = _make_icon("MissionDocumentIcon", load(DOCUMENT_ICON_PATH), _child_rect(SLOTS["mission_intel_button"], MISSION_SLOTS["left_icon_zone"]), TEAL_INK, 0.72, 5)
	_arrow_icon = _make_icon("PrimaryArrowIcon", load(ARROW_ICON_PATH), _child_rect(SLOTS["primary_enter_cta"], PRIMARY_SLOTS["right_action_badge"]), PAPER_INK, 0.72, 5)

	_title_label = _make_label("RegionTitle", SLOTS["title_slot"], 27, INK, HORIZONTAL_ALIGNMENT_CENTER, 1, true)
	var status_rect: Rect2 = SLOTS["status_stamp"]
	status_rect.position.y -= 4.0
	_status_label = _make_label("RegionStatus", status_rect, 15, RUST_INK, HORIZONTAL_ALIGNMENT_CENTER, 2, true)
	_body_label = _make_label("RegionBody", REGION_BODY_INNER, 17, Color("22251f"), HORIZONTAL_ALIGNMENT_LEFT, 4, false)

	var mission_rect: Rect2 = SLOTS["mission_intel_button"]
	_mission_title_label = _make_label("MissionTitle", _child_rect(mission_rect, MISSION_SLOTS["title_label"]), 16, TEAL_INK, HORIZONTAL_ALIGNMENT_LEFT, 1, true)
	_mission_facts_label = _make_label("MissionFacts", _child_rect(mission_rect, MISSION_SLOTS["facts_label"]), 14, MUTED_INK, HORIZONTAL_ALIGNMENT_CENTER, 1, false)
	_summary_divider = _make_rule("MissionSummaryDivider", _child_rect(mission_rect, Rect2(10.0, 42.0, 264.0, 1.0)), Color(0.247, 0.4, 0.388, 0.28), 5)
	_build_state_indicator(_child_rect(mission_rect, MISSION_SLOTS["state_indicator"]))

	for index in range(PREVIEW_LIMIT):
		var row: Rect2 = TASK_ROWS[index]
		var name_rect := Rect2(row.position + Vector2(0.0, 2.0), Vector2(row.size.x, 22.0))
		var meta_rect := Rect2(row.position + Vector2(0.0, 22.0), Vector2(row.size.x, 17.0))
		_task_name_labels.append(_make_label("MissionPreview%dName" % (index + 1), name_rect, 16, Color("22251f"), HORIZONTAL_ALIGNMENT_LEFT, 1, true))
		_task_meta_labels.append(_make_label("MissionPreview%dMeta" % (index + 1), meta_rect, 13, TEAL_INK, HORIZONTAL_ALIGNMENT_LEFT, 1, false))
	_task_divider = _make_rule("MissionPreviewDivider", Rect2(TASK_ROWS[1].position.x, TASK_ROWS[1].position.y, TASK_ROWS[1].size.x, 1.0), Color(0.38, 0.41, 0.34, 0.32), 5)

	_primary_label = _make_label("PrimaryEnterLabel", _child_rect(SLOTS["primary_enter_cta"], PRIMARY_SLOTS["label_plate"]), 20, PAPER_INK, HORIZONTAL_ALIGNMENT_CENTER, 1, true)
	_summary_button = _make_hit_button("MissionSummaryButton", SLOTS["mission_intel_button"], 20)
	_summary_button.add_theme_stylebox_override("focus", _make_focus_style(TEAL_INK))
	_summary_button.tooltip_text = "展开任务情报"
	_summary_button.pressed.connect(_on_summary_pressed)
	_summary_button.mouse_entered.connect(func() -> void: _set_summary_emphasis(true))
	_summary_button.mouse_exited.connect(func() -> void: _set_summary_emphasis(false))

	_primary_button = _make_hit_button("PrimaryEnterButton", SLOTS["primary_enter_cta"], 21)
	_primary_button.add_theme_stylebox_override("focus", _make_focus_style(Color("d8d3ad")))
	_primary_button.tooltip_text = "进入地区任务台"
	_primary_button.pressed.connect(func() -> void: enter_region_requested.emit())
	_primary_button.mouse_entered.connect(func() -> void: _set_primary_emphasis(true))
	_primary_button.mouse_exited.connect(func() -> void: _set_primary_emphasis(false))

	_update_state_visibility()


func _update_content() -> void:
	_title_label.text = str(_payload.get("region_detail_title", "取材区域"))
	_status_label.text = str(_payload.get("region_status_primary", "未选择"))
	_body_label.text = str(_payload.get("region_dossier_body_text", _payload.get("region_brief", "请选择本周要进入的取材区域。")))
	_mission_title_label.text = str(_payload.get("region_mission_intel_title", "任务情报"))
	_primary_label.text = str(_payload.get("region_enter_text", "暂不可进入"))

	var can_enter := bool(_payload.get("region_enter_enabled", false))
	_primary_button.disabled = not can_enter
	_summary_button.disabled = not _mission_available
	_summary_button.tooltip_text = "收起任务情报" if _expanded else "展开任务情报"
	_photo.visible = _region_id == "us"
	_photo_fallback.visible = not _photo.visible

	match str(_payload.get("region_status_primary", "")):
		"红线升温":
			_status_label.add_theme_color_override("font_color", RUST_INK)
		"青线追踪":
			_status_label.add_theme_color_override("font_color", TEAL_INK)
		"锁定", "未选择":
			_status_label.add_theme_color_override("font_color", LOCKED_INK)
		_:
			_status_label.add_theme_color_override("font_color", Color("59613f"))

	_primary_texture.modulate = Color.WHITE if can_enter else Color(0.64, 0.64, 0.60, 0.72)
	_primary_label.add_theme_color_override("font_color", PAPER_INK if can_enter else Color(0.77, 0.75, 0.67, 0.82))
	_arrow_icon.modulate = PAPER_INK if can_enter else Color(0.77, 0.75, 0.67, 0.72)
	_update_state_visibility()


func _update_state_visibility() -> void:
	if not is_instance_valid(_body_label):
		return
	_body_label.visible = not _expanded
	var rendered_rows := mini(PREVIEW_LIMIT, _preview_rows.size()) if _expanded else 0
	for index in range(PREVIEW_LIMIT):
		var visible := index < rendered_rows
		_task_name_labels[index].visible = visible
		_task_meta_labels[index].visible = visible
		if visible:
			var row: Dictionary = _preview_rows[index]
			_task_name_labels[index].text = str(row.get("name", "未命名任务"))
			_task_meta_labels[index].text = "%s · 耗时%d天" % [str(row.get("kind_label", "线索")), int(row.get("days", 0))]
	_task_divider.visible = rendered_rows >= 2

	if _expanded:
		_mission_facts_label.text = "已显示 %d / 共 %d 条" % [rendered_rows, _preview_total]
	elif _mission_available:
		_mission_facts_label.text = str(_payload.get("region_mission_intel_facts", ""))
	else:
		_mission_facts_label.text = str(_payload.get("region_mission_intel_locked_text", "解锁后可查看"))

	_indicator_horizontal.visible = _mission_available
	_indicator_vertical.visible = _mission_available and not _expanded
	var mission_color := TEAL_INK if _mission_available else LOCKED_INK
	_mission_title_label.add_theme_color_override("font_color", mission_color)
	_mission_facts_label.add_theme_color_override("font_color", MUTED_INK if _mission_available else LOCKED_INK)
	_document_icon.modulate = mission_color
	_indicator_horizontal.color = Color(mission_color.r, mission_color.g, mission_color.b, 0.9)
	_indicator_vertical.color = Color(mission_color.r, mission_color.g, mission_color.b, 0.9)
	_summary_button.tooltip_text = "收起任务情报" if _expanded else "展开任务情报"


func _on_summary_pressed() -> void:
	set_mission_intel_expanded(not _expanded)


func _set_summary_emphasis(active: bool) -> void:
	if not _mission_available:
		return
	var color := Color("2f7772") if active else TEAL_INK
	_mission_title_label.add_theme_color_override("font_color", color)
	_document_icon.modulate = color
	_indicator_horizontal.color = color
	_indicator_vertical.color = color


func _set_primary_emphasis(active: bool) -> void:
	if _primary_button.disabled:
		return
	_primary_texture.modulate = Color(1.06, 1.06, 1.02, 1.0) if active else Color.WHITE


func _update_design_transform() -> void:
	var scale_factor := minf(size.x / REFERENCE_SIZE.x, size.y / REFERENCE_SIZE.y)
	if scale_factor <= 0.0:
		scale_factor = 1.0
	_design_root.scale = Vector2(scale_factor, scale_factor)
	_design_root.position = (size - REFERENCE_SIZE * scale_factor) * 0.5
	for node in _design_root.find_children("*", "Label", true, false):
		var label := node as Label
		if label != null and label.has_meta("runtime_font_size"):
			var runtime_size := int(label.get_meta("runtime_font_size"))
			label.add_theme_font_size_override("font_size", maxi(1, roundi(float(runtime_size) / scale_factor)))


func _build_state_indicator(rect: Rect2) -> void:
	_indicator_horizontal = _make_rule(
		"MissionStateHorizontal",
		Rect2(rect.position + Vector2(rect.size.x * 0.20, rect.size.y * 0.47), Vector2(rect.size.x * 0.60, 1.5)),
		TEAL_INK,
		6
	)
	_indicator_vertical = _make_rule(
		"MissionStateVertical",
		Rect2(rect.position + Vector2(rect.size.x * 0.46, rect.size.y * 0.22), Vector2(1.5, rect.size.y * 0.56)),
		TEAL_INK,
		6
	)


func _build_debug_layer() -> void:
	_debug_layer = Control.new()
	_debug_layer.name = "ContractDebugOverlay"
	_debug_layer.position = Vector2.ZERO
	_debug_layer.size = REFERENCE_SIZE
	_debug_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_debug_layer.z_index = 80
	_design_root.add_child(_debug_layer)
	var colors := {
		"header_icon": Color("51eeff"),
		"title_slot": Color("ff48ca"),
		"status_stamp": Color("ff6f5f"),
		"photo_slot": Color("48ecae"),
		"region_body": Color("ffd444"),
		"mission_intel_button": Color("4fdae8"),
		"primary_enter_cta": Color("aecc5b"),
	}
	for slot_name in colors:
		_make_debug_rect(_debug_layer, SLOTS[slot_name], colors[slot_name])
	_make_debug_rect(_debug_layer, REGION_BODY_INNER, Color("65ff94"))
	for row in TASK_ROWS:
		_make_debug_rect(_debug_layer, row, Color("58edf4"))
	_debug_layer.visible = false


func _make_texture(node_name: String, texture: Texture2D, rect: Rect2, stretch_mode: TextureRect.StretchMode, z: int) -> TextureRect:
	var node := TextureRect.new()
	node.name = node_name
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.texture = texture
	node.position = rect.position
	node.size = rect.size
	node.stretch_mode = stretch_mode
	node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	node.z_index = z
	_design_root.add_child(node)
	return node


func _make_icon(node_name: String, texture: Texture2D, rect: Rect2, color: Color, scale_factor: float, z: int) -> TextureRect:
	var icon_rect := Rect2(rect.position + rect.size * (1.0 - scale_factor) * 0.5, rect.size * scale_factor)
	var node := _make_texture(node_name, texture, icon_rect, TextureRect.STRETCH_KEEP_ASPECT_CENTERED, z)
	node.modulate = color
	return node


func _make_label(node_name: String, rect: Rect2, font_size: int, color: Color, alignment: HorizontalAlignment, max_lines: int, bold: bool) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.text = ""
	label.horizontal_alignment = alignment
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.clip_text = true
	label.max_lines_visible = max_lines
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("font", _ui_font)
	label.add_theme_font_size_override("font_size", font_size)
	label.set_meta("runtime_font_size", font_size)
	label.add_theme_color_override("font_color", color)
	if bold:
		label.add_theme_constant_override("outline_size", 0)
	label.z_index = 7
	_design_root.add_child(label)
	return label


func _make_rule(node_name: String, rect: Rect2, color: Color, z: int) -> ColorRect:
	var rule := ColorRect.new()
	rule.name = node_name
	rule.position = rect.position
	rule.size = rect.size
	rule.color = color
	rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rule.z_index = z
	_design_root.add_child(rule)
	return rule


func _make_hit_button(node_name: String, rect: Rect2, z: int) -> Button:
	var button := Button.new()
	button.name = node_name
	button.position = rect.position
	button.size = rect.size
	button.text = ""
	button.focus_mode = Control.FOCUS_ALL
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	button.z_index = z
	var empty := StyleBoxEmpty.new()
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		button.add_theme_stylebox_override(state, empty)
	_design_root.add_child(button)
	return button


func _make_focus_style(color: Color) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color.TRANSPARENT
	style.border_color = Color(color.r, color.g, color.b, 0.92)
	style.set_border_width_all(2)
	style.corner_radius_top_left = 2
	style.corner_radius_top_right = 2
	style.corner_radius_bottom_left = 2
	style.corner_radius_bottom_right = 2
	return style


func _make_debug_rect(parent: Control, rect: Rect2, color: Color) -> void:
	var panel := Panel.new()
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = Color(color.r, color.g, color.b, 0.06)
	style.border_color = color
	style.set_border_width_all(1)
	panel.add_theme_stylebox_override("panel", style)
	parent.add_child(panel)


func _child_rect(parent: Rect2, child: Rect2) -> Rect2:
	return Rect2(parent.position + child.position, child.size)


func _rect_array(rect: Rect2) -> Array[float]:
	return [rect.position.x, rect.position.y, rect.size.x, rect.size.y]
