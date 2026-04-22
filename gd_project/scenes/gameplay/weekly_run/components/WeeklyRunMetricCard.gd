extends PanelContainer
class_name WeeklyRunMetricCard

const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

@onready var title_label: Label = $VBox/Title
@onready var value_label: Label = $VBox/Value

func _ready() -> void:
	UiStyle.apply_panel_style(self, Color(0.09, 0.12, 0.18, 1.0), Color(0.23, 0.29, 0.35, 1.0), 10)

func bind(label: String, value: String) -> void:
	title_label.text = label
	value_label.text = value
