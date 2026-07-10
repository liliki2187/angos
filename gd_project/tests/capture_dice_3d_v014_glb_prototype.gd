extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-07-dice-3d-v014-number-priority-glb-uv-godot"
const SCENE := "res://scenes/dev/Dice3DV014GlbPrototype.tscn"

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
		["40-runtime-cell-contract.png", 0.0],
		["41-runtime-cell-precompress.png", 0.06],
		["42-runtime-cell-fast-tumble.png", 0.28],
		["43-runtime-cell-impact.png", 0.53],
		["44-runtime-cell-rebound-settle.png", 0.78],
		["45-runtime-cell-final-read.png", 1.12],
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
