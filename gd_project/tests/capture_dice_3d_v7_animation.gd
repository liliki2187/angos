extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-03-dice-3d-v7-prototype/animation_frames_v7_5"
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

	var frame_index := 0
	for _i in range(4):
		frame_index = await _capture_at(scene, 0.0, frame_index)

	var motion_frames := 30
	for i in range(motion_frames):
		var t := lerpf(0.0, 1.18, float(i) / float(motion_frames - 1))
		frame_index = await _capture_at(scene, t, frame_index)

	for _i in range(12):
		frame_index = await _capture_at(scene, 1.12, frame_index)

	quit(0)

func _capture_at(scene: Control, demo_time: float, frame_index: int) -> int:
	scene.set_demo_time(demo_time)
	await _settle_frames(3)
	_save_png("frame_%03d.png" % frame_index)
	return frame_index + 1

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _save_png(file_name: String) -> void:
	var image := root.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
