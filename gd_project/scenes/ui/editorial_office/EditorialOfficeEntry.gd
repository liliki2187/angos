extends Control

const TITLE_SCENE := "res://scenes/ui/title_screen/TitleScreen.tscn"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const ASSET := "res://Assets/ui/angus_packaging/editorial_office/"

var ui_font: SystemFont
var stage: Control
var overlay: Control
var overlay_panel: Panel
var overlay_kicker: Label
var overlay_title: Label
var overlay_body: Control
var overlay_result: Label
var queue_status: Label
var toast: Label
var todo_cards := {}

var event_payloads := {
	"science": {
		"kicker": "势力传真",
		"title": "科学会联络员：标题必须降温",
		"mode": "dialogue",
		"portrait": ASSET + "portrait-science-liaison-v1.png",
		"quote": "标题里不要再写“活的天气”。公众会把比喻当成预报。",
		"detail": "这不是独立剧情线，只是本周开局压力。你的处理方式会写进本周议程，影响天气类选题的公开措辞。",
		"choices": [
			{"label": "接受措辞限制", "result": "已记入议程：天气类标题降低传播，但科学会压力下降。"},
			{"label": "追问限制代价", "result": "已记入议程：新增一条势力压力线索，本周截稿压力不变。"},
			{"label": "先搁置传真", "result": "已记入议程：本周压力上升，仍可照常发刊。"},
		],
	},
	"letter": {
		"kicker": "读者来信",
		"title": "皇后区读者：蓝光回到窗外",
		"mode": "letter",
		"sender": "皇后区读者 / 匿名",
		"quote": "你们上期写的蓝光，我家窗外今晚也有。它不像灯，更像有人把天花板划开了。",
		"linked": "关联：上期头版《东海岸蓝光不是海港灯》",
		"effect": "后果：归档为下周线索；东海岸地区出现“现实回声”标记。",
		"choices": [
			{"label": "归档为线索", "result": "已处理：来信进入黑板候选线索，下周简报可引用。"},
			{"label": "标为公众误读", "result": "已处理：减少噪音，但可能错过一条东海岸钩子。"},
			{"label": "约读者回访", "result": "已处理：生成一个低频来访机会，占用本周一格注意力。"},
		],
	},
	"peddler": {
		"kicker": "来访者",
		"title": "广告小贩：一盒彩色旧相机",
		"mode": "dialogue",
		"portrait": ASSET + "portrait-ad-peddler-v1.png",
		"quote": "三台相机，一台拍现在，一台拍昨天，一台专拍没付广告费的真相。",
		"detail": "来访和小贩不是办公室经营系统，只是开局事件皮肤。处理结果只影响本周资源、广告压力或一个素材钩子。",
		"choices": [
			{"label": "买下旧相机", "result": "已处理：获得一格异常照片素材，小贩广告条件进入待审。"},
			{"label": "只收名片", "result": "已处理：来访跨周保留，但下周报价上涨。"},
			{"label": "拒绝夹带广告", "result": "已处理：版面保持干净，本周少一个便宜素材来源。"},
		],
	},
	"broadcast": {
		"kicker": "世界回响",
		"title": "深夜城市频道：普通蓝光特别报道",
		"mode": "broadcast",
		"image": ASSET + "tv-broadcast-crt-component-v1.png",
		"quote": "地方台连续三次把红月切成广告，主持人仍坚持：东海岸蓝光只是摄像机故障。",
		"detail": "电视只给一条强回响，不做频道系统。它把上期刊发造成的现实变化变成一张可截图的插页。",
		"choices": [
			{"label": "记录为世界回响", "result": "已记录：本周简报可显示一条广播摘录。"},
			{"label": "剪下字幕条", "result": "已记录：获得一个传播素材钩子。"},
			{"label": "关掉电视", "result": "已关闭：不改变本周待办。"},
		],
	},
}

func _ready() -> void:
	_setup_font()
	_build_scene()


func _setup_font() -> void:
	ui_font = SystemFont.new()
	ui_font.font_names = PackedStringArray([
		"Microsoft YaHei",
		"Noto Sans CJK SC",
		"SimHei",
		"Arial Unicode MS",
	])


func _build_scene() -> void:
	_add_background()
	stage = Control.new()
	stage.size = Vector2(1500.0, 1032.0)
	stage.position = Vector2((1920.0 - stage.size.x) * 0.5, 24.0)
	add_child(stage)

	_add_room(stage)
	_add_command_panel(stage)
	_add_screen_texture()
	_add_overlay()


func _add_background() -> void:
	var bg := ColorRect.new()
	bg.color = Color(0.018, 0.032, 0.038, 1.0)
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var wash := ColorRect.new()
	wash.color = Color(0.04, 0.10, 0.12, 0.28)
	wash.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(wash)

	_add_glow(self, Vector2(210.0, 160.0), Vector2(620.0, 420.0), Color(0.07, 0.44, 0.48, 0.16), 1.8)
	_add_glow(self, Vector2(1340.0, 150.0), Vector2(540.0, 760.0), Color(0.65, 0.06, 0.05, 0.10), 1.4)


func _add_room(parent: Control) -> void:
	var room := Panel.new()
	room.position = Vector2.ZERO
	room.size = Vector2(1094.0, 1032.0)
	room.clip_contents = true
	room.add_theme_stylebox_override("panel", _style_panel(Color(0.035, 0.065, 0.075, 0.96), Color(0.92, 0.86, 0.68, 0.16), 8.0))
	parent.add_child(room)

	var wall := ColorRect.new()
	wall.position = Vector2.ZERO
	wall.size = Vector2(1094.0, 660.0)
	wall.color = Color(0.045, 0.085, 0.095, 0.72)
	room.add_child(wall)

	var floor := ColorRect.new()
	floor.position = Vector2(0.0, 650.0)
	floor.size = Vector2(1094.0, 382.0)
	floor.color = Color(0.018, 0.035, 0.04, 0.92)
	room.add_child(floor)

	_add_room_glows(room)
	_add_masthead(room)
	_add_blackboard(room)
	_add_broadcast_tv(room)
	_add_window(room)
	_add_desk(room)


func _add_masthead(parent: Control) -> void:
	var lockup := Control.new()
	lockup.position = Vector2(30.0, 34.0)
	lockup.size = Vector2(430.0, 124.0)
	lockup.rotation_degrees = -1.7
	parent.add_child(lockup)

	var red_shadow := Panel.new()
	red_shadow.position = Vector2(8.0, 14.0)
	red_shadow.size = Vector2(410.0, 102.0)
	red_shadow.add_theme_stylebox_override("panel", _style_panel(Color(0.58, 0.07, 0.05, 0.56), Color(0.0, 0.0, 0.0, 0.0), 0.0))
	lockup.add_child(red_shadow)

	var cyan_shadow := Panel.new()
	cyan_shadow.position = Vector2(18.0, 5.0)
	cyan_shadow.size = Vector2(410.0, 102.0)
	cyan_shadow.add_theme_stylebox_override("panel", _style_panel(Color(0.03, 0.30, 0.34, 0.36), Color(0.0, 0.0, 0.0, 0.0), 0.0))
	lockup.add_child(cyan_shadow)

	var sign := Panel.new()
	sign.position = Vector2.ZERO
	sign.size = Vector2(410.0, 102.0)
	sign.add_theme_stylebox_override("panel", _style_panel(Color(0.045, 0.06, 0.055, 0.94), Color(0.92, 0.86, 0.68, 0.68), 0.0))
	lockup.add_child(sign)

	var red_bar := ColorRect.new()
	red_bar.position = Vector2(0.0, 0.0)
	red_bar.size = Vector2(16.0, 102.0)
	red_bar.color = Color(0.93, 0.22, 0.18, 0.96)
	red_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	sign.add_child(red_bar)

	var title_group := Control.new()
	title_group.position = Vector2(32.0, 18.0)
	title_group.size = Vector2(360.0, 54.0)
	sign.add_child(title_group)
	_add_print_label(title_group, "世界未解之谜周刊", Vector2.ZERO, 28)

	var underline := ColorRect.new()
	underline.position = Vector2(60.0, 42.0)
	underline.size = Vector2(62.0, 3.0)
	underline.color = Color(0.93, 0.22, 0.18, 0.96)
	underline.mouse_filter = Control.MOUSE_FILTER_IGNORE
	title_group.add_child(underline)

	sign.add_child(_placed_label("主编室 · WORLD MYSTERIES WEEKLY", Vector2(34.0, 70.0), Vector2(360.0, 18.0), 11, Color(0.84, 0.82, 0.68, 0.82), true))


func _add_blackboard(parent: Control) -> void:
	var board := Control.new()
	board.position = Vector2(34.0, 156.0)
	board.size = Vector2(414.0, 244.0)
	parent.add_child(board)

	_add_texture(board, ASSET + "agenda-blackboard-clean-v2.png", Vector2.ZERO, board.size, TextureRect.STRETCH_SCALE)
	_add_thread(board, Vector2(132.0, 112.0), 106.0, 12.0)
	_add_thread(board, Vector2(222.0, 126.0), 86.0, 48.0)
	_add_thread(board, Vector2(256.0, 164.0), 58.0, -6.0)

	_add_sticker(board, "board-sticker-cream-note-1.png", Vector2(56.0, 54.0), Vector2(112.0, 82.0), -5.0, "已刊发\n东海岸蓝光", Color(0.06, 0.04, 0.02, 1.0), 11)
	_add_sticker(board, "board-sticker-cream-note-2.png", Vector2(202.0, 54.0), Vector2(118.0, 78.0), 4.0, "旧线缺口\nM330 空白段", Color(0.06, 0.04, 0.02, 1.0), 11)
	_add_sticker(board, "board-sticker-cyan-card.png", Vector2(128.0, 126.0), Vector2(138.0, 74.0), -1.0, "当前课题\n第二个月亮还没找到源头", Color(0.03, 0.055, 0.06, 1.0), 10)
	_add_sticker(board, "board-sticker-red-strip.png", Vector2(270.0, 150.0), Vector2(128.0, 44.0), 3.0, "下一站：天文台", Color(1.0, 0.95, 0.76, 1.0), 11)


func _add_broadcast_tv(parent: Control) -> void:
	var tv := Button.new()
	tv.position = Vector2(714.0, 38.0)
	tv.size = Vector2(348.0, 224.0)
	tv.text = ""
	tv.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	tv.add_theme_stylebox_override("normal", _style_panel(Color(0.0, 0.0, 0.0, 0.0), Color(0.12, 0.74, 0.84, 0.32), 4.0))
	tv.add_theme_stylebox_override("hover", _style_panel(Color(0.12, 0.74, 0.84, 0.08), Color(0.95, 0.92, 0.72, 0.82), 4.0))
	tv.add_theme_stylebox_override("pressed", _style_panel(Color(0.0, 0.0, 0.0, 0.1), Color(0.12, 0.74, 0.84, 0.58), 4.0))
	tv.pressed.connect(_open_event.bind("broadcast"))
	parent.add_child(tv)

	_add_texture(tv, ASSET + "tv-broadcast-crt-component-v1.png", Vector2(-18.0, -8.0), Vector2(382.0, 244.0), TextureRect.STRETCH_KEEP_ASPECT)
	var caption := PanelContainer.new()
	caption.position = Vector2(28.0, 140.0)
	caption.size = Vector2(246.0, 60.0)
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	caption.add_theme_stylebox_override("panel", _style_panel(Color(0.01, 0.015, 0.018, 0.86), Color(0.12, 0.74, 0.84, 0.7), 0.0))
	tv.add_child(caption)
	var margin := _margin(10, 7, 10, 7)
	caption.add_child(margin)
	var label := _label("深夜城市频道\n东海岸热线暴增；主播坚持称那只是“普通蓝光”。", 11, Color(0.96, 0.92, 0.78, 0.94), true)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	margin.add_child(label)


func _add_window(parent: Control) -> void:
	var frame := Panel.new()
	frame.position = Vector2(696.0, 304.0)
	frame.size = Vector2(342.0, 224.0)
	frame.clip_contents = true
	frame.add_theme_stylebox_override("panel", _style_panel(Color(0.04, 0.04, 0.035, 0.9), Color(0.92, 0.86, 0.68, 0.18), 4.0))
	parent.add_child(frame)
	_add_texture(frame, ASSET + "window-city-rain-ambient-v1.png", Vector2(12.0, 12.0), Vector2(318.0, 184.0), TextureRect.STRETCH_KEEP_ASPECT_COVERED)

	var note := PanelContainer.new()
	note.position = frame.position + Vector2(32.0, 176.0)
	note.size = Vector2(204.0, 44.0)
	note.add_theme_stylebox_override("panel", _style_panel(Color(0.82, 0.74, 0.52, 0.96), Color(0.08, 0.06, 0.03, 0.45), 0.0))
	parent.add_child(note)
	var margin := _margin(9, 6, 9, 6)
	note.add_child(margin)
	var label := _label("窗外：雨夜。蓝光很远，暂时只像天气。", 10, Color(0.06, 0.04, 0.02, 1.0), true)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	margin.add_child(label)


func _add_desk(parent: Control) -> void:
	var desk := _add_texture(parent, ASSET + "editor-desk-press-compact.png", Vector2(118.0, 560.0), Vector2(888.0, 420.0), TextureRect.STRETCH_KEEP_ASPECT)
	desk.mouse_filter = Control.MOUSE_FILTER_IGNORE


func _add_room_glows(parent: Control) -> void:
	_add_glow(parent, Vector2(610.0, 18.0), Vector2(478.0, 284.0), Color(0.08, 0.58, 0.66, 0.24), 2.1)
	_add_glow(parent, Vector2(632.0, 282.0), Vector2(460.0, 310.0), Color(0.08, 0.40, 0.58, 0.18), 1.8)
	_add_glow(parent, Vector2(150.0, 474.0), Vector2(840.0, 430.0), Color(0.95, 0.55, 0.24, 0.20), 1.6)
	_add_glow(parent, Vector2(28.0, 142.0), Vector2(450.0, 300.0), Color(0.90, 0.10, 0.07, 0.13), 2.4)


func _add_screen_texture() -> void:
	var overlay_rect := ColorRect.new()
	overlay_rect.color = Color.WHITE
	overlay_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay_rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	var shader := Shader.new()
	shader.code = """
shader_type canvas_item;

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void fragment() {
	vec2 p = SCREEN_UV;
	float scanline = step(0.58, fract(p.y * 270.0)) * 0.07;
	float grain = (hash(floor(p * vec2(360.0, 210.0))) - 0.5) * 0.045;
	float edge = smoothstep(0.52, 0.88, distance(p, vec2(0.50, 0.50)));
	float grid_x = step(0.993, fract(p.x * 22.0));
	float grid_y = step(0.992, fract(p.y * 12.0));
	float grid = clamp(grid_x + grid_y, 0.0, 1.0) * 0.045;
	vec3 color = vec3(0.0, 0.0, 0.0) * (0.06 + edge * 0.22 + scanline);
	color += vec3(0.05, 0.46, 0.52) * grid;
	color += vec3(grain);
	COLOR = vec4(color, clamp(0.10 + edge * 0.16 + scanline, 0.0, 0.38));
}
"""
	var material := ShaderMaterial.new()
	material.shader = shader
	overlay_rect.material = material
	add_child(overlay_rect)


func _add_glow(parent: Control, pos: Vector2, size_value: Vector2, color: Color, falloff: float) -> void:
	var glow := ColorRect.new()
	glow.position = pos
	glow.size = size_value
	glow.color = Color.WHITE
	glow.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var shader := Shader.new()
	shader.code = """
shader_type canvas_item;

uniform vec4 tint : source_color = vec4(1.0, 0.6, 0.2, 0.2);
uniform float falloff = 1.8;

void fragment() {
	vec2 p = UV - vec2(0.5);
	float d = length(p * vec2(1.05, 0.82));
	float halo = pow(max(0.0, 1.0 - smoothstep(0.0, 0.72, d)), falloff);
	COLOR = vec4(tint.rgb, tint.a * halo);
}
"""
	var material := ShaderMaterial.new()
	material.shader = shader
	material.set_shader_parameter("tint", color)
	material.set_shader_parameter("falloff", falloff)
	glow.material = material
	parent.add_child(glow)


func _add_command_panel(parent: Control) -> void:
	var side := Panel.new()
	side.position = Vector2(1118.0, 0.0)
	side.size = Vector2(382.0, 1032.0)
	side.add_theme_stylebox_override("panel", _style_panel(Color(0.025, 0.035, 0.04, 0.92), Color(0.92, 0.86, 0.68, 0.18), 8.0))
	parent.add_child(side)

	side.add_child(_placed_label("WEEKLY DESK QUEUE", Vector2(22.0, 38.0), Vector2(338.0, 20.0), 12, Color(0.86, 0.84, 0.74, 0.8), true))
	var title := _placed_label("先处理待办，再开本周编辑会。", Vector2(22.0, 72.0), Vector2(342.0, 92.0), 30, Color(1.0, 0.95, 0.76, 1.0), true)
	title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	side.add_child(title)
	var desc := _placed_label("来信、传真和来访会改变本周议程。部分事项今天必须拆，部分可以跨周留下。", Vector2(22.0, 172.0), Vector2(338.0, 58.0), 14, Color(0.9, 0.88, 0.78, 0.76), false)
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	side.add_child(desc)

	_add_metric_strip(side, Vector2(22.0, 240.0))
	_make_todo_card(side, "science", Vector2(22.0, 334.0), Color(0.93, 0.22, 0.18, 1.0), "势力传真", "今日必须", "科学会要求改掉“活的天气”。", "接受限制、追问代价或先搁置；会影响本周天气类报道压力。", "不处理：本周压力上升")
	_make_todo_card(side, "letter", Vector2(22.0, 482.0), Color(0.12, 0.76, 0.84, 1.0), "读者来信", "本周消失", "蓝光目击来信堆到桌边。", "读者称上期蓝光解释正在窗外重演；处理后写入下周钩子。", "处理后：归档为线索")
	_make_todo_card(side, "peddler", Vector2(22.0, 630.0), Color(0.42, 0.76, 0.52, 1.0), "来访者", "可搁置", "广告小贩带来一盒彩色旧相机。", "可能换取版面资源，也可能夹带下期广告条件。", "跨周保留：价格会上涨")

	var footer := PanelContainer.new()
	footer.position = Vector2(22.0, 776.0)
	footer.size = Vector2(338.0, 92.0)
	footer.add_theme_stylebox_override("panel", _style_panel(Color(0.18, 0.06, 0.045, 0.35), Color(0.94, 0.72, 0.28, 0.28), 6.0))
	side.add_child(footer)
	var footer_margin := _margin(14, 12, 12, 12)
	footer.add_child(footer_margin)
	var footer_box := VBoxContainer.new()
	footer_box.add_theme_constant_override("separation", 6)
	footer_margin.add_child(footer_box)
	footer_box.add_child(_label("待办范围", 12, Color(0.96, 0.72, 0.24, 1.0), true))
	queue_status = _label("", 13, Color(0.92, 0.9, 0.78, 0.82), false)
	queue_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	footer_box.add_child(queue_status)

	var enter_btn := _button("进入本周编辑会  →", Vector2(22.0, 886.0), Vector2(338.0, 54.0), Color(0.05, 0.55, 0.67, 0.96), Color(0.12, 0.76, 0.84, 0.82), 17)
	enter_btn.pressed.connect(_enter_weekly_meeting)
	side.add_child(enter_btn)

	var back_btn := _button("回到开屏  ↩", Vector2(22.0, 950.0), Vector2(338.0, 44.0), Color(0.08, 0.10, 0.105, 0.7), Color(0.92, 0.86, 0.68, 0.18), 13)
	back_btn.pressed.connect(_goto_scene.bind(TITLE_SCENE))
	side.add_child(back_btn)

	toast = _placed_label("", Vector2(22.0, 1002.0), Vector2(338.0, 22.0), 11, Color(0.14, 0.82, 0.9, 0.9), true)
	side.add_child(toast)
	_update_queue_status()


func _add_metric_strip(parent: Control, pos: Vector2) -> void:
	var labels := [
		["截稿", "6 天"],
		["头版目标", "1 篇"],
		["压力", "科学会"],
	]
	for i in range(labels.size()):
		var panel := PanelContainer.new()
		panel.position = pos + Vector2(i * 112.0, 0.0)
		panel.size = Vector2(112.0, 74.0)
		panel.add_theme_stylebox_override("panel", _style_panel(Color(0.22, 0.21, 0.18, 0.72), Color(0.92, 0.86, 0.68, 0.12), 0.0))
		parent.add_child(panel)
		var margin := _margin(12, 10, 8, 8)
		panel.add_child(margin)
		var box := VBoxContainer.new()
		box.add_theme_constant_override("separation", 5)
		margin.add_child(box)
		box.add_child(_label(labels[i][0], 11, Color(0.86, 0.84, 0.74, 0.52), true))
		box.add_child(_label(labels[i][1], 18, Color(1.0, 0.95, 0.76, 1.0), true))


func _make_todo_card(parent: Control, key: String, pos: Vector2, accent: Color, kind: String, status: String, title: String, body: String, fate: String) -> void:
	var card := Button.new()
	card.position = pos
	card.size = Vector2(338.0, 116.0)
	card.text = ""
	card.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	card.add_theme_stylebox_override("normal", _style_panel(Color(0.08, 0.085, 0.085, 0.58), Color(accent.r, accent.g, accent.b, 0.56), 6.0))
	card.add_theme_stylebox_override("hover", _style_panel(Color(0.11, 0.12, 0.12, 0.72), Color(1.0, 0.95, 0.76, 0.82), 6.0))
	card.add_theme_stylebox_override("pressed", _style_panel(Color(0.06, 0.07, 0.07, 0.8), Color(accent.r, accent.g, accent.b, 0.72), 6.0))
	card.pressed.connect(_open_event.bind(key))
	parent.add_child(card)
	todo_cards[key] = card

	var meta := _placed_label("%s                                      %s" % [kind, status], Vector2(14.0, 12.0), Vector2(310.0, 18.0), 10, Color(0.88, 0.84, 0.74, 0.44), true)
	meta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	card.add_child(meta)
	var title_label := _placed_label(title, Vector2(14.0, 36.0), Vector2(310.0, 25.0), 17, Color(1.0, 0.95, 0.76, 1.0), true)
	title_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	card.add_child(title_label)
	var body_label := _placed_label(body, Vector2(14.0, 63.0), Vector2(310.0, 34.0), 12, Color(0.9, 0.88, 0.78, 0.68), false)
	body_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	card.add_child(body_label)
	var fate_label := _placed_label(fate, Vector2(14.0, 96.0), Vector2(210.0, 18.0), 10, Color(0.9, 0.88, 0.78, 0.74), true)
	fate_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	card.add_child(fate_label)


func _add_overlay() -> void:
	overlay = Control.new()
	overlay.visible = false
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)

	var scrim := ColorRect.new()
	scrim.color = Color(0.0, 0.0, 0.0, 0.78)
	scrim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(scrim)

	overlay_panel = Panel.new()
	overlay_panel.size = Vector2(980.0, 540.0)
	overlay_panel.position = Vector2((1920.0 - 980.0) * 0.5, (1080.0 - 540.0) * 0.5)
	overlay_panel.add_theme_stylebox_override("panel", _style_panel(Color(0.04, 0.055, 0.058, 0.96), Color(0.92, 0.86, 0.68, 0.22), 8.0))
	overlay.add_child(overlay_panel)

	overlay_kicker = _placed_label("", Vector2(24.0, 22.0), Vector2(720.0, 18.0), 12, Color(0.12, 0.78, 0.84, 1.0), true)
	overlay_panel.add_child(overlay_kicker)
	overlay_title = _placed_label("", Vector2(24.0, 48.0), Vector2(790.0, 42.0), 28, Color(1.0, 0.95, 0.76, 1.0), true)
	overlay_panel.add_child(overlay_title)
	var close_btn := _button("×", Vector2(918.0, 20.0), Vector2(42.0, 42.0), Color(0.16, 0.16, 0.15, 0.75), Color(0.92, 0.86, 0.68, 0.58), 22)
	close_btn.pressed.connect(_close_overlay)
	overlay_panel.add_child(close_btn)

	var line := ColorRect.new()
	line.position = Vector2(0.0, 94.0)
	line.size = Vector2(980.0, 1.0)
	line.color = Color(0.92, 0.86, 0.68, 0.14)
	overlay_panel.add_child(line)

	overlay_body = Control.new()
	overlay_body.position = Vector2(24.0, 116.0)
	overlay_body.size = Vector2(928.0, 404.0)
	overlay_panel.add_child(overlay_body)


func _open_event(key: String) -> void:
	var payload: Dictionary = event_payloads.get(key, {})
	if payload.is_empty():
		return
	_clear_children(overlay_body)
	overlay_kicker.text = str(payload.get("kicker", ""))
	overlay_title.text = str(payload.get("title", ""))
	var mode := str(payload.get("mode", "dialogue"))
	if mode == "letter":
		_build_letter_overlay(payload, key)
	elif mode == "broadcast":
		_build_broadcast_overlay(payload, key)
	else:
		_build_dialogue_overlay(payload, key)
	overlay.visible = true


func _build_dialogue_overlay(payload: Dictionary, key: String) -> void:
	var portrait_panel := Panel.new()
	portrait_panel.position = Vector2(0.0, 0.0)
	portrait_panel.size = Vector2(300.0, 390.0)
	portrait_panel.clip_contents = true
	portrait_panel.add_theme_stylebox_override("panel", _style_panel(Color(0.02, 0.03, 0.032, 0.78), Color(0.92, 0.86, 0.68, 0.14), 8.0))
	overlay_body.add_child(portrait_panel)
	_add_texture(portrait_panel, str(payload.get("portrait", "")), Vector2(-32.0, 8.0), Vector2(360.0, 384.0), TextureRect.STRETCH_KEEP_ASPECT)

	var card := PanelContainer.new()
	card.position = Vector2(326.0, 128.0)
	card.size = Vector2(602.0, 230.0)
	card.add_theme_stylebox_override("panel", _style_panel(Color(0.12, 0.13, 0.12, 0.72), Color(0.93, 0.22, 0.18, 0.95), 8.0))
	overlay_body.add_child(card)
	var margin := _margin(22, 18, 22, 16)
	card.add_child(margin)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 13)
	margin.add_child(box)
	var quote := _label("“%s”" % str(payload.get("quote", "")), 22, Color(1.0, 0.95, 0.76, 1.0), true)
	quote.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(quote)
	var detail := _label(str(payload.get("detail", "")), 13, Color(0.9, 0.88, 0.78, 0.72), false)
	detail.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(detail)
	_add_choice_row(box, payload, key)


func _build_letter_overlay(payload: Dictionary, key: String) -> void:
	var paper := Control.new()
	paper.position = Vector2(12.0, 0.0)
	paper.size = Vector2(390.0, 404.0)
	overlay_body.add_child(paper)
	_add_texture(paper, ASSET + "reader-letter-sheet-v1.png", Vector2(0.0, -8.0), Vector2(390.0, 420.0), TextureRect.STRETCH_SCALE)
	paper.add_child(_placed_label(str(payload.get("sender", "")), Vector2(55.0, 74.0), Vector2(260.0, 22.0), 12, Color(0.08, 0.055, 0.03, 1.0), true))
	var quote := _placed_label("“%s”" % str(payload.get("quote", "")), Vector2(55.0, 116.0), Vector2(276.0, 144.0), 23, Color(0.08, 0.055, 0.03, 1.0), true)
	quote.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	paper.add_child(quote)
	var link := _placed_label("%s\n%s" % [payload.get("linked", ""), payload.get("effect", "")], Vector2(55.0, 284.0), Vector2(278.0, 60.0), 11, Color(0.08, 0.055, 0.03, 1.0), true)
	link.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	paper.add_child(link)

	var detail_panel := PanelContainer.new()
	detail_panel.position = Vector2(438.0, 42.0)
	detail_panel.size = Vector2(490.0, 310.0)
	detail_panel.add_theme_stylebox_override("panel", _style_panel(Color(0.08, 0.09, 0.09, 0.5), Color(0.12, 0.76, 0.84, 0.32), 6.0))
	overlay_body.add_child(detail_panel)
	var margin := _margin(18, 16, 18, 16)
	detail_panel.add_child(margin)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 12)
	margin.add_child(box)
	var intro := _label("来信是发刊回响的薄层反馈牌，不是独立收件箱。它只把读者误读、现实回声和下一周钩子接回本周议程。", 14, Color(0.9, 0.88, 0.78, 0.74), false)
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(intro)
	box.add_child(_fact_strip(str(payload.get("linked", "")), Color(0.12, 0.76, 0.84, 1.0)))
	box.add_child(_fact_strip(str(payload.get("effect", "")), Color(0.94, 0.72, 0.28, 1.0)))
	box.add_child(_fact_strip("期限：本周不拆会消失。", Color(0.93, 0.22, 0.18, 1.0)))
	_add_choice_row(box, payload, key)


func _build_broadcast_overlay(payload: Dictionary, key: String) -> void:
	var screen := Panel.new()
	screen.position = Vector2(0.0, 14.0)
	screen.size = Vector2(520.0, 360.0)
	screen.clip_contents = true
	screen.add_theme_stylebox_override("panel", _style_panel(Color(0.02, 0.025, 0.026, 0.9), Color(0.92, 0.86, 0.68, 0.18), 8.0))
	overlay_body.add_child(screen)
	_add_texture(screen, str(payload.get("image", "")), Vector2(-6.0, -8.0), Vector2(532.0, 376.0), TextureRect.STRETCH_KEEP_ASPECT_COVERED)
	var lower := PanelContainer.new()
	lower.position = Vector2(24.0, 278.0)
	lower.size = Vector2(472.0, 66.0)
	lower.add_theme_stylebox_override("panel", _style_panel(Color(0.01, 0.015, 0.018, 0.86), Color(0.93, 0.22, 0.18, 0.95), 0.0))
	screen.add_child(lower)
	var lower_margin := _margin(14, 9, 14, 9)
	lower.add_child(lower_margin)
	var quote := _label(str(payload.get("quote", "")), 17, Color(1.0, 0.95, 0.76, 1.0), true)
	quote.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	lower_margin.add_child(quote)

	var detail_panel := PanelContainer.new()
	detail_panel.position = Vector2(560.0, 78.0)
	detail_panel.size = Vector2(368.0, 286.0)
	detail_panel.add_theme_stylebox_override("panel", _style_panel(Color(0.08, 0.09, 0.09, 0.48), Color(0.12, 0.76, 0.84, 0.28), 6.0))
	overlay_body.add_child(detail_panel)
	var margin := _margin(16, 14, 16, 14)
	detail_panel.add_child(margin)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 12)
	margin.add_child(box)
	var detail := _label(str(payload.get("detail", "")), 14, Color(0.9, 0.88, 0.78, 0.72), false)
	detail.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(detail)
	box.add_child(_fact_strip("频道：深夜城市频道", Color(0.12, 0.76, 0.84, 1.0)))
	box.add_child(_fact_strip("关联：上期蓝光头版", Color(0.94, 0.72, 0.28, 1.0)))
	box.add_child(_fact_strip("结果：可进入本周简报，不新增电视系统。", Color(0.93, 0.22, 0.18, 1.0)))
	_add_choice_row(box, payload, key)


func _add_choice_row(parent: VBoxContainer, payload: Dictionary, key: String) -> void:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 10)
	parent.add_child(row)
	for choice in payload.get("choices", []):
		var button := _button(str(choice.get("label", "")), Vector2.ZERO, Vector2(0.0, 44.0), Color(0.04, 0.22, 0.25, 0.8), Color(0.12, 0.76, 0.84, 0.58), 13)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.pressed.connect(_on_choice.bind(key, str(choice.get("result", ""))))
		row.add_child(button)
	overlay_result = _label("", 12, Color(0.12, 0.78, 0.84, 0.95), true)
	overlay_result.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	parent.add_child(overlay_result)


func _on_choice(key: String, result: String) -> void:
	overlay_result.text = result
	toast.text = result
	if key != "broadcast":
		_mark_done(key)


func _mark_done(key: String) -> void:
	var card: Button = todo_cards.get(key)
	if card == null or card.has_meta("done"):
		return
	card.set_meta("done", true)
	card.modulate = Color(0.82, 1.0, 0.84, 0.78)
	card.add_child(_placed_label("已处理", Vector2(270.0, 12.0), Vector2(58.0, 18.0), 10, Color(0.5, 0.92, 0.58, 1.0), true))
	_update_queue_status()


func _update_queue_status() -> void:
	var remaining := 0
	var must := 0
	for key in todo_cards.keys():
		var card: Button = todo_cards[key]
		if not card.has_meta("done"):
			remaining += 1
			if key == "science":
				must += 1
	if queue_status != null:
		queue_status.text = "还有 %d 件未处理，其中 %d 件今日必须。进入编辑会前会再次确认。" % [remaining, must]


func _enter_weekly_meeting() -> void:
	var science: Button = todo_cards.get("science")
	if science != null and not science.has_meta("done"):
		toast.text = "还有今日必须事项未处理：科学会传真会在进入编辑会前再次弹出。"
		_open_event("science")
		return
	_goto_scene(WEEKLY_RUN_SCENE)


func _goto_scene(path: String) -> void:
	var error := get_tree().change_scene_to_file(path)
	if error != OK:
		toast.text = "场景未能打开：%s" % path
		push_error("[EditorialOfficeEntry] change_scene failed: %s" % path)


func _close_overlay() -> void:
	overlay.visible = false


func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") and overlay != null and overlay.visible:
		_close_overlay()


func _add_thread(parent: Control, pos: Vector2, width: float, rotation_degrees_value: float) -> void:
	var line := ColorRect.new()
	line.position = pos
	line.size = Vector2(width, 2.0)
	line.color = Color(0.93, 0.22, 0.18, 0.75)
	line.rotation_degrees = rotation_degrees_value
	line.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(line)


func _add_sticker(parent: Control, image_name: String, pos: Vector2, size_value: Vector2, rotation_degrees_value: float, text_value: String, color: Color, font_size: int) -> void:
	var sticker := Control.new()
	sticker.position = pos
	sticker.size = size_value
	sticker.rotation_degrees = rotation_degrees_value
	sticker.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(sticker)
	_add_texture(sticker, ASSET + image_name, Vector2.ZERO, size_value, TextureRect.STRETCH_SCALE)
	var label := _placed_label(text_value, Vector2(13.0, 18.0), size_value - Vector2(24.0, 22.0), font_size, color, true)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	sticker.add_child(label)


func _add_texture(parent: Control, path: String, pos: Vector2, size_value: Vector2, stretch) -> TextureRect:
	var texture := TextureRect.new()
	var loaded_texture: Texture2D = load(path)
	texture.texture = loaded_texture
	texture.position = pos
	texture.size = size_value
	texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	texture.stretch_mode = stretch
	texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if loaded_texture != null:
		var source_size := loaded_texture.get_size()
		if source_size.x > 0.0 and source_size.y > 0.0:
			var scale_value := Vector2(size_value.x / source_size.x, size_value.y / source_size.y)
			if stretch == TextureRect.STRETCH_KEEP_ASPECT or stretch == TextureRect.STRETCH_KEEP_ASPECT_COVERED or stretch == TextureRect.STRETCH_KEEP_ASPECT_CENTERED:
				var uniform_scale: float
				if stretch == TextureRect.STRETCH_KEEP_ASPECT_COVERED:
					uniform_scale = max(scale_value.x, scale_value.y)
				else:
					uniform_scale = min(scale_value.x, scale_value.y)
				scale_value = Vector2.ONE * uniform_scale
			texture.size = source_size
			texture.scale = scale_value
	parent.add_child(texture)
	return texture


func _fact_strip(text_value: String, accent: Color) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(0.0, 36.0)
	panel.add_theme_stylebox_override("panel", _style_panel(Color(0.9, 0.86, 0.68, 0.06), accent, 0.0))
	var margin := _margin(12, 8, 10, 8)
	panel.add_child(margin)
	var label := _label(text_value, 12, Color(0.9, 0.88, 0.78, 0.78), true)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	margin.add_child(label)
	return panel


func _add_print_label(parent: Control, text_value: String, pos: Vector2, font_size: int) -> void:
	var shadow := _placed_label(text_value, pos + Vector2(0.0, 4.0), Vector2(390.0, 48.0), font_size, Color(0.0, 0.0, 0.0, 0.70), true)
	parent.add_child(shadow)
	var cyan := _placed_label(text_value, pos + Vector2(2.0, -1.0), Vector2(390.0, 48.0), font_size, Color(0.12, 0.78, 0.86, 0.45), true)
	parent.add_child(cyan)
	var red := _placed_label(text_value, pos + Vector2(-2.0, 2.0), Vector2(390.0, 48.0), font_size, Color(0.93, 0.22, 0.18, 0.52), true)
	parent.add_child(red)
	var main := _placed_label(text_value, pos, Vector2(390.0, 48.0), font_size, Color(1.0, 0.95, 0.76, 1.0), true)
	main.add_theme_constant_override("outline_size", 2)
	main.add_theme_color_override("font_outline_color", Color(0.02, 0.018, 0.012, 0.90))
	parent.add_child(main)


func _placed_label(text_value: String, pos: Vector2, size_value: Vector2, font_size: int, color: Color, bold: bool) -> Label:
	var label := _label(text_value, font_size, color, bold)
	label.position = pos
	label.size = size_value
	label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	return label


func _label(text_value: String, font_size: int, color: Color, bold: bool) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_override("font", ui_font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	if bold:
		label.add_theme_constant_override("outline_size", 1)
		label.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.76))
	return label


func _button(text_value: String, pos: Vector2, size_value: Vector2, bg: Color, border: Color, font_size: int) -> Button:
	var button := Button.new()
	button.position = pos
	button.size = size_value
	button.custom_minimum_size = size_value
	button.text = text_value
	button.alignment = HORIZONTAL_ALIGNMENT_LEFT
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	button.add_theme_font_override("font", ui_font)
	button.add_theme_font_size_override("font_size", font_size)
	button.add_theme_color_override("font_color", Color(0.96, 0.98, 0.96, 1.0))
	button.add_theme_stylebox_override("normal", _style_panel(bg, border, 8.0))
	button.add_theme_stylebox_override("hover", _style_panel(bg.lightened(0.08), border.lightened(0.25), 8.0))
	button.add_theme_stylebox_override("pressed", _style_panel(bg.darkened(0.08), border, 8.0))
	button.add_theme_stylebox_override("focus", _style_panel(Color(0.95, 0.88, 0.66, 0.16), Color(0.96, 0.92, 0.72, 0.88), 8.0))
	return button


func _margin(left: int, top: int, right: int, bottom: int) -> MarginContainer:
	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", left)
	margin.add_theme_constant_override("margin_top", top)
	margin.add_theme_constant_override("margin_right", right)
	margin.add_theme_constant_override("margin_bottom", bottom)
	return margin


func _style_panel(bg: Color, border: Color, radius: float) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.set_corner_radius_all(int(radius))
	style.set_content_margin(SIDE_LEFT, 12)
	style.set_content_margin(SIDE_TOP, 8)
	style.set_content_margin(SIDE_RIGHT, 12)
	style.set_content_margin(SIDE_BOTTOM, 8)
	return style


func _clear_children(parent: Node) -> void:
	for child in parent.get_children():
		parent.remove_child(child)
		child.queue_free()
