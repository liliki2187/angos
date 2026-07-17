extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-15-region-task-board-runtime-v2"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	var ok := true
	ok = await _capture_state("", "01-region-empty-selection.png") and ok
	ok = await _capture_state("m330", "02-region-m330-selected.png") and ok
	ok = await _capture_state("temp_ufo", "03-region-deadline-selected.png") and ok
	ok = await _capture_state("m330", "04-region-m330-selected-1600x900.png", Vector2i(1600, 900)) and ok
	ok = await _capture_state("m330", "07-region-summary-nine-line-stress.png", Vector2i(1920, 1080), 9) and ok
	if not ok:
		push_error("Region task board v2 capture rejected one or more incomplete frames.")
		quit(1)
		return
	print("capture_region_task_board_runtime_v2.gd OK")
	quit(0)

func _capture_state(selected_task_id: String, file_name: String, capture_size: Vector2i = Vector2i(1920, 1080), summary_line_count: int = 0) -> bool:
	# 每个证明状态使用独立视口，避免移除 / 重建任务卡时复用旧脏区。
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = capture_size
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
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
	await _settle_frames(6)
	if not selected_task_id.is_empty():
		var board = scene.explore_phase.get_node("RegionTaskBoardV2")
		board.call("_on_event_pressed", selected_task_id)
		await _settle_frames(8)
		if summary_line_count > 0:
			var stress_payload: Dictionary = scene._build_explore_payload()
			var summary_lines: Array[String] = []
			for line_index in range(summary_line_count):
				summary_lines.append("第 %d 行：异常目击、口供矛盾与截稿风险需要在同一摘要区连续阅读。" % [line_index + 1])
			stress_payload.region_node_summary = "\n".join(summary_lines)
			board.call("render", stress_payload)
			await _settle_frames(6)
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var saved := _save_png(viewport, OUT_DIR, file_name)
	root.remove_child(viewport)
	viewport.queue_free()
	await process_frame
	return saved

func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _save_png(viewport: SubViewport, directory: String, file_name: String) -> bool:
	var texture := viewport.get_texture()
	if texture == null:
		push_error("SubViewport texture is null for %s" % file_name)
		return false
	var image := texture.get_image()
	if image == null:
		push_error("SubViewport image is null for %s" % file_name)
		return false
	if _sample_black_ratio(image) > 0.08:
		push_error("Capture contains an incomplete black dirty region: %s" % file_name)
		return false
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [directory, file_name]))
	return true

func _sample_black_ratio(image: Image) -> float:
	var black := 0
	var total := 0
	for y in range(0, image.get_height(), 24):
		for x in range(0, image.get_width(), 24):
			var color := image.get_pixel(x, y)
			if maxf(color.r, maxf(color.g, color.b)) < 0.006:
				black += 1
			total += 1
	return float(black) / maxf(1.0, float(total))
