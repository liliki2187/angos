extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-24-world-map-benchmark-landing"
const FIXTURE_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v095_right_dossier_candidate_a5/right_dossier_candidate_a5_runtime_fixture.json"
const PARENT_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v095_right_dossier_candidate_a5/ingredients/right_dossier_candidate_a5_parent_2x.png"
const POPOVER_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v095_right_dossier_candidate_a5/ingredients/right_dossier_candidate_a5_mission_popover_2x.png"
const PRIMARY_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v093_right_dossier_candidate_a3/ingredients/right_action_lane_candidate_a3_primary_olive_2x.png"
const PHOTO_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/right_dossier_north_america_photo_552x352.png"
const GLOBE_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_globe.png"
const DOCUMENT_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_document.png"
const ARROW_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_arrow.png"

const RUNTIME_SIZE := Vector2i(1920, 1080)
const DISPLAY_SCALE := 1.5
const DOSSIER_SIZE := Vector2(320.0, 520.0) * DISPLAY_SCALE
const DOSSIER_POS := Vector2(1180.0, 150.0)
const PHOTO_SOURCE_SIZE := Vector2i(552, 352)
const PHOTO_RATIO := 69.0 / 44.0
const HEADER_AXIS_Y := 59.0
const HEADER_ICON_OFFSET_Y := 3.0
const STATUS_GROUP_OFFSET_Y := -4.0
const REGION_BODY_INNER := Rect2(34.0, 292.0, 252.0, 82.0)
const REGION_BODY_NO_TEXT := Rect2(22.0, 288.0, 4.0, 90.0)
const POPOVER_PARENT := Rect2(-294.0, 326.0, 284.0, 156.0)

const SLOTS := {
	"header_icon": Rect2(24.0, 38.0, 36.0, 36.0),
	"title_slot": Rect2(82.0, 42.0, 160.0, 34.0),
	"status_stamp": Rect2(246.0, 34.0, 58.0, 58.0),
	"photo_slot": Rect2(22.0, 98.0, 276.0, 176.0),
	"region_body": Rect2(22.0, 288.0, 276.0, 90.0),
	"mission_intel_button": Rect2(18.0, 390.0, 284.0, 44.0),
	"primary_enter_cta": Rect2(18.0, 444.0, 284.0, 50.0),
}
const MISSION_SLOTS := {
	"left_icon_zone": Rect2(10.0, 5.0, 28.0, 34.0),
	"title_label": Rect2(42.0, 6.0, 56.0, 32.0),
	"facts_label": Rect2(102.0, 6.0, 142.0, 32.0),
	"chevron_zone": Rect2(252.0, 4.0, 20.0, 36.0),
}
const PRIMARY_SLOTS := {
	"left_icon_zone": Rect2(12.0, 8.0, 34.0, 34.0),
	"label_plate": Rect2(62.0, 9.0, 170.0, 32.0),
	"right_action_badge": Rect2(238.0, 5.0, 42.0, 40.0),
}
const SUMMARY_DIVIDER := Rect2(10.0, 42.0, 264.0, 1.0)

var _viewport: SubViewport
var _root_control: Control
var _parent_texture: Texture2D
var _popover_texture: Texture2D
var _primary_texture: Texture2D
var _photo_texture: Texture2D
var _globe_icon: Texture2D
var _document_icon: Texture2D
var _arrow_icon: Texture2D
var _runtime_fixture: Dictionary
var _expanded_baseline: Image
var _qa_rects: Dictionary = {}


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	if not _load_runtime_fixture():
		quit(1)
		return
	_parent_texture = _load_texture(PARENT_PATH)
	_popover_texture = _load_texture(POPOVER_PATH)
	_primary_texture = _load_texture(PRIMARY_PATH)
	_photo_texture = _load_texture(PHOTO_PATH)
	_globe_icon = _load_texture(GLOBE_ICON_PATH)
	_document_icon = _load_texture(DOCUMENT_ICON_PATH)
	_arrow_icon = _load_texture(ARROW_ICON_PATH)
	if _parent_texture == null or _popover_texture == null or _primary_texture == null or _photo_texture == null or _globe_icon == null or _document_icon == null or _arrow_icon == null:
		quit(1)
		return
	if _parent_texture.get_size() != Vector2(640, 1040):
		push_error("A5 parent ingredient dimensions drifted")
		quit(1)
		return
	if _popover_texture.get_size() != Vector2(568, 312):
		push_error("A5 popover ingredient dimensions drifted")
		quit(1)
		return
	if _primary_texture.get_size() != Vector2(568, 100):
		push_error("A5 reused primary action dimensions drifted")
		quit(1)
		return
	if not _validate_photo_contract():
		quit(1)
		return
	_setup_viewport()
	var ok := true
	ok = await _capture(false, false, "623-world-map-wmw-v0-9-5-right-dossier-candidate-a5-godot-collapsed.png") and ok
	ok = await _capture(true, false, "624-world-map-wmw-v0-9-5-right-dossier-candidate-a5-godot-expanded.png") and ok
	ok = await _capture(true, true, "625-world-map-wmw-v0-9-5-right-dossier-candidate-a5-godot-qa.png") and ok
	if not ok:
		push_error("Godot v0.9.5 right-dossier candidate A5 capture failed")
		quit(1)
		return
	print("capture_world_map_wmw_right_dossier_runtime_v095.gd OK")
	quit(0)


func _load_runtime_fixture() -> bool:
	var absolute_path := ProjectSettings.globalize_path(FIXTURE_PATH)
	var file := FileAccess.open(absolute_path, FileAccess.READ)
	if file == null:
		push_error("Missing production runtime fixture: " + absolute_path)
		return false
	var parsed = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("Runtime fixture is not a JSON object: " + absolute_path)
		return false
	_runtime_fixture = parsed
	var required := [
		"region_title",
		"status_display_text",
		"region_body_text",
		"mission_intel_title",
		"mission_intel_facts",
		"mission_preview",
		"mission_preview_total",
		"primary_enter_label",
	]
	for key in required:
		if not _runtime_fixture.has(key):
			push_error("Runtime fixture is missing field: " + key)
			return false
	if str(_runtime_fixture.get("provenance", "")) != "production_runtime_export" or _runtime_fixture.get("generated_from_production_data", false) != true:
		push_error("Runtime fixture provenance is not production data")
		return false
	if _runtime_fixture.has("decision_facts"):
		push_error("Retired decision_facts leaked into A5 fixture")
		return false
	if str(_runtime_fixture["mission_intel_title"]) != "任务情报":
		push_error("A5 mission summary title drifted")
		return false
	if not _runtime_fixture["mission_preview"] is Array or _runtime_fixture["mission_preview"].is_empty():
		push_error("A5 mission preview must contain production rows")
		return false
	print("runtime_fixture provenance=production_runtime_export region=%s preview=%d" % [str(_runtime_fixture.get("region_id", "")), _runtime_fixture["mission_preview"].size()])
	return true


func _load_texture(path: String) -> Texture2D:
	var image := Image.load_from_file(ProjectSettings.globalize_path(path))
	if image == null:
		push_error("Missing runtime image: " + path)
		return null
	return ImageTexture.create_from_image(image)


func _validate_photo_contract() -> bool:
	var actual_size := Vector2i(_photo_texture.get_width(), _photo_texture.get_height())
	if actual_size != PHOTO_SOURCE_SIZE:
		push_error("A5 photo ingredient must be exactly %s, got %s" % [PHOTO_SOURCE_SIZE, actual_size])
		return false
	var actual_ratio := float(actual_size.x) / float(actual_size.y)
	var ratio_error := absf(actual_ratio - PHOTO_RATIO) / PHOTO_RATIO
	var slot: Rect2 = SLOTS["photo_slot"]
	var slot_ratio := slot.size.x / slot.size.y
	if ratio_error > 0.005 or absf(slot_ratio - PHOTO_RATIO) / PHOTO_RATIO > 0.005:
		push_error("A5 photo ratio contract drifted")
		return false
	print("photo_contract size=%s ratio_error=%.6f stretch=KEEP_ASPECT_COVERED" % [actual_size, ratio_error])
	return true


func _setup_viewport() -> void:
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


func _clear_scene() -> void:
	for child in _root_control.get_children():
		_root_control.remove_child(child)
		child.free()
	_qa_rects.clear()


func _capture(expanded: bool, show_qa: bool, file_name: String) -> bool:
	if show_qa:
		if not expanded or _expanded_baseline == null:
			push_error("A5 QA must overlay the retained expanded baseline")
			return false
		_add_qa_overlays(expanded)
	else:
		_clear_scene()
		_build_scene(expanded)
	await _settle_frames(8)
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	return _save_png(file_name, expanded, show_qa)


func _save_png(file_name: String, expanded: bool, is_qa: bool) -> bool:
	var texture := _viewport.get_texture()
	if texture == null:
		push_error("SubViewport texture is null for %s" % file_name)
		return false
	var image := texture.get_image()
	if image == null:
		push_error("SubViewport image is null for %s" % file_name)
		return false
	if _is_all_black(image):
		push_error("Captured image is all black for %s" % file_name)
		return false
	var color_count := _sampled_color_count(image)
	if color_count < 100:
		push_error("Captured image has only %d sampled colors for %s" % [color_count, file_name])
		return false
	if is_qa:
		var missing := _count_missing_baseline_pixels(image, _expanded_baseline)
		if missing > 20:
			push_error("A5 QA capture lost %d sampled expanded-state pixels" % missing)
			return false
	elif expanded:
		_expanded_baseline = image.duplicate()
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


func _count_missing_baseline_pixels(image: Image, baseline: Image) -> int:
	if baseline == null or baseline.get_size() != image.get_size():
		return 1000000
	var missing := 0
	for y in range(0, image.get_height(), 4):
		for x in range(0, image.get_width(), 4):
			var before := baseline.get_pixel(x, y)
			var after := image.get_pixel(x, y)
			var before_peak: float = maxf(before.r, maxf(before.g, before.b))
			var after_peak: float = maxf(after.r, maxf(after.g, after.b))
			if before_peak > 0.16 and after_peak < before_peak * 0.48:
				missing += 1
	return missing


func _build_scene(expanded: bool) -> void:
	var bg := ColorRect.new()
	bg.color = Color("#071315")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root_control.add_child(bg)

	var stage := ColorRect.new()
	stage.color = Color("#0b2022")
	stage.position = Vector2(1140, 122)
	stage.size = Vector2(555, 914)
	_root_control.add_child(stage)

	_add_label("Godot 4.6.2 · WMW dossier A5", Rect2(64, 56, 600, 48), 31, Color("#f2ead0"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("A211 · merged summary; +36 px region body.", Rect2(66, 106, 600, 34), 18, Color("#c8d7c8"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("REGION CONTEXT", Rect2(90, 228, 300, 34), 21, Color("#65ff94"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("Continuous body: 54 px becomes 90 px.\nThe retired facts strip is fully removed.", Rect2(90, 268, 570, 80), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("ONE SUMMARY ROW", Rect2(90, 418, 300, 34), 21, Color("#ffd444"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("Title, counts and chevron share one row.\nThe row owns one hit target.", Rect2(90, 458, 570, 80), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("FIXED PRIMARY ACTION", Rect2(90, 608, 330, 34), 21, Color("#48ecae"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("The olive CTA keeps its original geometry.\nThe drawer opens left; it never moves or covers the CTA.", Rect2(90, 648, 570, 80), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_label("STATE: %s" % ("EXPANDED" if expanded else "COLLAPSED"), Rect2(90, 858, 460, 42), 24, Color("#f2ead0"), HORIZONTAL_ALIGNMENT_LEFT, "")
	_add_dossier(expanded)


func _add_dossier(expanded: bool) -> void:
	var photo_rect := _slot_rect("photo_slot")
	_add_photo_texture(_photo_texture, photo_rect)
	_add_texture(_parent_texture, DOSSIER_POS, DOSSIER_SIZE)

	var mission_rect := _slot_rect("mission_intel_button")
	var primary_rect := _slot_rect("primary_enter_cta")
	_add_texture(_primary_texture, primary_rect.position, primary_rect.size)

	var header_icon_rect := _slot_rect("header_icon")
	header_icon_rect.position.y += HEADER_ICON_OFFSET_Y * DISPLAY_SCALE
	_add_icon(_globe_icon, header_icon_rect, Color("#5d604e"), 0.86)
	_add_label(str(_runtime_fixture["region_title"]), _slot_rect("title_slot"), 27, Color("#1c1e19"), HORIZONTAL_ALIGNMENT_CENTER, "region_title")
	var status := _slot_rect("status_stamp")
	status.position.y += STATUS_GROUP_OFFSET_Y * DISPLAY_SCALE
	_add_label(str(_runtime_fixture["status_display_text"]), status, 15, Color("#8e3627"), HORIZONTAL_ALIGNMENT_CENTER, "status_display_text")
	_add_label(str(_runtime_fixture["region_body_text"]), _reference_rect(REGION_BODY_INNER), 17, Color("#22251f"), HORIZONTAL_ALIGNMENT_LEFT, "region_body_text")

	_add_icon(_document_icon, _child_slot_rect(mission_rect, MISSION_SLOTS["left_icon_zone"]), Color("#3f6663"), 0.72)
	_add_label(str(_runtime_fixture["mission_intel_title"]), _child_slot_rect(mission_rect, MISSION_SLOTS["title_label"]), 16, Color("#3f6663"), HORIZONTAL_ALIGNMENT_LEFT, "mission_intel_title")
	_add_label(str(_runtime_fixture["mission_intel_facts"]), _child_slot_rect(mission_rect, MISSION_SLOTS["facts_label"]), 14, Color("#4b5145"), HORIZONTAL_ALIGNMENT_CENTER, "mission_intel_facts")
	_add_chevron(_child_slot_rect(mission_rect, MISSION_SLOTS["chevron_zone"]), Color("#3f6663"), expanded)
	_add_divider(_child_slot_rect(mission_rect, SUMMARY_DIVIDER), Color(0.247, 0.4, 0.388, 0.28))

	var primary_label := _child_slot_rect(primary_rect, PRIMARY_SLOTS["label_plate"])
	var primary_right := _child_slot_rect(primary_rect, PRIMARY_SLOTS["right_action_badge"])
	_add_label(str(_runtime_fixture["primary_enter_label"]), primary_label, 20, Color("#eee5c9"), HORIZONTAL_ALIGNMENT_CENTER, "primary_enter_label")
	_add_icon(_arrow_icon, primary_right, Color("#eee5c9"), 0.72)

	if expanded:
		_add_popover(mission_rect)


func _add_popover(mission_rect: Rect2) -> void:
	var popover_rect := _reference_rect(POPOVER_PARENT)
	_add_texture(_popover_texture, popover_rect.position, popover_rect.size)
	var rows: Array = _runtime_fixture["mission_preview"]
	var row_height := 36.0 * DISPLAY_SCALE
	var top := popover_rect.position.y + 12.0 * DISPLAY_SCALE
	for index in range(rows.size()):
		var item: Dictionary = rows[index]
		var row_y := top + index * row_height
		if index > 0:
			_add_divider(Rect2(popover_rect.position.x + 12.0 * DISPLAY_SCALE, row_y - 4.0 * DISPLAY_SCALE, popover_rect.size.x - 24.0 * DISPLAY_SCALE, 1.0), Color(0.41, 0.43, 0.36, 0.35))
		_add_label(str(item["kind_label"]), Rect2(popover_rect.position.x + 12.0 * DISPLAY_SCALE, row_y, 36.0 * DISPLAY_SCALE, 24.0 * DISPLAY_SCALE), 14, Color("#3f6663"), HORIZONTAL_ALIGNMENT_LEFT, "mission_preview_%d_kind" % (index + 1))
		_add_label(str(item["name"]), Rect2(popover_rect.position.x + 52.0 * DISPLAY_SCALE, row_y, 178.0 * DISPLAY_SCALE, 24.0 * DISPLAY_SCALE), 15, Color("#252720"), HORIZONTAL_ALIGNMENT_LEFT, "mission_preview_%d_name" % (index + 1))
		_add_label("%d天" % int(item["days"]), Rect2(popover_rect.position.x + 232.0 * DISPLAY_SCALE, row_y, 40.0 * DISPLAY_SCALE, 24.0 * DISPLAY_SCALE), 14, Color("#555a4d"), HORIZONTAL_ALIGNMENT_RIGHT, "mission_preview_%d_days" % (index + 1))
	_add_label("预览 %d 项 · 共 %d 项" % [rows.size(), int(_runtime_fixture["mission_preview_total"])], Rect2(popover_rect.position.x + 12.0 * DISPLAY_SCALE, popover_rect.end.y - 26.0 * DISPLAY_SCALE, popover_rect.size.x - 24.0 * DISPLAY_SCALE, 20.0 * DISPLAY_SCALE), 13, Color("#555a4d"), HORIZONTAL_ALIGNMENT_RIGHT, "mission_preview_footer")
	var connector_y := mission_rect.position.y + mission_rect.size.y * 0.5
	_add_divider(Rect2(popover_rect.end.x - 1.0, connector_y, DOSSIER_POS.x - popover_rect.end.x + 1.0, 2.0), Color("#3f6663"))
	_qa_rects["mission_preview_popover"] = popover_rect


func _slot_rect(name: String) -> Rect2:
	return _reference_rect(SLOTS[name])


func _reference_rect(rect: Rect2) -> Rect2:
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


func _add_photo_texture(texture: Texture2D, rect: Rect2) -> void:
	var node := TextureRect.new()
	node.texture = texture
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	node.position = rect.position
	node.size = rect.size
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


func _add_chevron(rect: Rect2, color: Color, expanded: bool) -> void:
	var chevron := Line2D.new()
	chevron.default_color = Color(color.r, color.g, color.b, 0.9)
	chevron.width = 2.25
	chevron.antialiased = true
	if expanded:
		chevron.add_point(rect.position + Vector2(rect.size.x * 0.20, rect.size.y * 0.64))
		chevron.add_point(rect.position + Vector2(rect.size.x * 0.50, rect.size.y * 0.36))
		chevron.add_point(rect.position + Vector2(rect.size.x * 0.80, rect.size.y * 0.64))
	else:
		chevron.add_point(rect.position + Vector2(rect.size.x * 0.20, rect.size.y * 0.36))
		chevron.add_point(rect.position + Vector2(rect.size.x * 0.50, rect.size.y * 0.64))
		chevron.add_point(rect.position + Vector2(rect.size.x * 0.80, rect.size.y * 0.36))
	_root_control.add_child(chevron)
	_qa_rects["mission_intel_chevron"] = rect


func _add_divider(rect: Rect2, color: Color) -> void:
	var divider := ColorRect.new()
	divider.color = color
	divider.position = rect.position
	divider.size = rect.size
	_root_control.add_child(divider)


func _add_label(text_value: String, rect: Rect2, font_size: int, color: Color, alignment: HorizontalAlignment, evidence_id: String) -> void:
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
	if evidence_id != "":
		_qa_rects[evidence_id] = rect


func _add_qa_overlays(expanded: bool) -> void:
	var slot_colors := {
		"header_icon": Color("#51eeff"),
		"title_slot": Color("#ff48ca"),
		"status_stamp": Color("#ff6f5f"),
		"photo_slot": Color("#48ecae"),
		"region_body": Color("#ffd444"),
		"mission_intel_button": Color("#4fdae8"),
		"primary_enter_cta": Color("#aecc5b"),
	}
	for name in slot_colors:
		_add_rect(_slot_rect(name), slot_colors[name], name)
	_add_rect(_reference_rect(REGION_BODY_INNER), Color("#65ff94"), "region_body_inner")
	_add_rect(_reference_rect(REGION_BODY_NO_TEXT), Color("#ff4b4b"), "no_text")
	for evidence_id in _qa_rects:
		var color := Color("#ff48ca") if evidence_id.contains("title") or evidence_id.contains("facts") or evidence_id.contains("body") else Color("#58edf4")
		_add_rect(_qa_rects[evidence_id], color, evidence_id)
	var axis := ColorRect.new()
	axis.color = Color("#65ff94")
	axis.position = Vector2(DOSSIER_POS.x, DOSSIER_POS.y + HEADER_AXIS_Y * DISPLAY_SCALE)
	axis.size = Vector2(DOSSIER_SIZE.x, 2.0)
	_root_control.add_child(axis)
	if expanded:
		_add_label("QA rects are generated from the same Rect2 values used by the runtime labels.", Rect2(690, 978, 990, 32), 16, Color("#f2ead0"), HORIZONTAL_ALIGNMENT_LEFT, "")


func _add_rect(rect: Rect2, color: Color, label_text: String) -> void:
	var box := ColorRect.new()
	box.color = Color(color.r, color.g, color.b, 0.06)
	box.position = rect.position
	box.size = rect.size
	_root_control.add_child(box)
	var line := ReferenceRect.new()
	line.position = rect.position
	line.size = rect.size
	line.border_color = color
	line.border_width = 2.0
	_root_control.add_child(line)
	var tag_rect := Rect2(rect.position + Vector2(3, 1), Vector2(minf(235.0, maxf(90.0, rect.size.x - 6.0)), 18.0))
	_add_label(label_text, tag_rect, 10, color, HORIZONTAL_ALIGNMENT_LEFT, "")


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
