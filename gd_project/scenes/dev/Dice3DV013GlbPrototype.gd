extends "res://scenes/dev/Dice3DV012GlbPrototype.gd"


const V013_GLB_PATHS := {
	"explore": "res://Assets/dice_models/v0_13/dice_explore_v0_13.glb",
	"reason": "res://Assets/dice_models/v0_13/dice_reason_v0_13.glb",
	"occult": "res://Assets/dice_models/v0_13/dice_occult_v0_13.glb",
	"ghost": "res://Assets/dice_models/v0_13/dice_ghost_v0_13.glb",
}


func _rewrite_copy_for_v011(node: Node) -> void:
	super._rewrite_copy_for_v011(node)
	if node is Label:
		var label := node as Label
		label.text = label.text.replace("v0.12", "v0.13")
		label.text = label.text.replace("GLB/UV 连续骰体预览", "GLB/UV 信息安全区预览")
		label.text = label.text.replace("GLB 封闭倒角骰体 + 正式 UV atlas", "GLB 封闭倒角骰体 + 文数分区 UV atlas")
		label.text = label.text.replace("godot_runtime_dice_motion_v0_12_glb_uv_closed_body", "godot_runtime_dice_motion_v0_13_text_safe_glb_uv")
	elif node is RichTextLabel:
		var rich := node as RichTextLabel
		rich.text = rich.text.replace("v0.12", "v0.13")
		rich.text = rich.text.replace("顶面/属性 + 点数/停住后能否优先读清", "顶面文字、数值徽章和图案水印是否互不遮挡")
		rich.text = rich.text.replace("顶/侧/角接缝是否读作实体倒角，而不是空缝或黑洞", "保留 v0.12 封闭接缝，同时检查标题 / 数值 / 水印三层信息安全区")


func _make_die(spec: Dictionary) -> Node3D:
	var kind := String(spec["kind"])
	var scene_path := String(V013_GLB_PATHS.get(kind, V013_GLB_PATHS["explore"]))
	var packed := load(scene_path) as PackedScene
	var root := Node3D.new()
	root.name = "TextSafeGlbDice3DV013"
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
		_stage_label.text = _stage_label.text.replace("godot_runtime_dice_motion_v0_12_glb_uv_closed_body", "godot_runtime_dice_motion_v0_13_text_safe_glb_uv")
