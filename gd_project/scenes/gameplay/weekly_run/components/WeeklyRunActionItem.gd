extends Button
class_name WeeklyRunActionItem

signal item_pressed(item_id)

const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

var item_id

func _ready() -> void:
	alignment = HORIZONTAL_ALIGNMENT_LEFT
	autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	if not pressed.is_connected(_on_pressed):
		pressed.connect(_on_pressed)

func bind(data: Dictionary) -> void:
	item_id = data.get("id", "")
	text = str(data.get("text", ""))
	custom_minimum_size = Vector2(0.0, float(data.get("min_height", 72.0)))
	UiStyle.apply_button_style(self, bool(data.get("selected", false)), bool(data.get("enabled", true)))

func _on_pressed() -> void:
	item_pressed.emit(item_id)
