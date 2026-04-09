extends Control

const Content = preload("res://scenes/gameplay/weekly_run/content/WeeklyRunContent.gd")
const WeeklyMaterialInventory = preload("res://scenes/gameplay/weekly_run/materials/WeeklyMaterialInventory.gd")
const MetricCardScene = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunMetricCard.tscn")
const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")
const BriefingPhaseScene = preload("res://scenes/gameplay/weekly_run/phases/WeeklyRunBriefingPhase.tscn")
const ExplorePhaseScene = preload("res://scenes/gameplay/weekly_run/phases/WeeklyRunExplorePhase.tscn")
const EditorialPhaseScene = preload("res://scenes/gameplay/weekly_run/phases/WeeklyRunEditorialPhase.tscn")
const SummaryPhaseScene = preload("res://scenes/gameplay/weekly_run/phases/WeeklyRunSummaryPhase.tscn")
const Systems = preload("res://scenes/gameplay/weekly_run/systems/WeeklyRunSystems.gd")
const WeeklyRunState = preload("res://scenes/gameplay/weekly_run/state/WeeklyRunState.gd")

@onready var header_panel: PanelContainer = $RootMargin/RootVBox/HeaderPanel
@onready var back_btn: Button = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/BackBtn
@onready var macro_bar: HBoxContainer = $RootMargin/RootVBox/MacroBar
@onready var week_label: Label = $RootMargin/RootVBox/WeekBar/WeekInfo/WeekLabel
@onready var day_label: Label = $RootMargin/RootVBox/WeekBar/WeekInfo/DayLabel
@onready var end_week_btn: Button = $RootMargin/RootVBox/WeekBar/EndWeekBtn
@onready var phase_host: Control = $RootMargin/RootVBox/PhaseHost

var run_state := WeeklyRunState.new()
var material_inventory := WeeklyMaterialInventory.new()
var filter_state := {"sci": true, "occult": true, "pop": true}
var selected_region_id := ""
var selected_node_id := ""
var selected_article_id := -1
var selected_staff_ids: Array[String] = []

var briefing_phase
var explore_phase
var editorial_phase
var summary_phase

func _ready() -> void:
	randomize()
	_mount_phase_scenes()
	_apply_shell_theme()
	_connect_shell_signals()
	_start_new_run()

func _mount_phase_scenes() -> void:
	briefing_phase = BriefingPhaseScene.instantiate()
	briefing_phase.name = "BriefingPhase"
	_mount_phase_scene(briefing_phase)
	explore_phase = ExplorePhaseScene.instantiate()
	explore_phase.name = "ExplorePhase"
	_mount_phase_scene(explore_phase)
	editorial_phase = EditorialPhaseScene.instantiate()
	editorial_phase.name = "EditorialPhase"
	_mount_phase_scene(editorial_phase)
	summary_phase = SummaryPhaseScene.instantiate()
	summary_phase.name = "SummaryPhase"
	_mount_phase_scene(summary_phase)

func _mount_phase_scene(phase: Control) -> void:
	phase_host.add_child(phase)
	phase.set_anchors_preset(Control.PRESET_FULL_RECT)
	phase.offset_left = 0.0
	phase.offset_top = 0.0
	phase.offset_right = 0.0
	phase.offset_bottom = 0.0
	phase.visible = false

func _apply_shell_theme() -> void:
	UiStyle.apply_panel_style(header_panel)
	UiStyle.apply_button_style(back_btn, false, true)
	UiStyle.apply_button_style(end_week_btn, true, true)

func _connect_shell_signals() -> void:
	back_btn.pressed.connect(_on_back_pressed)
	end_week_btn.pressed.connect(_on_advance_phase_pressed)
	explore_phase.connect("filter_toggled", Callable(self, "_on_filter_pressed"))
	explore_phase.connect("region_selected", Callable(self, "_on_region_pressed"))
	explore_phase.connect("node_selected", Callable(self, "_on_node_pressed"))
	explore_phase.connect("staff_toggled", Callable(self, "_toggle_staff"))
	explore_phase.connect("execute_requested", Callable(self, "_on_execute_pressed"))
	editorial_phase.connect("article_selected", Callable(self, "_on_article_selected"))
	editorial_phase.connect("slot_selected", Callable(self, "_place_article_in_slot"))
	editorial_phase.connect("clear_layout_requested", Callable(self, "_clear_layout"))
	editorial_phase.connect("settle_requested", Callable(self, "_settle_issue"))
	summary_phase.connect("next_week_requested", Callable(self, "_next_week"))

func _on_back_pressed() -> void:
	get_tree().change_scene_to_file(str(Globals.scene_paths.get("main_menu", "res://scenes/ui/main_menu/MainMenu.tscn")))

func _start_new_run() -> void:
	run_state = WeeklyRunState.new()
	material_inventory = WeeklyMaterialInventory.new()
	filter_state = {"sci": true, "occult": true, "pop": true}
	selected_node_id = ""
	selected_article_id = -1
	selected_staff_ids.clear()
	Systems.initialize_new_run(run_state, material_inventory)
	selected_region_id = _default_region_id()
	_refresh_all()

func _refresh_all() -> void:
	var started_at := _log_flow_start("_refresh_all", "phase=%s selected_node=%s" % [run_state.current_phase, selected_node_id])
	_ensure_valid_region_selection()
	_ensure_valid_node_selection()
	week_label.text = "第 %d 周 · %s" % [run_state.week, _phase_label(run_state.current_phase)]
	day_label.text = "剩余 %d / %d 天 · 订阅 %d · editorialProfile %.2f" % [run_state.remaining_days, Content.WEEK_DAYS, run_state.subscribers, run_state.editorial_profile]
	_refresh_phase_actions()
	_refresh_macro_bar()
	_refresh_phase_views()
	_log_flow_end("_refresh_all", started_at, "phase=%s selected_node=%s" % [run_state.current_phase, selected_node_id])

func _refresh_phase_actions() -> void:
	match run_state.current_phase:
		"briefing":
			end_week_btn.visible = true
			end_week_btn.text = "确认简报 · 进入探索"
			UiStyle.apply_button_style(end_week_btn, true, true)
		"explore":
			end_week_btn.visible = true
			end_week_btn.text = "结束探索 · 进入编辑部"
			UiStyle.apply_button_style(end_week_btn, true, true)
		_:
			end_week_btn.visible = false

func _refresh_macro_bar() -> void:
	var started_at := _log_flow_start("_refresh_macro_bar", "items=%d" % Content.MACRO_LABELS.size())
	_clear_container(macro_bar)
	for item in Content.MACRO_LABELS:
		var card := MetricCardScene.instantiate()
		macro_bar.add_child(card)
		card.bind(str(item.label), str(run_state.macro_stats[item.key]))
	_log_flow_end("_refresh_macro_bar", started_at, "items=%d" % Content.MACRO_LABELS.size())

func _refresh_phase_views() -> void:
	var started_at := _log_flow_start("_refresh_phase_views", "phase=%s" % run_state.current_phase)
	briefing_phase.visible = run_state.current_phase == "briefing"
	explore_phase.visible = run_state.current_phase == "explore"
	editorial_phase.visible = run_state.current_phase == "editorial"
	summary_phase.visible = run_state.current_phase == "summary"

	if briefing_phase.visible:
		briefing_phase.render(_build_briefing_payload())
	if explore_phase.visible:
		explore_phase.render(_build_explore_payload())
	if editorial_phase.visible:
		editorial_phase.render(_build_editorial_payload())
	if summary_phase.visible:
		summary_phase.render(_build_summary_payload())
	_log_flow_end("_refresh_phase_views", started_at, "phase=%s" % run_state.current_phase)

func _build_briefing_payload() -> Dictionary:
	var tasks: Array = []
	for task in run_state.active_tasks:
		tasks.append({
			"title": "任务",
			"body": str(task.summary),
		})
	if tasks.is_empty():
		tasks.append({
			"title": "任务",
			"body": "本周暂无额外任务。",
		})

	var hooks: Array = []
	if run_state.next_week_hooks.is_empty():
		hooks.append({
			"title": "状态",
			"body": "上一期没有额外余波。",
		})
	else:
		hooks.append({
			"title": "利润档",
			"body": str(run_state.next_week_hooks.get("profit_band", "neutral")),
		})
		if run_state.next_week_hooks.has("dominant_axis"):
			hooks.append({
				"title": "本期倾向",
				"body": str(run_state.next_week_hooks.get("dominant_axis", "mixed")),
			})
		if run_state.next_week_hooks.has("empty_slots"):
			hooks.append({
				"title": "空版记录",
				"body": "%d 个空版位" % int(run_state.next_week_hooks.get("empty_slots", 0)),
			})

	var opportunities: Array = []
	for region in Content.REGION_DATA:
		if not Systems.is_region_unlocked(run_state, region):
			continue
		var node_names: Array = []
		for node in region.nodes:
			if Systems.is_node_visible(run_state, node):
				node_names.append(str(node.name))
		opportunities.append({
			"title": str(region.name),
			"body": "可见机会：%s" % (_join_strings(node_names, " / ") if not node_names.is_empty() else "当前没有可见节点。"),
		})
	if opportunities.is_empty():
		opportunities.append({
			"title": "机会概览",
			"body": "当前没有可见机会。",
		})

	return {
		"briefing_text": "[b]第 %d 周开场[/b]\n\n%s" % [run_state.week, Content.get_briefing_text(run_state.briefing_event_id)],
		"tasks": tasks,
		"hooks": hooks,
		"opportunities": opportunities,
	}

func _build_explore_payload() -> Dictionary:
	var started_at := _log_flow_start("_build_explore_payload", "selected_region=%s selected_node=%s" % [selected_region_id, selected_node_id])
	var regions: Array = []
	for region in Content.REGION_DATA:
		regions.append({
			"id": str(region.id),
			"text": "%s\n%s" % [str(region.name), str(region.hint)],
			"selected": selected_region_id == str(region.id),
			"enabled": Systems.is_region_unlocked(run_state, region),
			"min_height": 72.0,
		})

	var nodes: Array = []
	var region := _get_selected_region()
	var region_hint := "请选择区域"
	if not region.is_empty():
		region_hint = "%s · %s" % [str(region.name), str(region.hint)]
		for node in region.nodes:
			if not Systems.is_node_visible(run_state, node):
				continue
			if not bool(filter_state.get(str(node.type), true)):
				continue
			var availability := _get_node_availability(node)
			nodes.append({
				"id": str(node.id),
				"text": "%s · %s\n耗时 %d 天 · %s · 对抗 %d\n%s" % [
					str(node.name),
					str(node.kind),
					int(node.days),
					str(node.difficulty),
					int(node.enemy),
					str(availability.reason),
				],
				"selected": selected_node_id == str(node.id),
				"enabled": bool(availability.enabled),
				"min_height": 88.0,
			})

	var staff: Array = []
	for staff_data in Content.STAFF_POOL:
		staff.append({
			"id": str(staff_data.id),
			"text": "%s · %s\n探索 %d  洞察 %d  诡思 %d\n生存 %d  理性 %d  社交 %d" % [
				str(staff_data.name),
				str(staff_data.role),
				int(staff_data.attrs.explore),
				int(staff_data.attrs.insight),
				int(staff_data.attrs.occult),
				int(staff_data.attrs.survival),
				int(staff_data.attrs.reason),
				int(staff_data.attrs.social),
			],
			"selected": selected_staff_ids.has(str(staff_data.id)),
			"enabled": true,
			"min_height": 106.0,
		})

	var materials: Array = []
	for material in material_inventory.get_materials_by_ids(run_state.new_material_ids):
		materials.append({
			"title": str(material.title),
			"body": "%s · tier %d · %s" % [
				Content.TAG_LABELS.get(str(material.type), str(material.type)),
				int(material.tier),
				str(material.source_region),
			],
		})
	if materials.is_empty():
		materials.append({
			"title": "素材库存",
			"body": "本周还没有新增素材。",
		})

	var logs: Array = []
	for entry in run_state.log_entries:
		logs.append({
			"title": "",
			"body": str(entry),
			"accent": Color(0.64, 0.70, 0.78, 1.0),
		})
	if logs.is_empty():
		logs.append({
			"title": "",
			"body": "还没有探索日志。",
			"accent": Color(0.64, 0.70, 0.78, 1.0),
		})

	var mission_payload := _build_mission_payload()
	var payload := {
		"filters": filter_state.duplicate(true),
		"regions": regions,
		"region_hint": region_hint,
		"nodes": nodes,
		"staff": staff,
		"selected_staff_text": "已选择：%d / 3" % selected_staff_ids.size(),
		"materials": materials,
		"logs": logs,
		"mission_summary": mission_payload.summary,
		"probability_text": mission_payload.probability,
		"dice_text": mission_payload.dice,
		"result_text": mission_payload.result,
		"result_color": mission_payload.color,
		"execute_enabled": mission_payload.execute_enabled,
	}
	_log_flow_end("_build_explore_payload", started_at, "regions=%d nodes=%d staff=%d materials=%d logs=%d" % [regions.size(), nodes.size(), staff.size(), materials.size(), logs.size()])
	return payload

func _build_mission_payload() -> Dictionary:
	var default_payload := {
		"summary": "从左侧区域与节点列表中选中一个外采目标。",
		"probability": "理论结果：等待选点",
		"dice": "",
		"result": "等待执行",
		"color": Color(0.88, 0.76, 0.36, 1.0),
		"execute_enabled": false,
	}
	var node := _get_selected_node()
	if node.is_empty():
		return default_payload

	var totals := _get_selected_staff_totals()
	var needs: Array = []
	for key in node.need.keys():
		needs.append("%s %d" % [Content.ATTR_LABELS.get(str(key), str(key)), int(node.need[key])])
	var probabilities := Systems.calculate_node_probabilities(node, totals)
	var availability := _get_node_availability(node)
	default_payload.summary = "[b]%s[/b]\n%s\n\n[color=#d8c8a2]需求：%s[/color]\n[color=#9fb3c7]当前派遣合计：探索 %d / 洞察 %d / 诡思 %d / 生存 %d / 理性 %d / 社交 %d[/color]\n[color=#8fa4bc]%s[/color]" % [
		str(node.name),
		str(node.description),
		_join_strings(needs, " · "),
		int(totals.explore),
		int(totals.insight),
		int(totals.occult),
		int(totals.survival),
		int(totals.reason),
		int(totals.social),
		str(node.risk_text),
	]
	default_payload.probability = "理论结果：大成功 %.0f%% · 小成功 %.0f%% · 失败 %.0f%%" % [
		float(probabilities.major) * 100.0,
		float(probabilities.minor) * 100.0,
		float(probabilities.fail) * 100.0,
	]
	default_payload.execute_enabled = bool(availability.enabled)

	if not run_state.last_dispatch_roll.is_empty() and str(run_state.last_dispatch_roll.get("node_id", "")) == str(node.id):
		default_payload.dice = _format_roll_text(run_state.last_dispatch_roll)
		default_payload.result = _build_roll_result_text(run_state.last_dispatch_roll)
		default_payload.color = _build_roll_result_color(run_state.last_dispatch_roll)
	return default_payload

func _build_editorial_payload() -> Dictionary:
	var articles: Array = []
	for article in run_state.article_candidates:
		var article_id := int(article.id)
		articles.append({
			"id": article_id,
			"text": "%s\n%s · %s · base %d" % [
				str(article.title),
				_join_strings(article.tags, " / "),
				str(article.quality),
				int(article.base_value),
			],
			"selected": selected_article_id == article_id,
			"enabled": not _is_article_placed(article_id),
			"min_height": 88.0,
		})

	var slots: Array = []
	for slot in Content.SLOT_DATA:
		var article := _get_article_by_id(int(run_state.slot_assignment.get(str(slot.id), -1)))
		var slot_text := ""
		if article.is_empty():
			slot_text = "%s · x%.2f\n%s\n点击这里放置当前选中的稿件" % [str(slot.name), float(slot.weight), str(slot.desc)]
		else:
			slot_text = "%s · x%.2f\n%s\n%s · %s" % [str(slot.name), float(slot.weight), str(article.title), str(article.quality), _join_strings(article.tags, " / ")]
		slots.append({
			"id": str(slot.id),
			"text": slot_text,
			"selected": selected_article_id != -1,
			"enabled": true,
			"min_height": 84.0,
		})

	var stats := Systems.build_settlement_preview(run_state, run_state.slot_assignment)
	run_state.settlement_preview = stats.duplicate(true)
	return {
		"subtitle": "本周新增素材 %d 条，可转化候选稿件 %d 篇。正式切片只暴露候选稿与版面映射。" % [run_state.new_material_ids.size(), run_state.article_candidates.size()],
		"articles": articles,
		"slots": slots,
		"stats_text": _build_live_stats_text(stats),
	}

func _build_summary_payload() -> Dictionary:
	var hooks_text := "暂无下一周钩子。"
	if not run_state.next_week_hooks.is_empty():
		var lines: Array = []
		lines.append("利润档：%s" % str(run_state.next_week_hooks.get("profit_band", "neutral")))
		if run_state.next_week_hooks.has("dominant_axis"):
			lines.append("本期倾向：%s" % str(run_state.next_week_hooks.get("dominant_axis", "mixed")))
		if run_state.next_week_hooks.has("empty_slots"):
			lines.append("空版记录：%d" % int(run_state.next_week_hooks.get("empty_slots", 0)))
		hooks_text = _join_strings(lines, "\n")

	return {
		"summary_text": _build_summary_text(),
		"hooks_text": hooks_text,
	}

func _build_live_stats_text(stats: Dictionary) -> String:
	return "[b]已填版位[/b] %d / 6\n[b]空版位[/b] %d\n[b]totalBaseValue[/b] %d\n[b]uniqueTags[/b] %d\n[b]comboRaw[/b] %d\n[b]linkedTags[/b] %d\n[b]negPenalty[/b] %d\n\n[b]三轴占比[/b]\n公共事务 P %d · 大众关注 M %d · 轻内容 L %d\n\n[b]核心乘数[/b]\nmQuality %.2f · mCombo %.2f · mDiversity %.2f\nmLayout %.2f · mEmpty %.2f · mPenalty %.2f\nmLink %.2f · mBalance %.2f · mBias %.2f\n\n[b]实时预估[/b]\n需求 %d\n销量 %d / 印量 %d\n卖报收入 %.0f\n订阅收入 %.0f\n广告收入 %.0f\n总收入 %.0f\n总成本 %.0f\n净利润 %.0f\n下周订阅预估 %d" % [
		int(stats.filled_slots),
		int(stats.empty_slots),
		int(stats.total_base_value),
		int(stats.unique_tags),
		int(stats.combo_raw),
		int(stats.linked_tags),
		int(stats.neg_penalty),
		int(stats.axis_p),
		int(stats.axis_m),
		int(stats.axis_l),
		float(stats.m_quality),
		float(stats.m_combo),
		float(stats.m_diversity),
		float(stats.m_layout),
		float(stats.m_empty),
		float(stats.m_penalty),
		float(stats.m_link),
		float(stats.m_balance),
		float(stats.m_bias),
		int(stats.demand),
		int(stats.sold),
		int(stats.print_capacity),
		float(stats.news_revenue),
		float(stats.sub_revenue),
		float(stats.ad_revenue),
		float(stats.total_revenue),
		float(stats.total_cost),
		float(stats.profit),
		int(stats.next_subscribers),
	]

func _build_summary_text() -> String:
	if run_state.settlement_result.is_empty():
		return "尚未结算。"
	var result := run_state.settlement_result
	return "[b]第 %d 周发行完成[/b]\n净利润 %.0f · 销量 %d / %d · 下一周订阅 %d\n\n[color=#d8c8a2]编辑定位[/color] %.2f -> %.2f\n[color=#9fb3c7]公信 %d  诡名 %d  声望 %d  守序 %d  狂性 %d[/color]\n\n%s" % [
		int(result.week),
		float(result.profit),
		int(result.sold),
		int(result.demand),
		int(result.next_subscribers),
		float(result.editorial_profile_before),
		float(result.editorial_profile_after),
		int(run_state.macro_stats.credibility),
		int(run_state.macro_stats.weirdness),
		int(run_state.macro_stats.reputation),
		int(run_state.macro_stats.order),
		int(run_state.macro_stats.mania),
		str(result.commentary),
	]

func _format_roll_text(roll: Dictionary) -> String:
	var lines: Array = []
	lines.append(_format_roll_row("调查池", roll.dice_a, roll.negated_a))
	lines.append(_format_roll_row("现场池", roll.dice_b, roll.negated_b))
	return _join_strings(lines, "\n")

func _format_roll_row(title_text: String, dice: Array, negated: Array) -> String:
	var tokens: Array = []
	for index in range(dice.size()):
		if negated.has(index):
			tokens.append("-")
		elif bool(dice[index]):
			tokens.append("+")
		else:
			tokens.append("x")
	return "[b]%s[/b] %s" % [title_text, _join_strings(tokens, " ")]

func _build_roll_result_text(roll: Dictionary) -> String:
	var tier_map := {"major": "大成功", "minor": "小成功", "fail": "失败"}
	return "%s · A %d/%d  B %d/%d" % [str(tier_map.get(str(roll.tier), "失败")), int(roll.hit_a), int(roll.k_a), int(roll.hit_b), int(roll.k_b)]

func _build_roll_result_color(roll: Dictionary) -> Color:
	match str(roll.tier):
		"major":
			return Color(0.46, 0.87, 0.60, 1.0)
		"fail":
			return Color(0.94, 0.52, 0.46, 1.0)
		_:
			return Color(0.88, 0.76, 0.36, 1.0)

func _on_filter_pressed(tag: String) -> void:
	filter_state[tag] = not bool(filter_state.get(tag, true))
	_refresh_all()

func _on_region_pressed(region_id: String) -> void:
	selected_region_id = region_id
	selected_node_id = ""
	_refresh_all()

func _on_node_pressed(node_id: String) -> void:
	var started_at := _log_flow_start("_on_node_pressed", "incoming_node=%s previous_node=%s" % [node_id, selected_node_id])
	selected_node_id = node_id
	_refresh_all()
	_log_flow_end("_on_node_pressed", started_at, "selected_node=%s" % selected_node_id)

func _on_article_selected(article_id: int) -> void:
	selected_article_id = article_id
	_refresh_all()

func _toggle_staff(staff_id: String) -> void:
	if selected_staff_ids.has(staff_id):
		selected_staff_ids.erase(staff_id)
	elif selected_staff_ids.size() < 3:
		selected_staff_ids.append(staff_id)
	_refresh_all()

func _on_advance_phase_pressed() -> void:
	if run_state.current_phase == "briefing":
		Systems.start_explore(run_state)
		run_state.append_log("简报确认完成：本周探索正式开始。")
		if not Systems.has_legal_dispatches(run_state):
			run_state.append_log("[color=#f0d8a0]系统判定[/color]：当前已无任何合法派遣组合，直接进入编辑部。")
			_enter_editorial_phase()
			return
		_refresh_all()
		return
	_enter_editorial_phase()

func _on_execute_pressed() -> void:
	var started_at := _log_flow_start("_on_execute_pressed", "selected_node=%s" % selected_node_id)
	var node := _get_selected_node()
	if node.is_empty():
		_log_flow_end("_on_execute_pressed", started_at, "selected_node missing")
		return
	var availability := _get_node_availability(node)
	if not bool(availability.enabled):
		run_state.append_log("[color=#f59a8b]%s[/color]" % str(availability.reason))
		_refresh_all()
		_log_flow_end("_on_execute_pressed", started_at, "blocked=%s" % str(availability.reason))
		return
	var roll := Systems.perform_split_check(node, _get_selected_staff_totals())
	var outcome := Systems.apply_dispatch_resolution(run_state, material_inventory, node, roll, str(_get_selected_region().name))
	run_state.append_log("[color=#f0d8a0]%s[/color]：%s" % [str(node.name), str(outcome.message)])
	run_state.append_log("素材入库：[color=#9fd4ff]%s[/color]" % str(outcome.material.title))
	_refresh_all()
	if not Systems.has_legal_dispatches(run_state) or run_state.remaining_days <= 0:
		run_state.append_log("[color=#f0d8a0]系统判定[/color]：本周探索已收尾，进入编辑部。")
		_enter_editorial_phase()
	_log_flow_end("_on_execute_pressed", started_at, "node=%s days=%d materials=%d" % [str(node.id), run_state.remaining_days, run_state.new_material_ids.size()])

func _enter_editorial_phase() -> void:
	if run_state.current_phase != "explore":
		return
	Systems.enter_editorial(run_state, material_inventory)
	selected_article_id = -1
	run_state.append_log("探索阶段结束：编辑部开始根据素材库存与认知条目生成候选稿件。")
	_refresh_all()

func _place_article_in_slot(slot_id: String) -> void:
	if selected_article_id == -1:
		return
	for key in run_state.slot_assignment.keys():
		if int(run_state.slot_assignment[key]) == selected_article_id:
			run_state.slot_assignment[key] = -1
	run_state.slot_assignment[slot_id] = selected_article_id
	selected_article_id = -1
	_refresh_all()

func _clear_layout() -> void:
	for slot in Content.SLOT_DATA:
		run_state.slot_assignment[str(slot.id)] = -1
	selected_article_id = -1
	_refresh_all()

func _settle_issue() -> void:
	Systems.publish_issue(run_state, run_state.slot_assignment)
	var result := Systems.settle_published_issue(run_state, material_inventory)
	run_state.append_log("本期发刊完成：利润 %.0f，销量 %d。" % [float(result.profit), int(result.sold)])
	_refresh_all()

func _next_week() -> void:
	selected_node_id = ""
	selected_article_id = -1
	selected_staff_ids.clear()
	Systems.begin_next_week(run_state)
	selected_region_id = _default_region_id()
	_refresh_all()

func _default_region_id() -> String:
	for region in Content.REGION_DATA:
		if Systems.is_region_unlocked(run_state, region):
			return str(region.id)
	return str(Content.REGION_DATA[0].id)

func _ensure_valid_region_selection() -> void:
	var selected_region := _get_selected_region()
	if selected_region.is_empty() or not Systems.is_region_unlocked(run_state, selected_region):
		selected_region_id = _default_region_id()

func _ensure_valid_node_selection() -> void:
	if selected_node_id == "":
		return
	var node := _get_selected_node()
	if node.is_empty():
		selected_node_id = ""
		return
	if not Systems.is_node_visible(run_state, node) or not bool(filter_state.get(str(node.type), true)):
		selected_node_id = ""

func _get_selected_region() -> Dictionary:
	return Systems.get_region_by_id(selected_region_id)

func _get_selected_node() -> Dictionary:
	return Systems.get_node_by_id(selected_region_id, selected_node_id)

func _get_selected_staff_totals() -> Dictionary:
	var totals := {"explore": 0, "insight": 0, "occult": 0, "survival": 0, "reason": 0, "social": 0}
	for staff_data in Content.STAFF_POOL:
		if selected_staff_ids.has(str(staff_data.id)):
			for key in totals.keys():
				totals[key] += int(staff_data.attrs[key])
	return totals

func _get_node_availability(node: Dictionary) -> Dictionary:
	return Systems.get_node_availability(run_state, node, selected_staff_ids, _get_selected_staff_totals())

func _get_article_by_id(article_id: int) -> Dictionary:
	return Systems.get_article_by_id(run_state, article_id)

func _is_article_placed(article_id: int) -> bool:
	for value in run_state.slot_assignment.values():
		if int(value) == article_id:
			return true
	return false

func _phase_label(phase: String) -> String:
	match phase:
		"briefing":
			return "简报"
		"explore":
			return "探索"
		"editorial":
			return "编辑"
		"summary":
			return "结算"
		_:
			return phase

func _clear_container(node: Node) -> void:
	for child in node.get_children():
		node.remove_child(child)
		child.queue_free()

func _join_strings(values: Array, separator: String) -> String:
	var output: Array = []
	for value in values:
		output.append(str(value))
	return separator.join(output)

func _log_flow_start(flow_name: String, details: String = "") -> int:
	var started_at := Time.get_ticks_usec()
	Globals.log("WeeklyRunGame", "%s START %s" % [flow_name, details])
	return started_at

func _log_flow_end(flow_name: String, started_at: int, details: String = "") -> void:
	var elapsed_ms := float(Time.get_ticks_usec() - started_at) / 1000.0
	Globals.log("WeeklyRunGame", "%s END %.2fms %s" % [flow_name, elapsed_ms, details])
