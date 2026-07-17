extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace"
const FRAME_DIR := OUT_DIR + "/dynamic-frames"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

var _layout_audit := {}


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	root.size = Vector2i(1920, 1080)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(FRAME_DIR))

	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	var scene := packed.instantiate() as Control
	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)

	await _settle_frames(4)
	scene._on_advance_phase_pressed()
	await _settle_frames(3)
	scene._enter_editorial_phase()
	await _settle_frames(4)
	_set_editorial_fixture(scene)
	scene._refresh_all()
	await _settle_frames(6)

	var editorial = scene.editorial_phase
	_save_png("%s/01-godot-same-paper-default.png" % OUT_DIR)
	_save_png("%s/frame_01_default.png" % FRAME_DIR)
	_record_layout(scene, "default")

	editorial._on_slot_pressed("front-side")
	await _settle_frames(5)
	_save_png("%s/02-godot-single-local-replace.png" % OUT_DIR)
	_save_png("%s/frame_02_slot_focused.png" % FRAME_DIR)
	_record_layout(scene, "slot_focused")

	editorial._on_context_replace_pressed()
	await _settle_frames(4)
	_save_png("%s/frame_03_replace_armed.png" % FRAME_DIR)

	editorial._cancel_transients()
	scene._on_article_selected(1006)
	await _settle_frames(4)
	_save_png("%s/frame_04_candidate_selected.png" % FRAME_DIR)

	editorial._on_slot_pressed("front-side")
	await _settle_frames(4)
	_save_png("%s/frame_05_replace_pending.png" % FRAME_DIR)

	var candidate_drag := {"source_kind": "candidate", "article_id": 1006, "source_slot_id": ""}
	editorial._on_drag_started(candidate_drag)
	await _settle_frames(4)
	_save_png("%s/frame_06_drag_started.png" % FRAME_DIR)
	editorial._on_drag_hovered("slot", "front-side")
	await _settle_frames(5)
	_save_png("%s/03-godot-drag-hover.png" % OUT_DIR)
	_save_png("%s/frame_07_drag_hover.png" % FRAME_DIR)
	_record_layout(scene, "drag_hover")

	editorial._on_article_dropped(candidate_drag, "slot", "front-side")
	await _settle_frames(5)
	_save_png("%s/frame_08_candidate_replaced.png" % FRAME_DIR)

	var slot_drag := {"source_kind": "slot", "article_id": 1001, "source_slot_id": "front-main"}
	editorial._on_drag_started(slot_drag)
	editorial._on_drag_hovered("candidate_pool", "")
	await _settle_frames(5)
	_save_png("%s/frame_09_drag_to_candidate_pool.png" % FRAME_DIR)
	editorial._on_article_dropped(slot_drag, "candidate_pool", "")
	await _settle_frames(5)
	_save_png("%s/frame_10_returned_to_candidates.png" % FRAME_DIR)

	editorial.show_confirmation()
	await _settle_frames(4)
	_record_layout(scene, "confirmation")
	_save_audit()
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
	scene.selected_article_id = -1


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _save_png(resource_path: String) -> void:
	var image := root.get_texture().get_image()
	var error := image.save_png(ProjectSettings.globalize_path(resource_path))
	if error != OK:
		push_error("截图写入失败：%s (%s)" % [resource_path, error_string(error)])


func _record_layout(scene: Control, state_id: String) -> void:
	var editorial = scene.editorial_phase
	_layout_audit[state_id] = {
		"layout_mode": "dual_page",
		"held_article_id": int(editorial._payload.get("held_article_id", -1)),
		"focused_slot_id": editorial._focused_slot_id,
		"replace_target_slot_id": editorial._replace_target_slot_id,
		"drag_active": editorial._drag_active,
		"drag_hover_kind": editorial._drag_hover_kind,
		"drag_hover_slot_id": editorial._drag_hover_slot_id,
		"context_replace_visible": editorial._context_replace_button.visible,
		"candidate_panel": _control_rect(editorial._candidate_panel),
		"edition_panel": _control_rect(editorial._edition_panel),
		"review_panel": _control_rect(editorial._review_panel),
		"masthead": _control_rect(editorial._masthead),
		"left_page": _control_rect(editorial._page_nodes.left),
		"right_page": _control_rect(editorial._page_nodes.right),
	}


func _control_rect(control: Control) -> Dictionary:
	return {
		"visible": control.visible,
		"global_position": [roundi(control.global_position.x), roundi(control.global_position.y)],
		"size": [roundi(control.size.x), roundi(control.size.y)],
		"scale": [snappedf(control.scale.x, 0.001), snappedf(control.scale.y, 0.001)],
	}


func _save_audit() -> void:
	var path := ProjectSettings.globalize_path("%s/layout-audit.json" % OUT_DIR)
	FileAccess.open(path, FileAccess.WRITE).store_string(JSON.stringify(_layout_audit, "  ") + "\n")
