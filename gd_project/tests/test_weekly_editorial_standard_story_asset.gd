extends SceneTree

const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const EditorialAssets := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunEditorialAssetManifest.gd")
const OUT_PATH := "res://../docs/screenshots/2026-07-16-weekly-editorial-blue-phone-booth-b-slice/standard-story-asset-audit.json"

const STANDARD_SLOTS := ["feature-1", "feature-2", "inner-1", "inner-2"]

var _checks := []


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	root.size = Vector2i(1920, 1080)
	var scene := (load(WEEKLY_RUN_SCENE) as PackedScene).instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	await _frames(4)
	scene._on_advance_phase_pressed()
	await _frames(2)
	scene._enter_editorial_phase()
	await _frames(3)
	_set_fixture(scene)
	scene._refresh_all()
	await _frames(4)

	var harbor_asset := EditorialAssets.get_story_asset_by_article_id(1003, "compact")
	var harbor_texture := EditorialAssets.load_texture("editorial_story_harbor_tomorrow_tide")
	var roswell_asset := EditorialAssets.get_story_asset_by_article_id(1004, "compact")
	var roswell_tall_asset := EditorialAssets.get_story_asset_by_article_id(1004, "tall")
	var roswell_texture := EditorialAssets.load_texture("editorial_story_roswell_copy_refusal")
	var roswell_roles: Array = roswell_asset.get("allowed_roles", [])
	var city_hall_asset := EditorialAssets.get_story_asset_by_article_id(1005, "compact")
	var city_hall_tall_asset := EditorialAssets.get_story_asset_by_article_id(1005, "tall")
	var city_hall_texture := EditorialAssets.load_texture("editorial_story_city_hall_shadow_department")
	var city_hall_roles: Array = city_hall_asset.get("allowed_roles", [])
	var cat_booth_asset := EditorialAssets.get_story_asset_by_article_id(1006, "compact")
	var cat_booth_tall_asset := EditorialAssets.get_story_asset_by_article_id(1006, "tall")
	var cat_booth_texture := EditorialAssets.load_texture("editorial_story_cats_refuse_blue_phone_booth")
	var cat_booth_roles: Array = cat_booth_asset.get("allowed_roles", [])
	_check("manifest_maps_harbor_article", not harbor_asset.is_empty() and int(harbor_asset.get("article_id", -1)) == 1003 and str(harbor_asset.get("asset_tier", "")) == "B")
	_check("manifest_query_maps_roswell_compact_and_tall", not roswell_asset.is_empty() and roswell_asset == roswell_tall_asset and int(roswell_asset.get("article_id", -1)) == 1004 and str(roswell_asset.get("asset_tier", "")) == "B")
	_check("roswell_roles_are_standard_slots_only", roswell_roles.size() == 2 and roswell_roles.has("compact") and roswell_roles.has("tall") and EditorialAssets.get_story_asset_by_article_id(1004, "main").is_empty())
	_check("manifest_query_maps_city_hall_compact_and_tall", not city_hall_asset.is_empty() and city_hall_asset == city_hall_tall_asset and int(city_hall_asset.get("article_id", -1)) == 1005 and str(city_hall_asset.get("asset_tier", "")) == "B")
	_check("city_hall_roles_are_standard_slots_only", city_hall_roles.size() == 2 and city_hall_roles.has("compact") and city_hall_roles.has("tall") and EditorialAssets.get_story_asset_by_article_id(1005, "main").is_empty())
	_check("manifest_query_maps_cat_booth_compact_and_tall", not cat_booth_asset.is_empty() and cat_booth_asset == cat_booth_tall_asset and int(cat_booth_asset.get("article_id", -1)) == 1006 and str(cat_booth_asset.get("asset_tier", "")) == "B")
	_check("cat_booth_roles_are_standard_slots_only", cat_booth_roles.size() == 2 and cat_booth_roles.has("compact") and cat_booth_roles.has("tall") and EditorialAssets.get_story_asset_by_article_id(1006, "main").is_empty())
	_check("all_four_production_bitmaps_load", harbor_texture != null and harbor_texture.get_size() == Vector2(756, 696) and roswell_texture != null and roswell_texture.get_size() == Vector2(756, 696) and city_hall_texture != null and city_hall_texture.get_size() == Vector2(756, 696) and cat_booth_texture != null and cat_booth_texture.get_size() == Vector2(756, 696))
	_check("roswell_asset_is_no_text_opaque_story_art", str(roswell_asset.get("background", "")) == "opaque" and (roswell_asset.get("no_text_rects", []) as Array).size() == 1)
	_check("city_hall_asset_is_no_text_opaque_story_art", str(city_hall_asset.get("background", "")) == "opaque" and (city_hall_asset.get("no_text_rects", []) as Array).size() == 1)
	_check("cat_booth_asset_is_no_text_opaque_story_art", str(cat_booth_asset.get("background", "")) == "opaque" and (cat_booth_asset.get("no_text_rects", []) as Array).size() == 1)

	var editorial = scene.editorial_phase
	var harbor_nodes: Dictionary = editorial._slot_nodes["feature-1"]
	var roswell_nodes: Dictionary = editorial._slot_nodes["feature-2"]
	var city_hall_nodes: Dictionary = editorial._slot_nodes["inner-1"]
	var cat_booth_nodes: Dictionary = editorial._slot_nodes["inner-2"]
	_check("default_feature_one_resolves_harbor", harbor_nodes.story_texture.texture == harbor_texture and harbor_nodes.story_texture.visible and not harbor_nodes.story_fallback.visible)
	_check("default_feature_two_resolves_roswell", roswell_nodes.story_texture.texture == roswell_texture and roswell_nodes.story_texture.visible and not roswell_nodes.story_fallback.visible)
	_check("default_inner_one_resolves_city_hall", city_hall_nodes.story_texture.texture == city_hall_texture and city_hall_nodes.story_texture.visible and not city_hall_nodes.story_fallback.visible)
	_check("default_inner_two_resolves_cat_booth", cat_booth_nodes.story_texture.texture == cat_booth_texture and cat_booth_nodes.story_texture.visible and not cat_booth_nodes.story_fallback.visible)
	_check("compact_photo_rect_stays_frozen", harbor_nodes.story_texture.position == Vector2(12, 64) and harbor_nodes.story_texture.size == Vector2(189, 170))
	_check("bitmap_content_never_consumes_input", harbor_nodes.story_texture.mouse_filter == Control.MOUSE_FILTER_IGNORE and roswell_nodes.story_texture.mouse_filter == Control.MOUSE_FILTER_IGNORE and city_hall_nodes.story_texture.mouse_filter == Control.MOUSE_FILTER_IGNORE and cat_booth_nodes.story_texture.mouse_filter == Control.MOUSE_FILTER_IGNORE and harbor_nodes.story_fallback.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	_check("runtime_uses_center_cover", harbor_nodes.story_texture.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_COVERED and roswell_nodes.story_texture.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_COVERED and city_hall_nodes.story_texture.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_COVERED and cat_booth_nodes.story_texture.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_COVERED)
	_check("default_replace_button_count_stays_zero", not editorial._context_replace_button.visible)

	var every_standard_slot_follows_article := true
	var no_stale_duplicate := true
	var expected_textures := {
		1003: harbor_texture,
		1004: roswell_texture,
		1005: city_hall_texture,
		1006: cat_booth_texture,
	}
	for mapped_article_id in [1003, 1004, 1005, 1006]:
		var expected_texture: Texture2D = expected_textures[mapped_article_id]
		for target_slot_id in STANDARD_SLOTS:
			for slot_id in STANDARD_SLOTS:
				scene.run_state.slot_assignment[slot_id] = -1
			scene.run_state.slot_assignment[target_slot_id] = mapped_article_id
			scene._refresh_all()
			await _frames(2)
			for slot_id in STANDARD_SLOTS:
				var nodes: Dictionary = editorial._slot_nodes[slot_id]
				if slot_id == target_slot_id:
					every_standard_slot_follows_article = every_standard_slot_follows_article and nodes.story_texture.texture == expected_texture and nodes.story_texture.visible and not nodes.story_fallback.visible
				else:
					no_stale_duplicate = no_stale_duplicate and not nodes.story_texture.visible
	_check("all_four_article_assets_follow_all_compact_and_tall_slots", every_standard_slot_follows_article)
	_check("moving_article_leaves_no_stale_duplicate", no_stale_duplicate)

	for slot_id in STANDARD_SLOTS:
		scene.run_state.slot_assignment[slot_id] = -1
	scene._refresh_all()
	await _frames(2)
	var empty_nodes: Dictionary = editorial._slot_nodes["inner-2"]
	_check("empty_slot_hides_art_and_fallback", empty_nodes.story_texture.texture == null and not empty_nodes.story_texture.visible and not empty_nodes.story_fallback.visible)

	var unmapped_articles_keep_fallback := true
	for unmapped_article_id in [1099]:
		for target_slot_id in ["feature-1", "inner-2"]:
			for slot_id in STANDARD_SLOTS:
				scene.run_state.slot_assignment[slot_id] = -1
			scene.run_state.slot_assignment[target_slot_id] = unmapped_article_id
			scene._refresh_all()
			await _frames(2)
			var nodes: Dictionary = editorial._slot_nodes[target_slot_id]
			unmapped_articles_keep_fallback = unmapped_articles_keep_fallback and nodes.story_texture.texture == null and not nodes.story_texture.visible and nodes.story_fallback.visible
	_check("unmapped_unknown_article_keeps_fallback", unmapped_articles_keep_fallback)

	for slot_id in STANDARD_SLOTS:
		scene.run_state.slot_assignment[slot_id] = -1
	scene.run_state.slot_assignment["feature-1"] = 1003
	scene._refresh_all()
	await _frames(2)
	var switched_nodes: Dictionary = editorial._slot_nodes["feature-1"]
	var switch_starts_with_harbor: bool = switched_nodes.story_texture.texture == harbor_texture and switched_nodes.story_texture.visible
	scene.run_state.slot_assignment["feature-1"] = 1004
	scene._refresh_all()
	await _frames(2)
	var switch_changes_to_roswell: bool = switched_nodes.story_texture.texture == roswell_texture and switched_nodes.story_texture.visible
	scene.run_state.slot_assignment["feature-1"] = 1005
	scene._refresh_all()
	await _frames(2)
	var switch_changes_to_city_hall: bool = switched_nodes.story_texture.texture == city_hall_texture and switched_nodes.story_texture.visible
	scene.run_state.slot_assignment["feature-1"] = 1006
	scene._refresh_all()
	await _frames(2)
	var switch_changes_to_cat_booth: bool = switched_nodes.story_texture.texture == cat_booth_texture and switched_nodes.story_texture.visible
	scene.run_state.slot_assignment["feature-1"] = 1099
	scene._refresh_all()
	await _frames(2)
	_check("switching_articles_maps_all_then_clears_previous_texture", switch_starts_with_harbor and switch_changes_to_roswell and switch_changes_to_city_hall and switch_changes_to_cat_booth and switched_nodes.story_texture.texture == null and not switched_nodes.story_texture.visible and switched_nodes.story_fallback.visible)

	var tall_nodes: Dictionary = editorial._slot_nodes["inner-2"]
	_check("tall_photo_rect_stays_frozen", tall_nodes.story_texture.position == Vector2(12, 74) and tall_nodes.story_texture.size == Vector2(189, 174))

	var passed := true
	for check in _checks:
		if not bool(check.get("pass", false)):
			passed = false
	var result := {
		"passed": passed,
		"check_count": _checks.size(),
		"checks": _checks,
		"asset_ids": ["editorial_story_harbor_tomorrow_tide", "editorial_story_roswell_copy_refusal", "editorial_story_city_hall_shadow_department", "editorial_story_cats_refuse_blue_phone_booth"],
		"article_ids": [1003, 1004, 1005, 1006],
		"covered_slots": STANDARD_SLOTS,
	}
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_PATH).get_base_dir())
	FileAccess.open(ProjectSettings.globalize_path(OUT_PATH), FileAccess.WRITE).store_string(JSON.stringify(result, "  ") + "\n")
	if not passed:
		push_error("weekly editorial standard story asset audit failed")
	quit(0 if passed else 1)


func _check(id: String, condition: bool) -> void:
	_checks.append({"id": id, "pass": condition})


func _set_fixture(scene: Control) -> void:
	scene.run_state.article_candidates.assign([
		{"id": 1001, "title": "M330 末班车在不存在的站台停了三秒", "tags": ["Gossip", "Humor"], "quality": "Gold", "base_value": 540, "negatives": [], "source": "material_inventory"},
		{"id": 1002, "title": "51 区夜班货车携带会呼吸的路牌", "tags": ["Military", "Economy"], "quality": "Gold", "base_value": 500, "negatives": [], "source": "material_inventory"},
		{"id": 1003, "title": "港口广播连续七晚播报明天的潮汐", "tags": ["Gossip", "Shopping"], "quality": "Silver", "base_value": 340, "negatives": [], "source": "material_inventory"},
		{"id": 1004, "title": "罗斯威尔档案第十四页拒绝被复印", "tags": ["Politics", "Military"], "quality": "Silver", "base_value": 320, "negatives": ["thin_source"], "source": "material_inventory"},
		{"id": 1005, "title": "市政厅新增了一个不存在的影子部门", "tags": ["Politics", "Humor"], "quality": "Bronze", "base_value": 220, "negatives": [], "source": "filler"},
		{"id": 1006, "title": "街区猫群一致拒绝经过蓝色电话亭", "tags": ["Pets", "Gossip"], "quality": "Bronze", "base_value": 190, "negatives": [], "source": "filler"},
		{"id": 1099, "title": "未映射审计稿", "tags": ["Gossip"], "quality": "Bronze", "base_value": 0, "negatives": [], "source": "test_fixture"},
	])
	scene.run_state.slot_assignment = {
		"front-main": 1001,
		"front-side": 1002,
		"feature-1": 1003,
		"feature-2": 1004,
		"inner-1": 1005,
		"inner-2": 1006,
	}
	scene.selected_article_id = -1


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame
