extends MarginContainer
class_name WeeklyRunEditorialPhase

signal article_selected(article_id)
signal slot_selected(slot_id)
signal clear_layout_requested
signal settle_requested

const ActionItemScene = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunActionItem.tscn")
const ScrollableText = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunScrollableText.gd")
const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

@onready var header_panel: PanelContainer = $RootVBox/EditorialHeader
@onready var editorial_subtitle: Label = $RootVBox/EditorialHeader/EditorialHeaderVBox/EditorialSubtitle
@onready var library_panel: PanelContainer = $RootVBox/EditorialColumns/LibraryPanel
@onready var article_list: VBoxContainer = $RootVBox/EditorialColumns/LibraryPanel/LibraryVBox/ArticleScroll/ArticleList
@onready var layout_panel: PanelContainer = $RootVBox/EditorialColumns/LayoutPanel
@onready var slot_list: VBoxContainer = $RootVBox/EditorialColumns/LayoutPanel/LayoutVBox/SlotScroll/SlotList
@onready var clear_layout_btn: Button = $RootVBox/EditorialColumns/LayoutPanel/LayoutVBox/LayoutActions/ClearLayoutBtn
@onready var settle_btn: Button = $RootVBox/EditorialColumns/LayoutPanel/LayoutVBox/LayoutActions/SettleBtn
@onready var stats_panel: PanelContainer = $RootVBox/EditorialColumns/StatsPanel
@onready var live_stats: ScrollableText = $RootVBox/EditorialColumns/StatsPanel/StatsVBox/StatsScroll

func _ready() -> void:
	add_theme_constant_override("margin_left", 4)
	add_theme_constant_override("margin_top", 4)
	add_theme_constant_override("margin_right", 4)
	add_theme_constant_override("margin_bottom", 4)
	for panel in [header_panel, library_panel, layout_panel, stats_panel]:
		UiStyle.apply_panel_style(panel)
	UiStyle.apply_button_style(clear_layout_btn, false, true)
	UiStyle.apply_button_style(settle_btn, true, true)
	clear_layout_btn.pressed.connect(func() -> void:
		clear_layout_requested.emit()
	)
	settle_btn.pressed.connect(func() -> void:
		settle_requested.emit()
	)

func render(payload: Dictionary) -> void:
	var started_at := _log_flow_start("render", "articles=%d slots=%d" % [
		(payload.get("articles", []) as Array).size(),
		(payload.get("slots", []) as Array).size(),
	])
	editorial_subtitle.text = str(payload.get("subtitle", ""))
	live_stats.set_text_content(str(payload.get("stats_text", "")))
	_rebuild_action_items(article_list, payload.get("articles", []), "article")
	_rebuild_action_items(slot_list, payload.get("slots", []), "slot")
	_log_flow_end("render", started_at)

func _rebuild_action_items(container: VBoxContainer, items: Array, item_kind: String) -> void:
	var started_at := _log_flow_start("_rebuild_action_items", "container=%s kind=%s items=%d existing=%d" % [container.name, item_kind, items.size(), container.get_child_count()])
	for child in container.get_children():
		container.remove_child(child)
		child.queue_free()
	for item in items:
		var action_item := ActionItemScene.instantiate()
		container.add_child(action_item)
		action_item.bind(item)
		action_item.item_pressed.connect(func(item_id) -> void:
			if item_kind == "article":
				article_selected.emit(int(item_id))
			else:
				slot_selected.emit(str(item_id))
		)
	_log_flow_end("_rebuild_action_items", started_at, "container=%s kind=%s rebuilt=%d" % [container.name, item_kind, items.size()])

func _log_flow_start(flow_name: String, details: String = "") -> int:
	var started_at := Time.get_ticks_usec()
	Globals.log("WeeklyRunEditorialPhase", "%s START %s" % [flow_name, details])
	return started_at

func _log_flow_end(flow_name: String, started_at: int, details: String = "") -> void:
	var elapsed_ms := float(Time.get_ticks_usec() - started_at) / 1000.0
	Globals.log("WeeklyRunEditorialPhase", "%s END %.2fms %s" % [flow_name, elapsed_ms, details])
