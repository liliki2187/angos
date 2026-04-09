extends MarginContainer
class_name WeeklyRunSummaryPhase

signal next_week_requested

const ScrollableText = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunScrollableText.gd")
const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

@onready var summary_panel: PanelContainer = $RootVBox/SummaryPanel
@onready var summary_text: ScrollableText = $RootVBox/SummaryPanel/SummaryVBox/SummaryScroll
@onready var hooks_panel: PanelContainer = $RootVBox/HooksPanel
@onready var hooks_text: RichTextLabel = $RootVBox/HooksPanel/HooksVBox/HooksText
@onready var next_week_btn: Button = $RootVBox/FooterHBox/NextWeekBtn

func _ready() -> void:
	add_theme_constant_override("margin_left", 4)
	add_theme_constant_override("margin_top", 4)
	add_theme_constant_override("margin_right", 4)
	add_theme_constant_override("margin_bottom", 4)
	for panel in [summary_panel, hooks_panel]:
		UiStyle.apply_panel_style(panel)
	UiStyle.apply_button_style(next_week_btn, true, true)
	next_week_btn.pressed.connect(func() -> void:
		next_week_requested.emit()
	)

func render(payload: Dictionary) -> void:
	summary_text.set_text_content(str(payload.get("summary_text", "")))
	hooks_text.text = str(payload.get("hooks_text", ""))
