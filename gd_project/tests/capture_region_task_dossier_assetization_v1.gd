extends SceneTree

const BoardV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd")

const OUT_DIR := "res://../docs/screenshots/2026-07-22-region-task-dossier-assetization-v1"
const FRAME_DIR := OUT_DIR + "/frames-dossier-runtime-v1"
const DOSSIER_RECT := Rect2i(1484, 96, 412, 960)


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(FRAME_DIR))
	_clear_old_frames()
	await _capture_selected_ready()
	await _capture_empty_disabled()
	await _capture_two_line_title_pressure()
	await _capture_runtime_state_demo()
	print("capture_region_task_dossier_assetization_v1.gd OK")
	quit(0)


func _capture_selected_ready() -> void:
	var viewport := _make_viewport()
	var board := _make_board(viewport)
	await _settle_frames(4)
	board.render(_selected_payload())
	await _settle_frames(10)
	await _save_full_and_dossier(viewport, "01-selected-ready-full-v1.png", "02-selected-ready-dossier-v1.png")
	await _dispose_viewport(viewport)


func _capture_empty_disabled() -> void:
	var viewport := _make_viewport()
	var board := _make_board(viewport)
	await _settle_frames(4)
	board.render(_empty_payload())
	await _settle_frames(10)
	await _save_dossier(viewport, "%s/03-empty-disabled-dossier-v1.png" % OUT_DIR)
	await _dispose_viewport(viewport)


func _capture_two_line_title_pressure() -> void:
	var viewport := _make_viewport()
	var board := _make_board(viewport)
	await _settle_frames(4)
	var payload := _selected_payload()
	payload.node_title = "明日电台与北岸停电预告的重复录音档案"
	board.render(payload)
	await _settle_frames(10)
	await _save_dossier(viewport, "%s/05-two-line-title-pressure-v1.png" % OUT_DIR)
	await _dispose_viewport(viewport)


func _capture_runtime_state_demo() -> void:
	var viewport := _make_viewport()
	var board := _make_board(viewport)
	await _settle_frames(4)
	var frame_index := 0
	board.render(_empty_payload())
	await _settle_frames(5)
	frame_index = await _hold_dossier_frames(viewport, frame_index, 10)
	board.render(_selected_payload())
	await _settle_frames(5)
	frame_index = await _hold_dossier_frames(viewport, frame_index, 12)
	var dispatch_button := board.find_child("DispatchButton", true, false) as Button
	if dispatch_button != null:
		dispatch_button.grab_focus()
	await _settle_frames(4)
	frame_index = await _hold_dossier_frames(viewport, frame_index, 10)
	board.render(_empty_payload())
	await _settle_frames(4)
	await _hold_dossier_frames(viewport, frame_index, 8)
	await _dispose_viewport(viewport)


func _make_viewport() -> SubViewport:
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(1920, 1080)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
	root.add_child(viewport)
	return viewport


func _make_board(viewport: SubViewport) -> Control:
	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1920, 1080)
	return board


func _selected_payload() -> Dictionary:
	return {
		"region_title": "北岸调查区",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": "event_radio_tomorrow",
		"nodes": [
			{
				"id": "event_radio_tomorrow",
				"name": "明日电台的停电预告",
				"kind": "chain",
				"days": 2,
				"type": "occult",
				"tone": "chain",
				"state": "available",
				"enabled": true,
				"map_pos": {"x": 0.73, "y": 0.34},
			},
			{
				"id": "event_substation",
				"name": "变电站空白值班表",
				"kind": "temp",
				"days": 1,
				"type": "sci",
				"tone": "deadline",
				"state": "urgent",
				"enabled": true,
				"map_pos": {"x": 0.52, "y": 0.60},
			},
		],
		"node_title": "明日电台的停电预告",
		"region_node_summary": "同一城区连续收到异常广播举报。\n停电后，旧电台会先播出明日新闻。\n三名听众记下了互相矛盾的时间。\n其中一段录音提到尚未发生的火灾。\n线路图显示信号绕过了主发射塔。\n编辑部需要确认预告是否能被改变。\n本次调查将决定后续连续追踪入口。",
		"region_node_meta": "地点：北岸旧电台 / 变电站\n耗时：2 天　需求：洞察 / 推理",
		"region_node_deadline": "本周截稿前 2 天",
		"region_node_chain": "连续追踪：成功后开启“被改写的明日版”",
		"region_node_risk_level": "高",
		"region_node_recommendation": "建议：优先派洞察记者；签批时复核黑骰风险。",
		"region_action_hint": "本页选择不会消耗天数。",
		"dispatch_open_enabled": true,
		"dispatch_open_text": "送至签批台",
	}


func _empty_payload() -> Dictionary:
	var payload := _selected_payload()
	payload.selected_node_id = ""
	payload.node_title = "选择一份事件档案"
	payload.region_node_summary = ""
	payload.region_node_meta = ""
	payload.region_node_deadline = ""
	payload.region_node_chain = ""
	payload.region_node_risk_level = ""
	payload.region_node_recommendation = ""
	payload.dispatch_open_enabled = false
	payload.dispatch_open_text = "先选择任务"
	return payload


func _hold_dossier_frames(viewport: SubViewport, frame_index: int, count: int) -> int:
	for _index in range(count):
		await process_frame
		viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
		await RenderingServer.frame_post_draw
		var image := viewport.get_texture().get_image().get_region(DOSSIER_RECT)
		var error := image.save_png(ProjectSettings.globalize_path("%s/frame_%03d.png" % [FRAME_DIR, frame_index]))
		if error != OK:
			push_error("Failed to save dossier animation frame: %s" % error_string(error))
		frame_index += 1
	return frame_index


func _save_full_and_dossier(viewport: SubViewport, full_name: String, dossier_name: String) -> void:
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	var full_error := image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, full_name]))
	if full_error != OK:
		push_error("Failed to save full dossier capture: %s" % error_string(full_error))
	var dossier := image.get_region(DOSSIER_RECT)
	var dossier_error := dossier.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, dossier_name]))
	if dossier_error != OK:
		push_error("Failed to save dossier crop: %s" % error_string(dossier_error))


func _save_dossier(viewport: SubViewport, path: String) -> void:
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image().get_region(DOSSIER_RECT)
	var error := image.save_png(ProjectSettings.globalize_path(path))
	if error != OK:
		push_error("Failed to save dossier crop: %s" % error_string(error))


func _clear_old_frames() -> void:
	var directory := DirAccess.open(ProjectSettings.globalize_path(FRAME_DIR))
	if directory == null:
		return
	for file_name in directory.get_files():
		if file_name.begins_with("frame_") and file_name.ends_with(".png"):
			directory.remove(file_name)


func _dispose_viewport(viewport: SubViewport) -> void:
	root.remove_child(viewport)
	viewport.queue_free()
	await process_frame


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
