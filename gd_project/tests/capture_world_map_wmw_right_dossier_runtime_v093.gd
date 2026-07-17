extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-24-world-map-benchmark-landing"
const FIXTURE_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v093_right_dossier_candidate_a3/right_dossier_candidate_a3_runtime_fixture.json"
const PARENT_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/right_dossier_page_candidate_a1_parent_hollow_shell_2x.png"
const MISSION_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v093_right_dossier_candidate_a3/ingredients/right_mission_intel_button_candidate_a3_disclosure_teal_2x.png"
const PRIMARY_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v093_right_dossier_candidate_a3/ingredients/right_action_lane_candidate_a3_primary_olive_2x.png"
const PHOTO_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/right_dossier_north_america_photo_552x352.png"
const GLOBE_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_globe.png"
const DOCUMENT_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_document.png"
const ARROW_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/runtime_icons/right_dossier_runtime_arrow.png"
const CHEVRON_ICON_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v093_right_dossier_candidate_a3/ingredients/runtime_icons/right_dossier_runtime_chevron_down.png"

const RUNTIME_SIZE := Vector2i(1920, 1080)
const DISPLAY_SCALE := 1.5
const DOSSIER_SIZE := Vector2(320.0, 520.0) * DISPLAY_SCALE
const DOSSIER_POS := Vector2(76.0, 150.0)
const PHOTO_SOURCE_SIZE := Vector2i(552, 352)
const PHOTO_RATIO := 69.0 / 44.0
const HEADER_AXIS_Y := 59.0
const HEADER_ICON_OFFSET_Y := 3.0
const STATUS_GROUP_OFFSET_Y := -4.0
const REGION_BODY_INNER := Rect2(34.0, 290.0, 252.0, 50.0)
const REGION_BODY_NO_TEXT := Rect2(22.0, 288.0, 4.0, 54.0)

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
var _chevron_icon: Texture2D
var _baseline_image: Image
var _baseline_right_panel_bright_pixels := 0
var _runtime_fixture: Dictionary


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	if not _load_runtime_fixture():
		quit(1)
		return
	_parent_texture = _load_texture(PARENT_PATH)
	_mission_texture = _load_texture(MISSION_PATH)
	_primary_texture = _load_texture(PRIMARY_PATH)
	_photo_texture = _load_texture(PHOTO_PATH)
	_globe_icon = _load_texture(GLOBE_ICON_PATH)
	_document_icon = _load_texture(DOCUMENT_ICON_PATH)
	_arrow_icon = _load_texture(ARROW_ICON_PATH)
	_chevron_icon = _load_texture(CHEVRON_ICON_PATH)
	if _parent_texture == null or _mission_texture == null or _primary_texture == null or _photo_texture == null or _globe_icon == null or _document_icon == null or _arrow_icon == null or _chevron_icon == null:
		quit(1)
		return
	if _mission_texture.get_size() != Vector2(568, 88) or _primary_texture.get_size() != Vector2(568, 100):
		push_error("A3 action child master dimensions drifted")
		quit(1)
		return
	if not _validate_photo_contract():
		quit(1)
		return
	var ok := true
	ok = await _capture(false, "608-world-map-wmw-v0-9-3-right-dossier-candidate-a3-godot-runtime.png") and ok
	ok = await _capture(true, "609-world-map-wmw-v0-9-3-right-dossier-candidate-a3-godot-runtime-qa.png") and ok
	if not ok:
		push_error("Godot v0.9.3 right-dossier candidate A3 capture failed.")
		quit(1)
		return
	print("capture_world_map_wmw_right_dossier_runtime_v093.gd OK")
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
		"decision_facts",
		"mission_intel_label",
		"mission_intel_expanded_label",
		"primary_enter_label",
	]
	for key in required:
		if not _runtime_fixture.has(key) or str(_runtime_fixture[key]).strip_edges() == "":
			push_error("Runtime fixture is missing visible field: " + key)
			return false
	if str(_runtime_fixture.get("provenance", "")) != "production_runtime_export" or _runtime_fixture.get("generated_from_production_data", false) != true:
		push_error("Runtime fixture provenance is not production data")
		return false
	if str(_runtime_fixture["status_display_text"]).contains("\n"):
		push_error("A3 status must remain a single semantic line")
		return false
	if str(_runtime_fixture["mission_intel_label"]) != "展开任务情报" or str(_runtime_fixture["mission_intel_expanded_label"]) != "收起任务情报":
		push_error("A207 disclosure copy drifted")
		return false
	if str(_runtime_fixture["mission_intel_label"]).contains("项"):
		push_error("Mission count leaked into A3 disclosure copy")
		return false
	if _runtime_fixture.has("recommendation"):
		push_error("Region-level recommendation is retired by A205")
		return false
	print("runtime_fixture provenance=production_runtime_export region=%s" % str(_runtime_fixture.get("region_id", "")))
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
		push_error("A1 photo ingredient must be exactly %s, got %s" % [PHOTO_SOURCE_SIZE, actual_size])
		return false
	var actual_ratio := float(actual_size.x) / float(actual_size.y)
	var ratio_error := absf(actual_ratio - PHOTO_RATIO) / PHOTO_RATIO
	if ratio_error > 0.005:
		push_error("A1 photo aspect ratio error %.6f exceeds 0.5%%" % ratio_error)
		return false
	var slot: Rect2 = SLOTS["photo_slot"]
	var slot_ratio := slot.size.x / slot.size.y
	if absf(slot_ratio - PHOTO_RATIO) / PHOTO_RATIO > 0.005:
		push_error("Runtime photo_slot ratio no longer matches locked 69:44 input")
		return false
	print("photo_contract size=%s ratio_error=%.6f stretch=KEEP_ASPECT_COVERED" % [actual_size, ratio_error])
	return true


func _capture(show_qa: bool, file_name: String) -> bool:
	if _viewport == null:
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
	elif not show_qa:
		push_error("Capture scene already exists before baseline capture")
		return false
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
		var right_panel_bright_pixels := _count_right_panel_bright_pixels(image)
		if _baseline_right_panel_bright_pixels < 100 or right_panel_bright_pixels < int(_baseline_right_panel_bright_pixels * 0.85):
			push_error("QA right panel content loss: baseline=%d qa=%d for %s." % [_baseline_right_panel_bright_pixels, right_panel_bright_pixels, file_name])
			return false
	else:
		_baseline_image = image.duplicate()
		_baseline_right_panel_bright_pixels = _count_right_panel_bright_pixels(image)
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


func _count_right_panel_bright_pixels(image: Image) -> int:
	var count := 0
	for y in range(40, 900, 4):
		for x in range(650, 1820, 4):
			var color := image.get_pixel(x, y)
			if maxf(color.r, maxf(color.g, color.b)) > 0.32:
				count += 1
	return count


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

	_add_label("Godot 4.6.2 · WMW right dossier candidate A3", Rect2(660, 56, 1160, 48), 31, Color("#f2ead0"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("A207: in-place disclosure vs sole cross-layer navigation; one row, one command, one hit rect.", Rect2(662, 106, 1120, 34), 18, Color("#c8d7c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("SEMANTIC OWNERSHIP", Rect2(710, 230, 360, 34), 21, Color("#65ff94"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("Title names the region; stamp reports current state; body/facts explain the decision. No stress-fixture copy remains.", Rect2(710, 270, 940, 70), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("PRODUCTION FIXTURE", Rect2(710, 390, 280, 34), 21, Color("#ffd444"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("WeeklyRunContent + WeeklyRunSystems export one JSON consumed by Python and Godot. Screenshot values are validated against it.", Rect2(710, 430, 940, 86), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("ACTION GRAMMAR", Rect2(710, 585, 250, 34), 20, Color("#48ecae"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("Disclosure: document + chevron. Navigation: label + arrow. Old rings and central plates are retired.", Rect2(710, 625, 930, 70), 19, Color("#dfe2c8"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label("A1 shell, exact 69:44 placeholder photo, optical axis and safe inset are reused without changing frozen geometry.", Rect2(710, 755, 930, 70), 18, Color("#c8d7c8"), HORIZONTAL_ALIGNMENT_LEFT)


func _add_dossier() -> void:
	var photo_rect := _slot_rect("photo_slot")
	_add_photo_texture(_photo_texture, photo_rect)
	_add_texture(_parent_texture, DOSSIER_POS, DOSSIER_SIZE)

	var mission_rect := _slot_rect("mission_intel_button")
	var primary_rect := _slot_rect("primary_enter_cta")
	_add_texture(_mission_texture, mission_rect.position, mission_rect.size)
	_add_texture(_primary_texture, primary_rect.position, primary_rect.size)

	var header_icon_rect := _slot_rect("header_icon")
	header_icon_rect.position.y += HEADER_ICON_OFFSET_Y * DISPLAY_SCALE
	_add_icon(_globe_icon, header_icon_rect, Color("#5d604e"), 0.86)
	_add_label(str(_runtime_fixture["region_title"]), _slot_rect("title_slot"), 27, Color("#1c1e19"), HORIZONTAL_ALIGNMENT_CENTER)
	var status := _slot_rect("status_stamp")
	status.position.y += STATUS_GROUP_OFFSET_Y * DISPLAY_SCALE
	_add_label(str(_runtime_fixture["status_display_text"]), status, 15, Color("#8e3627"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_label(str(_runtime_fixture["region_body_text"]), _reference_rect(REGION_BODY_INNER), 16, Color("#22251f"), HORIZONTAL_ALIGNMENT_LEFT)
	_add_label(str(_runtime_fixture["decision_facts"]), _slot_rect("decision_facts"), 16, Color("#3e4438"), HORIZONTAL_ALIGNMENT_CENTER)

	var mission_left := _child_slot_rect(mission_rect, MISSION_SLOTS["left_icon_zone"])
	var mission_label := _child_slot_rect(mission_rect, MISSION_SLOTS["label_plate"])
	var mission_right := _child_slot_rect(mission_rect, MISSION_SLOTS["right_action_badge"])
	_add_icon(_document_icon, mission_left, Color("#eee5c9"), 0.72)
	_add_label(str(_runtime_fixture["mission_intel_label"]), mission_label, 18, Color("#eee5c9"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_icon(_chevron_icon, mission_right, Color("#eee5c9"), 0.62)

	var primary_label := _child_slot_rect(primary_rect, PRIMARY_SLOTS["label_plate"])
	var primary_right := _child_slot_rect(primary_rect, PRIMARY_SLOTS["right_action_badge"])
	_add_label(str(_runtime_fixture["primary_enter_label"]), primary_label, 20, Color("#eee5c9"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_icon(_arrow_icon, primary_right, Color("#eee5c9"), 0.72)


func _slot_rect(name: String) -> Rect2:
	var rect: Rect2 = SLOTS[name]
	return _reference_rect(rect)


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
	var mission_rect := _slot_rect("mission_intel_button")
	var primary_rect := _slot_rect("primary_enter_cta")
	_add_rect(_child_slot_rect(mission_rect, MISSION_SLOTS["left_icon_zone"]), Color("#58edf4"), "doc")
	_add_rect(_child_slot_rect(mission_rect, MISSION_SLOTS["label_plate"]), Color("#ff48ca"), "disclosure_label")
	_add_rect(_child_slot_rect(mission_rect, MISSION_SLOTS["right_action_badge"]), Color("#58edf4"), "chevron")
	_add_rect(_child_slot_rect(primary_rect, PRIMARY_SLOTS["label_plate"]), Color("#ff48ca"), "navigation_label")
	_add_rect(_child_slot_rect(primary_rect, PRIMARY_SLOTS["right_action_badge"]), Color("#aecc5b"), "arrow")
	_add_rect(_reference_rect(REGION_BODY_INNER), Color("#65ff94"), "region_body_inner")
	_add_rect(_reference_rect(REGION_BODY_NO_TEXT), Color("#ff4b4b"), "no_text")
	var axis := ColorRect.new()
	axis.color = Color("#65ff94")
	axis.position = Vector2(DOSSIER_POS.x, DOSSIER_POS.y + HEADER_AXIS_Y * DISPLAY_SCALE)
	axis.size = Vector2(DOSSIER_SIZE.x, 2.0)
	_root_control.add_child(axis)


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
