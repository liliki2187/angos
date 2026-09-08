extends Control

const INK := Color("26312d")
const UFO_NOTE_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/ufo_note_228x256.png")
const THREE_WINDOW_EVENT_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/three_window_event_224x84.png")

var _font: Font
var _ufo_note: TextureRect
var _event_plate: TextureRect


func configure(font: Font) -> void:
	_font = font
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_build_ufo_note()
	_build_event_plate()


func get_asset_contract_snapshot() -> Dictionary:
	return {
		"programmatic_final_art": false,
		"ufo_note": _texture_contract(_ufo_note),
		"three_window_event": _texture_contract(_event_plate),
		"runtime_copy": "ImpossibleNoteCopy",
		"interactive": false,
	}


func _build_ufo_note() -> void:
	var root := Control.new()
	root.name = "UfoEvidenceNote"
	root.position = Vector2(558, 218)
	root.size = Vector2(124, 128)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)

	_ufo_note = _make_texture("UfoNoteArt", Rect2(5, 0, 114, 128), UFO_NOTE_TEXTURE)
	root.add_child(_ufo_note)

	var note := Label.new()
	note.name = "ImpossibleNoteCopy"
	note.position = Vector2(12, 78)
	note.size = Vector2(90, 36)
	note.text = "不是飞碟。\n大概。"
	note.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	note.mouse_filter = Control.MOUSE_FILTER_IGNORE
	note.add_theme_font_override("font", _font)
	note.add_theme_font_size_override("font_size", 14)
	note.add_theme_color_override("font_color", INK)
	root.add_child(note)


func _build_event_plate() -> void:
	_event_plate = _make_texture(
		"ThreeWindowEventArt",
		Rect2(718, 266, 112, 42),
		THREE_WINDOW_EVENT_TEXTURE,
	)
	add_child(_event_plate)


func _make_texture(node_name: String, rect: Rect2, source: Texture2D) -> TextureRect:
	var texture_rect := TextureRect.new()
	texture_rect.name = node_name
	texture_rect.position = rect.position
	texture_rect.size = rect.size
	texture_rect.texture = source
	texture_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	texture_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	texture_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	texture_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return texture_rect


func _texture_contract(texture_rect: TextureRect) -> Dictionary:
	if not is_instance_valid(texture_rect) or texture_rect.texture == null:
		return {}
	return {
		"resource_path": texture_rect.texture.resource_path,
		"source_size": [texture_rect.texture.get_width(), texture_rect.texture.get_height()],
		"display_rect": [int(texture_rect.global_position.x), int(texture_rect.global_position.y), int(texture_rect.size.x), int(texture_rect.size.y)],
		"stretch_mode": texture_rect.stretch_mode,
		"mouse_filter": texture_rect.mouse_filter,
	}
