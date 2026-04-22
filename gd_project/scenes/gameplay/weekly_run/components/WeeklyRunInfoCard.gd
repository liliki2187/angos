extends PanelContainer
class_name WeeklyRunInfoCard

const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

@onready var title_label: Label = $VBox/Title
@onready var body_label: RichTextLabel = $VBox/Body

func _ready() -> void:
	UiStyle.apply_panel_style(self, Color(0.06, 0.09, 0.13, 1.0), Color(0.21, 0.27, 0.33, 1.0), 10)

func bind(title: String, body: String, accent_color: Color = Color(0.84, 0.68, 0.37, 1.0)) -> void:
	title_label.visible = title != ""
	title_label.text = title
	title_label.add_theme_color_override("font_color", accent_color)
	body_label.text = body
