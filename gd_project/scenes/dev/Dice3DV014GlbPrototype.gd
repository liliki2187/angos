extends "res://scenes/dev/Dice3DV013GlbPrototype.gd"


const V014_GLB_PATHS := {
	"explore": "res://Assets/dice_models/v0_14/dice_explore_v0_14.glb",
	"reason": "res://Assets/dice_models/v0_14/dice_reason_v0_14.glb",
	"occult": "res://Assets/dice_models/v0_14/dice_occult_v0_14.glb",
	"ghost": "res://Assets/dice_models/v0_14/dice_ghost_v0_14.glb",
}


func _rewrite_copy_for_v011(node: Node) -> void:
	super._rewrite_copy_for_v011(node)
	if node is Label:
		var label := node as Label
		label.text = label.text.replace("v0.13", "v0.14")
		label.text = label.text.replace("信息安全区预览", "数字优先骰面预览")
		label.text = label.text.replace("文数分区 UV atlas", "数字放大 / 图标缩小 UV atlas")
		label.text = label.text.replace("godot_runtime_dice_motion_v0_13_text_safe_glb_uv", "godot_runtime_dice_motion_v0_14_number_priority_glb_uv")
	elif node is RichTextLabel:
		var rich := node as RichTextLabel
		rich.text = rich.text.replace("v0.13", "v0.14")
		rich.text = rich.text.replace("顶面文字、数值徽章和图案水印是否互不遮挡", "顶面数字是否升为第二主读信息，图标是否退为小水印")
		rich.text = rich.text.replace("标题 / 数值 / 水印三层信息安全区", "标题 / 放大数字 / 小水印三层信息权重")


func _make_die(spec: Dictionary) -> Node3D:
	var kind := String(spec["kind"])
	var scene_path := String(V014_GLB_PATHS.get(kind, V014_GLB_PATHS["explore"]))
	var packed := load(scene_path) as PackedScene
	var root := Node3D.new()
	root.name = "NumberPriorityGlbDice3DV014"
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
		_stage_label.text = _stage_label.text.replace("godot_runtime_dice_motion_v0_13_text_safe_glb_uv", "godot_runtime_dice_motion_v0_14_number_priority_glb_uv")
