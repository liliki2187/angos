extends SceneTree

const PrototypeScene := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedPrototype.tscn")

var _failed := false


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	print("world_map_integrated_test: instantiate")
	var prototype := PrototypeScene.instantiate()
	prototype.position = Vector2.ZERO
	prototype.size = Vector2(1920, 1080)
	root.add_child(prototype)
	print("world_map_integrated_test: added")
	await process_frame
	await process_frame
	print("world_map_integrated_test: ready")

	var initial: Dictionary = prototype.get_state_snapshot()
	print("world_map_integrated_test: initial snapshot")
	_assert_equal(initial["selected_region_id"], "north_america", "initial region must be north_america")
	_assert_equal(initial["selected_cards"], ["north_america"], "exactly one region card must be selected")
	_assert_equal(initial["selected_beacons"], ["north_america"], "exactly one map beacon must be selected")
	_assert_equal(initial["dossier"]["region_id"], "north_america", "dossier must share the selected region id")
	_assert_equal(initial["dossier"]["status"], "红线升温", "dossier must expose warning independently")
	_assert_equal(initial["button_count"], 8, "only three cards, three beacons, disclosure and CTA may be interactive")
	_assert_equal(initial["interactive_button_names"], ["MapBeacon_east_asia", "MapBeacon_north_america", "MapBeacon_pacific", "MissionDisclosure", "PrimaryEnterCta", "RegionCard_east_asia", "RegionCard_north_america", "RegionCard_pacific"], "the exact eight interactive nodes must remain stable")
	_assert_equal(initial["schedule"]["advance_enabled"], false, "advance day must stay honestly disabled until runtime support exists")
	_assert_equal(initial["schedule"]["state"], "disabled_runtime_unavailable", "schedule state must expose the runtime boundary")
	_assert_equal(initial["schedule"]["root_mouse_filter"], Control.MOUSE_FILTER_IGNORE, "disabled schedule root must not consume pointer input")
	_assert_equal(initial["schedule"]["pointer_consuming_descendant_count"], 0, "disabled schedule subtree must not consume pointer input")
	_assert_equal(initial["schedule"]["focusable_descendant_count"], 0, "disabled schedule subtree must stay out of keyboard focus")
	var cta := prototype.get_node("SelectedRegionDossier/PrimaryEnterCta") as Button
	var collapsed_cta_rect := _rect_to_int_array(cta.get_global_rect())

	var north_card := prototype.get_node("RegionIndex/RegionCard_north_america") as Button
	north_card.emit_signal("pressed")
	await process_frame
	var via_card: Dictionary = prototype.get_state_snapshot()
	_assert_equal(via_card["selected_cards"], via_card["selected_beacons"], "card activation must keep card and beacon selection synchronized")
	_assert_equal(via_card["dossier"]["region_id"], via_card["selected_region_id"], "card activation must keep dossier synchronized")

	var east_beacon := prototype.get_node("MapBeacon_east_asia") as Button
	east_beacon.emit_signal("pressed")
	await process_frame
	var blocked: Dictionary = prototype.get_state_snapshot()
	_assert_equal(blocked["selected_region_id"], "north_america", "locked beacon must not replace the selected region")
	_assert_equal(blocked["blocked_region_id"], "east_asia", "locked beacon must expose disabled feedback")
	_assert_equal(blocked["dossier"]["region_id"], "north_america", "locked beacon must not replace dossier content")
	_assert_equal(blocked["index_feedback"], "东亚神秘地带仍锁定，条件见对应地区卡；选区未改变。", "locked feedback must fit the one-line status slot and keep the card as the condition source")

	var north_beacon := prototype.get_node("MapBeacon_north_america") as Button
	north_beacon.emit_signal("pressed")
	await process_frame
	var via_beacon: Dictionary = prototype.get_state_snapshot()
	_assert_equal(via_beacon["blocked_region_id"], "", "available beacon activation must clear locked feedback")
	_assert_equal(via_beacon["selected_cards"], via_beacon["selected_beacons"], "beacon activation must keep both selectors synchronized")

	prototype.set_mission_expanded(true)
	await process_frame
	var expanded: Dictionary = prototype.get_state_snapshot()
	_assert_equal(expanded["dossier"]["expanded"], true, "mission disclosure must have a real expanded state")
	_assert_equal(_rect_to_int_array(cta.get_global_rect()), collapsed_cta_rect, "mission expansion must not move the primary CTA")

	var hit_rects: Dictionary = prototype.get_hit_rect_snapshot()
	_assert_equal(hit_rects["north_card"], [52, 226, 340, 170], "north card hit rect drifted")
	_assert_equal(hit_rects["north_beacon"], [662, 318, 212, 76], "north beacon hit rect drifted")
	_assert_equal(hit_rects["pacific_beacon"], [1054, 666, 244, 84], "pacific beacon must use the restored map depth")
	_assert_equal(hit_rects["map_safe_rect"], [432, 154, 960, 902], "map safe rect drifted")
	_assert_equal(hit_rects["mission_disclosure"], [1443, 596, 414, 56], "mission disclosure hit rect drifted")
	_assert_equal(hit_rects["primary_cta"], [1443, 956, 414, 76], "primary CTA hit rect drifted")
	_assert_equal(hit_rects["schedule_gate"], [36, 810, 372, 246], "schedule gate must close the left responsibility column")
	_assert_equal(hit_rects["dossier_rect"], [1416, 24, 468, 1032], "dossier must restore full-height responsibility")
	_assert_equal(hit_rects["advance_day_disabled"], [52, 882, 340, 94], "disabled advance control rect drifted")
	_assert_equal(hit_rects["schedule_gate"][1] + hit_rects["schedule_gate"][3], 1056, "schedule must end at the 24px bottom safe edge")
	_assert_equal(hit_rects["map_safe_rect"][1] + hit_rects["map_safe_rect"][3], 1056, "map must end at the 24px bottom safe edge")
	_assert_equal(hit_rects["dossier_rect"][1] + hit_rects["dossier_rect"][3], 1056, "dossier must end at the 24px bottom safe edge")

	var image_contract: Dictionary = prototype.get_region_image_contract_snapshot()
	var north_card_image: Dictionary = image_contract["cards"]["north_america"]
	var east_card_image: Dictionary = image_contract["cards"]["east_asia"]
	var pacific_card_image: Dictionary = image_contract["cards"]["pacific"]
	var dossier_image: Dictionary = image_contract["dossier"]
	_assert_equal(north_card_image["source_size"], [1104, 704], "card image must use the 69:44 canonical source")
	_assert_equal(north_card_image["display_size"], [138, 88], "card image display contract drifted")
	_assert_equal(dossier_image["display_size"], [414, 264], "dossier image display contract drifted")
	_assert_equal(dossier_image["resource_path"], north_card_image["resource_path"], "card and dossier must reuse one canonical region texture")
	_assert_equal(north_card_image["stretch_mode"], TextureRect.STRETCH_KEEP_ASPECT_CENTERED, "card image must keep full-frame aspect-centered display")
	_assert_equal(dossier_image["stretch_mode"], TextureRect.STRETCH_KEEP_ASPECT_CENTERED, "dossier image must keep full-frame aspect-centered display")
	_assert_equal(north_card_image["resource_path"], "res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/north_america_story_1104x704.png", "north America must use the no-text imagegen runtime source")
	_assert_equal(east_card_image["source_size"], [1104, 704], "east Asia card must use the 69:44 canonical source")
	_assert_equal(east_card_image["display_size"], [138, 88], "east Asia card display contract drifted")
	_assert_equal(east_card_image["stretch_mode"], TextureRect.STRETCH_KEEP_ASPECT_CENTERED, "east Asia card must keep full-frame aspect-centered display")
	_assert_equal(east_card_image["resource_path"], "res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/east_asia_story_1104x704.png", "east Asia must use the no-text imagegen runtime source")
	_assert_equal(pacific_card_image["source_size"], [1104, 704], "Pacific card must use the 69:44 canonical source")
	_assert_equal(pacific_card_image["display_size"], [138, 88], "Pacific card display contract drifted")
	_assert_equal(pacific_card_image["stretch_mode"], TextureRect.STRETCH_KEEP_ASPECT_CENTERED, "Pacific card must keep full-frame aspect-centered display")
	_assert_equal(pacific_card_image["resource_path"], "res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/pacific_story_1104x704.png", "Pacific must use the no-text imagegen runtime source")

	var visual_assets: Dictionary = prototype.get_visual_asset_contract_snapshot()
	_assert_equal(visual_assets["classification"], "runtime_state_preview", "visual slice must not claim production status")
	_assert_equal(visual_assets["map_board"]["source_size"], [960, 902], "map board must match the A282 map field without runtime scaling drift")
	_assert_equal(visual_assets["map_board"]["display_rect"], [432, 154, 960, 902], "map board display rect drifted")
	_assert_equal(visual_assets["map_board"]["runtime_overlay_owns_beacons"], true, "map board must stay no-text and leave beacons to runtime")
	_assert_equal(visual_assets["map_decor"]["programmatic_final_art"], false, "map decor must use real bitmap art rather than programmatic final symbols")
	_assert_equal(visual_assets["map_decor"]["ufo_note"]["resource_path"], "res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/ufo_note_228x256.png", "UFO note must use the imagegen-derived transparent asset")
	_assert_equal(visual_assets["map_decor"]["ufo_note"]["source_size"], [228, 256], "UFO note 2x source size drifted")
	_assert_equal(visual_assets["map_decor"]["ufo_note"]["display_rect"], [563, 218, 114, 128], "UFO note display rect drifted")
	_assert_equal(visual_assets["map_decor"]["three_window_event"]["resource_path"], "res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/three_window_event_224x84.png", "three-window event must use the imagegen-derived transparent asset")
	_assert_equal(visual_assets["map_decor"]["three_window_event"]["display_rect"], [718, 266, 112, 42], "three-window event display rect drifted")
	_assert_equal(visual_assets["beacons"]["north_america"]["state"], "selected_warning", "north America beacon must compose the selected warning bitmap state")
	_assert_equal(visual_assets["beacons"]["north_america"]["resource_path"], "res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_selected_warning_144.png", "selected warning beacon must use the real bitmap state")
	_assert_equal(visual_assets["beacons"]["east_asia"]["state"], "locked", "east Asia beacon must use the locked bitmap state")
	_assert_equal(visual_assets["beacons"]["pacific"]["state"], "locked", "Pacific beacon must use the locked bitmap state")
	_assert_equal(visual_assets["beacons"]["north_america"]["programmatic_final_art"], false, "beacon final art must not be drawn from runtime primitives")
	_assert_equal(visual_assets["beacons"]["north_america"]["display_size"], [72, 72], "beacon display registration must remain 72x72")
	_assert_equal(visual_assets["beacons"]["north_america"]["mouse_filter"], Control.MOUSE_FILTER_IGNORE, "beacon art must not add a pointer-consuming layer")

	north_beacon.set_state(false, false)
	await process_frame
	_assert_beacon_asset_contract(
		north_beacon.get_asset_contract_snapshot(),
		"default",
		"res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_default_144.png",
	)
	north_beacon.set_state(true, false)
	await process_frame
	_assert_beacon_asset_contract(
		north_beacon.get_asset_contract_snapshot(),
		"selected",
		"res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_selected_144.png",
	)
	north_beacon.set_state(true, true)
	await process_frame
	_assert_beacon_asset_contract(
		north_beacon.get_asset_contract_snapshot(),
		"selected_warning",
		"res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_selected_warning_144.png",
	)
	east_beacon.set_state(false, false)
	await process_frame
	_assert_beacon_asset_contract(
		east_beacon.get_asset_contract_snapshot(),
		"locked",
		"res://Assets/prototypes/world_map_integrated/a_style_v2_symbols_v1/eye_locked_144.png",
	)

	if _failed:
		quit(1)
		return
	print("test_world_map_integrated_prototype.gd OK")
	quit(0)


func _assert_equal(actual: Variant, expected: Variant, message: String) -> void:
	if actual == expected:
		return
	_failed = true
	push_error("%s | expected=%s actual=%s" % [message, expected, actual])


func _rect_to_int_array(rect: Rect2) -> Array[int]:
	return [int(rect.position.x), int(rect.position.y), int(rect.size.x), int(rect.size.y)]


func _assert_beacon_asset_contract(snapshot: Dictionary, state: String, resource_path: String) -> void:
	_assert_equal(snapshot["state"], state, "beacon state-to-texture mapping drifted")
	_assert_equal(snapshot["resource_path"], resource_path, "beacon state resolved the wrong bitmap")
	_assert_equal(snapshot["source_size"], [144, 144], "beacon state must use the 2x 144x144 source")
	_assert_equal(snapshot["display_size"], [72, 72], "beacon state must keep the shared 72x72 registration")
	_assert_equal(snapshot["stretch_mode"], TextureRect.STRETCH_KEEP_ASPECT_CENTERED, "beacon state must keep aspect-centered display")
	_assert_equal(snapshot["mouse_filter"], Control.MOUSE_FILTER_IGNORE, "beacon bitmap must stay pointer-transparent")
	_assert_equal(snapshot["programmatic_final_art"], false, "beacon state must remain real bitmap art")
