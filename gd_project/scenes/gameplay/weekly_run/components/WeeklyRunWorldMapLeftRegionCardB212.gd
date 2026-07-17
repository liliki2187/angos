extends Button
class_name WeeklyRunWorldMapLeftRegionCardB212

signal region_selected(region_id: String)

const REFERENCE_SIZE := Vector2(204.0, 160.0)
const ATLAS_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b212_meta_retired_atlas_2x.png"
const ICON_PATHS := {
	"selected": "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_runtime_icon_selected.png",
	"available": "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_runtime_icon_available.png",
	"warning": "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_runtime_icon_warning.png",
	"locked": "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_runtime_icon_locked.png",
}
const REGION_PHOTO_PATHS := {
	"us": "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_clean_photo_selected.png",
	"east_asia": "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_clean_photo_locked.png",
	"pacific": "res://Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b210_clean_photo_available.png",
}
const STATE_INDEX := {
	"selected": 0,
	"available": 1,
	"warning": 2,
	"locked": 3,
}
const TITLE_RECT := Rect2(22.0, 104.0, 114.0, 32.0)
const ICON_RECT := Rect2(151.0, 108.0, 30.0, 30.0)
const PHOTO_RECT := Rect2(21.0, 24.0, 174.0, 64.0)

var _region_id := ""
var _state := "available"
var _source_selected_region_id := ""
var _atlas_rect: TextureRect
var _region_photo: TextureRect
var _state_icon: TextureRect
var _title_label: Label
var _focus_ring: Panel


static func has_runtime_assets() -> bool:
	if not ResourceLoader.exists(ATLAS_PATH):
		return false
	for path in ICON_PATHS.values():
		if not ResourceLoader.exists(path):
			return false
	for path in REGION_PHOTO_PATHS.values():
		if not ResourceLoader.exists(path):
			return false
	return true


func _ready() -> void:
	custom_minimum_size = REFERENCE_SIZE
	size = REFERENCE_SIZE
	text = ""
	focus_mode = Control.FOCUS_ALL
	mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	for style_name in ["normal", "hover", "pressed", "disabled", "focus"]:
		add_theme_stylebox_override(style_name, StyleBoxEmpty.new())
	_build_visuals()
	pressed.connect(func() -> void: region_selected.emit(_region_id))
	focus_entered.connect(func() -> void: _focus_ring.visible = true)
	focus_exited.connect(func() -> void: _focus_ring.visible = false)
	mouse_entered.connect(func() -> void: _atlas_rect.modulate = Color(1.08, 1.08, 1.04, 1.0))
	mouse_exited.connect(func() -> void: _atlas_rect.modulate = Color.WHITE)


func render(region: Dictionary, selected_region_id: String) -> void:
	_region_id = str(region.get("id", ""))
	_source_selected_region_id = selected_region_id
	_state = _derive_state(region, selected_region_id)
	_title_label.text = str(region.get("name", region.get("label", "未命名区域")))
	_region_photo.texture = load(str(REGION_PHOTO_PATHS.get(_region_id, REGION_PHOTO_PATHS["pacific"])))
	tooltip_text = "%s · %s" % [_title_label.text, _state_label(_state)]
	_apply_state_texture()


func get_state_snapshot() -> Dictionary:
	return {
		"region_id": _region_id,
		"selected_region_id": _source_selected_region_id,
		"selected": _region_id == _source_selected_region_id,
		"state": _state,
		"title": _title_label.text if is_instance_valid(_title_label) else "",
		"reference_size": [REFERENCE_SIZE.x, REFERENCE_SIZE.y],
		"interactive_target": "full_card",
	}


func _derive_state(region: Dictionary, selected_region_id: String) -> String:
	if _region_id == selected_region_id:
		return "selected"
	if not bool(region.get("unlocked", region.get("enabled", false))):
		return "locked"
	if str(region.get("tone", "normal")) in ["deadline", "warning"]:
		return "warning"
	return "available"


func _build_visuals() -> void:
	_atlas_rect = TextureRect.new()
	_atlas_rect.name = "B212CardAtlas"
	_atlas_rect.position = Vector2.ZERO
	_atlas_rect.size = REFERENCE_SIZE
	_atlas_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_atlas_rect.stretch_mode = TextureRect.STRETCH_SCALE
	_atlas_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_atlas_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_atlas_rect)

	_region_photo = TextureRect.new()
	_region_photo.name = "ProvisionalRegionPhoto"
	_region_photo.position = PHOTO_RECT.position
	_region_photo.size = PHOTO_RECT.size
	_region_photo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_region_photo.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_region_photo.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_region_photo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_region_photo)

	_title_label = Label.new()
	_title_label.name = "RegionTitle"
	_title_label.position = TITLE_RECT.position
	_title_label.size = TITLE_RECT.size
	_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_title_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_title_label.clip_text = true
	_title_label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	_title_label.add_theme_font_size_override("font_size", 15)
	_title_label.add_theme_color_override("font_color", Color("20221d"))
	_title_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_title_label)

	_state_icon = TextureRect.new()
	_state_icon.name = "RuntimeStateIcon"
	_state_icon.position = ICON_RECT.position
	_state_icon.size = ICON_RECT.size
	_state_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_state_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_state_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_state_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_state_icon)

	_focus_ring = Panel.new()
	_focus_ring.name = "KeyboardFocusRing"
	_focus_ring.position = Vector2(3.0, 3.0)
	_focus_ring.size = REFERENCE_SIZE - Vector2(6.0, 6.0)
	_focus_ring.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var focus_style := StyleBoxFlat.new()
	focus_style.bg_color = Color.TRANSPARENT
	focus_style.border_color = Color("e5d99d")
	focus_style.set_border_width_all(2)
	_focus_ring.add_theme_stylebox_override("panel", focus_style)
	_focus_ring.visible = false
	add_child(_focus_ring)


func _apply_state_texture() -> void:
	var atlas := AtlasTexture.new()
	atlas.atlas = load(ATLAS_PATH)
	atlas.region = Rect2(float(STATE_INDEX[_state]) * 408.0, 0.0, 408.0, 320.0)
	_atlas_rect.texture = atlas
	_state_icon.texture = load(str(ICON_PATHS[_state]))


func _state_label(state: String) -> String:
	match state:
		"selected":
			return "当前选择"
		"warning":
			return "风险预警"
		"locked":
			return "尚未解锁"
		_:
			return "可选择"
