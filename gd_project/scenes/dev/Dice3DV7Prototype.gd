extends Control

const VIEW_SIZE := Vector2i(680, 396)
const ROLL_END := 1.18

var _viewport: SubViewport
var _stage_label: Label
var _dice_entries: Array[Dictionary] = []
var _start_ms := 0
var _manual_time := -1.0


func _ready() -> void:
	_start_ms = Time.get_ticks_msec()
	_build_ui()
	_build_scene()
	set_process(true)


func set_demo_time(seconds: float) -> void:
	_manual_time = seconds
	_apply_motion(seconds)


func clear_demo_time() -> void:
	_manual_time = -1.0


func _process(_delta: float) -> void:
	var t := _manual_time
	if t < 0.0:
		t = fmod(float(Time.get_ticks_msec() - _start_ms) / 1000.0, 2.8)
	_apply_motion(t)


func _build_ui() -> void:
	var bg := ColorRect.new()
	bg.color = Color("#130f10")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var title := Label.new()
	title.position = Vector2(96, 54)
	title.size = Vector2(1220, 42)
	title.text = "Dice Motion v7.5 - 3D dice inside a real judgment cell"
	title.add_theme_font_size_override("font_size", 34)
	title.add_theme_color_override("font_color", Color("#f3d38a"))
	add_child(title)

	var subtitle := Label.new()
	subtitle.position = Vector2(98, 106)
	subtitle.size = Vector2(1220, 28)
	subtitle.text = "Goal: validate the dice inside a local Angus judgment modal, not a standalone 3D stage."
	subtitle.add_theme_font_size_override("font_size", 18)
	subtitle.add_theme_color_override("font_color", Color("#c8d2dc"))
	add_child(subtitle)

	var frame := Panel.new()
	frame.position = Vector2(96, 158)
	frame.size = Vector2(1220, 734)
	frame.add_theme_stylebox_override("panel", _panel_style(Color("#171a1f"), Color("#3a414c")))
	add_child(frame)

	var task_card := Panel.new()
	task_card.position = Vector2(24, 22)
	task_card.size = Vector2(336, 260)
	task_card.add_theme_stylebox_override("panel", _panel_style(Color("#d5c8a6"), Color("#7c6640")))
	frame.add_child(task_card)

	_add_label(task_card, Vector2(22, 18), Vector2(292, 28), "M330 Last Bus", 26, Color("#2a241e"))
	_add_label(task_card, Vector2(22, 54), Vector2(292, 28), "Task goal", 18, Color("#72542d"))
	_add_label(task_card, Vector2(22, 84), Vector2(292, 54), "Reach effective points before the final witness account collapses.", 18, Color("#393028"), true)
	_add_metric_chip(task_card, Vector2(22, 154), "Target", "6")
	_add_metric_chip(task_card, Vector2(122, 154), "Current", "6")
	_add_metric_chip(task_card, Vector2(222, 154), "Risk", "+2")
	_add_label(task_card, Vector2(22, 216), Vector2(292, 24), "Relevant faces: Leads / Insight / Nerves", 16, Color("#40352a"))

	var summary_card := Panel.new()
	summary_card.position = Vector2(24, 302)
	summary_card.size = Vector2(336, 270)
	summary_card.add_theme_stylebox_override("panel", _panel_style(Color("#20262a"), Color("#50606a")))
	frame.add_child(summary_card)

	_add_label(summary_card, Vector2(20, 18), Vector2(288, 28), "Judgment contract", 22, Color("#f3d38a"))
	_add_label(summary_card, Vector2(20, 60), Vector2(288, 104), "This preview keeps the real judgment structure visible: task goal, character dice, result summary, and submit action.", 18, Color("#cfd7d2"), true)
	_add_label(summary_card, Vector2(20, 174), Vector2(288, 28), "This round validates:", 18, Color("#f3d38a"))
	_add_label(summary_card, Vector2(20, 208), Vector2(288, 48), "3D dice scale inside a 2D modal\nresult readability after the motion stops", 16, Color("#cfd7d2"), true)

	var tray_frame := Panel.new()
	tray_frame.position = Vector2(384, 22)
	tray_frame.size = Vector2(724, 468)
	tray_frame.add_theme_stylebox_override("panel", _panel_style(Color("#111719"), Color("#9d7f42")))
	frame.add_child(tray_frame)

	_add_label(tray_frame, Vector2(22, 16), Vector2(500, 30), "Roll board", 26, Color("#f3d38a"))
	_add_label(tray_frame, Vector2(22, 50), Vector2(420, 24), "Three participating character dice, bounded to their own slots.", 16, Color("#c8d2dc"))

	var viewport_wrap := SubViewportContainer.new()
	viewport_wrap.position = Vector2(22, 78)
	viewport_wrap.size = Vector2(VIEW_SIZE)
	viewport_wrap.custom_minimum_size = Vector2(VIEW_SIZE)
	viewport_wrap.stretch = true
	tray_frame.add_child(viewport_wrap)

	_viewport = SubViewport.new()
	_viewport.size = VIEW_SIZE
	_viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	_viewport.own_world_3d = true
	viewport_wrap.add_child(_viewport)

	var control_strip := Panel.new()
	control_strip.position = Vector2(384, 512)
	control_strip.size = Vector2(724, 160)
	control_strip.add_theme_stylebox_override("panel", _panel_style(Color("#1c2226"), Color("#42515a")))
	frame.add_child(control_strip)

	_add_label(control_strip, Vector2(22, 18), Vector2(240, 28), "Player control", 22, Color("#f3d38a"))
	_add_label(control_strip, Vector2(462, 18), Vector2(230, 28), "Preview: 6/6 · pass", 20, Color("#b8f0ca"))
	_add_button_plate(control_strip, Vector2(22, 62), Vector2(164, 60), "Lock 2")
	_add_button_plate(control_strip, Vector2(202, 62), Vector2(210, 60), "Reroll 1 die")
	_add_button_plate(control_strip, Vector2(428, 62), Vector2(264, 60), "Submit judgment", true)

	var result_card := Panel.new()
	result_card.position = Vector2(1128, 22)
	result_card.size = Vector2(68, 650)
	result_card.add_theme_stylebox_override("panel", _panel_style(Color("#2a201b"), Color("#8b5f36")))
	frame.add_child(result_card)

	_add_label(result_card, Vector2(12, 18), Vector2(44, 28), "OK", 22, Color("#f3d38a"))
	_add_vertical_result(result_card, Vector2(18, 70), "6/6")
	_add_label(result_card, Vector2(10, 548), Vector2(48, 60), "PASS", 16, Color("#b8f0ca"))

	_stage_label = Label.new()
	_stage_label.position = Vector2(24, 696)
	_stage_label.size = Vector2(1170, 26)
	_stage_label.text = "Artifact type: runtime_cell_preview_v0"
	_stage_label.add_theme_font_size_override("font_size", 18)
	_stage_label.add_theme_color_override("font_color", Color("#f3d38a"))
	frame.add_child(_stage_label)

	var side := PanelContainer.new()
	side.position = Vector2(1360, 158)
	side.size = Vector2(464, 734)
	side.add_theme_stylebox_override("panel", _panel_style(Color("#1b1e24"), Color("#48515e")))
	add_child(side)

	var side_margin := MarginContainer.new()
	side_margin.add_theme_constant_override("margin_left", 24)
	side_margin.add_theme_constant_override("margin_top", 24)
	side_margin.add_theme_constant_override("margin_right", 24)
	side_margin.add_theme_constant_override("margin_bottom", 24)
	side.add_child(side_margin)

	var bullets := RichTextLabel.new()
	bullets.fit_content = true
	bullets.scroll_active = false
	bullets.bbcode_enabled = true
	bullets.add_theme_font_size_override("normal_font_size", 18)
	bullets.text = "[color=#f3d38a][b]Review gate[/b][/color]\n\n" \
		+ "This is a runtime cell preview, not final art.\n\n" \
		+ "Show now:\n" \
		+ "- dice inside judgment layout\n" \
		+ "- task goal near result\n" \
		+ "- submit preview stays readable\n" \
		+ "- motion does not steal the page\n\n" \
		+ "Do not judge yet:\n" \
		+ "- final Angus material\n" \
		+ "- face atlas direction\n" \
		+ "- final modal ornament\n" \
		+ "- full interaction state matrix\n\n" \
		+ "[color=#c8d2dc]Pass condition: at 1920x1080, a player can read task target, rolled result, and submit status without the dice overpowering the UI.[/color]"
	side_margin.add_child(bullets)


func _add_chip(parent: Control, pos: Vector2, text: String) -> void:
	var chip := Panel.new()
	chip.position = pos
	chip.size = Vector2(118, 42)
	chip.add_theme_stylebox_override("panel", _panel_style(Color("#2a2220"), Color("#735b35")))
	parent.add_child(chip)

	var label := Label.new()
	label.position = Vector2(10, 10)
	label.size = Vector2(98, 22)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.text = text
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", Color("#ebd59c"))
	chip.add_child(label)


func _add_label(parent: Control, pos: Vector2, size: Vector2, text: String, font_size: int, color: Color, wrap := false) -> Label:
	var label := Label.new()
	label.position = pos
	label.size = size
	label.text = text
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	if wrap:
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	parent.add_child(label)
	return label


func _add_metric_chip(parent: Control, pos: Vector2, title: String, value: String) -> void:
	var chip := Panel.new()
	chip.position = pos
	chip.size = Vector2(88, 48)
	chip.add_theme_stylebox_override("panel", _panel_style(Color("#efe2b8"), Color("#7c6640")))
	parent.add_child(chip)

	_add_label(chip, Vector2(8, 6), Vector2(72, 16), title, 14, Color("#6b5333"))
	var value_label := _add_label(chip, Vector2(8, 20), Vector2(72, 24), value, 22, Color("#2a241e"))
	value_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER


func _add_button_plate(parent: Control, pos: Vector2, size: Vector2, text: String, primary := false) -> void:
	var plate := Panel.new()
	plate.position = pos
	plate.size = size
	var bg := Color("#2a2f35")
	var border := Color("#59636e")
	if primary:
		bg = Color("#5b3b1d")
		border = Color("#f0b35e")
	plate.add_theme_stylebox_override("panel", _panel_style(bg, border))
	parent.add_child(plate)

	var label := _add_label(plate, Vector2(12, 16), Vector2(size.x - 24, 28), text, 22, Color("#f6e6ad"))
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER


func _add_vertical_result(parent: Control, pos: Vector2, text: String) -> void:
	var label := Label.new()
	label.position = pos
	label.size = Vector2(36, 420)
	var chars: Array[String] = []
	for i in range(text.length()):
		chars.append(text.substr(i, 1))
	label.text = "\n".join(chars)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 24)
	label.add_theme_color_override("font_color", Color("#f6e6ad"))
	parent.add_child(label)


func _panel_style(bg: Color, border: Color) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.corner_radius_top_left = 8
	style.corner_radius_top_right = 8
	style.corner_radius_bottom_left = 8
	style.corner_radius_bottom_right = 8
	return style


func _build_scene() -> void:
	var world := Node3D.new()
	_viewport.add_child(world)

	var environment := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color("#101719")
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("#6b6f64")
	env.ambient_light_energy = 0.82
	environment.environment = env
	world.add_child(environment)

	var camera := Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 4.55
	camera.position = Vector3(0.0, 5.2, 2.35)
	world.add_child(camera)
	camera.look_at(Vector3(0.0, -0.45, -0.08), Vector3.UP)
	camera.current = true

	var key := DirectionalLight3D.new()
	key.position = Vector3(-2.0, 5.2, 2.8)
	key.rotation_degrees = Vector3(-62, -28, 0)
	key.light_energy = 2.3
	key.shadow_enabled = true
	world.add_child(key)

	var fill := OmniLight3D.new()
	fill.position = Vector3(3.4, 2.0, 1.6)
	fill.light_color = Color("#e9bd73")
	fill.light_energy = 0.34
	fill.omni_range = 8.0
	world.add_child(fill)

	var table := MeshInstance3D.new()
	var table_mesh := PlaneMesh.new()
	table_mesh.size = Vector2(7.4, 3.18)
	table.mesh = table_mesh
	table.position = Vector3(0, -0.74, 0)
	table.material_override = _mat(Color("#202827"), 0.94, Color("#000000"))
	world.add_child(table)

	_add_dice_cell(world, {
		"label": "Mara",
		"top": "2",
		"kind": "field",
		"center": Vector3(-2.08, -0.2, 0.05),
		"accent": Color("#f0b35e"),
		"offset": 0.0,
	})
	_add_dice_cell(world, {
		"label": "Dr. Ke",
		"top": "3",
		"kind": "blue",
		"center": Vector3(0.0, -0.2, 0.05),
		"accent": Color("#5ab9d6"),
		"offset": 0.045,
	})
	_add_dice_cell(world, {
		"label": "Ives",
		"top": "1",
		"kind": "black",
		"center": Vector3(2.08, -0.2, 0.05),
		"accent": Color("#d35b69"),
		"offset": 0.09,
	})


func _add_dice_cell(world: Node3D, spec: Dictionary) -> void:
	var center := spec["center"] as Vector3
	var accent := spec["accent"] as Color
	_add_cell_frame(world, center, String(spec["label"]), accent)

	var shadow := _make_shadow(Color(0, 0, 0, 0.42))
	shadow.position = Vector3(center.x, -0.722, center.z)
	shadow.scale = Vector3(0.54, 1.0, 0.32)
	world.add_child(shadow)

	var die := _make_die(String(spec["kind"]), String(spec["top"]))
	die.position = center
	die.scale = Vector3.ONE * 0.62
	world.add_child(die)

	_dice_entries.append({
		"die": die,
		"shadow": shadow,
		"base": center,
		"offset": float(spec["offset"]),
		"max_x": 0.16,
		"max_z": 0.075,
	})


func _add_cell_frame(world: Node3D, center: Vector3, label_text: String, accent: Color) -> void:
	var pad := MeshInstance3D.new()
	var pad_mesh := PlaneMesh.new()
	pad_mesh.size = Vector2(1.62, 1.18)
	pad.mesh = pad_mesh
	pad.position = Vector3(center.x, -0.735, center.z)
	pad.material_override = _mat(Color("#18201f"), 0.9, Color("#000000"))
	world.add_child(pad)

	var rail_mat := _mat(accent.darkened(0.22), 0.86, accent)
	_add_rail(world, Vector3(center.x, -0.705, center.z - 0.64), Vector3(1.76, 0.024, 0.03), rail_mat)
	_add_rail(world, Vector3(center.x, -0.705, center.z + 0.64), Vector3(1.76, 0.024, 0.03), rail_mat)
	_add_rail(world, Vector3(center.x - 0.88, -0.705, center.z), Vector3(0.03, 0.024, 1.28), rail_mat)
	_add_rail(world, Vector3(center.x + 0.88, -0.705, center.z), Vector3(0.03, 0.024, 1.28), rail_mat)

	var name_plate := MeshInstance3D.new()
	var name_mesh := BoxMesh.new()
	name_mesh.size = Vector3(1.22, 0.024, 0.16)
	name_plate.mesh = name_mesh
	name_plate.position = Vector3(center.x, -0.695, center.z + 0.82)
	name_plate.material_override = _mat(Color("#332820"), 0.88, accent.darkened(0.15))
	world.add_child(name_plate)

	var label := Label3D.new()
	label.text = label_text
	label.font_size = 30
	label.modulate = Color("#f6e6ad")
	label.outline_size = 4
	label.outline_modulate = Color(0.02, 0.015, 0.01, 0.86)
	label.shaded = false
	label.position = Vector3(center.x, -0.665, center.z + 0.825)
	label.rotation_degrees = Vector3(-90, 0, 0)
	world.add_child(label)


func _add_rail(world: Node3D, pos: Vector3, size: Vector3, mat: StandardMaterial3D) -> void:
	var rail := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	rail.mesh = mesh
	rail.position = pos
	rail.material_override = mat
	world.add_child(rail)


func _make_die(kind: String, top_text: String) -> Node3D:
	var root := Node3D.new()
	root.name = "ContainedDice3D"

	var body := MeshInstance3D.new()
	body.mesh = _make_soft_cube_mesh(1.0, 0.16, 10)
	body.material_override = _dice_material(kind)
	body.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	root.add_child(body)

	_add_face_label(root, top_text, Vector3(0, 0.516, 0), Vector3.UP, Vector3.FORWARD, 72)
	_add_face_label(root, "+", Vector3(0, 0, 0.516), Vector3.FORWARD, Vector3.UP, 48)
	_add_face_label(root, "-", Vector3(0.516, 0, 0), Vector3.RIGHT, Vector3.UP, 48)
	return root


func _make_soft_cube_mesh(size: float, soften: float, steps: int) -> ArrayMesh:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var half := size * 0.5
	var axes := [
		{"axis": 0, "sign": 1.0},
		{"axis": 0, "sign": -1.0},
		{"axis": 1, "sign": 1.0},
		{"axis": 1, "sign": -1.0},
		{"axis": 2, "sign": 1.0},
		{"axis": 2, "sign": -1.0},
	]
	for face in axes:
		var axis := int(face["axis"])
		var sign := float(face["sign"])
		for y in range(steps):
			for x in range(steps):
				var u0 := -1.0 + 2.0 * float(x) / float(steps)
				var v0 := -1.0 + 2.0 * float(y) / float(steps)
				var u1 := -1.0 + 2.0 * float(x + 1) / float(steps)
				var v1 := -1.0 + 2.0 * float(y + 1) / float(steps)
				var p00 := _soft_cube_point(axis, sign, u0, v0, half, soften)
				var p10 := _soft_cube_point(axis, sign, u1, v0, half, soften)
				var p11 := _soft_cube_point(axis, sign, u1, v1, half, soften)
				var p01 := _soft_cube_point(axis, sign, u0, v1, half, soften)
				_add_quad_outward(st, p00, p10, p11, p01, _face_normal(axis, sign))
	st.generate_normals()
	return st.commit()


func _soft_cube_point(axis: int, sign: float, u: float, v: float, half: float, soften: float) -> Vector3:
	var p: Vector3
	if axis == 0:
		p = Vector3(sign, u, v)
	elif axis == 1:
		p = Vector3(u, sign, v)
	else:
		p = Vector3(u, v, sign)
	var rounded := p.normalized()
	return p.lerp(rounded, soften) * half


func _add_tri(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3) -> void:
	st.add_vertex(a)
	st.add_vertex(b)
	st.add_vertex(c)


func _add_quad_outward(st: SurfaceTool, p00: Vector3, p10: Vector3, p11: Vector3, p01: Vector3, normal: Vector3) -> void:
	var tri_normal := (p10 - p00).cross(p11 - p00)
	if tri_normal.dot(normal) >= 0.0:
		_add_tri(st, p00, p10, p11)
		_add_tri(st, p00, p11, p01)
	else:
		_add_tri(st, p00, p11, p10)
		_add_tri(st, p00, p01, p11)


func _face_normal(axis: int, sign: float) -> Vector3:
	if axis == 0:
		return Vector3(sign, 0.0, 0.0)
	if axis == 1:
		return Vector3(0.0, sign, 0.0)
	return Vector3(0.0, 0.0, sign)


func _add_face_label(root: Node3D, text: String, pos: Vector3, normal: Vector3, up_hint: Vector3, font_size: int) -> void:
	var label := Label3D.new()
	label.text = text
	label.font_size = font_size
	label.modulate = Color("#fff1c5")
	label.outline_size = 10
	label.outline_modulate = Color(0.03, 0.02, 0.01, 0.92)
	label.shaded = true
	label.double_sided = true
	label.no_depth_test = false
	if normal.is_equal_approx(Vector3.UP):
		label.rotation_degrees = Vector3(-90, 0, 0)
	else:
		label.look_at_from_position(pos, pos + normal, up_hint)
	root.add_child(label)


func _dice_material(kind: String) -> StandardMaterial3D:
	if kind == "black":
		return _mat(Color("#8d2531"), 0.82, Color("#d35b69"))
	if kind == "blue":
		return _mat(Color("#276f86"), 0.84, Color("#5ab9d6"))
	return _mat(Color("#b36a24"), 0.84, Color("#f0b35e"))


func _mat(albedo: Color, roughness: float, emission := Color("#000000")) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = albedo
	mat.roughness = roughness
	mat.metallic = 0.0
	mat.emission_enabled = emission.r > 0.0 or emission.g > 0.0 or emission.b > 0.0
	mat.emission = emission
	mat.emission_energy_multiplier = 0.06
	mat.specular_mode = BaseMaterial3D.SPECULAR_SCHLICK_GGX
	return mat


func _make_shadow(color: Color) -> MeshInstance3D:
	var shadow := MeshInstance3D.new()
	var mesh := CylinderMesh.new()
	mesh.top_radius = 0.62
	mesh.bottom_radius = 0.62
	mesh.height = 0.012
	mesh.radial_segments = 48
	shadow.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	shadow.material_override = mat
	return shadow


func _apply_motion(t: float) -> void:
	if _dice_entries.is_empty():
		return
	var tt: float = clampf(t, 0.0, ROLL_END)
	var stage := "motion blockout"

	for entry in _dice_entries:
		var local_t: float = clampf(tt - float(entry["offset"]), 0.0, 1.16)
		stage = _apply_contained_motion(entry, local_t)

	_stage_label.text = "Artifact: runtime_cell_preview_v0 / Stage: %s / %.0fms" % [stage, tt * 1000.0]


func _apply_contained_motion(entry: Dictionary, tt: float) -> String:
	var die := entry["die"] as Node3D
	var shadow := entry["shadow"] as MeshInstance3D
	var base := entry["base"] as Vector3
	var max_x := float(entry["max_x"])
	var max_z := float(entry["max_z"])
	var stage := "prep"
	var pos := base
	var rot := Vector3(0.0, 0.0, 0.0)
	var scale := Vector3.ONE * 0.62
	var shadow_scale := Vector3(0.54, 1.0, 0.32)
	var shadow_alpha := 0.28

	if tt < 0.08:
		var p: float = tt / 0.08
		stage = "pre-compress"
		pos.y = lerpf(base.y + 0.02, base.y - 0.035, p)
		rot.z = lerpf(0.08, -0.08, p)
		scale = Vector3(0.63, 0.60, 0.63).lerp(Vector3(0.65, 0.56, 0.65), p)
		shadow_scale = Vector3(0.58, 1.0, 0.34)
		shadow_alpha = 0.36
	elif tt < 0.42:
		var p: float = (tt - 0.08) / 0.34
		stage = "slot fast tumble"
		var arc := sin(p * PI)
		pos = base + Vector3(max_x * sin(p * PI * 0.86), 0.08 + arc * 0.34, max_z * sin(p * PI * 1.4))
		rot = Vector3(-TAU * 2.35 * p, TAU * 1.65 * p, 0.12 + sin(p * TAU * 1.4) * 0.14)
		shadow_scale = Vector3(0.44 + p * 0.08, 1.0, 0.25 + p * 0.04)
		shadow_alpha = 0.18
	elif tt < 0.55:
		var p: float = (tt - 0.42) / 0.13
		stage = "slot impact"
		var start := base + Vector3(max_x * 0.86, 0.42, max_z * 0.55)
		var end := base + Vector3(max_x * 0.58, -0.02, max_z * 0.28)
		pos = start.lerp(end, _ease_in(p))
		rot = Vector3(-TAU * 2.35 - p * 0.55, TAU * 1.65 + p * 0.3, -0.1)
		scale = Vector3(0.62 + p * 0.03, 0.62 - p * 0.07, 0.62 + p * 0.03)
		shadow_scale = Vector3(0.5 + p * 0.2, 1.0, 0.28 + p * 0.1)
		shadow_alpha = 0.25 + p * 0.32
	elif tt < 0.76:
		var p: float = (tt - 0.55) / 0.21
		stage = "small rebound"
		var rebound := sin(p * PI) * 0.13
		pos = base + Vector3(lerpf(max_x * 0.58, max_x * 0.18, p), 0.03 + rebound, lerpf(max_z * 0.28, 0.0, p))
		rot = Vector3(-1.0 + p * 0.42, 0.12 - p * 0.08, -0.08 + rebound * 0.46)
		scale = Vector3.ONE * 0.62
		shadow_scale = Vector3(0.68 - p * 0.08, 1.0, 0.38 - p * 0.04)
		shadow_alpha = 0.44 - p * 0.12
	elif tt < 0.98:
		var p: float = (tt - 0.76) / 0.22
		stage = "result face correction"
		pos = (base + Vector3(max_x * 0.18, 0.03, 0.0)).lerp(base, _ease_out(p))
		rot = Vector3(-0.58, 0.05, 0.04).lerp(Vector3.ZERO, _ease_out_back(p))
		shadow_scale = Vector3(0.58, 1.0, 0.34)
		shadow_alpha = 0.38
	else:
		var p: float = (tt - 0.98) / 0.18
		stage = "final readable beat"
		pos = base
		rot = Vector3.ZERO
		var pulse: float = sin(clampf(p, 0.0, 1.0) * PI)
		scale = Vector3.ONE * (0.62 + pulse * 0.022)
		shadow_scale = Vector3(0.58 + pulse * 0.08, 1.0, 0.34 + pulse * 0.04)
		shadow_alpha = 0.38 + pulse * 0.1

	die.position = pos
	die.rotation = rot
	die.scale = scale
	shadow.position.x = pos.x
	shadow.position.z = pos.z
	shadow.scale = shadow_scale
	var mat := shadow.material_override as StandardMaterial3D
	if mat:
		mat.albedo_color = Color(0, 0, 0, shadow_alpha)
	return stage


func _ease_out(t: float) -> float:
	return 1.0 - pow(1.0 - clampf(t, 0.0, 1.0), 3.0)


func _ease_in(t: float) -> float:
	return pow(clampf(t, 0.0, 1.0), 3.0)


func _ease_out_back(t: float) -> float:
	var p: float = clampf(t, 0.0, 1.0) - 1.0
	var c := 1.7
	return 1.0 + p * p * ((c + 1.0) * p + c)
