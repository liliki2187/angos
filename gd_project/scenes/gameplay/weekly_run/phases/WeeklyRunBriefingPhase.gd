extends MarginContainer
class_name WeeklyRunBriefingPhase

const InfoCardScene = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunInfoCard.tscn")
const ScrollableText = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunScrollableText.gd")
const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

@onready var briefing_panel: PanelContainer = $RootVBox/ContentSplit/BriefingPanel
@onready var briefing_text: ScrollableText = $RootVBox/ContentSplit/BriefingPanel/BriefingVBox/BriefingScroll
@onready var tasks_panel: PanelContainer = $RootVBox/ContentSplit/SideVBox/TasksPanel
@onready var task_list: VBoxContainer = $RootVBox/ContentSplit/SideVBox/TasksPanel/TasksVBox/TaskScroll/TaskList
@onready var hooks_panel: PanelContainer = $RootVBox/ContentSplit/SideVBox/HooksPanel
@onready var hook_list: VBoxContainer = $RootVBox/ContentSplit/SideVBox/HooksPanel/HooksVBox/HookScroll/HookList
@onready var opportunity_panel: PanelContainer = $RootVBox/OpportunityPanel
@onready var opportunity_list: VBoxContainer = $RootVBox/OpportunityPanel/OpportunityVBox/OpportunityScroll/OpportunityList

func _ready() -> void:
	add_theme_constant_override("margin_left", 4)
	add_theme_constant_override("margin_top", 4)
	add_theme_constant_override("margin_right", 4)
	add_theme_constant_override("margin_bottom", 4)
	for panel in [briefing_panel, tasks_panel, hooks_panel, opportunity_panel]:
		UiStyle.apply_panel_style(panel)

func render(payload: Dictionary) -> void:
	briefing_text.set_text_content(str(payload.get("briefing_text", "")))
	_rebuild_info_cards(task_list, payload.get("tasks", []))
	_rebuild_info_cards(hook_list, payload.get("hooks", []))
	_rebuild_info_cards(opportunity_list, payload.get("opportunities", []))

func _rebuild_info_cards(container: VBoxContainer, items: Array) -> void:
	for child in container.get_children():
		container.remove_child(child)
		child.queue_free()
	for item in items:
		var card := InfoCardScene.instantiate()
		container.add_child(card)
		card.bind(str(item.get("title", "")), str(item.get("body", "")))
