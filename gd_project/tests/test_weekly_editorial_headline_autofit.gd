extends SceneTree

const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const OUT_PATH := "res://../docs/screenshots/2026-07-15-weekly-editorial-headline-autofit/headline-autofit-audit.json"

var _checks := []
var _cases := {}


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

	var editorial = scene.editorial_phase
	var main: Dictionary = editorial._slot_nodes["front-main"]
	var secondary: Dictionary = editorial._slot_nodes["front-side"]
	var standard: Dictionary = editorial._slot_nodes["feature-1"]

	_cases.main_single = await _headline_case(editorial, main.title, "main", "M330末班车停站")
	_cases.secondary_single = await _headline_case(editorial, secondary.title, "secondary", "51区货车失联")
	_cases.standard_single = await _headline_case(editorial, standard.title, "compact", "港口潮汐异常")
	_check("single_line_uses_role_maximums", _cases.main_single.font_size == 32 and _cases.secondary_single.font_size == 25 and _cases.standard_single.font_size == 18)
	_check("single_line_cases_remain_single", _cases.main_single.visible_lines == 1 and _cases.secondary_single.visible_lines == 1 and _cases.standard_single.visible_lines == 1)

	_cases.main_double = await _headline_case(editorial, main.title, "main", "M330末班车在不存在的站台停了三秒")
	_cases.secondary_double = await _headline_case(editorial, secondary.title, "secondary", "51区货车载着会呼吸的路牌驶入封锁区后再次失去联络")
	_cases.standard_double = await _headline_case(editorial, standard.title, "compact", "港口广播连续七晚播报明天的潮汐")
	_check("double_line_cases_use_double_ladders", _cases.main_double.font_size in [24, 22] and _cases.secondary_double.font_size in [18, 17] and _cases.standard_double.font_size == 14)
	_check("double_line_cases_show_two_lines", _cases.main_double.visible_lines == 2 and _cases.secondary_double.visible_lines == 2 and _cases.standard_double.visible_lines == 2)

	var extreme_title := "M330末班车在不存在的站台停了三秒并带回无人签收的夜班记录随后驶入封锁区且整座城市的钟表同时倒转"
	_cases.main_extreme = await _headline_case(editorial, main.title, "main", extreme_title)
	_check("extreme_title_uses_lowest_fallback", _cases.main_extreme.font_size == 22 and _cases.main_extreme.fit_mode == "fallback")
	_check("extreme_title_keeps_source_and_clamps_to_two_lines", main.title.text == extreme_title and main.title.get_line_count() > 2 and main.title.get_visible_line_count() == 2 and main.title.text_overrun_behavior == TextServer.OVERRUN_TRIM_ELLIPSIS)

	var stable_size: int = main.title.get_theme_font_size("font_size")
	var stable_mode: String = str(main.title.get_meta("headline_fit_mode"))
	var stable := true
	for _index in range(100):
		editorial._fit_headline(main.title, extreme_title, "main")
		if main.title.get_theme_font_size("font_size") != stable_size or str(main.title.get_meta("headline_fit_mode")) != stable_mode:
			stable = false
			break
	_check("repeated_fit_is_deterministic", stable)

	_check("title_and_photo_rects_stay_frozen", main.title_carrier.position == Vector2(16, 14) and main.title_carrier.size == Vector2(410, 68) and main.story_texture.position == Vector2(16, 92) and main.story_texture.size == Vector2(410, 218) and secondary.title_carrier.position == Vector2(16, 14) and secondary.title_carrier.size == Vector2(410, 54) and secondary.story_texture.position == Vector2(16, 78) and secondary.story_texture.size == Vector2(410, 210))

	var passed := true
	for check in _checks:
		if not bool(check.pass):
			passed = false
	var result := {"passed": passed, "check_count": _checks.size(), "checks": _checks, "cases": _cases}
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_PATH).get_base_dir())
	FileAccess.open(ProjectSettings.globalize_path(OUT_PATH), FileAccess.WRITE).store_string(JSON.stringify(result, "  ") + "\n")
	if not passed:
		push_error("weekly editorial headline autofit audit failed")
	quit(0 if passed else 1)


func _headline_case(editorial: Control, label: Label, role: String, value: String) -> Dictionary:
	editorial._fit_headline(label, value, role)
	await _frames(2)
	return {
		"text": value,
		"font_size": label.get_theme_font_size("font_size"),
		"fit_mode": str(label.get_meta("headline_fit_mode")),
		"line_count": label.get_line_count(),
		"visible_lines": label.get_visible_line_count(),
	}


func _check(id: String, condition: bool) -> void:
	_checks.append({"id": id, "pass": condition})


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame
