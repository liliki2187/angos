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
	var explore_phase := scene.get_node("RootMargin/RootVBox/PhaseHost/ExplorePhase") as Control
	var world_map_assembly := explore_phase.call("get_world_map_assembly") as Control
	_assert_true(world_map_assembly != null, "进入探索后应挂载独立 WMW 世界地图总装。")
	_assert_visible_inside(world_map_assembly, scene, "world_map_assembly")
	_assert_true(not explore_phase.get_node("RootVBox").visible, "独立世界地图总装启用后应隐藏旧 GLOBAL CHANNEL 宿主。")
	var world_snapshot: Dictionary = world_map_assembly.call("get_state_snapshot")
	_assert_true(str(world_snapshot.get("selected_region_id", "")) == "us", "世界地图总装默认应选择北美区域。")
	scene._on_region_pressed("east_asia")
	await process_frame
	await process_frame
	world_snapshot = world_map_assembly.call("get_state_snapshot")
	_assert_true(str(world_snapshot.get("selected_region_id", "")) == "east_asia", "锁定区域选择仍应同步到世界地图总装。")
	scene._on_region_pressed("us")
	await process_frame
	await process_frame
	scene._on_enter_region_requested()
	await process_frame
	await process_frame
	var region_board := explore_phase.get_node_or_null("RegionTaskBoardV2") as Control
	_assert_true(region_board != null, "进入区域后应挂载资产化区域任务台。")
	_assert_visible_inside(region_board, scene, "region_task_board")
	_assert_true(not explore_phase.get_node("RootVBox").visible, "资产化区域任务台启用后应隐藏旧区域节点布局。")
	scene._on_node_pressed("m330")
	await process_frame
	await process_frame
	_assert_true(bool(region_board.call("is_dispatch_enabled")), "选择区域任务后应启用派遣入口。")
	scene._on_open_dispatch_requested()
	await process_frame
	await process_frame
	_assert_true(explore_phase.get_node("RootVBox/DispatchView").visible, "进入签批后应显示独立派遣签批台。")
	_assert_visible_inside(explore_phase.get_node("RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel") as Control, explore_phase, "dispatch_review_panel")
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
	await process_frame
	await process_frame
	var editorial_phase := scene.get_node("RootMargin/RootVBox/PhaseHost/EditorialPhase") as Control
	_assert_true(editorial_phase.visible, "进入编辑阶段后应显示资产化双页排版台。")
	var editorial_status := editorial_phase.find_child("EditorialStatusBar", true, false) as Control
	_assert_true(editorial_status.visible and editorial_status.size.x > 80.0 and editorial_status.size.y > 40.0, "编辑状态栏应可见并保持稳定尺寸。")
	_assert_visible_inside(editorial_phase.find_child("CandidatePool", true, false) as Control, editorial_phase, "editorial_candidates")
	_assert_visible_inside(editorial_phase.find_child("EditionWorkspace", true, false) as Control, editorial_phase, "editorial_edition")
	_assert_visible_inside(editorial_phase.find_child("SignoffPanel", true, false) as Control, editorial_phase, "editorial_signoff")

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
	var summary_phase := scene.get_node("RootMargin/RootVBox/PhaseHost/SummaryPhase") as Control
	_assert_true(summary_phase.visible, "发刊结算后应显示本周总结阶段。")
	_assert_scroll_text_width(summary_phase.get_node("RootVBox/SummaryPanel/SummaryVBox/SummaryScroll") as Control, summary_phase.get_node("RootVBox/SummaryPanel/SummaryVBox/SummaryScroll/Body") as Control, "summary")
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

func _assert_visible_inside(control: Control, parent: Control, stage_label: String) -> void:
	_assert_true(control.visible, "%s 必须可见。" % stage_label)
	_assert_true(control.size.x > 80.0 and control.size.y > 80.0, "%s 必须有稳定尺寸。" % stage_label)
	_assert_true(control.global_position.x >= parent.global_position.x - 0.5, "%s 左边界必须落在父容器内。" % stage_label)
	_assert_true(control.global_position.y >= parent.global_position.y - 0.5, "%s 上边界必须落在父容器内。" % stage_label)

func _assert_world_map_safe_zones(explore_phase: Control, stage_label: String) -> void:
	var detail_panel := explore_phase.get_node("RootVBox/WorldView/WorldDetailPanel") as Control
	var right_safe_limit := detail_panel.global_position.x + detail_panel.size.x - 64.0
	for path in [
		"RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldTicketVBox/WorldDeadlineTicket",
		"RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldTicketVBox/WorldChainTicket",
		"RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldCtaHint",
		"RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/EnterRegionBtn",
	]:
		var control := explore_phase.get_node(path) as Control
		_assert_true(control.global_position.x + control.size.x <= right_safe_limit + 0.5, "%s %s 不应进入右侧装饰禁区。" % [stage_label, control.name])

	var index_panel := explore_phase.get_node("RootVBox/WorldView/WorldIndexPanel") as Control
	var index_title := explore_phase.get_node("RootVBox/WorldView/WorldIndexPanel/WorldIndexVBox/WorldIndexTitle") as Control
	var index_subtitle := explore_phase.get_node("RootVBox/WorldView/WorldIndexPanel/WorldIndexVBox/WorldIndexSubtitle") as Control
	var index_footer := explore_phase.get_node("RootVBox/WorldView/WorldIndexPanel/WorldIndexVBox/WorldIndexFooter") as Control
	_assert_true(index_title.global_position.y >= index_panel.global_position.y + 52.0, "%s INDEX 标题必须避开顶部夹子和纸边。" % stage_label)
	_assert_true(index_subtitle.global_position.y >= index_panel.global_position.y + 78.0, "%s INDEX 副标题必须避开顶部夹子和标题。" % stage_label)
	_assert_true(index_footer.global_position.y <= index_panel.global_position.y + index_panel.size.y - 150.0, "%s INDEX 底部摘要必须避开纸张底边装饰。" % stage_label)

	var deadline_ticket := explore_phase.get_node("RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldTicketVBox/WorldDeadlineTicket") as Control
	var chain_ticket := explore_phase.get_node("RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldTicketVBox/WorldChainTicket") as Control
	var region_detail_text := explore_phase.get_node("RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/RegionDetailText") as Control
	var world_cta_hint := explore_phase.get_node("RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldCtaHint") as Control
	var enter_button := explore_phase.get_node("RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/EnterRegionBtn") as Control
	var log_chip_1 := explore_phase.get_node("RootVBox/WorldProofStrip/WorldProofHBox/WorldLogChip1") as Control
	var log_chip_2 := explore_phase.get_node("RootVBox/WorldProofStrip/WorldProofHBox/WorldLogChip2") as Control
	var log_chip_3 := explore_phase.get_node("RootVBox/WorldProofStrip/WorldProofHBox/WorldLogChip3") as Control
	_assert_style_margin(region_detail_text, "normal", SIDE_LEFT, 42.0, "%s Region detail text must avoid the left bookmark/tab art." % stage_label)
	_assert_style_margin(region_detail_text, "normal", SIDE_TOP, 112.0, "%s Region detail text must avoid the top bookmark and paper edge." % stage_label)
	_assert_style_margin(region_detail_text, "normal", SIDE_BOTTOM, 16.0, "%s Region detail text must avoid the lower paper trim." % stage_label)
	_assert_style_margin(world_cta_hint, "normal", SIDE_LEFT, 16.0, "%s CTA hint text must avoid the left label edge." % stage_label)
	_assert_style_margin(world_cta_hint, "normal", SIDE_TOP, 9.0, "%s CTA hint text must avoid the top label edge." % stage_label)
	_assert_style_margin(deadline_ticket, "normal", SIDE_LEFT, 100.0, "%s 红票文字必须避开左侧色块。" % stage_label)
	_assert_style_margin(deadline_ticket, "normal", SIDE_RIGHT, 60.0, "%s 红票文字必须避开右侧装饰。" % stage_label)
	_assert_style_margin(chain_ticket, "normal", SIDE_LEFT, 100.0, "%s 青票文字必须避开左侧色块。" % stage_label)
	_assert_style_margin(chain_ticket, "normal", SIDE_RIGHT, 60.0, "%s 青票文字必须避开右侧装饰。" % stage_label)
	_assert_style_margin(enter_button, "normal", SIDE_RIGHT, 80.0, "%s CTA 文字必须避开箭头和右侧装饰。" % stage_label)
	_assert_style_margin(enter_button, "normal", SIDE_BOTTOM, 16.0, "%s CTA text must stay above the lower trim and rivets." % stage_label)
	_assert_style_margin(enter_button, "disabled", SIDE_BOTTOM, 20.0, "%s disabled CTA text must stay above the lower trim and rivets." % stage_label)
	_assert_font_luma(enter_button, "font_disabled_color", 0.84, "%s disabled CTA text must keep enough contrast." % stage_label)
	for chip in [log_chip_1, log_chip_2, log_chip_3]:
		_assert_style_margin(chip, "normal", SIDE_LEFT, 120.0, "%s %s 文字必须避开左侧色块。" % [stage_label, chip.name])
		_assert_style_margin(chip, "normal", SIDE_RIGHT, 40.0, "%s %s 文字必须避开右侧装饰。" % [stage_label, chip.name])

func _assert_style_margin(control: Control, style_name: String, side: Side, minimum: float, message: String) -> void:
	var style := control.get_theme_stylebox(style_name)
	_assert_true(style != null, "%s 必须存在 stylebox。" % control.name)
	if style == null:
		return
	_assert_true(style.get_content_margin(side) >= minimum, message)

func _assert_font_luma(control: Control, color_name: String, minimum: float, message: String) -> void:
	var color := control.get_theme_color(color_name)
	var luma := color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722
	_assert_true(luma >= minimum, message)

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
