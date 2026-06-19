extends MarginContainer
class_name WeeklyRunExplorePhase

signal filter_toggled(tag)
signal region_selected(region_id)
signal enter_region_requested
signal back_to_world_requested
signal back_to_region_requested
signal node_selected(node_id)
signal open_dispatch_requested
signal staff_toggled(staff_id)
signal selected_staff_slot_removed(staff_id)
signal execute_requested

const ActionItemScene = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunActionItem.tscn")
const UiStyle = preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

var _use_world_imagegen_v5 := false
var _world_imagegen_bg_texture: Texture2D = null
var _use_region_task_artboard_v3 := false
var _use_region_task_assetized := false
var _use_region_task_art := false
var _region_task_bg_texture: Texture2D = null
var _region_task_map_texture: Texture2D = null
var _region_task_route_texture: Texture2D = null
var _current_view_mode := "world"

@onready var stage_panel: PanelContainer = $RootVBox/StagePanel
@onready var stage_kicker: Label = $RootVBox/StagePanel/StageHBox/StageTitleBox/StageKicker
@onready var stage_title: Label = $RootVBox/StagePanel/StageHBox/StageTitleBox/StageTitle
@onready var stage_note: Label = $RootVBox/StagePanel/StageHBox/StageTitleBox/StageNote
@onready var stage_status: Label = $RootVBox/StagePanel/StageHBox/StageStatus

@onready var world_view: HBoxContainer = $RootVBox/WorldView
@onready var world_index_panel: PanelContainer = $RootVBox/WorldView/WorldIndexPanel
@onready var world_index_title: Label = $RootVBox/WorldView/WorldIndexPanel/WorldIndexVBox/WorldIndexTitle
@onready var world_index_subtitle: Label = $RootVBox/WorldView/WorldIndexPanel/WorldIndexVBox/WorldIndexSubtitle
@onready var region_list: VBoxContainer = $RootVBox/WorldView/WorldIndexPanel/WorldIndexVBox/RegionScroll/RegionList
@onready var world_index_footer: RichTextLabel = $RootVBox/WorldView/WorldIndexPanel/WorldIndexVBox/WorldIndexFooter
@onready var world_map_panel: PanelContainer = $RootVBox/WorldView/WorldMapPanel
@onready var world_map_backdrop: TextureRect = $RootVBox/WorldView/WorldMapPanel/WorldMapStack/WorldMapBackdrop
@onready var world_map_canvas: Control = $RootVBox/WorldView/WorldMapPanel/WorldMapStack/WorldMapCanvas
@onready var world_pin_layer: Control = $RootVBox/WorldView/WorldMapPanel/WorldMapStack/WorldPinLayer
@onready var world_editor_sticker: TextureRect = $RootVBox/WorldView/WorldMapPanel/WorldMapStack/WorldEditorSticker
@onready var world_detail_panel: PanelContainer = $RootVBox/WorldView/WorldDetailPanel
@onready var world_detail_kicker: Label = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldDetailKicker
@onready var region_detail_title: Label = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/RegionDetailTitle
@onready var world_story_preview: TextureRect = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldStoryPreview
@onready var world_deadline_ticket: Label = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldTicketVBox/WorldDeadlineTicket
@onready var world_chain_ticket: Label = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldTicketVBox/WorldChainTicket
@onready var region_detail_text: RichTextLabel = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/RegionDetailText
@onready var world_cta_hint: RichTextLabel = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/WorldCtaHint
@onready var enter_region_btn: Button = $RootVBox/WorldView/WorldDetailPanel/WorldDetailVBox/EnterRegionBtn
@onready var world_proof_strip: PanelContainer = $RootVBox/WorldProofStrip
@onready var world_log_title: Label = $RootVBox/WorldProofStrip/WorldProofHBox/WorldLogTitle
@onready var world_log_chips: Array[Label] = [
	$RootVBox/WorldProofStrip/WorldProofHBox/WorldLogChip1,
	$RootVBox/WorldProofStrip/WorldProofHBox/WorldLogChip2,
	$RootVBox/WorldProofStrip/WorldProofHBox/WorldLogChip3,
]
@onready var world_proof_text: Label = $RootVBox/WorldProofStrip/WorldProofHBox/WorldProofText

@onready var region_view: MarginContainer = $RootVBox/RegionView
@onready var region_hbox: HBoxContainer = $RootVBox/RegionView/RegionHBox
@onready var node_index_panel: PanelContainer = $RootVBox/RegionView/RegionHBox/NodeIndexPanel
@onready var back_to_world_btn: Button = $RootVBox/RegionView/RegionHBox/NodeIndexPanel/NodeIndexVBox/BackToWorldBtn
@onready var node_index_title: Label = $RootVBox/RegionView/RegionHBox/NodeIndexPanel/NodeIndexVBox/NodeIndexTitle
@onready var filter_row: HBoxContainer = $RootVBox/RegionView/RegionHBox/NodeIndexPanel/NodeIndexVBox/FilterRow
@onready var btn_filter_sci: Button = $RootVBox/RegionView/RegionHBox/NodeIndexPanel/NodeIndexVBox/FilterRow/BtnFilterSci
@onready var btn_filter_occult: Button = $RootVBox/RegionView/RegionHBox/NodeIndexPanel/NodeIndexVBox/FilterRow/BtnFilterOccult
@onready var btn_filter_pop: Button = $RootVBox/RegionView/RegionHBox/NodeIndexPanel/NodeIndexVBox/FilterRow/BtnFilterPop
@onready var node_list: VBoxContainer = $RootVBox/RegionView/RegionHBox/NodeIndexPanel/NodeIndexVBox/NodeScroll/NodeList
@onready var region_map_panel: PanelContainer = $RootVBox/RegionView/RegionHBox/RegionMapPanel
@onready var region_map_backdrop: TextureRect = $RootVBox/RegionView/RegionHBox/RegionMapPanel/RegionMapStack/RegionMapBackdrop
@onready var region_route_layer: TextureRect = $RootVBox/RegionView/RegionHBox/RegionMapPanel/RegionMapStack/RegionRouteLayer
@onready var region_map_canvas: Control = $RootVBox/RegionView/RegionHBox/RegionMapPanel/RegionMapStack/RegionMapCanvas
@onready var node_pin_layer: Control = $RootVBox/RegionView/RegionHBox/RegionMapPanel/RegionMapStack/NodePinLayer
@onready var region_task_panel: PanelContainer = $RootVBox/RegionView/RegionHBox/RegionTaskPanel
@onready var region_task_title: Label = $RootVBox/RegionView/RegionHBox/RegionTaskPanel/RegionTaskVBox/RegionTaskTitle
@onready var region_task_text: RichTextLabel = $RootVBox/RegionView/RegionHBox/RegionTaskPanel/RegionTaskVBox/RegionTaskText
@onready var open_dispatch_btn: Button = $RootVBox/RegionView/RegionHBox/RegionTaskPanel/RegionTaskVBox/OpenDispatchBtn

@onready var dispatch_view: Control = $RootVBox/DispatchView
@onready var dispatch_mission_panel: PanelContainer = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchMissionPanel
@onready var dispatch_back_btn: Button = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchMissionPanel/DispatchMissionVBox/DispatchBackBtn
@onready var dispatch_node_title_label: Label = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchMissionPanel/DispatchMissionVBox/DispatchNodeTitleLabel
@onready var dispatch_node_fact_text: RichTextLabel = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchMissionPanel/DispatchMissionVBox/DispatchNodeFactText
@onready var dispatch_dice_pool_panel: PanelContainer = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchDicePoolPanel
@onready var selected_staff_label: Label = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchDicePoolPanel/DispatchDicePoolVBox/DicePoolHeader/SelectedStaffLabel
@onready var selected_slot_labels: Array[Button] = [
	$RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchDicePoolPanel/DispatchDicePoolVBox/SelectedSlotRow/SelectedSlot1,
	$RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchDicePoolPanel/DispatchDicePoolVBox/SelectedSlotRow/SelectedSlot2,
	$RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchDicePoolPanel/DispatchDicePoolVBox/SelectedSlotRow/SelectedSlot3,
]
@onready var staff_grid: GridContainer = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchDicePoolPanel/DispatchDicePoolVBox/StaffScroll/StaffGrid
@onready var dispatch_review_panel: PanelContainer = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel
@onready var review_title: Label = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel/DispatchReviewVBox/ReviewTitle
@onready var probability_label: Label = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel/DispatchReviewVBox/ProbabilityLabel
@onready var dice_text: RichTextLabel = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel/DispatchReviewVBox/DiceText
@onready var result_label: Label = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel/DispatchReviewVBox/ResultLabel
@onready var dispatch_stamp_texture: TextureRect = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel/DispatchReviewVBox/DispatchStampTexture
@onready var execute_btn: Button = $RootVBox/DispatchView/DispatchContent/DispatchShell/DispatchReviewPanel/DispatchReviewVBox/ExecuteBtn
@onready var dispatch_summary_panel: PanelContainer = $RootVBox/DispatchView/DispatchSummaryPanel
@onready var dispatch_summary_text: RichTextLabel = $RootVBox/DispatchView/DispatchSummaryPanel/DispatchSummaryText

func _ready() -> void:
	add_theme_constant_override("margin_left", 2)
	add_theme_constant_override("margin_top", 2)
	add_theme_constant_override("margin_right", 2)
	add_theme_constant_override("margin_bottom", 2)
	_use_world_imagegen_v5 = UiStyle.has_world_imagegen_v5_runtime_assets()
	_apply_world_runtime_art()
	_apply_region_task_runtime_art()

	var panels: Array[Control] = [
		stage_panel, world_index_panel, world_map_panel, world_detail_panel, world_proof_strip,
		node_index_panel, region_map_panel, region_task_panel,
		dispatch_mission_panel, dispatch_review_panel, dispatch_dice_pool_panel, dispatch_summary_panel,
	]
	for panel in panels:
		UiStyle.apply_panel_style(panel, Color(0.055, 0.075, 0.090, 0.94), Color(0.20, 0.30, 0.32, 1.0), 8)
	UiStyle.apply_channel_shell_style(stage_panel)
	UiStyle.apply_world_index_panel_style(world_index_panel)
	UiStyle.apply_wall_map_shell_style(world_map_panel)
	UiStyle.apply_world_detail_panel_style(world_detail_panel)
	UiStyle.apply_world_log_strip_style(world_proof_strip)
	UiStyle.apply_panel_style(dispatch_mission_panel, Color(0.052, 0.072, 0.082, 0.93), Color(0.22, 0.48, 0.50, 1.0), 8)
	UiStyle.apply_panel_style(dispatch_dice_pool_panel, Color(0.045, 0.062, 0.070, 0.91), Color(0.20, 0.32, 0.34, 1.0), 8)
	UiStyle.apply_panel_style(dispatch_review_panel, Color(0.070, 0.082, 0.082, 0.94), Color(0.62, 0.48, 0.18, 1.0), 8)
	UiStyle.apply_panel_style(dispatch_summary_panel, Color(0.050, 0.064, 0.064, 0.96), Color(0.38, 0.30, 0.18, 1.0), 8)
	dispatch_node_title_label.add_theme_color_override("font_color", Color(0.94, 0.94, 0.84, 1.0))
	dispatch_node_title_label.add_theme_constant_override("outline_size", 4)
	dispatch_node_title_label.add_theme_color_override("font_outline_color", Color(0.02, 0.04, 0.04, 0.95))
	dispatch_node_fact_text.add_theme_color_override("default_color", Color(0.90, 0.89, 0.76, 1.0))
	selected_staff_label.add_theme_color_override("font_color", Color(0.90, 0.89, 0.76, 1.0))
	review_title.add_theme_color_override("font_color", Color(0.96, 0.82, 0.48, 1.0))
	review_title.add_theme_constant_override("outline_size", 2)
	review_title.add_theme_color_override("font_outline_color", Color(0.02, 0.04, 0.04, 0.95))
	probability_label.add_theme_color_override("font_color", Color(0.94, 0.92, 0.78, 1.0))
	dice_text.add_theme_color_override("default_color", Color(0.88, 0.88, 0.76, 1.0))
	dispatch_summary_text.add_theme_color_override("default_color", Color(0.88, 0.86, 0.70, 1.0))
	dispatch_summary_text.add_theme_font_size_override("normal_font_size", 14)
	dispatch_summary_text.add_theme_font_size_override("bold_font_size", 14)
	_style_stage_header()
	_style_world_panel_headers()
	_style_world_proof_strip()
	if _use_world_imagegen_v5:
		_use_world_imagegen_v5 = _apply_world_imagegen_v5_candidate_style()
		if not _use_world_imagegen_v5:
			_apply_world_runtime_art()
	for slot_label in selected_slot_labels:
		_connect_selected_slot_button(slot_label)
		_style_dispatch_slot(slot_label, false)

	var buttons: Array[Button] = [
		enter_region_btn, back_to_world_btn, btn_filter_sci, btn_filter_occult,
		btn_filter_pop, open_dispatch_btn, dispatch_back_btn, execute_btn,
	]
	for button in buttons:
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		UiStyle.apply_button_style(button, false, true)
	UiStyle.apply_world_cta_button(enter_region_btn, true)
	UiStyle.apply_primary_channel_button(open_dispatch_btn, false)
	UiStyle.apply_primary_channel_button(execute_btn, false)
	_style_region_task_board()

	enter_region_btn.pressed.connect(func() -> void:
		enter_region_requested.emit()
	)
	back_to_world_btn.pressed.connect(func() -> void:
		back_to_world_requested.emit()
	)
	open_dispatch_btn.pressed.connect(func() -> void:
		open_dispatch_requested.emit()
	)
	dispatch_back_btn.pressed.connect(func() -> void:
		back_to_region_requested.emit()
	)
	execute_btn.pressed.connect(func() -> void:
		execute_requested.emit()
	)
	btn_filter_sci.pressed.connect(func() -> void:
		filter_toggled.emit("sci")
	)
	btn_filter_occult.pressed.connect(func() -> void:
		filter_toggled.emit("occult")
	)
	btn_filter_pop.pressed.connect(func() -> void:
		filter_toggled.emit("pop")
	)

func _connect_selected_slot_button(button: Button) -> void:
	button.pressed.connect(func() -> void:
		var staff_id := str(button.get_meta("staff_id", ""))
		if staff_id != "":
			selected_staff_slot_removed.emit(staff_id)
	)

func _draw() -> void:
	if _current_view_mode == "region" and _region_task_bg_texture != null:
		draw_texture_rect(_region_task_bg_texture, Rect2(Vector2.ZERO, size), false)
	elif _use_world_imagegen_v5 and _world_imagegen_bg_texture != null:
		draw_texture_rect(_world_imagegen_bg_texture, Rect2(Vector2.ZERO, size), false)

func _apply_world_imagegen_v5_candidate_style() -> bool:
	var ok := true
	world_detail_panel.custom_minimum_size = Vector2(450.0, 0.0)
	world_story_preview.custom_minimum_size = Vector2(0.0, 112.0)
	world_story_preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	world_deadline_ticket.custom_minimum_size = Vector2(0.0, 64.0)
	world_chain_ticket.custom_minimum_size = Vector2(0.0, 64.0)
	enter_region_btn.custom_minimum_size = Vector2(0.0, 58.0)
	world_index_footer.custom_minimum_size = Vector2(0.0, 168.0)
	world_index_footer.add_theme_color_override("default_color", Color(0.15, 0.29, 0.25, 1.0))
	world_index_footer.add_theme_font_size_override("normal_font_size", 13)
	world_index_footer.add_theme_font_size_override("bold_font_size", 13)
	world_detail_kicker.add_theme_font_size_override("font_size", 13)
	world_detail_kicker.z_index = 2
	region_detail_title.add_theme_font_size_override("font_size", 24)
	region_detail_title.custom_minimum_size = Vector2(0.0, 34.0)
	region_detail_title.clip_text = true
	region_detail_title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	region_detail_title.max_lines_visible = 1
	region_detail_title.z_index = 3
	region_detail_title.add_theme_color_override("font_color", Color(0.98, 0.91, 0.70, 1.0))
	region_detail_title.add_theme_constant_override("outline_size", 3)
	region_detail_title.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.92))
	world_story_preview.z_index = 0
	region_detail_text.add_theme_font_size_override("normal_font_size", 14)
	region_detail_text.add_theme_font_size_override("bold_font_size", 14)
	region_detail_text.add_theme_constant_override("line_separation", 3)
	enter_region_btn.add_theme_font_size_override("font_size", 18)
	ok = UiStyle.apply_world_imagegen_v5_index_panel_style(world_index_panel) and ok
	ok = UiStyle.apply_world_imagegen_v5_detail_panel_style(world_detail_panel) and ok
	ok = UiStyle.apply_world_imagegen_v5_log_strip_style(world_proof_strip) and ok
	ok = UiStyle.apply_world_imagegen_v5_cta_button(enter_region_btn, not enter_region_btn.disabled) and ok
	return ok

func _apply_world_runtime_art() -> void:
	if _use_world_imagegen_v5:
		world_editor_sticker.visible = false
		_world_imagegen_bg_texture = UiStyle.load_world_imagegen_texture("wm_bg_shell")
		var imagegen_map_texture := UiStyle.load_world_imagegen_texture("wm_world_board_base")
		if imagegen_map_texture != null:
			world_map_backdrop.texture = imagegen_map_texture
		var imagegen_story_texture := UiStyle.load_world_imagegen_texture("wm_story_preview_north_america")
		if imagegen_story_texture != null:
			world_story_preview.texture = imagegen_story_texture
		queue_redraw()
		return
	_world_imagegen_bg_texture = null
	world_editor_sticker.visible = true
	queue_redraw()
	var map_texture := UiStyle.load_world_map_texture("wm-world-board-v3-base.png")
	if map_texture != null:
		world_map_backdrop.texture = map_texture
	var story_texture := UiStyle.load_world_map_texture("wm-story-preview-v4.png")
	if story_texture != null:
		world_story_preview.texture = story_texture

func _apply_region_task_runtime_art() -> void:
	_use_region_task_artboard_v3 = UiStyle.has_region_task_artboard_v3_runtime_assets()
	if _use_region_task_artboard_v3:
		_region_task_bg_texture = UiStyle.load_region_task_asset_texture("rt_artboard_full")
		_use_region_task_assetized = _region_task_bg_texture != null
		_use_region_task_art = _region_task_bg_texture != null
		_region_task_map_texture = null
		_region_task_route_texture = null
		region_map_backdrop.visible = false
		region_route_layer.visible = false
		if _use_region_task_art:
			queue_redraw()
			return
	_use_region_task_artboard_v3 = false
	_use_region_task_assetized = UiStyle.has_region_task_assetized_runtime_assets()
	if _use_region_task_assetized:
		_region_task_bg_texture = UiStyle.load_region_task_asset_texture("rt_board_shell")
		_region_task_map_texture = UiStyle.load_region_task_asset_texture("rt_map_base_clean")
		_region_task_route_texture = UiStyle.load_region_task_asset_texture("rt_map_route_layer")
		_use_region_task_art = _region_task_bg_texture != null and _region_task_map_texture != null
		region_map_backdrop.texture = _region_task_map_texture
		region_route_layer.texture = _region_task_route_texture
		region_map_backdrop.visible = _use_region_task_art
		region_route_layer.visible = _use_region_task_art and _region_task_route_texture != null
		if _use_region_task_art:
			queue_redraw()
			return
	_use_region_task_assetized = false
	_region_task_map_texture = null
	_region_task_route_texture = null
	region_map_backdrop.visible = false
	region_route_layer.visible = false
	_region_task_bg_texture = null
	_use_region_task_art = false
	queue_redraw()

func render(payload: Dictionary) -> void:
	var view_mode := str(payload.get("view_mode", "world"))
	_current_view_mode = view_mode
	var selected_region := str(payload.get("selected_region_id", ""))
	var selected_node := str(payload.get("selected_node_id", ""))

	world_view.visible = view_mode == "world"
	world_proof_strip.visible = view_mode == "world"
	region_view.visible = view_mode == "region"
	dispatch_view.visible = view_mode == "dispatch"
	stage_panel.visible = view_mode == "dispatch"
	stage_status.text = "第 %d 周 · 剩余 %d 天 · 新素材 %d" % [
		int(payload.get("week", 1)),
		int(payload.get("remaining_days", 0)),
		int(payload.get("new_material_count", 0)),
	]
	queue_redraw()

	match view_mode:
		"world":
			stage_title.text = "全球频道 · 本周取材地图"
			stage_note.text = "监听城市异常与读者线索，先锁定取材区域；进入区域后才审任务，不消耗天数。"
			_render_world(payload, selected_region)
		"dispatch":
			stage_title.text = "编辑部派遣签批台"
			stage_note.text = "把任务从地图上拿到桌面，配置本次骰池，再签批外勤。"
			_render_dispatch(payload)
		_:
			stage_title.text = "%s · 区域任务台" % str(payload.get("region_title", "北美禁区带"))
			stage_note.text = "选择任务档案，送至签批台配置本次骰池。"
			_render_region(payload, selected_node)

func _render_world(payload: Dictionary, selected_region: String) -> void:
	world_index_panel.visible = true
	world_map_canvas.call("configure", "world", selected_region)
	_rebuild_action_items(region_list, payload.get("regions", []), "region")
	world_index_footer.text = _build_world_index_footer_text(payload)
	_rebuild_region_pins(payload.get("regions", []))
	region_detail_title.text = str(payload.get("region_detail_title", "取材区域"))
	_update_world_story_preview(payload)
	_render_world_story_tickets(payload)
	region_detail_text.text = _build_world_detail_text(payload)
	_render_world_proof_strip(payload)
	var can_enter := bool(payload.get("region_enter_enabled", false))
	_style_world_detail_body(can_enter)
	_render_world_cta_hint(payload, can_enter)
	enter_region_btn.text = str(payload.get("region_enter_text", "进入选定地区" if can_enter else "暂不可进入"))
	if _use_world_imagegen_v5:
		UiStyle.apply_world_imagegen_v5_cta_button(enter_region_btn, can_enter)
	else:
		UiStyle.apply_world_cta_button(enter_region_btn, can_enter)

func _update_world_story_preview(payload: Dictionary) -> void:
	if not _use_world_imagegen_v5:
		return
	var region_id := str(payload.get("selected_region_id", ""))
	if region_id == "us":
		var story_texture := UiStyle.load_world_imagegen_texture("wm_story_preview_north_america")
		if story_texture != null:
			world_story_preview.texture = story_texture
			world_story_preview.self_modulate = Color.WHITE
			return
	world_story_preview.texture = null
	world_story_preview.self_modulate = Color.WHITE

func _render_region(payload: Dictionary, selected_node: String) -> void:
	region_map_canvas.call("configure", "region", selected_node)
	region_map_canvas.visible = not _use_region_task_art
	region_map_backdrop.visible = _use_region_task_assetized and not _use_region_task_artboard_v3 and _region_task_map_texture != null
	region_route_layer.visible = _use_region_task_assetized and not _use_region_task_artboard_v3 and _region_task_route_texture != null
	_style_filter_button(btn_filter_sci, bool(payload.get("filters", {}).get("sci", true)))
	_style_filter_button(btn_filter_occult, bool(payload.get("filters", {}).get("occult", true)))
	_style_filter_button(btn_filter_pop, bool(payload.get("filters", {}).get("pop", true)))
	_rebuild_action_items(node_list, payload.get("nodes", []), "node")
	_rebuild_node_pins(payload.get("nodes", []))

	var has_node := selected_node != ""
	region_task_title.text = str(payload.get("node_title", "选择取材任务"))
	if has_node:
		region_task_text.text = _build_region_task_safe_text(payload)
	else:
		region_task_text.text = "[color=#27352f]选择一份任务档案，查看线索、耗时和风险。[/color]\n\n[color=#087b85]选中后可送至签批台，本页不消耗天数。[/color]"
	open_dispatch_btn.text = str(payload.get("dispatch_open_text", "送至签批台"))
	var can_open_dispatch := bool(payload.get("dispatch_open_enabled", false))
	if _use_region_task_artboard_v3:
		UiStyle.apply_region_task_artboard_v3_cta_button(open_dispatch_btn, can_open_dispatch)
	elif _use_region_task_assetized:
		if not UiStyle.apply_region_task_assetized_cta_button(open_dispatch_btn, can_open_dispatch):
			UiStyle.apply_region_task_v2_cta_button(open_dispatch_btn, can_open_dispatch)
	elif _use_region_task_art:
		UiStyle.apply_region_task_v2_cta_button(open_dispatch_btn, can_open_dispatch)
	else:
		UiStyle.apply_primary_channel_button(open_dispatch_btn, can_open_dispatch)

func _build_region_task_safe_text(payload: Dictionary) -> String:
	var lines: Array[String] = []
	var summary := _compact_region_task_sentence(str(payload.get("region_node_summary", "")), 46)
	var meta := _compact_region_task_sentence(str(payload.get("region_node_meta", "")), 34)
	var deadline := _compact_region_task_sentence(str(payload.get("region_node_deadline", "")), 24)
	var chain := _compact_region_task_sentence(str(payload.get("region_node_chain", "")), 24)
	var hint := _compact_region_task_sentence(str(payload.get("region_action_hint", "")), 28)
	if summary != "":
		lines.append("[color=#27352f]%s[/color]" % summary)
	if meta != "":
		lines.append("[color=#8c6d2d]%s[/color]" % meta)
	if deadline != "":
		lines.append("[color=#b72a22][b]%s[/b][/color]" % deadline)
	if chain != "":
		lines.append("[color=#087b85][b]%s[/b][/color]" % chain)
	if hint != "":
		lines.append("\n[color=#087b85]%s[/color]" % hint)
	return "\n".join(lines)

func _compact_region_task_sentence(value: String, max_length: int) -> String:
	var text := value.replace("\n", " ").replace("。", "").strip_edges()
	if text.length() > max_length:
		text = text.substr(0, max_length - 1) + "…"
	return text

func _render_dispatch(payload: Dictionary) -> void:
	_rebuild_action_items(staff_grid, payload.get("staff", []), "staff")
	dispatch_node_title_label.text = str(payload.get("node_title", "选择一个取材任务"))
	dispatch_node_fact_text.text = str(payload.get("node_fact_text", ""))
	selected_staff_label.text = str(payload.get("selected_staff_text", "已选择 0 / 3"))
	_render_selected_staff_slots(payload.get("selected_staff_slots", []))
	probability_label.text = str(payload.get("probability_text", "有效点：等待选人"))
	dice_text.text = str(payload.get("dice_text", ""))
	result_label.text = str(payload.get("result_text", "等待签批"))
	result_label.add_theme_color_override("font_color", payload.get("result_color", Color(0.88, 0.76, 0.36, 1.0)))
	var enabled := bool(payload.get("execute_enabled", false))
	var execute_state := str(payload.get("execute_state", "idle"))
	dispatch_summary_text.text = _build_dispatch_summary_text(payload, enabled, execute_state)
	var active_stamp := enabled or ["loading", "stamped"].has(execute_state)
	dispatch_stamp_texture.modulate = Color(1, 1, 1, 0.92 if active_stamp else 0.30)
	execute_btn.text = str(payload.get("execute_text", "签批外勤"))
	_style_dispatch_execute_button(execute_btn, enabled, execute_state)

func _render_selected_staff_slots(slot_items: Array) -> void:
	for index in range(selected_slot_labels.size()):
		var button := selected_slot_labels[index]
		var slot_data: Dictionary = {}
		if index < slot_items.size() and typeof(slot_items[index]) == TYPE_DICTIONARY:
			slot_data = slot_items[index]
		var filled := bool(slot_data.get("filled", false))
		var staff_id := str(slot_data.get("id", ""))
		button.set_meta("staff_id", staff_id if filled else "")
		button.text = "%s\n%s" % [
			str(slot_data.get("name", "空席位 %d" % [index + 1])),
			str(slot_data.get("body", "从候选编辑中加入")),
		]
		button.tooltip_text = "点击移出本次骰池" if filled else "空席位"
		_style_dispatch_slot(button, filled)

func _style_dispatch_slot(button: Button, filled: bool) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.070, 0.095, 0.100, 0.96)
	style.border_color = Color(0.18, 0.36, 0.38, 1.0)
	if filled:
		style.bg_color = Color(0.15, 0.13, 0.070, 0.98)
		style.border_color = Color(0.88, 0.64, 0.28, 1.0)
	style.set_border_width_all(1)
	style.corner_radius_top_left = 4
	style.corner_radius_top_right = 4
	style.corner_radius_bottom_left = 4
	style.corner_radius_bottom_right = 4
	style.content_margin_left = 10
	style.content_margin_right = 10
	style.content_margin_top = 6
	style.content_margin_bottom = 6
	var hover := style.duplicate()
	hover.bg_color = style.bg_color.lightened(0.08)
	var pressed := style.duplicate()
	pressed.bg_color = style.bg_color.darkened(0.08)
	button.add_theme_stylebox_override("normal", style)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("disabled", style.duplicate())
	button.add_theme_color_override("font_color", Color(0.96, 0.86, 0.55, 1.0) if filled else Color(0.56, 0.66, 0.66, 1.0))
	button.add_theme_color_override("font_hover_color", Color(1.0, 0.91, 0.60, 1.0) if filled else Color(0.56, 0.66, 0.66, 1.0))
	button.add_theme_color_override("font_pressed_color", Color(0.90, 0.72, 0.38, 1.0) if filled else Color(0.56, 0.66, 0.66, 1.0))
	button.add_theme_color_override("font_disabled_color", Color(0.56, 0.66, 0.66, 1.0))
	button.add_theme_font_size_override("font_size", 13)
	button.add_theme_constant_override("outline_size", 2)
	button.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.85))
	button.alignment = HORIZONTAL_ALIGNMENT_CENTER
	button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	button.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	button.disabled = not filled
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND if filled else Control.CURSOR_ARROW

func _style_dispatch_execute_button(button: Button, enabled: bool, execute_state: String) -> void:
	var force_visible := ["loading", "stamped"].has(execute_state)
	if not UiStyle.apply_dispatch_signoff_cta_button(button, enabled or force_visible, execute_state):
		UiStyle.apply_primary_channel_button(button, enabled or force_visible)
	button.disabled = (not enabled) or force_visible
	if execute_state == "loading":
		button.modulate = Color(1.08, 0.96, 0.76, 1.0)
	elif execute_state == "stamped":
		button.modulate = Color(0.96, 1.08, 0.88, 1.0)
	else:
		button.modulate = Color.WHITE

func _build_dispatch_summary_text(payload: Dictionary, enabled: bool, execute_state: String) -> String:
	var state_label := "[color=#9ee6c6][b]可签批[/b][/color]" if enabled else "[color=#ff8e7c][b]未就绪[/b][/color]"
	if execute_state == "loading":
		state_label = "[color=#ffd36d][b]签批中[/b][/color]"
	elif execute_state == "stamped":
		state_label = "[color=#a8ef9c][b]已盖章[/b][/color]"
	var staff_summary := _one_line_text(str(payload.get("selected_staff_text", "本次骰池 0 / 3")), 24)
	var probability_summary := _one_line_text(str(payload.get("probability_text", "有效点：等待选人")), 34)
	var result_summary := _one_line_text(str(payload.get("result_text", "等待签批")), 44)
	var cta_summary := _one_line_text(str(payload.get("execute_text", "签批外勤")), 16)
	return "[b]派遣回条[/b]  %s  |  %s  |  %s  |  %s  |  CTA：%s" % [
		state_label,
		staff_summary,
		probability_summary,
		result_summary,
		cta_summary,
	]

func _one_line_text(value: String, max_chars: int) -> String:
	var clean := value.replace("\r", " ").replace("\n", " · ").strip_edges()
	while clean.find("  ") >= 0:
		clean = clean.replace("  ", " ")
	if clean.length() > max_chars:
		return "%s..." % clean.substr(0, max_chars - 3)
	return clean

func _style_stage_header() -> void:
	stage_kicker.text = "GLOBAL CHANNEL / WORLD MYSTERIES WEEKLY"
	stage_kicker.add_theme_font_size_override("font_size", 11)
	stage_kicker.add_theme_color_override("font_color", Color(0.52, 0.84, 0.86, 1.0))
	stage_title.add_theme_font_size_override("font_size", 21)
	stage_title.add_theme_color_override("font_color", Color(0.97, 0.93, 0.74, 1.0))
	stage_title.add_theme_constant_override("outline_size", 3)
	stage_title.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.92))
	stage_note.add_theme_font_size_override("font_size", 12)
	stage_status.add_theme_font_size_override("font_size", 14)
	stage_status.add_theme_color_override("font_color", Color(0.96, 0.88, 0.64, 1.0))
	_apply_label_badge(stage_status, Color(0.08, 0.07, 0.035, 0.96), Color(0.58, 0.43, 0.18, 1.0))

func _style_world_panel_headers() -> void:
	world_index_title.text = "INDEX"
	world_index_subtitle.text = "区域索引"
	world_detail_kicker.text = "STORY / 本区选题夹"
	world_index_title.add_theme_color_override("font_color", Color(0.19, 0.24, 0.18, 1.0))
	world_index_title.add_theme_constant_override("outline_size", 1)
	world_index_title.add_theme_color_override("font_outline_color", Color(0.98, 0.88, 0.64, 0.46))
	world_index_subtitle.add_theme_font_size_override("font_size", 13)
	world_index_subtitle.add_theme_color_override("font_color", Color(0.08, 0.42, 0.43, 1.0))
	world_index_subtitle.add_theme_constant_override("outline_size", 1)
	world_index_subtitle.add_theme_color_override("font_outline_color", Color(0.98, 0.90, 0.70, 0.36))
	world_index_footer.add_theme_color_override("default_color", Color(0.76, 0.78, 0.68, 1.0))
	world_index_footer.add_theme_font_size_override("normal_font_size", 13)
	world_index_footer.add_theme_font_size_override("bold_font_size", 13)
	region_list.add_theme_constant_override("separation", 5)
	world_detail_kicker.add_theme_font_size_override("font_size", 13)
	world_detail_kicker.add_theme_color_override("font_color", Color(0.98, 0.90, 0.72, 1.0))
	_apply_label_badge(world_detail_kicker, Color(0.79, 0.14, 0.10, 0.98), Color(0.09, 0.04, 0.03, 0.94), 8)
	region_detail_title.add_theme_color_override("font_color", Color(0.075, 0.095, 0.095, 1.0))
	region_detail_title.add_theme_constant_override("outline_size", 0)
	region_detail_title.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.0))
	region_detail_text.add_theme_color_override("default_color", Color(0.18, 0.23, 0.20, 1.0))
	region_detail_text.add_theme_font_size_override("normal_font_size", 14)
	region_detail_text.add_theme_font_size_override("bold_font_size", 14)
	region_detail_text.add_theme_constant_override("line_separation", 5)
	world_story_preview.custom_minimum_size = Vector2(0.0, 112.0)
	world_story_preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_style_world_story_ticket(world_deadline_ticket, "deadline")
	_style_world_story_ticket(world_chain_ticket, "chain")

func _style_world_proof_strip() -> void:
	world_proof_strip.custom_minimum_size = Vector2(0.0, 84.0)
	world_log_title.custom_minimum_size = Vector2(112.0, 58.0)
	world_log_title.text = "CHANNEL"
	world_log_title.add_theme_font_size_override("font_size", 14)
	world_log_title.add_theme_color_override("font_color", Color(0.32, 0.82, 0.86, 1.0))
	world_log_title.add_theme_constant_override("outline_size", 2)
	world_log_title.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.88))
	_apply_label_badge(world_log_title, Color(0.018, 0.034, 0.038, 0.96), Color(0.18, 0.56, 0.60, 0.62), 4, 14, 10, 14, 10, 3)
	for chip in world_log_chips:
		_style_world_log_chip(chip, Color(0.12, 0.14, 0.13, 0.60), "neutral")
	_style_world_log_chip(world_proof_text, Color(0.08, 0.54, 0.61, 0.76), "next")

func _style_world_story_ticket(label: Label, variant: String) -> void:
	label.custom_minimum_size = Vector2(0.0, 64.0)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.autowrap_mode = TextServer.AUTOWRAP_OFF
	label.clip_text = true
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.max_lines_visible = 2 if _use_world_imagegen_v5 else 3
	label.add_theme_font_size_override("font_size", 13 if _use_world_imagegen_v5 else 12)
	label.add_theme_color_override("font_color", Color(0.14, 0.18, 0.16, 1.0))
	label.add_theme_constant_override("line_spacing", 2 if _use_world_imagegen_v5 else 3)
	UiStyle.apply_world_story_ticket_style(label, variant)

func _render_world_ticket_slots(ticket: Label, title: String, count: String, body: String, variant: String) -> void:
	ticket.text = ""
	_style_world_story_ticket(ticket, variant)
	var title_label := _ensure_overlay_label(ticket, "TicketTitle")
	var count_label := _ensure_overlay_label(ticket, "TicketCount")
	var body_label := _ensure_overlay_label(ticket, "TicketBody")
	_place_overlay_label(title_label, 122.0, 5.0, 146.0, 25.0)
	_place_overlay_label(count_label, 206.0, 5.0, 62.0, 25.0)
	_place_overlay_label(body_label, 122.0, 29.0, 64.0, 50.0)
	title_label.text = title
	count_label.text = count
	body_label.text = body
	title_label.add_theme_font_size_override("font_size", 14)
	count_label.add_theme_font_size_override("font_size", 14)
	body_label.add_theme_font_size_override("font_size", 14)
	var title_color := Color(0.62, 0.10, 0.08, 1.0) if variant == "deadline" else Color(0.04, 0.42, 0.46, 1.0)
	title_label.add_theme_color_override("font_color", title_color)
	count_label.add_theme_color_override("font_color", Color(0.12, 0.15, 0.13, 1.0))
	body_label.add_theme_color_override("font_color", Color(0.20, 0.24, 0.20, 1.0))
	count_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	for child_label in [title_label, count_label, body_label]:
		child_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		child_label.clip_text = true
		child_label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
		child_label.mouse_filter = Control.MOUSE_FILTER_IGNORE

func _ensure_overlay_label(parent: Control, child_name: String) -> Label:
	var existing := parent.get_node_or_null(child_name)
	if existing is Label:
		return existing
	var label := Label.new()
	label.name = child_name
	parent.add_child(label)
	return label

func _place_overlay_label(label: Label, left: float, top: float, right: float, bottom: float) -> void:
	label.anchor_left = 0.0
	label.anchor_top = 0.0
	label.anchor_right = 1.0
	label.anchor_bottom = 0.0
	label.offset_left = left
	label.offset_top = top
	label.offset_right = -right
	label.offset_bottom = bottom

func _render_world_story_tickets(payload: Dictionary) -> void:
	var counts: Dictionary = payload.get("region_counts", _count_world_node_tones(payload))
	var remaining_days := int(payload.get("remaining_days", 0))
	var target_count := int(counts.get("visible", payload.get("nodes", []).size()))
	var deadline_count := int(counts.get("deadline", 0))
	var clue_count := int(counts.get("clue", 0))
	var chain_count := int(counts.get("chain", 0))
	var can_enter := bool(payload.get("region_enter_enabled", false))
	var status_variant := "locked" if not can_enter else "deadline" if deadline_count > 0 else "chain" if chain_count > 0 else "selected"
	var status_title := str(payload.get("region_status_primary", "可进入" if can_enter else "锁定"))
	var status_body := "已打开" if can_enter else "未开封"
	if _use_world_imagegen_v5:
		var compact_status := "红线" if status_title == "红线升温" else "青线" if status_title == "青线追踪" else status_title
		_render_world_ticket_slots(world_deadline_ticket, "状态", compact_status, status_body, status_variant)
		_render_world_ticket_slots(world_chain_ticket, "小结", "目标%d" % target_count, "限%d 线%d 深%d" % [deadline_count, clue_count, chain_count], "chain" if can_enter else "locked")
		return
	world_deadline_ticket.text = "地区状态\n%s · 剩 %d 天\n%s" % [status_title, remaining_days, status_body]
	world_chain_ticket.text = "任务小结\n目标 %d · 限时 %d\n线索 %d · 深链 %d" % [target_count, deadline_count, clue_count, chain_count]

func _render_world_proof_strip(payload: Dictionary) -> void:
	var chip_defaults := [
		{"title": "最近变化", "body": "等待地区选择", "border": Color(0.79, 0.14, 0.10, 0.74), "variant": "deadline"},
		{"title": "地区异动", "body": "暂无", "border": Color(0.08, 0.60, 0.66, 0.74), "variant": "chain"},
		{"title": "地区预警", "body": "选择后显示", "border": Color(0.92, 0.68, 0.22, 0.72), "variant": "selected"},
	]
	var receipts: Array = payload.get("world_receipts", [])
	for receipt_index in range(mini(chip_defaults.size(), receipts.size())):
		var receipt: Dictionary = receipts[receipt_index]
		chip_defaults[receipt_index].title = str(receipt.get("title", chip_defaults[receipt_index].title))
		chip_defaults[receipt_index].body = str(receipt.get("body", chip_defaults[receipt_index].body))
		chip_defaults[receipt_index].variant = str(receipt.get("variant", chip_defaults[receipt_index].variant))
		if chip_defaults[receipt_index].variant == "locked":
			chip_defaults[receipt_index].border = Color(0.45, 0.44, 0.38, 0.76)
	for index in range(world_log_chips.size()):
		var title := str(chip_defaults[index].get("title", "回条"))
		var body := str(chip_defaults[index].get("body", ""))
		if _use_world_imagegen_v5:
			var compact_text := "%s：%s" % [title, body]
			if compact_text.length() > 28:
				compact_text = compact_text.substr(0, 27) + "…"
			world_log_chips[index].text = compact_text
		else:
			if body.length() > 16:
				body = body.substr(0, 15) + "…"
			world_log_chips[index].text = "%s\n%s" % [title, body]
		_style_world_log_chip(
			world_log_chips[index],
			chip_defaults[index].get("border", Color(0.12, 0.14, 0.13, 0.60)),
			str(chip_defaults[index].get("variant", "neutral"))
		)
	if _use_world_imagegen_v5:
		world_proof_text.visible = false
	else:
		world_proof_text.visible = true
		world_proof_text.text = "下一步\n进入地区 · 不耗天数"
		_style_world_log_chip(world_proof_text, Color(0.08, 0.54, 0.61, 0.76), "next")

func _strip_bbcode(value: String) -> String:
	var regex := RegEx.new()
	var error := regex.compile("\\[/?[^\\]]+\\]")
	if error != OK:
		return value
	return regex.sub(value, "", true)

func _count_world_node_tones(payload: Dictionary) -> Dictionary:
	var counts := {"deadline": 0, "chain": 0}
	for item in payload.get("nodes", []):
		match str(item.get("tone", "normal")):
			"deadline":
				counts["deadline"] = int(counts.get("deadline", 0)) + 1
			"chain":
				counts["chain"] = int(counts.get("chain", 0)) + 1
	return counts

func _build_world_detail_text(payload: Dictionary) -> String:
	var lines: Array[String] = []
	lines.append(str(payload.get("region_detail_text", "")))

	var node_items: Array = payload.get("nodes", [])
	if _use_world_imagegen_v5:
		lines.clear()
		var can_enter := bool(payload.get("region_enter_enabled", false))
		var title_color := "#0b6972" if can_enter else "#60615a"
		lines.append("[color=%s][b]地区简介[/b][/color]  [color=#17211c]%s[/color]" % [
			title_color,
			str(payload.get("region_brief", payload.get("region_detail_text", ""))),
		])
		lines.append("[color=#0b6972][b]任务小结[/b][/color]  [color=#17211c]%s[/color]" % [
			str(payload.get("region_summary_line", "目标 0 / 限时 0 / 线索 0 / 深链 0")),
		])
		var warning_color := "#a3261d" if not can_enter or str(payload.get("region_status_primary", "")) == "红线升温" else "#087b85"
		lines.append("[color=#0b6972][b]%s[/b][/color]  [color=%s]%s[/color]" % [
			str(payload.get("region_warning_title", "地区预警")),
			warning_color,
			str(payload.get("region_warning_text", "暂无额外预警。")),
		])
		var footer := str(payload.get("region_footer_status", "本屏不消耗天数。"))
		footer = footer.replace("后果：", "").replace("地区任务台", "任务台")
		lines.append("[color=#8c6d2d]%s[/color]" % footer)
		return _join_strings(lines, "\n")

	if not node_items.is_empty():
		var preview_lines: Array[String] = []
		var max_count := mini(2, node_items.size())
		for index in range(max_count):
			var item: Dictionary = node_items[index]
			var item_lines := str(item.get("text", "")).split("\n")
			var title := str(item_lines[0]) if item_lines.size() > 0 else str(item.get("label", "未命名线报"))
			var meta := str(item_lines[1]) if item_lines.size() > 1 else ""
			var tone := str(item.get("tone", "normal"))
			var color := "#18201f"
			if tone == "deadline":
				color = "#b72a22"
			elif tone == "chain":
				color = "#087b85"
			preview_lines.append("[color=%s]▸ %s[/color]\n  [color=#4d5c58]%s[/color]" % [color, title, meta])
		if node_items.size() > max_count:
			preview_lines.append("[color=#4d5c58]另有 %d 张夹在区域任务台。[/color]" % [node_items.size() - max_count])
		lines.append("[color=#087b85]可进入的选题[/color]\n%s" % _join_strings(preview_lines, "\n"))

	return _join_strings(lines, "\n\n")

func _build_world_index_footer_text(payload: Dictionary) -> String:
	var regions: Array = payload.get("regions", [])
	var unlocked_count := 0
	var locked_count := 0
	for item in regions:
		if bool(item.get("unlocked", true)):
			unlocked_count += 1
		else:
			locked_count += 1

	var node_items: Array = payload.get("nodes", [])
	var deadline_count := 0
	var chain_count := 0
	for item in node_items:
		match str(item.get("tone", "normal")):
			"deadline":
				deadline_count += 1
			"chain":
				chain_count += 1

	if _use_world_imagegen_v5:
		return "[b]已开封%d/%d[/b]  [color=#213530]本区%d[/color]  [color=#a3261d]红%d[/color]  [color=#087b85]青%d[/color]" % [
			unlocked_count,
			regions.size(),
			node_items.size(),
			deadline_count,
			chain_count,
		]

	return "[b]索引柜底签[/b]\n[color=#e8dfb8]已开封 %d / %d · 本区线报 %d[/color]\n[color=#ff5a48]红条截稿 %d[/color]\n[color=#32dbe3]青条追踪 %d[/color]\n[color=#9ba79a]封存 %d 区：保留缺口说明，不消耗天数。[/color]" % [
		unlocked_count,
		regions.size(),
		node_items.size(),
		deadline_count,
		chain_count,
		locked_count,
	]

func _apply_label_badge(
	label: Label,
	bg: Color,
	border: Color,
	left_width: int = 1,
	margin_left: int = 10,
	margin_top: int = 6,
	margin_right: int = 10,
	margin_bottom: int = 6,
	radius: int = 4
) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.border_width_left = left_width
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	style.content_margin_left = maxi(margin_left, left_width + 10)
	style.content_margin_top = margin_top
	style.content_margin_right = margin_right
	style.content_margin_bottom = margin_bottom
	style.shadow_color = Color(0.01, 0.015, 0.012, 0.22)
	style.shadow_size = 3
	style.shadow_offset = Vector2(2.0, 2.0)
	label.add_theme_stylebox_override("normal", style)

func _style_world_log_chip(label: Label, border: Color, variant: String) -> void:
	var font_color := Color(0.10, 0.13, 0.11, 1.0) if _use_world_imagegen_v5 else Color(0.92, 0.88, 0.70, 1.0)
	label.custom_minimum_size = Vector2(0.0, 58.0)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.autowrap_mode = TextServer.AUTOWRAP_OFF
	label.clip_text = true
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.max_lines_visible = 1 if _use_world_imagegen_v5 else 2
	label.add_theme_font_size_override("font_size", 16 if _use_world_imagegen_v5 else 11)
	label.add_theme_color_override("font_color", font_color)
	label.add_theme_constant_override("line_spacing", 0 if _use_world_imagegen_v5 else 3)
	label.add_theme_constant_override("outline_size", 0 if _use_world_imagegen_v5 else 2)
	label.add_theme_color_override("font_outline_color", Color(0.01, 0.02, 0.02, 0.0 if _use_world_imagegen_v5 else 0.88))
	UiStyle.apply_world_log_chip_texture_style(label, variant)

func _style_world_detail_body(can_enter: bool) -> void:
	if not _use_world_imagegen_v5:
		world_cta_hint.visible = false
		return
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.94, 0.86, 0.66, 0.0)
	style.border_color = Color(0.0, 0.0, 0.0, 0.0)
	style.content_margin_left = 46
	style.content_margin_top = 116
	style.content_margin_right = 18
	style.content_margin_bottom = 18
	region_detail_text.add_theme_stylebox_override("normal", style)
	region_detail_text.scroll_active = false
	region_detail_text.add_theme_color_override("default_color", Color(0.14, 0.18, 0.15, 1.0))
	region_detail_text.add_theme_font_size_override("normal_font_size", 16)
	region_detail_text.add_theme_font_size_override("bold_font_size", 16)
	region_detail_text.add_theme_constant_override("line_separation", 7)

func _render_world_cta_hint(payload: Dictionary, can_enter: bool) -> void:
	if not _use_world_imagegen_v5:
		world_cta_hint.visible = false
		return
	world_cta_hint.visible = true
	world_cta_hint.scroll_active = false
	world_cta_hint.bbcode_enabled = true
	world_cta_hint.custom_minimum_size = Vector2(0.0, 46.0)
	world_cta_hint.add_theme_font_size_override("normal_font_size", 15)
	world_cta_hint.add_theme_font_size_override("bold_font_size", 15)
	world_cta_hint.add_theme_constant_override("line_separation", 2)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.015, 0.045, 0.048, 0.62)
	style.border_color = Color(0.10, 0.42, 0.44, 0.70)
	style.set_border_width_all(1)
	style.content_margin_left = 18
	style.content_margin_top = 10
	style.content_margin_right = 14
	style.content_margin_bottom = 9
	world_cta_hint.add_theme_stylebox_override("normal", style)
	if can_enter:
		world_cta_hint.text = "[color=#8ec8c2][b]进入区域任务台[/b] · 不消耗天数[/color]"
	else:
		var gap := str(payload.get("region_unlock_gap_short", payload.get("region_unlock_gap", "缺少线索许可")))
		world_cta_hint.text = "[color=#ff6755][b]缺口：[/b][/color][color=#f1d99b]%s[/color]" % gap

func _apply_left_strip_badge(
	label: Label,
	bg: Color,
	strip: Color,
	left_width: int,
	margin_left: int,
	margin_top: int,
	margin_right: int,
	margin_bottom: int,
	radius: int
) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = strip
	style.set_border_width_all(0)
	style.border_width_left = left_width
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	style.content_margin_left = maxi(margin_left, left_width + 12)
	style.content_margin_top = margin_top
	style.content_margin_right = margin_right
	style.content_margin_bottom = margin_bottom
	style.shadow_color = Color(0.01, 0.015, 0.012, 0.20)
	style.shadow_size = 3
	style.shadow_offset = Vector2(2.0, 2.0)
	label.add_theme_stylebox_override("normal", style)

func _style_filter_button(button: Button, selected: bool) -> void:
	button.custom_minimum_size = Vector2(0.0, 32.0)
	if _use_region_task_assetized:
		if not UiStyle.apply_region_task_assetized_filter_button(button, selected):
			UiStyle.apply_region_task_v2_filter_button(button, selected)
	elif _use_region_task_art:
		UiStyle.apply_region_task_v2_filter_button(button, selected)
	else:
		UiStyle.apply_button_style(button, selected, true)

func _rebuild_action_items(container: Control, items: Array, item_kind: String) -> void:
	_clear_container(container)
	for item in items:
		var action_item := ActionItemScene.instantiate()
		container.add_child(action_item)
		var item_data: Dictionary = item.duplicate(true)
		if item_kind == "region" and _use_world_imagegen_v5:
			item_data["world_imagegen_v5"] = true
		if item_kind == "node" and _use_region_task_art:
			if _use_region_task_artboard_v3:
				item_data["region_task_artboard_v3"] = true
				item_data["min_height"] = 150.0
			elif _use_region_task_assetized:
				item_data["region_task_assetized"] = true
				item_data["min_height"] = 120.0
			else:
				item_data["region_task_v2"] = true
				item_data["min_height"] = 96.0
		if item_kind == "staff":
			item_data["min_height"] = 148.0
		action_item.bind(item_data)
		action_item.item_pressed.connect(func(item_id) -> void:
			match item_kind:
				"region":
					region_selected.emit(str(item_id))
				"node":
					node_selected.emit(str(item_id))
				"staff":
					staff_toggled.emit(str(item_id))
		)

func _rebuild_region_pins(items: Array) -> void:
	_clear_container(world_pin_layer)
	for item in items:
		var pos: Dictionary = item.get("map_pos", {"x": 0.5, "y": 0.5})
		var enabled := bool(item.get("unlocked", item.get("enabled", true)))
		var pin := _make_pin_button(
			_format_region_pin_label(item),
			float(pos.get("x", 0.5)),
			float(pos.get("y", 0.5)),
			bool(item.get("selected", false)),
			enabled,
			str(item.get("tone", "normal"))
		)
		world_pin_layer.add_child(pin)
		pin.pressed.connect(func() -> void:
			region_selected.emit(str(item.get("id", "")))
		)

func _rebuild_node_pins(items: Array) -> void:
	_clear_container(node_pin_layer)
	for item in items:
		var pos: Dictionary = item.get("map_pos", {"x": 0.5, "y": 0.5})
		var pin := _make_pin_button(
			str(item.get("pin_label", item.get("label", ""))),
			float(pos.get("x", 0.5)),
			float(pos.get("y", 0.5)),
			bool(item.get("selected", false)),
			bool(item.get("enabled", true)),
			str(item.get("tone", "normal"))
		)
		node_pin_layer.add_child(pin)
		pin.pressed.connect(func() -> void:
			node_selected.emit(str(item.get("id", "")))
		)

func _make_pin_button(label: String, x: float, y: float, selected: bool, enabled: bool, tone: String) -> Button:
	var button := Button.new()
	button.text = label
	button.autowrap_mode = TextServer.AUTOWRAP_OFF
	button.alignment = HORIZONTAL_ALIGNMENT_CENTER
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND if enabled else Control.CURSOR_ARROW
	button.anchor_left = x
	button.anchor_top = y
	button.anchor_right = x
	button.anchor_bottom = y
	if _current_view_mode == "region" and _use_region_task_artboard_v3:
		button.text = ""
		button.offset_left = -36.0
		button.offset_top = -58.0
		button.offset_right = 36.0
		button.offset_bottom = 14.0
		button.custom_minimum_size = Vector2(72.0, 72.0)
		UiStyle.apply_region_task_artboard_v3_invisible_hotspot(button, enabled)
		return button
	if _current_view_mode == "region" and _use_region_task_assetized:
		button.text = ""
		button.offset_left = -32.0
		button.offset_top = -56.0
		button.offset_right = 32.0
		button.offset_bottom = 8.0
		button.custom_minimum_size = Vector2(64.0, 64.0)
		if UiStyle.apply_region_task_assetized_pin_button(button, selected, enabled, tone):
			return button
		button.text = label
	if _current_view_mode == "region" and _use_region_task_art:
		if selected:
			button.text = _compact_region_pin_label(label)
			button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			button.offset_left = -62.0
			button.offset_top = -42.0
			button.offset_right = 62.0
			button.offset_bottom = 22.0
			button.custom_minimum_size = Vector2(124.0, 64.0)
			UiStyle.apply_region_task_v2_pin_style(button, selected, enabled, tone)
		else:
			button.text = ""
			button.offset_left = -16.0
			button.offset_top = -16.0
			button.offset_right = 16.0
			button.offset_bottom = 16.0
			button.custom_minimum_size = Vector2(32.0, 32.0)
			UiStyle.apply_region_task_v2_anchor_pin_style(button, enabled, tone)
		return button
	if _use_world_imagegen_v5:
		button.text = ""
		button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		button.offset_left = -46.0
		button.offset_top = -96.0
		button.offset_right = 46.0
		button.offset_bottom = 18.0
		button.custom_minimum_size = Vector2(92.0, 114.0)
		if UiStyle.apply_world_imagegen_v5_pin_style(button, selected, enabled, tone):
			return button
		button.text = label
	if enabled:
		button.offset_left = -52.0
		button.offset_top = -102.0
		button.offset_right = 52.0
		button.offset_bottom = 22.0
		button.custom_minimum_size = Vector2(104.0, 124.0)
	else:
		button.offset_left = -48.0
		button.offset_top = -96.0
		button.offset_right = 48.0
		button.offset_bottom = 18.0
		button.custom_minimum_size = Vector2(96.0, 114.0)
	UiStyle.apply_map_pin_style(button, selected, enabled, tone)
	if not enabled:
		button.modulate = Color(1.06, 0.95, 0.80, 0.94) if selected else Color(0.82, 0.82, 0.74, 0.72)
	return button

func _style_region_task_board() -> void:
	if not _use_region_task_art:
		return
	if _use_region_task_artboard_v3:
		region_view.add_theme_constant_override("margin_left", 110)
		region_view.add_theme_constant_override("margin_top", 116)
		region_view.add_theme_constant_override("margin_right", 70)
		region_view.add_theme_constant_override("margin_bottom", 104)
		region_hbox.add_theme_constant_override("separation", 40)
		node_index_panel.custom_minimum_size = Vector2(430.0, 840.0)
		region_map_panel.custom_minimum_size = Vector2(760.0, 760.0)
		region_task_panel.custom_minimum_size = Vector2(470.0, 850.0)
		region_map_panel.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		region_map_panel.size_flags_vertical = Control.SIZE_SHRINK_BEGIN
		UiStyle.apply_region_task_artboard_v3_layout_panel_style(node_index_panel, "left")
		UiStyle.apply_region_task_artboard_v3_layout_panel_style(region_map_panel, "map")
		UiStyle.apply_region_task_artboard_v3_layout_panel_style(region_task_panel, "right")
		back_to_world_btn.visible = false
		node_index_title.visible = false
		filter_row.visible = false
	elif _use_region_task_assetized:
		region_view.add_theme_constant_override("margin_left", 50)
		region_view.add_theme_constant_override("margin_top", 124)
		region_view.add_theme_constant_override("margin_right", 50)
		region_view.add_theme_constant_override("margin_bottom", 110)
		region_hbox.add_theme_constant_override("separation", 30)
		node_index_panel.custom_minimum_size = Vector2(410.0, 840.0)
		region_map_panel.custom_minimum_size = Vector2(960.0, 742.0)
		region_task_panel.custom_minimum_size = Vector2(386.0, 840.0)
		region_map_panel.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		region_map_panel.size_flags_vertical = Control.SIZE_SHRINK_BEGIN
		UiStyle.apply_region_task_assetized_layout_panel_style(node_index_panel, "left")
		UiStyle.apply_region_task_assetized_layout_panel_style(region_map_panel, "map")
		UiStyle.apply_region_task_assetized_layout_panel_style(region_task_panel, "right")
		back_to_world_btn.visible = true
		node_index_title.visible = true
		filter_row.visible = true
	else:
		region_view.add_theme_constant_override("margin_left", 104)
		region_view.add_theme_constant_override("margin_top", 96)
		region_view.add_theme_constant_override("margin_right", 58)
		region_view.add_theme_constant_override("margin_bottom", 112)
		region_hbox.add_theme_constant_override("separation", 22)
		node_index_panel.custom_minimum_size = Vector2(440.0, 0.0)
		region_task_panel.custom_minimum_size = Vector2(460.0, 0.0)
		region_map_panel.size_flags_stretch_ratio = 1.0
		UiStyle.apply_region_task_v2_panel_style(node_index_panel, "left")
		UiStyle.apply_region_task_v2_panel_style(region_map_panel, "map")
		UiStyle.apply_region_task_v2_panel_style(region_task_panel, "right")
		back_to_world_btn.visible = true
		node_index_title.visible = true
		filter_row.visible = true
	back_to_world_btn.text = "返回地图"
	back_to_world_btn.custom_minimum_size = Vector2(118.0, 28.0) if _use_region_task_assetized else Vector2(132.0, 30.0)
	back_to_world_btn.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	UiStyle.apply_region_task_v2_small_button(back_to_world_btn)
	node_index_title.add_theme_color_override("font_color", Color(0.12, 0.15, 0.13, 1.0))
	node_index_title.add_theme_font_size_override("font_size", 20 if _use_region_task_assetized else 22)
	node_index_title.add_theme_constant_override("outline_size", 0)
	region_task_title.add_theme_color_override("font_color", Color(0.09, 0.12, 0.11, 1.0))
	region_task_title.add_theme_font_size_override("font_size", 24)
	region_task_title.add_theme_constant_override("outline_size", 0)
	region_task_title.clip_text = true
	region_task_title.autowrap_mode = TextServer.AUTOWRAP_OFF
	region_task_title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	region_task_title.max_lines_visible = 1
	region_task_title.custom_minimum_size = Vector2(0.0, 0.0)
	region_task_text.add_theme_color_override("default_color", Color(0.13, 0.17, 0.15, 1.0))
	region_task_text.add_theme_font_size_override("normal_font_size", 17)
	region_task_text.add_theme_font_size_override("bold_font_size", 17)
	region_task_text.add_theme_constant_override("line_separation", 7)
	region_task_text.scroll_active = false
	region_task_text.custom_minimum_size = Vector2(0.0, 0.0)
	if _use_region_task_artboard_v3:
		region_task_title.add_theme_font_size_override("font_size", 22)
		region_task_title.custom_minimum_size = Vector2(0.0, 108.0)
		region_task_text.add_theme_font_size_override("normal_font_size", 16)
		region_task_text.add_theme_font_size_override("bold_font_size", 16)
		region_task_text.add_theme_constant_override("line_separation", 6)
		open_dispatch_btn.custom_minimum_size = Vector2(0.0, 72.0)
		open_dispatch_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	elif _use_region_task_assetized:
		open_dispatch_btn.custom_minimum_size = Vector2(0.0, 64.0)
		open_dispatch_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	else:
		open_dispatch_btn.custom_minimum_size = Vector2(260.0, 44.0)
		open_dispatch_btn.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	node_list.add_theme_constant_override("separation", 12 if _use_region_task_artboard_v3 else 8)

func _compact_region_pin_label(label: String) -> String:
	var lines := label.split("\n")
	if lines.size() < 2:
		return label.substr(0, 8)
	var title := str(lines[1]).strip_edges()
	if title.length() > 8:
		title = title.substr(0, 7) + "…"
	return "%s\n%s" % [str(lines[0]).strip_edges(), title]

func _format_region_pin_label(item: Dictionary) -> String:
	if not bool(item.get("unlocked", true)):
		if bool(item.get("selected", false)):
			return "锁"
		return ""
	if bool(item.get("selected", false)):
		return "已选"
	return ""

func _clear_container(node: Node) -> void:
	for child in node.get_children():
		node.remove_child(child)
		child.queue_free()

func _join_strings(parts: Array[String], separator: String) -> String:
	var result := ""
	for index in range(parts.size()):
		if index > 0:
			result += separator
		result += parts[index]
	return result
