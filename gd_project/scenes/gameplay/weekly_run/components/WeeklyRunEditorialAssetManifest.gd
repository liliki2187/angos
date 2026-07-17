extends RefCounted

const MANIFEST_RES_PATH := "res://Assets/ui/angus_packaging/weekly_editorial/weekly_editorial_asset_manifest.json"

static var _manifest_cache: Dictionary = {}
static var _texture_cache: Dictionary = {}


static func load_manifest(force_reload: bool = false) -> Dictionary:
	if not force_reload and not _manifest_cache.is_empty():
		return _manifest_cache
	var file := FileAccess.open(ProjectSettings.globalize_path(MANIFEST_RES_PATH), FileAccess.READ)
	if file == null:
		push_warning("Weekly editorial asset manifest is missing: %s" % MANIFEST_RES_PATH)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("Weekly editorial asset manifest is not a JSON object")
		return {}
	_manifest_cache = parsed
	return _manifest_cache


static func get_asset(asset_id: String) -> Dictionary:
	for asset in load_manifest().get("assets", []):
		if typeof(asset) == TYPE_DICTIONARY and str(asset.get("id", "")) == asset_id:
			return asset
	return {}


static func get_story_asset_by_article_id(article_id: int, role: String = "") -> Dictionary:
	for asset in load_manifest().get("assets", []):
		if typeof(asset) != TYPE_DICTIONARY:
			continue
		if str(asset.get("asset_type", "")) != "story_art" or int(asset.get("article_id", -1)) != article_id:
			continue
		var allowed_roles: Array = asset.get("allowed_roles", [])
		if not allowed_roles.is_empty() and role != "" and not allowed_roles.has(role):
			continue
		return asset
	return {}


static func load_texture(asset_id: String) -> Texture2D:
	if _texture_cache.has(asset_id):
		return _texture_cache[asset_id]
	var asset := get_asset(asset_id)
	if asset.is_empty():
		push_warning("Weekly editorial asset not found: %s" % asset_id)
		return null
	var res_path := _to_res_path(str(asset.get("final_path", "")))
	var image := Image.load_from_file(ProjectSettings.globalize_path(res_path))
	if image == null or image.is_empty():
		push_warning("Weekly editorial texture failed to load: %s" % res_path)
		return null
	var texture := ImageTexture.create_from_image(image)
	_texture_cache[asset_id] = texture
	return texture


static func _to_res_path(path: String) -> String:
	var normalized := path.replace("\\", "/")
	if normalized.begins_with("res://"):
		return normalized
	var marker := "gd_project/"
	var index := normalized.find(marker)
	if index >= 0:
		return "res://%s" % normalized.substr(index + marker.length())
	return ""
