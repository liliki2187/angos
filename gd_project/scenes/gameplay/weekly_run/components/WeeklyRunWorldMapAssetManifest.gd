extends RefCounted
class_name WeeklyRunWorldMapAssetManifest

const MANIFEST_RES_PATH_V5 := "res://Assets/ui/angus_packaging/world_map/imagegen_v5/world_map_imagegen_manifest.json"
const MANIFEST_RES_PATH_V6 := "res://Assets/ui/angus_packaging/world_map/imagegen_v6/world_map_imagegen_manifest.json"
const MANIFEST_RES_PATH := MANIFEST_RES_PATH_V5

static var _manifest_cache: Dictionary = {}
static var _manifest_cache_by_path: Dictionary = {}
static var _texture_cache: Dictionary = {}
static var _frame_texture_cache: Dictionary = {}

static func load_manifest(force_reload: bool = false) -> Dictionary:
	return load_manifest_path(MANIFEST_RES_PATH, force_reload)

static func load_manifest_v6(force_reload: bool = false) -> Dictionary:
	return load_manifest_path(MANIFEST_RES_PATH_V6, force_reload)

static func load_manifest_path(manifest_res_path: String, force_reload: bool = false) -> Dictionary:
	if not force_reload and _manifest_cache_by_path.has(manifest_res_path):
		return _manifest_cache_by_path[manifest_res_path]
	var text := _read_runtime_text(manifest_res_path)
	if text.is_empty():
		push_warning("World map imagegen manifest is missing or empty: %s" % manifest_res_path)
		return {}
	var parsed = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("World map imagegen manifest is not a JSON object: %s" % manifest_res_path)
		return {}
	_manifest_cache_by_path[manifest_res_path] = parsed
	if manifest_res_path == MANIFEST_RES_PATH:
		_manifest_cache = parsed
	return parsed

static func get_asset(asset_id: String, manifest: Dictionary = {}) -> Dictionary:
	var data := manifest if not manifest.is_empty() else load_manifest()
	for asset in data.get("assets", []):
		if typeof(asset) == TYPE_DICTIONARY and str(asset.get("id", "")) == asset_id:
			return asset
	return {}

static func load_asset_texture(asset_id: String, manifest: Dictionary = {}) -> Texture2D:
	var asset := get_asset(asset_id, manifest)
	if asset.is_empty():
		push_warning("World map imagegen asset not found: %s" % asset_id)
		return null
	var res_path := _to_res_path(str(asset.get("final_path", "")))
	if res_path.is_empty():
		push_warning("World map imagegen asset has no final_path: %s" % asset_id)
		return null
	if _texture_cache.has(res_path):
		return _texture_cache[res_path]
	var image := Image.load_from_file(ProjectSettings.globalize_path(res_path))
	if image == null or image.is_empty():
		push_warning("World map imagegen texture failed to load: %s" % res_path)
		return null
	var texture := ImageTexture.create_from_image(image)
	_texture_cache[res_path] = texture
	return texture

static func load_asset_frame_texture(asset_id: String, frame_id: String, manifest: Dictionary = {}) -> Texture2D:
	var manifest_id := str(manifest.get("id", "default"))
	var cache_key := "%s::%s::%s" % [manifest_id, asset_id, frame_id]
	if _frame_texture_cache.has(cache_key):
		return _frame_texture_cache[cache_key]
	var asset := get_asset(asset_id, manifest)
	if asset.is_empty():
		push_warning("World map imagegen atlas asset not found: %s" % asset_id)
		return null
	for frame in asset.get("frames", []):
		if typeof(frame) != TYPE_DICTIONARY or str(frame.get("id", "")) != frame_id:
			continue
		var rect: Array = frame.get("rect", [])
		if rect.size() != 4:
			push_warning("World map imagegen atlas frame has invalid rect: %s::%s" % [asset_id, frame_id])
			return null
		var atlas := load_asset_texture(asset_id, manifest)
		if atlas == null:
			return null
		var texture := AtlasTexture.new()
		texture.atlas = atlas
		texture.region = Rect2(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))
		_frame_texture_cache[cache_key] = texture
		return texture
	push_warning("World map imagegen atlas frame not found: %s::%s" % [asset_id, frame_id])
	return null

static func runtime_rect(asset_id: String, manifest: Dictionary = {}) -> Rect2:
	var asset := get_asset(asset_id, manifest)
	var rect: Array = asset.get("runtime_rect", [])
	if rect.size() != 4:
		return Rect2()
	return Rect2(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))

static func text_safe_rects(asset_id: String, manifest: Dictionary = {}) -> Array:
	return get_asset(asset_id, manifest).get("dynamic_text_rects", [])

static func _read_runtime_text(res_path: String) -> String:
	var file := FileAccess.open(ProjectSettings.globalize_path(res_path), FileAccess.READ)
	if file == null:
		return ""
	var text := file.get_as_text()
	file.close()
	return text

static func _to_res_path(path: String) -> String:
	var normalized := path.replace("\\", "/")
	if normalized.begins_with("res://"):
		return normalized
	var marker := "gd_project/"
	var index := normalized.find(marker)
	if index >= 0:
		return "res://%s" % normalized.substr(index + marker.length())
	if normalized.begins_with("Assets/"):
		return "res://%s" % normalized
	return ""
