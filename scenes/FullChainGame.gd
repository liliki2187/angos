extends Control

const DIFFICULTY_P := {
	"easy": 0.60,
	"normal": 0.50,
	"hard": 1.0 / 3.0,
}

const MACRO_LABELS := [
	{"key": "credibility", "label": "公信"},
	{"key": "weirdness", "label": "诡名"},
	{"key": "reputation", "label": "声望"},
	{"key": "order", "label": "守序"},
	{"key": "mania", "label": "狂性"},
]

const SLOT_DATA := [
	{"id": "front-main", "name": "头版头条", "weight": 1.00, "desc": "最高曝光，承担本期调性。"},
	{"id": "front-side", "name": "头版次条", "weight": 0.70, "desc": "高曝光，适合补足主话题。"},
	{"id": "feature-1", "name": "重点专题 A", "weight": 0.45, "desc": "适合高价值调查稿。"},
	{"id": "feature-2", "name": "重点专题 B", "weight": 0.40, "desc": "适合做题材连携。"},
	{"id": "inner-1", "name": "内页 A", "weight": 0.20, "desc": "标准曝光，适合补多样性。"},
	{"id": "inner-2", "name": "内页 B", "weight": 0.20, "desc": "标准曝光，适合边缘稿件。"},
]

const STAFF_POOL := [
	{"id": "ivy", "name": "艾薇·冷烛", "role": "外采调查", "attrs": {"explore": 5, "insight": 4, "occult": 2, "survival": 3, "reason": 3, "social": 2}},
	{"id": "qiao", "name": "乔然", "role": "城市跑口", "attrs": {"explore": 3, "insight": 4, "occult": 1, "survival": 2, "reason": 5, "social": 4}},
	{"id": "mora", "name": "莫拉", "role": "灵视记者", "attrs": {"explore": 2, "insight": 3, "occult": 5, "survival": 2, "reason": 2, "social": 3}},
	{"id": "reed", "name": "里德", "role": "战地摄影", "attrs": {"explore": 4, "insight": 2, "occult": 1, "survival": 5, "reason": 3, "social": 2}},
]

const REGION_DATA := [
	{
		"id": "us",
		"name": "北美禁区带",
		"hint": "初始解锁。都市传说与军事封锁交叠。",
		"unlock_rule": "always",
		"nodes": [
			{"id": "n51", "name": "51 区外围公路", "kind": "permanent", "days": 2, "type": "sci", "difficulty": "normal", "enemy": 2, "k_a": 3, "k_b": 2, "need": {"explore": 4, "survival": 2}, "description": "围绕夜间封锁和可疑货运展开跟拍，寻找能上头版的实证。", "risk_text": "军方与保安巡逻频繁。"},
			{"id": "skin", "name": "罗斯威尔档案残页", "kind": "permanent", "days": 1, "type": "sci", "difficulty": "normal", "enemy": 1, "k_a": 2, "k_b": 2, "need": {"insight": 3, "reason": 3}, "description": "在档案馆和旧报社之间追索失踪页。", "risk_text": "成功质量决定后续区域解锁速度。"},
			{"id": "temp_ufo", "name": "突发：雷达异常光点", "kind": "temp", "days": 2, "type": "pop", "difficulty": "hard", "enemy": 3, "k_a": 4, "k_b": 3, "deadline_day": 4, "need": {"explore": 5, "survival": 3}, "description": "城市雷达站刚刚记录到异常光点，热度高但窗口极短。", "risk_text": "过期即消失。"},
			{"id": "hidden_gate", "name": "灵视：黑色方尖碑的回声", "kind": "hidden", "days": 3, "type": "occult", "difficulty": "normal", "enemy": 4, "k_a": 4, "k_b": 2, "unlock_rule": "hidden_monolith", "need": {"occult": 4, "survival": 2}, "description": "当诡名与狂性同时越界，灵视记者会听见来自沙海的回声。", "risk_text": "失败会推高狂性。"},
		],
	},
	{
		"id": "east_asia",
		"name": "东亚神秘地带",
		"hint": "需要：声望≥55 或拿到罗斯威尔残页证据。",
		"unlock_rule": "east_asia",
		"nodes": [
			{"id": "harbor_echo", "name": "港口回声仓栈", "kind": "permanent", "days": 2, "type": "pop", "difficulty": "normal", "enemy": 2, "k_a": 3, "k_b": 2, "need": {"social": 3, "reason": 3}, "description": "跟随码头流言和失踪航运记录，拼出被压下来的新闻源。", "risk_text": "适合补足大众关注。"},
			{"id": "mountain_signal", "name": "山中电台失踪案", "kind": "permanent", "days": 3, "type": "occult", "difficulty": "hard", "enemy": 3, "k_a": 4, "k_b": 3, "need": {"explore": 4, "occult": 3, "survival": 3}, "description": "沿着废弃电台的短波干扰深入山谷。", "risk_text": "高风险高回报。"},
		],
	},
]

const STORY_TAG_MAP := {
	"sci": ["Politics", "Military", "Economy"],
	"occult": ["Gossip", "Pets", "Humor"],
	"pop": ["Sport", "Shopping", "Gossip"],
}

const QUALITY_MAP := {
	1: {"quality": "Bronze", "base_value": 150},
	2: {"quality": "Silver", "base_value": 300},
	3: {"quality": "Gold", "base_value": 450},
}

const ATTR_LABELS := {
	"explore": "探索",
	"insight": "洞察",
	"occult": "诡思",
	"survival": "生存",
	"reason": "理性",
	"social": "社交",
}

const TAG_LABELS := {
	"sci": "科学纪实",
	"occult": "神秘玄学",
	"pop": "大众热度",
}

const FILLER_SUBJECTS := {
	"Politics": ["预算案风波", "地方选举震荡", "安全听证泄密", "市政采购黑幕"],
	"Military": ["边境演训记录", "驻防调整谣言", "军备采购追踪", "哨所口供残卷"],
	"Economy": ["码头物流停摆", "黑市金价异动", "厂区裁员余震", "消费指数回落"],
	"Sport": ["主场重建争议", "联赛爆冷", "俱乐部内幕", "冠军游行失控"],
	"Gossip": ["名流秘会", "夜宴侧录", "家族婚约风波", "演员罢演内幕"],
	"Pets": ["宠物诊所失踪案", "街区猫狗热潮", "罕见生物传闻", "流浪犬收容争议"],
	"Humor": ["荒诞榜单", "街头怪谈栏目", "讽刺小剧场", "报社笑料合订本"],
	"Shopping": ["促销季暗箱", "百货断货潮", "抢购失控", "新品试卖记录"],
}

const BRIEFINGS := [
	"纸价又涨了一轮；但读者对超自然栏目的来信也明显变多。",
	"本周城里出现两起“官方否认但群众坚信”的目击报告。",
	"势力联系人放来消息：如果这周发刊足够稳，下一张区域通行许可就会松动。",
	"广告主变得谨慎了，意味着组版时不能只顾刺激，还得照顾整体可信度和版面平衡。",
]

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
@onready var story_list: VBoxContainer = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LibraryPanel/LibraryVBox/StoryScroll/StoryList
@onready var slot_list: VBoxContainer = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LayoutPanel/LayoutVBox/SlotList
@onready var clear_layout_btn: Button = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LayoutPanel/LayoutVBox/LayoutActions/ClearLayoutBtn
@onready var settle_btn: Button = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/LayoutPanel/LayoutVBox/LayoutActions/SettleBtn
@onready var live_stats: RichTextLabel = $RootMargin/RootVBox/EditorialPhase/EditorialColumns/StatsPanel/StatsVBox/LiveStats
@onready var summary_phase: PanelContainer = $RootMargin/RootVBox/SummaryPhase
@onready var summary_text: RichTextLabel = $RootMargin/RootVBox/SummaryPhase/SummaryVBox/SummaryText
@onready var next_week_btn: Button = $RootMargin/RootVBox/SummaryPhase/SummaryVBox/NextWeekBtn

var macro_stats := {}
var week := 1
var day := 7
var subscribers := 1200
var editorial_profile := 0.0
var week_briefing := ""
var log_entries: Array[String] = []
var filter_state := {"sci": true, "occult": true, "pop": true}
var selected_region_id := "us"
var selected_node_id := ""
var selected_story_id := -1
var selected_staff_ids: Array[String] = []
var weekly_clues: Array[Dictionary] = []
var story_pool: Array[Dictionary] = []
var slot_assignment := {}
var next_story_id := 1
var flags := {}
var resolved_nodes := {}
var current_phase := "explore"
var last_roll: Dictionary = {}
var last_summary: Dictionary = {}
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
		button.text = TAG_LABELS[tag]
		button.custom_minimum_size = Vector2(0, 30)
		button.pressed.connect(_on_filter_pressed.bind(tag))
		filter_row.add_child(button)
		filter_buttons[tag] = button
	_style_filter_buttons()

func _connect_buttons() -> void:
	back_btn.pressed.connect(_on_back_pressed)
	end_week_btn.pressed.connect(_enter_editorial_phase)
	execute_btn.pressed.connect(_on_execute_pressed)
	clear_layout_btn.pressed.connect(_clear_layout)
	settle_btn.pressed.connect(_settle_issue)
	next_week_btn.pressed.connect(_next_week)

func _on_back_pressed() -> void:
	get_tree().change_scene_to_file(str(Globals.scene_paths.get("main_menu", "res://scenes/MainMenu.tscn")))

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

func _on_story_selected(story_id: int) -> void:
	selected_story_id = story_id
	_refresh_story_pool()
	_refresh_slots()

func _start_new_run() -> void:
	week = 1
	day = 7
	subscribers = 1200
	editorial_profile = 0.0
	macro_stats = {"credibility": 42, "weirdness": 38, "reputation": 45, "order": 48, "mania": 22}
	selected_region_id = "us"
	selected_node_id = ""
	selected_story_id = -1
	selected_staff_ids.clear()
	weekly_clues.clear()
	story_pool.clear()
	slot_assignment.clear()
	flags.clear()
	resolved_nodes.clear()
	last_roll.clear()
	last_summary.clear()
	current_phase = "explore"
	week_briefing = BRIEFINGS[randi() % BRIEFINGS.size()]
	log_entries = ["[color=#f0d8a0]第 1 周开始[/color]：目标是在 Godot 里完整跑通一条周循环。"]
	_refresh_all()

func _refresh_all() -> void:
	explore_phase.visible = current_phase == "explore"
	editorial_phase.visible = current_phase == "editorial"
	summary_phase.visible = current_phase == "summary"
	week_label.text = "第 %d 周 · 周刊营运" % week
	day_label.text = "剩余 %d / 7 天 · 订阅 %d · editorialProfile %.2f" % [day, subscribers, editorial_profile]
	_refresh_macro_bar()
	_refresh_week_briefing()
	_refresh_region_and_nodes()
	_refresh_staff_grid()
	_refresh_clues()
	_refresh_mission_panel()
	_refresh_log()
	if current_phase == "editorial":
		_refresh_story_pool()
		_refresh_slots()
		_refresh_live_stats()
	if current_phase == "summary":
		_refresh_summary()

func _refresh_macro_bar() -> void:
	_clear_container(macro_bar)
	for item in MACRO_LABELS:
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
		value.text = str(macro_stats[item.key])
		value.add_theme_font_size_override("font_size", 21)
		box.add_child(value)

func _refresh_week_briefing() -> void:
	var unlocked := []
	for region in REGION_DATA:
		if _is_region_unlocked(region):
			unlocked.append(str(region.name))
	week_start_text.text = "[b]本周简报[/b]\n%s\n\n[color=#d8c8a2]当前开放区域：%s[/color]" % [week_briefing, _join_strings(unlocked, ", ")]

func _refresh_region_and_nodes() -> void:
	_clear_container(region_list)
	for region in REGION_DATA:
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 72)
		button.text = "%s\n%s" % [str(region.name), str(region.hint)]
		button.disabled = not _is_region_unlocked(region)
		button.pressed.connect(_on_region_pressed.bind(str(region.id)))
		_style_button(button, selected_region_id == str(region.id))
		region_list.add_child(button)
	_clear_container(node_list)
	var region := _get_selected_region()
	region_hint_label.text = "请选择区域" if region.is_empty() else "%s · %s" % [str(region.name), str(region.hint)]
	if region.is_empty():
		return
	for node in region.nodes:
		if not _is_node_visible(node):
			continue
		if not bool(filter_state.get(str(node.type), true)):
			continue
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 88)
		var availability := _get_node_availability(node)
		button.text = "%s · %s\n耗时 %d 天 · %s · 对抗 %d\n%s" % [str(node.name), str(node.kind), int(node.days), str(node.difficulty), int(node.enemy), str(availability.reason)]
		button.disabled = not availability.enabled
		button.pressed.connect(_on_node_pressed.bind(str(node.id)))
		_style_button(button, selected_node_id == str(node.id))
		node_list.add_child(button)

func _refresh_staff_grid() -> void:
	_clear_container(staff_grid)
	selected_staff_label.text = "已选择：%d / 3" % selected_staff_ids.size()
	for staff in STAFF_POOL:
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
		button.pressed.connect(_toggle_staff.bind(str(staff.id)))
		_style_button(button, selected_staff_ids.has(str(staff.id)))
		staff_grid.add_child(button)

func _refresh_clues() -> void:
	_clear_container(clue_list)
	if weekly_clues.is_empty():
		var empty := Label.new()
		empty.text = "还没有线索。先从低风险节点起手。"
		empty.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		empty.add_theme_color_override("font_color", Color(0.64, 0.70, 0.78, 1.0))
		clue_list.add_child(empty)
		return
	for clue in weekly_clues:
		var panel := PanelContainer.new()
		_style_panel(panel, Color(0.06, 0.09, 0.13, 1.0), Color(0.21, 0.27, 0.33, 1.0), 10)
		clue_list.add_child(panel)
		var text := RichTextLabel.new()
		text.bbcode_enabled = true
		text.fit_content = true
		text.scroll_active = false
		text.text = "[b]%s[/b]\n%s · tier %d · %s" % [str(clue.title), TAG_LABELS.get(str(clue.type), str(clue.type)), int(clue.tier), str(clue.source_region)]
		panel.add_child(text)

func _refresh_mission_panel() -> void:
	_clear_container(dice_rows)
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
		var current := int(totals.get(str(key), 0))
		var required := int(node.need[key])
		var color := "#7ad1a3" if current >= required else "#f59a8b"
		needs.append("[color=%s]%s %d / %d[/color]" % [color, ATTR_LABELS.get(str(key), str(key)), current, required])
	var prob := _calculate_node_probabilities(node)
	mission_summary.text = "[b]%s[/b]\n%s\n\n[color=#d8c8a2]需求：%s[/color]\n[color=#9fb3c7]当前派遣合计：探索 %d / 洞察 %d / 诡思 %d / 生存 %d / 理性 %d / 社交 %d[/color]\n[color=#8fa4bc]%s[/color]" % [
		str(node.name),
		str(node.description),
		" · ".join(PackedStringArray(needs)),
		int(totals.explore),
		int(totals.insight),
		int(totals.occult),
		int(totals.survival),
		int(totals.reason),
		int(totals.social),
		str(node.risk_text),
	]
	probability_label.text = "理论结果：大成功 %.1f%% · 小成功 %.1f%% · 失败 %.1f%%" % [prob.major * 100.0, prob.minor * 100.0, prob.fail * 100.0]
	if last_roll.get("node_id", "") == str(node.id):
		_render_roll(last_roll)
	else:
		result_label.text = "等待执行"
		result_label.add_theme_color_override("font_color", Color(0.88, 0.76, 0.36, 1.0))
	execute_btn.disabled = not bool(_get_node_availability(node).enabled)

func _refresh_log() -> void:
	log_text.clear()
	for entry in log_entries:
		log_text.append_text("%s\n" % entry)

func _toggle_staff(staff_id: String) -> void:
	if selected_staff_ids.has(staff_id):
		selected_staff_ids.erase(staff_id)
	elif selected_staff_ids.size() < 3:
		selected_staff_ids.append(staff_id)
	else:
		_add_log("[color=#f59a8b]派遣上限是 3 人。[/color]")
	_refresh_staff_grid()
	_refresh_mission_panel()

func _on_execute_pressed() -> void:
	var node := _get_selected_node()
	if node.is_empty():
		return
	var availability := _get_node_availability(node)
	if not bool(availability.enabled):
		_add_log("[color=#f59a8b]%s[/color]" % str(availability.reason))
		return
	var roll := _perform_split_check(node, _get_selected_staff_totals())
	last_roll = roll
	_render_roll(roll)
	_apply_node_resolution(node, roll)
	_refresh_all()
	if day <= 0:
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
		die.text = "—" if is_negated else ("✓" if dice[index] else "✗")
		die.custom_minimum_size = Vector2(28, 28)
		die.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		die.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		die.add_theme_font_size_override("font_size", 16)
		var die_color := Color(0.58, 0.62, 0.67, 1.0)
		if not is_negated:
			die_color = Color(0.46, 0.87, 0.60, 1.0) if dice[index] else Color(0.94, 0.52, 0.46, 1.0)
		die.add_theme_color_override("font_color", die_color)
		row.add_child(die)

func _apply_node_resolution(node: Dictionary, roll: Dictionary) -> void:
	day = max(0, day - int(node.days))
	resolved_nodes[str(node.id)] = true
	var clue := _generate_clue(node, roll)
	if not clue.is_empty():
		weekly_clues.append(clue)
	match str(roll.tier):
		"major":
			macro_stats.reputation += 3
			macro_stats.credibility += 2 if node.type == "sci" else 1
			macro_stats.weirdness += 2 if node.type == "occult" else 0
			macro_stats.order += 1
			week_briefing = "这次外采拿到了能直接进入编辑部的高质量线索。"
		"minor":
			macro_stats.reputation += 1
			macro_stats.credibility += 1 if node.type == "sci" else 0
			macro_stats.weirdness += 1 if node.type == "occult" else 0
			week_briefing = "这条线索可用，但还缺少最后一击。"
		_:
			macro_stats.order -= 2
			macro_stats.mania += 2
			week_briefing = "外采失手，只带回一条残缺线索。"
	if str(node.id) == "skin" and roll.tier != "fail":
		flags["roswell_dossier"] = true
	selected_node_id = ""
	last_roll.clear()
	_add_log("[color=#f0d8a0]%s[/color]：%s" % [str(node.name), week_briefing])
	if not clue.is_empty():
		_add_log("线索入库：[color=#9fd4ff]%s[/color]" % str(clue.title))

func _generate_clue(node: Dictionary, roll: Dictionary) -> Dictionary:
	var tier := 1
	if roll.tier == "major":
		tier = 3
	elif roll.tier == "minor":
		tier = 2
	var suffixes := {
		"sci": ["军方备忘录", "照片底片", "雷达转录", "船运清单"],
		"occult": ["低语片段", "异象素描", "供述抄本", "祭仪录音"],
		"pop": ["目击者热帖", "城市速报", "流言剪报", "街头口供"],
	}
	var suffix_list: Array = suffixes.get(str(node.type), ["现场摘要"])
	return {
		"id": "%s_%d" % [str(node.id), week],
		"title": "%s · %s" % [str(node.name), str(suffix_list[randi() % suffix_list.size()])],
		"type": str(node.type),
		"tier": tier,
		"source_region": str(_get_selected_region().name),
		"source_node": str(node.name),
		"risk_flags": ["fragmented"] if roll.tier == "fail" else [],
	}

func _enter_editorial_phase() -> void:
	if current_phase != "explore":
		return
	current_phase = "editorial"
	selected_story_id = -1
	_generate_story_pool()
	_add_log("探索阶段结束，编辑部开始根据线索生成故事库。")
	_refresh_all()

func _generate_story_pool() -> void:
	story_pool.clear()
	next_story_id = 1
	for clue in weekly_clues:
		story_pool.append(_story_from_clue(clue))
	while story_pool.size() < 10:
		story_pool.append(_generate_filler_story())

func _story_from_clue(clue: Dictionary) -> Dictionary:
	var tag_pool: Array = STORY_TAG_MAP.get(str(clue.type), ["Shopping"])
	var primary := str(tag_pool[randi() % tag_pool.size()])
	var secondary := str(tag_pool[(randi() + 1) % tag_pool.size()])
	var quality_data: Dictionary = QUALITY_MAP.get(int(clue.tier), QUALITY_MAP[1])
	var story := {"id": next_story_id, "title": str(clue.title), "tags": [primary] if primary == secondary else [primary, secondary], "quality": str(quality_data.quality), "base_value": int(quality_data.base_value), "negatives": clue.risk_flags.duplicate(), "source": "exploration"}
	next_story_id += 1
	return story

func _generate_filler_story() -> Dictionary:
	var all_tags := FILLER_SUBJECTS.keys()
	var primary := str(all_tags[randi() % all_tags.size()])
	var subject_list: Array = FILLER_SUBJECTS[primary]
	var quality_roll: int = [1, 1, 2, 2, 3][randi() % 5]
	var quality_data: Dictionary = QUALITY_MAP[quality_roll]
	var story := {"id": next_story_id, "title": str(subject_list[randi() % subject_list.size()]), "tags": [primary], "quality": str(quality_data.quality), "base_value": int(quality_data.base_value * 0.85), "negatives": ["thin_source"] if quality_roll == 1 and randf() < 0.45 else [], "source": "filler"}
	next_story_id += 1
	return story

func _refresh_story_pool() -> void:
	_clear_container(story_list)
	editorial_subtitle.text = "本周共 %d 条线索，故事库已补足到 %d 篇。先点击稿件，再点击右侧版位放置。" % [weekly_clues.size(), story_pool.size()]
	for story in story_pool:
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 88)
		button.text = "%s\n%s · %s · base %d" % [str(story.title), _join_strings(story.tags, " / "), str(story.quality), int(story.base_value)]
		button.disabled = _is_story_placed(int(story.id))
		button.pressed.connect(_on_story_selected.bind(int(story.id)))
		_style_button(button, selected_story_id == int(story.id))
		if button.disabled:
			button.text += "\n已上版"
		story_list.add_child(button)

func _refresh_slots() -> void:
	_clear_container(slot_list)
	for slot in SLOT_DATA:
		var story := _get_story_by_id(int(slot_assignment.get(str(slot.id), -1)))
		var button := Button.new()
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.custom_minimum_size = Vector2(0, 84)
		if story.is_empty():
			button.text = "%s · x%.2f\n%s\n点击这里放置当前选中的稿件" % [str(slot.name), float(slot.weight), str(slot.desc)]
		else:
			button.text = "%s · x%.2f\n%s\n%s · %s" % [str(slot.name), float(slot.weight), str(story.title), str(story.quality), _join_strings(story.tags, " / ")]
		button.pressed.connect(_place_story_in_slot.bind(str(slot.id)))
		_style_button(button, selected_story_id != -1)
		slot_list.add_child(button)

func _place_story_in_slot(slot_id: String) -> void:
	if selected_story_id == -1:
		return
	for key in slot_assignment.keys():
		if int(slot_assignment[key]) == selected_story_id:
			slot_assignment[key] = -1
	slot_assignment[slot_id] = selected_story_id
	selected_story_id = -1
	_refresh_story_pool()
	_refresh_slots()
	_refresh_live_stats()

func _clear_layout() -> void:
	for slot in SLOT_DATA:
		slot_assignment[str(slot.id)] = -1
	selected_story_id = -1
	_refresh_story_pool()
	_refresh_slots()
	_refresh_live_stats()

func _refresh_live_stats() -> void:
	var stats := _calculate_editorial_stats()
	live_stats.text = "[b]已填版位[/b] %d / 6\n[b]空版位[/b] %d\n[b]totalBaseValue[/b] %d\n[b]uniqueTags[/b] %d\n[b]comboRaw[/b] %d\n[b]linkedTags[/b] %d\n[b]negPenalty[/b] %d\n\n[b]三轴占比[/b]\n公共事务 P %d · 大众关注 M %d · 轻内容 L %d\n\n[b]核心乘数[/b]\nmQuality %.2f · mCombo %.2f · mDiversity %.2f\nmLayout %.2f · mEmpty %.2f · mPenalty %.2f\nmLink %.2f · mBalance %.2f · mBias %.2f\n\n[b]实时预估[/b]\n需求 %d\n销量 %d / 印量 %d\n卖报收入 %.0f\n订阅收入 %.0f\n广告收入 %.0f\n总收入 %.0f\n总成本 %.0f\n净利润 %.0f\n下周订阅预估 %d" % [
		int(stats.filled_slots), int(stats.empty_slots), int(stats.total_base_value), int(stats.unique_tags), int(stats.combo_raw), int(stats.linked_tags), int(stats.neg_penalty),
		int(stats.axis_p), int(stats.axis_m), int(stats.axis_l),
		float(stats.m_quality), float(stats.m_combo), float(stats.m_diversity), float(stats.m_layout), float(stats.m_empty), float(stats.m_penalty), float(stats.m_link), float(stats.m_balance), float(stats.m_bias),
		int(stats.demand), int(stats.sold), int(stats.print_capacity), float(stats.news_revenue), float(stats.sub_revenue), float(stats.ad_revenue), float(stats.total_revenue), float(stats.total_cost), float(stats.profit), int(stats.next_subscribers),
	]

func _calculate_editorial_stats() -> Dictionary:
	var placed := []
	for slot in SLOT_DATA:
		var story := _get_story_by_id(int(slot_assignment.get(str(slot.id), -1)))
		if not story.is_empty():
			placed.append({"slot": slot, "story": story})
	var filled_slots := placed.size()
	var empty_slots := SLOT_DATA.size() - filled_slots
	var total_base_value := 0.0
	var tag_counts := {}
	var neg_penalty := 0
	var axis_p := 0
	var axis_m := 0
	var axis_l := 0
	for item in placed:
		var slot: Dictionary = item.slot
		var story: Dictionary = item.story
		total_base_value += float(story.base_value) * float(slot.weight)
		neg_penalty += story.negatives.size()
		for tag in story.tags:
			tag_counts[str(tag)] = int(tag_counts.get(str(tag), 0)) + 1
			if tag in ["Politics", "Military", "Economy"]:
				axis_p += 1
			elif tag in ["Sport", "Shopping"]:
				axis_m += 1
			else:
				axis_l += 1
	var unique_tags := tag_counts.size()
	var combo_raw := 0
	var linked_tags := 0
	for count in tag_counts.values():
		if int(count) > 1:
			combo_raw += int(count) - 1
			linked_tags += 1
	var total_axes: int = maxi(1, axis_p + axis_m + axis_l)
	var avg_axis := float(total_axes) / 3.0
	var deviation := absf(axis_p - avg_axis) + absf(axis_m - avg_axis) + absf(axis_l - avg_axis)
	var m_quality := clampf(0.88 + total_base_value / 2100.0, 0.88, 1.55)
	var m_combo := clampf(1.00 + combo_raw * 0.04, 1.00, 1.32)
	var m_diversity := clampf(0.92 + unique_tags * 0.035, 0.92, 1.24)
	var m_layout := 0.88 + filled_slots * 0.07
	var m_empty := clampf(1.00 - empty_slots * 0.12, 0.35, 1.00)
	var m_penalty := clampf(1.00 - neg_penalty * 0.05, 0.70, 1.00)
	var m_link := clampf(1.00 + linked_tags * 0.03, 1.00, 1.18)
	var m_balance := clampf(1.14 - deviation * 0.06, 0.82, 1.14)
	var m_bias := clampf(1.00 + _dominant_axis_shift(axis_p, axis_m, axis_l) * editorial_profile * 0.06, 0.92, 1.08)
	var demand := int(round((3200.0 + subscribers * 0.45 + total_base_value * 1.45) * m_quality * m_combo * m_diversity * m_layout * m_empty * m_penalty * m_link * m_balance * m_bias))
	var print_capacity := 4200
	var sold := clampi(demand, 0, print_capacity)
	var news_revenue := sold * 0.30
	var sub_revenue := subscribers * 0.18
	var ad_revenue := 2.0 * 180.0 * clampf(0.70 + linked_tags * 0.05 + (m_bias - 1.0), 0.45, 1.20)
	var total_revenue := news_revenue + sub_revenue + ad_revenue
	var total_cost := 210.0 + 980.0 + 260.0 + filled_slots * 28.0
	var profit := total_revenue - total_cost
	return {
		"filled_slots": filled_slots, "empty_slots": empty_slots, "total_base_value": int(round(total_base_value)), "unique_tags": unique_tags, "combo_raw": combo_raw, "linked_tags": linked_tags, "neg_penalty": neg_penalty,
		"axis_p": axis_p, "axis_m": axis_m, "axis_l": axis_l,
		"m_quality": m_quality, "m_combo": m_combo, "m_diversity": m_diversity, "m_layout": m_layout, "m_empty": m_empty, "m_penalty": m_penalty, "m_link": m_link, "m_balance": m_balance, "m_bias": m_bias,
		"demand": demand, "sold": sold, "print_capacity": print_capacity, "news_revenue": news_revenue, "sub_revenue": sub_revenue, "ad_revenue": ad_revenue, "total_revenue": total_revenue, "total_cost": total_cost, "profit": profit,
		"next_subscribers": max(600, int(round(subscribers + profit / 130.0 + (m_balance - 1.0) * 180.0 + (m_quality - 1.0) * 220.0 - empty_slots * 45.0))),
		"next_editorial_profile": clampf(editorial_profile + _dominant_axis_shift(axis_p, axis_m, axis_l) * 0.12, -1.0, 1.0),
	}

func _settle_issue() -> void:
	var stats := _calculate_editorial_stats()
	last_summary = stats.duplicate(true)
	last_summary.week = week
	last_summary.editorial_profile_before = editorial_profile
	subscribers = int(stats.next_subscribers)
	editorial_profile = float(stats.next_editorial_profile)
	last_summary.editorial_profile_after = editorial_profile
	macro_stats.reputation += int(clamp(roundi(stats.profit / 700.0), -2, 3))
	macro_stats.credibility += 1 if stats.axis_p >= stats.axis_m and stats.axis_p >= stats.axis_l else 0
	macro_stats.weirdness += 1 if _count_occult_clues() >= 2 else 0
	macro_stats.order += 1 if stats.empty_slots == 0 else -1
	macro_stats.mania = max(0, macro_stats.mania - 1 if stats.m_balance >= 1.0 else macro_stats.mania + 1)
	last_summary.commentary = _settlement_commentary(stats)
	current_phase = "summary"
	_add_log("本期发刊完成：利润 %.0f，销量 %d。" % [float(stats.profit), int(stats.sold)])
	_refresh_all()

func _refresh_summary() -> void:
	if last_summary.is_empty():
		summary_text.text = "尚未结算。"
		return
	summary_text.text = "[b]第 %d 周发行完成[/b]\n净利润 %.0f · 销量 %d / %d · 下一周订阅 %d\n\n[color=#d8c8a2]编辑定位[/color] %.2f → %.2f\n[color=#9fb3c7]公信 %d  诡名 %d  声望 %d  守序 %d  狂性 %d[/color]\n\n%s" % [
		int(last_summary.week), float(last_summary.profit), int(last_summary.sold), int(last_summary.demand), int(last_summary.next_subscribers),
		float(last_summary.editorial_profile_before), float(last_summary.editorial_profile_after),
		int(macro_stats.credibility), int(macro_stats.weirdness), int(macro_stats.reputation), int(macro_stats.order), int(macro_stats.mania),
		str(last_summary.commentary),
	]

func _next_week() -> void:
	week += 1
	day = 7
	selected_node_id = ""
	selected_story_id = -1
	selected_staff_ids.clear()
	weekly_clues.clear()
	story_pool.clear()
	slot_assignment.clear()
	resolved_nodes.clear()
	last_roll.clear()
	current_phase = "explore"
	week_briefing = BRIEFINGS[randi() % BRIEFINGS.size()]
	_add_log("[color=#f0d8a0]进入第 %d 周[/color]：新的简报与外采节点已经刷新。" % week)
	_refresh_all()

func _perform_split_check(node: Dictionary, totals: Dictionary) -> Dictionary:
	var p := float(DIFFICULTY_P.get(str(node.difficulty), 0.50))
	var attr_a := int(totals.explore) + int(totals.insight) + int(totals.occult)
	var attr_b := int(totals.survival) + int(totals.reason)
	var total_pool: int = maxi(1, attr_a + attr_b)
	var enemy_a := floori(float(int(node.enemy)) * attr_a / total_pool)
	var enemy_b := int(node.enemy) - enemy_a
	var k_a := clampi(int(node.k_a), 0, max(0, attr_a - enemy_a))
	var k_b := clampi(int(node.k_b), 0, max(0, attr_b - enemy_b))
	var dice_a := _roll_dice(attr_a, p)
	var dice_b := _roll_dice(attr_b, p)
	var negated_a := _random_negate_indices(attr_a, mini(enemy_a, attr_a))
	var negated_b := _random_negate_indices(attr_b, mini(enemy_b, attr_b))
	var hit_a := 0
	for index in range(attr_a):
		if not negated_a.has(index) and dice_a[index]:
			hit_a += 1
	var hit_b := 0
	for index in range(attr_b):
		if not negated_b.has(index) and dice_b[index]:
			hit_b += 1
	var tier := "fail"
	if hit_a >= k_a and hit_b >= k_b:
		tier = "major"
	elif hit_a >= k_a or hit_b >= k_b:
		tier = "minor"
	return {"node_id": str(node.id), "dice_a": dice_a, "dice_b": dice_b, "negated_a": negated_a, "negated_b": negated_b, "hit_a": hit_a, "hit_b": hit_b, "k_a": k_a, "k_b": k_b, "tier": tier}

func _calculate_node_probabilities(node: Dictionary) -> Dictionary:
	var totals := _get_selected_staff_totals()
	var attr_a := int(totals.explore) + int(totals.insight) + int(totals.occult)
	var attr_b := int(totals.survival) + int(totals.reason)
	var total_pool: int = maxi(1, attr_a + attr_b)
	var enemy_a := floori(float(int(node.enemy)) * attr_a / total_pool)
	var enemy_b := int(node.enemy) - enemy_a
	var n_a_eff: int = maxi(0, attr_a - enemy_a)
	var n_b_eff: int = maxi(0, attr_b - enemy_b)
	var k_a := clampi(int(node.k_a), 0, n_a_eff)
	var k_b := clampi(int(node.k_b), 0, n_b_eff)
	var p := float(DIFFICULTY_P.get(str(node.difficulty), 0.50))
	var p_a := _binomial_cdf_ge(n_a_eff, k_a, p) if n_a_eff > 0 else 0.0
	var p_b := _binomial_cdf_ge(n_b_eff, k_b, p) if n_b_eff > 0 else 0.0
	return {"major": p_a * p_b, "minor": p_a * (1.0 - p_b) + (1.0 - p_a) * p_b, "fail": (1.0 - p_a) * (1.0 - p_b)}

func _get_selected_region() -> Dictionary:
	for region in REGION_DATA:
		if str(region.id) == selected_region_id:
			return region
	return {}

func _get_selected_node() -> Dictionary:
	var region := _get_selected_region()
	for node in region.get("nodes", []):
		if str(node.id) == selected_node_id:
			return node
	return {}

func _get_selected_staff_totals() -> Dictionary:
	var totals := {"explore": 0, "insight": 0, "occult": 0, "survival": 0, "reason": 0, "social": 0}
	for staff in STAFF_POOL:
		if selected_staff_ids.has(str(staff.id)):
			for key in totals.keys():
				totals[key] += int(staff.attrs[key])
	return totals

func _get_node_availability(node: Dictionary) -> Dictionary:
	if day < int(node.days):
		return {"enabled": false, "reason": "剩余天数不足"}
	if selected_staff_ids.is_empty():
		return {"enabled": false, "reason": "先选择 1-3 名职员"}
	if str(node.kind) == "temp" and bool(resolved_nodes.get(str(node.id), false)):
		return {"enabled": false, "reason": "这个临时节点本周已处理"}
	if node.has("deadline_day") and day < int(node.deadline_day):
		return {"enabled": false, "reason": "这个突发节点已经过期"}
	var totals := _get_selected_staff_totals()
	for key in node.need.keys():
		if int(totals.get(str(key), 0)) < int(node.need[key]):
			return {"enabled": false, "reason": "派遣属性未满足需求"}
	return {"enabled": true, "reason": "可执行"}

func _is_region_unlocked(region: Dictionary) -> bool:
	match str(region.unlock_rule):
		"always":
			return true
		"east_asia":
			return macro_stats.reputation >= 55 or bool(flags.get("roswell_dossier", false))
		_:
			return false

func _is_node_visible(node: Dictionary) -> bool:
	if str(node.kind) != "hidden":
		return true
	return _hidden_node_unlocked(node)

func _hidden_node_unlocked(node: Dictionary) -> bool:
	match str(node.get("unlock_rule", "")):
		"hidden_monolith":
			return macro_stats.mania >= 35 and macro_stats.weirdness >= 40
		_:
			return true

func _get_story_by_id(story_id: int) -> Dictionary:
	for story in story_pool:
		if int(story.id) == story_id:
			return story
	return {}

func _is_story_placed(story_id: int) -> bool:
	for value in slot_assignment.values():
		if int(value) == story_id:
			return true
	return false

func _dominant_axis_shift(axis_p: int, axis_m: int, axis_l: int) -> float:
	if axis_p >= axis_m and axis_p >= axis_l:
		return -1.0
	if axis_m >= axis_l:
		return 1.0
	return 0.6

func _count_occult_clues() -> int:
	var count := 0
	for clue in weekly_clues:
		if str(clue.type) == "occult":
			count += 1
	return count

func _settlement_commentary(stats: Dictionary) -> String:
	if float(stats.profit) >= 700.0:
		return "这一期既卖得动，也让编辑部的定位更清晰，探索与组版的接口已经打通。"
	if float(stats.profit) >= 0.0:
		return "这一期勉强盈利，版面结构已经可用，但仍要继续压空版和偏科。"
	return "这一期亏损，主要问题通常是空版过多、题材失衡或高价值稿件不足。"

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
		child.free()

func _add_log(text: String) -> void:
	log_entries.append(text)
	if log_entries.size() > 12:
		log_entries = log_entries.slice(log_entries.size() - 12, log_entries.size())

func _join_strings(values: Array, separator: String) -> String:
	var out := []
	for value in values:
		out.append(str(value))
	return separator.join(out)

func _roll_dice(n: int, p: float) -> Array:
	var results := []
	for _i in range(max(0, n)):
		results.append(randf() < p)
	return results

func _random_negate_indices(total: int, count: int) -> Array:
	var indices := []
	for index in range(total):
		indices.append(index)
	indices.shuffle()
	return indices.slice(0, mini(count, total))

func _binomial_coeff(n: int, k: int) -> int:
	if k < 0 or k > n:
		return 0
	if k == 0 or k == n:
		return 1
	var result := 1
	var limit := mini(k, n - k)
	for i in range(limit):
		result = result * (n - i) / (i + 1)
	return result

func _binomial_pmf(n: int, k: int, p: float) -> float:
	return _binomial_coeff(n, k) * pow(p, k) * pow(1.0 - p, n - k)

func _binomial_cdf_ge(n: int, k: int, p: float) -> float:
	var total := 0.0
	for value in range(k, n + 1):
		total += _binomial_pmf(n, value, p)
	return clampf(total, 0.0, 1.0)
