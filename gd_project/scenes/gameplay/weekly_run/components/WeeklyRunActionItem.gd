extends Button
class_name WeeklyRunActionItem

signal item_pressed(item_id)

const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

var item_id
var visual_style := ""
var card_number := ""
var stamp_text := ""
var accent_color := Color(0.80, 0.14, 0.10, 1.0)
var use_world_imagegen_v5 := false
var use_region_task_artboard_v3 := false
var use_region_task_assetized := false
var use_region_task_v2 := false
var region_selected := false
var region_enabled := true

func _ready() -> void:
	alignment = HORIZONTAL_ALIGNMENT_LEFT
	autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	clip_text = true
	text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	if not pressed.is_connected(_on_pressed):
		pressed.connect(_on_pressed)

func bind(data: Dictionary) -> void:
	item_id = data.get("id", "")
	visual_style = str(data.get("visual_style", ""))
	use_world_imagegen_v5 = bool(data.get("world_imagegen_v5", false))
	use_region_task_artboard_v3 = bool(data.get("region_task_artboard_v3", false))
	use_region_task_assetized = bool(data.get("region_task_assetized", false))
	use_region_task_v2 = bool(data.get("region_task_v2", false))
	_configure_region_card_text(str(data.get("text", "")), bool(data.get("selected", false)), bool(data.get("enabled", true)))
	custom_minimum_size = Vector2(0.0, float(data.get("min_height", 72.0)))
	if use_region_task_artboard_v3:
		UiStyle.apply_region_task_artboard_v3_task_button(self, bool(data.get("selected", false)), bool(data.get("enabled", true)))
		queue_redraw()
		return
	if use_region_task_assetized and UiStyle.apply_region_task_assetized_task_card_button(
		self,
		_region_task_assetized_card_state(visual_style, bool(data.get("selected", false)), bool(data.get("enabled", true))),
		bool(data.get("enabled", true))
	):
		queue_redraw()
		return
	if use_region_task_v2 and UiStyle.apply_region_task_v2_action_item_style(
		self,
		visual_style,
		bool(data.get("selected", false)),
		bool(data.get("enabled", true))
	):
		queue_redraw()
		return
	if use_world_imagegen_v5 and UiStyle.apply_world_imagegen_v5_action_item_style(
		self,
		visual_style,
		bool(data.get("selected", false)),
		bool(data.get("enabled", true))
	):
		queue_redraw()
		return
	UiStyle.apply_action_item_style(
		self,
		visual_style,
		bool(data.get("selected", false)),
		bool(data.get("enabled", true))
	)
	queue_redraw()

func _region_task_assetized_card_state(style_name: String, selected: bool, enabled: bool) -> String:
	if not enabled:
		return "unavailable"
	if selected:
		return "selected"
	if style_name == "node_deadline":
		return "deadline"
	if style_name == "node_chain":
		return "assigned"
	return "normal"

func _on_pressed() -> void:
	item_pressed.emit(item_id)

func _configure_region_card_text(raw_text: String, selected: bool, enabled: bool) -> void:
	region_selected = selected
	region_enabled = enabled
	if not visual_style.begins_with("region_"):
		card_number = ""
		stamp_text = ""
		text = raw_text
		return

	var lines := raw_text.split("\n")
	var first_line := str(lines[0]) if lines.size() > 0 else raw_text
	var split_at := first_line.find(" ")
	if split_at > 0:
		card_number = first_line.substr(0, split_at).strip_edges()
		var title := first_line.substr(split_at + 1).strip_edges()
		var rest: Array[String] = []
		for index in range(1, lines.size()):
			rest.append(str(lines[index]))
		text = "%s\n%s" % [title, "\n".join(rest)]
	else:
		card_number = ""
		text = raw_text

	if visual_style == "region_file_cyan":
		accent_color = Color(0.08, 0.54, 0.61, 1.0)
	elif visual_style == "region_locked_file":
		accent_color = Color(0.42, 0.42, 0.36, 1.0)
	else:
		accent_color = Color(0.79, 0.14, 0.10, 1.0)

	stamp_text = "缺口未补" if not enabled else "已选题" if selected else "可进入"

func _draw() -> void:
	if not visual_style.begins_with("region_"):
		return
	var font := get_theme_default_font()
	if card_number != "":
		var number_color := Color(0.96, 0.92, 0.78, 0.96)
		if visual_style == "region_locked_file":
			number_color = Color(0.72, 0.72, 0.64, 0.82)
			if region_selected and not region_enabled:
				number_color = Color(0.96, 0.84, 0.50, 0.98)
		draw_string(font, Vector2(12, 36), card_number, HORIZONTAL_ALIGNMENT_LEFT, 32.0, 18, number_color)
