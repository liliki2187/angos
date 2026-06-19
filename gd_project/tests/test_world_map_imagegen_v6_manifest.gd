extends SceneTree

const WorldMapManifest := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssetManifest.gd")

func _init() -> void:
	var manifest := WorldMapManifest.load_manifest_v6(true)
	_assert(not manifest.is_empty(), "v6 manifest should load through runtime file access")
	_assert(str(manifest.get("id", "")) == "world_map_imagegen_v6", "manifest id should match v6")

	var map_asset := WorldMapManifest.get_asset("wm_map_board_v6g_component_candidate", manifest)
	_assert(not map_asset.is_empty(), "v6g map board component should exist")
	_assert(WorldMapManifest.runtime_rect("wm_map_board_v6g_component_candidate", manifest).size.x > 0.0, "v6g map board runtime rect should be valid")

	var cta_texture := WorldMapManifest.load_asset_frame_texture("wm_cta_plate_v6g_state_atlas_candidate", "default", manifest)
	_assert(cta_texture != null, "v6g CTA default frame should load")

	var pin_texture := WorldMapManifest.load_asset_frame_texture("wm_pin_icon_v6g_atlas_candidate", "pin_selected", manifest)
	_assert(pin_texture != null, "v6g selected pin frame should load")

	var default_manifest := WorldMapManifest.load_manifest(true)
	_assert(str(default_manifest.get("id", "")) == "world_map_imagegen_v5", "default manifest should remain v5")

	print("test_world_map_imagegen_v6_manifest.gd OK")
	quit(0)

func _assert(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	quit(1)
