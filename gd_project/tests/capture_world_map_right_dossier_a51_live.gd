extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-24-world-map-benchmark-landing"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const CAPTURE_SIZE := Vector2i(1920, 1080)
const RIGHT_DOSSIER_BOUNDARY_X := 1400

var _scene: Control
var _dossier: Control
var _collapsed_baseline: Image
var _expanded_baseline: Image

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	root.size = CAPTURE_SIZE
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	if not await _build_live_scene():
		quit(1)
		return

	var ok := true
	ok = _validate_state(false) and ok
	ok = await _capture("639-world-map-wmw-right-dossier-a5-1-live-collapsed.png", "collapsed") and ok

	_dossier.call("set_mission_intel_expanded", true)
	await _settle_frames(6)
	ok = _validate_state(true) and ok
	ok = await _capture("640-world-map-wmw-right-dossier-a5-1-live-expanded.png", "expanded") and ok

	_dossier.call("set_debug_zones", true)
	await _settle_frames(4)
	ok = await _capture("641-world-map-wmw-right-dossier-a5-1-live-contract-qa.png", "qa") and ok

	if not ok:
		push_error("A5.1 production runtime capture rejected one or more states")
		quit(1)
		return
	print("capture_world_map_right_dossier_a51_live.gd OK")
	quit(0)

func _build_live_scene() -> bool:
	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	if packed == null:
		push_error("WeeklyRunGame.tscn could not be loaded")
		return false
	_scene = packed.instantiate() as Control
	root.add_child(_scene)
	_scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	_scene.offset_left = 0.0
	_scene.offset_top = 0.0
	_scene.offset_right = 0.0
	_scene.offset_bottom = 0.0
	await _settle_frames(6)
	_scene.call("_on_advance_phase_pressed")
	await _settle_frames(10)
	_dossier = _scene.explore_phase.call("get_world_right_dossier_a51") as Control
	if _dossier == null:
		push_error("A5.1 dossier is not mounted in the production scene")
		return false
	var dossier_rect := _dossier.get_global_rect()
	if dossier_rect.position.x < RIGHT_DOSSIER_BOUNDARY_X or dossier_rect.end.x > CAPTURE_SIZE.x - 16:
		push_error("A5.1 dossier escaped the right-column boundary: %s" % dossier_rect)
		return false
	if dossier_rect.size.x < 400.0:
		push_error("A5.1 dossier host is narrower than the approved desktop placement: %s" % dossier_rect)
		return false
	print("live_dossier_rect=%s" % dossier_rect)
	return true

func _validate_state(expanded: bool) -> bool:
	var state: Dictionary = _dossier.call("get_state_snapshot")
	if str(state.get("region_id", "")) != "us":
		push_error("Live dossier is not bound to the selected production region")
		return false
	if bool(state.get("expanded", false)) != expanded:
		push_error("Live dossier expanded state drifted")
		return false
	if int(state.get("preview_source_rows", 0)) != 4:
		push_error("Production North America preview must expose four visible missions")
		return false
	if state.get("interactive_button_names", []) != ["MissionSummaryButton", "PrimaryEnterButton"]:
		push_error("Live dossier interactive controls drifted")
		return false
	if int(state.get("task_row_hit_rects", -1)) != 0:
		push_error("Live mission preview rows must remain read-only")
		return false
	var expected_rows := 2 if expanded else 0
	if int(state.get("preview_rendered_rows", -1)) != expected_rows:
		push_error("Live dossier preview row count drifted")
		return false
	if expanded and str(state.get("mission_facts", "")) != "已显示 2 / 共 4 条":
		push_error("Live dossier expanded count drifted")
		return false
	return true

func _capture(file_name: String, state_id: String) -> bool:
	await _settle_frames(6)
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
	if not _validate_full_frame(image, file_name):
		return false
	if state_id == "expanded" and _count_outside_dossier_changes(image, _collapsed_baseline) > 0:
		push_error("Expanded state changed pixels outside the right dossier")
		return false
	if state_id == "qa" and _count_outside_dossier_changes(image, _expanded_baseline) > 0:
		push_error("QA overlay changed pixels outside the right dossier")
		return false
	if state_id == "collapsed":
		_collapsed_baseline = image.duplicate()
	elif state_id == "expanded":
		_expanded_baseline = image.duplicate()
	var result := image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
	if result != OK:
		push_error("save_png failed for %s: %s" % [file_name, result])
		return false
	print("saved %s sampled_colors=%d transparent_samples=0" % [file_name, _sampled_color_count(image)])
	return true

func _validate_full_frame(image: Image, file_name: String) -> bool:
	if image.get_size() != CAPTURE_SIZE:
		push_error("Capture size drifted for %s: %s" % [file_name, image.get_size()])
		return false
	if _sampled_transparent_count(image) > 0:
		push_error("Capture contains transparent dirty-frame samples for %s" % file_name)
		return false
	var sampled_colors := _sampled_color_count(image)
	if sampled_colors < 240:
		push_error("Capture has only %d sampled colors for %s" % [sampled_colors, file_name])
		return false
	var required_regions := {
		"header": Rect2i(0, 0, 1920, 120),
		"left_index": Rect2i(24, 130, 310, 820),
		"map": Rect2i(340, 130, 1120, 820),
		"right_dossier": Rect2i(1480, 180, 416, 760),
	}
	for region_name in required_regions:
		var region_metrics := _region_signal(image, required_regions[region_name])
		if region_metrics.colors < 24 or region_metrics.light_samples < 8:
			push_error("Capture region %s is incomplete for %s: %s" % [region_name, file_name, region_metrics])
			return false
	return true

func _region_signal(image: Image, rect: Rect2i) -> Dictionary:
	var colors := {}
	var light_samples := 0
	for y in range(rect.position.y, rect.end.y, 8):
		for x in range(rect.position.x, rect.end.x, 8):
			var color := image.get_pixel(x, y)
			colors[color.to_rgba32()] = true
			if maxf(color.r, maxf(color.g, color.b)) > 0.16:
				light_samples += 1
	return {"colors": colors.size(), "light_samples": light_samples}

func _count_outside_dossier_changes(image: Image, baseline: Image) -> int:
	if baseline == null or image.get_size() != baseline.get_size():
		return 1000000
	var changed := 0
	for y in range(0, image.get_height(), 4):
		for x in range(0, RIGHT_DOSSIER_BOUNDARY_X, 4):
			if image.get_pixel(x, y) != baseline.get_pixel(x, y):
				changed += 1
	return changed

func _sampled_color_count(image: Image) -> int:
	var colors := {}
	for y in range(0, image.get_height(), 8):
		for x in range(0, image.get_width(), 8):
			colors[image.get_pixel(x, y).to_rgba32()] = true
	return colors.size()

func _sampled_transparent_count(image: Image) -> int:
	var transparent := 0
	for y in range(0, image.get_height(), 8):
		for x in range(0, image.get_width(), 8):
			if image.get_pixel(x, y).a < 0.999:
				transparent += 1
	return transparent

func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
