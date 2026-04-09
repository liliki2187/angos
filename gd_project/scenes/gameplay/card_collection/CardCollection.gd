extends Control
# ============================================================
# 卡牌图鉴场景
# 功能：
#   - 展示 100 张占位卡牌，每行 5 张（1:2 宽高比）
#   - 支持垂直滚动浏览
#   - 点击卡牌弹出详情页（标题 + 图片 + 介绍）
#   - 点击遮罩层或关闭按钮关闭详情
# ============================================================

# 场景节点引用
@onready var btn_back: Button = get_node_or_null("Header/HBox/BtnBack")
@onready var grid: GridContainer = get_node_or_null("ScrollContainer/GridContainer")
@onready var card_detail: PanelContainer = get_node_or_null("CardDetail")
@onready var dimmer: ColorRect = get_node_or_null("Dimmer")

var _detail_shown := false

func _set_full_rect(ctrl: Control):
	ctrl.anchor_left = 0.0
	ctrl.anchor_top = 0.0
	ctrl.anchor_right = 1.0
	ctrl.anchor_bottom = 1.0
	ctrl.offset_left = 0.0
	ctrl.offset_top = 0.0
	ctrl.offset_right = 0.0
	ctrl.offset_bottom = 0.0

func _set_center_rect(ctrl: Control, half_w: float, half_h: float):
	ctrl.anchor_left = 0.5
	ctrl.anchor_top = 0.5
	ctrl.anchor_right = 0.5
	ctrl.anchor_bottom = 0.5
	ctrl.offset_left = -half_w
	ctrl.offset_top = -half_h
	ctrl.offset_right = half_w
	ctrl.offset_bottom = half_h

func _ready():
	_resolve_nodes()
	Globals.log("CardCollection", "_ready() called")
	Globals.log("CardCollection", "  btn_back valid=%s" % str(is_instance_valid(btn_back)))
	Globals.log("CardCollection", "  grid valid=%s" % str(is_instance_valid(grid)))
	Globals.log("CardCollection", "  card_detail valid=%s" % str(is_instance_valid(card_detail)))
	Globals.log("CardCollection", "  dimmer valid=%s" % str(is_instance_valid(dimmer)))

	if is_instance_valid(btn_back):
		if not btn_back.pressed.is_connected(_on_back):
			btn_back.pressed.connect(_on_back)
		Globals.log("CardCollection", "btn_back.pressed connected")
	else:
		Globals.log_error("CardCollection", "btn_back node not found!")

	if is_instance_valid(dimmer):
		dimmer.mouse_filter = Control.MOUSE_FILTER_IGNORE
		if not dimmer.gui_input.is_connected(_on_dimmer_input):
			dimmer.gui_input.connect(_on_dimmer_input)

	_populate_cards()

func _resolve_nodes():
	if not is_instance_valid(btn_back):
		btn_back = find_child("BtnBack", true, false) as Button
	if not is_instance_valid(grid):
		grid = find_child("GridContainer", true, false) as GridContainer
	if not is_instance_valid(card_detail):
		card_detail = find_child("CardDetail", true, false) as PanelContainer
	if not is_instance_valid(dimmer):
		dimmer = find_child("Dimmer", true, false) as ColorRect

func _populate_cards():
	"""生成所有占位卡牌并添加到网格中"""
	var count: int = int(Globals.card.get("count", 0))
	var card_w: float = float(Globals.card.get("width", 100))
	var card_h: float = float(Globals.card.get("height", 200))
	Globals.log("CardCollection", "_populate_cards() count=%d" % count)

	if not is_instance_valid(grid):
		Globals.log_error("CardCollection", "grid node not valid!")
		return

	for i in range(count):
		var card = _make_card(i)
		if card != null:
			grid.add_child(card)
		else:
			Globals.log_error("CardCollection", "_make_card returned null at index %d" % i)

	Globals.log("CardCollection", "done, grid children=%d" % grid.get_child_count())
	Globals.log("CardCollection", "  grid size=%s pos=%s" % [str(grid.size), str(grid.global_position)])

func _make_card(index: int) -> PanelContainer:
	"""创建单张卡牌控件（标题 → 图片占位框 → 介绍文字）"""
	var card_w: float = float(Globals.card.get("width", 100))
	var card_h: float = float(Globals.card.get("height", 200))
	var colors = Globals.theme_colors

	var panel = PanelContainer.new()
	panel.custom_minimum_size = Vector2(card_w, card_h)

	var style = StyleBoxFlat.new()
	style.bg_color = colors["bg_card"]
	style.corner_radius_top_left = 6
	style.corner_radius_top_right = 6
	style.corner_radius_bottom_left = 6
	style.corner_radius_bottom_right = 6
	style.set_border_width_all(1)
	style.border_color = colors["border"]
	panel.add_theme_stylebox_override("panel", style)

	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 4)
	_set_full_rect(vbox)
	panel.add_child(vbox)

	# 标题
	var title = Label.new()
	title.text = "卡牌 #%d" % index
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 12)
	title.add_theme_color_override("font_color", colors["text_primary"])
	vbox.add_child(title)

	# 图片占位框
	var img_bg = PanelContainer.new()
	img_bg.custom_minimum_size = Vector2(card_w - 16, card_w - 16)
	var img_style = StyleBoxFlat.new()
	img_style.bg_color = colors["bg_image"]
	img_style.corner_radius_top_left = 4
	img_style.corner_radius_top_right = 4
	img_style.corner_radius_bottom_left = 4
	img_style.corner_radius_bottom_right = 4
	img_bg.add_theme_stylebox_override("panel", img_style)
	vbox.add_child(img_bg)

	var img_label = Label.new()
	img_label.text = "🖼"
	img_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	img_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_set_full_rect(img_label)
	img_bg.add_child(img_label)

	# 介绍文字
	var desc = Label.new()
	desc.text = "神秘的卡牌..."
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	desc.add_theme_font_size_override("font_size", 10)
	desc.add_theme_color_override("font_color", colors["text_secondary"])
	vbox.add_child(desc)

	# 透明点击区域
	var btn = Button.new()
	btn.text = ""
	btn.flat = true
	btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_set_full_rect(btn)
	btn.add_theme_stylebox_override("normal", StyleBoxEmpty.new())
	btn.add_theme_stylebox_override("hover", StyleBoxEmpty.new())
	btn.add_theme_stylebox_override("pressed", StyleBoxEmpty.new())
	btn.pressed.connect(_on_card_clicked.bind(index))
	panel.add_child(btn)

	return panel

func _on_card_clicked(index: int):
	Globals.log("CardCollection", "card clicked #%d" % index)
	_show_card_detail(index)

func _show_card_detail(index: int):
	if is_instance_valid(dimmer):
		dimmer.visible = true
		dimmer.mouse_filter = Control.MOUSE_FILTER_STOP
	_detail_shown = true
	_populate_detail(index)

func _populate_detail(index: int):
	"""构建卡牌详情页（标题 + 大图 + 介绍 + 关闭按钮）"""
	Globals.log("CardCollection", "detail #%d" % index)
	var colors = Globals.theme_colors

	for child in card_detail.get_children():
		child.queue_free()

	var style = StyleBoxFlat.new()
	style.bg_color = colors["bg_panel"]
	style.set_border_width_all(2)
	style.border_color = colors["border_detail"]
	style.corner_radius_top_left = 10
	style.corner_radius_top_right = 10
	style.corner_radius_bottom_left = 10
	style.corner_radius_bottom_right = 10
	card_detail.add_theme_stylebox_override("panel", style)

	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 12)
	_set_center_rect(vbox, 120.0, 180.0)
	card_detail.add_child(vbox)

	var title = Label.new()
	title.text = "卡牌 #%d" % index
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 22)
	title.add_theme_color_override("font_color", Color(0.95, 0.9, 1.0))
	vbox.add_child(title)

	var img_bg = PanelContainer.new()
	img_bg.custom_minimum_size = Vector2(200, 200)
	var img_style = StyleBoxFlat.new()
	img_style.bg_color = colors["bg_image"]
	img_style.corner_radius_top_left = 8
	img_style.corner_radius_top_right = 8
	img_style.corner_radius_bottom_left = 8
	img_style.corner_radius_bottom_right = 8
	img_bg.add_theme_stylebox_override("panel", img_style)
	vbox.add_child(img_bg)

	var img_label = Label.new()
	img_label.text = "🖼 卡牌图片"
	img_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	img_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_set_full_rect(img_label)
	img_bg.add_child(img_label)

	var desc = Label.new()
	desc.text = "这是第 %d 张卡牌的详细介绍。\n这张卡牌蕴含着神秘的力量，\n等待着被主人唤醒..." % index
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	desc.add_theme_font_size_override("font_size", 14)
	desc.add_theme_color_override("font_color", colors["text_dim"])
	vbox.add_child(desc)

	var btn_close = Button.new()
	btn_close.text = "关闭"
	btn_close.custom_minimum_size = Vector2(120, 36)
	vbox.add_child(btn_close)
	btn_close.pressed.connect(_hide_card_detail)

	card_detail.visible = true

func _hide_card_detail():
	if is_instance_valid(card_detail):
		card_detail.visible = false
	if is_instance_valid(dimmer):
		dimmer.visible = false
		dimmer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_detail_shown = false

func _on_dimmer_input(event: InputEvent):
	if _detail_shown and event is InputEventMouseButton and event.pressed:
		_hide_card_detail()

func _on_back():
	call_deferred("_goto_main_menu")

func _goto_main_menu():
	var path := str(Globals.scene_paths.get("main_menu", "res://scenes/ui/main_menu/MainMenu.tscn"))
	Globals.log("CardCollection", "_goto_main_menu() -> %s" % path)
	if not ResourceLoader.exists(path):
		Globals.log_error("CardCollection", "main menu scene not found: %s" % path)
		return
	var err = get_tree().change_scene_to_file(path)
	if err != OK:
		Globals.log_error("CardCollection", "change_scene failed: %d" % err)
