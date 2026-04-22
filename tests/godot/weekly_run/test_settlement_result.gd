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
	Systems.start_explore(state)

	material_inventory.ingest_material({
		"id": "smoke_material_1",
		"title": "测试素材 · 头版主稿",
		"type": "sci",
		"tier": 3,
		"source_region": "北美禁区带",
		"source_node": "51 区外围公路",
		"risk_flags": [],
	})
	state.new_material_ids.append("smoke_material_1")

	Systems.enter_editorial(state, material_inventory)
	var slot_assignment := _fill_first_slots(state)
	var preview := Systems.publish_issue(state, slot_assignment)
	var result := Systems.settle_published_issue(state, material_inventory)

	_assert_true(not preview.is_empty(), "发刊前必须生成 settlement_preview。")
	_assert_true(not state.settlement_result.is_empty(), "结算后必须写入 settlement_result。")
	_assert_true(state.next_week_hooks.has("profit_band"), "结算后必须生成 next_week_hooks。")
	_assert_true(result.has("next_subscribers"), "结算结果必须包含 next_subscribers。")
	_assert_true(state.subscribers == int(result.next_subscribers), "长期订阅值必须和 settlement_result 对齐。")

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
		print("test_settlement_result.gd OK")
		quit(0)
		return
	print("test_settlement_result.gd FAILURES=%d" % _failures.size())
	quit(1)
