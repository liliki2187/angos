extends RefCounted

const MANIFEST_RES_PATH := "res://Assets/ui/angus_packaging/region_task/region_task_asset_manifest_v2.json"

static var _manifest_cache: Dictionary = {}
static var _texture_cache: Dictionary = {}

static func load_manifest(force_reload: bool = false) -> Dictionary:
	if not force_reload and not _manifest_cache.is_empty():
		return _manifest_cache
	var file := FileAccess.open(ProjectSettings.globalize_path(MANIFEST_RES_PATH), FileAccess.READ)
	if file == null:
		push_warning("Region task v2 manifest is missing: %s" % MANIFEST_RES_PATH)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("Region task v2 manifest is not a JSON object: %s" % MANIFEST_RES_PATH)
		return {}
	_manifest_cache = parsed
	return _manifest_cache

static func get_asset(asset_id: String, manifest: Dictionary = {}) -> Dictionary:
	var data := manifest if not manifest.is_empty() else load_manifest()
	for asset in data.get("assets", []):
		if typeof(asset) == TYPE_DICTIONARY and str(asset.get("id", "")) == asset_id:
			return asset
	return {}

static func has_runtime_slice_assets() -> bool:
	var manifest := load_manifest()
	if str(manifest.get("id", "")) != "region_task_board_clean_lowpoly_v2":
		return false
	var map_asset := get_asset("rt2_map_base_clean", manifest)
	var res_path := _to_res_path(str(map_asset.get("final_path", "")))
	return not res_path.is_empty() and FileAccess.file_exists(ProjectSettings.globalize_path(res_path))

static func load_asset_texture(asset_id: String) -> Texture2D:
	var asset := get_asset(asset_id)
	if asset.is_empty():
		push_warning("Region task v2 asset not found: %s" % asset_id)
		return null
	var res_path := _to_res_path(str(asset.get("final_path", "")))
	if res_path.is_empty():
		push_warning("Region task v2 asset has no loadable final_path: %s" % asset_id)
		return null
	if _texture_cache.has(res_path):
		return _texture_cache[res_path]
	var image := Image.load_from_file(ProjectSettings.globalize_path(res_path))
	if image == null or image.is_empty():
		push_warning("Region task v2 texture failed to load: %s" % res_path)
		return null
	var texture := ImageTexture.create_from_image(image)
	_texture_cache[res_path] = texture
	return texture

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
