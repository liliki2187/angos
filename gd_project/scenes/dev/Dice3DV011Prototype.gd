extends "res://scenes/dev/Dice3DV7Prototype.gd"


const V011_ROOT := "res://Assets/dice_textures/v0_11"
const V011_RUNTIME_SCALE_MULTIPLIER := 1.18
const V011_FACE_CAP_SIZE := 1.055
const V011_FACE_CAP_OFFSET := 0.522
const V011_EDGE_BAND_OFFSET := 0.526
const V011_EDGE_BAND_LENGTH := 1.045
const V011_EDGE_BAND_THICKNESS := 0.032


func _build_ui() -> void:
	super._build_ui()
	_rewrite_copy_for_v011(self)
	if _viewport:
		_viewport.msaa_3d = Viewport.MSAA_4X
	if _stage_label:
		_stage_label.text = "Artifact type: godot_runtime_dice_motion_v0_11_simplified_faces"


func _rewrite_copy_for_v011(node: Node) -> void:
	if node is Label:
		var label := node as Label
		label.text = label.text.replace("Dice Motion v0.9.2 - Angus 3D角色骰内嵌骰面预览", "Dice Motion v0.11 - Angus 简化骰面 Godot 预览")
		label.text = label.text.replace("验证 AI 骰面图集切图后进入 Godot 3D 骰子", "验证简化骰面 tile 进入 Godot 3D 骰子")
		label.text = label.text.replace("本轮改为“2x2 方形 sheet -> 几何 gate -> 方形 tile -> 贴进 Godot 3D 骰子”：先挡住源资源比例错误。", "本轮使用“无字生图底面 -> 程序真字回填 -> 方形 tile -> Godot 贴图”：顶面优先读属性 + 点数。")
		label.text = label.text.replace("Artifact type: godot_runtime_dice_motion_v0_9_2_inset_faces", "Artifact type: godot_runtime_dice_motion_v0_11_simplified_faces")
	elif node is RichTextLabel:
		var rich := node as RichTextLabel
		rich.text = rich.text.replace("这张图是 Godot 运行中的贴图资产验证稿，不再是纯程序色块 blockout。", "这张图是 Godot 运行中的 v0.11 简化骰面贴图验证稿，不再是纯程序色块 blockout。")
		rich.text = rich.text.replace("AI 生成骰面是否先过方形几何 gate", "v0.11 骰面源 sheet 是否先过方形几何 gate")
		rich.text = rich.text.replace("顶面真实骰面信息停住后能否读清", "顶面“属性 + 点数”停住后能否优先读清")
		rich.text = rich.text.replace("四种语义色和黑骰是否区分明确", "图案水印化后，四种语义色和黑骰是否仍区分明确")
	for child in node.get_children():
		_rewrite_copy_for_v011(child)


func _make_die(spec: Dictionary) -> Node3D:
	var root := Node3D.new()
	root.name = "SimplifiedDice3DV011"
	var style := _dice_style(String(spec["kind"]))

	var body := MeshInstance3D.new()
	body.mesh = _make_soft_cube_mesh(1.0, 0.055, 8)
	body.material_override = _dice_material(style)
	body.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	root.add_child(body)

	_add_face_texture(root, String(style["top_tex"]), "top")
	_add_face_texture(root, String(style["front_tex"]), "front")
	_add_face_texture(root, String(style["right_tex"]), "right")
	_add_face_texture(root, String(style["front_tex"]), "back")
	_add_face_texture(root, String(style["right_tex"]), "left")
	_add_face_texture(root, String(style["bottom_tex"]), "bottom")
	_add_edge_band_shell(root, style)
	return root


func _add_face_texture(root: Node3D, texture_path: String, face: String) -> void:
	var texture := _load_runtime_texture(texture_path)
	if texture == null:
		return
	var plane := MeshInstance3D.new()
	var mesh := PlaneMesh.new()
	mesh.size = Vector2(V011_FACE_CAP_SIZE, V011_FACE_CAP_SIZE)
	plane.mesh = mesh
	plane.material_override = _face_texture_material(texture)
	var offset := V011_FACE_CAP_OFFSET
	if face == "front":
		plane.position = Vector3(0, 0, offset)
		plane.rotation_degrees = Vector3(90, 0, 0)
	elif face == "back":
		plane.position = Vector3(0, 0, -offset)
		plane.rotation_degrees = Vector3(-90, 0, 0)
	elif face == "right":
		plane.position = Vector3(offset, 0, 0)
		plane.rotation_degrees = Vector3(0, 0, -90)
	elif face == "left":
		plane.position = Vector3(-offset, 0, 0)
		plane.rotation_degrees = Vector3(0, 0, 90)
	elif face == "bottom":
		plane.position = Vector3(0, -offset, 0)
		plane.rotation_degrees = Vector3(180, 0, 0)
	else:
		plane.position = Vector3(0, offset, 0)
	root.add_child(plane)


func _dice_style(kind: String) -> Dictionary:
	if kind == "reason":
		return {
			"body": Color("#1f7884"),
			"rim": Color("#d9e3d6"),
			"print": Color("#f2e5bc"),
			"side_print": Color("#d4ded6"),
			"outline": Color(0.02, 0.08, 0.09, 0.9),
			"top_tex": "%s/dice_face_top_reason.png" % V011_ROOT,
			"front_tex": "%s/dice_face_side_reason_watermark.png" % V011_ROOT,
			"right_tex": "%s/dice_face_side_reason_watermark.png" % V011_ROOT,
			"bottom_tex": "%s/dice_face_side_reason_watermark.png" % V011_ROOT,
		}
	if kind == "occult":
		return {
			"body": Color("#463158"),
			"rim": Color("#a886b7"),
			"print": Color("#f0dfba"),
			"side_print": Color("#c9b6d2"),
			"outline": Color(0.03, 0.02, 0.05, 0.92),
			"top_tex": "%s/dice_face_top_occult.png" % V011_ROOT,
			"front_tex": "%s/dice_face_side_occult_watermark.png" % V011_ROOT,
			"right_tex": "%s/dice_face_side_occult_watermark.png" % V011_ROOT,
			"bottom_tex": "%s/dice_face_side_occult_watermark.png" % V011_ROOT,
		}
	if kind == "ghost":
		return {
			"body": Color("#171719"),
			"rim": Color("#e85b36"),
			"print": Color("#ff7048"),
			"side_print": Color("#a79aa7"),
			"outline": Color(0.02, 0.01, 0.01, 0.95),
			"top_tex": "%s/dice_face_top_ghost.png" % V011_ROOT,
			"front_tex": "%s/dice_face_side_ghost_watermark.png" % V011_ROOT,
			"right_tex": "%s/dice_face_side_ghost_watermark.png" % V011_ROOT,
			"bottom_tex": "%s/dice_face_side_ghost_watermark.png" % V011_ROOT,
		}
	return {
		"body": Color("#43552a"),
		"rim": Color("#d5ddb2"),
		"print": Color("#f2e5bc"),
		"side_print": Color("#cbd5a4"),
		"outline": Color(0.02, 0.04, 0.02, 0.92),
		"top_tex": "%s/dice_face_top_explore.png" % V011_ROOT,
		"front_tex": "%s/dice_face_side_explore_watermark.png" % V011_ROOT,
		"right_tex": "%s/dice_face_side_explore_watermark.png" % V011_ROOT,
		"bottom_tex": "%s/dice_face_side_explore_watermark.png" % V011_ROOT,
	}


func _add_edge_band_shell(root: Node3D, style: Dictionary) -> void:
	var body := style["body"] as Color
	var rim := style["rim"] as Color
	var edge_color := body.lerp(rim, 0.18)
	var edge_mat := _mat(edge_color, 0.76, rim)
	var o := V011_EDGE_BAND_OFFSET
	var l := V011_EDGE_BAND_LENGTH
	var t := V011_EDGE_BAND_THICKNESS

	for sy in [-1.0, 1.0]:
		for sz in [-1.0, 1.0]:
			_add_edge_band(root, Vector3(0.0, sy * o, sz * o), Vector3(l, t, t), edge_mat)
	for sx in [-1.0, 1.0]:
		for sz in [-1.0, 1.0]:
			_add_edge_band(root, Vector3(sx * o, 0.0, sz * o), Vector3(t, l, t), edge_mat)
	for sx in [-1.0, 1.0]:
		for sy in [-1.0, 1.0]:
			_add_edge_band(root, Vector3(sx * o, sy * o, 0.0), Vector3(t, t, l), edge_mat)


func _add_edge_band(root: Node3D, position: Vector3, size: Vector3, material: StandardMaterial3D) -> void:
	var band := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	band.mesh = mesh
	band.position = position
	band.material_override = material
	root.add_child(band)


func _apply_motion(t: float) -> void:
	super._apply_motion(t)
	if _stage_label:
		_stage_label.text = _stage_label.text.replace("godot_runtime_dice_motion_v0_9_2_inset_faces", "godot_runtime_dice_motion_v0_11_simplified_faces")


func _apply_contained_motion(entry: Dictionary, tt: float) -> String:
	var stage := super._apply_contained_motion(entry, tt)
	var die := entry["die"] as Node3D
	if die:
		die.scale *= V011_RUNTIME_SCALE_MULTIPLIER
	return stage
