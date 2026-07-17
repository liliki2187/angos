extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-14-weekly-editorial-benchmark-landing"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	root.size = Vector2i(1920, 1080)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))

	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	var scene := packed.instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	scene.offset_left = 0.0
	scene.offset_top = 0.0
	scene.offset_right = 0.0
	scene.offset_bottom = 0.0

	await _settle_frames(4)
	scene._on_advance_phase_pressed()
	await _settle_frames(3)
	scene._enter_editorial_phase()
	await _settle_frames(3)

	_set_editorial_fixture(scene)
	scene._refresh_all()
	await _settle_frames(5)
	_save_png("01-editorial-current-runtime.png")
	quit(0)

func _set_editorial_fixture(scene: Control) -> void:
	scene.run_state.article_candidates.assign([
		{"id": 1001, "title": "M330 末班车在不存在的站台停了三秒", "tags": ["Gossip", "Humor"], "quality": "Gold", "base_value": 540, "negatives": [], "source": "material_inventory"},
		{"id": 1002, "title": "51 区夜班货车携带会呼吸的路牌", "tags": ["Military", "Economy"], "quality": "Gold", "base_value": 500, "negatives": [], "source": "material_inventory"},
		{"id": 1003, "title": "港口广播连续七晚播报明天的潮汐", "tags": ["Gossip", "Shopping"], "quality": "Silver", "base_value": 340, "negatives": [], "source": "material_inventory"},
		{"id": 1004, "title": "罗斯威尔档案第十四页拒绝被复印", "tags": ["Politics", "Military"], "quality": "Silver", "base_value": 320, "negatives": ["thin_source"], "source": "material_inventory"},
		{"id": 1005, "title": "市政厅新增了一个不存在的影子部门", "tags": ["Politics", "Humor"], "quality": "Bronze", "base_value": 220, "negatives": [], "source": "filler"},
		{"id": 1006, "title": "街区猫群一致拒绝经过蓝色电话亭", "tags": ["Pets", "Gossip"], "quality": "Bronze", "base_value": 190, "negatives": [], "source": "filler"},
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
	scene.selected_article_id = 1006

func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _save_png(file_name: String) -> void:
	var image := root.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
