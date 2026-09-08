extends Control
## A359：正式世界地图表现层，沿用游戏 payload 和两个既有动作信号。

signal region_selected(region_id: String)
signal enter_region_requested

const Catalog = preload("res://scenes/gameplay/weekly_run/components/WorldMapNewsCatalog.gd")
const PaperEdge = preload("res://scenes/gameplay/weekly_run/components/WorldMapPaperEdge.gdshader")
const DossierContour = preload("res://scenes/gameplay/weekly_run/components/WorldMapDossierContour.gd")
const SIZE := Vector2(1920, 1080)
const INK := Color("102125")
const MUTED := Color("485754")
const PAPER := Color("ebdec5")
const HONEY := Color("d6a53e")
const TEAL := Color("558d8d")
const RUST := Color("9e3d2d")
const PHOTO_RATIO := 1672.0 / 941.0
const PRIMARY_RECT := Rect2(1278, 914, 550, 76)
const SELECTED_PAPER_OFFSET := Vector2(7, -3)

var _canvas: Control
var _scroll: ScrollContainer
var _list: VBoxContainer
var _cards: Dictionary = {}
var _pins: Dictionary = {}
var _models: Dictionary = {}
var _payload: Dictionary = {}
var _selected := ""
var _expanded := true
var _available := false
var _font: SystemFont
var _bold: SystemFont
var _hand: SystemFont
var _region_title: Label
var _risk: Label
var _headline: Label
var _deck: Label
var _photo: TextureRect
var _photo_empty: Label
var _evidence: Control
var _evidence_photo: TextureRect
var _evidence_empty: Label
var _note: Label
var _kicker: Label
var _issue: Label
var _day: Label
var _remaining_days: Label
var _schedule_hint: Label
var _list_hint: Label
var _summary: Button
var _summary_title: Label
var _summary_hint: Label
var _task_counts: Label
var _task_warning: Label
var _task_paper: NinePatchRect
var _task_header: NinePatchRect
var _task_rows: Array[Control] = []
var _task_backing: NinePatchRect
var _paper_material: ShaderMaterial
var _front_material: ShaderMaterial
var _photo_edge_material: ShaderMaterial
var _primary: Button
var _primary_label: Label
var _primary_paper: NinePatchRect
var _access: Label
var _empty_tasks: Label
var _task_labels: Array[Label] = []
var _task_meta: Array[Label] = []
var _connector: Line2D

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_PASS
	_font = SystemFont.new()
	_font.font_names = PackedStringArray(["Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans CJK SC"])
	_bold = SystemFont.new()
	_bold.font_names = _font.font_names
	_bold.font_weight = 700
	_hand = SystemFont.new()
	_hand.font_names = PackedStringArray(["KaiTi", "STKaiti", "Microsoft YaHei"])
	_paper_material = ShaderMaterial.new()
	_paper_material.shader = PaperEdge
	_front_material = ShaderMaterial.new()
	_front_material.shader = PaperEdge
	_front_material.set_shader_parameter("front_only", true)
	_photo_edge_material = ShaderMaterial.new()
	_photo_edge_material.shader = PaperEdge
	_photo_edge_material.set_shader_parameter("smooth_edges", false)
	_photo_edge_material.set_shader_parameter("smooth_quad", true)
	_build()
	_fit()

func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED and is_instance_valid(_canvas):
		_fit()

func _fit() -> void:
	var factor := minf(size.x / SIZE.x, size.y / SIZE.y)
	_canvas.scale = Vector2.ONE * factor
	_canvas.position = (size - SIZE * factor) * 0.5

func has_independent_host() -> bool:
	return true

static func has_runtime_assets() -> bool:
	return ResourceLoader.exists(Catalog.ASSET_DIR + "background.png")

func _build() -> void:
	_canvas = Control.new()
	_canvas.name = "SoftColumns1920"
	_canvas.size = SIZE
	_canvas.clip_contents = true
	_canvas.mouse_filter = Control.MOUSE_FILTER_PASS
	add_child(_canvas)
	_image(_canvas, "Background", Rect2(Vector2.ZERO, SIZE), Catalog.texture(Catalog.ASSET_DIR + "background.png"), false)
	_label(_canvas, "Masthead", Rect2(142, 23, 450, 62), "世界未解之谜周刊", 36, PAPER, true)
	_image(_canvas, "Brand", Rect2(24, 20, 108, 97), Catalog.texture(Catalog.ASSET_DIR + "wmw-brand.png"))
	_label(_canvas, "EnglishTitle", Rect2(145, 82, 460, 24), "W O R L D  M Y S T E R Y  W E E K L Y", 13, PAPER)
	_issue = _label(_canvas, "Issue", Rect2(145, 111, 380, 22), "", 14, Color("b9c7bc"))
	_list_hint = _label(_canvas, "RegionScrollHint", Rect2(40, 900, 508, 27), "", 15, PAPER)
	_scroll = ScrollContainer.new()
	_scroll.name = "RegionsScroll"
	_scroll.position = Vector2(20, 140)
	_scroll.size = Vector2(564, 758)
	_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	_scroll.follow_focus = true
	_canvas.add_child(_scroll)
	_style_scroll()
	_scroll.get_v_scroll_bar().value_changed.connect(func(_value: float) -> void: _update_list_hint())
	_scroll.get_v_scroll_bar().changed.connect(func() -> void: call_deferred("_update_list_hint"))
	_list = VBoxContainer.new()
	_list.name = "RegionCards"
	_list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_list.add_theme_constant_override("separation", 7)
	_scroll.add_child(_list)
	_paper(_canvas, "SchedulePaper", Rect2(26, 932, 548, 125), "schedule-paper", Vector4(36, 22, 32, 22))
	_label(_canvas, "ScheduleTitle", Rect2(67, 951, 370, 31), "全局日程", 21, INK, true)
	_day = _label(_canvas, "CurrentDay", Rect2(67, 980, 225, 28), "", 21)
	_remaining_days = _label(_canvas, "WeekDaysRemaining", Rect2(291, 980, 243, 28), "", 21, INK, true)
	_remaining_days.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_schedule_hint = _label(_canvas, "ScheduleReadOnly", Rect2(67, 1009, 447, 24), "", 17, MUTED)
	_connector = Line2D.new()
	_connector.name = "SelectedEvidenceLink"
	_connector.width = 3
	_connector.default_color = PAPER.darkened(0.1)
	_connector.antialiased = true
	_canvas.add_child(_connector)
	_evidence = Control.new()
	_evidence.name = "CurrentRegionEvidence"
	_evidence.position = Vector2(638, 554)
	_evidence.size = Vector2(278, 200)
	_evidence.rotation = deg_to_rad(-6)
	_evidence.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_canvas.add_child(_evidence)
	_paper(_evidence, "EvidencePaper", Rect2(0, 0, 278, 214), "region-tag", Vector4(22, 18, 22, 18))
	_evidence_photo = _image(_evidence, "SharedPhoto", Rect2(28, 24, 226, 226 / PHOTO_RATIO), null)
	_evidence_photo.material = _photo_edge_material
	_evidence_empty = _label(_evidence, "MissingPhoto", Rect2(22, 38, 232, 84), "配图待补", 22, MUTED)
	_label(_evidence, "EvidenceCaption", Rect2(31, 159, 218, 25), "来稿附图  /  WMW", 14, MUTED)
	_paper(_canvas, "EditorNote", Rect2(818, 741, 181, 190), "note-paper", Vector4(25, 48, 25, 24))
	_note = _label(_canvas, "EditorNoteText", Rect2(850, 798, 140, 112), "", 27)
	_note.add_theme_font_override("font", _hand)
	_note.rotation = deg_to_rad(6)
	_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	var dossier := _paper(_canvas, "DossierPaper", Rect2(1213, 9, 694, 1051), "dossier-paper", Vector4(44, 134, 168, 36))
	var contour_rows := DossierContour.rows(dossier.texture)
	if contour_rows != null:
		var contour_material := _paper_material.duplicate() as ShaderMaterial
		contour_material.set_shader_parameter("contour_rows", contour_rows)
		contour_material.set_shader_parameter("contour_enabled", true)
		dossier.material = contour_material
	_kicker = _label(_canvas, "NewsKicker", Rect2(1284, 94, 278, 30), "", 18, MUTED)
	_kicker.mouse_filter = Control.MOUSE_FILTER_PASS
	_risk = _label(_canvas, "RegionRisk", Rect2(1575, 96, 164, 28), "", 20, RUST, true)
	_risk.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_rule(Rect2(1280, 129, 547, 1), Color("a9a18a"))
	_region_title = _label(_canvas, "RegionTitle", Rect2(1280, 140, 550, 81), "", 44, INK, true)
	_region_title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_region_title.max_lines_visible = 2
	_region_title.mouse_filter = Control.MOUSE_FILTER_PASS
	_photo = _image(_canvas, "DossierSharedPhoto", Rect2(1338, 216, 430, 430 / PHOTO_RATIO), null)
	_photo_empty = _label(_canvas, "DossierMissingPhoto", Rect2(1340, 326, 436, 58), "这份来稿的配图尚待补齐", 24, MUTED)
	_headline = _label(_canvas, "NewsHeadline", Rect2(1280, 466, 550, 100), "", 36, INK, true)
	_headline.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_headline.max_lines_visible = 2
	_headline.mouse_filter = Control.MOUSE_FILTER_PASS
	_deck = _label(_canvas, "NewsDeck", Rect2(1280, 569, 550, 54), "", 18)
	_deck.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_deck.max_lines_visible = 2
	_deck.mouse_filter = Control.MOUSE_FILTER_PASS
	# A363 接续：单张任务附页；文字按实际行数排版，纸面随内容收放。
	_task_backing = _task_surface("MissionBacking", Color("799596"))
	_task_paper = _task_surface("MissionPaper", Color(0.84, 0.98, 1.06))
	_task_header = _task_surface("MissionHeaderPaper", Color("386366"))
	_summary = _button(_canvas, "MissionDisclosure", Rect2(1296, 620, 514, 34), func() -> void: set_mission_intel_expanded(not _expanded))
	for state in ["hover", "pressed", "focus"]:
		var feedback := StyleBoxFlat.new()
		feedback.bg_color = Color(0.2, 0.45, 0.45, 0.05 if state == "hover" else 0.10)
		feedback.border_color = TEAL
		feedback.border_width_bottom = 1 if state == "focus" else 0
		_summary.add_theme_stylebox_override(state, feedback)
	_summary_title = _label(_canvas, "MissionSummaryTitle", Rect2(1296, 620, 235, 32), "", 22, Color("f5edda"), true)
	_summary_hint = _label(_canvas, "MissionSummaryHint", Rect2(1550, 620, 260, 32), "", 17, MUTED)
	_summary_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_task_counts = _label(_canvas, "MissionCounts", Rect2(1296, 660, 514, 25), "", 18, MUTED)
	_task_warning = _label(_canvas, "MissionWarning", Rect2(1296, 692, 514, 49), "", 17, MUTED)
	_task_warning.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_task_warning.max_lines_visible = 2
	_task_warning.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_task_warning.mouse_filter = Control.MOUSE_FILTER_PASS
	for i in range(2):
		var row := Control.new()
		row.name = "TaskPreview%d" % i
		row.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_canvas.add_child(row)
		_task_rows.append(row)
		_task_labels.append(_label(row, "TaskName%d" % i, Rect2(0, 0, 514, 60), "", 21, INK, true))
		_task_labels[i].autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		_task_labels[i].max_lines_visible = 2
		_task_labels[i].vertical_alignment = VERTICAL_ALIGNMENT_TOP
		_task_labels[i].mouse_filter = Control.MOUSE_FILTER_PASS
		_task_meta.append(_label(row, "TaskMeta%d" % i, Rect2(0, 32, 514, 24), "", 17, MUTED))
	_empty_tasks = _label(_canvas, "TaskEmptyOrLocked", Rect2(1296, 760, 514, 116), "", 20, MUTED)
	_empty_tasks.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_empty_tasks.max_lines_visible = 3
	_empty_tasks.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_primary_paper = _paper(_canvas, "ActionPaper", PRIMARY_RECT, "action-paper", Vector4(27, 22, 27, 18))
	_primary = _button(_canvas, "PrimaryEnterButton", PRIMARY_RECT, _activate_primary)
	_primary_label = _label(_canvas, "PrimaryText", Rect2(1290, 926, 526, 48), "", 32, INK, true)
	_primary_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_access = _label(_canvas, "AccessHint", Rect2(1296, 991, 514, 24), "", 16, MUTED)

func _task_surface(node_name: String, tint: Color) -> NinePatchRect:
	var front := AtlasTexture.new()
	front.atlas = Catalog.texture(Catalog.ASSET_DIR + "region-tag.png")
	front.region = Rect2(17, 12, 334, 143)
	var paper := _paper(_canvas, node_name, Rect2(1278, 625, 550, 240), "region-tag", Vector4(9, 8, 9, 8))
	paper.texture = front
	paper.material = _front_material
	paper.modulate = tint
	return paper

func _text_height(label: Label, width: float, limit: int = 2) -> float:
	label.size.x = width
	var lines := mini(limit, maxi(1, label.get_line_count()))
	var line_height := label.get_theme_font("font").get_height(label.get_theme_font_size("font_size"))
	var height := ceilf(line_height * lines + label.get_theme_constant("line_spacing") * (lines - 1)) + 2.0
	label.size.y = height
	label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	return height

func _layout_right_column() -> void:
	const TEXT_X := 1296.0
	const TEXT_W := 514.0
	var headline_height := _text_height(_headline, TEXT_W)
	var deck_height := _text_height(_deck, TEXT_W)
	var warning_height := _text_height(_task_warning, TEXT_W) if not _task_warning.text.is_empty() else 0.0
	var full_rows_height := 0.0
	var shown_rows_height := 0.0
	var rows: Array = _payload.get("region_mission_preview", []) if _available else []
	for i in range(2):
		var name_height := _text_height(_task_labels[i], TEXT_W)
		var row_height := name_height + 4.0 + _text_height(_task_meta[i], TEXT_W, 1)
		_task_meta[i].position = Vector2(0, name_height + 4)
		_task_rows[i].size = Vector2(TEXT_W, row_height)
		if i < rows.size():
			full_rows_height += row_height + (12.0 if i > 0 else 0.0)
			if _expanded:
				shown_rows_height = full_rows_height
	var empty_height := _text_height(_empty_tasks, TEXT_W, 3) if _empty_tasks.visible else 0.0
	var intro_height := 64.0 + warning_height + 12.0
	var expanded_height := intro_height + maxf(full_rows_height, empty_height if rows.is_empty() else 0.0) + 20.0
	var paper_height := intro_height + maxf(shown_rows_height, empty_height) + 20.0
	# 折叠不重新放大照片，避免整栏跳动；最长内容优先，不缩文字或丢提醒。
	var photo_height := minf(450.0 / PHOTO_RATIO, PRIMARY_RECT.position.y - 18.0 - 210.0 - 14.0 - headline_height - 10.0 - deck_height - 22.0 - expanded_height)
	photo_height = maxf(150.0, photo_height)
	_photo.position = Vector2(TEXT_X, 210)
	_photo.size = Vector2(photo_height * PHOTO_RATIO, photo_height)
	_photo_empty.position = Vector2(TEXT_X, 280)
	_headline.position = Vector2(TEXT_X, _photo.position.y + photo_height + 14)
	_deck.position = Vector2(TEXT_X, _headline.position.y + headline_height + 10)
	var paper_y := _deck.position.y + deck_height + 22
	_task_paper.position = Vector2(1270, paper_y)
	_task_paper.size = Vector2(558, paper_height)
	_task_backing.position = _task_paper.position + Vector2(4, 4)
	_task_backing.size = _task_paper.size
	_task_header.position = Vector2(1284, paper_y - 9)
	_task_header.size = Vector2(244 if _available else 318, 48)
	_summary.position = Vector2(1580, paper_y - 1)
	_summary.size = Vector2(230, 34)
	_summary_title.position = Vector2(TEXT_X + 6, paper_y + 2)
	_summary_title.size.x = 290 if not _available else 225
	_summary_hint.position = Vector2(1550, paper_y + 4)
	_task_counts.position = Vector2(TEXT_X, paper_y + 36)
	_task_warning.position = Vector2(TEXT_X, paper_y + 64)
	var row_y := paper_y + intro_height
	for i in range(2):
		_task_rows[i].position = Vector2(TEXT_X, row_y)
		if _task_rows[i].visible:
			row_y += _task_rows[i].size.y + 12
	_empty_tasks.position = Vector2(TEXT_X, paper_y + intro_height)

func render(payload: Dictionary) -> void:
	_payload = payload.duplicate(true)
	var next_selected := str(payload.get("selected_region_id", ""))
	var changed := next_selected != _selected
	var animate_selection := changed and not _selected.is_empty()
	_selected = next_selected
	if changed:
		_expanded = true
	var regions: Array = payload.get("regions", [])
	_models.clear()
	for region in regions:
		_models[str(region.get("id", ""))] = region
	_sync_cards(regions, animate_selection)
	_sync_pins(regions)
	_available = bool(payload.get("region_enter_enabled", false)) and _models.has(_selected)
	var model: Dictionary = _models.get(_selected, {})
	var news := Catalog.get_news(model)
	var tex := news.get("texture") as Texture2D
	_photo.texture = tex
	_evidence_photo.texture = tex
	_photo_empty.visible = tex == null
	_evidence_empty.visible = tex == null
	_evidence.visible = not model.is_empty()
	_note.text = str(news.get("note", "")) if not model.is_empty() else "等待\n新来稿。"
	_kicker.text = "当前查看 · %02d %s" % [_models.keys().find(_selected) + 1, str(news.get("map_label", model.get("name", "")))] if not model.is_empty() else "等待地区来稿"
	_kicker.tooltip_text = _kicker.text
	_region_title.text = str(model.get("name", "请选择地区"))
	_region_title.tooltip_text = _region_title.text
	_risk.text = (str(payload.get("region_status_primary", "")) if _available else "地区锁定") if not model.is_empty() else ""
	_risk.add_theme_color_override("font_color", _region_risk_color())
	_headline.text = str(news.get("headline", "")) if not model.is_empty() else "等一份来自远方的消息"
	_headline.tooltip_text = _headline.text
	_deck.text = str(news.get("deck", "")) if not model.is_empty() else "选择左侧来稿或地图上的地区，查看新闻与调查机会。"
	_deck.tooltip_text = _deck.text
	_issue.text = "ISSUE %03d  /  WEEK %02d" % [int(payload.get("issue", 1)), int(payload.get("week", 1))]
	var day := maxi(1, int(payload.get("week_days", 7)) - int(payload.get("remaining_days", 7)) + 1)
	_day.text = "当前第 %d 天" % day
	_remaining_days.text = "本周剩余 %d 天" % maxi(0, int(payload.get("remaining_days", 0)))
	_remaining_days.add_theme_color_override("font_color", RUST if int(payload.get("remaining_days", 0)) <= 2 else INK)
	_schedule_hint.text = "选题会尚未开始                 日程只读" if int(payload.get("remaining_days", 0)) > 0 else "本周取材已结束                 日程只读"
	_primary.disabled = not _available
	_primary_label.text = "进入地区任务台 →" if _available else "暂不可进入"
	_primary_paper.modulate = Color.WHITE if _available else Color("a9b3aa")
	_access.text = "可进入调查 · 进入本身不消耗天数" if _available else "来稿可浏览 · 地区尚未解锁"
	if model.is_empty():
		_access.text = "选择地区后可查看进入条件"
	_render_tasks()
	_update_list_hint()
	_update_connector()
	if changed and _cards.has(_selected):
		call_deferred("_reveal_selected")

func _sync_cards(regions: Array, animate_selection: bool = false) -> void:
	# 超出原有三卡容量才叠放透明纸边：保留照片规格，露出第四张的标题。
	var overflowing := regions.size() > 3
	_list.add_theme_constant_override("separation", -26 if overflowing else 7)
	for id in _cards.keys():
		if not _models.has(id):
			var old: Control = _cards[id].root
			_list.remove_child(old)
			old.queue_free()
			_cards.erase(id)
	for i in range(regions.size()):
		var model: Dictionary = regions[i]
		var id := str(model.get("id", ""))
		if not _cards.has(id):
			_cards[id] = _make_card(id)
		var card: Dictionary = _cards[id]
		_list.move_child(card.root, i)
		var news := Catalog.get_news(model)
		card.photo.texture = news.texture
		card.empty.visible = news.texture == null
		card.title.text = "%02d  %s" % [i + 1, str(model.get("name", id))]
		card.title.tooltip_text = card.title.text
		card.headline.text = str(news.headline)
		var unlocked := bool(model.get("unlocked", model.get("enabled", false)))
		var selected := id == _selected
		card.state.text = ("已选中 · 可进入" if unlocked else "已选中\n锁定 · 可预览") if selected else ("可进入" if unlocked else "锁定 · 可预览")
		var tone := str(model.get("tone", ""))
		card.risk.text = "红线升温" if tone == "deadline" else "青线追踪" if tone == "chain" else ""
		card.risk.add_theme_color_override("font_color", RUST if tone == "deadline" else Color("2a6669"))
		_set_card_selection(card, selected, animate_selection)
		card.hit.set_meta("region_id", id)
		card.hit.set_meta("selected", selected)
		card.hit.tooltip_text = "%s\n%s\n%s" % [str(model.get("name", id)), str(news.headline), card.state.text]
		card.source_path = str(news.source_path)
	call_deferred("_refresh_scroll_layout")

func _refresh_scroll_layout() -> void:
	# 新增/移除卡片及改变间距会在同帧排版；下一帧再让外层取最终高度。
	await get_tree().process_frame
	_scroll.queue_sort()
	call_deferred("_update_list_hint")

func _make_card(id: String) -> Dictionary:
	var item := Control.new()
	item.name = "RegionCard_" + id
	item.custom_minimum_size = Vector2(528, 248)
	item.mouse_filter = Control.MOUSE_FILTER_PASS
	_list.add_child(item)
	# A360：重复使用现有真实纸张素材，选中表现独立于图片、锁定和鼠标焦点。
	var shadow := _paper(item, "SelectedPaperShadow", Rect2(17, 65, 511, 191), "action-paper", Vector4(25, 20, 25, 18))
	shadow.modulate = Color(0.03, 0.05, 0.05, 0.55)
	var backing := _paper(item, "SelectedHoneyBacking", Rect2(7, 48, 516, 204), "action-paper", Vector4(25, 20, 25, 18))
	var face := Control.new()
	face.name = "PaperFace"
	face.size = Vector2(530, 248)
	face.mouse_filter = Control.MOUSE_FILTER_IGNORE
	item.add_child(face)
	_paper(face, "Paper", Rect2(0, 0, 530, 248), "region-paper", Vector4(50, 93, 45, 30))
	# 回形针独占左侧暖白纸边；纸签与编号均避开夹具，并保留完整的左内距。
	var title_paper := _paper(face, "SelectedTitlePaper", Rect2(84, 35, 415, 57), "action-paper", Vector4(17, 14, 17, 14))
	var title := _label(face, "RegionName", Rect2(104, 49, 391, 32), "", 23, INK, true)
	var photo := _image(face, "SharedPhoto", Rect2(42, 86, 246, 246 / PHOTO_RATIO), null)
	var missing := _label(face, "MissingPhoto", Rect2(76, 124, 190, 41), "配图待补", 20, MUTED)
	var headline := _label(face, "NewsHook", Rect2(307, 87, 187, 77), "", 21)
	headline.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	headline.max_lines_visible = 3
	var state_label := _label(face, "RegionAccess", Rect2(307, 164, 190, 52), "", 17, MUTED)
	state_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	state_label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	var risk := _label(face, "RegionWarning", Rect2(307, 197, 185, 23), "", 17, RUST)
	# 热区保持稳定，短暂纸张位移不改变列表布局或输入目标。
	var hit := _button(item, "SelectRegion", Rect2(25, 31, 487, 211), func() -> void: region_selected.emit(id))
	_style_selection_hit(hit)
	return {"root": item, "hit": hit, "face": face, "shadow": shadow, "backing": backing, "title_paper": title_paper, "selected": false, "settle_tween": null, "title": title, "photo": photo, "empty": missing, "headline": headline, "state": state_label, "risk": risk, "source_path": ""}

func _set_card_selection(card: Dictionary, selected: bool, animate: bool) -> void:
	card.backing.visible = selected
	card.shadow.visible = selected
	card.title_paper.visible = selected
	if selected == bool(card.selected):
		return
	card.selected = selected
	var old_tween = card.settle_tween
	if old_tween is Tween and old_tween.is_valid():
		old_tween.kill()
	card.settle_tween = null
	var destination := SELECTED_PAPER_OFFSET if selected else Vector2.ZERO
	card.face.position = destination
	if selected and animate:
		card.face.position = destination + Vector2(0, -5)
		var settle := create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		settle.tween_property(card.face, "position", destination, 0.16)
		card.settle_tween = settle

func _style_selection_hit(hit: Button) -> void:
	for state in ["hover", "pressed", "focus"]:
		var style := StyleBoxFlat.new()
		style.bg_color = Color(1, 1, 1, 0.045 if state == "hover" else 0.07)
		if state == "focus":
			style.bg_color = Color.TRANSPARENT
			style.border_color = TEAL
			style.set_border_width_all(2)
		hit.add_theme_stylebox_override(state, style)

func _sync_pins(regions: Array) -> void:
	for id in _pins.keys():
		if not _models.has(id):
			_pins[id].root.queue_free()
			_pins.erase(id)
	var occupied: Array[Rect2] = []
	var unplaced := 0
	for i in range(regions.size()):
		var model: Dictionary = regions[i]
		var id := str(model.get("id", ""))
		var news := Catalog.get_news(model)
		var fallback := Vector2(588 + (unplaced % 3) * 204, 190 + floori(unplaced / 3.0) * 76)
		var point: Vector2 = news.get("anchor", fallback)
		if not news.has("anchor"):
			unplaced += 1
		var rect := Rect2(point, Vector2(183, 61))
		# 扩区样本的入口不重叠；视觉点位是本底图的呈现数据，不改玩法坐标。
		for existing in occupied:
			if rect.intersects(existing.grow(8)):
				rect.position.y = existing.end.y + 12
		occupied.append(rect)
		if not _pins.has(id):
			var group := Control.new()
			group.name = "MapRegion_" + id
			group.size = rect.size
			group.mouse_filter = Control.MOUSE_FILTER_PASS
			_canvas.add_child(group)
			var paper := _paper(group, "Tag", Rect2(Vector2.ZERO, rect.size), "region-tag", Vector4(20, 14, 20, 14))
			var gold := _paper(group, "SelectedHoneyTag", Rect2(9, 5, 169, 53), "action-paper", Vector4(16, 14, 16, 14))
			var number_paper := _paper(group, "SelectedNumberPaper", Rect2(17, 15, 36, 29), "region-tag", Vector4.ZERO)
			number_paper.modulate = Color("193b41")
			var hit := _button(group, "SelectMapRegion", Rect2(Vector2.ZERO, rect.size), func() -> void: region_selected.emit(id))
			_style_selection_hit(hit)
			var number := _label(group, "RegionNumber", Rect2(19, 16, 33, 27), "", 19, INK, true)
			number.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			var label := _label(group, "RegionLabel", Rect2(58, 15, 113, 28), "", 19, INK, true)
			_pins[id] = {"root": group, "paper": paper, "gold": gold, "number_paper": number_paper, "number": number, "hit": hit, "label": label}
		var pin: Dictionary = _pins[id]
		pin.root.position = rect.position
		pin.hit.set_meta("region_id", id)
		pin.hit.set_meta("selected", id == _selected)
		pin.hit.tooltip_text = str(model.get("name", id)) + (" · 可进入" if bool(model.get("unlocked", false)) else " · 锁定，可预览")
		pin.number.text = "%02d" % (i + 1)
		pin.label.text = "%s%s" % [str(news.get("map_label", model.get("name", id))), "" if bool(model.get("unlocked", false)) else " · 锁"]
		pin.gold.visible = id == _selected
		pin.number_paper.visible = id == _selected
		pin.number.add_theme_color_override("font_color", PAPER if id == _selected else INK)
		pin.label.add_theme_color_override("font_color", INK if id == _selected else Color("253e40"))
		pin.paper.modulate = Color.WHITE if id == _selected else Color("b5c5b6")

func _render_tasks() -> void:
	var rows: Array = _payload.get("region_mission_preview", []) if _available else []
	var total := rows.size()
	_summary.disabled = total == 0
	_summary.visible = total > 0
	_summary_title.text = "地区任务 · %d" % total if _available else "地区任务 · 尚未解锁"
	_summary_hint.text = ("预览 %d / %d  ·  收起 −" % [mini(2, total), total] if _expanded else "展开任务预览 ＋") if total > 0 else ""
	_summary.tooltip_text = ("收起任务预览" if _expanded else "展开任务预览") if total > 0 else ""
	var counts: Dictionary = _payload.get("region_counts", {})
	_task_counts.text = "限时 %d   ·   线索 %d   ·   深链 %d" % [int(counts.get("deadline", 0)), int(counts.get("clue", 0)), int(counts.get("chain", 0))] if _available else "解锁后显示任务分布"
	_task_warning.text = str(_payload.get("region_warning_text", "进入地区后查看具体任务。")) if _available else "先满足地区解锁条件。"
	_task_warning.tooltip_text = _task_warning.text
	_task_warning.add_theme_color_override("font_color", _region_risk_color())
	_task_header.modulate = Color("386366") if _available else Color("627b79")
	_empty_tasks.visible = total == 0
	if not _models.has(_selected):
		_summary_title.text = "地区任务"
		_task_counts.text = "等待选择地区"
		_task_warning.text = ""
		_empty_tasks.text = "选择地区后查看调查机会。"
	elif not _available:
		_empty_tasks.text = str(_payload.get("region_unlock_gap", "尚未满足进入条件。"))
	elif total == 0:
		_empty_tasks.text = "地区已开放，当前暂无可用任务。\n仍可进入地区任务台查看。"
	else:
		_empty_tasks.text = "进入地区后选择具体任务。"
	for i in range(2):
		var show_row := _expanded and i < total
		_task_rows[i].visible = show_row
		if i < total:
			var row: Dictionary = rows[i]
			var kind := str(row.get("kind", "permanent"))
			var color := RUST if kind == "temp" else Color("2a6669") if kind == "chain" else MUTED
			_task_labels[i].text = str(row.get("name", "未命名任务"))
			_task_labels[i].tooltip_text = _task_labels[i].text
			_task_meta[i].text = "%s · 调查耗时 %d 天" % [str(row.get("kind_label", "线索")), int(row.get("days", 0))]
			_task_meta[i].add_theme_color_override("font_color", color)
	_layout_right_column()

func _region_risk_color() -> Color:
	if not _available:
		return MUTED
	match str(_payload.get("region_status_primary", "")):
		"红线升温":
			return RUST
		"青线追踪":
			return Color("2a6669")
	return MUTED

func set_mission_intel_expanded(value: bool) -> void:
	_expanded = value
	_render_tasks()

func _activate_primary() -> void:
	if _available and not _primary.disabled:
		enter_region_requested.emit()

func activate_primary_for_test() -> void:
	_activate_primary()

func _reveal_selected() -> void:
	if _cards.has(_selected):
		_scroll.ensure_control_visible(_cards[_selected].root)

func _update_connector() -> void:
	_connector.clear_points()
	for child in _connector.get_children():
		child.queue_free()
	_connector.visible = _pins.has(_selected)
	if _pins.has(_selected):
		var start: Vector2 = _pins[_selected].root.position + Vector2(65, 61)
		var points := [start, start + Vector2(16, 55), _evidence.position + Vector2(116, 7)]
		for i in range(points.size() - 1):
			var delta: Vector2 = points[i + 1] - points[i]
			var direction := delta.normalized()
			for distance in range(0, int(delta.length()), 27):
				var dash := Line2D.new()
				dash.width = 5
				dash.default_color = PAPER
				dash.antialiased = true
				dash.add_point(points[i] + direction * distance)
				dash.add_point(points[i] + direction * minf(distance + 13, delta.length()))
				_connector.add_child(dash)

func _update_list_hint() -> void:
	var bar := _scroll.get_v_scroll_bar()
	var has_more_below := bar.max_value - bar.page - bar.value > 1.0
	_list_hint.visible = has_more_below
	_list_hint.text = "更多地区 ↓   ·   共 %d 个地区" % _cards.size() if has_more_below else ""

func _style_scroll() -> void:
	var bar := _scroll.get_v_scroll_bar()
	bar.custom_minimum_size.x = 28
	bar.mouse_default_cursor_shape = Control.CURSOR_VSIZE
	bar.tooltip_text = "拖动纸签，或使用滚轮浏览地区"
	var track := _scroll_paper(Color("74999a"))
	bar.add_theme_stylebox_override("scroll", track)
	bar.add_theme_stylebox_override("scroll_focus", track)
	for key in ["grabber", "grabber_highlight", "grabber_pressed"]:
		var grab := _scroll_paper(Color.WHITE if key == "grabber" else Color("fff1ca"))
		bar.add_theme_stylebox_override(key, grab)
	# 固定刻度在轨道左沿，作为可拖动纸尺的轻量提示；不拥有热区。
	for i in range(31):
		var tick := Line2D.new()
		tick.name = "RulerTick%d" % i
		tick.width = 1.0
		tick.default_color = Color("244e54")
		tick.add_point(Vector2(3, 18 + i * 24))
		tick.add_point(Vector2(10 if i % 5 == 0 else 7, 18 + i * 24))
		bar.add_child(tick)

func _scroll_paper(tint: Color) -> StyleBoxTexture:
	var style := StyleBoxTexture.new()
	style.texture = Catalog.texture(Catalog.ASSET_DIR + "region-tag.png")
	# 只在控件采样时略去母图外部透明留边，避免细纸尺被透明边吃掉。
	style.region_rect = Rect2(18, 13, 334, 145)
	style.modulate_color = tint
	style.texture_margin_left = 4
	style.texture_margin_right = 8
	style.texture_margin_top = 10
	style.texture_margin_bottom = 12
	style.content_margin_left = 14
	style.content_margin_right = 14
	style.content_margin_top = 18
	style.content_margin_bottom = 18
	return style

func _label(parent: Node, node_name: String, rect: Rect2, value: String, px: int, color: Color = INK, bold: bool = false) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.text = value
	label.add_theme_font_override("font", _bold if bold else _font)
	label.add_theme_font_size_override("font_size", px)
	label.add_theme_color_override("font_color", color)
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.clip_text = true
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(label)
	return label

func _image(parent: Node, node_name: String, rect: Rect2, tex: Texture2D, keep_aspect: bool = true) -> TextureRect:
	var image := TextureRect.new()
	image.name = node_name
	image.position = rect.position
	image.size = rect.size
	image.texture = tex
	image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED if keep_aspect else TextureRect.STRETCH_SCALE
	image.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(image)
	return image

func _paper(parent: Node, node_name: String, rect: Rect2, filename: String, margins: Vector4) -> NinePatchRect:
	var paper := NinePatchRect.new()
	paper.name = node_name
	paper.position = rect.position
	paper.size = rect.size
	paper.texture = Catalog.texture(Catalog.ASSET_DIR + filename + ".png")
	paper.patch_margin_left = int(margins.x)
	paper.patch_margin_top = int(margins.y)
	paper.patch_margin_right = int(margins.z)
	paper.patch_margin_bottom = int(margins.w)
	paper.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	paper.material = _paper_material
	paper.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(paper)
	return paper

func _button(parent: Node, node_name: String, rect: Rect2, action: Callable) -> Button:
	var button := Button.new()
	button.name = node_name
	button.position = rect.position
	button.size = rect.size
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	button.focus_mode = Control.FOCUS_ALL
	button.add_theme_stylebox_override("normal", StyleBoxEmpty.new())
	button.add_theme_stylebox_override("disabled", StyleBoxEmpty.new())
	for key in ["hover", "pressed", "focus"]:
		var style := StyleBoxFlat.new()
		style.bg_color = Color(0.7, 0.92, 0.88, 0.07 if key == "hover" else 0.12)
		style.border_color = TEAL if key != "focus" else HONEY
		style.set_border_width_all(2)
		button.add_theme_stylebox_override(key, style)
	button.pressed.connect(action)
	parent.add_child(button)
	return button

func _rule(rect: Rect2, color: Color) -> void:
	var line := ColorRect.new()
	line.position = rect.position
	line.size = rect.size
	line.color = color
	line.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_canvas.add_child(line)

func get_dossier() -> Control:
	return self

func get_state_snapshot() -> Dictionary:
	var shared := false
	if _cards.has(_selected):
		shared = _cards[_selected].photo.texture == _photo.texture and _photo.texture == _evidence_photo.texture
	return {
		"selected_region_id": _selected, "dossier_region_id": _selected,
		"region_count": _cards.size(), "map_region_count": _pins.size(),
		"shared_texture_identity": shared, "photo_path": _photo.texture.resource_path if _photo.texture else "",
		"image_keep_aspect": _photo.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_CENTERED,
		"expanded": _expanded, "primary_disabled": _primary.disabled,
		"primary_rect": [PRIMARY_RECT.position.x, PRIMARY_RECT.position.y, PRIMARY_RECT.size.x, PRIMARY_RECT.size.y],
		"task_total": (_payload.get("region_mission_preview", []) as Array).size() if _available else 0,
		"scroll_vertical": _scroll.scroll_vertical,
		"empty_text": _empty_tasks.text, "title": _region_title.text,
		"task_counts_text": _task_counts.text, "task_warning_text": _task_warning.text,
		"remaining_days_text": _remaining_days.text,
		"task_paper_rect": [_task_paper.position.x, _task_paper.position.y, _task_paper.size.x, _task_paper.size.y],
		"photo_rect": [_photo.position.x, _photo.position.y, _photo.size.x, _photo.size.y],
		"artifact_type": "godot_runtime_soft_columns", "schedule_read_only": true,
	}

func set_debug_zones(_enabled: bool) -> void:
	pass
