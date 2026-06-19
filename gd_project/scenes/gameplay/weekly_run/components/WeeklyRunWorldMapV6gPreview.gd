extends Control

const WorldMapManifest := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssetManifest.gd")

const LOGICAL_SIZE := Vector2(1920.0, 1080.0)

const ASSET_LEFT_INDEX := "wm_left_index_stack_v6g_component_candidate"
const ASSET_MAP_BOARD := "wm_map_board_v6g_component_candidate"
const ASSET_RIGHT_DOSSIER := "wm_right_dossier_body_v6g_component_candidate"
const ASSET_CTA_DEFAULT := "wm_cta_plate_v6g_default_candidate"
const ASSET_BOTTOM_TICKER := "wm_bottom_ticker_v6g_component_candidate"
const ASSET_SIDE_TABS := "wm_side_tab_rail_v6g_component_candidate"
const ASSET_CTA_ATLAS := "wm_cta_plate_v6g_state_atlas_candidate"
const ASSET_PIN_ATLAS := "wm_pin_icon_v6g_atlas_candidate"
const ASSET_STORY_PREVIEW_NORTH_AMERICA := "wm_story_preview_north_america"

const TEXT_BODY := "body"
const TEXT_META := "meta"
const TEXT_QUIET_TITLE := "quiet_title"
const TEXT_SELECTED_TITLE := "selected_title"
const TEXT_DOSSIER_TITLE := "dossier_title"
const TEXT_SECTION := "section"
const TEXT_FOOTER := "footer"
const TEXT_TICKER := "ticker"
const TEXT_CTA := "cta"

var show_debug_zones := false
var show_task_intel_popover := false

var _manifest: Dictionary = {}
var _manifest_v5: Dictionary = {}
var _world_root: Control
var _ui_font: SystemFont
var _task_intel_popover_nodes: Array[CanvasItem] = []

func configure(debug_zones: bool = false, task_intel_open: bool = false) -> void:
	show_debug_zones = debug_zones
	show_task_intel_popover = task_intel_open

func _ready() -> void:
	_setup_font()
	_manifest = WorldMapManifest.load_manifest_v6()
	_manifest_v5 = WorldMapManifest.load_manifest()
	_build_preview()
	_layout_world_root()

func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED and _world_root != null:
		_layout_world_root()

func _build_preview() -> void:
	_world_root = Control.new()
	_world_root.name = "WorldMapV6gPreviewRoot"
	_world_root.custom_minimum_size = LOGICAL_SIZE
	_world_root.size = LOGICAL_SIZE
	add_child(_world_root)

	var background := ColorRect.new()
	background.name = "DeepNavyBackground"
	background.color = Color(0.015, 0.029, 0.045, 1.0)
	background.position = Vector2.ZERO
	background.size = LOGICAL_SIZE
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_world_root.add_child(background)

	_add_component(ASSET_LEFT_INDEX)
	_add_component(ASSET_MAP_BOARD)
	_add_component(ASSET_RIGHT_DOSSIER)
	_add_component(ASSET_BOTTOM_TICKER)
	_add_component(ASSET_SIDE_TABS)
	_add_cta_component()
	_add_routes_and_pins()
	_add_dynamic_text()

	if show_debug_zones:
		_add_debug_zones()

func _setup_font() -> void:
	_ui_font = SystemFont.new()
	_ui_font.font_names = PackedStringArray([
		"Microsoft YaHei",
		"Microsoft YaHei UI",
		"Source Han Sans SC",
		"Noto Sans CJK SC",
		"Noto Sans SC",
		"HarmonyOS Sans SC",
		"DengXian",
		"SimHei",
		"Arial Unicode MS",
	])

func _layout_world_root() -> void:
	if _world_root == null:
		return
	var scale_factor := minf(size.x / LOGICAL_SIZE.x, size.y / LOGICAL_SIZE.y)
	if scale_factor <= 0.0:
		scale_factor = 1.0
	_world_root.scale = Vector2(scale_factor, scale_factor)
	_world_root.position = (size - LOGICAL_SIZE * scale_factor) * 0.5

func _add_component(asset_id: String) -> TextureRect:
	var texture := WorldMapManifest.load_asset_texture(asset_id, _manifest)
	var rect := _asset_runtime_rect(asset_id)
	var node := TextureRect.new()
	node.name = asset_id
	node.texture = texture
	node.position = rect.position
	node.size = rect.size
	node.stretch_mode = TextureRect.STRETCH_SCALE
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	node.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	node.z_index = 2
	_world_root.add_child(node)
	return node

func _add_cta_component() -> void:
	var rect := _asset_runtime_rect(ASSET_CTA_DEFAULT)
	var texture := WorldMapManifest.load_asset_frame_texture(ASSET_CTA_ATLAS, "default", _manifest)
	if texture == null:
		texture = WorldMapManifest.load_asset_texture(ASSET_CTA_DEFAULT, _manifest)

	var cta := TextureRect.new()
	cta.name = "PrimaryCtaDefaultFrame"
	cta.texture = texture
	cta.position = rect.position
	cta.size = rect.size
	cta.stretch_mode = TextureRect.STRETCH_SCALE
	cta.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	cta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cta.z_index = 6
	_world_root.add_child(cta)

	var hit := Button.new()
	hit.name = "PrimaryCtaHitPreview"
	hit.text = ""
	hit.position = rect.position
	hit.size = rect.size
	hit.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	hit.focus_mode = Control.FOCUS_NONE
	hit.flat = true
	hit.z_index = 8
	_make_button_transparent(hit)
	_world_root.add_child(hit)

func _add_routes_and_pins() -> void:
	var map_asset := WorldMapManifest.get_asset(ASSET_MAP_BOARD, _manifest)
	var map_rect := _asset_runtime_rect(ASSET_MAP_BOARD)
	var anchors: Dictionary = map_asset.get("anchor_points", {})

	var north := _anchor_to_screen(anchors, map_rect, "north_america")
	var south := _anchor_to_screen(anchors, map_rect, "south_america")
	var europe := _anchor_to_screen(anchors, map_rect, "europe_africa")
	var east_asia := _anchor_to_screen(anchors, map_rect, "east_asia")
	var oceania := _anchor_to_screen(anchors, map_rect, "oceania")

	_add_route_line([north, europe, east_asia], Color(0.82, 0.10, 0.07, 0.86), 4.0, "SelectedRedRoute")
	_add_route_line([north, south], Color(0.04, 0.72, 0.76, 0.60), 3.0, "SelectedCyanTrace")
	_add_route_line([south, europe, oceania], Color(0.40, 0.62, 0.66, 0.18), 2.0, "DimmedBackgroundRoute")

	_add_selection_halo(north)
	_add_pin("pin_selected", north, "NorthAmericaSelectedPin", Color(1, 1, 1, 1), Vector2(64.0, 64.0))
	_add_pin("pin_normal", south, "SouthAmericaDimmedPin", Color(0.70, 0.88, 0.88, 0.58), Vector2(48.0, 48.0), Vector2(-6.0, -4.0))
	_add_pin("pin_urgent", europe, "EuropeAfricaDimmedPin", Color(0.95, 0.66, 0.58, 0.68), Vector2(46.0, 46.0), Vector2(8.0, -20.0))
	_add_pin("pin_locked", east_asia, "EastAsiaDimmedPin", Color(0.58, 0.66, 0.70, 0.54), Vector2(46.0, 46.0), Vector2(4.0, -12.0))
	_add_pin("pin_completed", oceania, "OceaniaDimmedPin", Color(0.60, 0.72, 0.76, 0.52), Vector2(46.0, 46.0), Vector2(-8.0, -14.0))

func _add_route_line(points: Array, color: Color, width: float, node_name: String) -> void:
	var line := Line2D.new()
	line.name = node_name
	line.points = PackedVector2Array(points)
	line.width = width
	line.default_color = color
	line.joint_mode = Line2D.LINE_JOINT_SHARP
	line.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	line.z_index = 12
	_world_root.add_child(line)

func _add_selection_halo(anchor: Vector2) -> void:
	var halo := Line2D.new()
	halo.name = "NorthAmericaSelectedHalo"
	var points := PackedVector2Array()
	var radius := 42.0
	for i in range(16):
		var angle := TAU * float(i) / 15.0
		points.append(anchor + Vector2(cos(angle), sin(angle)) * radius)
	halo.points = points
	halo.width = 3.0
	halo.default_color = Color(0.94, 0.78, 0.34, 0.90)
	halo.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	halo.z_index = 16
	_world_root.add_child(halo)

	var offset_halo := Line2D.new()
	offset_halo.name = "NorthAmericaSelectedCyanOffset"
	offset_halo.points = points
	offset_halo.position = Vector2(4.0, -3.0)
	offset_halo.width = 2.0
	offset_halo.default_color = Color(0.05, 0.75, 0.82, 0.45)
	offset_halo.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	offset_halo.z_index = 15
	_world_root.add_child(offset_halo)

func _add_pin(frame_id: String, anchor: Vector2, node_name: String, tint: Color, pin_size: Vector2, visual_offset: Vector2 = Vector2.ZERO) -> void:
	var texture := WorldMapManifest.load_asset_frame_texture(ASSET_PIN_ATLAS, frame_id, _manifest)
	var pin := TextureRect.new()
	pin.name = node_name
	pin.texture = texture
	pin.position = anchor + visual_offset - Vector2(pin_size.x * 0.5, pin_size.y * 0.88)
	pin.size = pin_size
	pin.modulate = tint
	pin.stretch_mode = TextureRect.STRETCH_SCALE
	pin.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	pin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	pin.z_index = 18
	_world_root.add_child(pin)

	var hit := Control.new()
	hit.name = "%sHitRect" % node_name
	hit.position = anchor - Vector2(22.0, 52.0)
	hit.size = Vector2(44.0, 56.0)
	hit.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	hit.z_index = 19
	_world_root.add_child(hit)

func _add_dynamic_text() -> void:
	var ink := Color(0.055, 0.075, 0.064, 1.0)
	var muted := Color(0.24, 0.30, 0.26, 0.88)
	var quiet := Color(0.30, 0.36, 0.34, 0.64)
	var red := Color(0.62, 0.10, 0.07, 1.0)
	var cyan := Color(0.02, 0.42, 0.45, 1.0)
	var gold := Color(0.58, 0.39, 0.08, 1.0)
	var navy := Color(0.025, 0.070, 0.105, 1.0)

	_add_top_status_strip(ink, red, cyan, gold)
	_add_selected_index_overlay()
	_add_label(ASSET_LEFT_INDEX, "slot_1_title", "北美禁区带", 23, ink, 1, HORIZONTAL_ALIGNMENT_LEFT, true)
	_add_label(ASSET_LEFT_INDEX, "slot_1_meta", "可进入 · 红线升温\n难度 中等  推荐 ★★★★", 16, muted, 2, HORIZONTAL_ALIGNMENT_LEFT)
	_add_label(ASSET_LEFT_INDEX, "slot_2_title", "东亚神秘地带", 19, quiet, 1, HORIZONTAL_ALIGNMENT_LEFT)
	_add_label(ASSET_LEFT_INDEX, "slot_2_meta", "锁定 · 声望 31/40\n难度 高  推荐 ★★", 15, quiet, 2, HORIZONTAL_ALIGNMENT_LEFT)
	_add_label(ASSET_LEFT_INDEX, "slot_3_title", "太平洋失航带", 19, quiet, 1, HORIZONTAL_ALIGNMENT_LEFT)
	_add_label(ASSET_LEFT_INDEX, "slot_3_meta", "可进入 · 普通线报\n难度 低  推荐 ★★★", 15, quiet, 2, HORIZONTAL_ALIGNMENT_LEFT)
	_add_label(ASSET_LEFT_INDEX, "slot_4_title", "南美红线档", 19, quiet, 1, HORIZONTAL_ALIGNMENT_LEFT)
	_add_label(ASSET_LEFT_INDEX, "slot_4_meta", "封存 · 许可不足\n难度 异常  推荐 ★", 15, quiet, 2, HORIZONTAL_ALIGNMENT_LEFT)

	_add_right_dossier_a80(ink, muted, red, cyan, gold, navy)

	_add_label(ASSET_BOTTOM_TICKER, "red_channel_status", "最新记录：城市频谱出现升温", 19, red, 1, HORIZONTAL_ALIGNMENT_LEFT, true)
	_add_label(ASSET_BOTTOM_TICKER, "cyan_channel_status", "档案更新：新增异常证词", 19, cyan, 1, HORIZONTAL_ALIGNMENT_LEFT, true)
	_add_label(ASSET_BOTTOM_TICKER, "navy_channel_status", "地区预警：进入后再选择线报", 19, ink, 1, HORIZONTAL_ALIGNMENT_LEFT, true)

	_add_label(ASSET_CTA_DEFAULT, "cta_label", "进入选定地区", 28, ink, 1, HORIZONTAL_ALIGNMENT_CENTER, true)

func _add_top_status_strip(ink: Color, red: Color, cyan: Color, gold: Color) -> void:
	var strip_rect := Rect2(Vector2(58.0, 30.0), Vector2(1798.0, 58.0))
	_add_panel_box(strip_rect, Color(0.010, 0.030, 0.045, 0.94), Color(0.03, 0.42, 0.48, 0.78), "A80TopStatusStrip", 22, 2, 0)
	_add_panel_box(Rect2(Vector2(88.0, 38.0), Vector2(210.0, 42.0)), Color(0.93, 0.87, 0.74, 0.95), Color(0.18, 0.22, 0.22, 0.72), "A80WeekTicket", 23, 2, 0)
	_add_panel_box(Rect2(Vector2(320.0, 38.0), Vector2(190.0, 42.0)), Color(0.93, 0.87, 0.74, 0.95), Color(0.18, 0.22, 0.22, 0.72), "A80DaysTicket", 23, 2, 0)
	_add_runtime_label(Rect2(Vector2(122.0, 43.0), Vector2(150.0, 32.0)), "探索周 01", 22, ink, 1, HORIZONTAL_ALIGNMENT_CENTER, true, 0, Color.TRANSPARENT, "A80WeekLabel", TEXT_SELECTED_TITLE)
	_add_runtime_label(Rect2(Vector2(352.0, 43.0), Vector2(128.0, 32.0)), "剩余 7 天", 22, ink, 1, HORIZONTAL_ALIGNMENT_CENTER, true, 0, Color.TRANSPARENT, "A80DaysLabel", TEXT_SELECTED_TITLE)

	var rail_rect := Rect2(Vector2(610.0, 36.0), Vector2(1005.0, 46.0))
	_add_panel_box(rail_rect, Color(0.015, 0.058, 0.082, 0.95), Color(0.09, 0.31, 0.36, 0.82), "A80WorldStateRail", 23, 2, 0)
	_add_runtime_label(Rect2(Vector2(636.0, 43.0), Vector2(92.0, 30.0)), "世界状态", 17, Color(0.61, 0.77, 0.75, 0.88), 1, HORIZONTAL_ALIGNMENT_LEFT, false, 0, Color.TRANSPARENT, "A80WorldStateLabel", TEXT_META)
	var metrics := [
		{"label": "公信", "value": "42", "color": cyan},
		{"label": "诡名", "value": "18", "color": red},
		{"label": "声望", "value": "31", "color": gold},
		{"label": "守序", "value": "26", "color": Color(0.20, 0.58, 0.82, 1.0)},
		{"label": "狂性", "value": "11", "color": Color(0.82, 0.12, 0.10, 1.0)}
	]
	for i in range(metrics.size()):
		var item: Dictionary = metrics[i]
		var x := 748.0 + float(i) * 162.0
		_add_macro_chip(Rect2(Vector2(x, 43.0), Vector2(132.0, 32.0)), str(item["label"]), str(item["value"]), item["color"])

func _add_macro_chip(rect: Rect2, label: String, value: String, color: Color) -> void:
	_add_panel_box(rect, Color(color.r, color.g, color.b, 0.10), Color(color.r, color.g, color.b, 0.72), "A80MacroChip_%s" % label, 24, 1, 0)
	_add_runtime_label(Rect2(rect.position + Vector2(12.0, 2.0), Vector2(62.0, 28.0)), label, 17, Color(0.88, 0.91, 0.84, 1.0), 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80MacroLabel_%s" % label, TEXT_META)
	_add_runtime_label(Rect2(rect.position + Vector2(76.0, 2.0), Vector2(38.0, 28.0)), value, 18, color, 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80MacroValue_%s" % label, TEXT_META)

func _add_right_dossier_a80(ink: Color, muted: Color, red: Color, cyan: Color, gold: Color, navy: Color) -> void:
	var asset_rect := _asset_runtime_rect(ASSET_RIGHT_DOSSIER)
	var origin := asset_rect.position

	_add_runtime_label(Rect2(origin + Vector2(54.0, 44.0), Vector2(128.0, 24.0)), "区域档案 01", 16, red, 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80DossierSlotLabel", TEXT_META)
	_add_runtime_label(Rect2(origin + Vector2(54.0, 76.0), Vector2(220.0, 38.0)), "北美禁区带", 28, ink, 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80DossierTitle", TEXT_DOSSIER_TITLE)
	_add_badge(Rect2(origin + Vector2(278.0, 78.0), Vector2(64.0, 28.0)), "中等", gold)
	_add_badge(Rect2(origin + Vector2(350.0, 78.0), Vector2(110.0, 28.0)), "推荐 ★★★★", cyan)

	var image_rect := Rect2(origin + Vector2(52.0, 124.0), Vector2(384.0, 114.0))
	_add_region_preview_image(image_rect)

	var state_rect := Rect2(origin + Vector2(52.0, 252.0), Vector2(384.0, 36.0))
	_add_ticket_panel(state_rect, red, "A80RedStateTicket", true)
	_add_runtime_label(Rect2(state_rect.position + Vector2(16.0, 2.0), Vector2(352.0, 32.0)), "红线升温 / 可进入 / 7天内提升狂性风险", 17, Color(0.92, 0.86, 0.72, 1.0), 1, HORIZONTAL_ALIGNMENT_CENTER, true, 0, Color.TRANSPARENT, "A80StateTicketLabel", TEXT_META)

	var task_rect := Rect2(origin + Vector2(82.0, 306.0), Vector2(312.0, 44.0))
	_add_task_intel_button(task_rect, "查看任务情报 · 3", cyan)

	var body_top := origin + Vector2(52.0, 360.0)
	_add_runtime_label(Rect2(body_top, Vector2(330.0, 24.0)), "地区特征", 18, cyan, 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80BodyFeatureTitle", TEXT_SECTION)
	_add_runtime_label(Rect2(body_top + Vector2(0.0, 26.0), Vector2(360.0, 34.0)), "城市传说与军事封锁交叠，异常信号活跃频发。", 15, ink, 2, HORIZONTAL_ALIGNMENT_LEFT, false, 0, Color.TRANSPARENT, "A80BodyFeatureText", TEXT_BODY)
	_add_runtime_label(Rect2(body_top + Vector2(0.0, 72.0), Vector2(330.0, 24.0)), "本周异变", 18, cyan, 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80BodyAnomalyTitle", TEXT_SECTION)
	_add_runtime_label(Rect2(body_top + Vector2(0.0, 98.0), Vector2(360.0, 34.0)), "红线升温：7 天内提升狂性风险。", 15, red, 2, HORIZONTAL_ALIGNMENT_LEFT, false, 0, Color.TRANSPARENT, "A80BodyAnomalyText", TEXT_BODY)
	_add_runtime_label(Rect2(body_top + Vector2(0.0, 144.0), Vector2(330.0, 24.0)), "可带回素材", 18, cyan, 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80BodyMaterialTitle", TEXT_SECTION)
	_add_runtime_label(Rect2(body_top + Vector2(0.0, 170.0), Vector2(360.0, 34.0)), "目击证词 / 封锁传闻 / 异常广播。", 15, ink, 2, HORIZONTAL_ALIGNMENT_LEFT, false, 0, Color.TRANSPARENT, "A80BodyMaterialText", TEXT_BODY)
	_add_runtime_label(Rect2(body_top + Vector2(0.0, 216.0), Vector2(330.0, 24.0)), "地区预警", 18, cyan, 1, HORIZONTAL_ALIGNMENT_LEFT, true, 0, Color.TRANSPARENT, "A80BodyWarningTitle", TEXT_SECTION)
	_add_runtime_label(Rect2(body_top + Vector2(0.0, 242.0), Vector2(360.0, 36.0)), "进入后本屏不消耗天数；具体线报在地区任务台选择。", 14, gold, 2, HORIZONTAL_ALIGNMENT_LEFT, false, 0, Color.TRANSPARENT, "A80BodyWarningText", TEXT_FOOTER)

	_add_task_intel_popover(Rect2(origin + Vector2(-372.0, 282.0), Vector2(430.0, 330.0)), navy, ink, red, cyan, gold)
	set_task_intel_popover_visible(show_task_intel_popover)

func _add_region_preview_image(rect: Rect2) -> void:
	_add_panel_box(rect.grow(3.0), Color(0.010, 0.025, 0.034, 1.0), Color(0.13, 0.18, 0.18, 0.90), "A80RegionImageFrame", 27, 2, 0)
	var texture := WorldMapManifest.load_asset_texture(ASSET_STORY_PREVIEW_NORTH_AMERICA, _manifest_v5)
	if texture == null:
		return
	var image := TextureRect.new()
	image.name = "A80RegionImageNorthAmerica"
	image.texture = texture
	image.position = rect.position
	image.size = rect.size
	image.clip_contents = true
	image.stretch_mode = TextureRect.STRETCH_SCALE
	image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	image.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	image.z_index = 28
	_world_root.add_child(image)

func _add_task_intel_button(rect: Rect2, text: String, cyan: Color) -> void:
	_add_rule_rect(Rect2(rect.position + Vector2(4.0, 5.0), rect.size), Color(0.0, 0.0, 0.0, 0.22), "A80TaskIntelShadow", 29)
	_add_ticket_panel(rect, cyan, "A80TaskIntelTicket", true)
	_add_runtime_label(Rect2(rect.position + Vector2(22.0, 4.0), Vector2(rect.size.x - 74.0, rect.size.y - 8.0)), text, 18, Color(0.90, 0.98, 0.94, 1.0), 1, HORIZONTAL_ALIGNMENT_LEFT, true, 1, Color(0.0, 0.08, 0.08, 0.45), "A80TaskIntelLabel", TEXT_SELECTED_TITLE)
	_add_runtime_label(Rect2(rect.position + Vector2(rect.size.x - 48.0, 3.0), Vector2(32.0, rect.size.y - 6.0)), ">", 24, Color(0.98, 0.91, 0.64, 1.0), 1, HORIZONTAL_ALIGNMENT_CENTER, true, 1, Color(0.0, 0.08, 0.08, 0.45), "A80TaskIntelArrow", TEXT_SELECTED_TITLE)

	var hit := Button.new()
	hit.name = "A80TaskIntelHitPreview"
	hit.text = ""
	hit.position = rect.position
	hit.size = rect.size
	hit.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	hit.focus_mode = Control.FOCUS_NONE
	hit.z_index = 37
	_make_button_transparent(hit)
	hit.pressed.connect(_on_task_intel_pressed)
	_world_root.add_child(hit)

func _add_task_intel_popover(rect: Rect2, navy: Color, ink: Color, red: Color, cyan: Color, gold: Color) -> void:
	_task_intel_popover_nodes.clear()
	_register_task_popover_node(_add_rule_rect(Rect2(rect.position + Vector2(7.0, 9.0), rect.size), Color(0.0, 0.0, 0.0, 0.26), "A80TaskPopoverShadow", 38))
	_register_task_popover_node(_add_panel_box(rect, Color(0.93, 0.87, 0.74, 0.98), Color(0.16, 0.21, 0.19, 0.92), "A80TaskIntelPopover", 39, 2, 0))
	_register_task_popover_node(_add_panel_box(Rect2(rect.position + Vector2(24.0, 20.0), Vector2(194.0, 36.0)), Color(cyan.r, cyan.g, cyan.b, 0.92), Color(cyan.r, cyan.g, cyan.b, 1.0), "A80PopoverTitlePlate", 40, 2, 0))
	_register_task_popover_node(_add_overlay_label(Rect2(rect.position + Vector2(38.0, 24.0), Vector2(170.0, 28.0)), "本区可追踪任务 3", 18, Color(0.92, 0.98, 0.94, 1.0), 1, HORIZONTAL_ALIGNMENT_LEFT, true, "A80PopoverTitle", 45))
	_register_task_popover_node(_add_overlay_label(Rect2(rect.position + Vector2(28.0, 64.0), Vector2(356.0, 26.0)), "只读预览，进入地区后再选择具体线报。", 15, Color(0.24, 0.30, 0.26, 0.88), 1, HORIZONTAL_ALIGNMENT_LEFT, false, "A80PopoverSubtitle", 45))

	_add_popover_row(Rect2(rect.position + Vector2(28.0, 104.0), Vector2(374.0, 58.0)), "民间传言：异常目击", "成本 2天 / 条件 人脉2", red)
	_add_popover_row(Rect2(rect.position + Vector2(28.0, 174.0), Vector2(374.0, 58.0)), "球状闪电：厨房火球", "成本 1天 / 条件 理性2", cyan)
	_add_popover_row(Rect2(rect.position + Vector2(28.0, 244.0), Vector2(374.0, 58.0)), "51区外围公路", "成本 2天 / 条件 探索2", gold)
	_register_task_popover_node(_add_overlay_label(Rect2(rect.position + Vector2(30.0, 302.0), Vector2(360.0, 24.0)), "无派遣、无骰池、无成功率；本弹窗仅说明任务池。", 14, Color(0.36, 0.26, 0.12, 0.90), 1, HORIZONTAL_ALIGNMENT_LEFT, false, "A80PopoverFooter", 45))

func _add_popover_row(rect: Rect2, title: String, meta: String, accent: Color) -> void:
	_register_task_popover_node(_add_panel_box(rect, Color(0.98, 0.92, 0.79, 0.92), Color(0.30, 0.34, 0.30, 0.62), "A80PopoverRow_%s" % title, 41, 1, 0))
	_register_task_popover_node(_add_rule_rect(Rect2(rect.position, Vector2(6.0, rect.size.y)), Color(accent.r, accent.g, accent.b, 0.86), "A80PopoverRowAccent_%s" % title, 42))
	_register_task_popover_node(_add_overlay_label(Rect2(rect.position + Vector2(16.0, 5.0), Vector2(rect.size.x - 30.0, 24.0)), title, 16, Color(0.08, 0.10, 0.08, 1.0), 1, HORIZONTAL_ALIGNMENT_LEFT, true, "A80PopoverRowTitle_%s" % title, 45))
	_register_task_popover_node(_add_overlay_label(Rect2(rect.position + Vector2(16.0, 30.0), Vector2(rect.size.x - 30.0, 22.0)), meta, 14, Color(0.29, 0.32, 0.28, 0.95), 1, HORIZONTAL_ALIGNMENT_LEFT, false, "A80PopoverRowMeta_%s" % title, 45))

func _register_task_popover_node(node: CanvasItem) -> void:
	_task_intel_popover_nodes.append(node)

func _on_task_intel_pressed() -> void:
	set_task_intel_popover_visible(not show_task_intel_popover)

func set_task_intel_popover_visible(visible: bool) -> void:
	show_task_intel_popover = visible
	for node in _task_intel_popover_nodes:
		if is_instance_valid(node):
			node.visible = visible

func _add_overlay_label(
	rect: Rect2,
	text: String,
	font_size: int,
	color: Color,
	max_lines: int,
	alignment: HorizontalAlignment,
	bold: bool,
	node_name: String,
	z_index: int
) -> Label:
	return _add_runtime_label_layer(rect, text, font_size, color, max_lines, alignment, bold, 0, Color.TRANSPARENT, node_name, z_index, Vector2.ZERO)

func _add_ticket_panel(rect: Rect2, color: Color, node_name: String, raised: bool) -> void:
	var bg_alpha := 0.90 if raised else 0.18
	var bg := Color(color.r, color.g, color.b, bg_alpha)
	var border := Color(color.r, color.g, color.b, 0.98)
	_add_panel_box(rect, bg, border, node_name, 30, 2, 0)
	if raised:
		_add_rule_rect(Rect2(rect.position + Vector2(12.0, 4.0), Vector2(rect.size.x - 24.0, 2.0)), Color(1.0, 1.0, 1.0, 0.16), "%sTopHighlight" % node_name, 31)
		_add_rule_rect(Rect2(rect.position + Vector2(12.0, rect.size.y - 5.0), Vector2(rect.size.x - 24.0, 2.0)), Color(0.0, 0.0, 0.0, 0.18), "%sBottomShade" % node_name, 31)

func _add_panel_box(rect: Rect2, bg_color: Color, border_color: Color, node_name: String, z_index: int, border_width: int = 1, radius: int = 0) -> Panel:
	var panel := Panel.new()
	panel.name = node_name
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.z_index = z_index
	var style := StyleBoxFlat.new()
	style.bg_color = bg_color
	style.border_color = border_color
	style.set_border_width_all(border_width)
	style.set_corner_radius_all(radius)
	panel.add_theme_stylebox_override("panel", style)
	_world_root.add_child(panel)
	return panel

func _add_selected_index_overlay() -> void:
	var asset_rect := _asset_runtime_rect(ASSET_LEFT_INDEX)
	var panel := Panel.new()
	panel.name = "NorthAmericaIndexSelectedOverlay"
	panel.position = asset_rect.position + Vector2(60.0, 16.0)
	panel.size = Vector2(315.0, 150.0)
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.z_index = 24
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.92, 0.74, 0.22, 0.030)
	style.border_color = Color.TRANSPARENT
	style.set_border_width_all(0)
	panel.add_theme_stylebox_override("panel", style)
	_world_root.add_child(panel)
	_add_corner_brackets(Rect2(panel.position, panel.size), Color(0.88, 0.66, 0.20, 0.90), "NorthAmericaIndexSelectedBrackets", 25)

func _add_region_status_badges(red: Color, cyan: Color) -> void:
	var status_rect := _global_text_rect(ASSET_RIGHT_DOSSIER, "story_preview_caption_or_status")
	_add_badge(Rect2(status_rect.position + Vector2(0.0, -2.0), Vector2(98.0, 26.0)), "红线升温", red)
	_add_badge(Rect2(status_rect.position + Vector2(112.0, -2.0), Vector2(82.0, 26.0)), "可进入", cyan)
	_add_runtime_label(
		Rect2(status_rect.position + Vector2(0.0, 30.0), Vector2(status_rect.size.x, 24.0)),
		"本周取材区已打开",
		17,
		Color(0.24, 0.30, 0.26, 0.88),
		1,
		HORIZONTAL_ALIGNMENT_LEFT
	)

func _add_badge(rect: Rect2, text: String, color: Color) -> void:
	var panel := Panel.new()
	panel.name = "StatusBadge_%s" % text
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.z_index = 31
	var style := StyleBoxFlat.new()
	style.bg_color = Color(color.r, color.g, color.b, 0.12)
	style.border_color = Color(color.r, color.g, color.b, 0.82)
	style.set_border_width_all(2)
	panel.add_theme_stylebox_override("panel", style)
	_world_root.add_child(panel)

	var label := Label.new()
	label.name = "%s_Label" % panel.name
	label.text = text
	label.position = rect.position + Vector2(7.0, 1.0)
	label.size = rect.size - Vector2(14.0, 2.0)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.z_index = 32
	label.add_theme_font_override("font", _ui_font)
	label.add_theme_font_size_override("font_size", 15)
	label.add_theme_color_override("font_color", color)
	label.add_theme_color_override("font_outline_color", Color(1.0, 0.96, 0.84, 0.35))
	label.add_theme_constant_override("outline_size", 1)
	_world_root.add_child(label)

func _add_label(
	asset_id: String,
	rect_id: String,
	text: String,
	font_size: int,
	color: Color,
	max_lines: int,
	alignment: HorizontalAlignment,
	bold: bool = false,
	outline_size: int = 0,
	outline_color: Color = Color.TRANSPARENT
) -> Label:
	var rect := _global_text_rect(asset_id, rect_id)
	var treatment := _text_treatment_for(asset_id, rect_id, max_lines, bold)
	_add_text_backing(rect, treatment, color, "%s_%s_Backing" % [asset_id, rect_id])
	return _add_runtime_label(rect, text, font_size, color, max_lines, alignment, bold, outline_size, outline_color, "%s_%s" % [asset_id, rect_id], treatment)

func _add_runtime_label(
	rect: Rect2,
	text: String,
	font_size: int,
	color: Color,
	max_lines: int,
	alignment: HorizontalAlignment,
	bold: bool = false,
	outline_size: int = 0,
	outline_color: Color = Color.TRANSPARENT,
	node_name: String = "RuntimeText",
	treatment: String = TEXT_BODY
) -> Label:
	_add_text_ink_layers(rect, text, font_size, color, max_lines, alignment, bold, node_name, treatment)
	return _add_runtime_label_layer(rect, text, font_size, color, max_lines, alignment, bold, outline_size, outline_color, node_name, 30, Vector2.ZERO)

func _add_runtime_label_layer(
	rect: Rect2,
	text: String,
	font_size: int,
	color: Color,
	max_lines: int,
	alignment: HorizontalAlignment,
	bold: bool,
	outline_size: int,
	outline_color: Color,
	node_name: String,
	z_index: int,
	offset: Vector2
) -> Label:
	var label := Label.new()
	label.name = node_name
	label.text = text
	label.position = rect.position + offset
	label.size = rect.size
	label.horizontal_alignment = alignment
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER if max_lines <= 1 else VERTICAL_ALIGNMENT_TOP
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.clip_text = true
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.max_lines_visible = max_lines
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.z_index = z_index
	label.add_theme_font_override("font", _ui_font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.add_theme_constant_override("line_spacing", 5 if font_size >= 19 else 3)
	label.add_theme_constant_override("outline_size", outline_size)
	label.add_theme_color_override("font_outline_color", outline_color)
	if bold:
		label.add_theme_constant_override("outline_size", max(outline_size, 1))
		label.add_theme_color_override("font_outline_color", Color(1.0, 0.96, 0.84, 0.34))
	_world_root.add_child(label)
	return label

func _add_text_ink_layers(
	rect: Rect2,
	text: String,
	font_size: int,
	color: Color,
	max_lines: int,
	alignment: HorizontalAlignment,
	bold: bool,
	node_name: String,
	treatment: String
) -> void:
	var shadow_alpha := 0.10
	if treatment in [TEXT_CTA, TEXT_DOSSIER_TITLE, TEXT_SELECTED_TITLE, TEXT_SECTION]:
		shadow_alpha = 0.18
	elif treatment in [TEXT_META, TEXT_FOOTER]:
		shadow_alpha = 0.07
	_add_runtime_label_layer(
		rect,
		text,
		font_size,
		Color(0.00, 0.00, 0.00, shadow_alpha),
		max_lines,
		alignment,
		bold,
		0,
		Color.TRANSPARENT,
		"%s_InkShadow" % node_name,
		28,
		Vector2(0.0, 1.0)
	)
	if treatment in [TEXT_CTA, TEXT_DOSSIER_TITLE, TEXT_SELECTED_TITLE]:
		_add_runtime_label_layer(
			rect,
			text,
			font_size,
			Color(0.74, 0.10, 0.07, 0.18),
			max_lines,
			alignment,
			bold,
			0,
			Color.TRANSPARENT,
			"%s_RedMisprint" % node_name,
			29,
			Vector2(-1.0, 1.0)
		)
		_add_runtime_label_layer(
			rect,
			text,
			font_size,
			Color(0.02, 0.48, 0.52, 0.14),
			max_lines,
			alignment,
			bold,
			0,
			Color.TRANSPARENT,
			"%s_CyanMisprint" % node_name,
			29,
			Vector2(1.0, -1.0)
		)

func _text_treatment_for(asset_id: String, rect_id: String, max_lines: int, bold: bool) -> String:
	if asset_id == ASSET_CTA_DEFAULT:
		return TEXT_CTA
	if asset_id == ASSET_BOTTOM_TICKER:
		return TEXT_TICKER
	if asset_id == ASSET_RIGHT_DOSSIER and rect_id == "region_title":
		return TEXT_DOSSIER_TITLE
	if asset_id == ASSET_RIGHT_DOSSIER and rect_id == "detail_header":
		return TEXT_SECTION
	if asset_id == ASSET_RIGHT_DOSSIER and rect_id == "detail_footer_status":
		return TEXT_FOOTER
	if asset_id == ASSET_LEFT_INDEX and rect_id == "slot_1_title":
		return TEXT_SELECTED_TITLE
	if asset_id == ASSET_LEFT_INDEX and rect_id.ends_with("_title"):
		return TEXT_QUIET_TITLE
	if asset_id == ASSET_LEFT_INDEX and rect_id.ends_with("_meta"):
		return TEXT_META
	if bold and max_lines <= 1:
		return TEXT_SELECTED_TITLE
	return TEXT_BODY

func _add_text_backing(rect: Rect2, treatment: String, color: Color, node_name: String) -> void:
	if treatment == TEXT_SECTION:
		_add_rule_rect(
			Rect2(rect.position + Vector2(0.0, rect.size.y - 5.0), Vector2(minf(rect.size.x, 210.0), 2.0)),
			Color(color.r, color.g, color.b, 0.32),
			node_name,
			27
		)
	elif treatment == TEXT_DOSSIER_TITLE:
		_add_rule_rect(
			Rect2(rect.position + Vector2(0.0, rect.size.y - 3.0), Vector2(minf(rect.size.x, 240.0), 2.0)),
			Color(0.10, 0.14, 0.13, 0.18),
			node_name,
			27
		)
	elif treatment == TEXT_SELECTED_TITLE:
		_add_rule_rect(
			Rect2(rect.position + Vector2(0.0, rect.size.y - 3.0), Vector2(minf(rect.size.x, 190.0), 2.0)),
			Color(0.76, 0.13, 0.08, 0.22),
			node_name,
			27
		)
	elif treatment == TEXT_CTA:
		_add_rule_rect(
			Rect2(rect.position + Vector2(16.0, 6.0), Vector2(maxf(rect.size.x - 32.0, 0.0), 2.0)),
			Color(0.72, 0.10, 0.06, 0.20),
			"%s_Top" % node_name,
			27
		)
		_add_rule_rect(
			Rect2(rect.position + Vector2(16.0, rect.size.y - 8.0), Vector2(maxf(rect.size.x - 32.0, 0.0), 2.0)),
			Color(0.02, 0.46, 0.50, 0.16),
			"%s_Bottom" % node_name,
			27
		)

func _add_rule_rect(rect: Rect2, color: Color, node_name: String, z_index: int) -> ColorRect:
	var rule := ColorRect.new()
	rule.name = node_name
	rule.position = rect.position
	rule.size = rect.size
	rule.color = color
	rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rule.z_index = z_index
	_world_root.add_child(rule)
	return rule

func _add_corner_brackets(rect: Rect2, color: Color, node_name: String, z_index: int) -> void:
	var corner := 34.0
	var thickness := 3.0
	_add_rule_rect(Rect2(rect.position, Vector2(corner, thickness)), color, "%sTopLeftH" % node_name, z_index)
	_add_rule_rect(Rect2(rect.position, Vector2(thickness, corner)), color, "%sTopLeftV" % node_name, z_index)
	_add_rule_rect(Rect2(rect.position + Vector2(rect.size.x - corner, 0.0), Vector2(corner, thickness)), color, "%sTopRightH" % node_name, z_index)
	_add_rule_rect(Rect2(rect.position + Vector2(rect.size.x - thickness, 0.0), Vector2(thickness, corner)), color, "%sTopRightV" % node_name, z_index)
	_add_rule_rect(Rect2(rect.position + Vector2(0.0, rect.size.y - thickness), Vector2(corner, thickness)), color, "%sBottomLeftH" % node_name, z_index)
	_add_rule_rect(Rect2(rect.position + Vector2(0.0, rect.size.y - corner), Vector2(thickness, corner)), color, "%sBottomLeftV" % node_name, z_index)
	_add_rule_rect(Rect2(rect.position + Vector2(rect.size.x - corner, rect.size.y - thickness), Vector2(corner, thickness)), color, "%sBottomRightH" % node_name, z_index)
	_add_rule_rect(Rect2(rect.position + Vector2(rect.size.x - thickness, rect.size.y - corner), Vector2(thickness, corner)), color, "%sBottomRightV" % node_name, z_index)

func _add_debug_zones() -> void:
	for asset in _manifest.get("assets", []):
		if typeof(asset) != TYPE_DICTIONARY:
			continue
		var asset_id := str(asset.get("id", ""))
		if asset_id.is_empty():
			continue
		var runtime_rect := _asset_runtime_rect(asset_id)
		if runtime_rect.size.x <= 0.0 or runtime_rect.size.y <= 0.0:
			continue
		for safe_zone in asset.get("dynamic_text_rects", []):
			if typeof(safe_zone) == TYPE_DICTIONARY:
				var rect := _rect_from_array(safe_zone.get("rect", []))
				_add_debug_panel(Rect2(runtime_rect.position + rect.position, rect.size), Color(0.15, 0.95, 0.45, 0.80), "SafeTextZone")
		for forbidden in asset.get("forbidden_zones", []):
			if typeof(forbidden) == TYPE_DICTIONARY:
				var rect := _rect_from_array(forbidden.get("rect", []))
				_add_debug_panel(Rect2(runtime_rect.position + rect.position, rect.size), Color(1.0, 0.10, 0.08, 0.75), "ForbiddenZone")
		if asset.has("hit_rect"):
			var hit_rect := _rect_from_array(asset.get("hit_rect", []))
			_add_debug_panel(Rect2(runtime_rect.position + hit_rect.position, hit_rect.size), Color(1.0, 0.88, 0.14, 0.70), "HitRect")
		var hit_rects = asset.get("hit_rects", {})
		if typeof(hit_rects) == TYPE_DICTIONARY:
			for key in hit_rects.keys():
				var hit := _rect_from_array(hit_rects[key])
				_add_debug_panel(Rect2(runtime_rect.position + hit.position, hit.size), Color(1.0, 0.88, 0.14, 0.70), "HitRect_%s" % str(key))
	_add_a80_debug_zones()

func _add_a80_debug_zones() -> void:
	var dossier_rect := _asset_runtime_rect(ASSET_RIGHT_DOSSIER)
	var origin := dossier_rect.position
	_add_debug_panel(Rect2(origin + Vector2(82.0, 306.0), Vector2(312.0, 44.0)), Color(1.0, 0.88, 0.14, 0.90), "A80TaskIntelHitRect")
	_add_debug_panel(Rect2(origin + Vector2(52.0, 352.0), Vector2(384.0, 16.0)), Color(1.0, 0.10, 0.08, 0.86), "A80TaskBodyAirGap")
	_add_debug_panel(Rect2(origin + Vector2(52.0, 372.0), Vector2(384.0, 214.0)), Color(0.15, 0.95, 0.45, 0.78), "A80RegionProseSafeArea")

func _add_debug_panel(rect: Rect2, color: Color, node_name: String) -> void:
	var panel := Panel.new()
	panel.name = node_name
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.z_index = 120
	var style := StyleBoxFlat.new()
	style.bg_color = Color(color.r, color.g, color.b, 0.08)
	style.border_color = color
	style.set_border_width_all(2)
	panel.add_theme_stylebox_override("panel", style)
	_world_root.add_child(panel)

func _asset_runtime_rect(asset_id: String) -> Rect2:
	return WorldMapManifest.runtime_rect(asset_id, _manifest)

func _global_text_rect(asset_id: String, rect_id: String) -> Rect2:
	var asset := WorldMapManifest.get_asset(asset_id, _manifest)
	var runtime_rect := _asset_runtime_rect(asset_id)
	for item in asset.get("dynamic_text_rects", []):
		if typeof(item) == TYPE_DICTIONARY and str(item.get("id", "")) == rect_id:
			var local_rect := _rect_from_array(item.get("rect", []))
			return Rect2(runtime_rect.position + local_rect.position, local_rect.size)
	push_warning("World map v6g preview missing text rect: %s::%s" % [asset_id, rect_id])
	return Rect2(runtime_rect.position, Vector2(120.0, 32.0))

func _anchor_to_screen(anchors: Dictionary, map_rect: Rect2, anchor_id: String) -> Vector2:
	var values: Array = anchors.get(anchor_id, [map_rect.size.x * 0.5, map_rect.size.y * 0.5])
	if values.size() != 2:
		return map_rect.get_center()
	return map_rect.position + Vector2(float(values[0]), float(values[1]))

func _rect_from_array(values: Array) -> Rect2:
	if values.size() != 4:
		return Rect2()
	return Rect2(float(values[0]), float(values[1]), float(values[2]), float(values[3]))

func _make_button_transparent(button: Button) -> void:
	var transparent := StyleBoxFlat.new()
	transparent.bg_color = Color.TRANSPARENT
	transparent.border_color = Color.TRANSPARENT
	transparent.set_border_width_all(0)
	button.add_theme_stylebox_override("normal", transparent)
	button.add_theme_stylebox_override("hover", transparent.duplicate())
	button.add_theme_stylebox_override("pressed", transparent.duplicate())
	button.add_theme_stylebox_override("disabled", transparent.duplicate())
	button.add_theme_stylebox_override("focus", transparent.duplicate())
