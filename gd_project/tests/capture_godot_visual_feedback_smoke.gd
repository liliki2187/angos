extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-29-godot-visual-feedback-smoke"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const CAPTURE_SIZE := Vector2i(1920, 1080)

var _scene: Control
var _captures: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	root.size = CAPTURE_SIZE
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))

	if not await _build_scene():
		quit(1)
		return

	var ok := true
	_scene.call("_on_advance_phase_pressed")
	await _settle_frames(10)
	ok = await _capture("01-world-map-region-ready.png", "world_map_region_ready") and ok

	_scene.call("_on_enter_region_requested")
	await _settle_frames(8)
	_scene.call("_on_node_pressed", "m330")
	await _settle_frames(8)
	ok = await _capture("02-region-task-m330-selected.png", "region_task_m330_selected") and ok

	_scene.call("_on_open_dispatch_requested")
	await _settle_frames(8)
	ok = await _capture("03-dispatch-m330-no-staff.png", "dispatch_m330_no_staff") and ok

	_scene.call("_toggle_staff", "ivy")
	_scene.call("_toggle_staff", "mora")
	await _settle_frames(8)
	ok = await _capture("04-dispatch-m330-staff-selected.png", "dispatch_m330_staff_selected") and ok

	_write_manifest(ok)
	if not ok:
		push_error("Godot visual feedback smoke rejected one or more screenshots.")
		quit(1)
		return

	print("capture_godot_visual_feedback_smoke.gd OK")
	quit(0)

func _build_scene() -> bool:
	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	if packed == null:
		push_error("WeeklyRunGame.tscn could not be loaded")
		return false

	_scene = packed.instantiate() as Control
	if _scene == null:
		push_error("WeeklyRunGame.tscn did not instantiate as Control")
		return false

	root.add_child(_scene)
	_scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	_scene.offset_left = 0.0
	_scene.offset_top = 0.0
	_scene.offset_right = 0.0
	_scene.offset_bottom = 0.0
	await _settle_frames(10)
	return true

func _capture(file_name: String, state_id: String) -> bool:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw

	var texture := root.get_texture()
	if texture == null:
		push_error("Root window texture is null for %s" % file_name)
		return false

	var image := texture.get_image()
	if image == null:
		push_error("Root window image is null for %s" % file_name)
		return false

	var metrics := _image_metrics(image)
	var passed := _validate_capture(image, metrics, file_name)
	var output_path := "%s/%s" % [OUT_DIR, file_name]
	if passed:
		var save_result := image.save_png(ProjectSettings.globalize_path(output_path))
		if save_result != OK:
			push_error("save_png failed for %s: %s" % [file_name, save_result])
			passed = false

	_captures.append({
		"state_id": state_id,
		"file": file_name,
		"size": "%dx%d" % [image.get_width(), image.get_height()],
		"sampled_colors": int(metrics.sampled_colors),
		"black_ratio": float(metrics.black_ratio),
		"transparent_samples": int(metrics.transparent_samples),
		"passed": passed,
	})
	print("visual_capture %s passed=%s colors=%d black_ratio=%.4f" % [file_name, str(passed), int(metrics.sampled_colors), float(metrics.black_ratio)])
	return passed

func _validate_capture(image: Image, metrics: Dictionary, file_name: String) -> bool:
	var ok := true
	if image.get_size() != CAPTURE_SIZE:
		push_error("Capture size drifted for %s: %s" % [file_name, image.get_size()])
		ok = false
	if int(metrics.transparent_samples) > 0:
		push_error("Capture contains transparent dirty-frame samples for %s" % file_name)
		ok = false
	if int(metrics.sampled_colors) < 240:
		push_error("Capture has only %d sampled colors for %s" % [int(metrics.sampled_colors), file_name])
		ok = false
	if float(metrics.black_ratio) > 0.35:
		push_error("Capture is suspiciously black for %s: %.4f" % [file_name, float(metrics.black_ratio)])
		ok = false

	var regions := {
		"header": Rect2i(0, 0, 1920, 120),
		"left": Rect2i(16, 128, 360, 840),
		"center": Rect2i(420, 128, 940, 840),
		"right": Rect2i(1400, 128, 500, 840),
	}
	for region_name in regions:
		var region_metrics := _region_signal(image, regions[region_name])
		if int(region_metrics.colors) < 18 or int(region_metrics.visible_samples) < 8:
			push_error("Capture region %s is incomplete for %s: %s" % [region_name, file_name, region_metrics])
			ok = false
	return ok

func _image_metrics(image: Image) -> Dictionary:
	var colors := {}
	var black := 0
	var transparent := 0
	var total := 0
	for y in range(0, image.get_height(), 8):
		for x in range(0, image.get_width(), 8):
			var color := image.get_pixel(x, y)
			colors[color.to_rgba32()] = true
			if maxf(color.r, maxf(color.g, color.b)) < 0.006:
				black += 1
			if color.a < 0.999:
				transparent += 1
			total += 1
	return {
		"sampled_colors": colors.size(),
		"black_ratio": float(black) / maxf(1.0, float(total)),
		"transparent_samples": transparent,
	}

func _region_signal(image: Image, rect: Rect2i) -> Dictionary:
	var colors := {}
	var visible_samples := 0
	for y in range(rect.position.y, rect.end.y, 12):
		for x in range(rect.position.x, rect.end.x, 12):
			var color := image.get_pixel(x, y)
			colors[color.to_rgba32()] = true
			if maxf(color.r, maxf(color.g, color.b)) > 0.08:
				visible_samples += 1
	return {
		"colors": colors.size(),
		"visible_samples": visible_samples,
	}

func _write_manifest(ok: bool) -> void:
	var manifest := {
		"script": "res://tests/capture_godot_visual_feedback_smoke.gd",
		"scene": WEEKLY_RUN_SCENE,
		"capture_size": "%dx%d" % [CAPTURE_SIZE.x, CAPTURE_SIZE.y],
		"purpose": "runtime visual feedback smoke; not a visual quality approval",
		"passed": ok,
		"captures": _captures,
	}
	var file := FileAccess.open(ProjectSettings.globalize_path("%s/capture-manifest.json" % OUT_DIR), FileAccess.WRITE)
	if file == null:
		push_error("Could not write visual feedback manifest")
		return
	file.store_string(JSON.stringify(manifest, "\t"))

func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
