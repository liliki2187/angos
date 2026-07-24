extends Control

signal back_to_world_requested
signal node_selected(node_id: String)
signal open_dispatch_requested

const ManifestV2 = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd")
const EventPin = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionEventPin.gd")

const REFERENCE_SIZE := Vector2(1920.0, 1080.0)
const HUD_RECT := Rect2(0, 0, 1920, 72)
const LEFT_RECT := Rect2(24, 96, 380, 804)
const MAP_RECT := Rect2(420, 96, 1040, 804)
const RIGHT_RECT := Rect2(1484, 96, 412, 960)
const SCHEDULE_RECT := Rect2(24, 916, 1436, 140)
const CLUSTER_THRESHOLD := 8
const CLUSTER_CELL_SIZE := 84.0

const NAVY := Color("071d2e")
const NAVY_LIGHT := Color("123548")
const INK := Color("18282d")
const PAPER := Color("e7dfca")
const PAPER_LIGHT := Color("f2ead6")
const PAPER_DARK := Color("c8bfa6")
const OLIVE := Color("8c9850")
const TEAL := Color("34767a")
const RUST := Color("ad5038")
const MUTED := Color("74766d")

var _design_root: Control
var _header_title: Label
var _header_status: Label
var _left_title: Label
var _card_scroll: ScrollContainer
var _card_list: VBoxContainer
var _card_empty: Label
var _map_texture: TextureRect
var _pin_layer: Control
var _dossier_kicker: Label
var _dossier_title: Label
var _dossier_summary: RichTextLabel
var _dossier_meta: Label
var _dossier_risk: Label
var _dossier_hint: Label
var _dossier_risk_title: Label
var _dossier_risk_accent: ColorRect
var _dossier_shell_texture: TextureRect
var _dossier_meta_plate: NinePatchRect
var _dossier_risk_plate: NinePatchRect
var _dispatch_button: Button
var _schedule_summary: Label
var _schedule_preview: Label
var _advance_button: Button

var _payload: Dictionary = {}
var _selected_task_id := ""
var _hovered_task_id := ""
var _pending_selection_transition_id := ""
var _card_buttons: Dictionary = {}
var _pin_buttons: Dictionary = {}
var _cluster_buttons: Dictionary = {}
var _cluster_member_pins: Dictionary = {}

func _ready() -> void:
	set_process_unhandled_key_input(true)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_build_interface()
	_update_design_transform()

func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED and is_instance_valid(_design_root):
		_update_design_transform()

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), NAVY, true)
	var vignette := Color(0.0, 0.035, 0.055, 0.38)
	draw_rect(Rect2(0, 0, size.x, 18), vignette, true)
	draw_rect(Rect2(0, size.y - 22, size.x, 22), vignette, true)

func _unhandled_key_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("ui_cancel"):
		back_to_world_requested.emit()
		get_viewport().set_input_as_handled()

func render(payload: Dictionary) -> void:
	_payload = payload.duplicate(true)
	_selected_task_id = str(payload.get("selected_node_id", ""))
	var region_title := str(payload.get("region_title", "取材区域"))
	_header_title.text = "WORLD MYSTERY WEEKLY  /  %s区域任务台" % region_title
	_header_status.text = "ISSUE %03d   WEEK %02d   DAYS LEFT %02d" % [
		int(payload.get("week", 1)),
		int(payload.get("week", 1)),
		int(payload.get("remaining_days", 0)),
	]
	_left_title.text = "%s  /  事件索引" % region_title
	var nodes: Array = payload.get("nodes", [])
	_rebuild_event_cards(nodes)
	_rebuild_event_pins(nodes)
	_pending_selection_transition_id = ""
	_render_dossier(payload)
	_render_schedule(payload, nodes)

func get_event_card_count() -> int:
	return _card_buttons.size()

func get_event_pin_count() -> int:
	return _pin_buttons.size()

func get_cluster_marker_count() -> int:
	return _cluster_buttons.size()

func get_cluster_keys() -> Array[String]:
	var keys: Array[String] = []
	for cluster_key in _cluster_buttons.keys():
		keys.append(str(cluster_key))
	keys.sort()
	return keys

func get_event_card_task_ids() -> Array[String]:
	var ids: Array[String] = []
	for task_id in _card_buttons.keys():
		ids.append(str(task_id))
	ids.sort()
	return ids

func get_event_pin_task_ids() -> Array[String]:
	var ids: Array[String] = []
	for task_id in _pin_buttons.keys():
		ids.append(str(task_id))
	ids.sort()
	return ids

func get_selected_task_id() -> String:
	return _selected_task_id

func is_dispatch_enabled() -> bool:
	return is_instance_valid(_dispatch_button) and not _dispatch_button.disabled

func is_map_texture_loaded() -> bool:
	return is_instance_valid(_map_texture) and _map_texture.texture != null

func is_advance_day_enabled() -> bool:
	return is_instance_valid(_advance_button) and not _advance_button.disabled

func get_dossier_summary_text() -> String:
	return _dossier_summary.text if is_instance_valid(_dossier_summary) else ""

func get_dossier_title_text() -> String:
	return _dossier_title.text if is_instance_valid(_dossier_title) else ""

func get_dossier_meta_text() -> String:
	return _dossier_meta.text if is_instance_valid(_dossier_meta) else ""

func get_dossier_risk_text() -> String:
	return _dossier_risk.text if is_instance_valid(_dossier_risk) else ""

func get_dossier_recommendation_text() -> String:
	return _dossier_hint.text if is_instance_valid(_dossier_hint) else ""

func is_dossier_summary_scroll_enabled() -> bool:
	return is_instance_valid(_dossier_summary) and _dossier_summary.scroll_active

func are_dossier_candidate_assets_loaded() -> bool:
	var cta_style := _dispatch_button.get_theme_stylebox("normal") if is_instance_valid(_dispatch_button) else null
	return (
		is_instance_valid(_dossier_shell_texture)
		and _dossier_shell_texture.texture != null
		and is_instance_valid(_dossier_meta_plate)
		and _dossier_meta_plate.texture != null
		and is_instance_valid(_dossier_risk_plate)
		and _dossier_risk_plate.texture != null
		and is_instance_valid(_dispatch_button)
		and cta_style is StyleBoxTexture
		and (cta_style as StyleBoxTexture).texture != null
	)

func get_visible_pin_label_count() -> int:
	var count := 0
	for pin_value in _pin_buttons.values():
		if bool(pin_value.call("is_caption_visible")):
			count += 1
	return count

func is_cluster_expanded(cluster_key: String) -> bool:
	var button = _cluster_buttons.get(cluster_key)
	return is_instance_valid(button) and bool(button.get_meta("expanded", false))

func get_pin_reference_positions() -> Array[Vector2]:
	var positions: Array[Vector2] = []
	for task_id in get_event_pin_task_ids():
		var pin = _pin_buttons.get(task_id)
		if is_instance_valid(pin):
			positions.append(pin.position)
	return positions

func has_visible_label_pin_overlap(clearance: float = 8.0) -> bool:
	for owner_id in _pin_buttons.keys():
		var owner_pin = _pin_buttons[owner_id]
		if not is_instance_valid(owner_pin) or not bool(owner_pin.call("is_caption_visible")):
			continue
		var caption_rect: Rect2 = owner_pin.call("get_caption_rect_in_pin")
		caption_rect.position += owner_pin.position
		caption_rect = caption_rect.grow(clearance)
		for other_id in _pin_buttons.keys():
			if other_id == owner_id:
				continue
			var other_pin = _pin_buttons[other_id]
			if not is_instance_valid(other_pin) or not other_pin.visible:
				continue
			if caption_rect.intersects(Rect2(other_pin.position, other_pin.size)):
				return true
	return false

func _build_interface() -> void:
	_design_root = Control.new()
	_design_root.name = "ReferenceCanvas1920x1080"
	_design_root.size = REFERENCE_SIZE
	_design_root.mouse_filter = Control.MOUSE_FILTER_PASS
	add_child(_design_root)
	_build_hud()
	_build_event_index()
	_build_map_stage()
	_build_dossier()
	_build_schedule()

func _build_hud() -> void:
	var hud := _make_panel(_design_root, HUD_RECT, NAVY, Color("456573"), 1, 0)
	var back_button := Button.new()
	back_button.name = "BackToWorldButton"
	back_button.position = Vector2(24, 14)
	back_button.size = Vector2(164, 44)
	back_button.text = "←  返回世界地图"
	back_button.focus_mode = Control.FOCUS_ALL
	back_button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_style_button(back_button, NAVY_LIGHT, Color("8293a0"), PAPER_LIGHT, 16)
	hud.add_child(back_button)
	back_button.pressed.connect(func() -> void: back_to_world_requested.emit())

	_header_title = _make_label(hud, "WORLD MYSTERY WEEKLY", Rect2(216, 11, 900, 50), 24, PAPER_LIGHT)
	_header_title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_header_title.add_theme_constant_override("outline_size", 2)
	_header_title.add_theme_color_override("font_outline_color", Color(0.0, 0.02, 0.03, 0.84))
	_header_status = _make_label(hud, "ISSUE 001   WEEK 01   DAYS LEFT 07", Rect2(1380, 11, 512, 50), 16, Color("b9c39b"))
	_header_status.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_header_status.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

func _build_event_index() -> void:
	_make_panel(_design_root, Rect2(42, 110, 370, 790), Color("173d57"), Color("294c60"), 1, 5)
	_make_panel(_design_root, Rect2(32, 102, 374, 796), Color("24577a"), Color("7b8d8e"), 1, 5)
	var panel := _make_panel(_design_root, LEFT_RECT, PAPER, PAPER_LIGHT, 3, 8)
	_left_title = _make_label(panel, "事件索引", Rect2(22, 20, 334, 38), 22, INK)
	var subtitle := _make_label(panel, "同一地区可出现多个任务标记", Rect2(22, 64, 334, 28), 13, Color("56645f"))
	subtitle.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_make_rule(panel, Rect2(20, 108, 340, 2), Color("83917d"))

	_card_scroll = ScrollContainer.new()
	_card_scroll.position = Vector2(20, 126)
	_card_scroll.size = Vector2(340, 506)
	_card_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	_card_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	panel.add_child(_card_scroll)
	_card_list = VBoxContainer.new()
	_card_list.custom_minimum_size = Vector2(324, 0)
	_card_list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_card_list.add_theme_constant_override("separation", 10)
	_card_scroll.add_child(_card_list)

	_card_empty = _make_label(panel, "当前筛选下没有可显示的事件。\n地图保留为地区背景，不生成透明热点。", Rect2(38, 250, 304, 110), 15, MUTED)
	_card_empty.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_card_empty.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_card_empty.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_card_empty.visible = false

	var receipt := _make_panel(panel, Rect2(20, 654, 340, 126), Color("d7cfb5"), Color("6e7764"), 2, 2)
	var receipt_title := _make_label(receipt, "本区取材回条", Rect2(14, 12, 312, 26), 15, INK)
	receipt_title.add_theme_color_override("font_color", TEAL)
	_schedule_summary = _make_label(receipt, "执行中 0 · 等待选择事件", Rect2(14, 46, 312, 62), 15, INK)
	_schedule_summary.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART

func _build_map_stage() -> void:
	var shadow := _make_panel(_design_root, Rect2(MAP_RECT.position + Vector2(8, 8), MAP_RECT.size), Color(0.01, 0.04, 0.06, 0.55), Color(0.01, 0.04, 0.06, 0.0), 0, 0)
	shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var map_panel := Control.new()
	map_panel.position = MAP_RECT.position
	map_panel.size = MAP_RECT.size
	map_panel.clip_contents = true
	_design_root.add_child(map_panel)
	_map_texture = TextureRect.new()
	_map_texture.position = Vector2.ZERO
	_map_texture.size = MAP_RECT.size
	_map_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_map_texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_map_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_map_texture.texture = ManifestV2.load_asset_texture("rt2_map_base_clean")
	map_panel.add_child(_map_texture)
	var wash := ColorRect.new()
	wash.position = Vector2.ZERO
	wash.size = MAP_RECT.size
	wash.color = Color(0.02, 0.10, 0.12, 0.07)
	wash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	map_panel.add_child(wash)
	_pin_layer = Control.new()
	_pin_layer.position = Vector2.ZERO
	_pin_layer.size = MAP_RECT.size
	_pin_layer.mouse_filter = Control.MOUSE_FILTER_PASS
	map_panel.add_child(_pin_layer)
	var border := _make_panel(_design_root, MAP_RECT, Color(0, 0, 0, 0), PAPER_LIGHT, 3, 0)
	border.mouse_filter = Control.MOUSE_FILTER_IGNORE
	border.z_index = 10

func _build_dossier() -> void:
	_make_panel(_design_root, Rect2(1498, 110, 398, 946), Color(0.01, 0.04, 0.06, 0.36), Color(0, 0, 0, 0), 0, 8)
	var panel := Control.new()
	panel.position = RIGHT_RECT.position
	panel.size = RIGHT_RECT.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_design_root.add_child(panel)

	_dossier_shell_texture = TextureRect.new()
	_dossier_shell_texture.name = "DossierShellAssetV1"
	_dossier_shell_texture.position = Vector2.ZERO
	_dossier_shell_texture.size = RIGHT_RECT.size
	_dossier_shell_texture.texture = ManifestV2.load_asset_texture("rt_dossier_shell")
	_dossier_shell_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_dossier_shell_texture.stretch_mode = TextureRect.STRETCH_SCALE
	_dossier_shell_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(_dossier_shell_texture)

	_dossier_kicker = _make_label(panel, "CURRENT ASSIGNMENT / 当前任务", Rect2(24, 24, 340, 20), 13, TEAL)
	_dossier_title = _make_label(panel, "选择一份事件档案", Rect2(24, 54, 340, 58), 25, INK)
	_dossier_title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_dossier_title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	_dossier_title.max_lines_visible = 2
	_make_rule(panel, Rect2(24, 132, 340, 1), Color("87917f"))

	var summary_caption := _make_label(panel, "摘要", Rect2(24, 148, 340, 22), 16, INK)
	summary_caption.add_theme_color_override("font_color", TEAL)
	_dossier_summary = RichTextLabel.new()
	_dossier_summary.position = Vector2(24, 184)
	_dossier_summary.size = Vector2(340, 252)
	_dossier_summary.bbcode_enabled = true
	_dossier_summary.fit_content = false
	_dossier_summary.scroll_active = false
	_dossier_summary.add_theme_font_size_override("normal_font_size", 16)
	_dossier_summary.add_theme_font_size_override("bold_font_size", 16)
	_dossier_summary.add_theme_constant_override("line_separation", 5)
	_dossier_summary.add_theme_color_override("default_color", INK)
	panel.add_child(_dossier_summary)

	_dossier_meta_plate = _make_dossier_section_plate(panel, Rect2(24, 472, 364, 140), "DossierMetaPlateV1")
	var meta_title := _make_label(_dossier_meta_plate, "地点 / 耗时 / 需求", Rect2(16, 16, 332, 22), 14, TEAL)
	meta_title.add_theme_color_override("font_color", TEAL)
	_dossier_meta = _make_label(_dossier_meta_plate, "等待选择后填入任务元信息。", Rect2(16, 48, 332, 72), 15, INK)
	_dossier_meta.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART

	_dossier_risk_plate = _make_dossier_section_plate(panel, Rect2(20, 622, 372, 174), "DossierRiskPlateV1")
	_dossier_risk_accent = ColorRect.new()
	_dossier_risk_accent.position = Vector2(10, 16)
	_dossier_risk_accent.size = Vector2(3, 142)
	_dossier_risk_accent.color = MUTED
	_dossier_risk_accent.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_dossier_risk_plate.add_child(_dossier_risk_accent)
	_dossier_risk_title = _make_label(_dossier_risk_plate, "风险等级 / 依据 / 建议", Rect2(16, 16, 332, 22), 14, MUTED)
	_dossier_risk_title.add_theme_color_override("font_color", MUTED)
	_dossier_risk = _make_label(_dossier_risk_plate, "等待选择后显示风险等级、截稿与连续追踪信息。", Rect2(16, 48, 332, 70), 15, INK)
	_dossier_risk.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_dossier_risk.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	_dossier_risk.max_lines_visible = 3
	_dossier_hint = _make_label(_dossier_risk_plate, "本页选择不会消耗天数。", Rect2(16, 122, 332, 40), 13, TEAL)
	_dossier_hint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_dossier_hint.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	_dossier_hint.max_lines_visible = 2

	_dispatch_button = Button.new()
	_dispatch_button.name = "DispatchButton"
	_dispatch_button.position = Vector2(28, 820)
	_dispatch_button.size = Vector2(356, 112)
	_dispatch_button.text = "先选择任务"
	_dispatch_button.focus_mode = Control.FOCUS_ALL
	_dispatch_button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_style_dossier_asset_button(_dispatch_button, ManifestV2.load_asset_texture("rt_dispatch_cta_mother"), INK, 22)
	panel.add_child(_dispatch_button)
	_dispatch_button.pressed.connect(func() -> void: open_dispatch_requested.emit())

func _build_schedule() -> void:
	_make_panel(_design_root, Rect2(SCHEDULE_RECT.position + Vector2(8, 8), SCHEDULE_RECT.size), Color(0.01, 0.04, 0.06, 0.58), Color(0, 0, 0, 0), 0, 0)
	var panel := _make_panel(_design_root, SCHEDULE_RECT, Color("d6cfb6"), PAPER_LIGHT, 3, 5)
	_advance_button = Button.new()
	_advance_button.name = "AdvanceDayDeferredButton"
	_advance_button.position = Vector2(28, 22)
	_advance_button.size = Vector2(318, 100)
	_advance_button.text = "推进一天 · 待接入"
	_advance_button.disabled = true
	_advance_button.tooltip_text = "当前玩法层没有独立的推进一天命令，本纵向切片不伪造该功能。"
	_style_button(_advance_button, Color("b5b09a"), Color("807b69"), Color("54564f"), 20)
	panel.add_child(_advance_button)
	var schedule_title := _make_label(panel, "本周日程", Rect2(372, 22, 450, 26), 15, TEAL)
	schedule_title.add_theme_color_override("font_color", TEAL)
	var schedule_body := _make_label(panel, "选择地图事件后，右侧签批入口会启用。", Rect2(372, 52, 450, 64), 16, INK)
	schedule_body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	var preview_title := _make_label(panel, "推进后果预览", Rect2(868, 22, 520, 26), 15, RUST)
	preview_title.add_theme_color_override("font_color", RUST)
	_schedule_preview = _make_label(panel, "时间推进规则尚未接入；任务截止变化不在本轮模拟。", Rect2(868, 52, 520, 64), 15, INK)
	_schedule_preview.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART

func _rebuild_event_cards(nodes: Array) -> void:
	_clear_children(_card_list)
	_card_buttons.clear()
	_card_empty.visible = nodes.is_empty()
	for item_value in nodes:
		if typeof(item_value) != TYPE_DICTIONARY:
			continue
		var item: Dictionary = item_value
		var task_id := str(item.get("id", ""))
		if task_id.is_empty():
			continue
		var button := Button.new()
		button.name = "EventCard_%s" % task_id
		button.custom_minimum_size = Vector2(324, 104)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.focus_mode = Control.FOCUS_ALL
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
		button.add_theme_font_size_override("font_size", 15)
		button.text = "%s\n%s · %d天 · %s" % [
			str(item.get("name", item.get("label", "未命名任务"))),
			_kind_label(str(item.get("kind", "permanent"))),
			int(item.get("days", 0)),
			_type_label(str(item.get("type", ""))),
		]
		button.set_meta("task_id", task_id)
		button.set_meta("source", "payload.nodes")
		button.disabled = not bool(item.get("enabled", true))
		button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND if not button.disabled else Control.CURSOR_ARROW
		_apply_card_style(button, task_id == _selected_task_id, false, str(item.get("tone", "normal")))
		_card_list.add_child(button)
		_card_buttons[task_id] = button
		button.pressed.connect(_on_event_pressed.bind(task_id))
		button.mouse_entered.connect(_on_card_hover.bind(task_id, true))
		button.mouse_exited.connect(_on_card_hover.bind(task_id, false))

func _rebuild_event_pins(nodes: Array) -> void:
	_clear_children(_pin_layer)
	_pin_buttons.clear()
	_cluster_buttons.clear()
	_cluster_member_pins.clear()
	var occupied_positions: Array[Vector2] = []
	for group_value in _partition_dense_groups(nodes):
		var group: Array = group_value
		if group.size() >= CLUSTER_THRESHOLD:
			_create_event_cluster(group, occupied_positions)
			continue
		var reserved_label_rects: Array[Rect2] = []
		for item_value in _selected_first(group):
			if typeof(item_value) != TYPE_DICTIONARY:
				continue
			var item: Dictionary = item_value
			var anchor_position := _anchor_position_for_item(item)
			var resolved_position := _resolve_pin_position(anchor_position, occupied_positions, reserved_label_rects)
			occupied_positions.append(resolved_position)
			_create_event_pin(item, anchor_position, resolved_position, true)
			if str(item.get("id", "")) == _selected_task_id:
				reserved_label_rects.append(_label_rect_for_item(item, resolved_position))

func _selected_first(group: Array) -> Array:
	var ordered: Array = []
	for item_value in group:
		if typeof(item_value) == TYPE_DICTIONARY and str(item_value.get("id", "")) == _selected_task_id:
			ordered.append(item_value)
	for item_value in group:
		if typeof(item_value) != TYPE_DICTIONARY or str(item_value.get("id", "")) != _selected_task_id:
			ordered.append(item_value)
	return ordered

func _partition_dense_groups(nodes: Array) -> Array:
	var buckets: Dictionary = {}
	var key_order: Array[String] = []
	for item_value in nodes:
		if typeof(item_value) != TYPE_DICTIONARY:
			continue
		var item: Dictionary = item_value
		if str(item.get("id", "")).is_empty():
			continue
		var anchor := _anchor_position_for_item(item) + Vector2(36.0, 40.0)
		var key := "%d:%d" % [
			int(round(anchor.x / CLUSTER_CELL_SIZE)),
			int(round(anchor.y / CLUSTER_CELL_SIZE)),
		]
		if not buckets.has(key):
			buckets[key] = []
			key_order.append(key)
		buckets[key].append(item)
	var groups: Array = []
	for key in key_order:
		groups.append(buckets[key])
	return groups

func _anchor_position_for_item(item: Dictionary) -> Vector2:
	var map_pos: Dictionary = item.get("map_pos", {"x": 0.5, "y": 0.5})
	var ratio := Vector2(
		clampf(float(map_pos.get("x", 0.5)), 0.055, 0.945),
		clampf(float(map_pos.get("y", 0.5)), 0.055, 0.945)
	)
	return Vector2(ratio.x * MAP_RECT.size.x - 36.0, ratio.y * MAP_RECT.size.y - 40.0)

func _label_rect_for_item(item: Dictionary, pin_position: Vector2) -> Rect2:
	var map_pos: Dictionary = item.get("map_pos", {"x": 0.5, "y": 0.5})
	var ratio_x := clampf(float(map_pos.get("x", 0.5)), 0.0, 1.0)
	var local_position := Vector2(-208.0, 4.0) if ratio_x > 0.72 else Vector2(78.0, 4.0)
	return Rect2(pin_position + local_position, Vector2(200.0, 72.0))

func _create_event_pin(item: Dictionary, anchor_position: Vector2, resolved_position: Vector2, visible_now: bool, cluster_key: String = "") -> void:
	var task_id := str(item.get("id", ""))
	if task_id.is_empty():
		return
	var pin := EventPin.new()
	pin.name = "EventPin_%s" % task_id
	pin.position = resolved_position
	pin.size = Vector2(72.0, 80.0)
	pin.set_meta("anchor_position", anchor_position)
	pin.set_meta("resolved_position", resolved_position)
	pin.set_meta("cluster_key", cluster_key)
	_pin_layer.add_child(pin)
	var should_animate_selection := task_id == _selected_task_id and task_id == _pending_selection_transition_id
	pin.configure(item, task_id == _selected_task_id and not should_animate_selection)
	if should_animate_selection:
		pin.set_external_hover(true)
		_start_pin_selection_transition.call_deferred(pin, task_id)
	pin.visible = visible_now
	_pin_buttons[task_id] = pin
	pin.pressed.connect(_on_event_pressed.bind(task_id))
	pin.hover_changed.connect(_on_pin_hover_changed)

func _create_event_cluster(group: Array, occupied_positions: Array[Vector2]) -> void:
	var sum := Vector2.ZERO
	var selected_inside := false
	for item_value in group:
		var item: Dictionary = item_value
		sum += _anchor_position_for_item(item)
		selected_inside = selected_inside or str(item.get("id", "")) == _selected_task_id
	var cluster_position := sum / float(group.size())
	cluster_position.x = clampf(cluster_position.x, 0.0, MAP_RECT.size.x - 72.0)
	cluster_position.y = clampf(cluster_position.y, 0.0, MAP_RECT.size.y - 80.0)
	var cluster_key := "cluster_%d_%d" % [int(round(cluster_position.x)), int(round(cluster_position.y))]
	occupied_positions.append(cluster_position)
	var members: Array = []
	var reserved_label_rects: Array[Rect2] = []
	for item_value in _selected_first(group):
		var item: Dictionary = item_value
		var anchor_position := _anchor_position_for_item(item)
		var resolved_position := _resolve_pin_position(cluster_position, occupied_positions, reserved_label_rects)
		occupied_positions.append(resolved_position)
		_create_event_pin(item, anchor_position, resolved_position, selected_inside, cluster_key)
		members.append(_pin_buttons[str(item.get("id", ""))])
		if str(item.get("id", "")) == _selected_task_id:
			reserved_label_rects.append(_label_rect_for_item(item, resolved_position))
	_cluster_member_pins[cluster_key] = members

	var cluster_button := Button.new()
	cluster_button.name = "EventCluster_%s" % cluster_key
	cluster_button.position = cluster_position
	cluster_button.size = Vector2(72.0, 72.0)
	cluster_button.focus_mode = Control.FOCUS_ALL
	cluster_button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	cluster_button.set_meta("expanded", selected_inside)
	cluster_button.set_meta("member_count", group.size())
	cluster_button.tooltip_text = "此处有 %d 个事件，点击%s。" % [group.size(), "收拢" if selected_inside else "展开"]
	_style_cluster_button(cluster_button, selected_inside, false)
	_pin_layer.add_child(cluster_button)
	_cluster_buttons[cluster_key] = cluster_button
	cluster_button.pressed.connect(_toggle_cluster.bind(cluster_key))

func _toggle_cluster(cluster_key: String) -> void:
	var button: Button = _cluster_buttons.get(cluster_key)
	if not is_instance_valid(button):
		return
	var expanded := not bool(button.get_meta("expanded", false))
	button.set_meta("expanded", expanded)
	for pin_value in _cluster_member_pins.get(cluster_key, []):
		if is_instance_valid(pin_value):
			pin_value.visible = expanded
	button.tooltip_text = "此处有 %d 个事件，点击%s。" % [int(button.get_meta("member_count", 0)), "收拢" if expanded else "展开"]
	_style_cluster_button(button, expanded, false)

func _style_cluster_button(button: Button, expanded: bool, hovered_member: bool) -> void:
	var accent := TEAL if expanded or hovered_member else OLIVE
	var normal := _style_box(Color("d6d1b4") if expanded else PAPER_LIGHT, accent if expanded else INK, 3, 8)
	normal.corner_radius_top_left = 13
	normal.corner_radius_top_right = 19
	normal.corner_radius_bottom_right = 12
	normal.corner_radius_bottom_left = 17
	normal.corner_detail = 2
	normal.shadow_color = Color(0.01, 0.03, 0.04, 0.34)
	normal.shadow_size = 3
	normal.shadow_offset = Vector2(3.0, 3.0)
	var hover: StyleBoxFlat = normal.duplicate()
	hover.bg_color = Color("d9d5b5").lightened(0.035)
	hover.border_color = accent
	hover.set_border_width_all(4)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", hover)
	button.add_theme_stylebox_override("focus", hover)
	button.add_theme_color_override("font_color", INK)
	button.add_theme_color_override("font_hover_color", INK)
	button.add_theme_color_override("font_pressed_color", INK)
	button.add_theme_color_override("font_focus_color", INK)
	button.add_theme_font_size_override("font_size", 19)
	button.text = str(button.get_meta("member_count", 0))

func _resolve_pin_position(anchor_position: Vector2, occupied_positions: Array[Vector2], reserved_label_rects: Array[Rect2] = []) -> Vector2:
	var offsets: Array[Vector2] = [
		Vector2.ZERO,
		Vector2(78, 0), Vector2(-78, 0), Vector2(0, 82), Vector2(0, -82),
		Vector2(62, 62), Vector2(-62, 62), Vector2(62, -62), Vector2(-62, -62),
		Vector2(156, 0), Vector2(-156, 0), Vector2(0, 164), Vector2(0, -164),
	]
	for offset in offsets:
		var candidate := anchor_position + offset
		candidate.x = clampf(candidate.x, 0.0, MAP_RECT.size.x - 72.0)
		candidate.y = clampf(candidate.y, 0.0, MAP_RECT.size.y - 80.0)
		var clear := true
		for occupied in occupied_positions:
			if candidate.distance_to(occupied) < 72.0:
				clear = false
				break
		if clear:
			var candidate_rect := Rect2(candidate, Vector2(72.0, 80.0))
			for reserved_rect in reserved_label_rects:
				if reserved_rect.grow(8.0).intersects(candidate_rect):
					clear = false
					break
		if clear:
			return candidate
	return Vector2(
		clampf(anchor_position.x, 0.0, MAP_RECT.size.x - 72.0),
		clampf(anchor_position.y, 0.0, MAP_RECT.size.y - 80.0)
	)

func _render_dossier(payload: Dictionary) -> void:
	var has_selection := not _selected_task_id.is_empty()
	_dossier_title.text = str(payload.get("node_title", "选择一份事件档案"))
	if has_selection:
		var summary := str(payload.get("region_node_summary", "暂无摘要。"))
		_dossier_summary.text = "[color=#18282d]%s[/color]" % summary
		_dossier_meta.text = str(payload.get("region_node_meta", "任务元信息暂缺。"))
		var risk_lines: Array[String] = []
		var risk_level := str(payload.get("region_node_risk_level", "未评估"))
		var risk_color := _dossier_risk_color(risk_level)
		_dossier_risk_title.add_theme_color_override("font_color", risk_color)
		_dossier_risk_accent.color = risk_color
		risk_lines.append("风险等级：%s" % risk_level)
		var deadline := str(payload.get("region_node_deadline", ""))
		var chain := str(payload.get("region_node_chain", ""))
		if not deadline.is_empty():
			risk_lines.append("截稿：%s" % deadline)
		if not chain.is_empty():
			risk_lines.append(chain)
		if deadline.is_empty() and chain.is_empty():
			risk_lines.append("常规调查 · 无额外截稿或链条提示")
		_dossier_risk.text = "\n".join(risk_lines)
		_dossier_hint.text = str(payload.get("region_node_recommendation", payload.get("region_action_hint", "本页选择不会消耗天数。")))
	else:
		_dossier_risk_title.add_theme_color_override("font_color", MUTED)
		_dossier_risk_accent.color = MUTED
		_dossier_summary.text = "[color=#59645f]选择左侧任务卡或地图图钉。地图地标只用于辨认地区，不可点击。[/color]"
		_dossier_meta.text = "等待选择后填入任务元信息。"
		_dossier_risk.text = "等待选择后显示风险等级、截稿与连续追踪信息。"
		_dossier_hint.text = "本页选择不会消耗天数。"
	var can_open := has_selection and bool(payload.get("dispatch_open_enabled", false))
	_dispatch_button.disabled = not can_open
	_dispatch_button.text = str(payload.get("dispatch_open_text", "送至签批台" if can_open else "先选择任务"))
	_dispatch_button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND if can_open else Control.CURSOR_ARROW

func _dossier_risk_color(risk_level: String) -> Color:
	var normalized := risk_level.strip_edges().to_lower()
	if normalized in ["高", "high", "critical"]:
		return RUST
	if normalized in ["中", "medium", "moderate"]:
		return Color("b47d35")
	if normalized in ["低", "low"]:
		return TEAL
	return MUTED

func _render_schedule(payload: Dictionary, nodes: Array) -> void:
	var enabled_count := 0
	for item_value in nodes:
		if typeof(item_value) == TYPE_DICTIONARY and bool(item_value.get("enabled", true)):
			enabled_count += 1
	_schedule_summary.text = "执行中 0 · 本区可处理 %d · %s" % [
		enabled_count,
		"已选 1" if not _selected_task_id.is_empty() else "等待选择",
	]
	_schedule_preview.text = "剩余 %d 天 · 时间推进规则尚未接入；本轮只验证事件选择与派遣闭环。" % int(payload.get("remaining_days", 0))

func _on_event_pressed(task_id: String) -> void:
	if task_id.is_empty():
		return
	_pending_selection_transition_id = task_id
	node_selected.emit(task_id)

func _start_pin_selection_transition(pin: Control, task_id: String) -> void:
	if not is_instance_valid(pin):
		return
	pin.call("set_selected", true, true)
	await get_tree().create_timer(0.096).timeout
	if is_instance_valid(pin):
		pin.call("set_external_hover", task_id == _hovered_task_id)

func _on_card_hover(task_id: String, hovering: bool) -> void:
	_hovered_task_id = task_id if hovering else ""
	if _pin_buttons.has(task_id):
		var pin = _pin_buttons[task_id]
		pin.call("set_external_hover", hovering)
		var cluster_key := str(pin.get_meta("cluster_key", ""))
		if not cluster_key.is_empty() and _cluster_buttons.has(cluster_key):
			var cluster_button: Button = _cluster_buttons[cluster_key]
			_style_cluster_button(cluster_button, bool(cluster_button.get_meta("expanded", false)), hovering)
	if _card_buttons.has(task_id):
		var item := _find_node(task_id)
		_apply_card_style(_card_buttons[task_id], task_id == _selected_task_id, hovering, str(item.get("tone", "normal")))

func _on_pin_hover_changed(task_id: String, hovering: bool) -> void:
	_hovered_task_id = task_id if hovering else ""
	if _card_buttons.has(task_id):
		var item := _find_node(task_id)
		_apply_card_style(_card_buttons[task_id], task_id == _selected_task_id, hovering, str(item.get("tone", "normal")))

func _find_node(task_id: String) -> Dictionary:
	for item_value in _payload.get("nodes", []):
		if typeof(item_value) == TYPE_DICTIONARY and str(item_value.get("id", "")) == task_id:
			return item_value
	return {}

func _apply_card_style(button: Button, selected: bool, hovered: bool, tone: String) -> void:
	var accent := OLIVE
	if tone == "deadline":
		accent = RUST
	elif tone == "chain":
		accent = TEAL
	elif tone == "locked":
		accent = MUTED
	var base := PAPER_LIGHT if not selected else Color("cbd09f")
	if hovered and not selected:
		base = Color("e0d8bc")
	var style := _style_box(base, accent if selected or hovered else Color("788078"), 2 if selected or hovered else 1, 3)
	style.content_margin_left = 16
	style.content_margin_right = 12
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	var hover_style: StyleBoxFlat = style.duplicate()
	hover_style.bg_color = base.lightened(0.035)
	var pressed_style: StyleBoxFlat = style.duplicate()
	pressed_style.bg_color = base.darkened(0.055)
	var disabled_style: StyleBoxFlat = style.duplicate()
	disabled_style.bg_color = Color("bcb8a7")
	disabled_style.border_color = Color("77776e")
	button.add_theme_stylebox_override("normal", style)
	button.add_theme_stylebox_override("hover", hover_style)
	button.add_theme_stylebox_override("pressed", pressed_style)
	button.add_theme_stylebox_override("focus", hover_style)
	button.add_theme_stylebox_override("disabled", disabled_style)
	button.add_theme_color_override("font_color", INK)
	button.add_theme_color_override("font_hover_color", INK)
	button.add_theme_color_override("font_pressed_color", INK)
	button.add_theme_color_override("font_focus_color", INK)
	button.add_theme_color_override("font_disabled_color", Color("686a65"))

func _make_dossier_section_plate(parent: Control, rect: Rect2, node_name: String) -> NinePatchRect:
	var plate := NinePatchRect.new()
	plate.name = node_name
	plate.position = rect.position
	plate.size = rect.size
	plate.texture = ManifestV2.load_asset_texture("rt_dossier_section_plate")
	plate.patch_margin_left = 48
	plate.patch_margin_top = 48
	plate.patch_margin_right = 72
	plate.patch_margin_bottom = 48
	plate.axis_stretch_horizontal = NinePatchRect.AXIS_STRETCH_MODE_STRETCH
	plate.axis_stretch_vertical = NinePatchRect.AXIS_STRETCH_MODE_STRETCH
	plate.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(plate)
	return plate

func _style_dossier_asset_button(button: Button, texture: Texture2D, font_color: Color, font_size: int) -> void:
	var normal := StyleBoxTexture.new()
	normal.texture = texture
	normal.texture_margin_left = 48
	normal.texture_margin_top = 36
	normal.texture_margin_right = 48
	normal.texture_margin_bottom = 36
	normal.content_margin_left = 40
	normal.content_margin_right = 40
	normal.content_margin_top = 22
	normal.content_margin_bottom = 22
	var hover: StyleBoxTexture = normal.duplicate()
	hover.modulate_color = Color("f4f6d7")
	var pressed: StyleBoxTexture = normal.duplicate()
	pressed.modulate_color = Color("d7d9b7")
	var disabled_style: StyleBoxTexture = normal.duplicate()
	disabled_style.modulate_color = Color("aeb09d")
	var focus: StyleBoxTexture = normal.duplicate()
	focus.modulate_color = Color("fffbd8")
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("focus", focus)
	button.add_theme_stylebox_override("disabled", disabled_style)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_focus_color", font_color)
	button.add_theme_color_override("font_disabled_color", Color("555b50"))
	button.add_theme_font_size_override("font_size", font_size)

func _style_button(button: Button, bg: Color, border: Color, font_color: Color, font_size: int) -> void:
	var style := _style_box(bg, border, 3, 2)
	style.shadow_color = Color(0.01, 0.03, 0.04, 0.34)
	style.shadow_size = 4
	var hover: StyleBoxFlat = style.duplicate()
	hover.bg_color = bg.lightened(0.07)
	var pressed: StyleBoxFlat = style.duplicate()
	pressed.bg_color = bg.darkened(0.08)
	var disabled_style: StyleBoxFlat = style.duplicate()
	disabled_style.bg_color = bg
	button.add_theme_stylebox_override("normal", style)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("focus", hover)
	button.add_theme_stylebox_override("disabled", disabled_style)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_focus_color", font_color)
	button.add_theme_color_override("font_disabled_color", font_color)
	button.add_theme_font_size_override("font_size", font_size)

func _make_panel(parent: Control, rect: Rect2, bg: Color, border: Color, border_width: int, shadow_size: int) -> Panel:
	var panel := Panel.new()
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := _style_box(bg, border, border_width, 2)
	if shadow_size > 0:
		style.shadow_color = Color(0.01, 0.03, 0.04, 0.34)
		style.shadow_size = shadow_size
	panel.add_theme_stylebox_override("panel", style)
	parent.add_child(panel)
	return panel

func _make_label(parent: Control, text_value: String, rect: Rect2, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.position = rect.position
	label.size = rect.size
	label.text = text_value
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	parent.add_child(label)
	return label

func _make_rule(parent: Control, rect: Rect2, color: Color) -> ColorRect:
	var rule := ColorRect.new()
	rule.position = rect.position
	rule.size = rect.size
	rule.color = color
	rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(rule)
	return rule

func _style_box(bg: Color, border: Color, width: int, radius: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(width)
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius + 2
	style.corner_radius_bottom_left = radius + 1
	style.corner_radius_bottom_right = radius
	return style

func _clear_children(parent: Node) -> void:
	for child in parent.get_children():
		parent.remove_child(child)
		child.queue_free()

func _update_design_transform() -> void:
	if not is_instance_valid(_design_root) or size.x <= 0.0 or size.y <= 0.0:
		return
	var fit_scale := minf(size.x / REFERENCE_SIZE.x, size.y / REFERENCE_SIZE.y)
	_design_root.scale = Vector2(fit_scale, fit_scale)
	_design_root.position = (size - REFERENCE_SIZE * fit_scale) * 0.5
	queue_redraw()

func _kind_label(kind: String) -> String:
	match kind:
		"temp":
			return "截稿"
		"chain":
			return "追踪"
		"hidden":
			return "异常"
		_:
			return "常驻"

func _type_label(type_id: String) -> String:
	match type_id:
		"sci":
			return "纪实"
		"occult":
			return "玄学"
		"pop":
			return "热点"
		_:
			return type_id
