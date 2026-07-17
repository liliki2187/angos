extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-24-world-map-benchmark-landing"
const PARENT_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v090_right_dossier_candidate_a/ingredients/right_dossier_page_candidate_a_parent_hollow_shell_2x.png"
const MISSION_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v090_right_dossier_candidate_a/ingredients/right_mission_intel_button_candidate_a_teal_2x.png"
const PRIMARY_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v090_right_dossier_candidate_a/ingredients/right_action_lane_candidate_a_primary_olive_2x.png"
const PHOTO_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_clean_photo_selected.png"
const GLOBE_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v090_right_dossier_candidate_a/ingredients/runtime_icons/right_dossier_runtime_globe.png"
const DOCUMENT_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v090_right_dossier_candidate_a/ingredients/runtime_icons/right_dossier_runtime_document.png"
const ARROW_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v090_right_dossier_candidate_a/ingredients/runtime_icons/right_dossier_runtime_arrow.png"
const CHECK_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v090_right_dossier_candidate_a/ingredients/runtime_icons/right_dossier_runtime_check.png"

const RUNTIME_SIZE := Vector2i(1920, 1080)
const DISPLAY_SCALE := 1.5
const DOSSIER_SIZE := Vector2(320.0, 520.0) * DISPLAY_SCALE
const DOSSIER_POS := Vector2(76.0, 150.0)

const SLOTS := {
	"header_icon": Rect2(24.0, 38.0, 36.0, 36.0),
	"title_slot": Rect2(82.0, 42.0, 160.0, 34.0),
	"status_stamp": Rect2(246.0, 34.0, 58.0, 58.0),
	"photo_slot": Rect2(22.0, 98.0, 276.0, 176.0),
	"region_body": Rect2(22.0, 288.0, 276.0, 54.0),
	"decision_facts": Rect2(22.0, 346.0, 276.0, 32.0),
	"mission_intel_button": Rect2(18.0, 390.0, 284.0, 44.0),
	"primary_enter_cta": Rect2(18.0, 444.0, 284.0, 50.0),
}
const MISSION_SLOTS := {
	"left_icon_zone": Rect2(10.0, 5.0, 34.0, 34.0),
	"label_plate": Rect2(58.0, 6.0, 170.0, 32.0),
	"right_action_badge": Rect2(232.0, 4.0, 40.0, 36.0),
}
const PRIMARY_SLOTS := {
	"left_icon_zone": Rect2(12.0, 8.0, 34.0, 34.0),
	"label_plate": Rect2(62.0, 9.0, 170.0, 32.0),
	"right_action_badge": Rect2(238.0, 5.0, 42.0, 40.0),
}

var _viewport: SubViewport
var _root_control: Control
var _parent_texture: Texture2D
var _mission_texture: Texture2D
var _primary_texture: Texture2D
var _photo_texture: Texture2D
var _globe_icon: Texture2D
var _document_icon: Texture2D
var _arrow_icon: Texture2D
var _check_icon: Texture2D
var _baseline_image: Image


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	_parent_texture = _load_texture(PARENT_PATH)
	_mission_texture = _load_texture(MISSION_PATH)
	_primary_texture = _load_texture(PRIMARY_PATH)
	_photo_texture = _load_texture(PHOTO_PATH)
	_globe_icon = _load_texture(GLOBE_ICON_PATH)
	_document_icon = _load_texture(DOCUMENT_ICON_PATH)
	_arrow_icon = _load_texture(ARROW_ICON_PATH)
	_check_icon = _load_texture(CHECK_ICON_PATH)
	if _parent_texture == null or _mission_texture == null or _primary_texture == null or _photo_texture == null or _globe_icon == null or _document_icon == null or _arrow_icon == null or _check_icon == null:
		quit(1)
		return
	var ok := true
	ok = await _capture(false, "585-world-map-wmw-v0-9-0-right-dossier-candidate-a-godot-runtime.png") and ok
	ok = await _capture(true, "586-world-map-wmw-v0-9-0-right-dossier-candidate-a-godot-runtime-qa.png") and ok
	if not ok:
		push_error("Godot v0.9.0 right-dossier capture failed.")
		quit(1)
		return
	print("capture_world_map_wmw_right_dossier_runtime_v090.gd OK")
	quit(0)


func _load_texture(path: String) -> Texture2D:
	var image := Image.load_from_file(ProjectSettings.globalize_path(path))
	if image == null:
		push_error("Missing runtime image: " + path)
		return null
	return ImageTexture.create_from_image(image)


func _capture(show_qa: bool, file_name: String) -> bool:
	_viewport = SubViewport.new()
	_viewport.disable_3d = true
	_viewport.size = RUNTIME_SIZE
	_viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	_viewport.transparent_bg = false
	root.add_child(_viewport)
	_root_control = Control.new()
	_root_control.position = Vector2.ZERO
	_root_control.size = Vector2(RUNTIME_SIZE)
	_viewport.add_child(_root_control)
	_build_scene()
	if show_qa:
		_add_qa_overlays()
	await _settle_frames(8)
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	return _save_png(file_name, show_qa)


func _save_png(file_name: String, is_qa: bool) -> bool:
	var texture := _viewport.get_texture()
	if texture == null:
		push_error("SubViewport texture is null for %s" % file_name)
		return false
	var image := texture.get_image()
	if image == null:
		push_error("SubViewport image is null for %s" % file_name)
		return false
	if _is_all_black(image):
		push_error("Captured image is all black for %s." % file_name)
		return false
	var color_count := _sampled_color_count(image)
	if color_count < 80:
		push_error("Captured image has only %d sampled colors for %s." % [color_count, file_name])
		return false
	if is_qa:
		var missing_baseline_pixels := _count_qa_missing_baseline_pixels(image)
		if missing_baseline_pixels > 20:
			push_error("QA capture lost %d sampled baseline pixels for %s." % [missing_baseline_pixels, file_name])
			return false
	else:
		_baseline_image = image.duplicate()
	var error := image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
	if error != OK:
		push_error("save_png failed for %s: %s" % [file_name, error])
		return false
	print("saved %s sampled_colors=%d" % [file_name, color_count])
	return true


func _is_all_black(image: Image) -> bool:
	for y in range(0, image.get_height(), 72):
		for x in range(0, image.get_width(), 96):
			var color := image.get_pixel(x, y)
			if color.r > 0.005 or color.g > 0.005 or color.b > 0.005:
				return false
	return true


func _sampled_color_count(image: Image) -> int:
	var colors := {}
	for y in range(0, image.get_height(), 8):
		for x in range(0, image.get_width(), 8):
			colors[image.get_pixel(x, y).to_rgba32()] = true
	return colors.size()


func _count_qa_missing_baseline_pixels(image: Image) -> int:
	if _baseline_image == null or _baseline_image.get_size() != image.get_size():
		return 1000000
	var missing := 0
	for y in range(0, image.get_height(), 4):
		for x in range(0, image.get_width(), 4):
			var before := _baseline_image.get_pixel(x, y)
			var after := image.get_pixel(x, y)
			var before_peak: float = maxf(before.r, maxf(before.g, before.b))
			var after_peak: float = maxf(after.r, maxf(after.g, after.b))
			if before_peak > 0.16 and after_peak < before_peak * 0.48:
				missing += 1
	return missing


func _build_scene() -> void:
	var bg := ColorRect.new()
	bg.color = Color("#071315")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root_control.add_child(bg)

	var stage := ColorRect.new()
	stage.color = Color("#0b2022")
	stage.position = Vector2(40, 122)
	stage.size = Vector2(555, 914)
	_root_control.add_child(stage)

	_add_dossier()

	_add_label("Godot 4.6.2 · WMW right dossier candidate A", Rect2(660, 56, 1160, 48), 31, Color("#f2ead0"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("Three clean masters: neutral parent hollow shell + teal secondary + olive primary.", Rect2(662, 106, 1120, 34), 18, Color("#c8d7c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("A196", Rect2(710, 230, 150, 34), 21, Color("#65ff94"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("Visible bodies share the same 284px width and centerline. Shadows are measured separately.", Rect2(710, 270, 920, 70), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("A199", Rect2(710, 390, 150, 34), 21, Color("#afcb5f"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("Primary default is muted olive. Teal remains secondary; rust and gray are reserved for risk and disabled states.", Rect2(710, 430, 920, 86), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("LAYER ORDER", Rect2(710, 585, 250, 34), 20, Color("#55e0e5"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("photo → hollow parent shell → independent child skins → runtime labels and symbols", Rect2(710, 625, 930, 70), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("No parent-side child frames. No text or state glyph is baked into the sprite masters.", Rect2(710, 755, 930, 70), 18, Color("#c8d7c8"), HORIZONTAL_ALIGNMENT_LEFT)


func _add_dossier() -> void:
	var photo_rect := _slot_rect("photo_slot")
	_add_texture(_photo_texture, photo_rect.position, photo_rect.size)
	_add_texture(_parent_texture, DOSSIER_POS, DOSSIER_SIZE)

	var mission_rect := _slot_rect("mission_intel_button")
	var primary_rect := _slot_rect("primary_enter_cta")
	_add_texture(_mission_texture, mission_rect.position, mission_rect.size)
	_add_texture(_primary_texture, primary_rect.position, primary_rect.size)

	_add_icon(_globe_icon, _slot_rect("header_icon"), Color("#5d604e"), 0.86)
	_add_label("北美禁区警戒带", _slot_rect("title_slot"), 27, Color("#1c1e19"), HORIZONTAL_ALIGNMENT_CENTER)
	var status := _slot_rect("status_stamp")
	_add_label("高危", Rect2(status.position, Vector2(status.size.x, status.size.y * 0.56)), 22, Color("#8e3627"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_label("推荐12", Rect2(status.position + Vector2(0, status.size.y * 0.54), Vector2(status.size.x, status.size.y * 0.46)), 14, Color("#572632"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_label("天线阵列仍在发射，林线内出现异常回波。\n进入前可先核对本周地区任务与封锁条件。", _slot_rect("region_body"), 16, Color("#22251f"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("限时 2 周 · 线索缺口 3 · 深链 1", _slot_rect("decision_facts"), 16, Color("#3e4438"), HORIZONTAL_ALIGNMENT_CENTER)

	var mission_left := _child_slot_rect(mission_rect, MISSION_SLOTS["left_icon_zone"])
	var mission_label := _child_slot_rect(mission_rect, MISSION_SLOTS["label_plate"])
	var mission_right := _child_slot_rect(mission_rect, MISSION_SLOTS["right_action_badge"])
	_add_icon(_document_icon, mission_left, Color("#eee5c9"), 0.84)
	_add_label("查看任务情报 · 12项", mission_label, 18, Color("#1f5255"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_icon(_arrow_icon, mission_right, Color("#eee5c9"), 0.78)

	var primary_left := _child_slot_rect(primary_rect, PRIMARY_SLOTS["left_icon_zone"])
	var primary_label := _child_slot_rect(primary_rect, PRIMARY_SLOTS["label_plate"])
	var primary_right := _child_slot_rect(primary_rect, PRIMARY_SLOTS["right_action_badge"])
	_add_icon(_arrow_icon, primary_left, Color("#eee5c9"), 0.78)
	_add_label("进入选定地区", primary_label, 20, Color("#3a4229"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_icon(_check_icon, primary_right, Color("#eee5c9"), 0.82)


func _slot_rect(name: String) -> Rect2:
	var rect: Rect2 = SLOTS[name]
	return Rect2(DOSSIER_POS + rect.position * DISPLAY_SCALE, rect.size * DISPLAY_SCALE)


func _child_slot_rect(parent_rect: Rect2, slot: Rect2) -> Rect2:
	return Rect2(parent_rect.position + slot.position * DISPLAY_SCALE, slot.size * DISPLAY_SCALE)


func _add_texture(texture: Texture2D, pos: Vector2, size: Vector2) -> void:
	var node := TextureRect.new()
	node.texture = texture
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.stretch_mode = TextureRect.STRETCH_SCALE
	node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	node.position = pos
	node.size = size
	_root_control.add_child(node)


func _add_icon(texture: Texture2D, rect: Rect2, color: Color, scale: float) -> void:
	var node := TextureRect.new()
	node.texture = texture
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	node.modulate = color
	node.size = rect.size * scale
	node.position = rect.position + (rect.size - node.size) * 0.5
	_root_control.add_child(node)


func _add_label(text_value: String, rect: Rect2, font_size: int, color: Color, alignment: HorizontalAlignment) -> void:
	var label := Label.new()
	label.text = text_value
	label.position = rect.position
	label.size = rect.size
	label.horizontal_alignment = alignment
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.clip_text = true
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	_root_control.add_child(label)


func _add_qa_overlays() -> void:
	var colors := {
		"header_icon": Color("#51eeff"),
		"title_slot": Color("#ff48ca"),
		"status_stamp": Color("#ff6f5f"),
		"photo_slot": Color("#48ecae"),
		"region_body": Color("#ffd444"),
		"decision_facts": Color("#a780ff"),
		"mission_intel_button": Color("#4fdae8"),
		"primary_enter_cta": Color("#aecc5b"),
	}
	for name in colors:
		_add_rect(_slot_rect(name), colors[name], name)


func _add_rect(rect: Rect2, color: Color, label_text: String) -> void:
	var box := ColorRect.new()
	box.color = Color(color.r, color.g, color.b, 0.08)
	box.position = rect.position
	box.size = rect.size
	_root_control.add_child(box)
	var line := ReferenceRect.new()
	line.position = rect.position
	line.size = rect.size
	line.border_color = color
	line.border_width = 2.0
	_root_control.add_child(line)
	_add_label(label_text, Rect2(rect.position + Vector2(3, 1), Vector2(220, 20)), 11, color, HORIZONTAL_ALIGNMENT_LEFT)


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
