extends RefCounted
class_name WeeklyRunRegionTaskAssetManifest

const MANIFEST_RES_PATH := "res://Assets/ui/angus_packaging/region_task/region_task_asset_manifest.json"

static var _manifest_cache: Dictionary = {}
static var _texture_cache: Dictionary = {}
static var _frame_texture_cache: Dictionary = {}

static func load_manifest(force_reload: bool = false) -> Dictionary:
	if not force_reload and not _manifest_cache.is_empty():
		return _manifest_cache
	var text := _read_runtime_text(MANIFEST_RES_PATH)
	if text.is_empty():
		push_warning("Region task asset manifest is missing or empty: %s" % MANIFEST_RES_PATH)
		return {}
	var parsed = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("Region task asset manifest is not a JSON object: %s" % MANIFEST_RES_PATH)
		return {}
	_manifest_cache = parsed
	return _manifest_cache

static func get_asset(asset_id: String, manifest: Dictionary = {}) -> Dictionary:
	var data := manifest if not manifest.is_empty() else load_manifest()
	for asset in data.get("assets", []):
		if typeof(asset) == TYPE_DICTIONARY and str(asset.get("id", "")) == asset_id:
			return asset
	return {}

static func has_asset(asset_id: String, manifest: Dictionary = {}) -> bool:
	return not get_asset(asset_id, manifest).is_empty()

static func has_frame(asset_id: String, frame_id: String, manifest: Dictionary = {}) -> bool:
	var asset := get_asset(asset_id, manifest)
	for frame in asset.get("frames", []):
		if typeof(frame) == TYPE_DICTIONARY and str(frame.get("id", "")) == frame_id:
			return true
	return false

static func asset_res_path(asset_id: String, manifest: Dictionary = {}) -> String:
	var asset := get_asset(asset_id, manifest)
	if asset.is_empty():
		return ""
	return _to_res_path(str(asset.get("final_path", "")))

static func asset_runtime_file_exists(asset_id: String, manifest: Dictionary = {}) -> bool:
	var res_path := asset_res_path(asset_id, manifest)
	if res_path.is_empty():
		return false
	return FileAccess.file_exists(ProjectSettings.globalize_path(res_path))

static func load_asset_texture(asset_id: String) -> Texture2D:
	var asset := get_asset(asset_id)
	if asset.is_empty():
		push_warning("Region task asset not found: %s" % asset_id)
		return null
	var res_path := _to_res_path(str(asset.get("final_path", "")))
	if res_path.is_empty():
		push_warning("Region task asset has no final_path: %s" % asset_id)
		return null
	if _texture_cache.has(res_path):
		return _texture_cache[res_path]
	var image := Image.load_from_file(ProjectSettings.globalize_path(res_path))
	if image == null or image.is_empty():
		push_warning("Region task texture failed to load: %s" % res_path)
		return null
	var texture := ImageTexture.create_from_image(image)
	_texture_cache[res_path] = texture
	return texture

static func load_asset_frame_texture(asset_id: String, frame_id: String) -> Texture2D:
	var cache_key := "%s::%s" % [asset_id, frame_id]
	if _frame_texture_cache.has(cache_key):
		return _frame_texture_cache[cache_key]
	var asset := get_asset(asset_id)
	if asset.is_empty():
		push_warning("Region task atlas asset not found: %s" % asset_id)
		return null
	for frame in asset.get("frames", []):
		if typeof(frame) != TYPE_DICTIONARY or str(frame.get("id", "")) != frame_id:
			continue
		var rect: Array = frame.get("rect", [])
		if rect.size() != 4:
			push_warning("Region task atlas frame has invalid rect: %s::%s" % [asset_id, frame_id])
			return null
		var atlas := load_asset_texture(asset_id)
		if atlas == null:
			return null
		var texture := AtlasTexture.new()
		texture.atlas = atlas
		texture.region = Rect2(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))
		_frame_texture_cache[cache_key] = texture
		return texture
	push_warning("Region task atlas frame not found: %s::%s" % [asset_id, frame_id])
	return null

static func runtime_rect(asset_id: String) -> Rect2:
	var asset := get_asset(asset_id)
	var rect: Array = asset.get("runtime_rect", [])
	if rect.size() != 4:
		return Rect2()
	return Rect2(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))

static func text_safe_rects(asset_id: String) -> Array:
	return get_asset(asset_id).get("content_rects", [])

static func forbidden_rects(asset_id: String) -> Array:
	return get_asset(asset_id).get("no_text_rects", [])

static func hit_rect(asset_id: String, frame_id: String = "") -> Rect2:
	var source := _frame_or_asset(asset_id, frame_id)
	var rect: Array = source.get("hit_rect", [])
	if rect.size() != 4:
		return Rect2()
	return Rect2(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))

static func hover_rect(asset_id: String, frame_id: String = "") -> Rect2:
	var source := _frame_or_asset(asset_id, frame_id)
	var rect: Array = source.get("hover_rect", [])
	if rect.size() != 4:
		return Rect2()
	return Rect2(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))

static func _frame_or_asset(asset_id: String, frame_id: String = "") -> Dictionary:
	var asset := get_asset(asset_id)
	if frame_id.is_empty():
		return asset
	for frame in asset.get("frames", []):
		if typeof(frame) == TYPE_DICTIONARY and str(frame.get("id", "")) == frame_id:
			return frame
	return asset

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
