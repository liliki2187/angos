extends MarginContainer
class_name WeeklyRunExplorePhase

signal filter_toggled(tag)
signal region_selected(region_id)
signal node_selected(node_id)
signal staff_toggled(staff_id)
signal execute_requested

const ActionItemScene = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunActionItem.tscn")
const InfoCardScene = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunInfoCard.tscn")
const ScrollableText = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunScrollableText.gd")
const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

@onready var region_panel: PanelContainer = $RootHBox/LeftVBox/RegionPanel
@onready var btn_filter_sci: Button = $RootHBox/LeftVBox/RegionPanel/RegionVBox/FilterRow/BtnFilterSci
@onready var btn_filter_occult: Button = $RootHBox/LeftVBox/RegionPanel/RegionVBox/FilterRow/BtnFilterOccult
@onready var btn_filter_pop: Button = $RootHBox/LeftVBox/RegionPanel/RegionVBox/FilterRow/BtnFilterPop
@onready var region_list: VBoxContainer = $RootHBox/LeftVBox/RegionPanel/RegionVBox/RegionScroll/RegionList
@onready var node_panel: PanelContainer = $RootHBox/LeftVBox/NodePanel
@onready var region_hint_label: Label = $RootHBox/LeftVBox/NodePanel/NodeVBox/RegionHintLabel
@onready var node_list: VBoxContainer = $RootHBox/LeftVBox/NodePanel/NodeVBox/NodeScroll/NodeList
@onready var staff_panel: PanelContainer = $RootHBox/MiddleVBox/StaffPanel
@onready var selected_staff_label: Label = $RootHBox/MiddleVBox/StaffPanel/StaffVBox/SelectedStaffLabel
@onready var staff_grid: GridContainer = $RootHBox/MiddleVBox/StaffPanel/StaffVBox/StaffScroll/StaffGrid
@onready var materials_panel: PanelContainer = $RootHBox/MiddleVBox/MaterialsPanel
@onready var material_list: VBoxContainer = $RootHBox/MiddleVBox/MaterialsPanel/MaterialsVBox/MaterialScroll/MaterialList
@onready var mission_panel: PanelContainer = $RootHBox/RightVBox/MissionPanel
@onready var mission_summary: ScrollableText = $RootHBox/RightVBox/MissionPanel/MissionVBox/MissionScroll
@onready var probability_label: Label = $RootHBox/RightVBox/MissionPanel/MissionVBox/ProbabilityLabel
@onready var dice_text: RichTextLabel = $RootHBox/RightVBox/MissionPanel/MissionVBox/DiceText
@onready var result_label: Label = $RootHBox/RightVBox/MissionPanel/MissionVBox/ResultLabel
@onready var execute_btn: Button = $RootHBox/RightVBox/MissionPanel/MissionVBox/ExecuteBtn
@onready var log_panel: PanelContainer = $RootHBox/RightVBox/LogPanel
@onready var log_list: VBoxContainer = $RootHBox/RightVBox/LogPanel/LogVBox/LogScroll/LogList

func _ready() -> void:
	add_theme_constant_override("margin_left", 4)
	add_theme_constant_override("margin_top", 4)
	add_theme_constant_override("margin_right", 4)
	add_theme_constant_override("margin_bottom", 4)
	for panel in [region_panel, node_panel, staff_panel, materials_panel, mission_panel, log_panel]:
		UiStyle.apply_panel_style(panel)
	for button in [btn_filter_sci, btn_filter_occult, btn_filter_pop, execute_btn]:
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	execute_btn.pressed.connect(func() -> void:
		execute_requested.emit()
	)
	btn_filter_sci.pressed.connect(func() -> void:
		filter_toggled.emit("sci")
	)
	btn_filter_occult.pressed.connect(func() -> void:
		filter_toggled.emit("occult")
	)
	btn_filter_pop.pressed.connect(func() -> void:
		filter_toggled.emit("pop")
	)

func render(payload: Dictionary) -> void:
	var started_at := _log_flow_start("render", "regions=%d nodes=%d staff=%d materials=%d logs=%d" % [
		(payload.get("regions", []) as Array).size(),
		(payload.get("nodes", []) as Array).size(),
		(payload.get("staff", []) as Array).size(),
		(payload.get("materials", []) as Array).size(),
		(payload.get("logs", []) as Array).size(),
	])
	selected_staff_label.text = str(payload.get("selected_staff_text", "已选择：0 / 3"))
	region_hint_label.text = str(payload.get("region_hint", "请选择区域"))
	mission_summary.set_text_content(str(payload.get("mission_summary", "")))
	probability_label.text = str(payload.get("probability_text", "理论结果：等待选点"))
	dice_text.text = str(payload.get("dice_text", ""))
	result_label.text = str(payload.get("result_text", "等待执行"))
	result_label.add_theme_color_override("font_color", payload.get("result_color", Color(0.88, 0.76, 0.36, 1.0)))
	execute_btn.disabled = not bool(payload.get("execute_enabled", false))
	UiStyle.apply_button_style(execute_btn, true, bool(payload.get("execute_enabled", false)))
	_style_filter_button(btn_filter_sci, bool(payload.get("filters", {}).get("sci", true)))
	_style_filter_button(btn_filter_occult, bool(payload.get("filters", {}).get("occult", true)))
	_style_filter_button(btn_filter_pop, bool(payload.get("filters", {}).get("pop", true)))
	_rebuild_action_items(region_list, payload.get("regions", []), "region")
	_rebuild_action_items(node_list, payload.get("nodes", []), "node")
	_rebuild_action_items(staff_grid, payload.get("staff", []), "staff")
	_rebuild_info_cards(material_list, payload.get("materials", []))
	_rebuild_info_cards(log_list, payload.get("logs", []))
	_log_flow_end("render", started_at)

func _style_filter_button(button: Button, selected: bool) -> void:
	button.custom_minimum_size = Vector2(0.0, 34.0)
	UiStyle.apply_button_style(button, selected, true)

func _rebuild_action_items(container: Control, items: Array, item_kind: String) -> void:
	var started_at := _log_flow_start("_rebuild_action_items", "container=%s kind=%s items=%d existing=%d" % [container.name, item_kind, items.size(), container.get_child_count()])
	for child in container.get_children():
		container.remove_child(child)
		child.queue_free()
	for item in items:
		var action_item := ActionItemScene.instantiate()
		container.add_child(action_item)
		action_item.bind(item)
		action_item.item_pressed.connect(func(item_id) -> void:
			match item_kind:
				"region":
					region_selected.emit(str(item_id))
				"node":
					node_selected.emit(str(item_id))
				"staff":
					staff_toggled.emit(str(item_id))
		)
	_log_flow_end("_rebuild_action_items", started_at, "container=%s kind=%s rebuilt=%d" % [container.name, item_kind, items.size()])

func _rebuild_info_cards(container: VBoxContainer, items: Array) -> void:
	var started_at := _log_flow_start("_rebuild_info_cards", "container=%s items=%d existing=%d" % [container.name, items.size(), container.get_child_count()])
	for child in container.get_children():
		container.remove_child(child)
		child.queue_free()
	for item in items:
		var card := InfoCardScene.instantiate()
		container.add_child(card)
		card.bind(str(item.get("title", "")), str(item.get("body", "")), item.get("accent", Color(0.84, 0.68, 0.37, 1.0)))
	_log_flow_end("_rebuild_info_cards", started_at, "container=%s rebuilt=%d" % [container.name, items.size()])

func _log_flow_start(flow_name: String, details: String = "") -> int:
	var started_at := Time.get_ticks_usec()
	Globals.log("WeeklyRunExplorePhase", "%s START %s" % [flow_name, details])
	return started_at

func _log_flow_end(flow_name: String, started_at: int, details: String = "") -> void:
	var elapsed_ms := float(Time.get_ticks_usec() - started_at) / 1000.0
	Globals.log("WeeklyRunExplorePhase", "%s END %.2fms %s" % [flow_name, elapsed_ms, details])
