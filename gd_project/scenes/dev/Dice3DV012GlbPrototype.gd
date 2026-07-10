extends "res://scenes/dev/Dice3DV011Prototype.gd"


const V012_GLB_PATHS := {
	"explore": "res://Assets/dice_models/v0_12/dice_explore_v0_12.glb",
	"reason": "res://Assets/dice_models/v0_12/dice_reason_v0_12.glb",
	"occult": "res://Assets/dice_models/v0_12/dice_occult_v0_12.glb",
	"ghost": "res://Assets/dice_models/v0_12/dice_ghost_v0_12.glb",
}


func _rewrite_copy_for_v011(node: Node) -> void:
	super._rewrite_copy_for_v011(node)
	if node is Label:
		var label := node as Label
		label.text = label.text.replace("Dice Motion v0.11 - Angus 简化骰面 Godot 预览", "Dice Motion v0.12 - Angus GLB/UV 连续骰体预览")
		label.text = label.text.replace("验证简化骰面 tile 进入 Godot 3D 骰子", "验证 GLB 封闭倒角骰体 + 正式 UV atlas 进入 Godot 3D 骰子")
		label.text = label.text.replace("本轮使用“无字生图底面 -> 程序真字回填 -> 方形 tile -> Godot 贴图”：顶面优先读属性 + 点数。", "本轮使用“方形 tile -> 3x2 UV atlas -> 封闭倒角 GLB -> Godot runtime”：重点检查顶面/侧面/角点不再露空缝。")
		label.text = label.text.replace("Artifact type: godot_runtime_dice_motion_v0_11_simplified_faces", "Artifact type: godot_runtime_dice_motion_v0_12_glb_uv_closed_body")
	elif node is RichTextLabel:
		var rich := node as RichTextLabel
		rich.text = rich.text.replace("v0.11 简化骰面贴图验证稿", "v0.12 GLB / UV 连续骰体验证稿")
		rich.text = rich.text.replace("v0.11 骰面源 sheet 是否先过方形几何 gate", "v0.12 GLB 是否使用封闭倒角 mesh 和 3x2 UV atlas")
		rich.text = rich.text.replace("方形 tile 是否已贴到 3D 骰子", "Godot 是否加载真实 GLB，而不是 6 张独立贴片")
		rich.text = rich.text.replace("顶面“属性 + 点数”停住后能否优先读清", "顶面“属性 + 点数”停住后能否优先读清")
		rich.text = rich.text.replace("图案水印化后，四种语义色和黑骰是否仍区分明确", "顶/侧/角接缝是否读作实体倒角，而不是空缝或黑洞")


func _make_die(spec: Dictionary) -> Node3D:
	var kind := String(spec["kind"])
	var scene_path := String(V012_GLB_PATHS.get(kind, V012_GLB_PATHS["explore"]))
	var packed := load(scene_path) as PackedScene
	var root := Node3D.new()
	root.name = "ClosedGlbDice3DV012"
	if packed == null:
		push_warning("Failed to load dice GLB: %s" % scene_path)
		return root
	var glb_instance := packed.instantiate() as Node3D
	if glb_instance == null:
		push_warning("Dice GLB did not instantiate as Node3D: %s" % scene_path)
		return root
	root.add_child(glb_instance)
	return root


func _apply_motion(t: float) -> void:
	super._apply_motion(t)
	if _stage_label:
		_stage_label.text = _stage_label.text.replace("godot_runtime_dice_motion_v0_11_simplified_faces", "godot_runtime_dice_motion_v0_12_glb_uv_closed_body")
