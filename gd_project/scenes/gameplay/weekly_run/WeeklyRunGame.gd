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

const DISPATCH_MAX_STAFF := 3

@onready var root_margin: MarginContainer = $RootMargin
@onready var header_panel: PanelContainer = $RootMargin/RootVBox/HeaderPanel
@onready var world_shell_art: TextureRect = $WorldShellArt
@onready var channel_mark: Label = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/ChannelMark
@onready var title_label: Label = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/TitleBox/Title
@onready var subtitle_label: Label = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/TitleBox/Subtitle
@onready var world_header_meta: PanelContainer = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta
@onready var world_header_cycle: Label = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderMetaTopRow/WorldHeaderCycle
@onready var world_header_clips: Label = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderMetaTopRow/WorldHeaderClips
@onready var world_state_title: Label = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderStateRow/WorldStateTitle
@onready var world_state_labels: Array[Label] = [
	$RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderStateRow/WorldStateCredibility,
	$RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderStateRow/WorldStateWeirdness,
	$RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderStateRow/WorldStateReputation,
	$RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderStateRow/WorldStateOrder,
	$RootMargin/RootVBox/HeaderPanel/HeaderHBox/WorldHeaderMeta/WorldHeaderMetaVBox/WorldHeaderStateRow/WorldStateMania,
]
@onready var back_btn: Button = $RootMargin/RootVBox/HeaderPanel/HeaderHBox/BackBtn
@onready var macro_bar: HBoxContainer = $RootMargin/RootVBox/MacroBar
@onready var week_bar: HBoxContainer = $RootMargin/RootVBox/WeekBar
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
var explore_view_mode := "world"
var dispatch_locked := false
var dispatch_notice_text := ""
var dispatch_signoff_state := "idle"

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
	_apply_header_panel_style()
	title_label.add_theme_font_size_override("font_size", 22)
	title_label.add_theme_color_override("font_color", Color(0.98, 0.94, 0.74, 1.0))
	title_label.add_theme_constant_override("outline_size", 3)
	title_label.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.92))
	subtitle_label.add_theme_font_size_override("font_size", 12)
	subtitle_label.add_theme_color_override("font_color", Color(0.58, 0.84, 0.86, 1.0))
	subtitle_label.text = "全球频道 / 取材 / 派遣 / 排版 / 发刊回响"
	_style_world_header_extras()
	macro_bar.add_theme_constant_override("separation", 5)
	UiStyle.apply_button_style(back_btn, false, true)
	UiStyle.apply_button_style(end_week_btn, true, true)
	week_label.add_theme_color_override("font_color", Color(0.95, 0.88, 0.66, 1.0))
	week_label.add_theme_constant_override("outline_size", 3)
	week_label.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.90))
	day_label.add_theme_color_override("font_color", Color(0.60, 0.82, 0.84, 1.0))
	day_label.add_theme_font_size_override("font_size", 13)

func _apply_header_panel_style(compact_world: bool = false) -> void:
	var style := StyleBoxFlat.new()
	if compact_world:
		style.bg_color = Color(0.020, 0.030, 0.034, 0.90)
		style.border_color = Color(0.18, 0.46, 0.50, 0.56)
		style.set_border_width_all(1)
		style.border_width_left = 5
		style.content_margin_left = 14
		style.content_margin_top = 8
		style.content_margin_right = 10
		style.content_margin_bottom = 8
		header_panel.add_theme_stylebox_override("panel", style)
		return
	style.bg_color = Color(0.034, 0.046, 0.050, 0.94)
	style.border_color = Color(0.68, 0.56, 0.34, 0.78)
	style.set_border_width_all(1)
	style.border_width_left = 3
	style.corner_radius_top_left = 5
	style.corner_radius_top_right = 5
	style.corner_radius_bottom_left = 5
	style.corner_radius_bottom_right = 5
	style.content_margin_left = 14
	style.content_margin_top = 8
	style.content_margin_right = 12
	style.content_margin_bottom = 8
	header_panel.add_theme_stylebox_override("panel", style)

func _style_world_header_extras() -> void:
	_apply_label_badge(channel_mark, Color(0.72, 0.12, 0.09, 0.98), Color(0.98, 0.70, 0.44, 0.58))
	channel_mark.add_theme_font_size_override("font_size", 42)
	channel_mark.add_theme_color_override("font_color", Color(0.90, 0.84, 0.62, 1.0))
	channel_mark.add_theme_constant_override("outline_size", 2)
	channel_mark.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.015, 0.85))
	_apply_header_meta_panel_style()
	world_header_cycle.add_theme_font_size_override("font_size", 13)
	world_header_cycle.add_theme_color_override("font_color", Color(0.76, 0.88, 0.82, 1.0))
	world_header_clips.add_theme_font_size_override("font_size", 13)
	world_header_clips.add_theme_color_override("font_color", Color(0.78, 0.88, 0.82, 0.86))
	world_state_title.add_theme_font_size_override("font_size", 11)
	world_state_title.add_theme_color_override("font_color", Color(0.45, 0.82, 0.84, 1.0))
	world_state_title.add_theme_constant_override("outline_size", 1)
	world_state_title.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.82))
	var state_borders := [
		Color(0.10, 0.70, 0.74, 0.72),
		Color(0.78, 0.18, 0.14, 0.78),
		Color(0.88, 0.62, 0.18, 0.78),
		Color(0.35, 0.52, 0.92, 0.72),
		Color(0.90, 0.14, 0.25, 0.78),
	]
	for index in range(world_state_labels.size()):
		var label: Label = world_state_labels[index]
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.add_theme_font_size_override("font_size", 15)
		label.add_theme_color_override("font_color", Color(0.94, 0.98, 0.90, 1.0))
		_apply_label_badge(label, Color(0.026, 0.044, 0.046, 0.96), state_borders[index], 7, 4, 5)

func _apply_header_meta_panel_style() -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.018, 0.028, 0.032, 0.96)
	style.border_color = Color(0.22, 0.54, 0.58, 0.58)
	style.set_border_width_all(1)
	style.corner_radius_top_left = 2
	style.corner_radius_top_right = 2
	style.corner_radius_bottom_left = 2
	style.corner_radius_bottom_right = 2
	style.content_margin_left = 10
	style.content_margin_top = 7
	style.content_margin_right = 10
	style.content_margin_bottom = 7
	world_header_meta.add_theme_stylebox_override("panel", style)

func _apply_label_badge(label: Label, bg: Color, border: Color, margin_x: int = 10, margin_y: int = 6, left_width: int = 1) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.border_width_left = left_width
	style.corner_radius_top_left = 2
	style.corner_radius_top_right = 2
	style.corner_radius_bottom_left = 2
	style.corner_radius_bottom_right = 2
	style.content_margin_left = margin_x
	style.content_margin_top = margin_y
	style.content_margin_right = margin_x
	style.content_margin_bottom = margin_y
	label.add_theme_stylebox_override("normal", style)

func _connect_shell_signals() -> void:
	back_btn.pressed.connect(_on_back_pressed)
	end_week_btn.pressed.connect(_on_advance_phase_pressed)
	explore_phase.connect("filter_toggled", Callable(self, "_on_filter_pressed"))
	explore_phase.connect("region_selected", Callable(self, "_on_region_pressed"))
	explore_phase.connect("enter_region_requested", Callable(self, "_on_enter_region_requested"))
	explore_phase.connect("back_to_world_requested", Callable(self, "_on_back_to_world_requested"))
	explore_phase.connect("back_to_region_requested", Callable(self, "_on_back_to_region_requested"))
	explore_phase.connect("node_selected", Callable(self, "_on_node_pressed"))
	explore_phase.connect("open_dispatch_requested", Callable(self, "_on_open_dispatch_requested"))
	explore_phase.connect("staff_toggled", Callable(self, "_toggle_staff"))
	explore_phase.connect("selected_staff_slot_removed", Callable(self, "_toggle_staff"))
	explore_phase.connect("execute_requested", Callable(self, "_on_execute_pressed"))
	editorial_phase.connect("article_selected", Callable(self, "_on_article_selected"))
	editorial_phase.connect("slot_selected", Callable(self, "_place_article_in_slot"))
	editorial_phase.connect("slot_cleared", Callable(self, "_clear_editorial_slot"))
	editorial_phase.connect("transfer_requested", Callable(self, "_apply_editorial_transfer"))
	editorial_phase.connect("held_article_cancelled", Callable(self, "_cancel_editorial_selection"))
	editorial_phase.connect("clear_layout_requested", Callable(self, "_clear_layout"))
	editorial_phase.connect("settle_requested", Callable(self, "_settle_issue"))
	summary_phase.connect("next_week_requested", Callable(self, "_next_week"))

func _on_back_pressed() -> void:
	var main_menu_path := "res://scenes/ui/main_menu/MainMenu.tscn"
	var globals := _get_globals_singleton()
	if globals != null:
		var scene_paths = globals.get("scene_paths")
		if scene_paths is Dictionary:
			main_menu_path = str(scene_paths.get("main_menu", main_menu_path))
	get_tree().change_scene_to_file(main_menu_path)

func _start_new_run() -> void:
	run_state = WeeklyRunState.new()
	material_inventory = WeeklyMaterialInventory.new()
	filter_state = {"sci": true, "occult": true, "pop": true}
	selected_node_id = ""
	selected_article_id = -1
	selected_staff_ids.clear()
	explore_view_mode = "world"
	dispatch_locked = false
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
	Systems.initialize_new_run(run_state, material_inventory)
	selected_region_id = _default_region_id()
	_refresh_all()

func _refresh_all() -> void:
	var started_at := _log_flow_start("_refresh_all", "phase=%s selected_node=%s" % [run_state.current_phase, selected_node_id])
	_ensure_valid_region_selection()
	_ensure_valid_node_selection()
	week_label.text = "第 %d 周 · %s" % [run_state.week, _phase_label(run_state.current_phase)]
	day_label.text = "剩余 %d / %d 天 · 订阅 %d · 主编声誉 %.0f%%" % [run_state.remaining_days, Content.WEEK_DAYS, run_state.subscribers, run_state.editorial_profile * 100.0]
	_refresh_phase_actions()
	_refresh_macro_bar()
	_refresh_phase_views()
	_sync_shell_chrome()
	_log_flow_end("_refresh_all", started_at, "phase=%s selected_node=%s" % [run_state.current_phase, selected_node_id])

func _sync_shell_chrome() -> void:
	var is_world_map := run_state.current_phase == "explore" and explore_view_mode == "world"
	var is_deep_explore := run_state.current_phase == "explore" and explore_view_mode in ["region", "dispatch"]
	var is_region_task_board := run_state.current_phase == "explore" and explore_view_mode == "region"
	var is_editorial := run_state.current_phase == "editorial"
	var uses_wmw_assembly: bool = is_world_map and is_instance_valid(explore_phase) and explore_phase.has_method("has_world_map_assembly") and bool(explore_phase.call("has_world_map_assembly"))
	var uses_full_screen_host: bool = is_region_task_board or uses_wmw_assembly
	root_margin.offset_left = 0.0 if uses_full_screen_host else 24.0
	root_margin.offset_top = 0.0 if uses_full_screen_host else 20.0
	root_margin.offset_right = 0.0 if uses_full_screen_host else -24.0
	root_margin.offset_bottom = 0.0 if uses_full_screen_host else -20.0
	header_panel.visible = not is_deep_explore and not is_editorial and not uses_wmw_assembly
	world_shell_art.visible = is_world_map and not uses_wmw_assembly
	macro_bar.visible = not is_world_map and not is_deep_explore and not is_editorial
	week_bar.visible = not is_world_map and not is_deep_explore and not is_editorial
	channel_mark.visible = is_world_map and not uses_wmw_assembly
	world_header_meta.visible = is_world_map and not uses_wmw_assembly
	if uses_wmw_assembly:
		return
	if is_deep_explore:
		return
	_apply_header_panel_style(is_world_map)
	if is_world_map:
		title_label.text = "GLOBAL CHANNEL"
		title_label.add_theme_font_size_override("font_size", 34)
		title_label.add_theme_color_override("font_color", Color(0.90, 0.24, 0.18, 1.0))
		subtitle_label.text = "本周世界取材墙"
		subtitle_label.add_theme_font_size_override("font_size", 14)
		world_header_cycle.text = "ISSUE 001 / WEEK %02d / DAYS LEFT %02d" % [
			run_state.week,
			run_state.remaining_days,
		]
		world_header_clips.text = "CLIPS %02d" % run_state.new_material_ids.size()
		var stat_values := [
			["◇ 公信", int(run_state.macro_stats.credibility)],
			["▲ 诡名", int(run_state.macro_stats.weirdness)],
			["★ 声望", int(run_state.macro_stats.reputation)],
			["□ 守序", int(run_state.macro_stats.order)],
			["! 狂性", int(run_state.macro_stats.mania)],
		]
		for index in range(world_state_labels.size()):
			var item: Array = stat_values[index]
			world_state_labels[index].text = "%s %02d" % [str(item[0]), int(item[1])]
	else:
		title_label.text = "《世界未解之谜周刊》· 正式周循环切片"
		title_label.add_theme_font_size_override("font_size", 22)
		title_label.add_theme_color_override("font_color", Color(0.98, 0.94, 0.74, 1.0))
		subtitle_label.text = "全球频道 / 取材 / 派遣 / 排版 / 发刊回响"
		subtitle_label.add_theme_font_size_override("font_size", 12)

func _compact_macro_state_text() -> String:
	var focus_data := _build_macro_focus_data()
	var parts: Array[String] = []
	for item in Content.MACRO_LABELS:
		var key := str(item.key)
		var label := str(item.label)
		var text := "%s%d" % [label, int(run_state.macro_stats[key])]
		if key == str(focus_data.get("key", "")):
			text += "(%s)" % str(focus_data.get("text", ""))
		parts.append(text)
	return _join_strings(parts, " / ")

func _refresh_phase_actions() -> void:
	match run_state.current_phase:
		"briefing":
			end_week_btn.visible = true
			end_week_btn.text = "确认简报 · 进入探索"
			UiStyle.apply_button_style(end_week_btn, true, true)
		"explore":
			end_week_btn.visible = false
		_:
			end_week_btn.visible = false

func _refresh_macro_bar() -> void:
	var started_at := _log_flow_start("_refresh_macro_bar", "items=%d" % Content.MACRO_LABELS.size())
	_clear_container(macro_bar)
	var focus_data := _build_macro_focus_data()
	for item in Content.MACRO_LABELS:
		var card := MetricCardScene.instantiate()
		macro_bar.add_child(card)
		var key := str(item.key)
		card.bind(
			str(item.label),
			str(run_state.macro_stats[key]),
			key,
			str(focus_data.get("text", "")) if key == str(focus_data.get("key", "")) else "",
			key == str(focus_data.get("key", ""))
		)
	_log_flow_end("_refresh_macro_bar", started_at, "items=%d" % Content.MACRO_LABELS.size())

func _build_macro_focus_data() -> Dictionary:
	var region := _get_selected_region()
	if region.is_empty() or Systems.is_region_unlocked(run_state, region):
		return {}
	match str(region.get("unlock_rule", "")):
		"east_asia":
			var need := 55
			var current := int(run_state.macro_stats.reputation)
			if current < need:
				return {"key": "reputation", "text": "缺 %d / 门槛 %d" % [need - current, need]}
		_:
			return {}
	return {}

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
	var map_nodes: Array = []
	for region in Content.REGION_DATA:
		var region_id := str(region.id)
		var region_enabled := Systems.is_region_unlocked(run_state, region)
		var region_counts := _build_region_counts(region)
		var visible_count := int(region_counts.get("visible", 0))
		var deadline_count := int(region_counts.get("deadline", 0))
		var chain_count := int(region_counts.get("chain", 0))
		var card_no := regions.size() + 1
		var region_state_line := _build_region_card_status_line(region, region_counts, region_enabled)
		var region_summary_line := _build_region_card_summary_line(region_counts)
		var region_card_style := "region_file_red" if card_no % 2 == 1 else "region_file_cyan"
		if not region_enabled:
			region_card_style = "region_locked_file"
		var region_tone := "normal"
		if not region_enabled:
			region_tone = "locked"
		elif deadline_count > 0:
			region_tone = "deadline"
		elif chain_count > 0:
			region_tone = "chain"
		regions.append({
			"id": region_id,
			"name": str(region.name),
			"hint": str(region.hint),
			"label": str(region.name),
			"text": "%02d  %s\n%s\n%s" % [card_no, str(region.name), region_state_line, region_summary_line],
			"selected": selected_region_id == region_id,
			"enabled": region_enabled,
			"unlocked": region_enabled,
			"tone": region_tone,
			"visual_style": region_card_style,
			"map_pos": region.get("map_pos", {"x": 0.5, "y": 0.5}),
			"min_height": 112.0,
		})
		if not region_enabled:
			continue
		for node in region.nodes:
			if not Systems.is_node_visible(run_state, node):
				continue
			if not bool(filter_state.get(str(node.type), true)):
				continue
			var map_availability := _get_node_availability(node)
			map_nodes.append({
				"id": str(node.id),
				"region_id": region_id,
				"region_name": str(region.name),
				"name": str(node.name),
				"kind": str(node.kind),
				"days": int(node.days),
				"type": str(node.type),
				"difficulty": str(node.difficulty),
				"enemy": int(node.enemy),
				"selected": selected_node_id == str(node.id),
				"enabled": bool(map_availability.enabled),
				"selectable": true,
				"availability_reason": str(map_availability.reason),
			})

	var nodes: Array = []
	var region := _get_selected_region()
	var region_unlocked := false
	var region_title := "取材区域"
	var region_detail_text := "请选择本周要进入的取材区域。"
	var region_hint := ""
	var region_unlock_gap := ""
	var selected_region_counts := {
		"visible": 0,
		"deadline": 0,
		"chain": 0,
		"clue": 0,
	}
	var region_summary_line := "目标 0 / 限时 0 / 线索 0 / 深链 0"
	var region_brief := "请选择本周要进入的取材区域。"
	var region_current_state := "等待选择取材地区。"
	var region_warning_title := "地区预警"
	var region_warning_text := "选择地区后显示进入条件与风险。"
	var region_footer_status := "后果：本屏不消耗天数。"
	var region_status_primary := "未选择"
	var region_status_secondary := "待选"
	var region_preview_rows: Array = []
	var region_mission_preview: Array = []
	var world_receipts: Array = []
	if not region.is_empty():
		region_unlocked = Systems.is_region_unlocked(run_state, region)
		region_title = str(region.name)
		region_hint = str(region.get("hint", ""))
		region_unlock_gap = _world_region_access_progress(region)
		selected_region_counts = _build_region_counts(region)
		region_summary_line = _build_region_detail_summary_line(selected_region_counts)
		region_brief = _build_region_brief(region, region_unlocked)
		region_current_state = _build_region_current_state(region_unlocked)
		region_warning_text = _build_region_warning_text(region, selected_region_counts, region_unlocked)
		region_footer_status = _build_region_footer_status(region_unlocked)
		region_status_primary = _build_region_status_primary(selected_region_counts, region_unlocked)
		region_status_secondary = "可进入" if region_unlocked else "暂不可进入"
		region_preview_rows = _build_region_preview_rows(region, selected_region_counts, region_unlocked)
		region_mission_preview = _build_region_mission_preview(region, region_unlocked)
		world_receipts = _build_world_region_receipts(region, selected_region_counts, region_unlocked)
		region_detail_text = _build_region_detail_text(region, region_unlocked)
		if region_unlocked:
			for node in region.nodes:
				if not Systems.is_node_visible(run_state, node):
					continue
				if not bool(filter_state.get(str(node.type), true)):
					continue
				var preview := Systems.calculate_effective_check_preview(node, selected_staff_ids)
				nodes.append({
					"id": str(node.id),
					"label": str(node.name),
					"pin_label": _node_pin_label(node),
					"text": "%s\n%s · %d天 · %s · %s" % [
						str(node.name),
						_node_card_kind_label(node),
						int(node.days),
						_compact_node_need_text(str(preview.relevant_labels)),
						str(preview.risk_label),
					],
					"selected": selected_node_id == str(node.id),
					"enabled": not bool(run_state.resolved_nodes.get(str(node.id), false)),
					"name": str(node.name),
					"kind": str(node.kind),
					"days": int(node.days),
					"type": str(node.type),
					"difficulty": str(node.difficulty),
					"enemy": int(node.enemy),
					"tone": _node_tone(node),
					"visual_style": _node_visual_style(node),
					"map_pos": node.get("map_pos", {"x": 0.5, "y": 0.5}),
					"min_height": 86.0,
				})

	var staff: Array = []
	var node_for_staff := _get_selected_node()
	var staff_pool_full := selected_staff_ids.size() >= DISPATCH_MAX_STAFF
	for staff_data in Content.STAFF_POOL:
		var staff_id := str(staff_data.id)
		var selected := selected_staff_ids.has(staff_id)
		var contribution_text := _build_staff_contribution_text(staff_data, node_for_staff)
		var staff_state_text := "点击加入本次骰池"
		var staff_visual_style := "staff_card"
		if selected:
			staff_state_text = "已入池 · 可点上方席位移出"
		elif staff_pool_full:
			staff_state_text = "席位已满 · 点上方席位移出一人"
			staff_visual_style = "staff_card_blocked_full"
		staff.append({
			"id": staff_id,
			"text": "%s · %s\n%s\n%s" % [
				str(staff_data.name),
				str(staff_data.role),
				contribution_text,
				staff_state_text,
			],
			"selected": selected,
			"enabled": not dispatch_locked,
			"visual_style": staff_visual_style,
			"min_height": 104.0,
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
		"view_mode": explore_view_mode,
		"week": run_state.week,
		"remaining_days": run_state.remaining_days,
		"new_material_count": run_state.new_material_ids.size(),
		"selected_region_id": selected_region_id,
		"selected_node_id": selected_node_id,
		"filters": filter_state.duplicate(true),
		"regions": regions,
		"map_regions": regions,
		"map_nodes": map_nodes,
		"week_days": Content.WEEK_DAYS,
		"region_title": region_title,
		"region_detail_title": region_title,
		"region_detail_text": region_detail_text,
		"region_hint": region_hint,
		"region_unlock_gap": region_unlock_gap,
		"region_unlock_gap_short": _compact_unlock_gap(region_unlock_gap),
		"region_counts": selected_region_counts,
		"region_summary_line": region_summary_line,
		"region_brief": region_brief,
		"region_current_state": region_current_state,
		"region_warning_title": region_warning_title,
		"region_warning_text": region_warning_text,
		"region_footer_status": region_footer_status,
		"region_status_primary": region_status_primary,
		"region_status_secondary": region_status_secondary,
		"region_preview_rows": region_preview_rows,
		"region_dossier_body_text": "%s\n%s" % [region_brief, region_warning_text],
		"region_mission_intel_title": str(Content.WORLD_MAP_UI_COPY["mission_intel_collapsed"]),
		"region_mission_intel_facts": "限时 %d · 线索 %d · 深链 %d" % [
			int(selected_region_counts.get("deadline", 0)),
			int(selected_region_counts.get("clue", 0)),
			int(selected_region_counts.get("chain", 0)),
		],
		"region_mission_intel_available": region_unlocked and not region_mission_preview.is_empty(),
		"region_mission_intel_locked_text": str(Content.WORLD_MAP_UI_COPY["mission_intel_locked"]),
		"region_mission_preview": region_mission_preview,
		"region_mission_preview_total": region_mission_preview.size(),
		"region_mission_preview_limit": 2,
		"world_receipts": world_receipts,
		"region_enter_enabled": region_unlocked,
		"region_mission_intel_text": str(Content.WORLD_MAP_UI_COPY["mission_intel_collapsed"]),
		"region_enter_text": str(Content.WORLD_MAP_UI_COPY["region_enter_enabled"] if region_unlocked else Content.WORLD_MAP_UI_COPY["region_enter_disabled"]),
		"dispatch_open_enabled": selected_node_id != "",
		"dispatch_open_text": "送至签批台" if selected_node_id != "" else "先选择任务",
		"nodes": nodes,
		"staff": staff,
		"selected_staff_text": _build_selected_staff_header_text(),
		"selected_staff_slots": mission_payload.selected_staff_slots,
		"materials": materials,
		"logs": logs,
		"node_title": mission_payload.node_title,
		"node_fact_text": mission_payload.summary,
		"region_node_summary": mission_payload.region_node_summary,
		"region_node_meta": mission_payload.region_node_meta,
		"region_node_deadline": mission_payload.region_node_deadline,
		"region_node_chain": mission_payload.region_node_chain,
		"region_node_risk_level": mission_payload.region_node_risk_level,
		"region_node_recommendation": mission_payload.region_node_recommendation,
		"region_action_hint": mission_payload.region_action_hint,
		"probability_text": mission_payload.probability,
		"dice_text": mission_payload.dice,
		"result_text": mission_payload.result,
		"result_color": mission_payload.color,
		"execute_enabled": mission_payload.execute_enabled,
		"execute_text": mission_payload.execute_text,
		"execute_state": mission_payload.execute_state,
	}
	_log_flow_end("_build_explore_payload", started_at, "regions=%d nodes=%d staff=%d materials=%d logs=%d" % [regions.size(), nodes.size(), staff.size(), materials.size(), logs.size()])
	return payload

func _build_region_counts(region: Dictionary) -> Dictionary:
	var counts := {
		"visible": 0,
		"deadline": 0,
		"chain": 0,
		"clue": 0,
	}
	for node in region.get("nodes", []):
		if not Systems.is_node_visible(run_state, node):
			continue
		counts["visible"] = int(counts.get("visible", 0)) + 1
		match str(node.get("kind", "permanent")):
			"temp":
				counts["deadline"] = int(counts.get("deadline", 0)) + 1
			"chain":
				counts["chain"] = int(counts.get("chain", 0)) + 1
			_:
				counts["clue"] = int(counts.get("clue", 0)) + 1
	return counts

func _world_region_access_progress(region: Dictionary) -> String:
	if Systems.is_region_unlocked(run_state, region):
		return "地区已开放。"
	match str(region.get("unlock_rule", "")):
		"east_asia":
			return "声望 %d / 55，或取得罗斯威尔残页证据。\n当前尚未取得该证据。" % int(run_state.macro_stats.reputation)
		"pacific_chain":
			return "完成北美连续追踪第 2 环。\n当前尚未完成该环节。"
	return str(region.get("unlock_gap", "尚未满足进入条件。"))

func _build_region_card_status_line(region: Dictionary, counts: Dictionary, unlocked: bool) -> String:
	if not unlocked:
		return "锁定  %s" % _compact_region_card_gap(str(region.get("unlock_gap", "缺少线索许可")))
	if int(counts.get("deadline", 0)) > 0:
		return "红线升温"
	if int(counts.get("chain", 0)) > 0:
		return "青线追踪  可推进"
	return "可进入  普通线报"

func _build_region_card_summary_line(counts: Dictionary) -> String:
	return "目标%d  限%d  线%d  深%d" % [
		int(counts.get("visible", 0)),
		int(counts.get("deadline", 0)),
		int(counts.get("clue", 0)),
		int(counts.get("chain", 0)),
	]

func _build_region_detail_summary_line(counts: Dictionary) -> String:
	return "目标 %d / 限 %d / 线 %d / 深 %d" % [
		int(counts.get("visible", 0)),
		int(counts.get("deadline", 0)),
		int(counts.get("clue", 0)),
		int(counts.get("chain", 0)),
	]

func _build_region_brief(region: Dictionary, unlocked: bool) -> String:
	var hint := str(region.get("hint", "")).strip_edges()
	if unlocked:
		hint = hint.replace("初始解锁。", "").strip_edges()
		return hint if hint != "" else "本周取材区已打开，可进入后选择具体线报。"
	return "该地区暂未开放，先补齐前置证据，再进入地区任务台。"

func _build_region_current_state(unlocked: bool) -> String:
	return "本周取材区已打开。" if unlocked else "当前地区未开封，仅显示预警。"

func _build_region_status_primary(counts: Dictionary, unlocked: bool) -> String:
	if not unlocked:
		return "锁定"
	if int(counts.get("deadline", 0)) > 0:
		return "红线升温"
	if int(counts.get("chain", 0)) > 0:
		return "青线追踪"
	return "可进入"

func _build_region_warning_text(region: Dictionary, counts: Dictionary, unlocked: bool) -> String:
	if not unlocked:
		return "缺口：%s" % _compact_region_card_gap(str(region.get("unlock_gap", "缺少线索许可")))
	if int(counts.get("deadline", 0)) > 0:
		return "存在限时任务，请进入地区查看具体截止条件。"
	if int(counts.get("chain", 0)) > 0:
		return "青线追踪会推进后续地区。"
	return "暂无额外惩罚。"

func _build_region_footer_status(unlocked: bool) -> String:
	return "后果：进入地区任务台，本屏不消耗天数。" if unlocked else "后果：暂不能进入，选择不消耗天数。"

func _build_region_preview_rows(region: Dictionary, counts: Dictionary, unlocked: bool) -> Array:
	var rows: Array = []
	if unlocked:
		if int(counts.get("deadline", 0)) > 0:
			rows.append({"tone": "deadline", "text": "存在限时任务，请查看具体截止条件。"})
		if int(counts.get("chain", 0)) > 0:
			rows.append({"tone": "chain", "text": "青线追踪会推进地区缺口。"})
		rows.append({"tone": "selected", "text": "进入后再选择具体线报。"})
	else:
		rows.append({"tone": "locked", "text": "锁定地区只展示预警与缺口。"})
		rows.append({"tone": "locked", "text": "缺口：%s" % _compact_unlock_gap(str(region.get("unlock_gap", "缺少线索许可")))})
		rows.append({"tone": "selected", "text": "先在已开封地区补齐前置证据。"})
	return rows

func _build_region_mission_preview(region: Dictionary, unlocked: bool) -> Array:
	var rows: Array = []
	if not unlocked:
		return rows
	for node in region.get("nodes", []):
		if not Systems.is_node_visible(run_state, node):
			continue
		rows.append({
			"id": str(node.get("id", "")),
			"name": str(node.get("name", "未命名任务")),
			"kind": str(node.get("kind", "permanent")),
			"kind_label": _world_mission_kind_label(node),
			"days": int(node.get("days", 0)),
		})
	return rows

func _world_mission_kind_label(node: Dictionary) -> String:
	match str(node.get("kind", "permanent")):
		"temp":
			return "限时"
		"chain":
			return "深链"
		"hidden":
			return "异常"
		_:
			return "线索"

func _build_world_region_receipts(region: Dictionary, counts: Dictionary, unlocked: bool) -> Array:
	var receipts: Array = []
	if unlocked:
		var change_text := "一处城市频道升温" if int(counts.get("deadline", 0)) > 0 else "地区情报已归档"
		receipts.append({"title": "最近变化", "body": change_text, "variant": "deadline" if int(counts.get("deadline", 0)) > 0 else "selected"})
		receipts.append({"title": "地区异动", "body": "红线 %d / 青线 %d" % [int(counts.get("deadline", 0)), int(counts.get("chain", 0))], "variant": "chain"})
		receipts.append({"title": "地区预警", "body": "进入后再选择线报", "variant": "selected"})
	else:
		receipts.append({"title": "最近变化", "body": "锁定档案保留", "variant": "locked"})
		receipts.append({"title": "地区异动", "body": "目标 %d / 缺口未补" % int(counts.get("visible", 0)), "variant": "locked"})
		receipts.append({"title": "地区预警", "body": _compact_unlock_gap(str(region.get("unlock_gap", "缺少线索许可"))), "variant": "locked"})
	return receipts

func _compact_region_hint(value: String) -> String:
	var text := value.replace("。", " · ").strip_edges()
	text = text.replace("初始解锁 · 都市传说与军事封锁交叠", "初始解锁")
	if text.ends_with("·"):
		text = text.substr(0, text.length() - 1).strip_edges()
	if text.length() > 18:
		text = text.substr(0, 17) + "…"
	return text

func _compact_unlock_gap(value: String) -> String:
	var text := value
	if text.contains("罗斯威尔"):
		return "声望≥55 / 罗斯威尔残页"
	if text.contains("北美禁区带连续追踪"):
		return "北美追踪第 2 环 / 线人许可"
	text = text.replace("缺口：", "")
	text = text.replace("完成北美禁区带连续追踪第 2 环，或取得可靠线人许可。", "完成北美追踪第 2 环 / 线人许可")
	text = text.replace("声望≥55 或拿到罗斯威尔档案残页证据。", "声望≥55 / 罗斯威尔残页")
	text = text.replace("声望≥55，或先拿到罗斯威尔档案残页证据。", "声望≥55 / 罗斯威尔残页")
	text = text.replace("缺少进入该区域的线索缺口。", "缺少线索许可")
	if text.length() > 28:
		text = text.substr(0, 27) + "…"
	return text

func _compact_region_card_gap(value: String) -> String:
	if value.contains("罗斯威尔"):
		return "声望≥55 / 残页"
	if value.contains("北美禁区带连续追踪"):
		return "追踪第2环 / 许可"
	var text := _compact_unlock_gap(value)
	if text.length() > 14:
		text = text.substr(0, 13) + "…"
	return text

func _compact_node_need_text(value: String) -> String:
	var text := value.replace("，", "/").replace(",", "/").replace(" / ", "/").strip_edges()
	text = text.replace("探索", "探")
	text = text.replace("洞察", "察")
	text = text.replace("诡思", "诡")
	text = text.replace("生存", "生")
	text = text.replace("理性", "理")
	text = text.replace("社交", "社")
	if text.length() > 8:
		text = text.substr(0, 7) + "…"
	return text

func _build_mission_payload() -> Dictionary:
	var default_payload := {
		"node_title": "选择取材任务",
		"region_node_summary": "选择一份任务档案，查看线索、耗时和风险。",
		"region_node_meta": "",
		"region_node_deadline": "",
		"region_node_chain": "",
		"region_node_risk_level": "",
		"region_node_recommendation": "",
		"region_action_hint": "选择后送至签批台配置骰池，本页不消耗天数。",
		"summary": "选择一份任务档案，查看线索、耗时和风险。",
		"probability": "有效点：等待选人",
		"dice": "",
		"result": "等待执行",
		"color": Color(0.88, 0.76, 0.36, 1.0),
		"execute_enabled": false,
		"execute_text": "签批外勤",
		"execute_state": "idle",
		"selected_staff_slots": _build_selected_staff_slots(),
	}
	var node := _get_selected_node()
	if node.is_empty():
		return default_payload

	var preview := Systems.calculate_effective_check_preview(node, selected_staff_ids)
	var probabilities := Systems.calculate_node_probabilities(node, selected_staff_ids)
	var availability := _get_node_availability(node)
	var review_rows := _build_dispatch_review_rows(node, preview, availability)
	var dice_detail := "[b]回报[/b] 线索 / 现象 / 情报引用\n[b]失败[/b] %s\n[b]分布[/b] 大 %.0f%% · 可用 %.0f%% · 失 %.0f%%" % [
		"只带回弱线索或推进压力" if str(node.kind) != "temp" else "截稿机会关闭，只留下残缺素材",
		float(probabilities.major) * 100.0,
		float(probabilities.minor) * 100.0,
		float(probabilities.fail) * 100.0,
	]
	default_payload.node_title = str(node.name)
	default_payload.region_node_summary = str(node.description)
	default_payload.region_node_meta = "%s · 需求 %s · %d天" % [
		_node_card_kind_label(node),
		_compact_node_need_text(str(preview.relevant_labels)),
		int(node.days),
	]
	default_payload.region_node_risk_level = str(preview.risk_label)
	default_payload.region_node_recommendation = "建议：优先配置 %s；签批台复核达标率。" % str(preview.relevant_labels)
	default_payload.region_action_hint = "送至签批台配置骰池，本页不消耗天数。"
	default_payload.summary = "[b]线报摘要[/b]\n%s\n[color=#8c6d2d]需求[/color] %s · [color=#8c6d2d]耗时[/color] %d天" % [
		str(node.description),
		str(preview.relevant_labels),
		int(node.days),
	]
	if node.has("deadline_day"):
		var deadline_remaining := maxi(0, int(run_state.remaining_days) - int(node.get("deadline_day", 0)) + 1)
		default_payload.region_node_deadline = "截稿剩 %d 天" % deadline_remaining
		default_payload.summary += "\n[color=#b72a22]截稿剩 %d 天。[/color]" % deadline_remaining
	if str(node.kind) == "chain":
		default_payload.region_node_chain = "连续追踪：成功后出现后续线索"
		default_payload.summary += "\n[color=#087b85]连续追踪：成功后出现后续线索。[/color]"
	default_payload.probability = "有效点 %d / 目标 %d · 达标率 %.0f%% · 风险：%s" % [
		int(preview.potential_points),
		int(preview.target),
		float(preview.success_rate) * 100.0,
		str(preview.risk_label),
	]
	default_payload.dice = _format_dispatch_review_text(review_rows, dice_detail)
	default_payload.execute_enabled = bool(availability.enabled) and not dispatch_locked
	default_payload.execute_text = "签批外勤"
	default_payload.execute_state = dispatch_signoff_state
	if not bool(availability.enabled):
		default_payload.result = str(availability.reason)
		default_payload.color = Color(0.94, 0.52, 0.46, 1.0)
	else:
		default_payload.result = "本次配置可签批；签批后将消耗天数并回收素材。"
		default_payload.color = Color(0.62, 0.86, 0.70, 1.0)
	if dispatch_notice_text != "":
		default_payload.result = dispatch_notice_text + "\n" + str(default_payload.result)
	if dispatch_signoff_state == "loading":
		default_payload.execute_enabled = false
		default_payload.execute_text = "签批中..."
		default_payload.result = "签批中：主编正在核准外勤单。"
		default_payload.color = Color(0.88, 0.76, 0.36, 1.0)
	elif dispatch_signoff_state == "stamped":
		default_payload.execute_enabled = false
		default_payload.execute_text = "已盖章"
		default_payload.result = "已盖章：外勤单已送出，正在回收素材。"
		default_payload.color = Color(0.62, 0.86, 0.70, 1.0)

	if not run_state.last_dispatch_roll.is_empty() and str(run_state.last_dispatch_roll.get("node_id", "")) == str(node.id):
		default_payload.dice = _format_roll_text(run_state.last_dispatch_roll)
		default_payload.result = _build_roll_result_text(run_state.last_dispatch_roll)
		default_payload.color = _build_roll_result_color(run_state.last_dispatch_roll)
	return default_payload

func _build_selected_staff_slots() -> Array:
	var slots: Array = []
	for index in range(DISPATCH_MAX_STAFF):
		if index < selected_staff_ids.size():
			var staff_id := str(selected_staff_ids[index])
			var staff_data := _get_staff_data(staff_id)
			var staff_name := str(staff_data.get("name", staff_id))
			var staff_role := str(staff_data.get("role", "已选队员"))
			slots.append({
				"id": staff_id,
				"name": staff_name,
				"body": "%s · 点此移出" % staff_role,
				"filled": true,
				"index": index,
			})
		else:
			slots.append({
				"id": "",
				"name": "空席位 %d" % [index + 1],
				"body": "从候选队员中加入",
				"filled": false,
				"index": index,
			})
	return slots

func _build_selected_staff_header_text() -> String:
	if selected_staff_ids.size() >= DISPATCH_MAX_STAFF:
		return "本次骰池 %d / %d · 点席位移出" % [selected_staff_ids.size(), DISPATCH_MAX_STAFF]
	return "本次骰池 %d / %d" % [selected_staff_ids.size(), DISPATCH_MAX_STAFF]

func _build_dispatch_review_rows(node: Dictionary, preview: Dictionary, availability: Dictionary) -> Array:
	var rows: Array = []
	var staff_count := selected_staff_ids.size()
	var staff_tone := "ok"
	var staff_value := "已选 %d/%d，可继续补人" % [staff_count, DISPATCH_MAX_STAFF]
	if staff_count == 0:
		staff_tone = "block"
		staff_value = "未选择队员"
	elif staff_count >= DISPATCH_MAX_STAFF:
		staff_tone = "warn"
		staff_value = "已满 %d/%d，换人需先移出" % [staff_count, DISPATCH_MAX_STAFF]
	rows.append({"label": "队员席位", "value": staff_value, "tone": staff_tone})

	var task_days := int(node.get("days", 0))
	var signed_remaining := run_state.remaining_days - task_days
	var days_ok := signed_remaining >= 0
	var days_value := "本周 %d -> 签后 %d（耗 %d）" % [run_state.remaining_days, max(0, signed_remaining), task_days]
	if not days_ok:
		days_value = "本周剩 %d 天 / 需 %d 天" % [run_state.remaining_days, task_days]
	rows.append({
		"label": "耗时核对",
		"value": days_value,
		"tone": "ok" if days_ok else "block",
	})

	var coverage_tone := "ok"
	var coverage_value := "有效上限 %d / 目标 %d" % [int(preview.get("potential_points", 0)), int(preview.get("target", 0))]
	if staff_count == 0:
		coverage_tone = "block"
		coverage_value = "等待选人后计算需求覆盖"
	elif int(preview.get("potential_points", 0)) < int(preview.get("target", 0)):
		coverage_tone = "block"
	rows.append({"label": "需求覆盖", "value": coverage_value, "tone": coverage_tone})

	var node_done := str(node.get("kind", "permanent")) != "permanent" and bool(run_state.resolved_nodes.get(str(node.get("id", "")), false))
	var deadline_ok := not node.has("deadline_day") or run_state.remaining_days >= int(node.get("deadline_day", 0))
	var task_tone := "ok"
	var task_value := "任务可派"
	if node_done:
		task_tone = "block"
		task_value = "本周已处理"
	elif not deadline_ok:
		task_tone = "block"
		task_value = "截稿窗口已关闭"
	rows.append({"label": "任务档案", "value": task_value, "tone": task_tone})

	if not bool(availability.get("enabled", false)):
		rows.append({"label": "主编复核", "value": str(availability.get("reason", "不可签批")), "tone": "block"})
	elif dispatch_signoff_state == "loading":
		rows.append({"label": "主编复核", "value": "签批中，等待盖章", "tone": "warn"})
	else:
		rows.append({"label": "主编复核", "value": "签批条件已齐", "tone": "ok"})

	if dispatch_notice_text != "":
		rows.append({"label": "操作反馈", "value": dispatch_notice_text, "tone": "warn"})
	return rows

func _format_dispatch_review_text(rows: Array, dice_detail: String) -> String:
	var lines: Array[String] = ["[b]签批复核[/b]"]
	for row in _sort_dispatch_review_rows(rows):
		var tone := str(row.get("tone", "ok"))
		var label := str(row.get("label", ""))
		var value := str(row.get("value", ""))
		if tone == "block":
			lines.append("[color=#f59a8b][b]阻断[/b][/color] %s：%s" % [label, value])
		elif tone == "warn":
			lines.append("[color=#f0d8a0][b]注意[/b][/color] %s：%s" % [label, value])
		else:
			lines.append("[color=#8ecf9a]· %s：%s[/color]" % [label, value])
	if dice_detail != "":
		lines.append("\n%s" % dice_detail)
	return _join_strings(lines, "\n")

func _sort_dispatch_review_rows(rows: Array) -> Array:
	var ordered: Array = []
	for tone in ["block", "warn", "ok"]:
		for row in rows:
			if typeof(row) == TYPE_DICTIONARY and str(row.get("tone", "ok")) == tone:
				ordered.append(row)
	return ordered

func _build_region_detail_text(region: Dictionary, unlocked: bool) -> String:
	var visible_count := 0
	var deadline_count := 0
	var chain_count := 0
	for node in region.get("nodes", []):
		if Systems.is_node_visible(run_state, node):
			visible_count += 1
			if str(node.kind) == "temp":
				deadline_count += 1
			if str(node.kind) == "chain":
				chain_count += 1
	var lines: Array[String] = []
	if unlocked:
		lines.append("[color=#087b85]编辑按语[/color]\n[color=#27352f]可进入 · 本区线报 %d[/color]" % visible_count)
		lines.append("[color=#087b85]为什么进这里[/color]\n[color=#27352f]%s[/color]" % str(region.get("hint", "")))
		lines.append("[color=#087b85]进入后能做[/color]\n[color=#27352f]可挑选 %d 张区域选题，再送到派遣签批台。[/color]" % visible_count)
	else:
		lines.append("[color=#087b85]决策摘要[/color]\n[color=#4d5c58]未开封 · 缺口待补 · 不消耗天数[/color]")
		lines.append("[color=#087b85]为什么先放回索引柜[/color]\n[color=#27352f]%s[/color]" % str(region.get("hint", "")))
		lines.append("[color=#087b85]锁定缺口[/color]\n[color=#6a7773]%s[/color]" % str(region.get("unlock_gap", "缺少进入该区域的线索缺口。")))
		lines.append("[color=#6a7773]锁定区只做缺口预览，不展开任务卡。[/color]")
	return _join_strings(lines, "\n\n")

func _node_pin_label(node: Dictionary) -> String:
	var kind := "常驻"
	match str(node.get("kind", "permanent")):
		"temp":
			kind = "截稿"
		"chain":
			kind = "追踪"
		"hidden":
			kind = "异常"
	return "%s\n%s" % [kind, str(node.get("name", "节点"))]

func _node_kind_label(node: Dictionary) -> String:
	var kind := "常驻调查"
	match str(node.get("kind", "permanent")):
		"temp":
			kind = "限时截稿"
		"chain":
			kind = "连续追踪"
		"hidden":
			kind = "灵视异常"
	var tag: String = str(Content.TAG_LABELS.get(str(node.get("type", "")), str(node.get("type", ""))))
	return "%s · %s" % [kind, str(tag)]

func _node_card_kind_label(node: Dictionary) -> String:
	var kind := "常驻"
	match str(node.get("kind", "permanent")):
		"temp":
			kind = "截稿"
		"chain":
			kind = "追踪"
		"hidden":
			kind = "异常"
	var tag: String = str(Content.TAG_LABELS.get(str(node.get("type", "")), str(node.get("type", ""))))
	return "%s/%s" % [kind, str(tag)]

func _node_tone(node: Dictionary) -> String:
	match str(node.get("kind", "permanent")):
		"temp":
			return "deadline"
		"chain":
			return "chain"
		"hidden":
			return "locked"
		_:
			return "normal"

func _node_visual_style(node: Dictionary) -> String:
	match str(node.get("kind", "permanent")):
		"temp":
			return "node_deadline"
		"chain":
			return "node_chain"
		_:
			return "node_file"

func _build_staff_contribution_text(staff_data: Dictionary, node: Dictionary) -> String:
	if node.is_empty():
		var attrs: Array[String] = []
		for key in ["explore", "insight", "occult", "survival", "reason", "social"]:
			attrs.append("%s %d" % [str(Content.ATTR_LABELS.get(key, key)), int(staff_data.attrs[key])])
		return "等待节点 · %s" % _join_strings(attrs.slice(0, 3), " / ")
	var relevant_attrs: Array = node.get("need", {}).keys()
	var faces: Array = staff_data.get("faces", [])
	var relevant_faces: Array[String] = []
	var best_points := 0
	var best_label := ""
	for face in faces:
		var attr := str(face.get("attr", ""))
		if relevant_attrs.has(attr):
			var points := int(face.get("points", 1))
			var face_label := "%s+%d" % [str(Content.ATTR_LABELS.get(attr, attr)), points]
			if points > best_points:
				best_points = points
				best_label = face_label
			relevant_faces.append(face_label)
	if relevant_faces.is_empty():
		return "无相关骰面 · 本次不建议"
	return "相关 %d/6 · 最高 %s" % [relevant_faces.size(), best_label]

func _build_editorial_payload() -> Dictionary:
	var articles: Array = []
	for article in run_state.article_candidates:
		var article_id := int(article.id)
		var placed_slot_id := ""
		var placed_slot_name := ""
		for slot in Content.SLOT_DATA:
			if int(run_state.slot_assignment.get(str(slot.id), -1)) == article_id:
				placed_slot_id = str(slot.id)
				placed_slot_name = str(slot.name)
				break
		articles.append({
			"id": article_id,
			"code": "A%02d" % (article_id % 100),
			"title": str(article.title),
			"tags": article.tags.duplicate(),
			"quality": str(article.quality),
			"base_value": int(article.base_value),
			"placed_slot": placed_slot_id,
			"placed_slot_name": placed_slot_name,
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
		var article_id := int(article.get("id", -1)) if not article.is_empty() else -1
		var slot_text := ""
		if article.is_empty():
			slot_text = "%s · x%.2f\n%s\n点击这里放置当前选中的稿件" % [str(slot.name), float(slot.weight), str(slot.desc)]
		else:
			slot_text = "%s · x%.2f\n%s\n%s · %s" % [str(slot.name), float(slot.weight), str(article.title), str(article.quality), _join_strings(article.tags, " / ")]
		slots.append({
			"id": str(slot.id),
			"name": str(slot.name),
			"weight": float(slot.weight),
			"description": str(slot.desc),
			"page_id": "left" if str(slot.id) in ["front-main", "feature-1", "feature-2"] else "right",
			"role": "main_head" if str(slot.id) == "front-main" else "secondary_head" if str(slot.id) == "front-side" else "standard_story",
			"article_id": article_id,
			"article_title": str(article.get("title", "")),
			"quality": str(article.get("quality", "")),
			"tags": article.get("tags", []).duplicate(),
			"text": slot_text,
			"selected": selected_article_id != -1,
			"enabled": true,
			"min_height": 84.0,
		})

	var stats := Systems.build_settlement_preview(run_state, run_state.slot_assignment)
	run_state.settlement_preview = stats.duplicate(true)
	return {
		"issue": run_state.week,
		"subtitle": "本周新增素材 %d 条，可转化候选稿件 %d 篇。正式切片只暴露候选稿与版面映射。" % [run_state.new_material_ids.size(), run_state.article_candidates.size()],
		"articles": articles,
		"slots": slots,
		"held_article_id": selected_article_id,
		"assignments": run_state.slot_assignment.duplicate(true),
		"stats": stats.duplicate(true),
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
	lines.append("[b]本次骰池[/b] 有效点 %d / 目标 %d · %s" % [
		int(roll.get("effective_points", 0)),
		int(roll.get("target", 0)),
		str(roll.get("risk_label", "")),
	])
	for face in roll.get("faces", []):
		var marker := "x"
		if bool(face.get("effective", false)):
			marker = "+%d" % int(face.get("points", 0))
		lines.append("%s：%s %s" % [str(face.get("staff_name", "")), str(face.get("label", "")), marker])
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
	return "%s · 有效点 %d/%d · 预估达标率 %.0f%%" % [
		str(tier_map.get(str(roll.get("tier", "fail")), "失败")),
		int(roll.get("effective_points", 0)),
		int(roll.get("target", 0)),
		float(roll.get("success_rate", 0.0)) * 100.0,
	]

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
	selected_staff_ids.clear()
	explore_view_mode = "world"
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
	_refresh_all()

func _on_enter_region_requested() -> void:
	var region := _get_selected_region()
	if region.is_empty() or not Systems.is_region_unlocked(run_state, region):
		_refresh_all()
		return
	explore_view_mode = "region"
	selected_node_id = ""
	selected_staff_ids.clear()
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
	_refresh_all()

func _on_back_to_world_requested() -> void:
	explore_view_mode = "world"
	selected_node_id = ""
	selected_staff_ids.clear()
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
	_refresh_all()

func _on_back_to_region_requested() -> void:
	explore_view_mode = "region"
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
	_refresh_all()

func _on_node_pressed(node_id: String) -> void:
	var started_at := _log_flow_start("_on_node_pressed", "incoming_node=%s previous_node=%s" % [node_id, selected_node_id])
	var owning_region_id := _get_region_id_for_node(node_id)
	if owning_region_id != "":
		selected_region_id = owning_region_id
	explore_view_mode = "region"
	if selected_node_id != node_id:
		selected_staff_ids.clear()
		dispatch_notice_text = ""
		dispatch_signoff_state = "idle"
	selected_node_id = node_id
	_refresh_all()
	_log_flow_end("_on_node_pressed", started_at, "selected_node=%s" % selected_node_id)

func _on_open_dispatch_requested() -> void:
	if selected_node_id == "":
		_refresh_all()
		return
	var node := _get_selected_node()
	if node.is_empty():
		selected_node_id = ""
		_refresh_all()
		return
	explore_view_mode = "dispatch"
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
	_refresh_all()

func _on_article_selected(article_id: int) -> void:
	selected_article_id = -1 if selected_article_id == article_id else article_id
	_refresh_all()

func _toggle_staff(staff_id: String) -> void:
	if dispatch_locked:
		dispatch_notice_text = "签批中，暂不能调整本次骰池。"
		_refresh_all()
		return
	var staff_data := _get_staff_data(staff_id)
	var staff_name := str(staff_data.get("name", staff_id))
	dispatch_signoff_state = "idle"
	if selected_staff_ids.has(staff_id):
		selected_staff_ids.erase(staff_id)
		dispatch_notice_text = "已将 %s 移出本次骰池。" % staff_name
	elif selected_staff_ids.size() < DISPATCH_MAX_STAFF:
		selected_staff_ids.append(staff_id)
		dispatch_notice_text = "已将 %s 加入本次骰池。" % staff_name
	else:
		dispatch_notice_text = "本次骰池已满，请点上方已选席位移出一人，再加入 %s。" % staff_name
	_refresh_all()

func _on_advance_phase_pressed() -> void:
	if run_state.current_phase == "briefing":
		Systems.start_explore(run_state)
		explore_view_mode = "world"
		dispatch_locked = false
		dispatch_notice_text = ""
		dispatch_signoff_state = "idle"
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
	if dispatch_locked:
		dispatch_notice_text = "签批中，暂不能重复提交。"
		_refresh_all()
		_log_flow_end("_on_execute_pressed", started_at, "dispatch locked")
		return
	var node := _get_selected_node()
	if node.is_empty():
		dispatch_notice_text = "当前任务丢失，请返回区域任务台重选。"
		_refresh_all()
		_log_flow_end("_on_execute_pressed", started_at, "selected_node missing")
		return
	var availability := _get_node_availability(node)
	if not bool(availability.enabled):
		dispatch_notice_text = "签批被拦下：%s" % str(availability.reason)
		run_state.append_log("[color=#f59a8b]%s[/color]" % dispatch_notice_text)
		_refresh_all()
		_log_flow_end("_on_execute_pressed", started_at, "blocked=%s" % str(availability.reason))
		return
	dispatch_locked = true
	dispatch_signoff_state = "loading"
	dispatch_notice_text = "签批中：主编正在核准外勤单。"
	_refresh_all()
	await get_tree().create_timer(0.18).timeout
	dispatch_signoff_state = "stamped"
	dispatch_notice_text = "已盖章：外勤单已送出，正在回收素材。"
	_refresh_all()
	await get_tree().create_timer(0.18).timeout
	var roll := Systems.perform_effective_point_check(node, selected_staff_ids)
	var outcome := Systems.apply_dispatch_resolution(run_state, material_inventory, node, roll, str(_get_selected_region().name))
	run_state.append_log("[color=#f0d8a0]%s[/color]：%s" % [str(node.name), str(outcome.message)])
	run_state.append_log("素材入库：[color=#9fd4ff]%s[/color]" % str(outcome.material.title))
	dispatch_locked = false
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
	explore_view_mode = "region"
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
	_apply_editorial_transfer("candidate", selected_article_id, "", "slot", slot_id)


func _apply_editorial_transfer(source_kind: String, article_id: int, source_slot_id: String, destination_kind: String, destination_slot_id: String) -> void:
	if run_state.current_phase != "editorial" or article_id == -1:
		return
	if source_kind not in ["candidate", "slot"] or destination_kind not in ["slot", "candidate_pool"]:
		return
	var valid_slot_ids: Array[String] = []
	for slot in Content.SLOT_DATA:
		valid_slot_ids.append(str(slot.id))
	if source_kind == "slot":
		if source_slot_id not in valid_slot_ids or int(run_state.slot_assignment.get(source_slot_id, -1)) != article_id:
			return
	elif _is_article_placed(article_id):
		return
	if destination_kind == "candidate_pool":
		if source_kind != "slot":
			return
		var removed_assignment: Dictionary = run_state.slot_assignment.duplicate(true)
		removed_assignment[source_slot_id] = -1
		if not _editorial_assignment_is_unique(removed_assignment):
			return
		run_state.slot_assignment = removed_assignment
		selected_article_id = -1
		_refresh_all()
		return
	if destination_slot_id not in valid_slot_ids:
		return
	if source_kind == "slot" and source_slot_id == destination_slot_id:
		selected_article_id = -1
		_refresh_all()
		return
	var next_assignment: Dictionary = run_state.slot_assignment.duplicate(true)
	var target_article_id := int(next_assignment.get(destination_slot_id, -1))
	if source_kind == "candidate":
		next_assignment[destination_slot_id] = article_id
	else:
		next_assignment[source_slot_id] = target_article_id
		next_assignment[destination_slot_id] = article_id
	if not _editorial_assignment_is_unique(next_assignment):
		return
	run_state.slot_assignment = next_assignment
	selected_article_id = -1
	_refresh_all()


func _editorial_assignment_is_unique(assignments: Dictionary) -> bool:
	var seen: Dictionary = {}
	for value in assignments.values():
		var assigned_article_id := int(value)
		if assigned_article_id == -1:
			continue
		if seen.has(assigned_article_id):
			return false
		seen[assigned_article_id] = true
	return true

func _clear_layout() -> void:
	for slot in Content.SLOT_DATA:
		run_state.slot_assignment[str(slot.id)] = -1
	selected_article_id = -1
	_refresh_all()

func _clear_editorial_slot(slot_id: String) -> void:
	if not run_state.slot_assignment.has(slot_id):
		return
	run_state.slot_assignment[slot_id] = -1
	selected_article_id = -1
	_refresh_all()

func _cancel_editorial_selection() -> void:
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
	explore_view_mode = "world"
	dispatch_locked = false
	dispatch_notice_text = ""
	dispatch_signoff_state = "idle"
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
	if selected_region.is_empty():
		selected_region_id = _default_region_id()
		return
	if explore_view_mode in ["region", "dispatch"] and not Systems.is_region_unlocked(run_state, selected_region):
		explore_view_mode = "world"
		selected_node_id = ""

func _ensure_valid_node_selection() -> void:
	if selected_node_id == "":
		if explore_view_mode == "dispatch":
			explore_view_mode = "region"
		return
	var region := _get_selected_region()
	if region.is_empty() or not Systems.is_region_unlocked(run_state, region):
		selected_node_id = ""
		if explore_view_mode == "dispatch":
			explore_view_mode = "region"
		return
	var node := _get_selected_node()
	if node.is_empty():
		selected_node_id = ""
		if explore_view_mode == "dispatch":
			explore_view_mode = "region"
		return
	if not Systems.is_node_visible(run_state, node) or not bool(filter_state.get(str(node.type), true)):
		selected_node_id = ""
		if explore_view_mode == "dispatch":
			explore_view_mode = "region"

func _get_selected_region() -> Dictionary:
	return Systems.get_region_by_id(selected_region_id)

func _get_selected_node() -> Dictionary:
	return Systems.get_node_by_id(selected_region_id, selected_node_id)

func _get_staff_data(staff_id: String) -> Dictionary:
	for staff_data in Content.STAFF_POOL:
		if str(staff_data.get("id", "")) == staff_id:
			return staff_data
	return {}

func _get_region_id_for_node(node_id: String) -> String:
	for region in Content.REGION_DATA:
		for node in region.nodes:
			if str(node.id) == node_id:
				return str(region.id)
	return ""

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
	_log_message("WeeklyRunGame", "%s START %s" % [flow_name, details])
	return started_at

func _log_flow_end(flow_name: String, started_at: int, details: String = "") -> void:
	var elapsed_ms := float(Time.get_ticks_usec() - started_at) / 1000.0
	_log_message("WeeklyRunGame", "%s END %.2fms %s" % [flow_name, elapsed_ms, details])

func _get_globals_singleton() -> Object:
	if Engine.has_singleton("Globals"):
		return Engine.get_singleton("Globals")
	return null

func _log_message(scene_name: String, message: String) -> void:
	var globals := _get_globals_singleton()
	if globals != null and globals.has_method("log"):
		globals.call("log", scene_name, message)
