extends ScrollContainer
class_name WeeklyRunScrollableText

@onready var body: RichTextLabel = $Body

func _ready() -> void:
	if not resized.is_connected(_sync_width):
		resized.connect(_sync_width)
	call_deferred("_sync_width")

func set_text_content(value: String) -> void:
	body.text = value
	call_deferred("_sync_width")

func _sync_width() -> void:
	body.custom_minimum_size.x = maxf(0.0, size.x)
