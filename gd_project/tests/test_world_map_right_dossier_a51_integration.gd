extends SceneTree

const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	_assert(packed != null, "weekly run scene should load")
	var scene := packed.instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_TOP_LEFT)
	scene.size = Vector2(1920, 1080)
	await _settle_frames(4)

	scene._on_advance_phase_pressed()
	await _settle_frames(6)
	var assembly := scene.explore_phase.get_world_map_assembly() as Control
	_assert(assembly != null, "independent WMW assembly should mount in the production world view")
	_assert(assembly.visible, "independent WMW assembly should be visible in world mode")
	_assert(not scene.explore_phase.root_vbox.visible, "legacy GLOBAL CHANNEL phase host should be hidden")
	_assert(not scene.header_panel.visible, "WeeklyRunGame legacy header should be hidden for the full-screen assembly")
	_assert(not scene.world_shell_art.visible, "legacy world shell art should be hidden for the full-screen assembly")
	_assert(scene.explore_phase.world_detail_panel.get_node_or_null("WorldRightDossierBackdrop") == null, "old isolated A5.1 backdrop mount must be removed")

	var collapsed: Dictionary = assembly.get_state_snapshot()
	_assert(str(collapsed.get("artifact_type", "")) == "runtime_state_preview", "assembly should identify the runtime-state preview artifact")
	_assert(str(collapsed.get("map_artifact_type", "")) == "structure_only", "map stage must disclose its structure-only status")
	_assert(collapsed.get("left_rect", []) == [24.0, 16.0, 228.0, 688.0], "left responsibility bounds should remain frozen")
	_assert(collapsed.get("center_rect", []) == [268.0, 16.0, 648.0, 688.0], "center responsibility bounds should remain frozen")
	_assert(collapsed.get("right_rect", []) == [932.0, 16.0, 320.0, 688.0], "right responsibility bounds should remain frozen")
	_assert(collapsed.get("dossier_rect", []) == [932.0, 30.0, 320.0, 520.0], "A5.1 global placement should preserve its frozen contract")
	_assert(float(collapsed.get("center_right_edge", 9999.0)) <= 916.0, "center content and shadows must not cross x=916")
	_assert(collapsed.get("map_layer_names", []) == ["MapBaseLayer", "RouteLayer", "SelectedRegionLayer", "PinLayer", "LabelLayer"], "central map should expose the five required layers")
	_assert(not bool(collapsed.get("old_global_channel_present", true)), "old GLOBAL CHANNEL identity must not survive in the assembly")
	_assert(not bool(collapsed.get("external_cta_present", true)), "external CTA must not be added")
	_assert(not bool(collapsed.get("symbol_strip_present", true)), "globe/eye/check/hand strip must not be added")
	_assert(int(collapsed.get("enter_region_day_cost", -1)) == 0, "entering the region task board itself should cost zero days")
	_assert(_four_endpoints_match(collapsed, "us"), "left card, selected pin, dossier, and CTA should share selected_region_id=us")

	var dossier := assembly.get_dossier() as Control
	_assert(dossier != null, "A5.1 dossier should live inside the independent assembly")
	var paper := dossier.find_child("DossierPaperShell", true, false) as TextureRect
	var photo := dossier.find_child("RegionPhotoPlaceholder", true, false) as TextureRect
	var primary_skin := dossier.find_child("PrimaryCtaSkin", true, false) as TextureRect
	_assert(paper != null and paper.size.is_equal_approx(Vector2(320, 520)), "paper texture should preserve the 320x520 A5.1 geometry")
	_assert(photo != null and photo.size.is_equal_approx(Vector2(276, 176)), "photo should preserve the 276x176 A5.1 slot")
	_assert(primary_skin != null and primary_skin.size.is_equal_approx(Vector2(284, 50)), "primary skin should preserve the 284x50 A5.1 action slot")
	var dossier_collapsed: Dictionary = collapsed.get("dossier", {})
	_assert(str(dossier_collapsed.get("title", "")) == "北美禁区带", "dossier title should come from the production payload")
	_assert(int(dossier_collapsed.get("preview_source_rows", 0)) == 4, "North America should expose four production task previews")
	_assert(dossier_collapsed.get("interactive_button_names", []) == ["MissionSummaryButton", "PrimaryEnterButton"], "A5.1 should expose exactly two actions")

	assembly.set_mission_intel_expanded(true)
	await _settle_frames(3)
	var expanded: Dictionary = assembly.get_state_snapshot()
	var dossier_expanded: Dictionary = expanded.get("dossier", {})
	_assert(bool(dossier_expanded.get("expanded", false)), "mission intelligence should expand in place")
	_assert(int(dossier_expanded.get("preview_rendered_rows", 0)) == 2, "expanded disclosure should render only two read-only tasks")
	_assert(_four_endpoints_match(expanded, "us"), "expanded disclosure must not change selected_region_id endpoints")

	scene._on_region_pressed("east_asia")
	await _settle_frames(4)
	var locked: Dictionary = assembly.get_state_snapshot()
	var dossier_locked: Dictionary = locked.get("dossier", {})
	_assert(_four_endpoints_match(locked, "east_asia"), "all four endpoints should follow locked East Asia selection")
	_assert(not bool(dossier_locked.get("expanded", true)), "changing region should collapse mission intelligence")
	_assert(bool(dossier_locked.get("summary_disabled", false)), "locked region should disable disclosure")
	_assert(bool(dossier_locked.get("primary_disabled", false)), "locked region should disable the primary CTA")
	_assert(int(dossier_locked.get("preview_source_rows", -1)) == 0, "locked region should not leak task names")

	scene._on_region_pressed("us")
	await _settle_frames(3)
	var days_before_enter := int(scene.run_state.remaining_days)
	assembly.activate_primary_for_test()
	await _settle_frames(4)
	_assert(str(scene.explore_view_mode) == "region", "A5.1 primary CTA should enter the existing region task board")
	_assert(int(scene.run_state.remaining_days) == days_before_enter, "entering the region task board should not consume a day")

	print("test_world_map_right_dossier_a51_integration.gd OK")
	quit(0)


func _four_endpoints_match(snapshot: Dictionary, expected: String) -> bool:
	return str(snapshot.get("selected_region_id", "")) == expected \
		and str(snapshot.get("left_selected_region_id", "")) == expected \
		and str(snapshot.get("map_selected_region_id", "")) == expected \
		and str(snapshot.get("dossier_region_id", "")) == expected \
		and str(snapshot.get("cta_region_id", "")) == expected


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _assert(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	quit(1)
