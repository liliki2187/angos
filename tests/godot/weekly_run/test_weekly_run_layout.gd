extends SceneTree

const Content = preload("res://scenes/gameplay/weekly_run/content/WeeklyRunContent.gd")
const Systems = preload("res://scenes/gameplay/weekly_run/systems/WeeklyRunSystems.gd")

var _failures: Array[String] = []

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(1920, 1080)
	root.add_child(viewport)

	var packed := load("res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn") as PackedScene
	var scene := packed.instantiate() as Control
	viewport.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	scene.offset_left = 0.0
	scene.offset_top = 0.0
	scene.offset_right = 0.0
	scene.offset_bottom = 0.0

	await process_frame
	await process_frame

	_assert_layout(scene, viewport, "start")
	_assert_true(scene.get_node("RootMargin/RootVBox/PhaseHost/BriefingPhase").visible, "新开局必须显示独立 briefing phase。")
	_assert_scroll_text_width(scene.get_node("RootMargin/RootVBox/PhaseHost/BriefingPhase/RootVBox/ContentSplit/BriefingPanel/BriefingVBox/BriefingScroll") as Control, scene.get_node("RootMargin/RootVBox/PhaseHost/BriefingPhase/RootVBox/ContentSplit/BriefingPanel/BriefingVBox/BriefingScroll/Body") as Control, "briefing")

	scene._on_advance_phase_pressed()
	await process_frame
	await process_frame
	_assert_scroll_text_width(scene.get_node("RootMargin/RootVBox/PhaseHost/ExplorePhase/RootHBox/RightVBox/MissionPanel/MissionVBox/MissionScroll") as Control, scene.get_node("RootMargin/RootVBox/PhaseHost/ExplorePhase/RootHBox/RightVBox/MissionPanel/MissionVBox/MissionScroll/Body") as Control, "mission")
	var state = scene.run_state
	var inventory = scene.material_inventory
	var material := {
		"id": "layout_probe_material",
		"title": "布局探针素材",
		"type": "sci",
		"tier": 3,
		"source_region": "北美禁区带",
		"source_node": "51 区外围公路",
		"risk_flags": [],
	}
	inventory.ingest_material(material)
	state.new_material_ids.append("layout_probe_material")
	scene._enter_editorial_phase()

	var slot_assignment := {}
	var article_index := 0
	for slot in Content.SLOT_DATA:
		if article_index < state.article_candidates.size():
			slot_assignment[str(slot.id)] = int(state.article_candidates[article_index].id)
		else:
			slot_assignment[str(slot.id)] = -1
		article_index += 1
	Systems.publish_issue(state, slot_assignment)
	Systems.settle_published_issue(state, inventory)
	scene._refresh_all()
	await process_frame
	await process_frame
	_assert_scroll_text_width(scene.get_node("RootMargin/RootVBox/PhaseHost/EditorialPhase/RootVBox/EditorialColumns/StatsPanel/StatsVBox/StatsScroll") as Control, scene.get_node("RootMargin/RootVBox/PhaseHost/EditorialPhase/RootVBox/EditorialColumns/StatsPanel/StatsVBox/StatsScroll/Body") as Control, "stats")
	scene._next_week()

	await process_frame
	await process_frame

	_assert_layout(scene, viewport, "next_week")
	_assert_true(scene.get_node("RootMargin/RootVBox/PhaseHost/BriefingPhase").visible, "进入下一周后仍应回到 briefing phase，而不是被 explore 壳子顶开。")
	_finish()

func _assert_layout(scene: Control, viewport: SubViewport, stage_label: String) -> void:
	var root_margin := scene.get_node("RootMargin") as Control
	var phase_host := scene.get_node("RootMargin/RootVBox/PhaseHost") as Control
	_assert_true(root_margin.size.y <= float(viewport.size.y), "%s 阶段下 RootMargin 不应超过视口高度。" % stage_label)
	_assert_true(phase_host.position.y + phase_host.size.y <= root_margin.position.y + root_margin.size.y + 0.5, "%s 阶段下 PhaseHost 必须落在 RootMargin 内。" % stage_label)

func _assert_scroll_text_width(scroll: Control, body: Control, stage_label: String) -> void:
	_assert_true(body.size.x >= scroll.size.x - 4.0, "%s 阶段下滚动文本内容宽度不应退化到左侧窄列。" % stage_label)

func _assert_true(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	_failures.append(message)

func _finish() -> void:
	if _failures.is_empty():
		print("test_weekly_run_layout.gd OK")
		quit(0)
		return
	print("test_weekly_run_layout.gd FAILURES=%d" % _failures.size())
	quit(1)
