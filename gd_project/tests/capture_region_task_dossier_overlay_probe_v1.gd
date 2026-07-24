extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-22-region-task-dossier-overlay-stitch-probe-v1"
const BASE_PATH := "res://Assets/ui/angus_packaging/region_task/v2/dossier_overlay_probe_v1/rt-dossier-base-shell-probe-v1-2x.png"
const SUMMARY_PATH := "res://Assets/ui/angus_packaging/region_task/v2/dossier_overlay_probe_v1/rt-dossier-summary-accent-probe-v1-2x.png"
const METADATA_PATH := "res://Assets/ui/angus_packaging/region_task/v2/dossier_overlay_probe_v1/rt-dossier-metadata-wash-probe-v1-2x.png"
const RISK_PATH := "res://Assets/ui/angus_packaging/region_task/v2/dossier_overlay_probe_v1/rt-dossier-risk-wash-probe-v1-2x.png"
const CTA_PATH := "res://Assets/ui/angus_packaging/region_task/v2/dossier_overlay_probe_v1/rt-dossier-cta-probe-v1-2x.png"

const DOSSIER_SIZE := Vector2(412.0, 960.0)
const PAPER_TEXT := Color("183a3f")
const TEAL_TEXT := Color("2b7373")
const RUST_TEXT := Color("9d4930")
const MUTED_TEXT := Color("5f6d69")
const CTA_TEXT := Color("eef0d8")


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(1920, 1080)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
	root.add_child(viewport)

	var background := ColorRect.new()
	background.color = Color("061f2d")
	background.position = Vector2.ZERO
	background.size = Vector2(1920, 1080)
	viewport.add_child(background)

	_add_screen_label(viewport, Rect2(238, 26, 560, 38), "叠印关闭：完整底纸仍独立成立", 24, Color("ddd7bd"))
	_add_screen_label(viewport, Rect2(1040, 26, 620, 38), "叠印开启：同一纸面 + 真实运行文字", 24, Color("ddd7bd"))
	_add_screen_label(viewport, Rect2(238, 58, 560, 24), "无色块、无 CTA、无文字", 14, Color("78aaa8"))
	_add_screen_label(viewport, Rect2(1040, 58, 620, 24), "青色 / 锈色只作为透明美术层；文字不进贴图", 14, Color("78aaa8"))

	var base_only := Control.new()
	base_only.position = Vector2(300, 86)
	base_only.size = DOSSIER_SIZE
	viewport.add_child(base_only)
	_add_full_dossier_texture(base_only, BASE_PATH)

	var final_dossier := Control.new()
	final_dossier.position = Vector2(1100, 86)
	final_dossier.size = DOSSIER_SIZE
	viewport.add_child(final_dossier)
	_build_final_dossier(final_dossier)

	for _frame in range(12):
		await process_frame
	viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
	await RenderingServer.frame_post_draw

	var full := viewport.get_texture().get_image()
	var full_path := ProjectSettings.globalize_path("%s/05-dossier-overlay-stitch-probe-1x-v3.png" % OUT_DIR)
	var full_error := full.save_png(full_path)
	if full_error != OK:
		push_error("Failed to save dossier overlay probe: %s" % error_string(full_error))

	var dossier_crop := full.get_region(Rect2i(1100, 86, 412, 960))
	var crop_path := ProjectSettings.globalize_path("%s/06-final-dossier-with-runtime-text-1x-v3.png" % OUT_DIR)
	var crop_error := dossier_crop.save_png(crop_path)
	if crop_error != OK:
		push_error("Failed to save final dossier crop: %s" % error_string(crop_error))

	print("capture_region_task_dossier_overlay_probe_v1.gd OK")
	quit(0)


func _build_final_dossier(parent: Control) -> void:
	_add_full_dossier_texture(parent, BASE_PATH)
	_add_full_dossier_texture(parent, SUMMARY_PATH)
	_add_full_dossier_texture(parent, METADATA_PATH)
	_add_full_dossier_texture(parent, RISK_PATH)
	_add_texture(parent, CTA_PATH, Rect2(28, 820, 356, 112))

	_add_label(parent, Rect2(40, 29, 348, 18), "当前任务 · CURRENT ASSIGNMENT", 11, TEAL_TEXT)
	_add_label(parent, Rect2(24, 55, 364, 34), "明日电台的停电预告", 23, PAPER_TEXT)

	_add_label(parent, Rect2(48, 153, 316, 20), "事件摘要", 11, TEAL_TEXT)
	_add_label(
		parent,
		Rect2(48, 184, 320, 242),
		"同一城区连续收到异常广播举报。\n停电后，旧电台会先播出明日新闻。\n三名听众记下了互相矛盾的时间。\n其中一段录音提到尚未发生的火灾。\n线路图显示信号绕过了主发射塔。\n编辑部需要确认预告是否能被改变。\n本次调查将决定后续连续追踪入口。",
		12,
		PAPER_TEXT,
		6
	)

	_add_label(parent, Rect2(48, 480, 310, 18), "地点 / 耗时 / 需求", 11, TEAL_TEXT)
	_add_label(parent, Rect2(48, 510, 320, 22), "地点：北岸旧电台 / 变电站", 14, PAPER_TEXT)
	_add_label(parent, Rect2(48, 546, 320, 22), "耗时：2天　需求：洞察 / 推理", 14, PAPER_TEXT)

	_add_label(parent, Rect2(62, 626, 300, 25), "风险等级：高", 17, RUST_TEXT)
	_add_label(parent, Rect2(62, 660, 300, 16), "依据", 11, RUST_TEXT)
	_add_label(parent, Rect2(62, 681, 306, 38), "截稿：本周截稿前 2 天\n连续追踪：成功后开启后续入口", 12, PAPER_TEXT, 3)
	_add_label(parent, Rect2(62, 730, 300, 16), "建议", 11, TEAL_TEXT)
	_add_label(parent, Rect2(62, 751, 306, 39), "优先派遣洞察较高的记者；\n签批时复核黑骰风险。", 12, PAPER_TEXT, 3)

	var cta_ready := _add_label(parent, Rect2(28, 841, 356, 18), "任务已就绪", 11, CTA_TEXT)
	cta_ready.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var cta_action := _add_label(parent, Rect2(28, 868, 356, 32), "送至签批台", 20, CTA_TEXT)
	cta_action.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER


func _add_full_dossier_texture(parent: Control, path: String) -> TextureRect:
	return _add_texture(parent, path, Rect2(Vector2.ZERO, DOSSIER_SIZE))


func _add_texture(parent: Control, path: String, rect: Rect2) -> TextureRect:
	var texture := load(path) as Texture2D
	if texture == null:
		push_error("Missing probe texture: %s" % path)
	var view := TextureRect.new()
	view.position = rect.position
	view.size = rect.size
	view.texture = texture
	view.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	view.stretch_mode = TextureRect.STRETCH_SCALE
	view.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	view.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(view)
	return view


func _add_label(
	parent: Control,
	rect: Rect2,
	text: String,
	font_size: int,
	color: Color,
	line_spacing: int = 0
) -> Label:
	var label := Label.new()
	label.position = rect.position
	label.size = rect.size
	label.text = text
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.add_theme_constant_override("line_spacing", line_spacing)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.clip_text = true
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(label)
	return label


func _add_screen_label(parent: Node, rect: Rect2, text: String, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.position = rect.position
	label.size = rect.size
	label.text = text
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	parent.add_child(label)
	return label
