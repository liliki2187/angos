extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-11-world-map-assetized-v4-godot"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	root.size = Vector2i(1920, 1080)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))

	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	var scene := packed.instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	scene.offset_left = 0.0
	scene.offset_top = 0.0
	scene.offset_right = 0.0
	scene.offset_bottom = 0.0

	await _settle_frames(8)
	scene._on_advance_phase_pressed()
	await _settle_frames(8)
	_save_png("01-world-map-assetized.png")

	scene._on_region_pressed("east_asia")
	await _settle_frames(8)
	_save_png("02-world-map-locked-region.png")
	quit(0)

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _save_png(file_name: String) -> void:
	var image := root.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
