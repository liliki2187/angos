extends Control

const WEEKLY_RUN_SCENE := preload("res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn")

func _ready() -> void:
	Globals.log("FullChainGame", "Deprecated full_chain scene opened; forwarding to weekly_run shim.")
	for child in get_children():
		remove_child(child)
		child.queue_free()

	var weekly_run := WEEKLY_RUN_SCENE.instantiate()
	weekly_run.name = "WeeklyRunCompatRoot"
	add_child(weekly_run)

	if weekly_run is Control:
		weekly_run.set_anchors_preset(Control.PRESET_FULL_RECT)
		weekly_run.offset_left = 0.0
		weekly_run.offset_top = 0.0
		weekly_run.offset_right = 0.0
		weekly_run.offset_bottom = 0.0
