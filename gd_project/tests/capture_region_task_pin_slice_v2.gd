extends SceneTree

const BoardV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd")
const EventPin := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionEventPin.gd")

const OUT_DIR := "res://../docs/screenshots/2026-07-16-region-task-pin-slice-v2"
const FRAME_DIR := OUT_DIR + "/frames"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(FRAME_DIR))
	await _capture_board(_fixture_payload(5, "event_2", true), "07-five-dense-selected-label-clearance.png")
	await _capture_board(_fixture_payload(8, "", true), "02-cluster-collapsed.png")
	await _capture_board(_fixture_payload(8, "", true), "03-cluster-expanded.png", true)
	await _capture_board(_edge_payload(), "04-right-edge-label-clamp.png")
	await _capture_state_matrix()
	await _capture_animation_frames()
	print("capture_region_task_pin_slice_v2.gd OK")
	quit(0)

func _capture_board(payload: Dictionary, file_name: String, expand_cluster: bool = false) -> void:
	var viewport := _make_viewport(Vector2i(1920, 1080))
	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1920, 1080)
	await _settle_frames(4)
	board.render(payload)
	await _settle_frames(6)
	if expand_cluster:
		var keys := board.get_cluster_keys()
		if not keys.is_empty():
			board.call("_toggle_cluster", keys[0])
			await _settle_frames(6)
	await _save_png(viewport, "%s/%s" % [OUT_DIR, file_name])
	await _dispose_viewport(viewport)

func _capture_state_matrix() -> void:
	var viewport := _make_viewport(Vector2i(1920, 1080))
	var stage := Control.new()
	stage.size = Vector2(1920, 1080)
	viewport.add_child(stage)
	var background := ColorRect.new()
	background.size = stage.size
	background.color = Color("071d2e")
	stage.add_child(background)
	_add_label(stage, "事件图钉资产化状态矩阵 · 真实 Godot 运行态", Rect2(74, 48, 1500, 52), 30, Color("f2ead6"))
	_add_label(stage, "同一透明母版；文字、图标、状态环、禁用线与角标均由运行时叠加", Rect2(76, 104, 1500, 38), 17, Color("aebc9a"))

	var states := [
		{"name": "AVAILABLE", "state": "available", "selected": false, "enabled": true, "tone": "normal", "kind": "permanent"},
		{"name": "HOVER", "state": "available", "selected": false, "enabled": true, "tone": "normal", "kind": "permanent", "hover": true},
		{"name": "SELECTED", "state": "available", "selected": true, "enabled": true, "tone": "chain", "kind": "chain"},
		{"name": "DISABLED", "state": "disabled", "selected": false, "enabled": false, "tone": "locked", "kind": "permanent"},
		{"name": "ASSIGNED", "state": "assigned", "selected": false, "enabled": true, "tone": "chain", "kind": "chain"},
		{"name": "URGENT", "state": "urgent", "selected": true, "enabled": true, "tone": "deadline", "kind": "temp"},
		{"name": "LOCKED", "state": "locked", "selected": false, "enabled": false, "tone": "locked", "kind": "hidden"},
		{"name": "FOCUS", "state": "available", "selected": false, "enabled": true, "tone": "normal", "kind": "permanent", "focus": true},
	]
	for index in range(states.size()):
		var spec: Dictionary = states[index]
		var column := index % 2
		var row := index / 2
		var origin := Vector2(110.0 + column * 900.0, 190.0 + row * 205.0)
		_add_label(stage, str(spec.name), Rect2(origin.x, origin.y - 34.0, 280.0, 28.0), 17, Color("d7cfb5"))
		var pin := EventPin.new()
		pin.position = origin
		pin.size = Vector2(72.0, 80.0)
		stage.add_child(pin)
		pin.configure({
			"id": "qa_%d" % index,
			"name": "M330 末班车空白段" if column == 0 else "雷达异常光点",
			"kind": spec.kind,
			"days": 2,
			"tone": spec.tone,
			"state": spec.state,
			"enabled": spec.enabled,
			"map_pos": {"x": 0.2 if column == 0 else 0.88, "y": 0.5},
		}, bool(spec.selected))
		if bool(spec.get("hover", false)):
			pin.set_external_hover(true)
		if bool(spec.get("focus", false)):
			pin.call_deferred("grab_focus")
	await _settle_frames(8)
	await _save_png(viewport, "%s/05-runtime-state-matrix.png" % OUT_DIR)
	await _dispose_viewport(viewport)

func _capture_animation_frames() -> void:
	var viewport := _make_viewport(Vector2i(1280, 720))
	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1280, 720)
	await _settle_frames(4)
	var payload := _fixture_payload(5, "", false)
	board.render(payload)
	await _settle_frames(6)
	var pin = board.find_child("EventPin_event_2", true, false)
	for frame_index in range(8):
		await _save_png(viewport, "%s/frame_%03d.png" % [FRAME_DIR, frame_index])
	if is_instance_valid(pin):
		pin.call("set_external_hover", true)
	for frame_index in range(8, 16):
		await _settle_frames(1)
		await _save_png(viewport, "%s/frame_%03d.png" % [FRAME_DIR, frame_index])
	payload.selected_node_id = "event_2"
	board.render(payload)
	for frame_index in range(16, 26):
		await _settle_frames(1)
		await _save_png(viewport, "%s/frame_%03d.png" % [FRAME_DIR, frame_index])
	await _dispose_viewport(viewport)

func _fixture_payload(event_count: int, selected_id: String, force_dense: bool) -> Dictionary:
	var nodes: Array = []
	for index in range(event_count):
		var task_id := "event_%d" % index
		nodes.append({
			"id": task_id,
			"name": "异常事件 %d" % [index + 1],
			"kind": "temp" if index == 2 else "chain" if index == 3 else "permanent",
			"days": 1 + index % 3,
			"type": "pop" if index == 2 else "occult" if index == 3 else "sci",
			"tone": "deadline" if index == 2 else "chain" if index == 3 else "normal",
			"state": "urgent" if index == 2 else "assigned" if index == 3 else "available",
			"enabled": true,
			"map_pos": {"x": 0.5, "y": 0.5} if force_dense else {"x": 0.18 + 0.15 * index, "y": 0.28 + 0.11 * (index % 3)},
		})
	return {
		"region_title": "合同验证区",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": selected_id,
		"nodes": nodes,
		"node_title": "异常事件 3" if not selected_id.is_empty() else "选择一份事件档案",
		"region_node_summary": "同一区域可以出现多个事件点；密集时先显示聚合标记，展开后仍保持任务 id 与地图图钉一一对应。",
		"region_node_meta": "限时/热点 · 需求 洞察/推理 · 2天",
		"region_node_deadline": "截稿剩 2 天" if not selected_id.is_empty() else "",
		"region_node_chain": "连续追踪：成功后出现后续线索" if not selected_id.is_empty() else "",
		"region_action_hint": "送至签批台配置骰池，本页不消耗天数。",
		"dispatch_open_enabled": not selected_id.is_empty(),
		"dispatch_open_text": "送至签批台" if not selected_id.is_empty() else "先选择任务",
	}

func _edge_payload() -> Dictionary:
	var payload := _fixture_payload(1, "event_0", false)
	payload.nodes[0].name = "右岸边界长标题事件"
	payload.nodes[0].map_pos = {"x": 0.945, "y": 0.10}
	return payload

func _make_viewport(viewport_size: Vector2i) -> SubViewport:
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = viewport_size
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
	root.add_child(viewport)
	return viewport

func _dispose_viewport(viewport: SubViewport) -> void:
	root.remove_child(viewport)
	viewport.queue_free()
	await process_frame

func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _save_png(viewport: SubViewport, path: String) -> void:
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path(path))

func _add_label(parent: Control, text_value: String, rect: Rect2, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.position = rect.position
	label.size = rect.size
	label.text = text_value
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	parent.add_child(label)
	return label
