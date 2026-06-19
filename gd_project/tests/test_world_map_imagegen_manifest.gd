extends SceneTree

const WorldMapManifest := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssetManifest.gd")

func _init() -> void:
	var manifest := WorldMapManifest.load_manifest(true)
	_assert(not manifest.is_empty(), "manifest should load through runtime file access")
	_assert(str(manifest.get("id", "")) == "world_map_imagegen_v5", "manifest id should match v5")

	var pin_asset := WorldMapManifest.get_asset("wm_pin_atlas", manifest)
	_assert(not pin_asset.is_empty(), "wm_pin_atlas should exist")
	_assert(pin_asset.get("background") == "transparent", "pin atlas should be transparent")

	var board_rect := WorldMapManifest.runtime_rect("wm_world_board_base")
	_assert(board_rect.size.x > 0.0 and board_rect.size.y > 0.0, "world board runtime rect should be valid")

	print("test_world_map_imagegen_manifest.gd OK")
	quit(0)

func _assert(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	quit(1)
