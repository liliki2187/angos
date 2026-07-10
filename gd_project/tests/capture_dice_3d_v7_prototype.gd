extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-07-dice-3d-v019d-text-only-runtime-godot"
const SCENE := "res://scenes/dev/Dice3DV7Prototype.tscn"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	root.size = Vector2i(1920, 1080)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))

	var packed := load(SCENE) as PackedScene
	var scene := packed.instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	scene.offset_left = 0.0
	scene.offset_top = 0.0
	scene.offset_right = 0.0
	scene.offset_bottom = 0.0

	await _settle_frames(8)
	var frames := [
		["20-runtime-cell-contract.png", 0.0],
		["21-runtime-cell-precompress.png", 0.06],
		["22-runtime-cell-fast-tumble.png", 0.28],
		["23-runtime-cell-impact.png", 0.53],
		["24-runtime-cell-rebound-settle.png", 0.78],
		["25-runtime-cell-final-read.png", 1.12],
	]
	for item in frames:
		scene.set_demo_time(float(item[1]))
		await _settle_frames(4)
		_save_png(String(item[0]))
	quit(0)

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _save_png(file_name: String) -> void:
	var image := root.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
