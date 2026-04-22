extends SceneTree

const Content = preload("res://scenes/gameplay/weekly_run/content/WeeklyRunContent.gd")
const WeeklyMaterialInventory = preload("res://scenes/gameplay/weekly_run/materials/WeeklyMaterialInventory.gd")
const Systems = preload("res://scenes/gameplay/weekly_run/systems/WeeklyRunSystems.gd")
const WeeklyRunState = preload("res://scenes/gameplay/weekly_run/state/WeeklyRunState.gd")

var _failures: Array[String] = []

func _init() -> void:
	randomize()
	var state := WeeklyRunState.new()
	var material_inventory := WeeklyMaterialInventory.new()
	Systems.initialize_new_run(state, material_inventory)
	_assert_true(state.current_phase == "briefing", "新开局必须先进入 briefing。")

	Systems.start_explore(state)
	_assert_true(state.current_phase == "explore", "确认简报后必须进入 explore。")

	Systems.enter_editorial(state, material_inventory)
	_assert_true(state.current_phase == "editorial", "探索结束后必须进入 editorial。")

	var slot_assignment := _fill_first_slots(state)
	Systems.publish_issue(state, slot_assignment)
	Systems.settle_published_issue(state, material_inventory)
	_assert_true(state.current_phase == "summary", "发刊结算后必须进入 summary。")
	_assert_true(not state.published_issue.is_empty(), "summary 前必须冻结 published_issue。")

	Systems.begin_next_week(state)
	_assert_true(state.week == 2, "进入下一周后周数必须加一。")
	_assert_true(state.current_phase == "briefing", "下一周必须重新进入 briefing。")

	_finish()

func _fill_first_slots(state: WeeklyRunState) -> Dictionary:
	var assignment := {}
	var article_index := 0
	for slot in Content.SLOT_DATA:
		if article_index < state.article_candidates.size():
			assignment[str(slot.id)] = int(state.article_candidates[article_index].id)
		else:
			assignment[str(slot.id)] = -1
		article_index += 1
	return assignment

func _assert_true(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	_failures.append(message)

func _finish() -> void:
	if _failures.is_empty():
		print("test_phase_flow.gd OK")
		quit(0)
		return
	print("test_phase_flow.gd FAILURES=%d" % _failures.size())
	quit(1)
