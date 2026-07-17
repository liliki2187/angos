extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-24-world-map-benchmark-landing"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const CAPTURE_SIZE := Vector2i(1920, 1080)

var _scene: Control
var _assembly: Control


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	root.size = CAPTURE_SIZE
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	if not await _build_live_scene():
		quit(1)
		return

	var ok := true
	ok = _validate_snapshot("us", false, false) and ok
	ok = await _capture("645-world-map-wmw-assembly-host-collapsed.png") and ok

	_assembly.call("set_mission_intel_expanded", true)
	await _settle_frames(5)
	ok = _validate_snapshot("us", true, false) and ok
	ok = await _capture("646-world-map-wmw-assembly-host-expanded.png") and ok

	_scene.call("_on_region_pressed", "east_asia")
	await _settle_frames(6)
	ok = _validate_snapshot("east_asia", false, true) and ok
	ok = await _capture("647-world-map-wmw-assembly-host-locked.png") and ok

	_scene.call("_on_region_pressed", "us")
	await _settle_frames(4)
	_assembly.call("set_debug_zones", true)
	await _settle_frames(4)
	ok = _validate_snapshot("us", false, false) and ok
	ok = await _capture("648-world-map-wmw-assembly-host-geometry-qa.png") and ok

	if not ok:
		push_error("WMW assembly-host capture rejected one or more states")
		quit(1)
		return
	print("capture_world_map_wmw_assembly_host.gd OK")
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
	_assembly = _scene.explore_phase.call("get_world_map_assembly") as Control
	if _assembly == null or not _assembly.visible:
		push_error("Independent WMW assembly is not visible in the production scene")
		return false
	if _scene.header_panel.visible or _scene.world_shell_art.visible or _scene.explore_phase.root_vbox.visible:
		push_error("Legacy WeeklyRunGame/GLOBAL CHANNEL host remains visible")
		return false
	var host_rect := _assembly.get_global_rect()
	if not host_rect.position.is_equal_approx(Vector2.ZERO) or not host_rect.size.is_equal_approx(Vector2(CAPTURE_SIZE)):
		push_error("WMW assembly did not receive the full 1920x1080 host: %s" % host_rect)
		return false
	print("live_wmw_assembly_rect=%s" % host_rect)
	return true


func _validate_snapshot(expected_region_id: String, expanded: bool, locked: bool) -> bool:
	var state: Dictionary = _assembly.call("get_state_snapshot")
	for key in ["selected_region_id", "left_selected_region_id", "map_selected_region_id", "dossier_region_id", "cta_region_id"]:
		if str(state.get(key, "")) != expected_region_id:
			push_error("%s drifted from selected_region_id=%s" % [key, expected_region_id])
			return false
	if str(state.get("map_artifact_type", "")) != "structure_only":
		push_error("Map placeholder status was not disclosed as structure_only")
		return false
	if float(state.get("center_right_edge", 9999.0)) > 916.0:
		push_error("Center region escaped its x=916 safe boundary")
		return false
	var dossier: Dictionary = state.get("dossier", {})
	if bool(dossier.get("expanded", false)) != expanded:
		push_error("Mission-intel expanded state drifted")
		return false
	if locked:
		if not bool(dossier.get("summary_disabled", false)) or not bool(dossier.get("primary_disabled", false)):
			push_error("Locked region actions are not both disabled")
			return false
		if int(dossier.get("preview_source_rows", -1)) != 0:
			push_error("Locked region leaked task preview rows")
			return false
	elif dossier.get("interactive_button_names", []) != ["MissionSummaryButton", "PrimaryEnterButton"]:
		push_error("A5.1 interactive controls drifted")
		return false
	return true


func _capture(file_name: String) -> bool:
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
	var result := image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
	if result != OK:
		push_error("save_png failed for %s: %s" % [file_name, result])
		return false
	if not _validate_full_frame(image, file_name):
		return false
	print("saved %s sampled_colors=%d" % [file_name, _sampled_color_count(image)])
	return true


func _validate_full_frame(image: Image, file_name: String) -> bool:
	if image.get_size() != CAPTURE_SIZE:
		push_error("Capture size drifted for %s: %s" % [file_name, image.get_size()])
		return false
	if _sampled_transparent_count(image) > 0:
		push_error("Capture contains transparent dirty-frame samples for %s" % file_name)
		return false
	var sampled_colors := _sampled_color_count(image)
	if sampled_colors < 160:
		push_error("Capture has only %d sampled colors for %s" % [sampled_colors, file_name])
		return false
	var required_regions := {
		"left_cards": Rect2i(36, 24, 342, 1032),
		"center_map": Rect2i(402, 24, 972, 1032),
		"right_dossier": Rect2i(1398, 45, 480, 780),
	}
	for region_name in required_regions:
		var metrics := _region_signal(image, required_regions[region_name])
		if metrics.colors < 18 or metrics.light_samples < 8:
			push_error("Capture region %s is incomplete for %s: %s" % [region_name, file_name, metrics])
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
