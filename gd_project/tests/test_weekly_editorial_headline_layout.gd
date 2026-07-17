extends SceneTree

const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const OUT_PATH := "res://../docs/screenshots/2026-07-15-weekly-editorial-headline-alignment/headline-layout-audit.json"

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
	await _frames(5)

	var editorial = scene.editorial_phase
	var main: Dictionary = editorial._slot_nodes["front-main"]
	var secondary: Dictionary = editorial._slot_nodes["front-side"]
	var compact: Dictionary = editorial._slot_nodes["feature-1"]
	var tall: Dictionary = editorial._slot_nodes["inner-1"]

	_check("main_headline_carrier_matches_contract", main.title_carrier.position == Vector2(16, 14) and main.title_carrier.size == Vector2(410, 68))
	_check("secondary_headline_carrier_matches_contract", secondary.title_carrier.position == Vector2(16, 14) and secondary.title_carrier.size == Vector2(410, 54))
	_check("headlines_use_eight_pixel_inner_padding", main.title.position == Vector2(8, 0) and main.title.size == Vector2(394, 68) and secondary.title.position == Vector2(8, 0) and secondary.title.size == Vector2(394, 54))
	_check("all_slot_titles_are_vertically_centered", _all_titles_match(editorial, func(label: Label) -> bool: return label.vertical_alignment == VERTICAL_ALIGNMENT_CENTER))
	_check("all_slot_titles_wrap_chinese_by_character", _all_titles_match(editorial, func(label: Label) -> bool: return label.autowrap_mode == TextServer.AUTOWRAP_ARBITRARY))
	_check("all_slot_titles_are_limited_to_two_lines", _all_titles_match(editorial, func(label: Label) -> bool: return label.max_lines_visible == 2))
	_check("all_slot_titles_use_compact_line_spacing", _all_titles_match(editorial, func(label: Label) -> bool: return label.get_theme_constant("line_spacing") == 0))
	_check("full_titles_are_preserved", main.title.text == str(scene.run_state.article_candidates[0].title) and secondary.title.text == str(scene.run_state.article_candidates[1].title))
	_check("long_headlines_use_both_available_lines", main.title.get_visible_line_count() == 2 and secondary.title.get_visible_line_count() == 2)
	_check("visible_titles_do_not_exceed_two_lines", compact.title.get_visible_line_count() <= 2 and tall.title.get_visible_line_count() <= 2)
	_check("headline_carriers_do_not_touch_photos", main.title_carrier.position.y + main.title_carrier.size.y <= main.story_texture.position.y and secondary.title_carrier.position.y + secondary.title_carrier.size.y <= secondary.story_texture.position.y)
	_check("photo_rects_remain_frozen", main.story_texture.position == Vector2(16, 92) and main.story_texture.size == Vector2(410, 218) and secondary.story_texture.position == Vector2(16, 78) and secondary.story_texture.size == Vector2(410, 210))
	_check("standard_story_title_rects_remain_frozen", compact.title.position == Vector2(12, 8) and compact.title.size == Vector2(189, 48) and tall.title.position == Vector2(12, 8) and tall.title.size == Vector2(189, 50))

	var passed := true
	for check in _checks:
		if not bool(check.get("pass", false)):
			passed = false
	var result := {
		"passed": passed,
		"check_count": _checks.size(),
		"checks": _checks,
		"metrics": {
			"main": _label_metrics(main.title),
			"secondary": _label_metrics(secondary.title),
		},
	}
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_PATH).get_base_dir())
	FileAccess.open(ProjectSettings.globalize_path(OUT_PATH), FileAccess.WRITE).store_string(JSON.stringify(result, "  ") + "\n")
	if not passed:
		push_error("weekly editorial headline layout audit failed")
	quit(0 if passed else 1)


func _all_titles_match(editorial: Control, predicate: Callable) -> bool:
	for nodes in editorial._slot_nodes.values():
		if not bool(predicate.call(nodes.title as Label)):
			return false
	return true


func _check(id: String, condition: bool) -> void:
	_checks.append({"id": id, "pass": condition})


func _label_metrics(label: Label) -> Dictionary:
	return {
		"characters": label.text.length(),
		"line_count": label.get_line_count(),
		"line_height": label.get_line_height(),
		"visible_line_count": label.get_visible_line_count(),
		"size": [label.size.x, label.size.y],
		"minimum_size": [label.get_minimum_size().x, label.get_minimum_size().y],
	}


func _set_fixture(scene: Control) -> void:
	scene.run_state.article_candidates.assign([
		{"id": 1001, "title": "M330 末班车在不存在的站台停了三秒并带回一份无人签收的夜班记录", "tags": ["Gossip", "Humor"], "quality": "Gold", "base_value": 540, "negatives": [], "source": "material_inventory"},
		{"id": 1002, "title": "51 区夜班货车携带会呼吸的路牌驶入封锁区后再次失去联络", "tags": ["Military", "Economy"], "quality": "Gold", "base_value": 500, "negatives": [], "source": "material_inventory"},
		{"id": 1003, "title": "港口广播连续七晚播报明天的潮汐", "tags": ["Gossip", "Shopping"], "quality": "Silver", "base_value": 340, "negatives": [], "source": "material_inventory"},
		{"id": 1004, "title": "罗斯威尔档案第十四页拒绝被复印", "tags": ["Politics", "Military"], "quality": "Silver", "base_value": 320, "negatives": [], "source": "material_inventory"},
		{"id": 1005, "title": "市政厅新增了一个不存在的影子部门", "tags": ["Politics", "Humor"], "quality": "Bronze", "base_value": 220, "negatives": [], "source": "filler"},
		{"id": 1006, "title": "街区猫群一致拒绝经过蓝色电话亭", "tags": ["Pets", "Gossip"], "quality": "Bronze", "base_value": 190, "negatives": [], "source": "filler"},
	])
	scene.run_state.slot_assignment = {"front-main": 1001, "front-side": 1002, "feature-1": 1003, "feature-2": 1004, "inner-1": 1005, "inner-2": -1}
	scene.selected_article_id = -1


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame
