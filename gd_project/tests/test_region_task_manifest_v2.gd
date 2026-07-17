extends SceneTree

const ManifestV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd")

func _init() -> void:
	var manifest := ManifestV2.load_manifest(true)
	_assert(not manifest.is_empty(), "v2 manifest should load")
	_assert(str(manifest.get("id", "")) == "region_task_board_clean_lowpoly_v2", "manifest id should match v2")
	_assert(int(manifest.get("version", 0)) == 4, "manifest version should be 4")
	var binding: Dictionary = manifest.get("data_binding", {})
	_assert(str(binding.get("event_collection", "")) == "payload.nodes", "event source should be payload.nodes")
	_assert(str(binding.get("event_position_field", "")) == "map_pos", "event position should come from map_pos")
	_assert(not bool(binding.get("fixed_hotspots", true)), "fixed hotspots must be disabled")
	_assert(bool(binding.get("card_pin_shared_id", false)), "card and pin must share an id")
	_assert(not manifest.has("hotspots"), "manifest must not contain a fixed hotspot table")

	var map_asset := ManifestV2.get_asset("rt2_map_base_clean", manifest)
	_assert(not map_asset.is_empty(), "map base asset should exist")
	_assert(not bool(map_asset.get("contains_task_pins", true)), "map raster must not bake task pins")
	_assert(not bool(map_asset.get("interactive", true)), "map raster should be non-interactive")
	_assert(ManifestV2.has_runtime_slice_assets(), "runtime slice assets should be available")
	_assert(ManifestV2.load_asset_texture("rt2_map_base_clean") != null, "map texture should load")
	for asset_id in ["rt2_task_pin_shell_v2", "rt2_task_pin_label_v2", "rt2_task_pin_kind_icons_v3"]:
		var pin_slice_asset := ManifestV2.get_asset(asset_id, manifest)
		_assert(not pin_slice_asset.is_empty(), "pin slice asset should exist: %s" % asset_id)
		_assert(not bool(pin_slice_asset.get("contains_runtime_text", true)), "pin slice must keep runtime text separate: %s" % asset_id)
		_assert(not bool(pin_slice_asset.get("contains_external_shadow", true)), "pin slice must keep external shadow in Godot: %s" % asset_id)
		_assert(ManifestV2.load_asset_texture(asset_id) != null, "pin slice texture should load: %s" % asset_id)

	var contract_paths: Array[String] = [str(manifest.get("page_contract", ""))]
	for path_value in manifest.get("component_contracts", {}).values():
		contract_paths.append(str(path_value))
	for contract_path in contract_paths:
		_assert(not contract_path.is_empty(), "contract path should not be empty")
		var res_path := "res://../%s" % contract_path
		_assert(FileAccess.file_exists(ProjectSettings.globalize_path(res_path)), "contract should exist: %s" % contract_path)

	print("test_region_task_manifest_v2.gd OK")
	quit(0)

func _assert(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	quit(1)
