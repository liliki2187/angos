extends TextureRect

const REGION_TEXTURES := {
	"north_america": preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/north_america_story_1104x704.png"),
	"east_asia": preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/east_asia_story_1104x704.png"),
	"pacific": preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/pacific_story_1104x704.png"),
}

var variant := "north_america"
var locked := false


func _ready() -> void:
	expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_apply_texture()


func configure(next_variant: String, next_locked: bool = false) -> void:
	variant = next_variant
	locked = next_locked
	_apply_texture()


func get_source_contract() -> Dictionary:
	var active_texture: Texture2D = texture
	return {
		"region_id": variant,
		"resource_path": active_texture.resource_path if active_texture != null else "",
		"source_size": [int(active_texture.get_width()), int(active_texture.get_height())] if active_texture != null else [0, 0],
		"display_size": [int(size.x), int(size.y)],
		"stretch_mode": stretch_mode,
	}


func _apply_texture() -> void:
	texture = REGION_TEXTURES.get(variant, REGION_TEXTURES["north_america"])
	self_modulate = Color("a7ada4") if locked else Color.WHITE
