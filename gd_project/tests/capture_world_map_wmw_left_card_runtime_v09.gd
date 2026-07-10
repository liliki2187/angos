extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-24-world-map-benchmark-landing"
const ATLAS_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b28_state_badge_globe_fix_atlas_2x.png"
const ICON_PATHS := [
	"res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b28_runtime_icon_selected.png",
	"res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b28_runtime_icon_available.png",
	"res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b28_runtime_icon_warning.png",
	"res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b28_runtime_icon_locked.png",
]

const RUNTIME_SIZE := Vector2i(1920, 1080)
const DISPLAY_SCALE := 1.5
const FRAME_SIZE := Vector2i(408, 320)
const CARD_SIZE := Vector2(204.0, 160.0) * DISPLAY_SCALE
const POSITIONS := [
	Vector2(44.0, 24.0) * DISPLAY_SCALE,
	Vector2(44.0, 196.0) * DISPLAY_SCALE,
	Vector2(44.0, 368.0) * DISPLAY_SCALE,
	Vector2(44.0, 540.0) * DISPLAY_SCALE,
]
const LABEL_PLATE := Rect2(Vector2(22.0, 104.0) * DISPLAY_SCALE, Vector2(114.0, 32.0) * DISPLAY_SCALE)
const META_LINE := Rect2(Vector2(22.0, 138.0) * DISPLAY_SCALE, Vector2(96.0, 10.0) * DISPLAY_SCALE)
const PHOTO_SLOT := Rect2(Vector2(21.0, 24.0) * DISPLAY_SCALE, Vector2(174.0, 64.0) * DISPLAY_SCALE)
const ACTION_BADGE := Rect2(Vector2(144.0, 101.0) * DISPLAY_SCALE, Vector2(44.0, 44.0) * DISPLAY_SCALE)
const LABEL_TITLE_FONT_SIZE := 25
const LABEL_TITLE_COLOR := Color("#121612")
const META_STATUS_FONT_SIZE := 14
const META_STATUS_COLOR := Color("#421c14")

const COPY := [
	{"title": "北美禁区带", "meta": "红线升温  推荐2"},
	{"title": "欧洲灰域", "meta": "可派遣  线报2"},
	{"title": "非洲禁区带", "meta": "异常升温  高危"},
	{"title": "南美禁区带", "meta": "锁定  需3线报"},
]

var _viewport: SubViewport
var _root_control: Control
var _atlas_image: Image
var _icon_textures: Array[Texture2D] = []
var _baseline_image: Image

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	_atlas_image = Image.load_from_file(ProjectSettings.globalize_path(ATLAS_PATH))
	if _atlas_image == null:
		push_error("Missing atlas: " + ATLAS_PATH)
		quit(1)
		return
	for icon_path in ICON_PATHS:
		var icon_image := Image.load_from_file(ProjectSettings.globalize_path(icon_path))
		if icon_image == null:
			push_error("Missing runtime badge icon: " + icon_path)
			quit(1)
			return
		_icon_textures.append(ImageTexture.create_from_image(icon_image))

	var ok := true
	ok = await _capture(false, "517-world-map-wmw-v0-9-14-left-card-b2-8-godot-single-component.png") and ok
	ok = await _capture(true, "518-world-map-wmw-v0-9-14-left-card-b2-8-godot-single-component-qa.png") and ok
	if not ok:
		push_error("Godot v0.9.14 B2.8 left-card capture failed to save one or more screenshots.")
		quit(1)
		return
	print("capture_world_map_wmw_left_card_runtime_v09.gd OK")
	quit(0)

func _capture(show_qa: bool, file_name: String) -> bool:
	# Each proof image gets its own viewport. Reusing a viewport can produce a
	# partial dirty-region redraw after the render target is cleared.
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
	# process_frame alone can fire before the render target is drawn, yielding
	# an all-black capture. The windowed runner must wait for a real draw pass.
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
		push_error("Captured image is all black for %s; render pass did not reach the SubViewport." % file_name)
		return false
	if is_qa:
		var missing_baseline_pixels := _count_qa_missing_baseline_pixels(image)
		if missing_baseline_pixels > 20:
			push_error("QA capture lost %d sampled baseline pixels for %s; refusing a partial draw." % [missing_baseline_pixels, file_name])
			return false
	else:
		_baseline_image = image.duplicate()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
	return true

func _is_all_black(image: Image) -> bool:
	for y in range(0, image.get_height(), 90):
		for x in range(0, image.get_width(), 160):
			var c := image.get_pixel(x, y)
			if c.r > 0.005 or c.g > 0.005 or c.b > 0.005:
				return false
	return true

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
			if before_peak > 0.08 and after_peak < 0.01:
				missing += 1
	return missing

func _build_scene() -> void:
	var bg := ColorRect.new()
	bg.color = Color("#071315")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root_control.add_child(bg)

	var panel := ColorRect.new()
	panel.color = Color(0.015, 0.045, 0.052, 1.0)
	panel.position = Vector2(42, 26)
	panel.size = Vector2(382, 1030)
	_root_control.add_child(panel)

	for i in range(4):
		_add_card(i, POSITIONS[i])

	var note := Label.new()
	note.text = "Godot v0.9.14 B2.8 left_region_card state badge + clean globe/photo"
	note.position = Vector2(450, 34)
	note.size = Vector2(1100, 40)
	note.add_theme_font_size_override("font_size", 28)
	note.add_theme_color_override("font_color", Color("#f3efd6"))
	_root_control.add_child(note)

	var sub := Label.new()
	sub.text = "Badge position follows the accepted benchmark rhythm; clean globe/photo ingredients and complete state icon are separate layers."
	sub.position = Vector2(450, 76)
	sub.size = Vector2(1200, 42)
	sub.add_theme_font_size_override("font_size", 18)
	sub.add_theme_color_override("font_color", Color("#d9dec7"))
	_root_control.add_child(sub)

func _add_card(index: int, pos: Vector2) -> void:
	var frame := _atlas_image.get_region(Rect2i(Vector2i(index * FRAME_SIZE.x, 0), FRAME_SIZE))
	var texture := ImageTexture.create_from_image(frame)
	var tex := TextureRect.new()
	tex.texture = texture
	tex.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tex.stretch_mode = TextureRect.STRETCH_SCALE
	tex.position = pos
	tex.size = CARD_SIZE
	_root_control.add_child(tex)

	var title := Label.new()
	title.text = COPY[index]["title"]
	title.position = pos + LABEL_PLATE.position + Vector2(12, 5)
	title.size = LABEL_PLATE.size - Vector2(18, 8)
	title.add_theme_font_size_override("font_size", LABEL_TITLE_FONT_SIZE)
	title.add_theme_color_override("font_color", LABEL_TITLE_COLOR)
	_root_control.add_child(title)

	var meta := Label.new()
	meta.text = COPY[index]["meta"]
	meta.position = pos + META_LINE.position + Vector2(5, -2)
	meta.size = META_LINE.size
	meta.add_theme_font_size_override("font_size", META_STATUS_FONT_SIZE)
	meta.add_theme_color_override("font_color", META_STATUS_COLOR)
	_root_control.add_child(meta)

	_add_runtime_icon(index, pos)


func _add_qa_overlays() -> void:
	for pos in POSITIONS:
		_add_rect(pos, CARD_SIZE, Color("#65ff8a"), "export")
		_add_rect(pos + PHOTO_SLOT.position, PHOTO_SLOT.size, Color("#58e9ff"), "photo")
		_add_rect(pos + LABEL_PLATE.position, LABEL_PLATE.size, Color("#ffe55d"), "label")
		_add_rect(pos + META_LINE.position, META_LINE.size, Color("#ff9f52"), "meta")
		_add_rect(pos + ACTION_BADGE.position, ACTION_BADGE.size, Color("#ff6969"), "action")

func _add_runtime_icon(index: int, pos: Vector2) -> void:
	var texture := _icon_textures[index]
	var icon := TextureRect.new()
	icon.texture = texture
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_SCALE
	var icon_size := Vector2(float(texture.get_width()), float(texture.get_height())) * (DISPLAY_SCALE / 2.0)
	icon.position = pos + ACTION_BADGE.position + ACTION_BADGE.size * 0.5 - icon_size * 0.5
	icon.size = icon_size
	_root_control.add_child(icon)

func _add_rect(pos: Vector2, size: Vector2, color: Color, label: String) -> void:
	var box := ColorRect.new()
	box.color = Color(color.r, color.g, color.b, 0.10)
	box.position = pos
	box.size = size
	_root_control.add_child(box)
	var line := ReferenceRect.new()
	line.position = pos
	line.size = size
	line.border_color = color
	line.border_width = 2.0
	_root_control.add_child(line)
	var tag := Label.new()
	tag.text = label
	tag.position = pos + Vector2(4, 1)
	tag.size = Vector2(160, 22)
	tag.add_theme_font_size_override("font_size", 12)
	tag.add_theme_color_override("font_color", color)
	_root_control.add_child(tag)

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame
