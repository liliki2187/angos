extends Control

const Content = preload("res://scenes/gameplay/weekly_run/content/WeeklyRunContent.gd")
const Systems = preload("res://scenes/gameplay/weekly_run/systems/WeeklyRunSystems.gd")
const WeeklyRunState = preload("res://scenes/gameplay/weekly_run/state/WeeklyRunState.gd")

@onready var back_btn: Button = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/BackBtn
@onready var macro_bar: HBoxContainer = $RootMargin/RootVBox/MacroBar
@onready var week_label: Label = $RootMargin/RootVBox/WeekBar/WeekInfo/WeekLabel
@onready var day_label: Label = $RootMargin/RootVBox/WeekBar/WeekInfo/DayLabel
@onready var end_week_btn: Button = $RootMargin/RootVBox/WeekBar/EndWeekBtn
@onready var explore_phase: VBoxContainer = $RootMargin/RootVBox/ExplorePhase
@onready var week_start_text: RichTextLabel = $RootMargin/RootVBox/ExplorePhase/WeekStartPanel/WeekStartText
@onready var filter_row: HBoxContainer = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/RegionPanel/RegionVBox/FilterRow
@onready var region_list: VBoxContainer = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/RegionPanel/RegionVBox/RegionList
@onready var selected_staff_label: Label = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/StaffPanel/StaffVBox/SelectedStaffLabel
@onready var staff_grid: GridContainer = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/StaffPanel/StaffVBox/StaffGrid
@onready var clue_list: VBoxContainer = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/CluePanel/ClueVBox/ClueList
@onready var region_hint_label: Label = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/NodePanel/NodeVBox/RegionHintLabel
@onready var node_list: VBoxContainer = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/NodePanel/NodeVBox/NodeList
@onready var mission_summary: RichTextLabel = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/MissionPanel/MissionVBox/MissionSummary
@onready var probability_label: Label = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/MissionPanel/MissionVBox/ProbabilityLabel
@onready var dice_rows: VBoxContainer = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/MissionPanel/MissionVBox/DiceWrap/DiceRows
@onready var result_label: Label = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/MissionPanel/MissionVBox/ResultLabel
@onready var execute_btn: Button = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/MissionPanel/MissionVBox/ExecuteBtn
@onready var log_text: RichTextLabel = $RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/LogPanel/LogVBox/LogText
@onready var editorial_phase: VBoxContainer = $RootMargin/RootVBox/EditorialPhase
@onready var editorial_subtitle: Label = $RootMargin/RootVBox/EditorialPhase/EditorialHeader/EditorialHeaderVBox/EditorialSubtitle
@onready var article_list: VBoxContainer = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LibraryPanel/LibraryVBox/StoryScroll/StoryList
@onready var slot_list: VBoxContainer = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LayoutPanel/LayoutVBox/SlotList
@onready var clear_layout_btn: Button = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LayoutPanel/LayoutVBox/LayoutActions/ClearLayoutBtn
@onready var settle_btn: Button = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LayoutPanel/LayoutVBox/LayoutActions/SettleBtn
@onready var live_stats: RichTextLabel = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/StatsPanel/StatsVBox/LiveStats
@onready var summary_phase: PanelContainer = $RootMargin/RootVBox/SummaryPhase
@onready var summary_text: RichTextLabel = $RootMargin/RootVBox/SummaryPhase/SummaryVBox/SummaryText
@onready var next_week_btn: Button = $RootMargin/RootVBox/SummaryPhase/SummaryVBox/NextWeekBtn

var run_state := WeeklyRunState.new()
var filter_state := {"sci": true, "occult": true, "pop": true}
var selected_region_id := "us"
var selected_node_id := ""
var selected_article_id := -1
var selected_staff_ids: Array[String] = []
var filter_buttons := {}

func _ready() -> void:
	randomize()
	_apply_theme()
	_build_filter_buttons()
	_connect_buttons()
	_start_new_run()

func _apply_theme() -> void:
	for button in [back_btn, end_week_btn, execute_btn, clear_layout_btn, settle_btn, next_week_btn]:
		_style_button(button, button != back_btn and button != clear_layout_btn)
	for panel in [
		$RootMargin/RootVBox/HeaderPanel,
		$RootMargin/RootVBox/ExplorePhase/WeekStartPanel,
		$RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/RegionPanel,
		$RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/StaffPanel,
		$RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreLeft/CluePanel,
		$RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/NodePanel,
		$RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/MissionPanel,
		$RootMargin/RootVBox/ExplorePhase/ExploreSplit/ExploreRight/LogPanel,
		$RootMargin/RootVBox/EditorialPhase/EditorialHeader,
		$RootMargin/RootVBox/EditorialPhase/EditorialColumns/LibraryPanel,
		$RootMargin/RootVBox/EditorialPhase/EditorialColumns/LayoutPanel,
		$RootMargin/RootVBox/EditorialPhase/EditorialColumns/StatsPanel,
		summary_phase,
	]:
		_style_panel(panel)

func _build_filter_buttons() -> void:
	for tag in ["sci", "occult", "pop"]:
		var button := Button.new()
		button.text = Content.TAG_LABELS[tag]
		button.custom_minimum_size = Vector2(0, 30)
		button.pressed.connect(_on_filter_pressed.bind(tag))
		filter_row.add_child(button)
		filter_buttons[tag] = button
	_style_filter_buttons()

func _connect_buttons() -> void:
	back_btn.pressed.connect(_on_back_pressed)
	end_week_btn.pressed.connect(_on_advance_phase_pressed)
	execute_btn.pressed.connect(_on_execute_pressed)
	clear_layout_btn.pressed.connect(_clear_layout)
	settle_btn.pressed.connect(_settle_issue)
	next_week_btn.pressed.connect(_next_week)

func _on_back_pressed() -> void:
	get_tree().change_scene_to_file(str(Globals.scene_paths.get("main_menu", "res://scenes/ui/main_menu/MainMenu.tscn")))

func _on_filter_pressed(tag: String) -> void:
	filter_state[tag] = not bool(filter_state[tag])
	_style_filter_buttons()
	_refresh_region_and_nodes()

func _on_region_pressed(region_id: String) -> void:
	selected_region_id = region_id
	selected_node_id = ""
	_refresh_region_and_nodes()
	_refresh_mission_panel()

func _on_node_pressed(node_id: String) -> void:
	selected_node_id = node_id
	_refresh_region_and_nodes()
	_refresh_mission_panel()

func _on_article_selected(article_id: int) -> void:
	selected_article_id = article_id
	_refresh_article_candidates()
	_refresh_slots()

func _start_new_run() -> void:
	run_state = WeeklyRunState.new()
	selected_region_id = "us"
	selected_node_id = ""
	selected_article_id = -1
	selected_staff_ids.clear()
	Systems.initialize_new_run(run_state)
	_refresh_all()

func _refresh_all() -> void:
	var show_explore_surface := run_state.current_phase == "briefing" or run_state.current_phase == "explore"
	explore_phase.visible = show_explore_surface
	editorial_phase.visible = run_state.current_phase == "editorial"
	summary_phase.visible = run_state.current_phase == "summary"
	week_label.text = "第 %d 周 · %s" % [run_state.week, _phase_label(run_state.current_phase)]
	day_label.text = "剩余 %d / %d 天 · 订阅 %d · editorialProfile %.2f" % [run_state.remaining_days, Content.WEEK_DAYS, run_state.subscribers, run_state.editorial_profile]
	_refresh_phase_actions()
	_refresh_macro_bar()
	_refresh_week_briefing()
	_refresh_region_and_nodes()
	_refresh_staff_grid()
	_refresh_materials()
	_refresh_mission_panel()
	_refresh_log()
	if run_state.current_phase == "editorial":
		_refresh_article_candidates()
		_refresh_slots()
		_refresh_live_stats()
	if run_state.current_phase == "summary":
		_refresh_summary()

func _refresh_phase_actions() -> void:
	end_week_btn.visible = run_state.current_phase != "summary"
	match run_state.current_phase:
		"briefing":
			end_week_btn.disabled = false
			end_week_btn.text = "确认简报 · 进入探索"
		"explore":
			end_week_btn.disabled = false
			end_week_btn.text = "结束探索 · 进入编辑部"
		_:
			end_week_btn.disabled = true
			end_week_btn.text = "阶段切换中"

func _refresh_macro_bar() -> void:
	_clear_container(macro_bar)
	for item in Content.MACRO_LABELS:
		var panel := PanelContainer.new()
		panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		_style_panel(panel, Color(0.09, 0.12, 0.18, 1.0), Color(0.23, 0.29, 0.35, 1.0), 10)
		macro_bar.add_child(panel)
		var box := VBoxContainer.new()
		box.custom_minimum_size = Vector2(0, 58)
		panel.add_child(box)
		var title := Label.new()
		title.text = str(item.label)
		title.add_theme_color_override("font_color", Color(0.84, 0.68, 0.37, 1.0))
		box.add_child(title)
		var value := Label.new()
		value.text = str(run_state.macro_stats[item.key])
		value.add_theme_font_size_override("font_size", 21)
		box.add_child(value)

func _refresh_week_briefing() -> void:
	var unlocked := []
	for region in Content.REGION_DATA:
		if Systems.is_region_unlocked(run_state, region):
			unlocked.append(str(region.name))
	var briefing_lines := Systems.build_briefing_lines(run_state)
	week_start_text.text = "[b]本周简报[/b]\n%s\n\n[color=#d8c8a2]当前开放区域：%s[/color]" % [
		_join_strings(briefing_lines, "\n"),
		_join_strings(unlocked, ", "),
	]

func _refresh_region_and_nodes() -> void:
	_clear_container(region_list)
	var can_explore := run_state.current_phase == "explore"
	for region in Content.REGION_DATA:
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 72)
		button.text = "%s\n%s" % [str(region.name), str(region.hint)]
		button.disabled = not Systems.is_region_unlocked(run_state, region) or not can_explore
		button.pressed.connect(_on_region_pressed.bind(str(region.id)))
		_style_button(button, selected_region_id == str(region.id))
		region_list.add_child(button)

	_clear_container(node_list)
	var region := _get_selected_region()
	region_hint_label.text = "请选择区域" if region.is_empty() else "%s · %s" % [str(region.name), str(region.hint)]
	if region.is_empty():
		return
	for node in region.nodes:
		if not Systems.is_node_visible(run_state, node):
			continue
		if not bool(filter_state.get(str(node.type), true)):
			continue
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 88)
		var availability := _get_node_availability(node)
		button.text = "%s · %s\n耗时 %d 天 · %s · 对抗 %d\n%s" % [
			str(node.name),
			str(node.kind),
			int(node.days),
			str(node.difficulty),
			int(node.enemy),
			str(availability.reason),
		]
		button.disabled = not bool(availability.enabled)
		button.pressed.connect(_on_node_pressed.bind(str(node.id)))
		_style_button(button, selected_node_id == str(node.id))
		node_list.add_child(button)

func _refresh_staff_grid() -> void:
	_clear_container(staff_grid)
	selected_staff_label.text = "已选择：%d / 3" % selected_staff_ids.size()
	for staff in Content.STAFF_POOL:
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 106)
		button.text = "%s · %s\n探索 %d  洞察 %d  诡思 %d\n生存 %d  理性 %d  社交 %d" % [
			str(staff.name),
			str(staff.role),
			int(staff.attrs.explore),
			int(staff.attrs.insight),
			int(staff.attrs.occult),
			int(staff.attrs.survival),
			int(staff.attrs.reason),
			int(staff.attrs.social),
		]
		button.disabled = run_state.current_phase != "explore"
		button.pressed.connect(_toggle_staff.bind(str(staff.id)))
		_style_button(button, selected_staff_ids.has(str(staff.id)))
		staff_grid.add_child(button)

func _refresh_materials() -> void:
	_clear_container(clue_list)
	var materials := run_state.get_new_materials()
	if materials.is_empty():
		var empty := Label.new()
		empty.text = "本周还没有新增素材。先确认简报，再开始派遣。"
		empty.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		empty.add_theme_color_override("font_color", Color(0.64, 0.70, 0.78, 1.0))
		clue_list.add_child(empty)
		return
	for material in materials:
		var panel := PanelContainer.new()
		_style_panel(panel, Color(0.06, 0.09, 0.13, 1.0), Color(0.21, 0.27, 0.33, 1.0), 10)
		clue_list.add_child(panel)
		var text := RichTextLabel.new()
		text.bbcode_enabled = true
		text.fit_content = true
		text.scroll_active = false
		text.text = "[b]%s[/b]\n%s · tier %d · %s" % [
			str(material.title),
			Content.TAG_LABELS.get(str(material.type), str(material.type)),
			int(material.tier),
			str(material.source_region),
		]
		panel.add_child(text)

func _refresh_mission_panel() -> void:
	_clear_container(dice_rows)
	if run_state.current_phase == "briefing":
		mission_summary.text = "先确认本周简报，再进入探索。当前简报已生成 %d 条任务与 %d 个可见机会。" % [run_state.active_tasks.size(), run_state.opportunity_ids.size()]
		probability_label.text = "理论结果：等待进入探索"
		result_label.text = "简报阶段"
		execute_btn.disabled = true
		return
	if run_state.current_phase != "explore":
		mission_summary.text = "当前不在探索阶段。"
		probability_label.text = "理论结果：等待阶段切换"
		result_label.text = "阶段锁定"
		execute_btn.disabled = true
		return

	var node := _get_selected_node()
	if node.is_empty():
		mission_summary.text = "从上方节点列表中选中一个外采目标。"
		probability_label.text = "理论结果：等待选点"
		result_label.text = "等待执行"
		execute_btn.disabled = true
		return

	var totals := _get_selected_staff_totals()
	var needs := []
	for key in node.need.keys():
		needs.append("%s %d" % [Content.ATTR_LABELS.get(str(key), str(key)), int(node.need[key])])
	mission_summary.text = "[b]%s[/b]\n%s\n\n[color=#d8c8a2]需求：%s[/color]\n[color=#9fb3c7]当前派遣合计：探索 %d / 洞察 %d / 诡思 %d / 生存 %d / 理性 %d / 社交 %d[/color]\n[color=#8fa4bc]%s[/color]" % [
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
	var probabilities := Systems.calculate_node_probabilities(node, totals)
	probability_label.text = "理论结果：大成功 %.0f%% · 小成功 %.0f%% · 失败 %.0f%%" % [
		float(probabilities.major) * 100.0,
		float(probabilities.minor) * 100.0,
		float(probabilities.fail) * 100.0,
	]
	var availability := _get_node_availability(node)
	result_label.text = "等待执行"
	execute_btn.disabled = not bool(availability.enabled)

func _refresh_log() -> void:
	log_text.text = _join_strings(run_state.log_entries, "\n\n")

func _toggle_staff(staff_id: String) -> void:
	if run_state.current_phase != "explore":
		return
	if selected_staff_ids.has(staff_id):
		selected_staff_ids.erase(staff_id)
	elif selected_staff_ids.size() < 3:
		selected_staff_ids.append(staff_id)
	_refresh_staff_grid()
	_refresh_mission_panel()
	_refresh_region_and_nodes()

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
	var node := _get_selected_node()
	if node.is_empty():
		return
	var availability := _get_node_availability(node)
	if not bool(availability.enabled):
		run_state.append_log("[color=#f59a8b]%s[/color]" % str(availability.reason))
		_refresh_log()
		return
	var roll := Systems.perform_split_check(node, _get_selected_staff_totals())
	_render_roll(roll)
	var outcome := Systems.apply_dispatch_resolution(run_state, node, roll, str(_get_selected_region().name))
	selected_node_id = ""
	run_state.append_log("[color=#f0d8a0]%s[/color]：%s" % [str(node.name), str(outcome.message)])
	run_state.append_log("素材入库：[color=#9fd4ff]%s[/color]" % str(outcome.material.title))
	_refresh_all()
	if not Systems.has_legal_dispatches(run_state):
		run_state.append_log("[color=#f0d8a0]系统判定[/color]：本周已无合法派遣组合，直接进入编辑部。")
		_enter_editorial_phase()
		return
	if run_state.remaining_days <= 0:
		_enter_editorial_phase()

func _render_roll(roll: Dictionary) -> void:
	_clear_container(dice_rows)
	_add_roll_row("调查池（探索+洞察+诡思）", roll.dice_a, roll.negated_a)
	_add_roll_row("现场池（生存+理性）", roll.dice_b, roll.negated_b)
	var tier_map := {"major": "大成功", "minor": "小成功", "fail": "失败"}
	result_label.text = "%s · A %d/%d  B %d/%d" % [str(tier_map.get(str(roll.tier), "失败")), int(roll.hit_a), int(roll.k_a), int(roll.hit_b), int(roll.k_b)]
	var color := Color(0.88, 0.76, 0.36, 1.0)
	if roll.tier == "major":
		color = Color(0.46, 0.87, 0.60, 1.0)
	elif roll.tier == "fail":
		color = Color(0.94, 0.52, 0.46, 1.0)
	result_label.add_theme_color_override("font_color", color)

func _add_roll_row(title_text: String, dice: Array, negated: Array) -> void:
	var title := Label.new()
	title.text = title_text
	title.add_theme_color_override("font_color", Color(0.64, 0.70, 0.78, 1.0))
	dice_rows.add_child(title)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 4)
	dice_rows.add_child(row)
	for index in range(dice.size()):
		var die := Label.new()
		var is_negated := negated.has(index)
		die.text = "-" if is_negated else ("+" if dice[index] else "x")
		die.custom_minimum_size = Vector2(28, 28)
		die.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		die.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		die.add_theme_font_size_override("font_size", 16)
		var die_color := Color(0.58, 0.62, 0.67, 1.0)
		if not is_negated:
			die_color = Color(0.46, 0.87, 0.60, 1.0) if dice[index] else Color(0.94, 0.52, 0.46, 1.0)
		die.add_theme_color_override("font_color", die_color)
		row.add_child(die)

func _enter_editorial_phase() -> void:
	if run_state.current_phase != "explore":
		return
	Systems.enter_editorial(run_state)
	selected_article_id = -1
	run_state.append_log("探索阶段结束，编辑部开始根据素材库存与认知条目生成候选稿件。")
	_refresh_all()

func _refresh_article_candidates() -> void:
	_clear_container(article_list)
	editorial_subtitle.text = "本周新增素材 %d 条，可转化候选稿件 %d 篇。先点击稿件，再点击右侧版位放置。" % [
		run_state.new_material_ids.size(),
		run_state.article_candidates.size(),
	]
	for article in run_state.article_candidates:
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 88)
		button.text = "%s\n%s · %s · base %d" % [
			str(article.title),
			_join_strings(article.tags, " / "),
			str(article.quality),
			int(article.base_value),
		]
		button.disabled = _is_article_placed(int(article.id))
		button.pressed.connect(_on_article_selected.bind(int(article.id)))
		_style_button(button, selected_article_id == int(article.id))
		if button.disabled:
			button.text += "\n已上版"
		article_list.add_child(button)

func _refresh_slots() -> void:
	_clear_container(slot_list)
	for slot in Content.SLOT_DATA:
		var article := _get_article_by_id(int(run_state.slot_assignment.get(str(slot.id), -1)))
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 84)
		if article.is_empty():
			button.text = "%s · x%.2f\n%s\n点击这里放置当前选中的稿件" % [str(slot.name), float(slot.weight), str(slot.desc)]
		else:
			button.text = "%s · x%.2f\n%s\n%s · %s" % [str(slot.name), float(slot.weight), str(article.title), str(article.quality), _join_strings(article.tags, " / ")]
		button.pressed.connect(_place_article_in_slot.bind(str(slot.id)))
		_style_button(button, selected_article_id != -1)
		slot_list.add_child(button)

func _place_article_in_slot(slot_id: String) -> void:
	if selected_article_id == -1:
		return
	for key in run_state.slot_assignment.keys():
		if int(run_state.slot_assignment[key]) == selected_article_id:
			run_state.slot_assignment[key] = -1
	run_state.slot_assignment[slot_id] = selected_article_id
	selected_article_id = -1
	_refresh_article_candidates()
	_refresh_slots()
	_refresh_live_stats()

func _clear_layout() -> void:
	for slot in Content.SLOT_DATA:
		run_state.slot_assignment[str(slot.id)] = -1
	selected_article_id = -1
	_refresh_article_candidates()
	_refresh_slots()
	_refresh_live_stats()

func _refresh_live_stats() -> void:
	var stats := Systems.build_settlement_preview(run_state, run_state.slot_assignment)
	run_state.settlement_preview = stats.duplicate(true)
	live_stats.text = "[b]已填版位[/b] %d / 6\n[b]空版位[/b] %d\n[b]totalBaseValue[/b] %d\n[b]uniqueTags[/b] %d\n[b]comboRaw[/b] %d\n[b]linkedTags[/b] %d\n[b]negPenalty[/b] %d\n\n[b]三轴占比[/b]\n公共事务 P %d · 大众关注 M %d · 轻内容 L %d\n\n[b]核心乘数[/b]\nmQuality %.2f · mCombo %.2f · mDiversity %.2f\nmLayout %.2f · mEmpty %.2f · mPenalty %.2f\nmLink %.2f · mBalance %.2f · mBias %.2f\n\n[b]实时预估[/b]\n需求 %d\n销量 %d / 印量 %d\n卖报收入 %.0f\n订阅收入 %.0f\n广告收入 %.0f\n总收入 %.0f\n总成本 %.0f\n净利润 %.0f\n下周订阅预估 %d" % [
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

func _settle_issue() -> void:
	Systems.publish_issue(run_state, run_state.slot_assignment)
	var result := Systems.settle_published_issue(run_state)
	run_state.append_log("本期发刊完成：利润 %.0f，销量 %d。" % [float(result.profit), int(result.sold)])
	_refresh_all()

func _refresh_summary() -> void:
	if run_state.settlement_result.is_empty():
		summary_text.text = "尚未结算。"
		return
	var result := run_state.settlement_result
	summary_text.text = "[b]第 %d 周发行完成[/b]\n净利润 %.0f · 销量 %d / %d · 下一周订阅 %d\n\n[color=#d8c8a2]编辑定位[/color] %.2f -> %.2f\n[color=#9fb3c7]公信 %d  诡名 %d  声望 %d  守序 %d  狂性 %d[/color]\n\n%s" % [
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

func _next_week() -> void:
	selected_node_id = ""
	selected_article_id = -1
	selected_staff_ids.clear()
	Systems.begin_next_week(run_state)
	_refresh_all()

func _get_selected_region() -> Dictionary:
	return Systems.get_region_by_id(selected_region_id)

func _get_selected_node() -> Dictionary:
	return Systems.get_node_by_id(selected_region_id, selected_node_id)

func _get_selected_staff_totals() -> Dictionary:
	var totals := {"explore": 0, "insight": 0, "occult": 0, "survival": 0, "reason": 0, "social": 0}
	for staff in Content.STAFF_POOL:
		if selected_staff_ids.has(str(staff.id)):
			for key in totals.keys():
				totals[key] += int(staff.attrs[key])
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

func _style_filter_buttons() -> void:
	for tag in filter_buttons.keys():
		_style_button(filter_buttons[tag], bool(filter_state[tag]))

func _style_panel(panel: Control, bg: Color = Color(0.08, 0.11, 0.16, 0.97), border: Color = Color(0.20, 0.25, 0.31, 1.0), radius: int = 14) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	style.content_margin_left = 12
	style.content_margin_top = 12
	style.content_margin_right = 12
	style.content_margin_bottom = 12
	panel.add_theme_stylebox_override("panel", style)

func _style_button(button: Button, emphasis: bool) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.09, 0.12, 0.18, 1.0)
	normal.border_color = Color(0.28, 0.34, 0.42, 1.0)
	if emphasis:
		normal.bg_color = Color(0.22, 0.18, 0.08, 1.0)
		normal.border_color = Color(0.80, 0.64, 0.33, 1.0)
	normal.set_border_width_all(1)
	normal.corner_radius_top_left = 10
	normal.corner_radius_top_right = 10
	normal.corner_radius_bottom_left = 10
	normal.corner_radius_bottom_right = 10
	normal.content_margin_left = 10
	normal.content_margin_right = 10
	normal.content_margin_top = 8
	normal.content_margin_bottom = 8
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", normal.duplicate())
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	var font_color := Color(0.95, 0.96, 0.98, 1.0)
	if emphasis:
		font_color = Color(0.95, 0.88, 0.72, 1.0)
	button.add_theme_color_override("font_color", font_color)

func _clear_container(node: Node) -> void:
	for child in node.get_children():
		node.remove_child(child)
		child.queue_free()

func _join_strings(values: Array, separator: String) -> String:
	var out := []
	for value in values:
		out.append(str(value))
	return separator.join(out)
