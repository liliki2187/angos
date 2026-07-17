extends PanelContainer

signal drag_hovered(target_kind: String, target_slot_id: String)
signal drag_exited(target_kind: String, target_slot_id: String)
signal article_dropped(source: Dictionary, target_kind: String, target_slot_id: String)

var drop_enabled := false


func _ready() -> void:
	mouse_exited.connect(func() -> void: drag_exited.emit("candidate_pool", ""))


func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:
	if not drop_enabled or not (data is Dictionary):
		return false
	var source := data as Dictionary
	if str(source.get("source_kind", "")) != "slot" or int(source.get("article_id", -1)) == -1:
		return false
	drag_hovered.emit("candidate_pool", "")
	return true


func _drop_data(_at_position: Vector2, data: Variant) -> void:
	if not _can_drop_data(_at_position, data):
		return
	article_dropped.emit((data as Dictionary).duplicate(true), "candidate_pool", "")
