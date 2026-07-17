extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-15-weekly-editorial-headline-autofit"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	root.size = Vector2i(1920, 1080)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	var scene := (load(WEEKLY_RUN_SCENE) as PackedScene).instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	await _frames(4)
	scene._on_advance_phase_pressed()
	await _frames(3)
	scene._enter_editorial_phase()
	await _frames(4)
	_set_fixture(scene)
	scene._refresh_all()
	await _frames(6)

	var mixed_image := root.get_texture().get_image()
	_save_image(mixed_image, "01-godot-headline-autofit-mixed-full.png")
	_save_image(mixed_image.get_region(Rect2i(430, 145, 1060, 555)), "02-godot-headline-autofit-mixed-crop.png")

	var main: Dictionary = scene.editorial_phase._slot_nodes["front-main"]
	var extreme_title := "M330末班车在不存在的站台停了三秒并带回无人签收的夜班记录随后驶入封锁区且整座城市的钟表同时倒转"
	scene.editorial_phase._fit_headline(main.title, extreme_title, "main")
	await _frames(4)
	var extreme_image := root.get_texture().get_image()
	_save_image(extreme_image.get_region(Rect2i(430, 210, 540, 455)), "03-godot-headline-autofit-extreme-crop.png")
	quit(0)


func _set_fixture(scene: Control) -> void:
	scene.run_state.article_candidates.assign([
		{"id": 1001, "title": "M330末班车停站", "tags": ["Gossip", "Humor"], "quality": "Gold", "base_value": 540, "negatives": [], "source": "material_inventory"},
		{"id": 1002, "title": "51区货车载着会呼吸的路牌驶入封锁区后再次失去联络", "tags": ["Military", "Economy"], "quality": "Gold", "base_value": 500, "negatives": [], "source": "material_inventory"},
		{"id": 1003, "title": "港口广播连续七晚播报明天的潮汐", "tags": ["Gossip", "Shopping"], "quality": "Silver", "base_value": 340, "negatives": [], "source": "material_inventory"},
		{"id": 1004, "title": "档案拒绝复印", "tags": ["Politics", "Military"], "quality": "Silver", "base_value": 320, "negatives": ["thin_source"], "source": "material_inventory"},
		{"id": 1005, "title": "市政厅新增了一个不存在的影子部门", "tags": ["Politics", "Humor"], "quality": "Bronze", "base_value": 220, "negatives": [], "source": "filler"},
		{"id": 1006, "title": "街区猫群拒绝经过电话亭", "tags": ["Pets", "Gossip"], "quality": "Bronze", "base_value": 190, "negatives": [], "source": "filler"},
	])
	scene.run_state.new_material_ids.assign(["m330", "n51", "harbor", "roswell"])
	scene.run_state.slot_assignment = {
		"front-main": 1001,
		"front-side": 1002,
		"feature-1": 1003,
		"feature-2": 1004,
		"inner-1": 1005,
		"inner-2": -1,
	}
	scene.selected_article_id = -1


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _save_image(image: Image, file_name: String) -> void:
	var error := image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
	if error != OK:
		push_error("截图写入失败：%s (%s)" % [file_name, error_string(error)])
