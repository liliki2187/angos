extends Button

signal drag_started(source: Dictionary)
signal drag_finished(source: Dictionary, successful: bool)
signal drag_hovered(target_kind: String, target_slot_id: String)
signal drag_exited(target_kind: String, target_slot_id: String)
signal article_dropped(source: Dictionary, target_kind: String, target_slot_id: String)

var drag_enabled := false
var drag_source_kind := ""
var drag_article_id := -1
var drag_source_slot_id := ""
var drag_preview_text := ""

var drop_enabled := false
var drop_target_kind := ""
var drop_target_slot_id := ""

var _drag_in_progress := false
var _active_source: Dictionary = {}


func _ready() -> void:
	mouse_exited.connect(_on_mouse_exited)


func configure_drag_source(source_kind: String, article_id: int, source_slot_id: String, preview_text: String) -> void:
	drag_source_kind = source_kind
	drag_article_id = article_id
	drag_source_slot_id = source_slot_id
	drag_preview_text = preview_text
	drag_enabled = article_id != -1 and source_kind in ["candidate", "slot"]


func clear_drag_source() -> void:
	drag_enabled = false
	drag_source_kind = ""
	drag_article_id = -1
	drag_source_slot_id = ""
	drag_preview_text = ""


func configure_drop_target(target_kind: String, target_slot_id: String = "") -> void:
	drop_target_kind = target_kind
	drop_target_slot_id = target_slot_id
	drop_enabled = target_kind in ["slot", "candidate_pool"]


func _get_drag_data(_at_position: Vector2) -> Variant:
	if disabled or not drag_enabled or drag_article_id == -1:
		return null
	_active_source = {
		"source_kind": drag_source_kind,
		"article_id": drag_article_id,
		"source_slot_id": drag_source_slot_id,
	}
	_drag_in_progress = true
	set_drag_preview(_make_drag_preview())
	drag_started.emit(_active_source.duplicate(true))
	return _active_source.duplicate(true)


func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:
	if disabled or not drop_enabled or not (data is Dictionary):
		return false
	var source := data as Dictionary
	var source_kind := str(source.get("source_kind", ""))
	var article_id := int(source.get("article_id", -1))
	if article_id == -1 or source_kind not in ["candidate", "slot"]:
		return false
	if drop_target_kind == "candidate_pool" and source_kind != "slot":
		return false
	drag_hovered.emit(drop_target_kind, drop_target_slot_id)
	return true


func _drop_data(_at_position: Vector2, data: Variant) -> void:
	if not _can_drop_data(_at_position, data):
		return
	article_dropped.emit((data as Dictionary).duplicate(true), drop_target_kind, drop_target_slot_id)


func _notification(what: int) -> void:
	if what != NOTIFICATION_DRAG_END or not _drag_in_progress:
		return
	_drag_in_progress = false
	var successful := get_viewport().gui_is_drag_successful()
	drag_finished.emit(_active_source.duplicate(true), successful)
	_active_source.clear()


func _on_mouse_exited() -> void:
	if drop_enabled:
		drag_exited.emit(drop_target_kind, drop_target_slot_id)


func _make_drag_preview() -> Control:
	var preview := PanelContainer.new()
	preview.custom_minimum_size = Vector2(228, 58)
	preview.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = Color("152933")
	style.border_color = Color("d6c08f")
	style.set_border_width_all(2)
	style.corner_radius_top_left = 3
	style.corner_radius_top_right = 3
	style.corner_radius_bottom_left = 3
	style.corner_radius_bottom_right = 3
	style.content_margin_left = 12
	style.content_margin_top = 8
	style.content_margin_right = 12
	style.content_margin_bottom = 8
	preview.add_theme_stylebox_override("panel", style)
	var label := Label.new()
	label.text = drag_preview_text if drag_preview_text != "" else "报道"
	label.add_theme_font_size_override("font_size", 13)
	label.add_theme_color_override("font_color", Color("d8d0bd"))
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	preview.add_child(label)
	return preview
