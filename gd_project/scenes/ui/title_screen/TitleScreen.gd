extends Control

const HERO_ART := "res://Assets/ui/angus_packaging/title_screen/title-screen-keyart-a-magazine-action.png"
const OFFICE_SCENE := "res://scenes/ui/editorial_office/EditorialOfficeEntry.tscn"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const LEGACY_MENU_SCENE := "res://scenes/ui/main_menu/MainMenu.tscn"

var ui_font: SystemFont
var feedback: Label


func _ready() -> void:
	_setup_font()
	_build_screen()


func _setup_font() -> void:
	ui_font = SystemFont.new()
	ui_font.font_names = PackedStringArray([
		"Microsoft YaHei",
		"Noto Sans CJK SC",
		"SimHei",
		"Arial Unicode MS",
	])


func _build_screen() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	_add_full_texture(HERO_ART)
	_add_atmosphere_layer()
	_add_brand_lockup()
	_add_launch_panel()
	_add_issue_strip()


func _add_full_texture(path: String) -> TextureRect:
	var texture := TextureRect.new()
	texture.texture = load(path)
	texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	texture.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(texture)
	return texture


func _add_atmosphere_layer() -> void:
	var atmosphere := ColorRect.new()
	atmosphere.color = Color.WHITE
	atmosphere.mouse_filter = Control.MOUSE_FILTER_IGNORE
	atmosphere.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	var shader := Shader.new()
	shader.code = """
shader_type canvas_item;

uniform vec2 focus = vec2(0.205, 0.285);
uniform float grain_alpha = 0.08;
uniform float scanline_alpha = 0.12;
uniform float grid_alpha = 0.10;

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void fragment() {
	vec2 p = SCREEN_UV;
	float focus_dist = distance(p, focus);
	float read_pool = 1.0 - smoothstep(0.10, 0.48, focus_dist);
	float left_fade = 1.0 - smoothstep(0.18, 0.52, p.x);
	float right_vignette = smoothstep(0.44, 0.92, p.x);
	float bottom_vignette = smoothstep(0.55, 1.0, p.y);
	float edge_vignette = 1.0 - smoothstep(0.52, 0.86, distance(p, vec2(0.55, 0.5)));
	float scanline = step(0.55, fract(p.y * 270.0)) * scanline_alpha;
	float grid_x = step(0.992, fract(p.x * 21.0));
	float grid_y = step(0.991, fract(p.y * 12.0));
	float grid = clamp(grid_x + grid_y, 0.0, 1.0) * grid_alpha * left_fade;
	float grain = (hash(floor(p * vec2(360.0, 210.0))) - 0.5) * grain_alpha;
	vec3 cyan = vec3(0.04, 0.44, 0.52);
	vec3 red = vec3(0.72, 0.05, 0.04);
	vec3 ink = vec3(0.0, 0.0, 0.0);
	vec3 color = ink * (0.30 + 0.28 * left_fade + 0.18 * right_vignette + 0.12 * bottom_vignette);
	color += cyan * grid;
	color += red * smoothstep(0.72, 1.0, p.x) * 0.10;
	color += vec3(grain);
	float alpha = 0.18 + left_fade * 0.48 + right_vignette * 0.20 + bottom_vignette * 0.16 - read_pool * 0.14 + scanline;
	COLOR = vec4(color, clamp(alpha, 0.0, 0.72));
}
"""
	var material := ShaderMaterial.new()
	material.shader = shader
	atmosphere.material = material
	add_child(atmosphere)


func _add_brand_lockup() -> void:
	var lockup := Control.new()
	lockup.position = Vector2(76.0, 72.0)
	lockup.size = Vector2(560.0, 176.0)
	lockup.rotation_degrees = -1.6
	add_child(lockup)

	var shadow_red := Panel.new()
	shadow_red.position = Vector2(10.0, 16.0)
	shadow_red.size = Vector2(532.0, 128.0)
	shadow_red.add_theme_stylebox_override("panel", _style_panel(Color(0.55, 0.08, 0.055, 0.58), Color(0.55, 0.08, 0.055, 0.0), 0.0))
	lockup.add_child(shadow_red)

	var shadow_cyan := Panel.new()
	shadow_cyan.position = Vector2(20.0, 6.0)
	shadow_cyan.size = Vector2(532.0, 128.0)
	shadow_cyan.add_theme_stylebox_override("panel", _style_panel(Color(0.03, 0.31, 0.35, 0.34), Color(0.03, 0.31, 0.35, 0.0), 0.0))
	lockup.add_child(shadow_cyan)

	var sign := Panel.new()
	sign.position = Vector2.ZERO
	sign.size = Vector2(532.0, 128.0)
	sign.add_theme_stylebox_override("panel", _style_panel(Color(0.032, 0.046, 0.045, 0.90), Color(0.92, 0.86, 0.68, 0.70), 0.0))
	lockup.add_child(sign)

	var red_bar := ColorRect.new()
	red_bar.position = Vector2(0.0, 0.0)
	red_bar.size = Vector2(18.0, 128.0)
	red_bar.color = Color(0.92, 0.22, 0.16, 0.96)
	red_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	sign.add_child(red_bar)

	var cyan_tab := ColorRect.new()
	cyan_tab.position = Vector2(486.0, 12.0)
	cyan_tab.size = Vector2(36.0, 12.0)
	cyan_tab.color = Color(0.10, 0.78, 0.86, 0.86)
	cyan_tab.mouse_filter = Control.MOUSE_FILTER_IGNORE
	sign.add_child(cyan_tab)

	var title_group := Control.new()
	title_group.position = Vector2(34.0, 23.0)
	title_group.size = Vector2(478.0, 70.0)
	sign.add_child(title_group)
	_add_print_label(title_group, "世界未解之谜周刊", Vector2.ZERO, 42)

	var underline := ColorRect.new()
	underline.position = Vector2(90.0, 60.0)
	underline.size = Vector2(90.0, 4.0)
	underline.color = Color(0.92, 0.22, 0.16, 0.96)
	underline.mouse_filter = Control.MOUSE_FILTER_IGNORE
	title_group.add_child(underline)

	var subtitle := _placed_label("主编室 · WORLD MYSTERIES WEEKLY", Vector2(36.0, 90.0), Vector2(440.0, 24.0), 13, Color(0.86, 0.82, 0.68, 0.86), true)
	sign.add_child(subtitle)

	var pin_line := ColorRect.new()
	pin_line.position = Vector2(488.0, 105.0)
	pin_line.size = Vector2(56.0, 2.0)
	pin_line.rotation_degrees = -12.0
	pin_line.color = Color(0.92, 0.86, 0.68, 0.52)
	pin_line.mouse_filter = Control.MOUSE_FILTER_IGNORE
	lockup.add_child(pin_line)


func _add_launch_panel() -> void:
	var launch := PanelContainer.new()
	launch.position = Vector2(78.0, 276.0)
	launch.size = Vector2(438.0, 348.0)
	launch.add_theme_stylebox_override("panel", _style_panel(Color(0.018, 0.032, 0.035, 0.60), Color(0.12, 0.76, 0.84, 0.28), 8.0))
	add_child(launch)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 22)
	margin.add_theme_constant_override("margin_top", 20)
	margin.add_theme_constant_override("margin_right", 22)
	margin.add_theme_constant_override("margin_bottom", 18)
	launch.add_child(margin)

	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 14)
	margin.add_child(box)

	var kicker_row := HBoxContainer.new()
	kicker_row.add_theme_constant_override("separation", 9)
	box.add_child(kicker_row)
	kicker_row.add_child(_rule(Color(0.93, 0.22, 0.18, 0.96), Vector2(30.0, 2.0)))
	kicker_row.add_child(_label("EDITORIAL START", 12, Color(0.15, 0.82, 0.9, 1.0), true))
	kicker_row.add_child(_rule(Color(0.93, 0.22, 0.18, 0.62), Vector2(30.0, 2.0)))

	var headline := _label("推开编辑部，开始本期。", 31, Color(1.0, 0.95, 0.78, 1.0), true)
	headline.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(headline)

	var copy := _label("不是去破案，而是把异常、来信和势力压力排成本周议程，再决定这一期怎么刊发。", 15, Color(0.88, 0.86, 0.76, 0.80), false)
	copy.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(copy)

	var flow := HBoxContainer.new()
	flow.add_theme_constant_override("separation", 8)
	box.add_child(flow)
	flow.add_child(_flow_chip("待办"))
	flow.add_child(_flow_arrow())
	flow.add_child(_flow_chip("编辑会"))
	flow.add_child(_flow_arrow())
	flow.add_child(_flow_chip("发刊"))

	var spacer := Control.new()
	spacer.custom_minimum_size = Vector2(0.0, 4.0)
	box.add_child(spacer)

	var start_btn := _button("进入编辑部  →", Color(0.05, 0.55, 0.67, 0.98), Color(0.16, 0.84, 0.92, 0.92), 19, true)
	start_btn.pressed.connect(_goto_scene.bind(OFFICE_SCENE))
	box.add_child(start_btn)

	feedback = _label("", 13, Color(0.17, 0.82, 0.9, 0.9), true)
	feedback.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(feedback)

	_add_dev_links()


func _add_dev_links() -> void:
	var dev := HBoxContainer.new()
	dev.position = Vector2(82.0, 648.0)
	dev.size = Vector2(390.0, 34.0)
	dev.add_theme_constant_override("separation", 8)
	add_child(dev)

	var weekly_btn := _button("开发：周循环", Color(0.04, 0.052, 0.055, 0.34), Color(0.92, 0.86, 0.68, 0.10), 11, false)
	weekly_btn.custom_minimum_size = Vector2(120.0, 30.0)
	weekly_btn.pressed.connect(_goto_scene.bind(WEEKLY_RUN_SCENE))
	dev.add_child(weekly_btn)

	var legacy_btn := _button("旧菜单 / PSD", Color(0.04, 0.052, 0.055, 0.28), Color(0.92, 0.86, 0.68, 0.08), 11, false)
	legacy_btn.custom_minimum_size = Vector2(120.0, 30.0)
	legacy_btn.pressed.connect(_goto_scene.bind(LEGACY_MENU_SCENE))
	dev.add_child(legacy_btn)


func _add_issue_strip() -> void:
	var strip := HBoxContainer.new()
	strip.position = Vector2(78.0, 1018.0)
	strip.size = Vector2(520.0, 24.0)
	strip.add_theme_constant_override("separation", 10)
	add_child(strip)

	var dot := ColorRect.new()
	dot.custom_minimum_size = Vector2(9.0, 9.0)
	dot.color = Color(0.93, 0.22, 0.18, 0.86)
	dot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	strip.add_child(dot)
	strip.add_child(_label("Godot 桌面效果版 · 标题页视觉落地", 12, Color(0.86, 0.82, 0.68, 0.48), true))


func _goto_scene(path: String) -> void:
	var error := get_tree().change_scene_to_file(path)
	if error != OK:
		feedback.text = "场景未能打开：%s" % path
		push_error("[TitleScreen] change_scene failed: %s" % path)


func _add_print_label(parent: Control, text_value: String, pos: Vector2, font_size: int) -> void:
	var shadow := _placed_label(text_value, pos + Vector2(0.0, 6.0), Vector2(520.0, 70.0), font_size, Color(0.0, 0.0, 0.0, 0.72), true)
	parent.add_child(shadow)
	var cyan := _placed_label(text_value, pos + Vector2(3.0, -2.0), Vector2(520.0, 70.0), font_size, Color(0.12, 0.78, 0.86, 0.52), true)
	parent.add_child(cyan)
	var red := _placed_label(text_value, pos + Vector2(-3.0, 3.0), Vector2(520.0, 70.0), font_size, Color(0.93, 0.22, 0.18, 0.58), true)
	parent.add_child(red)
	var main := _placed_label(text_value, pos, Vector2(520.0, 70.0), font_size, Color(1.0, 0.95, 0.78, 1.0), true)
	main.add_theme_constant_override("outline_size", 2)
	main.add_theme_color_override("font_outline_color", Color(0.02, 0.018, 0.012, 0.92))
	parent.add_child(main)


func _flow_chip(text_value: String) -> Label:
	var chip := _label(text_value, 11, Color(0.90, 0.86, 0.68, 0.78), true)
	chip.custom_minimum_size = Vector2(54.0, 22.0)
	chip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	chip.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return chip


func _flow_arrow() -> Label:
	var arrow := _label("→", 12, Color(0.12, 0.78, 0.86, 0.62), true)
	arrow.custom_minimum_size = Vector2(18.0, 22.0)
	arrow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return arrow


func _rule(color: Color, size_value: Vector2) -> ColorRect:
	var rule := ColorRect.new()
	rule.custom_minimum_size = size_value
	rule.color = color
	rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return rule


func _placed_label(text_value: String, pos: Vector2, size_value: Vector2, font_size: int, color: Color, bold: bool) -> Label:
	var label := _label(text_value, font_size, color, bold)
	label.position = pos
	label.size = size_value
	return label


func _label(text_value: String, font_size: int, color: Color, bold: bool) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_override("font", ui_font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	if bold:
		label.add_theme_constant_override("outline_size", 1)
		label.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.70))
	return label


func _button(text_value: String, bg: Color, border: Color, font_size: int, high_impact: bool) -> Button:
	var button := Button.new()
	button.text = text_value
	button.custom_minimum_size = Vector2(0.0, 54.0)
	button.alignment = HORIZONTAL_ALIGNMENT_LEFT
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	button.add_theme_font_override("font", ui_font)
	button.add_theme_font_size_override("font_size", font_size)
	button.add_theme_color_override("font_color", Color(0.96, 0.98, 0.96, 1.0))
	button.add_theme_stylebox_override("normal", _style_panel(bg, border, 8.0, high_impact))
	button.add_theme_stylebox_override("hover", _style_panel(bg.lightened(0.08), border.lightened(0.28), 8.0, true))
	button.add_theme_stylebox_override("pressed", _style_panel(bg.darkened(0.08), border, 8.0, high_impact))
	button.add_theme_stylebox_override("focus", _style_panel(Color(0.95, 0.88, 0.66, 0.18), Color(0.96, 0.92, 0.72, 0.9), 8.0, true))
	return button


func _style_panel(bg: Color, border: Color, radius: float, glow: bool = false) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.set_corner_radius_all(int(radius))
	style.set_content_margin(SIDE_LEFT, 14)
	style.set_content_margin(SIDE_TOP, 10)
	style.set_content_margin(SIDE_RIGHT, 14)
	style.set_content_margin(SIDE_BOTTOM, 10)
	if glow:
		style.shadow_color = Color(border.r, border.g, border.b, 0.26)
		style.shadow_size = 18
		style.shadow_offset = Vector2(0.0, 6.0)
	return style
