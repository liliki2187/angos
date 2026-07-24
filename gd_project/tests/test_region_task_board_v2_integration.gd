extends SceneTree

const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	_assert(packed != null, "weekly run scene should load")
	var scene := packed.instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_TOP_LEFT)
	scene.size = Vector2(1920, 1080)
	await _settle_frames(3)

	scene._on_advance_phase_pressed()
	await _settle_frames(3)
	scene._on_enter_region_requested()
	await _settle_frames(4)
	_assert(str(scene.explore_view_mode) == "region", "main flow should enter the region board")
	var board = scene.explore_phase.get_node_or_null("RegionTaskBoardV2")
	_assert(board != null, "region v2 board should be mounted")
	_assert(board.visible, "region v2 board should be visible")
	_assert(not scene.explore_phase.root_vbox.visible, "legacy region layout should be hidden")
	_assert(is_equal_approx(scene.root_margin.offset_left, 0.0), "deep explore should use the full desktop width")
	_assert(board.size.is_equal_approx(Vector2(1920, 1080)), "region board should receive the full 1920x1080 reference canvas")
	_assert(board.get_event_pin_count() == 4, "current North America fixture should expose four visible event pins")

	board.call("_on_event_pressed", "m330")
	await _settle_frames(4)
	_assert(str(scene.selected_node_id) == "m330", "board event signal should update the game selection")
	_assert(board.get_selected_task_id() == "m330", "board should rerender the selected event")
	_assert(board.get_dossier_title_text() == "M330 末班车空白段", "dossier title should come from the selected m330 node")
	_assert(board.get_dossier_meta_text().find("追踪") >= 0 and board.get_dossier_meta_text().find("2天") >= 0, "dossier type and duration should match the selected m330 node")
	_assert(board.get_dossier_risk_text().find("连续追踪") >= 0 and board.get_dossier_risk_text().find("截稿") < 0, "dossier risk basis should match the selected chain node without stale deadline data")
	_assert(board.get_dossier_risk_text().begins_with("风险等级："), "selected production dossier should show the calculated risk level")
	_assert(board.get_dossier_recommendation_text().begins_with("建议："), "selected production dossier should show a staffing recommendation")
	_assert(board.is_dispatch_enabled(), "dispatch CTA should enable after selection")
	var dispatch_button := board.find_child("DispatchButton", true, false) as Button
	_assert(dispatch_button != null, "dispatch button should be discoverable")
	dispatch_button.pressed.emit()
	await _settle_frames(4)
	_assert(str(scene.explore_view_mode) == "dispatch", "dispatch CTA should open the existing dispatch flow")
	_assert(not board.visible, "region board should hide after entering dispatch")
	_assert(is_equal_approx(scene.root_margin.offset_left, 24.0), "existing dispatch layout should keep its original outer margin")

	print("test_region_task_board_v2_integration.gd OK")
	quit(0)

func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _assert(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	quit(1)
