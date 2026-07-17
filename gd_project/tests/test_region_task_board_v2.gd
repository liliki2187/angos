extends SceneTree

const BoardV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd")

var _selected_signal_id := ""

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var board := BoardV2.new()
	root.add_child(board)
	board.position = Vector2.ZERO
	board.size = Vector2(1920, 1080)
	board.node_selected.connect(func(task_id: String) -> void: _selected_signal_id = task_id)
	await process_frame
	_assert(board.is_map_texture_loaded(), "board should load the clean map texture")

	board.render(_fixture_payload(0, ""))
	_assert(board.get_event_card_count() == 0, "zero events should create zero cards")
	_assert(board.get_event_pin_count() == 0, "zero events should create zero pins")
	_assert(board.get_visible_pin_label_count() == 0, "zero events should show zero pin labels")
	_assert(not board.is_dispatch_enabled(), "dispatch should be disabled without selection")

	board.render(_fixture_payload(1, "event_0"))
	_assert(board.get_event_card_count() == 1, "one event should create one card")
	_assert(board.get_event_pin_count() == 1, "one event should create one pin")
	_assert(board.get_event_card_task_ids() == board.get_event_pin_task_ids(), "one-event card and pin ids should match")
	_assert(board.get_selected_task_id() == "event_0", "selected event id should be preserved")
	_assert(board.get_visible_pin_label_count() == 1, "only the selected pin label should persist")
	_assert(board.is_dispatch_enabled(), "dispatch should enable for selected event")
	_assert(board.get_dossier_summary_text().find("用于压力测试") >= 0, "dossier should receive runtime summary text")

	board.render(_fixture_payload(5, "event_3"))
	_assert(board.get_event_card_count() == 5, "N events should create N cards")
	_assert(board.get_event_pin_count() == 5, "N events should create N pins")
	_assert(board.get_event_card_task_ids() == board.get_event_pin_task_ids(), "N-event card and pin ids should match")
	_assert(not board.is_advance_day_enabled(), "advance day must stay disabled until gameplay logic exists")
	board.call("_on_event_pressed", "event_4")
	_assert(_selected_signal_id == "event_4", "event selection should emit the source task id")

	var dense_payload := _fixture_payload(5, "event_2")
	for item in dense_payload.nodes:
		item.map_pos = {"x": 0.5, "y": 0.5}
	board.render(dense_payload)
	var dense_positions := board.get_pin_reference_positions()
	var unique_positions: Dictionary = {}
	for position in dense_positions:
		unique_positions["%.1f,%.1f" % [position.x, position.y]] = true
	_assert(unique_positions.size() == 5, "dense event coordinates should resolve to five distinct hit targets")
	_assert(board.get_visible_pin_label_count() == 1, "dense state should still keep only one persistent label")
	_assert(not board.has_visible_label_pin_overlap(8.0), "selected dense label should keep 8px clearance from every other visible pin")
	_assert(board.get_cluster_marker_count() == 0, "five dense events should remain individually available")

	var cluster_payload := _fixture_payload(8, "")
	for item in cluster_payload.nodes:
		item.map_pos = {"x": 0.5, "y": 0.5}
	board.render(cluster_payload)
	_assert(board.get_event_pin_count() == 8, "clustered events should keep all task ids bound to runtime pins")
	_assert(board.get_cluster_marker_count() == 1, "eight events in one dense cell should use one runtime cluster marker")
	_assert(board.get_visible_pin_label_count() == 0, "collapsed cluster should not leak hidden pin labels")
	var cluster_keys := board.get_cluster_keys()
	_assert(cluster_keys.size() == 1, "cluster should expose one stable runtime key")
	board.call("_toggle_cluster", cluster_keys[0])
	_assert(board.is_cluster_expanded(cluster_keys[0]), "cluster marker should expand on activation")

	cluster_payload.selected_node_id = "event_2"
	board.render(cluster_payload)
	cluster_keys = board.get_cluster_keys()
	_assert(board.is_cluster_expanded(cluster_keys[0]), "cluster containing the selected event should start expanded")
	_assert(board.get_visible_pin_label_count() == 1, "expanded selected cluster should keep one persistent label")

	for line_count in [7, 8, 9]:
		var text_stress_payload := _fixture_payload(1, "event_0")
		var summary_lines: Array[String] = []
		for line_index in range(line_count):
			summary_lines.append("第 %d 行：用于验证长摘要不会侵入底部派遣入口。" % [line_index + 1])
		text_stress_payload.region_node_summary = "\n".join(summary_lines)
		board.render(text_stress_payload)
		_assert(board.get_dossier_summary_text().count("\n") + 1 == line_count, "%d-line summary should remain intact" % line_count)
		_assert(board.is_dispatch_enabled(), "%d-line summary should not disable or cover the dispatch contract" % line_count)

	print("test_region_task_board_v2.gd OK")
	quit(0)

func _fixture_payload(event_count: int, selected_id: String) -> Dictionary:
	var nodes: Array = []
	for index in range(event_count):
		var task_id := "event_%d" % index
		nodes.append({
			"id": task_id,
			"name": "事件 %d" % [index + 1],
			"kind": "temp" if index == 2 else "chain" if index == 3 else "permanent",
			"days": 1 + index % 3,
			"type": "pop" if index == 2 else "occult" if index == 3 else "sci",
			"tone": "deadline" if index == 2 else "chain" if index == 3 else "normal",
			"selected": task_id == selected_id,
			"enabled": true,
			"map_pos": {"x": 0.16 + 0.16 * index, "y": 0.24 + 0.12 * (index % 3)},
		})
	return {
		"region_title": "合同测试区",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": selected_id,
		"nodes": nodes,
		"node_title": "事件档案" if selected_id != "" else "选择一份事件档案",
		"region_node_summary": "用于压力测试的长摘要：同一区域允许出现多个事件，右侧摘要必须保留足够的连续文字空间。",
		"region_node_meta": "常驻/纪实 · 需求 洞察/推理 · 2天",
		"region_node_deadline": "截稿剩 2 天" if selected_id != "" else "",
		"region_node_chain": "连续追踪：成功后出现后续线索" if selected_id != "" else "",
		"region_action_hint": "送至签批台配置骰池，本页不消耗天数。",
		"dispatch_open_enabled": selected_id != "",
		"dispatch_open_text": "送至签批台" if selected_id != "" else "先选择任务",
	}

func _assert(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	quit(1)
