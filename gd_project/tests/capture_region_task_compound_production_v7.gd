extends SceneTree

const BoardV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd")
const EventPin := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionEventPin.gd")

const OUT_DIR := "res://../docs/screenshots/2026-07-21-region-task-compound-production-v7"
const FRAME_DIR := OUT_DIR + "/frames-runtime-v7"


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(FRAME_DIR))
	_clear_old_frames()
	await _capture_board(_fixture_payload(5, "event_2", true), "01-five-dense-selected-v7.png")
	await _capture_board(_edge_payload(), "02-right-edge-dossier-v7.png")
	await _capture_state_and_kind_matrix()
	await _capture_board(_fixture_payload(8, "", true), "05-cluster-collapsed-v7.png")
	await _capture_board(_fixture_payload(8, "", true), "06-cluster-expanded-v7.png", true)
	await _capture_runtime_animation()
	print("capture_region_task_compound_production_v7.gd OK")
	quit(0)


func _clear_old_frames() -> void:
	var directory := DirAccess.open(ProjectSettings.globalize_path(FRAME_DIR))
	if directory == null:
		return
	for file_name in directory.get_files():
		if file_name.begins_with("frame_") and file_name.ends_with(".png"):
			directory.remove(file_name)


func _capture_board(payload: Dictionary, file_name: String, expand_cluster: bool = false) -> void:
	var viewport := _make_viewport()
	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1920, 1080)
	await _settle_frames(4)
	board.render(payload)
	await _settle_frames(8)
	if expand_cluster:
		var cluster_keys := board.get_cluster_keys()
		if not cluster_keys.is_empty():
			board.call("_toggle_cluster", cluster_keys[0])
			await _settle_frames(8)
	await _save_png(viewport, "%s/%s" % [OUT_DIR, file_name])
	await _dispose_viewport(viewport)


func _capture_state_and_kind_matrix() -> void:
	var viewport := _make_viewport()
	var stage := Control.new()
	stage.size = Vector2(1920, 1080)
	viewport.add_child(stage)
	var background := ColorRect.new()
	background.size = stage.size
	background.color = Color("071d2e")
	stage.add_child(background)
	_add_label(stage, "区域任务短签 v7 · 一体 compound 真实运行态", Rect2(70, 42, 1500, 48), 30, Color("f2ead6"))
	_add_label(stage, "上排 HOVER：中性 B 闭合框；中排 SELECTED：框与后纸跟随任务类型色；下排：固定美术状态 badge / 键盘焦点", Rect2(72, 96, 1700, 36), 17, Color("aebc9a"))

	var kinds := [
		{"kind": "permanent", "label": "常驻 / 绿色", "name": "罗斯威尔档案残页"},
		{"kind": "chain", "label": "连续 / 青蓝", "name": "M330 末班车空白段"},
		{"kind": "hidden", "label": "隐藏 / 深蓝灰", "name": "黑色方尖碑回声"},
		{"kind": "temp", "label": "限时 / 棕黄", "name": "雷达异常光点"},
	]
	for index in range(kinds.size()):
		var kind_spec: Dictionary = kinds[index]
		var x := 72.0 + float(index) * 450.0
		_add_label(stage, str(kind_spec.label), Rect2(x, 150, 330, 26), 16, Color("d7cfb5"))
		var hover_pin := _add_pin(stage, Vector2(x, 188), "hover_%d" % index, str(kind_spec.name), str(kind_spec.kind), "available", true, false, 0.3)
		hover_pin.set_external_hover(true)
		var selected_pin := _add_pin(stage, Vector2(x, 382), "selected_%d" % index, str(kind_spec.name), str(kind_spec.kind), "available", true, true, 0.3)
		_add_label(stage, "SELECTED / 类型色框 + 类型色后纸", Rect2(x, 350, 350, 26), 14, Color("d7cfb5"))

	var state_specs := [
		{"label": "ASSIGNED / 已派遣", "state": "assigned", "enabled": true, "kind": "chain"},
		{"label": "URGENT / 紧急", "state": "urgent", "enabled": true, "kind": "temp"},
		{"label": "LOCKED / 锁定", "state": "locked", "enabled": false, "kind": "hidden"},
		{"label": "FOCUS / 键盘焦点", "state": "available", "enabled": true, "kind": "permanent", "focus": true},
	]
	for index in range(state_specs.size()):
		var state_spec: Dictionary = state_specs[index]
		var x := 72.0 + float(index) * 450.0
		_add_label(stage, str(state_spec.label), Rect2(x, 590, 330, 26), 16, Color("d7cfb5"))
		var pin := _add_pin(stage, Vector2(x, 628), "state_%d" % index, "固定状态美术 badge", str(state_spec.kind), str(state_spec.state), bool(state_spec.enabled), false, 0.3)
		if bool(state_spec.get("focus", false)):
			pin.call_deferred("grab_focus")

	_add_label(stage, "实现边界：图钉头与名称横条是同一张透明状态图；Godot 只叠动态 icon / 文字并做 alpha 过渡。", Rect2(72, 900, 1740, 40), 17, Color("68a37d"))
	await _settle_frames(10)
	await _save_png(viewport, "%s/03-runtime-state-and-kind-matrix-v7.png" % OUT_DIR)
	await _dispose_viewport(viewport)


func _capture_runtime_animation() -> void:
	var viewport := _make_viewport()
	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1920, 1080)
	await _settle_frames(4)
	board.render(_fixture_payload(1, "", false))
	await _settle_frames(8)
	var pin := board.find_child("EventPin_event_0", true, false) as Control
	if pin == null:
		push_error("Missing production pin for runtime animation")
		await _dispose_viewport(viewport)
		return
	var frame_index := 0
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 14)
	pin.call("set_external_hover", true)
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 8)
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 16)
	pin.call("set_selected", true, true)
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 8)
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 22)
	pin.call("set_selected", false, true)
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 6)
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 10)
	pin.call("set_external_hover", false)
	frame_index = await _hold_animation_frames(viewport, pin, frame_index, 8)
	await _hold_animation_frames(viewport, pin, frame_index, 12)
	await _dispose_viewport(viewport)


func _hold_animation_frames(viewport: SubViewport, pin: Control, frame_index: int, count: int) -> int:
	for _index in range(count):
		await process_frame
		viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
		await RenderingServer.frame_post_draw
		var image := viewport.get_texture().get_image()
		var origin := Vector2i(roundi(pin.global_position.x - 40.0), roundi(pin.global_position.y - 12.0))
		var cropped := image.get_region(Rect2i(origin, Vector2i(390, 124)))
		cropped.save_png(ProjectSettings.globalize_path("%s/frame_%03d.png" % [FRAME_DIR, frame_index]))
		frame_index += 1
	return frame_index


func _add_pin(parent: Control, position_value: Vector2, task_id: String, title: String, kind: String, state: String, enabled: bool, selected: bool, ratio_x: float) -> Control:
	var pin := EventPin.new()
	pin.position = position_value
	pin.size = Vector2(72, 80)
	parent.add_child(pin)
	pin.configure({
		"id": task_id,
		"name": title,
		"kind": kind,
		"days": 2,
		"tone": "normal",
		"state": state,
		"enabled": enabled,
		"map_pos": {"x": ratio_x, "y": 0.5},
	}, selected)
	return pin


func _fixture_payload(event_count: int, selected_id: String, force_dense: bool) -> Dictionary:
	var nodes: Array = []
	for index in range(event_count):
		var task_id := "event_%d" % index
		nodes.append({
			"id": task_id,
			"name": "异常事件 %d" % [index + 1],
			"kind": "temp" if index == 2 else "chain" if index == 3 else "hidden" if index == 4 else "permanent",
			"days": 1 + index % 3,
			"type": "pop" if index == 2 else "occult" if index == 3 else "sci",
			"tone": "deadline" if index == 2 else "chain" if index == 3 else "locked" if index == 4 else "normal",
			"state": "urgent" if index == 2 else "assigned" if index == 3 else "locked" if index == 4 else "available",
			"enabled": index != 4,
			"map_pos": {"x": 0.5, "y": 0.5} if force_dense else {"x": 0.23 + 0.15 * index, "y": 0.34 + 0.12 * (index % 3)},
		})
	var selected_node: Dictionary = {}
	for node_value in nodes:
		if str(node_value.get("id", "")) == selected_id:
			selected_node = node_value
			break
	var selected_kind := str(selected_node.get("kind", ""))
	var selected_kind_label := "限时截稿" if selected_kind == "temp" else "连续追踪" if selected_kind == "chain" else "灵视异常" if selected_kind == "hidden" else "常驻调查"
	return {
		"region_title": "合同验证区",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": selected_id,
		"nodes": nodes,
		"node_title": str(selected_node.get("name", "选择一份事件档案")),
		"region_node_summary": "同一区域可以出现多个事件点；短签头部与名称横条使用同画布美术状态图，密集避让与任务 id 绑定保持不变。",
		"region_node_meta": "%s · 需求 洞察/推理 · %d天" % [selected_kind_label, int(selected_node.get("days", 0))] if not selected_id.is_empty() else "",
		"region_node_deadline": "截稿剩 2 天" if selected_kind == "temp" else "",
		"region_node_chain": "连续追踪：成功后出现后续线索" if selected_kind == "chain" else "失败会错过本周窗口" if selected_kind == "temp" else "",
		"region_node_risk_level": "中" if not selected_id.is_empty() else "",
		"region_node_recommendation": "建议：优先配置 洞察/推理；签批台复核达标率。" if not selected_id.is_empty() else "",
		"region_action_hint": "送至签批台配置骰池，本页不消耗天数。",
		"dispatch_open_enabled": not selected_id.is_empty(),
		"dispatch_open_text": "送至签批台" if not selected_id.is_empty() else "先选择任务",
	}


func _edge_payload() -> Dictionary:
	var payload := _fixture_payload(1, "event_0", false)
	payload.nodes[0].name = "右岸边界长标题事件"
	payload.nodes[0].kind = "chain"
	payload.nodes[0].state = "assigned"
	payload.nodes[0].map_pos = {"x": 0.945, "y": 0.22}
	payload.node_title = "右岸边界长标题事件"
	payload.region_node_summary = "这个状态同时验证右边缘左挂短签、标题省略，以及右侧 dossier 的风险等级与建议是否在选中后真实出现。"
	payload.region_node_meta = "连续追踪 · 需求 洞察/推理 · 1天"
	payload.region_node_deadline = ""
	payload.region_node_chain = "连续追踪：成功后出现后续线索"
	return payload


func _make_viewport() -> SubViewport:
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(1920, 1080)
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
	var error := image.save_png(ProjectSettings.globalize_path(path))
	if error != OK:
		push_error("Failed to save production v7 capture: %s" % error_string(error))


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
