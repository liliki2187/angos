extends Control
class_name WeeklyRunWorldMapAssembly

signal region_selected(region_id: String)
signal enter_region_requested

const LeftRegionCard = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapLeftRegionCardB212.gd")
const StructureLayer = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapStructureLayer.gd")
const RightDossier = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapRightDossierA51.gd")

const REFERENCE_SIZE := Vector2(1280.0, 720.0)
const LEFT_RECT := Rect2(24.0, 16.0, 228.0, 688.0)
const CENTER_RECT := Rect2(268.0, 16.0, 648.0, 688.0)
const RIGHT_RECT := Rect2(932.0, 16.0, 320.0, 688.0)
const MAP_RECT := Rect2(284.0, 64.0, 616.0, 464.0)
const DOSSIER_RECT := Rect2(932.0, 30.0, 320.0, 520.0)

const PAPER := Color("e9dfbd")
const INK := Color("1c211d")
const NIGHT := Color("07171b")
const TEAL := Color("1d4a4d")
const CYAN := Color("75aaa3")
const OLIVE := Color("aab356")
const RUST := Color("a54836")

var _design_root: Control
var _map_stage: Control
var _map_base_layer: Control
var _route_layer: Control
var _selected_region_layer: Control
var _pin_layer: Control
var _label_layer: Control
var _left_card_layer: Control
var _right_dossier: Control
var _center_title: Label
var _center_meta: Label
var _center_summary: Label
var _center_hint: Label
var _debug_layer: Control
var _payload: Dictionary = {}
var _selected_region_id := ""
var _region_buttons: Dictionary = {}
var _left_cards: Dictionary = {}


static func has_runtime_assets() -> bool:
	return LeftRegionCard.has_runtime_assets() and RightDossier.has_runtime_assets()


func _ready() -> void:
	set_meta("artifact_type", "runtime_state_preview")
	set_meta("map_artifact_type", "structure_only")
	mouse_filter = Control.MOUSE_FILTER_PASS
	_build_interface()
	_update_design_transform()


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED and is_instance_valid(_design_root):
		_update_design_transform()


func render(payload: Dictionary) -> void:
	_payload = payload.duplicate(true)
	_selected_region_id = str(_payload.get("selected_region_id", ""))
	var regions: Array = _payload.get("regions", []).duplicate(true)
	_render_left_cards(regions)
	_render_map(regions)
	_right_dossier.call("render", _build_dossier_payload(_payload))
	_center_meta.text = "ISSUE %03d  /  WEEK %02d  /  DAYS LEFT %02d" % [
		int(_payload.get("issue", 1)),
		int(_payload.get("week", 1)),
		int(_payload.get("remaining_days", 0)),
	]
	_center_summary.text = str(_payload.get("region_detail_title", "请选择取材区域"))
	_center_hint.text = str(_payload.get("region_hint", "从左侧档案或地图节点选择地区；进入地区任务台本身不消耗天数。"))


func has_independent_host() -> bool:
	return true


func set_mission_intel_expanded(value: bool) -> void:
	_right_dossier.call("set_mission_intel_expanded", value)


func set_debug_zones(value: bool) -> void:
	_debug_layer.visible = value
	_right_dossier.call("set_debug_zones", value)


func activate_primary_for_test() -> void:
	_right_dossier.call("activate_primary_for_test")


func get_dossier() -> Control:
	return _right_dossier


func get_state_snapshot() -> Dictionary:
	var card_snapshots: Array = []
	for region_id in _left_cards:
		card_snapshots.append(_left_cards[region_id].call("get_state_snapshot"))
	card_snapshots.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return str(a.region_id) < str(b.region_id))
	var selected_pin_id := ""
	for region_id in _region_buttons:
		var pin := _region_buttons[region_id] as Button
		if bool(pin.get_meta("selected", false)):
			selected_pin_id = str(region_id)
			break
	var dossier_snapshot: Dictionary = _right_dossier.call("get_state_snapshot")
	return {
		"artifact_type": str(get_meta("artifact_type")),
		"map_artifact_type": str(get_meta("map_artifact_type")),
		"selected_region_id": _selected_region_id,
		"left_selected_region_id": _selected_left_region_id(card_snapshots),
		"map_selected_region_id": selected_pin_id,
		"dossier_region_id": str(dossier_snapshot.get("region_id", "")),
		"cta_region_id": str(dossier_snapshot.get("region_id", "")),
		"dossier": dossier_snapshot,
		"left_cards": card_snapshots,
		"host_reference_size": [REFERENCE_SIZE.x, REFERENCE_SIZE.y],
		"left_rect": _rect_array(LEFT_RECT),
		"center_rect": _rect_array(CENTER_RECT),
		"right_rect": _rect_array(RIGHT_RECT),
		"map_rect": _rect_array(MAP_RECT),
		"dossier_rect": _rect_array(DOSSIER_RECT),
		"center_right_edge": CENTER_RECT.end.x,
		"map_layer_names": ["MapBaseLayer", "RouteLayer", "SelectedRegionLayer", "PinLayer", "LabelLayer"],
		"old_global_channel_present": false,
		"external_cta_present": false,
		"symbol_strip_present": false,
		"enter_region_day_cost": 0,
	}


func _build_interface() -> void:
	_design_root = Control.new()
	_design_root.name = "WMWAssemblyReferenceCanvas1280x720"
	_design_root.position = Vector2.ZERO
	_design_root.size = REFERENCE_SIZE
	_design_root.clip_contents = true
	_design_root.mouse_filter = Control.MOUSE_FILTER_PASS
	add_child(_design_root)

	var background := ColorRect.new()
	background.name = "FullScreenBackground"
	background.position = Vector2.ZERO
	background.size = REFERENCE_SIZE
	background.color = NIGHT
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_design_root.add_child(background)

	_make_panel("LeftResponsibilityZone", LEFT_RECT, Color("0d292d"), Color(0.38, 0.65, 0.62, 0.25), 1)
	_make_panel("CenterResponsibilityZone", CENTER_RECT, Color("0b2428"), Color(0.38, 0.65, 0.62, 0.30), 1)

	_left_card_layer = Control.new()
	_left_card_layer.name = "LeftRegionCardLayer"
	_left_card_layer.position = Vector2.ZERO
	_left_card_layer.size = REFERENCE_SIZE
	_left_card_layer.mouse_filter = Control.MOUSE_FILTER_PASS
	_left_card_layer.z_index = 2
	_design_root.add_child(_left_card_layer)

	_center_title = _make_label("CenterTitle", Rect2(286.0, 24.0, 360.0, 28.0), "WORLD MYSTERIES WEEKLY", 18, PAPER, HORIZONTAL_ALIGNMENT_LEFT, true, 3)
	_center_meta = _make_label("CenterMeta", Rect2(640.0, 26.0, 258.0, 24.0), "", 11, CYAN, HORIZONTAL_ALIGNMENT_RIGHT, false, 3)

	_map_stage = Control.new()
	_map_stage.name = "MapStage"
	_map_stage.position = MAP_RECT.position
	_map_stage.size = MAP_RECT.size
	_map_stage.clip_contents = true
	_map_stage.mouse_filter = Control.MOUSE_FILTER_PASS
	_map_stage.z_index = 2
	_map_stage.set_meta("artifact_type", "structure_only")
	_design_root.add_child(_map_stage)

	_map_base_layer = _make_structure_layer("MapBaseLayer", "base", 0)
	_route_layer = _make_structure_layer("RouteLayer", "routes", 1)
	_selected_region_layer = _make_structure_layer("SelectedRegionLayer", "selected", 2)
	_pin_layer = _make_map_layer("PinLayer", 3, Control.MOUSE_FILTER_PASS)
	_label_layer = _make_map_layer("LabelLayer", 4, Control.MOUSE_FILTER_IGNORE)

	_make_panel("CenterLowerBand", Rect2(284.0, 544.0, 616.0, 144.0), Color("102f32"), Color(0.43, 0.68, 0.63, 0.20), 2)
	_center_summary = _make_label("SelectedRegionSummary", Rect2(304.0, 560.0, 576.0, 34.0), "请选择取材区域", 23, PAPER, HORIZONTAL_ALIGNMENT_LEFT, true, 3)
	_center_hint = _make_label("SelectedRegionHint", Rect2(304.0, 600.0, 576.0, 56.0), "", 14, Color("b7c9ba"), HORIZONTAL_ALIGNMENT_LEFT, false, 3)
	_center_hint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_center_hint.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	var zero_cost := _make_label("ZeroCostRule", Rect2(304.0, 657.0, 576.0, 20.0), "选择与进入地区任务台：0 天", 12, OLIVE, HORIZONTAL_ALIGNMENT_RIGHT, true, 3)
	zero_cost.tooltip_text = "只有实际派遣任务才消耗天数"

	_right_dossier = RightDossier.new()
	_right_dossier.name = "WorldMapRightDossierA51"
	_right_dossier.position = DOSSIER_RECT.position
	_right_dossier.size = DOSSIER_RECT.size
	_design_root.add_child(_right_dossier)
	_right_dossier.connect("enter_region_requested", func() -> void: enter_region_requested.emit())

	_build_debug_layer()


func _render_left_cards(regions: Array) -> void:
	for child in _left_card_layer.get_children():
		child.queue_free()
	_left_cards.clear()
	var y := LEFT_RECT.position.y
	for index in range(mini(4, regions.size())):
		var region: Dictionary = regions[index]
		var card := LeftRegionCard.new()
		card.name = "RegionCard_%s" % str(region.get("id", index))
		card.position = Vector2(36.0, y)
		card.size = Vector2(204.0, 160.0)
		_left_card_layer.add_child(card)
		card.call("render", region, _selected_region_id)
		var region_id := str(region.get("id", ""))
		card.connect("region_selected", func(next_region_id: String) -> void: region_selected.emit(next_region_id))
		_left_cards[region_id] = card
		y += 172.0


func _render_map(regions: Array) -> void:
	_map_base_layer.call("render", regions, _selected_region_id)
	_route_layer.call("render", regions, _selected_region_id)
	_selected_region_layer.call("render", regions, _selected_region_id)
	for child in _pin_layer.get_children():
		child.queue_free()
	for child in _label_layer.get_children():
		child.queue_free()
	_region_buttons.clear()
	for region in regions:
		var region_id := str(region.get("id", ""))
		var map_pos: Dictionary = region.get("map_pos", {"x": 0.5, "y": 0.5})
		var point := Vector2(float(map_pos.get("x", 0.5)) * MAP_RECT.size.x, float(map_pos.get("y", 0.5)) * MAP_RECT.size.y)
		var selected := region_id == _selected_region_id
		var unlocked := bool(region.get("unlocked", region.get("enabled", false)))
		var pin := Button.new()
		pin.name = "RegionPin_%s" % region_id
		pin.position = point - Vector2(13.0, 13.0)
		pin.size = Vector2(26.0, 26.0)
		pin.text = ""
		pin.focus_mode = Control.FOCUS_ALL
		pin.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		pin.set_meta("selected", selected)
		pin.tooltip_text = str(region.get("name", region_id))
		_apply_pin_style(pin, selected, unlocked)
		_pin_layer.add_child(pin)
		pin.pressed.connect(_on_map_pin_pressed.bind(region_id))
		_region_buttons[region_id] = pin

		var label := Label.new()
		label.name = "RegionLabel_%s" % region_id
		label.position = point + Vector2(16.0, -12.0)
		label.size = Vector2(142.0, 32.0)
		if label.position.x + label.size.x > MAP_RECT.size.x - 6.0:
			label.position.x = point.x - label.size.x - 16.0
		label.text = str(region.get("name", region_id))
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.clip_text = true
		label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
		label.add_theme_font_size_override("font_size", 13)
		label.add_theme_color_override("font_color", PAPER if selected else Color("b4c4b6"))
		label.add_theme_constant_override("outline_size", 4)
		label.add_theme_color_override("font_outline_color", Color("092024"))
		label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_label_layer.add_child(label)


func _build_dossier_payload(payload: Dictionary) -> Dictionary:
	var result := {}
	for field in [
		"selected_region_id", "region_detail_title", "region_status_primary",
		"region_dossier_body_text", "region_brief", "region_mission_intel_title",
		"region_mission_intel_facts", "region_mission_intel_available",
		"region_mission_intel_locked_text", "region_mission_preview",
		"region_mission_preview_total", "region_mission_preview_limit",
		"region_enter_enabled", "region_enter_text",
	]:
		result[field] = payload.get(field)
	return result


func _on_map_pin_pressed(region_id: String) -> void:
	region_selected.emit(region_id)


func _make_structure_layer(node_name: String, mode: String, z: int) -> Control:
	var layer := StructureLayer.new()
	layer.name = node_name
	layer.layer_mode = mode
	layer.position = Vector2.ZERO
	layer.size = MAP_RECT.size
	layer.z_index = z
	_map_stage.add_child(layer)
	return layer


func _make_map_layer(node_name: String, z: int, filter: Control.MouseFilter) -> Control:
	var layer := Control.new()
	layer.name = node_name
	layer.position = Vector2.ZERO
	layer.size = MAP_RECT.size
	layer.mouse_filter = filter
	layer.z_index = z
	_map_stage.add_child(layer)
	return layer


func _make_panel(node_name: String, rect: Rect2, fill: Color, border: Color, z: int) -> Panel:
	var panel := Panel.new()
	panel.name = node_name
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.z_index = z
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = border
	style.set_border_width_all(1)
	style.corner_radius_top_left = 2
	style.corner_radius_top_right = 2
	style.corner_radius_bottom_left = 2
	style.corner_radius_bottom_right = 2
	panel.add_theme_stylebox_override("panel", style)
	_design_root.add_child(panel)
	return panel


func _make_label(node_name: String, rect: Rect2, value: String, font_size: int, color: Color, alignment: HorizontalAlignment, bold: bool, z: int) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.text = value
	label.horizontal_alignment = alignment
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.clip_text = true
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	if bold:
		label.add_theme_constant_override("outline_size", 0)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.z_index = z
	_design_root.add_child(label)
	return label


func _apply_pin_style(pin: Button, selected: bool, unlocked: bool) -> void:
	var fill := OLIVE if selected else (Color("d9cf9e") if unlocked else Color("59625c"))
	var border := Color("f1e8bd") if selected else Color("10292b")
	for style_name in ["normal", "hover", "pressed", "focus"]:
		var style := StyleBoxFlat.new()
		style.bg_color = fill.lightened(0.12) if style_name == "hover" else fill
		style.border_color = border
		style.set_border_width_all(2)
		style.corner_radius_top_left = 13
		style.corner_radius_top_right = 13
		style.corner_radius_bottom_left = 13
		style.corner_radius_bottom_right = 13
		pin.add_theme_stylebox_override(style_name, style)


func _build_debug_layer() -> void:
	_debug_layer = Control.new()
	_debug_layer.name = "AssemblyGeometryDebugOverlay"
	_debug_layer.position = Vector2.ZERO
	_debug_layer.size = REFERENCE_SIZE
	_debug_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_debug_layer.z_index = 90
	_design_root.add_child(_debug_layer)
	_make_debug_rect(LEFT_RECT, Color("43e5ff"))
	_make_debug_rect(CENTER_RECT, Color("ffd54a"))
	_make_debug_rect(RIGHT_RECT, Color("ff5eac"))
	_make_debug_rect(MAP_RECT, Color("62e5a8"))
	_make_debug_rect(DOSSIER_RECT, Color("ff8f5d"))
	var boundary := ColorRect.new()
	boundary.name = "CenterSafeBoundaryX916"
	boundary.position = Vector2(915.0, 0.0)
	boundary.size = Vector2(2.0, REFERENCE_SIZE.y)
	boundary.color = Color("ffdf4b")
	boundary.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_debug_layer.add_child(boundary)
	_debug_layer.visible = false


func _make_debug_rect(rect: Rect2, color: Color) -> void:
	var panel := Panel.new()
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = Color(color.r, color.g, color.b, 0.04)
	style.border_color = color
	style.set_border_width_all(1)
	panel.add_theme_stylebox_override("panel", style)
	_debug_layer.add_child(panel)


func _update_design_transform() -> void:
	var scale_factor := minf(size.x / REFERENCE_SIZE.x, size.y / REFERENCE_SIZE.y)
	if scale_factor <= 0.0:
		scale_factor = 1.0
	_design_root.scale = Vector2(scale_factor, scale_factor)
	_design_root.position = (size - REFERENCE_SIZE * scale_factor) * 0.5


func _selected_left_region_id(cards: Array) -> String:
	for card in cards:
		if bool(card.get("selected", false)):
			return str(card.get("region_id", ""))
	return ""


func _rect_array(rect: Rect2) -> Array[float]:
	return [rect.position.x, rect.position.y, rect.size.x, rect.size.y]
