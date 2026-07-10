extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-07-dice-3d-v013-text-safe-glb-uv-godot/animation_frames"
const SCENE := "res://scenes/dev/Dice3DV013GlbPrototype.tscn"

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

	var times: Array[float] = []
	for _i in range(4):
		times.append(0.0)
	var motion_frames := 30
	for i in range(motion_frames):
		var t := lerpf(0.0, 1.18, float(i) / float(motion_frames - 1))
		times.append(t)
	for _i in range(12):
		times.append(1.12)

	var frame_index := 0
	for t in times:
		scene.set_demo_time(t)
		await _settle_frames(4)
		_save_png("frame_%03d.png" % frame_index)
		frame_index += 1

	quit(0)

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _save_png(file_name: String) -> void:
	var image := root.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
