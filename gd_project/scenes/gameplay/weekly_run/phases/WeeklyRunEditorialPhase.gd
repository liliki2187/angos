extends MarginContainer

signal article_selected(article_id)
signal slot_selected(slot_id)
signal slot_cleared(slot_id)
signal transfer_requested(source_kind, article_id, source_slot_id, destination_kind, destination_slot_id)
signal held_article_cancelled
signal clear_layout_requested
signal settle_requested

const EditorialAssets := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunEditorialAssetManifest.gd")
const EditorialDragButton := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunEditorialDragButton.gd")
const EditorialCandidateDropZone := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunEditorialCandidateDropZone.gd")

const COLOR_DARK_BOARD := Color("041925")
const COLOR_PANEL := Color("0b1e28")
const COLOR_PANEL_ALT := Color("102936")
const COLOR_OLIVE := Color("7e8a48")
const COLOR_OLIVE_MID := Color("636936")
const COLOR_COBALT := Color("263951")
const COLOR_TEAL := Color("455b69")
const COLOR_RUST := Color("886b42")
const COLOR_PAPER := Color("b49365")
const COLOR_PAPER_LIGHT := Color("d3b37c")
const COLOR_IVORY := Color("d8d0bd")
const COLOR_INK := Color("10191d")
const COLOR_MUTED := Color("829097")

const OVERVIEW_EDITION_WIDTH := 1040.0
const PAGE_SIZE := Vector2(490.0, 800.0)
const HEADLINE_SINGLE_WIDTH_RATIO := 0.92
const HEADLINE_HORIZONTAL_RESERVE := 6.0
const HEADLINE_VERTICAL_RESERVE := 2.0
const HEADLINE_SIZE_STEPS := {
	"main": {"single": [32, 29, 26], "double": [24, 22]},
	"secondary": {"single": [25, 22, 20], "double": [18, 17]},
	"standard": {"single": [18, 16], "double": [14]},
}

var _payload: Dictionary = {}
var _confirmation_open := false
var _publishing := false
var _article_buttons: Array[Button] = []
var _slot_nodes: Dictionary = {}
var _page_nodes: Dictionary = {}
var _focused_slot_id := ""
var _replace_target_slot_id := ""
var _drag_active := false
var _drag_source: Dictionary = {}
var _drag_hover_kind := ""
var _drag_hover_slot_id := ""

var _root_vbox: VBoxContainer
var _status_bar: PanelContainer
var _status_title: Label
var _workspace: HBoxContainer
var _candidate_panel: PanelContainer
var _candidate_list: VBoxContainer
var _edition_panel: PanelContainer
var _edition_canvas: Control
var _masthead: PanelContainer
var _review_panel: PanelContainer
var _review_title: Label
var _review_headline: Label
var _review_outcome: Label
var _review_risk: Label
var _primary_action: Button
var _clear_action: Button
var _confirmation_plate: PanelContainer
var _confirmation_label: Label
var _confirmation_back: Button
var _confirmation_confirm: Button
var _context_replace_button: Button


func _ready() -> void:
	add_theme_constant_override("margin_left", 56)
	add_theme_constant_override("margin_top", 4)
	add_theme_constant_override("margin_right", 56)
	add_theme_constant_override("margin_bottom", 44)
	_build_interface()
	_apply_dual_page_geometry()


func render(payload: Dictionary) -> void:
	_payload = payload.duplicate(true)
	_rebuild_candidate_list()
	_refresh_pages()
	_refresh_review()
	_refresh_status()


func _unhandled_input(event: InputEvent) -> void:
	if not visible or _confirmation_open or _publishing:
		return
	if event.is_action_pressed("ui_cancel"):
		var had_transient := _has_local_transient() or int(_payload.get("held_article_id", -1)) != -1
		_cancel_transients()
		if int(_payload.get("held_article_id", -1)) != -1:
			held_article_cancelled.emit()
		if had_transient:
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed and (_has_local_transient() or int(_payload.get("held_article_id", -1)) != -1):
		_cancel_transients()
		if int(_payload.get("held_article_id", -1)) != -1:
			held_article_cancelled.emit()


func show_confirmation() -> void:
	_cancel_transients()
	if int(_payload.get("held_article_id", -1)) != -1:
		held_article_cancelled.emit()
	_confirmation_open = true
	_refresh_interaction_lock()
	_refresh_review()


func _build_interface() -> void:
	_root_vbox = VBoxContainer.new()
	_root_vbox.name = "EditorialRoot"
	_root_vbox.add_theme_constant_override("separation", 20)
	add_child(_root_vbox)

	_status_bar = PanelContainer.new()
	_status_bar.name = "EditorialStatusBar"
	_status_bar.custom_minimum_size = Vector2(1760, 52)
	_status_bar.add_theme_stylebox_override("panel", _flat_style(COLOR_DARK_BOARD, COLOR_OLIVE_MID, 1, 2, 10))
	_root_vbox.add_child(_status_bar)
	var status_row := HBoxContainer.new()
	status_row.add_theme_constant_override("separation", 16)
	_status_bar.add_child(status_row)
	_status_title = _label("第 1 期 · 发刊排版", 21, COLOR_IVORY)
	_status_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	status_row.add_child(_status_title)

	_workspace = HBoxContainer.new()
	_workspace.name = "EditorialWorkspace"
	_workspace.custom_minimum_size = Vector2(1760, 920)
	_workspace.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_workspace.add_theme_constant_override("separation", 20)
	_root_vbox.add_child(_workspace)

	_build_candidate_panel()
	_build_edition_panel()
	_build_review_panel()


func _build_candidate_panel() -> void:
	_candidate_panel = EditorialCandidateDropZone.new()
	_candidate_panel.name = "CandidatePool"
	_candidate_panel.custom_minimum_size = Vector2(320, 920)
	_candidate_panel.add_theme_stylebox_override("panel", _flat_style(COLOR_PANEL, COLOR_TEAL, 1, 2, 0))
	_workspace.add_child(_candidate_panel)
	_candidate_panel.drag_hovered.connect(_on_drag_hovered)
	_candidate_panel.drag_exited.connect(_on_drag_exited)
	_candidate_panel.article_dropped.connect(_on_article_dropped)
	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 16)
	margin.add_theme_constant_override("margin_top", 18)
	margin.add_theme_constant_override("margin_right", 16)
	margin.add_theme_constant_override("margin_bottom", 18)
	_candidate_panel.add_child(margin)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 12)
	margin.add_child(column)
	column.add_child(_label("候选报道", 23, COLOR_IVORY))
	var rule := HSeparator.new()
	rule.modulate = COLOR_OLIVE
	column.add_child(rule)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(scroll)
	_candidate_list = VBoxContainer.new()
	_candidate_list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_candidate_list.add_theme_constant_override("separation", 12)
	scroll.add_child(_candidate_list)


func _build_edition_panel() -> void:
	_edition_panel = PanelContainer.new()
	_edition_panel.name = "EditionWorkspace"
	_edition_panel.custom_minimum_size = Vector2(OVERVIEW_EDITION_WIDTH, 920)
	_edition_panel.add_theme_stylebox_override("panel", _flat_style(COLOR_DARK_BOARD, Color("243843"), 1, 0, 0))
	_workspace.add_child(_edition_panel)
	_edition_canvas = Control.new()
	_edition_canvas.name = "EditionCanvas"
	_edition_canvas.custom_minimum_size = Vector2(OVERVIEW_EDITION_WIDTH, 920)
	_edition_canvas.clip_contents = true
	_edition_panel.add_child(_edition_canvas)

	_build_masthead()

	_page_nodes.left = _make_page("left")
	_page_nodes.right = _make_page("right")
	_edition_canvas.add_child(_page_nodes.left)
	_edition_canvas.add_child(_page_nodes.right)

	_context_replace_button = Button.new()
	_context_replace_button.name = "ContextReplaceButton"
	_context_replace_button.text = "换稿"
	_context_replace_button.tooltip_text = "为当前版位选择另一篇报道"
	_context_replace_button.size = Vector2(44, 44)
	_context_replace_button.visible = false
	_context_replace_button.z_index = 50
	_context_replace_button.add_theme_font_size_override("font_size", 12)
	_style_button(_context_replace_button, false)
	_context_replace_button.pressed.connect(_on_context_replace_pressed)
	_edition_canvas.add_child(_context_replace_button)


func _build_masthead() -> void:
	_masthead = PanelContainer.new()
	_masthead.name = "EditionMasthead"
	_masthead.position = Vector2(15, 16)
	_masthead.size = Vector2(1010, 56)
	_masthead.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_masthead.add_theme_stylebox_override("panel", _flat_style(COLOR_PANEL, COLOR_COBALT, 1, 0, 0))
	_edition_canvas.add_child(_masthead)

	var canvas := Control.new()
	canvas.custom_minimum_size = Vector2(1010, 56)
	canvas.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_masthead.add_child(canvas)

	_add_masthead_ellipse(canvas, Vector2(30, 28), Vector2(14, 14), COLOR_OLIVE, 2.0)
	_add_masthead_ellipse(canvas, Vector2(30, 28), Vector2(6, 14), COLOR_OLIVE, 1.0)
	_add_masthead_ellipse(canvas, Vector2(30, 28), Vector2(14, 6), COLOR_OLIVE, 1.0)

	var chinese_title := _label("世界未解之谜周刊", 26, COLOR_IVORY)
	chinese_title.position = Vector2(56, 7)
	chinese_title.size = Vector2(300, 42)
	chinese_title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	chinese_title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(chinese_title)

	var english_title := _label("WORLD MYSTERY WEEKLY", 12, COLOR_MUTED)
	english_title.position = Vector2(380, 18)
	english_title.size = Vector2(194, 20)
	english_title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	english_title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(english_title)

	var rule := ColorRect.new()
	rule.position = Vector2(596, 27)
	rule.size = Vector2(224, 2)
	rule.color = COLOR_OLIVE_MID
	rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(rule)

	var swatch_colors := [COLOR_OLIVE, COLOR_COBALT, COLOR_RUST]
	for index in range(swatch_colors.size()):
		var swatch := ColorRect.new()
		swatch.position = Vector2(844 + index * 22, 20)
		swatch.size = Vector2(14, 16)
		swatch.color = swatch_colors[index]
		swatch.mouse_filter = Control.MOUSE_FILTER_IGNORE
		canvas.add_child(swatch)

	var monogram := _label("WMW", 16, COLOR_PAPER_LIGHT)
	monogram.position = Vector2(928, 14)
	monogram.size = Vector2(66, 28)
	monogram.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	monogram.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	monogram.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(monogram)

	var baseline := ColorRect.new()
	baseline.position = Vector2(0, 53)
	baseline.size = Vector2(1010, 3)
	baseline.color = COLOR_OLIVE_MID
	baseline.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(baseline)


func _add_masthead_ellipse(parent: Control, center: Vector2, radii: Vector2, color: Color, width: float) -> void:
	var line := Line2D.new()
	var points := PackedVector2Array()
	for index in range(32):
		var angle := TAU * float(index) / 32.0
		points.append(center + Vector2(cos(angle) * radii.x, sin(angle) * radii.y))
	line.points = points
	line.closed = true
	line.default_color = color
	line.width = width
	line.antialiased = true
	parent.add_child(line)


func _make_page(page_id: String) -> PanelContainer:
	var page := PanelContainer.new()
	page.name = "MainPage" if page_id == "left" else "SecondaryPage"
	page.size = PAGE_SIZE
	page.pivot_offset = PAGE_SIZE * 0.5
	var page_bg := Color("aa916b")
	page.add_theme_stylebox_override("panel", _flat_style(page_bg, COLOR_PAPER_LIGHT, 2, 2, 0))
	var canvas := Control.new()
	canvas.custom_minimum_size = PAGE_SIZE
	page.add_child(canvas)
	var header := PanelContainer.new()
	header.position = Vector2(24, 24)
	header.size = Vector2(442, 52)
	header.mouse_filter = Control.MOUSE_FILTER_IGNORE
	header.add_theme_stylebox_override("panel", _flat_style(Color(0.08, 0.10, 0.08, 0.18), Color(0.15, 0.20, 0.16, 0.32), 1, 2, 10))
	var header_color := COLOR_IVORY if page_id == "left" else Color(COLOR_IVORY.r, COLOR_IVORY.g, COLOR_IVORY.b, 0.82)
	var header_label := _label("第 1 版 · 主头版页" if page_id == "left" else "第 2 版 · 副头版页", 18 if page_id == "left" else 16, header_color)
	header_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	header_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	header.add_child(header_label)
	canvas.add_child(header)
	if page_id == "left":
		_make_slot(canvas, "front-main", Vector2(24, 92), Vector2(442, 374), "main")
		_make_slot(canvas, "feature-1", Vector2(24, 486), Vector2(213, 282), "compact")
		_make_slot(canvas, "feature-2", Vector2(253, 486), Vector2(213, 282), "compact")
	else:
		_make_slot(canvas, "front-side", Vector2(24, 92), Vector2(442, 342), "secondary")
		_make_slot(canvas, "inner-1", Vector2(24, 454), Vector2(213, 314), "tall")
		_make_slot(canvas, "inner-2", Vector2(253, 454), Vector2(213, 314), "tall")
	return page


func _make_slot(parent: Control, slot_id: String, position: Vector2, size: Vector2, role: String) -> void:
	var root := Control.new()
	root.name = slot_id.replace("-", "_")
	root.position = position
	root.size = size
	root.set_meta("slot_id", slot_id)
	root.set_meta("role", role)
	parent.add_child(root)

	var background := PanelContainer.new()
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	background.add_theme_stylebox_override("panel", _slot_style(role, false, false))
	root.add_child(background)

	var base_texture: TextureRect
	var story_texture: TextureRect
	var story_fallback: ColorRect
	var story_frame: PanelContainer
	var story_article_id := -1
	if role == "main":
		base_texture = TextureRect.new()
		base_texture.name = "GeneratedMainHeadShell"
		base_texture.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		base_texture.texture = EditorialAssets.load_texture("editorial_main_head_slot_base")
		base_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		base_texture.stretch_mode = TextureRect.STRETCH_SCALE
		base_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(base_texture)
		story_texture = TextureRect.new()
		story_texture.name = "GeneratedM330Story"
		story_texture.position = Vector2(16, 92)
		story_texture.size = Vector2(410, 218)
		story_texture.texture = EditorialAssets.load_texture("editorial_story_m330_last_train")
		story_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		story_texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		story_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(story_texture)
		story_article_id = 1001
	elif role == "secondary":
		base_texture = TextureRect.new()
		base_texture.name = "GeneratedSecondaryHeadShell"
		base_texture.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		base_texture.texture = EditorialAssets.load_texture("editorial_secondary_head_slot_base")
		base_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		base_texture.stretch_mode = TextureRect.STRETCH_SCALE
		base_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(base_texture)

		story_fallback = ColorRect.new()
		story_fallback.name = "SecondaryStoryFallback"
		story_fallback.position = Vector2(16, 78)
		story_fallback.size = Vector2(410, 210)
		story_fallback.color = COLOR_COBALT
		story_fallback.mouse_filter = Control.MOUSE_FILTER_IGNORE
		story_fallback.visible = false
		root.add_child(story_fallback)

		story_texture = TextureRect.new()
		story_texture.name = "GeneratedArea51Story"
		story_texture.position = Vector2(16, 78)
		story_texture.size = Vector2(410, 210)
		story_texture.texture = EditorialAssets.load_texture("editorial_story_area51_breathing_sign")
		story_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		story_texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		story_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		story_texture.visible = false
		root.add_child(story_texture)
		story_article_id = 1002

		story_frame = PanelContainer.new()
		story_frame.name = "StoryFrame"
		story_frame.position = Vector2(16, 78)
		story_frame.size = Vector2(410, 210)
		story_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
		story_frame.add_theme_stylebox_override("panel", _flat_style(Color(0, 0, 0, 0), COLOR_PAPER_LIGHT, 1, 0, 0))
		story_frame.visible = false
		root.add_child(story_frame)
	else:
		story_fallback = ColorRect.new()
		story_fallback.name = "StoryColorBlock"
		story_fallback.position = Vector2(12, 64 if role == "compact" else 74)
		story_fallback.size = Vector2(189, 170 if role == "compact" else 174)
		story_fallback.color = COLOR_TEAL if slot_id.hash() % 2 == 0 else COLOR_OLIVE_MID
		story_fallback.mouse_filter = Control.MOUSE_FILTER_IGNORE
		story_fallback.visible = false
		root.add_child(story_fallback)

		story_texture = TextureRect.new()
		story_texture.name = "StoryTexture"
		story_texture.position = story_fallback.position
		story_texture.size = story_fallback.size
		story_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		story_texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		story_texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		story_texture.visible = false
		root.add_child(story_texture)

	var title := _label("空版位", 24 if role == "main" else 18 if role == "secondary" else 14, COLOR_INK)
	title.name = "Headline"
	var title_carrier: Control
	if role in ["main", "secondary"]:
		title_carrier = Control.new()
		title_carrier.name = "HeadlineCarrier"
		title_carrier.position = Vector2(16, 14)
		title_carrier.size = Vector2(410, 68 if role == "main" else 54)
		title_carrier.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(title_carrier)
		title.position = Vector2(8, 0)
		title.size = Vector2(394, 68 if role == "main" else 54)
		title_carrier.add_child(title)
	else:
		title.position = Vector2(12, 8)
		title.size = Vector2(size.x - 24, 48 if role == "compact" else 50)
		root.add_child(title)
	# 中文标题通常没有空格分词，按任意字符换行才能真正利用两行标题安全区。
	title.autowrap_mode = TextServer.AUTOWRAP_ARBITRARY
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	title.max_lines_visible = 2
	title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	title.add_theme_constant_override("line_spacing", 0)
	title.clip_text = true
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var meta := _label("等待报道", 13 if role in ["main", "secondary"] else 12, COLOR_INK)
	meta.name = "Meta"
	var meta_carrier: Control
	if role == "main":
		meta.position = Vector2(16, 318)
		meta.size = Vector2(360, 42)
	elif role == "secondary":
		meta_carrier = Control.new()
		meta_carrier.name = "MetaCarrier"
		meta_carrier.position = Vector2(16, 300)
		meta_carrier.size = Vector2(360, 30)
		meta_carrier.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(meta_carrier)
		meta.position = Vector2(8, 0)
		meta.size = Vector2(344, 30)
		meta_carrier.add_child(meta)
	elif role == "compact":
		meta.position = Vector2(12, 244)
		meta.size = Vector2(137, 24)
	else:
		meta.position = Vector2(12, 260)
		meta.size = Vector2(137, 26)
	meta.clip_text = true
	meta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if role != "secondary":
		root.add_child(meta)

	var target := EditorialDragButton.new()
	target.name = "SlotTarget"
	target.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	target.text = ""
	target.focus_mode = Control.FOCUS_ALL
	target.z_index = 10
	_style_transparent_target(target, COLOR_OLIVE, 2)
	target.pressed.connect(func() -> void: _on_slot_pressed(slot_id))
	target.configure_drop_target("slot", slot_id)
	target.drag_started.connect(_on_drag_started)
	target.drag_finished.connect(_on_drag_finished)
	target.drag_hovered.connect(_on_drag_hovered)
	target.drag_exited.connect(_on_drag_exited)
	target.article_dropped.connect(_on_article_dropped)
	root.add_child(target)

	var status_inner := PanelContainer.new()
	status_inner.name = "StatusInnerFrame"
	status_inner.position = Vector2(4, 4)
	status_inner.size = size - Vector2(8, 8)
	status_inner.mouse_filter = Control.MOUSE_FILTER_IGNORE
	status_inner.z_index = 11
	status_inner.visible = false
	root.add_child(status_inner)

	_slot_nodes[slot_id] = {
		"root": root,
		"background": background,
		"base_texture": base_texture,
		"story_texture": story_texture,
		"story_fallback": story_fallback,
		"story_frame": story_frame,
		"story_article_id": story_article_id,
		"title_carrier": title_carrier,
		"meta_carrier": meta_carrier,
		"title": title,
		"meta": meta,
		"target": target,
		"status_inner": status_inner,
		"role": role,
		"size": size,
	}


func _build_review_panel() -> void:
	_review_panel = PanelContainer.new()
	_review_panel.name = "SignoffPanel"
	_review_panel.custom_minimum_size = Vector2(360, 920)
	_review_panel.add_theme_stylebox_override("panel", _flat_style(Color("12252c"), COLOR_PAPER, 1, 2, 0))
	_workspace.add_child(_review_panel)
	var canvas := Control.new()
	canvas.custom_minimum_size = Vector2(360, 920)
	_review_panel.add_child(canvas)

	_review_title = _label("发刊复核", 24, COLOR_IVORY)
	_review_title.position = Vector2(16, 16)
	_review_title.size = Vector2(328, 48)
	canvas.add_child(_review_title)

	_review_headline = _review_card(canvas, Vector2(16, 80), Vector2(328, 126), "主头版")
	_review_outcome = _review_card(canvas, Vector2(16, 222), Vector2(328, 104), "预计结果")
	_review_risk = _review_card(canvas, Vector2(16, 342), Vector2(328, 132), "风险 / 阻断")

	_clear_action = Button.new()
	_clear_action.position = Vector2(16, 768)
	_clear_action.size = Vector2(328, 42)
	_clear_action.text = "清空双版"
	_style_button(_clear_action, false)
	_clear_action.pressed.connect(func() -> void: clear_layout_requested.emit())
	canvas.add_child(_clear_action)

	_primary_action = Button.new()
	_primary_action.position = Vector2(16, 824)
	_primary_action.size = Vector2(328, 72)
	_primary_action.text = "签批送印"
	_primary_action.add_theme_font_size_override("font_size", 21)
	_style_button(_primary_action, true)
	_primary_action.pressed.connect(_on_primary_action)
	canvas.add_child(_primary_action)

	_confirmation_plate = PanelContainer.new()
	_confirmation_plate.name = "ConfirmationPlate"
	_confirmation_plate.position = Vector2(16, 472)
	_confirmation_plate.size = Vector2(328, 392)
	_confirmation_plate.visible = false
	_confirmation_plate.z_index = 28
	_confirmation_plate.add_theme_stylebox_override("panel", _flat_style(Color("d0b27d"), COLOR_RUST, 3, 2, 0))
	canvas.add_child(_confirmation_plate)
	var confirm_canvas := Control.new()
	confirm_canvas.custom_minimum_size = Vector2(328, 392)
	_confirmation_plate.add_child(confirm_canvas)
	_confirmation_label = _label("", 15, COLOR_INK)
	_confirmation_label.position = Vector2(16, 16)
	_confirmation_label.size = Vector2(296, 250)
	_confirmation_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	confirm_canvas.add_child(_confirmation_label)
	_confirmation_back = Button.new()
	_confirmation_back.position = Vector2(16, 278)
	_confirmation_back.size = Vector2(128, 42)
	_confirmation_back.text = "返回修改"
	_style_button(_confirmation_back, false)
	_confirmation_back.pressed.connect(_close_confirmation)
	confirm_canvas.add_child(_confirmation_back)
	_confirmation_confirm = Button.new()
	_confirmation_confirm.position = Vector2(16, 326)
	_confirmation_confirm.size = Vector2(296, 52)
	_confirmation_confirm.text = "确认送印"
	_style_button(_confirmation_confirm, true)
	_confirmation_confirm.pressed.connect(_confirm_publish)
	confirm_canvas.add_child(_confirmation_confirm)


func _review_card(parent: Control, position: Vector2, size: Vector2, heading: String) -> Label:
	var panel := PanelContainer.new()
	panel.position = position
	panel.size = size
	panel.add_theme_stylebox_override("panel", _flat_style(Color("0b1a22"), COLOR_TEAL, 1, 2, 12))
	parent.add_child(panel)
	var label := _label(heading, 15, COLOR_IVORY)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	panel.add_child(label)
	return label


func _rebuild_candidate_list() -> void:
	for child in _candidate_list.get_children():
		_candidate_list.remove_child(child)
		child.queue_free()
	_article_buttons.clear()
	for article in _payload.get("articles", []):
		if str(article.get("placed_slot", "")) != "":
			continue
		var button := EditorialDragButton.new()
		button.custom_minimum_size = Vector2(288, 92)
		var article_id := int(article.get("id", -1))
		var status := "已选" if bool(article.get("selected", false)) else "候选"
		button.text = "%s  ·  %s\n%s\n%s" % [
			str(article.get("code", "A%02d" % article_id)),
			status,
			_short_title(str(article.get("title", "无标题")), 18),
			"%s · %s" % [str(article.get("quality", "")), _join_text(article.get("tags", []), " / ")],
		]
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.add_theme_font_size_override("font_size", 13)
		button.disabled = false
		_style_candidate_button(button, bool(article.get("selected", false)), button.disabled)
		button.tooltip_text = "再次点击取消选择；也可直接拖入版位" if bool(article.get("selected", false)) else "点击选择，或直接拖入版位"
		button.configure_drag_source("candidate", article_id, "", "%s · %s" % [str(article.get("code", "")), _short_title(str(article.get("title", "无标题")), 20)])
		button.configure_drop_target("candidate_pool")
		button.pressed.connect(func() -> void: _on_candidate_pressed(article_id))
		button.drag_started.connect(_on_drag_started)
		button.drag_finished.connect(_on_drag_finished)
		button.drag_hovered.connect(_on_drag_hovered)
		button.drag_exited.connect(_on_drag_exited)
		button.article_dropped.connect(_on_article_dropped)
		_candidate_list.add_child(button)
		_article_buttons.append(button)
	_refresh_interaction_lock()


func _refresh_pages() -> void:
	var slot_lookup := {}
	for slot in _payload.get("slots", []):
		slot_lookup[str(slot.get("id", ""))] = slot
	var held_id := int(_payload.get("held_article_id", -1))
	for slot_id in _slot_nodes.keys():
		var nodes: Dictionary = _slot_nodes[slot_id]
		var slot: Dictionary = slot_lookup.get(slot_id, {})
		var article_id := int(slot.get("article_id", -1))
		var occupied := article_id != -1
		var role := str(nodes.role)
		var title: Label = nodes.title
		var meta: Label = nodes.meta
		var story_texture: TextureRect = nodes.story_texture
		var display_title := ""
		if occupied:
			var full_title := str(slot.get("article_title", "无标题"))
			display_title = full_title
			title.tooltip_text = full_title
			var story_meta := "%s · %s" % [str(slot.get("quality", "")), _join_text(slot.get("tags", []), " / ")]
			meta.text = story_meta
			meta.tooltip_text = story_meta
		else:
			display_title = "%s · 空版位" % str(slot.get("name", slot_id))
			title.tooltip_text = display_title
			meta.text = "等待报道"
			meta.tooltip_text = meta.text
		_fit_headline(title, display_title, role)
		var story_article_id := int(nodes.get("story_article_id", -1))
		var story_asset_matches := false
		if story_texture != null and role in ["compact", "tall"]:
			var story_asset := EditorialAssets.get_story_asset_by_article_id(article_id, role) if occupied else {}
			if not story_asset.is_empty():
				story_texture.texture = EditorialAssets.load_texture(str(story_asset.get("id", "")))
			else:
				story_texture.texture = null
			story_asset_matches = occupied and story_texture.texture != null
		else:
			story_asset_matches = occupied and story_texture != null and story_texture.texture != null and (story_article_id == -1 or article_id == story_article_id)
		if story_texture != null:
			story_texture.visible = story_asset_matches
			story_texture.modulate = Color.WHITE
		var story_fallback: ColorRect = nodes.story_fallback
		if story_fallback != null:
			story_fallback.visible = occupied and not story_asset_matches
		var story_frame: PanelContainer = nodes.story_frame
		if story_frame != null:
			story_frame.visible = occupied
		var target = nodes.target
		if occupied:
			target.configure_drag_source("slot", article_id, slot_id, _short_title(str(slot.get("article_title", "报道")), 22))
		else:
			target.clear_drag_source()
		target.configure_drop_target("slot", slot_id)
		var is_drag_source: bool = _drag_active and str(_drag_source.get("source_kind", "")) == "slot" and str(_drag_source.get("source_slot_id", "")) == slot_id
		var is_drag_hover: bool = _drag_active and _drag_hover_kind == "slot" and _drag_hover_slot_id == slot_id
		var is_focused: bool = not _drag_active and _focused_slot_id == slot_id
		if is_drag_hover:
			_style_transparent_target(target, COLOR_PAPER_LIGHT, 3)
		elif is_drag_source:
			_style_transparent_target(target, Color(COLOR_COBALT.r, COLOR_COBALT.g, COLOR_COBALT.b, 0.60), 2)
		elif _drag_active:
			_style_transparent_target(target, Color(COLOR_OLIVE.r, COLOR_OLIVE.g, COLOR_OLIVE.b, 0.55), 2)
		elif is_focused:
			_style_transparent_target(target, COLOR_PAPER_LIGHT, 3)
		else:
			_style_transparent_target(target, COLOR_OLIVE_MID, 1)
		target.tooltip_text = "点击查看换稿；拖拽移动报道" if occupied else "将候选报道拖入此版位"
		var status_inner: PanelContainer = nodes.status_inner
		status_inner.visible = is_focused or is_drag_hover
		if status_inner.visible:
			status_inner.add_theme_stylebox_override("panel", _flat_style(Color(0, 0, 0, 0), COLOR_OLIVE, 1, 0, 0))
		var background: PanelContainer = nodes.background
		background.add_theme_stylebox_override("panel", _slot_style(role, _drag_active, is_drag_hover))
	_update_context_replace_button(slot_lookup, held_id)
	_refresh_candidate_drop_style()
	_refresh_interaction_lock()


func _refresh_review() -> void:
	var stats: Dictionary = _payload.get("stats", {})
	var main_slot := _slot_payload("front-main")
	var main_title := str(main_slot.get("article_title", "尚未设置主头版"))
	_review_headline.text = "主头版\n%s" % _short_title(main_title, 30)
	_review_outcome.text = "预计结果\n完整度 %d / 6   ·   销量 %d\n净收益 %+.0f" % [
		int(stats.get("filled_slots", 0)),
		int(stats.get("sold", 0)),
		float(stats.get("profit", 0.0)),
	]
	var empty_slots := int(stats.get("empty_slots", 6))
	var risk_text := "无硬阻断"
	if int(main_slot.get("article_id", -1)) == -1:
		risk_text = "主头版空缺\n依现行规则仍可尝试送印，但后果显著"
	elif empty_slots > 0:
		risk_text = "空版位 %d\n发行需求与收益将受到惩罚" % empty_slots
	_review_risk.text = "风险 / 阻断\n%s" % risk_text

	_confirmation_plate.visible = _confirmation_open
	_primary_action.visible = not _confirmation_open
	if _confirmation_open:
		_confirmation_label.text = "整期确认\n\n主头版：%s\n副头版：%s\n完整度：%d / 6\n预计销量：%d\n预计净收益：%+.0f\n\n%s" % [
			_short_title(main_title, 18),
			_short_title(str(_slot_payload("front-side").get("article_title", "未设置")), 18),
			int(stats.get("filled_slots", 0)),
			int(stats.get("sold", 0)),
			float(stats.get("profit", 0.0)),
			risk_text,
		]
	_primary_action.text = "签批送印"
	_clear_action.visible = not _confirmation_open
	_refresh_interaction_lock()


func _refresh_status() -> void:
	_status_title.text = "第 %02d 期 · 发刊排版" % int(_payload.get("issue", 1))


func _on_slot_pressed(slot_id: String) -> void:
	if _confirmation_open or _publishing or _drag_active:
		return
	var held_id := int(_payload.get("held_article_id", -1))
	var slot := _slot_payload(slot_id)
	var article_id := int(slot.get("article_id", -1))
	if _replace_target_slot_id != "" and held_id == -1:
		if slot_id == _replace_target_slot_id:
			return
		if article_id != -1:
			var target_slot_id := _replace_target_slot_id
			_cancel_transients(false)
			transfer_requested.emit("slot", article_id, slot_id, "slot", target_slot_id)
		else:
			_cancel_transients()
		return
	if held_id != -1:
		if article_id == -1:
			_cancel_transients(false)
			transfer_requested.emit("candidate", held_id, "", "slot", slot_id)
		else:
			_focused_slot_id = slot_id
			_replace_target_slot_id = ""
			_refresh_pages()
		return
	if article_id != -1:
		_focused_slot_id = slot_id
		_replace_target_slot_id = ""
		_refresh_pages()
	else:
		_cancel_transients()


func _on_candidate_pressed(article_id: int) -> void:
	if _confirmation_open or _publishing or _drag_active:
		return
	if _replace_target_slot_id != "" and int(_payload.get("held_article_id", -1)) == -1:
		var target_slot_id := _replace_target_slot_id
		_cancel_transients(false)
		transfer_requested.emit("candidate", article_id, "", "slot", target_slot_id)
		return
	_focused_slot_id = ""
	_replace_target_slot_id = ""
	article_selected.emit(article_id)


func _on_context_replace_pressed() -> void:
	if _confirmation_open or _publishing or _drag_active or _focused_slot_id == "":
		return
	var held_id := int(_payload.get("held_article_id", -1))
	if held_id != -1:
		var target_slot_id := _focused_slot_id
		_cancel_transients(false)
		transfer_requested.emit("candidate", held_id, "", "slot", target_slot_id)
		return
	_replace_target_slot_id = _focused_slot_id
	_refresh_pages()


func _on_drag_started(source: Dictionary) -> void:
	if _confirmation_open or _publishing:
		return
	_drag_active = true
	_drag_source = source.duplicate(true)
	_drag_hover_kind = ""
	_drag_hover_slot_id = ""
	_focused_slot_id = ""
	_replace_target_slot_id = ""
	if str(source.get("source_kind", "")) == "slot" and int(_payload.get("held_article_id", -1)) != -1:
		held_article_cancelled.emit()
	_refresh_pages()


func _on_drag_hovered(target_kind: String, target_slot_id: String) -> void:
	if not _drag_active or _confirmation_open or _publishing:
		return
	if _drag_hover_kind == target_kind and _drag_hover_slot_id == target_slot_id:
		return
	_drag_hover_kind = target_kind
	_drag_hover_slot_id = target_slot_id
	_refresh_pages()


func _on_drag_exited(target_kind: String, target_slot_id: String) -> void:
	if not _drag_active or _drag_hover_kind != target_kind or _drag_hover_slot_id != target_slot_id:
		return
	_drag_hover_kind = ""
	_drag_hover_slot_id = ""
	_refresh_pages()


func _on_article_dropped(source: Dictionary, target_kind: String, target_slot_id: String) -> void:
	if _confirmation_open or _publishing:
		_cancel_transients()
		return
	var source_kind := str(source.get("source_kind", ""))
	var article_id := int(source.get("article_id", -1))
	var source_slot_id := str(source.get("source_slot_id", ""))
	_cancel_transients(false)
	transfer_requested.emit(source_kind, article_id, source_slot_id, target_kind, target_slot_id)


func _on_drag_finished(_source: Dictionary, successful: bool) -> void:
	var had_held_article := int(_payload.get("held_article_id", -1)) != -1
	_cancel_transients()
	if not successful and had_held_article:
		held_article_cancelled.emit()


func _cancel_transients(refresh_visuals: bool = true) -> void:
	_focused_slot_id = ""
	_replace_target_slot_id = ""
	_drag_active = false
	_drag_source.clear()
	_drag_hover_kind = ""
	_drag_hover_slot_id = ""
	if refresh_visuals and not _slot_nodes.is_empty():
		_refresh_pages()


func _has_local_transient() -> bool:
	return _focused_slot_id != "" or _replace_target_slot_id != "" or _drag_active


func _update_context_replace_button(slot_lookup: Dictionary, held_id: int) -> void:
	if _context_replace_button == null:
		return
	var show_button := not _confirmation_open and not _publishing and not _drag_active and _focused_slot_id != "" and _replace_target_slot_id == ""
	var slot: Dictionary = slot_lookup.get(_focused_slot_id, {})
	show_button = show_button and int(slot.get("article_id", -1)) != -1
	_context_replace_button.visible = show_button
	if not show_button:
		return
	var nodes: Dictionary = _slot_nodes[_focused_slot_id]
	var root: Control = nodes.root
	var slot_size: Vector2 = nodes.size
	var root_local := _edition_canvas.get_global_transform().affine_inverse() * root.global_position
	_context_replace_button.position = root_local + Vector2(slot_size.x - 52, slot_size.y - 52)
	_context_replace_button.text = "换稿"
	_context_replace_button.tooltip_text = "确认用当前候选替换此版位" if held_id != -1 else "为当前版位选择另一篇报道"


func _refresh_candidate_drop_style() -> void:
	if _candidate_panel == null:
		return
	var is_hover := _drag_active and _drag_hover_kind == "candidate_pool"
	var border := COLOR_PAPER_LIGHT if is_hover else COLOR_TEAL
	var width := 3 if is_hover else 1
	_candidate_panel.add_theme_stylebox_override("panel", _flat_style(COLOR_PANEL, border, width, 2, 0))


func _on_primary_action() -> void:
	if _publishing:
		return
	show_confirmation()


func _close_confirmation() -> void:
	if _publishing:
		return
	_confirmation_open = false
	_refresh_review()


func _confirm_publish() -> void:
	if _publishing:
		return
	_publishing = true
	_confirmation_back.disabled = true
	_confirmation_confirm.disabled = true
	_confirmation_confirm.text = "已盖章 · 正在送印"
	_confirmation_label.text += "\n\n送印单已冻结，印刷机正在启动……"
	var tween := create_tween().set_loops(3)
	tween.tween_property(_confirmation_plate, "modulate", Color(1.0, 0.88, 0.70, 1.0), 0.22)
	tween.tween_property(_confirmation_plate, "modulate", Color.WHITE, 0.22)
	await get_tree().create_timer(1.5).timeout
	settle_requested.emit()


func _apply_dual_page_geometry() -> void:
	_candidate_panel.visible = true
	_edition_panel.custom_minimum_size.x = OVERVIEW_EDITION_WIDTH
	_edition_canvas.custom_minimum_size.x = OVERVIEW_EDITION_WIDTH
	_masthead.position = Vector2(15, 16)
	_masthead.size = Vector2(1010, 56)
	(_page_nodes.left as Control).position = Vector2(15, 88)
	(_page_nodes.left as Control).scale = Vector2.ONE
	(_page_nodes.right as Control).position = Vector2(535, 88)
	(_page_nodes.right as Control).scale = Vector2.ONE


func _refresh_interaction_lock() -> void:
	var locked := _confirmation_open or _publishing
	for button in _article_buttons:
		button.disabled = locked
		button.mouse_filter = Control.MOUSE_FILTER_IGNORE if locked else Control.MOUSE_FILTER_STOP
	for nodes in _slot_nodes.values():
		(nodes.target as Button).disabled = locked
		nodes.target.drop_enabled = not locked
	_candidate_panel.drop_enabled = not locked and _drag_active
	_context_replace_button.disabled = locked
	if locked:
		_context_replace_button.visible = false
	_clear_action.disabled = locked
	_primary_action.disabled = _publishing


func _slot_payload(slot_id: String) -> Dictionary:
	for slot in _payload.get("slots", []):
		if str(slot.get("id", "")) == slot_id:
			return slot
	return {}


func _fit_headline(label: Label, full_title: String, role: String) -> void:
	var fit_role := role if role in ["main", "secondary"] else "standard"
	var font := label.get_theme_font("font")
	var fit_key := "%s|%s|%.2f|%.2f|%d" % [fit_role, full_title, label.size.x, label.size.y, font.get_instance_id()]
	label.text = full_title
	if label.has_meta("headline_fit_key") and str(label.get_meta("headline_fit_key")) == fit_key:
		return

	var config: Dictionary = HEADLINE_SIZE_STEPS[fit_role]
	var chosen_size := int((config.double as Array)[-1])
	var chosen_mode := "fallback"
	var single_width_limit := minf(label.size.x * HEADLINE_SINGLE_WIDTH_RATIO, label.size.x - HEADLINE_HORIZONTAL_RESERVE)
	for candidate_value in config.single:
		var candidate_size := int(candidate_value)
		var text_size := font.get_string_size(full_title, HORIZONTAL_ALIGNMENT_LEFT, -1, candidate_size)
		if text_size.x <= single_width_limit and font.get_height(candidate_size) <= label.size.y - HEADLINE_VERTICAL_RESERVE:
			chosen_size = candidate_size
			chosen_mode = "single"
			break

	if chosen_mode != "single":
		label.max_lines_visible = -1
		label.text_overrun_behavior = TextServer.OVERRUN_NO_TRIMMING
		label.clip_text = false
		for candidate_value in config.double:
			var candidate_size := int(candidate_value)
			label.add_theme_font_size_override("font_size", candidate_size)
			var line_count := label.get_line_count()
			var text_height := float(label.get_line_height()) * float(line_count)
			if line_count <= 2 and text_height <= label.size.y:
				chosen_size = candidate_size
				chosen_mode = "double"
				break

	label.add_theme_font_size_override("font_size", chosen_size)
	label.max_lines_visible = 2
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.clip_text = true
	label.set_meta("headline_fit_key", fit_key)
	label.set_meta("headline_fit_mode", chosen_mode)
	label.set_meta("headline_fit_size", chosen_size)


func _short_title(value: String, limit: int) -> String:
	if value.length() <= limit:
		return value
	return value.left(maxi(1, limit - 1)) + "…"


func _join_text(values: Array, separator: String) -> String:
	var parts: Array[String] = []
	for value in values:
		parts.append(str(value))
	return separator.join(parts)


func _label(text_value: String, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	return label


func _flat_style(bg: Color, border: Color, border_width: int, radius: int, content_margin: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(border_width)
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	style.content_margin_left = content_margin
	style.content_margin_top = content_margin
	style.content_margin_right = content_margin
	style.content_margin_bottom = content_margin
	return style


func _style_button(button: Button, primary: bool, flat_header: bool = false) -> void:
	var bg := COLOR_OLIVE_MID if primary else Color("1d3440")
	var border := COLOR_PAPER_LIGHT if primary else COLOR_TEAL
	if flat_header:
		bg = Color(0.08, 0.10, 0.08, 0.18)
		border = Color(0.15, 0.20, 0.16, 0.32)
	var normal := _flat_style(bg, border, 1, 2, 10)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = bg.lightened(0.09)
	hover.border_color = COLOR_PAPER_LIGHT
	button.add_theme_stylebox_override("hover", hover)
	var pressed := normal.duplicate()
	pressed.bg_color = bg.darkened(0.08)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var color := COLOR_INK if primary else COLOR_IVORY
	button.add_theme_color_override("font_color", color)
	button.add_theme_color_override("font_hover_color", color)
	button.add_theme_color_override("font_pressed_color", color)
	button.add_theme_color_override("font_disabled_color", Color(color.r, color.g, color.b, 0.46))


func _style_candidate_button(button: Button, selected: bool, disabled: bool) -> void:
	var bg := Color("5f6338") if selected else Color("142a34")
	var border := COLOR_PAPER_LIGHT if selected else COLOR_TEAL
	if disabled:
		bg = Color("172127")
		border = Color("35434a")
	var normal := _flat_style(bg, border, 2 if selected else 1, 2, 12)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = bg.lightened(0.08)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	button.add_theme_color_override("font_color", COLOR_IVORY)
	button.add_theme_color_override("font_hover_color", COLOR_PAPER_LIGHT)
	button.add_theme_color_override("font_disabled_color", COLOR_MUTED)


func _style_transparent_target(button: Button, border: Color, width: int) -> void:
	var normal_width := maxi(1, width - 1)
	var normal_alpha := 0.82 if width >= 4 else 0.28
	var normal := _flat_style(Color(0, 0, 0, 0), Color(border.r, border.g, border.b, normal_alpha), normal_width, 2, 0)
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.border_color = border
	hover.set_border_width_all(width)
	button.add_theme_stylebox_override("hover", hover)
	var pressed := hover.duplicate()
	pressed.border_color = border.lightened(0.14)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("focus", hover.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())


func _slot_style(role: String, has_held: bool, replace_target: bool) -> StyleBoxFlat:
	if role == "main":
		return _flat_style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0)
	var bg := Color(0, 0, 0, 0) if role == "secondary" else Color("b49c73")
	var border := COLOR_OLIVE if has_held else COLOR_TEAL
	if replace_target:
		border = COLOR_PAPER_LIGHT
	return _flat_style(bg, border, 2 if has_held else 1, 2, 8)
