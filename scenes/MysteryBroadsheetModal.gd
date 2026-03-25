extends Control

const PAGE_TEXTURE := preload("res://design/generated-settlement-reference/2026-03-18/output/06-mystery-broadsheet-reference.png")
const WARNING_SHADER := preload("res://scenes/mystery_broadsheet/WarningPulse.gdshader")
const VIDEO_SHADER := preload("res://scenes/mystery_broadsheet/VideoGlitch.gdshader")
const EXPLOSION_OVERLAY_SCRIPT := preload("res://scenes/mystery_broadsheet/MysteryExplosionOverlay.gd")

const PAGE_SIZE := Vector2(1240.0, 2520.0)
const WARNING_IMAGE_RECT := Rect2(18.0, 500.0, 342.0, 234.0)
const WARNING_TEXT_RECT := Rect2(18.0, 275.0, 338.0, 220.0)
const HERO_RECT := Rect2(680.0, 255.0, 525.0, 1455.0)
const VIDEO_RECT := Rect2(44.0, 2070.0, 648.0, 375.0)
const PAPER_TINT := Color(0.95, 0.9, 0.83, 0.08)
const WARNING_HEADLINE := "如果 51 区空车\n再次出现\n不要独自追车"
const PIECE_REGIONS := [
	Rect2(0.0, 0.0, 770.0, 240.0),
	Rect2(770.0, 0.0, 470.0, 240.0),
	Rect2(0.0, 240.0, 375.0, 1510.0),
	Rect2(375.0, 240.0, 305.0, 1510.0),
	Rect2(680.0, 240.0, 560.0, 1510.0),
	Rect2(0.0, 1750.0, 730.0, 770.0),
	Rect2(730.0, 1750.0, 510.0, 770.0),
]

signal closed

var _scrim: ColorRect
var _shell: Control
var _shadow: Panel
var _stage: Control
var _page: TextureRect
var _warning_area: Control
var _warning_crop: TextureRect
var _warning_text_holder: Control
var _warning_text: RichTextLabel
var _hero_area: Control
var _hero_crop: TextureRect
var _video_area: Control
var _video_ghost_a: TextureRect
var _video_ghost_b: TextureRect
var _video_crop: TextureRect
var _piece_layer: Control
var _piece_nodes: Array = []
var _explosion_overlay: Control

var _warning_material: ShaderMaterial
var _video_material: ShaderMaterial

var _base_scale := 0.2
var _shell_scale := 0.2:
	set(value):
		_shell_scale = value
		if is_instance_valid(_shell):
			_shell.scale = Vector2.ONE * _shell_scale
			_sync_shell_position()

var _warning_time := 0.0
var _warning_tick := 0.0
var _warning_char_index := 0
var _warning_glyph_count := 0

var _hero_hovered := false
var _video_has_been_hovered := false
var _video_target_weirdness := 0.0
var _video_weirdness := 0.0
var _closing := false


func _ready() -> void:
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	_build_modal()
	_warning_glyph_count = _count_visible_glyphs(WARNING_HEADLINE)
	_refresh_warning_text()
	resized.connect(_layout_modal)
	_layout_modal()


func open_modal() -> void:
	if visible and not _closing:
		return

	_reset_modal_state()
	visible = true
	set_process(true)
	_shell.modulate.a = 0.0
	_scrim.color = Color(0.03, 0.02, 0.03, 0.0)
	_shell_scale = _base_scale * 0.94

	var tween := create_tween().set_parallel(true)
	tween.tween_property(_scrim, "color:a", 0.72, 0.22)
	tween.tween_property(_shell, "modulate:a", 1.0, 0.22)
	tween.tween_property(self, "_shell_scale", _base_scale, 0.28).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _unhandled_input(event: InputEvent) -> void:
	if not visible or _closing:
		return

	if event.is_action_pressed("ui_cancel"):
		_start_close_sequence()
		get_viewport().set_input_as_handled()


func _process(delta: float) -> void:
	if not visible:
		return

	_warning_time += delta
	_warning_tick += delta
	if _warning_tick >= 0.12:
		_warning_tick = 0.0
		_warning_char_index = (_warning_char_index + 1) % max(_warning_glyph_count, 1)
		_refresh_warning_text()

	var warning_pulse := pow(sin(_warning_time * 1.45) * 0.5 + 0.5, 1.4)
	var ghost_strength := clampf(0.12 + warning_pulse * 0.44 + absf(sin(_warning_time * 6.2)) * 0.08, 0.0, 1.0)
	_warning_material.set_shader_parameter("gray_amount", 0.18 + warning_pulse * 0.58)
	_warning_material.set_shader_parameter("ghost_strength", ghost_strength)
	_warning_area.position = WARNING_IMAGE_RECT.position + Vector2(sin(_warning_time * 14.0) * 1.3, cos(_warning_time * 11.5) * 0.9)
	_warning_area.rotation = deg_to_rad(sin(_warning_time * 3.8) * 0.7)
	_warning_text_holder.position = WARNING_TEXT_RECT.position + Vector2(sin(_warning_time * 9.8) * 0.9, cos(_warning_time * 13.2) * 0.7)

	if _hero_hovered:
		_hero_crop.position = Vector2(randf_range(-6.0, 6.0), randf_range(-8.0, 8.0))
		_hero_crop.rotation = deg_to_rad(randf_range(-1.8, 1.8))
	else:
		_hero_crop.position = _hero_crop.position.lerp(Vector2.ZERO, minf(1.0, delta * 18.0))
		_hero_crop.rotation = lerpf(_hero_crop.rotation, 0.0, minf(1.0, delta * 16.0))

	var decay_speed := 5.5 if _video_target_weirdness > _video_weirdness else 11.5
	_video_weirdness = move_toward(_video_weirdness, _video_target_weirdness, delta * decay_speed)
	_video_material.set_shader_parameter("weirdness", _video_weirdness)

	_video_ghost_a.visible = _video_weirdness > 0.02
	_video_ghost_b.visible = _video_weirdness > 0.05
	_video_ghost_a.position = Vector2(-18.0, 8.0) * _video_weirdness
	_video_ghost_b.position = Vector2(15.0, -10.0) * _video_weirdness
	_video_ghost_a.modulate = Color(0.76, 0.14, 0.14, 0.24 * _video_weirdness)
	_video_ghost_b.modulate = Color(0.1, 0.62, 0.68, 0.22 * _video_weirdness)
	_video_crop.position = Vector2(sin(_warning_time * 21.0), cos(_warning_time * 17.0)) * 6.0 * _video_weirdness
	_video_crop.rotation = deg_to_rad(sin(_warning_time * 8.5) * 1.8 * _video_weirdness)
	_video_area.rotation = deg_to_rad(sin(_warning_time * 4.6) * 3.4 * _video_weirdness)
	_video_area.scale = Vector2.ONE * (1.0 + 0.02 * _video_weirdness)


func _build_modal() -> void:
	_scrim = ColorRect.new()
	_scrim.color = Color(0.03, 0.02, 0.03, 0.0)
	_scrim.mouse_filter = Control.MOUSE_FILTER_STOP
	_fill_rect(_scrim)
	_scrim.gui_input.connect(_on_scrim_input)
	add_child(_scrim)

	_shell = Control.new()
	_shell.size = PAGE_SIZE
	_shell.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_shell)

	_shadow = Panel.new()
	_shadow.size = PAGE_SIZE
	_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_shadow.add_theme_stylebox_override("panel", _make_shadow_style())
	_shell.add_child(_shadow)

	_stage = Control.new()
	_stage.size = PAGE_SIZE
	_stage.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_shell.add_child(_stage)

	_page = TextureRect.new()
	_page.texture = PAGE_TEXTURE
	_page.position = Vector2.ZERO
	_page.size = PAGE_SIZE
	_page.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_page.stretch_mode = TextureRect.STRETCH_SCALE
	_page.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_page)

	_warning_material = ShaderMaterial.new()
	_warning_material.shader = WARNING_SHADER
	_warning_material.set_shader_parameter("gray_amount", 0.2)
	_warning_material.set_shader_parameter("ghost_strength", 0.18)

	_warning_area = _make_region_holder(WARNING_IMAGE_RECT)
	_stage.add_child(_warning_area)
	_warning_crop = _make_crop_texture(WARNING_IMAGE_RECT, _warning_material)
	_warning_area.add_child(_warning_crop)

	_warning_text_holder = _make_region_holder(WARNING_TEXT_RECT)
	_warning_text_holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_warning_text_holder)

	var warning_mask := ColorRect.new()
	warning_mask.color = PAPER_TINT
	_fill_rect(warning_mask)
	warning_mask.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_warning_text_holder.add_child(warning_mask)

	_warning_text = RichTextLabel.new()
	_warning_text.bbcode_enabled = true
	_warning_text.fit_content = true
	_warning_text.scroll_active = false
	_warning_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_warning_text.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_warning_text.size = WARNING_TEXT_RECT.size
	_warning_text.add_theme_font_size_override("normal_font_size", 74)
	_warning_text_holder.add_child(_warning_text)

	_hero_area = _make_region_holder(HERO_RECT)
	_hero_area.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_hero_area.mouse_entered.connect(func() -> void: _hero_hovered = true)
	_hero_area.mouse_exited.connect(_on_hero_exited)
	_stage.add_child(_hero_area)
	_hero_crop = _make_crop_texture(HERO_RECT)
	_hero_area.add_child(_hero_crop)

	_video_material = ShaderMaterial.new()
	_video_material.shader = VIDEO_SHADER
	_video_material.set_shader_parameter("weirdness", 0.0)

	_video_area = _make_region_holder(VIDEO_RECT)
	_video_area.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_video_area.mouse_entered.connect(_on_video_entered)
	_video_area.mouse_exited.connect(_on_video_exited)
	_stage.add_child(_video_area)

	_video_ghost_a = _make_crop_texture(VIDEO_RECT)
	_video_ghost_a.visible = false
	_video_ghost_a.modulate = Color(0.76, 0.14, 0.14, 0.0)
	_video_area.add_child(_video_ghost_a)

	_video_ghost_b = _make_crop_texture(VIDEO_RECT)
	_video_ghost_b.visible = false
	_video_ghost_b.modulate = Color(0.1, 0.62, 0.68, 0.0)
	_video_area.add_child(_video_ghost_b)

	_video_crop = _make_crop_texture(VIDEO_RECT, _video_material)
	_video_area.add_child(_video_crop)

	_piece_layer = Control.new()
	_piece_layer.size = PAGE_SIZE
	_piece_layer.visible = false
	_piece_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_piece_layer)
	_build_piece_layer()

	_explosion_overlay = Control.new()
	_explosion_overlay.set_script(EXPLOSION_OVERLAY_SCRIPT)
	_explosion_overlay.visible = false
	_explosion_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_explosion_overlay.size = PAGE_SIZE
	_stage.add_child(_explosion_overlay)


func _make_region_holder(region: Rect2) -> Control:
	var holder := Control.new()
	holder.position = region.position
	holder.size = region.size
	holder.clip_contents = false
	holder.mouse_filter = Control.MOUSE_FILTER_STOP
	return holder


func _make_crop_texture(region: Rect2, material: Material = null) -> TextureRect:
	var texture := TextureRect.new()
	texture.texture = _make_region_texture(region)
	texture.position = Vector2.ZERO
	texture.size = region.size
	texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	texture.stretch_mode = TextureRect.STRETCH_SCALE
	texture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if material != null:
		texture.material = material
	return texture


func _make_region_texture(region: Rect2) -> AtlasTexture:
	var atlas := AtlasTexture.new()
	atlas.atlas = PAGE_TEXTURE
	atlas.region = region
	return atlas


func _build_piece_layer() -> void:
	for region in PIECE_REGIONS:
		var piece := TextureRect.new()
		piece.texture = _make_region_texture(region)
		piece.position = region.position
		piece.size = region.size
		piece.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		piece.stretch_mode = TextureRect.STRETCH_SCALE
		piece.mouse_filter = Control.MOUSE_FILTER_IGNORE
		piece.pivot_offset = region.size * 0.5
		piece.visible = false
		piece.set_meta("base_position", region.position)
		_piece_layer.add_child(piece)
		_piece_nodes.append(piece)


func _make_shadow_style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(1.0, 0.98, 0.94, 0.04)
	style.set_border_width_all(2)
	style.border_color = Color(0.32, 0.23, 0.17, 0.22)
	style.shadow_color = Color(0.04, 0.01, 0.01, 0.36)
	style.shadow_size = 52
	style.corner_radius_top_left = 10
	style.corner_radius_top_right = 10
	style.corner_radius_bottom_left = 10
	style.corner_radius_bottom_right = 10
	return style


func _layout_modal() -> void:
	if not is_instance_valid(_shell):
		return

	var usable := size - Vector2(180.0, 56.0)
	usable.x = maxf(usable.x, 220.0)
	usable.y = maxf(usable.y, 320.0)
	_base_scale = minf(usable.x / PAGE_SIZE.x, usable.y / PAGE_SIZE.y)
	_base_scale = clampf(_base_scale, 0.16, 1.0)
	if visible and not _closing:
		_shell_scale = _base_scale
	else:
		_sync_shell_position()


func _sync_shell_position() -> void:
	_shell.position = (size - PAGE_SIZE * _shell.scale) * 0.5


func _on_scrim_input(event: InputEvent) -> void:
	if _closing:
		return

	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_start_close_sequence()


func _on_hero_exited() -> void:
	_hero_hovered = false


func _on_video_entered() -> void:
	_video_has_been_hovered = true
	_video_target_weirdness = 0.0


func _on_video_exited() -> void:
	if _video_has_been_hovered and not _closing:
		_video_target_weirdness = 1.0


func _refresh_warning_text() -> void:
	var bbcode := "[font_size=74][color=#b94739]"
	var glyph_index := 0
	for character in WARNING_HEADLINE:
		if character == "\n":
			bbcode += "\n"
			continue
		if character == " ":
			bbcode += " "
			continue

		if glyph_index == _warning_char_index:
			bbcode += "[shake rate=32 level=16 connected=1][wave amp=24 freq=5.2]%s[/wave][/shake]" % character
		else:
			bbcode += character
		glyph_index += 1
	bbcode += "[/color][/font_size]"
	_warning_text.clear()
	_warning_text.append_text(bbcode)


func _count_visible_glyphs(text: String) -> int:
	var count := 0
	for character in text:
		if character != "\n" and character != " ":
			count += 1
	return count


func _start_close_sequence() -> void:
	if _closing or not visible:
		return

	_closing = true
	_piece_layer.visible = true
	_explosion_overlay.visible = true
	_explosion_overlay.set("progress", 0.0)

	for piece in _piece_nodes:
		piece.visible = true
		piece.modulate = Color(1.0, 1.0, 1.0, 1.0)
		piece.rotation = 0.0
		piece.position = piece.get_meta("base_position")

	_page.modulate = Color.WHITE

	var flash_tween := create_tween().set_parallel(true)
	flash_tween.tween_property(_page, "modulate:a", 0.14, 0.18)
	flash_tween.tween_property(_explosion_overlay, "progress", 1.0, 0.74).set_trans(Tween.TRANS_QUART).set_ease(Tween.EASE_OUT)
	flash_tween.tween_property(_scrim, "color:a", 0.82, 0.12)

	for piece_variant in _piece_nodes:
		var piece: TextureRect = piece_variant
		var base_position: Vector2 = piece.get_meta("base_position")
		var piece_center: Vector2 = base_position + piece.size * 0.5
		var direction: Vector2 = (piece_center - PAGE_SIZE * 0.5).normalized()
		if direction == Vector2.ZERO:
			direction = Vector2.RIGHT.rotated(randf() * TAU)

		var offset: Vector2 = direction * randf_range(48.0, 128.0) + Vector2(randf_range(-36.0, 36.0), randf_range(-26.0, 26.0))
		var target_position: Vector2 = base_position + offset
		var target_rotation := deg_to_rad(randf_range(-18.0, 18.0))
		var target_scale := Vector2.ONE * randf_range(0.96, 1.06)

		var piece_tween := create_tween().set_parallel(true)
		piece_tween.tween_property(piece, "position", target_position, 0.68).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT).set_delay(randf_range(0.01, 0.12))
		piece_tween.tween_property(piece, "rotation", target_rotation, 0.68).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT).set_delay(randf_range(0.01, 0.1))
		piece_tween.tween_property(piece, "scale", target_scale, 0.68).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT).set_delay(randf_range(0.01, 0.08))

	await get_tree().create_timer(0.86).timeout
	_finish_close_sequence()


func _finish_close_sequence() -> void:
	_reset_modal_state()
	visible = false
	set_process(false)
	emit_signal("closed")


func _reset_modal_state() -> void:
	_closing = false
	_hero_hovered = false
	_video_has_been_hovered = false
	_video_target_weirdness = 0.0
	_video_weirdness = 0.0
	_warning_tick = 0.0
	_warning_time = 0.0
	_warning_char_index = 0
	_refresh_warning_text()

	_scrim.mouse_filter = Control.MOUSE_FILTER_STOP
	_scrim.color = Color(0.03, 0.02, 0.03, 0.0)
	_page.modulate = Color.WHITE

	_warning_area.position = WARNING_IMAGE_RECT.position
	_warning_area.rotation = 0.0
	_warning_text_holder.position = WARNING_TEXT_RECT.position

	_hero_crop.position = Vector2.ZERO
	_hero_crop.rotation = 0.0

	_video_crop.position = Vector2.ZERO
	_video_crop.rotation = 0.0
	_video_area.rotation = 0.0
	_video_area.scale = Vector2.ONE
	_video_ghost_a.visible = false
	_video_ghost_b.visible = false

	_warning_material.set_shader_parameter("gray_amount", 0.2)
	_warning_material.set_shader_parameter("ghost_strength", 0.18)
	_video_material.set_shader_parameter("weirdness", 0.0)

	_piece_layer.visible = false
	for piece in _piece_nodes:
		piece.visible = false
		piece.scale = Vector2.ONE
		piece.rotation = 0.0
		piece.position = piece.get_meta("base_position")

	_explosion_overlay.visible = false
	_explosion_overlay.set("progress", 0.0)
	_layout_modal()


func _fill_rect(control: Control) -> void:
	control.anchor_left = 0.0
	control.anchor_top = 0.0
	control.anchor_right = 1.0
	control.anchor_bottom = 1.0
	control.offset_left = 0.0
	control.offset_top = 0.0
	control.offset_right = 0.0
	control.offset_bottom = 0.0
