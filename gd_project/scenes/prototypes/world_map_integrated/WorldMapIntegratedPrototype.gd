extends Control

const BackdropScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedBackdrop.gd")
const RegionCardScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedRegionCard.gd")
const BeaconScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedBeacon.gd")
const DossierScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedDossier.gd")
const ScheduleGateScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedScheduleGate.gd")
const ReviewOverlayScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedReviewOverlay.gd")
const MapDecorScript := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedMapDecor.gd")

const REFERENCE_SIZE := Vector2(1920, 1080)
const PAPER := Color("eee8d7")
const INK := Color("17252b")
const MUTED := Color("5b696d")
const COBALT := Color("356783")
const RUST := Color("9a4a36")

const REGION_DATA := {
	"north_america": {
		"region_id": "north_america", "display_name": "北美禁区带", "status_text": "红线升温",
		"secondary_text": "红线升温\n截稿倒计时 7 天", "thumbnail_variant": "north_america", "locked": false, "warning": true,
	},
	"east_asia": {
		"region_id": "east_asia", "display_name": "东亚神秘地带", "status_text": "封锁",
		"secondary_text": "声望≥55 或\n「罗斯威尔残页」", "thumbnail_variant": "east_asia", "locked": true, "warning": false,
	},
	"pacific": {
		"region_id": "pacific", "display_name": "太平洋失航带", "status_text": "封锁",
		"secondary_text": "北美追踪第2环 或\n线人许可", "thumbnail_variant": "pacific", "locked": true, "warning": false,
	},
}

var selected_region_id := "north_america"
var blocked_region_id := ""
var _font: Font
var _backdrop: Control
var _region_cards := {}
var _beacons := {}
var _dossier: Control
var _review_overlay: Control
var _schedule_gate: Control
var _map_decor: Control
var _index_feedback_label: Label
var _built := false


func _ready() -> void:
	if _built:
		return
	_built = true
	custom_minimum_size = REFERENCE_SIZE
	mouse_filter = Control.MOUSE_FILTER_PASS
	_setup_font()
	_build_interface()
	_sync_selection("初始状态")


func set_review_overlay(value: bool) -> void:
	if is_instance_valid(_review_overlay):
		_review_overlay.visible = value


func set_mission_expanded(value: bool) -> void:
	if is_instance_valid(_dossier):
		_dossier.set_mission_expanded(value)


func activate_region_for_test(region_id: String, source: String = "test") -> void:
	_activate_region(region_id, source)


func activate_primary_for_test() -> void:
	if is_instance_valid(_dossier):
		_dossier.activate_primary_for_test()


func get_state_snapshot() -> Dictionary:
	var selected_cards: Array[String] = []
	var selected_beacons: Array[String] = []
	var interactive_button_names: Array[String] = []
	for region_id in _region_cards:
		if bool(_region_cards[region_id].is_selected):
			selected_cards.append(str(region_id))
	for region_id in _beacons:
		if bool(_beacons[region_id].is_selected):
			selected_beacons.append(str(region_id))
	selected_cards.sort()
	selected_beacons.sort()
	for button in find_children("*", "Button", true, false):
		interactive_button_names.append(str(button.name))
	interactive_button_names.sort()
	return {
		"selected_region_id": selected_region_id,
		"blocked_region_id": blocked_region_id,
		"selected_cards": selected_cards,
		"selected_beacons": selected_beacons,
		"dossier": _dossier.get_state_snapshot() if is_instance_valid(_dossier) else {},
		"button_count": find_children("*", "Button", true, false).size(),
		"interactive_button_names": interactive_button_names,
		"index_feedback": _index_feedback_label.text if is_instance_valid(_index_feedback_label) else "",
		"schedule": _schedule_gate.get_state_snapshot() if is_instance_valid(_schedule_gate) else {},
	}


func get_hit_rect_snapshot() -> Dictionary:
	return {
		"north_card": [52, 226, 340, 170], "east_card": [52, 408, 340, 170], "pacific_card": [52, 590, 340, 170],
		"north_beacon": [662, 318, 212, 76], "east_beacon": [1000, 336, 216, 76], "pacific_beacon": [1054, 666, 244, 84],
		"map_safe_rect": [432, 154, 960, 902], "mission_disclosure": [1443, 596, 414, 56],
		"primary_cta": [1443, 956, 414, 76], "schedule_gate": [36, 810, 372, 246],
		"dossier_rect": [1416, 24, 468, 1032],
		"advance_day_disabled": [52, 882, 340, 94],
	}


func get_region_image_contract_snapshot() -> Dictionary:
	var card_snapshots := {}
	for region_id in _region_cards:
		card_snapshots[region_id] = _region_cards[region_id].get_image_contract_snapshot()
	return {
		"cards": card_snapshots,
		"dossier": _dossier.get_state_snapshot().get("lead_image", {}) if is_instance_valid(_dossier) else {},
	}


func get_visual_asset_contract_snapshot() -> Dictionary:
	var beacon_assets := {}
	for region_id in _beacons:
		beacon_assets[region_id] = _beacons[region_id].get_asset_contract_snapshot()
	return {
		"classification": "runtime_state_preview",
		"map_board": _backdrop.get_asset_contract() if is_instance_valid(_backdrop) else {},
		"region_images": get_region_image_contract_snapshot(),
		"map_decor": _map_decor.get_asset_contract_snapshot() if is_instance_valid(_map_decor) else {},
		"beacons": beacon_assets,
	}


func _setup_font() -> void:
	if DisplayServer.get_name() == "headless":
		_font = ThemeDB.fallback_font
		return
	var system_font := SystemFont.new()
	system_font.font_names = PackedStringArray(["Microsoft YaHei UI", "Microsoft YaHei", "Source Han Sans SC", "Noto Sans CJK SC", "Noto Sans SC", "DengXian", "SimHei"])
	_font = system_font


func _build_interface() -> void:
	_backdrop = BackdropScript.new()
	_backdrop.name = "MapField"
	_backdrop.position = Vector2.ZERO
	_backdrop.size = REFERENCE_SIZE
	_backdrop.z_index = 0
	add_child(_backdrop)
	_build_masthead()
	_build_region_index()
	_build_beacons()
	_build_dossier()
	_build_time_strip()
	_build_map_copy()
	_build_map_decor()
	_review_overlay = ReviewOverlayScript.new()
	_review_overlay.name = "ReviewOverlay"
	_review_overlay.position = Vector2.ZERO
	_review_overlay.size = REFERENCE_SIZE
	_review_overlay.z_index = 100
	add_child(_review_overlay)
	_review_overlay.configure(_font)
	_review_overlay.visible = false


func _build_masthead() -> void:
	var mark := _make_label("ChannelMark", Rect2(40, 24, 180, 24), 13, Color("bfc7bb"), HORIZONTAL_ALIGNMENT_LEFT, 3)
	mark.text = "WMW / NIGHT DESK"
	var title := _make_label("Masthead", Rect2(40, 46, 420, 70), 43, PAPER, HORIZONTAL_ALIGNMENT_LEFT, 3)
	title.text = "世界未解之谜周刊"
	var issue := _make_label("IssueMeta", Rect2(480, 50, 440, 48), 18, Color("c4cec2"), HORIZONTAL_ALIGNMENT_LEFT, 3)
	issue.text = "ISSUE 001  ·  WEEK 01"
	var tone := _make_label("BrandTone", Rect2(980, 42, 380, 44), 16, Color("aebbb5"), HORIZONTAL_ALIGNMENT_RIGHT, 3)
	tone.text = "今晚世界依旧勉强正常"
	var rule := ColorRect.new()
	rule.position = Vector2(40, 128)
	rule.size = Vector2(1352, 2)
	rule.color = Color(0.78, 0.81, 0.72, 0.18)
	rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rule.z_index = 2
	add_child(rule)


func _build_region_index() -> void:
	var shell := Panel.new()
	shell.name = "RegionIndex"
	shell.position = Vector2(36, 154)
	shell.size = Vector2(372, 640)
	shell.z_index = 5
	var style := StyleBoxFlat.new()
	style.bg_color = Color("102b35")
	style.border_color = Color(0.79, 0.80, 0.70, 0.58)
	style.border_width_left = 1
	style.border_width_top = 1
	style.border_width_right = 1
	style.border_width_bottom = 1
	style.shadow_color = Color(0, 0, 0, 0.34)
	style.shadow_size = 10
	shell.add_theme_stylebox_override("panel", style)
	add_child(shell)
	var kicker := _make_label_in(shell, "IndexKicker", Rect2(16, 12, 240, 20), 12, Color("aebbb5"))
	kicker.text = "REGION INDEX / 异常投递范围"
	var heading := _make_label_in(shell, "IndexTitle", Rect2(16, 32, 220, 38), 25, PAPER)
	heading.text = "地区索引"
	var count := _make_label_in(shell, "IndexCount", Rect2(250, 34, 106, 32), 13, Color("aebbb5"))
	count.text = "1 / 3 可进入"
	count.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	var layout := [["north_america", Vector2(16, 72), 0.0], ["east_asia", Vector2(16, 254), 6.0], ["pacific", Vector2(16, 436), 2.0]]
	for item in layout:
		var region_id: String = item[0]
		var card := RegionCardScript.new()
		card.name = "RegionCard_%s" % region_id
		card.position = item[1]
		card.size = Vector2(340, 170)
		card.configure(REGION_DATA[region_id], _font, float(item[2]))
		card.region_activated.connect(func(id: String) -> void: _activate_region(id, "地区卡"))
		card.locked_region_activated.connect(func(id: String) -> void: _activate_region(id, "地区卡"))
		shell.add_child(card)
		_region_cards[region_id] = card
	_index_feedback_label = _make_label_in(shell, "IndexFeedback", Rect2(16, 610, 340, 22), 12, Color("aebbb5"))
	_index_feedback_label.text = "只选择地区；任务与派遣在下一层。"
	_index_feedback_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART


func _build_beacons() -> void:
	var layout := [
		["north_america", Vector2(662, 318), Vector2(212, 76), Vector2(28, 34), Rect2(62, 14, 138, 40)],
		["east_asia", Vector2(1000, 336), Vector2(216, 76), Vector2(188, 36), Rect2(10, 14, 146, 40)],
		["pacific", Vector2(1054, 666), Vector2(244, 84), Vector2(216, 44), Rect2(10, 10, 174, 40)],
	]
	for item in layout:
		var region_id: String = item[0]
		var beacon := BeaconScript.new()
		beacon.name = "MapBeacon_%s" % region_id
		beacon.position = item[1]
		beacon.size = item[2]
		beacon.configure(REGION_DATA[region_id], _font, item[3], item[4])
		beacon.z_index = 4
		beacon.region_activated.connect(func(id: String) -> void: _activate_region(id, "地图节点"))
		beacon.locked_region_activated.connect(func(id: String) -> void: _activate_region(id, "地图节点"))
		add_child(beacon)
		_beacons[region_id] = beacon


func _build_dossier() -> void:
	_dossier = DossierScript.new()
	_dossier.name = "SelectedRegionDossier"
	_dossier.position = Vector2(1416, 24)
	_dossier.size = Vector2(468, 1032)
	_dossier.z_index = 7
	_dossier.configure(_font)
	_dossier.mission_intel_toggled.connect(_on_mission_toggled)
	_dossier.enter_region_requested.connect(_on_enter_region_requested)
	add_child(_dossier)


func _build_time_strip() -> void:
	_schedule_gate = ScheduleGateScript.new()
	_schedule_gate.name = "ScheduleGate"
	_schedule_gate.position = Vector2(36, 810)
	_schedule_gate.size = Vector2(372, 246)
	_schedule_gate.z_index = 6
	_schedule_gate.configure(_font)
	add_child(_schedule_gate)


func _build_map_copy() -> void:
	var heading := _make_label("MapDeskLabel", Rect2(456, 160, 560, 36), 18, Color("c2cbbf"), HORIZONTAL_ALIGNMENT_LEFT, 2)
	heading.text = "世界异常分布 / EDITORIAL EVIDENCE MAP"
	var note := _make_label("MapLegalNote", Rect2(1040, 952, 330, 28), 12, Color("9faeaa"), HORIZONTAL_ALIGNMENT_RIGHT, 2)
	note.text = "地图仅供参考 · 现实恕不退款"


func _build_map_decor() -> void:
	_map_decor = MapDecorScript.new()
	_map_decor.name = "MapDecor"
	_map_decor.position = Vector2.ZERO
	_map_decor.size = REFERENCE_SIZE
	_map_decor.z_index = 3
	_map_decor.configure(_font)
	add_child(_map_decor)


func _activate_region(region_id: String, source: String) -> void:
	if not REGION_DATA.has(region_id):
		return
	var data: Dictionary = REGION_DATA[region_id]
	if bool(data.get("locked", false)):
		blocked_region_id = region_id
		_index_feedback_label.text = "%s仍锁定，条件见对应地区卡；选区未改变。" % str(data.get("display_name", "该地区"))
		_index_feedback_label.add_theme_color_override("font_color", RUST)
		_sync_selection(source)
		return
	selected_region_id = region_id
	blocked_region_id = ""
	_index_feedback_label.text = "已选择；任务与派遣在下一层。"
	_index_feedback_label.add_theme_color_override("font_color", Color("aebbb5"))
	_sync_selection(source)


func _sync_selection(_source: String) -> void:
	for region_id in _region_cards:
		var data: Dictionary = REGION_DATA[region_id]
		_region_cards[region_id].set_state(region_id == selected_region_id, bool(data.get("warning", false)), region_id == blocked_region_id)
	for region_id in _beacons:
		var data: Dictionary = REGION_DATA[region_id]
		_beacons[region_id].set_state(region_id == selected_region_id, bool(data.get("warning", false)), region_id == blocked_region_id)
	var selected_data: Dictionary = REGION_DATA[selected_region_id]
	_dossier.render_region({"region_id": selected_region_id, "display_name": selected_data.get("display_name", "北美禁区带"), "status_text": selected_data.get("status_text", "红线升温"), "headline": "洗衣店里出现了一片海", "summary": "断电两小时后，潮线仍在三扇滚筒窗之间保持水平。\n店外道路干燥，最近海岸线在一千公里外。", "mission_facts": "限时 1 · 线索 2 · 深链 1"})


func _on_mission_toggled(_expanded: bool) -> void:
	pass


func _on_enter_region_requested(_region_id: String) -> void:
	_index_feedback_label.text = "准备进入地区任务台（0 天）。"


func _make_label(node_name: String, rect: Rect2, font_size: int, color: Color, alignment: HorizontalAlignment, z: int) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.horizontal_alignment = alignment
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.z_index = z
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
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("font", _font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	parent.add_child(label)
	return label
