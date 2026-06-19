extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-15-region-task-board-godot-v2"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))

	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(1920, 1080)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)

	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	var scene := packed.instantiate() as Control
	viewport.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	scene.offset_left = 0.0
	scene.offset_top = 0.0
	scene.offset_right = 0.0
	scene.offset_bottom = 0.0

	await _settle_frames(4)
	scene._on_advance_phase_pressed()
	await _settle_frames(4)
	scene._on_enter_region_requested()
	await _settle_frames(4)
	_save_png(viewport, "01-region-task-board-empty.png")

	scene._on_node_pressed("m330")
	await _settle_frames(4)
	_save_png(viewport, "02-region-task-board-m330-selected.png")

	scene._on_node_pressed("temp_ufo")
	await _settle_frames(4)
	_save_png(viewport, "03-region-task-board-deadline-selected.png")
	quit(0)

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _save_png(viewport: SubViewport, file_name: String) -> void:
	var image := viewport.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
