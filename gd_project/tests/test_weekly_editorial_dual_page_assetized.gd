extends SceneTree

const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"
const OUT_PATH := "res://../docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/interaction-audit.json"

var _checks := []


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	root.size = Vector2i(1920, 1080)
	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	var scene := packed.instantiate() as Control
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

	var editorial = scene.editorial_phase
	var secondary_nodes: Dictionary = editorial._slot_nodes["front-side"]
	_check("dual_page_is_only_layout", editorial._candidate_panel.visible and editorial.find_child("ContextPageSwitch", true, false) == null)
	_check("three_column_geometry", editorial._candidate_panel.global_position.round() == Vector2(80, 96) and editorial._candidate_panel.size.round() == Vector2(320, 920) and editorial._edition_panel.global_position.round() == Vector2(420, 96) and editorial._edition_panel.size.round() == Vector2(1040, 920) and editorial._review_panel.global_position.round() == Vector2(1480, 96) and editorial._review_panel.size.round() == Vector2(360, 920))
	_check("dual_pages_keep_frozen_geometry", editorial._page_nodes.left.global_position.round() == Vector2(435, 184) and editorial._page_nodes.left.size.round() == Vector2(490, 800) and editorial._page_nodes.right.global_position.round() == Vector2(955, 184) and editorial._page_nodes.right.size.round() == Vector2(490, 800))
	var left_style := editorial._page_nodes.left.get_theme_stylebox("panel") as StyleBoxFlat
	var right_style := editorial._page_nodes.right.get_theme_stylebox("panel") as StyleBoxFlat
	_check("both_pages_share_same_paper_color", left_style.bg_color == right_style.bg_color and left_style.border_color == right_style.border_color)
	_check("main_secondary_hierarchy_uses_geometry_not_page_color", editorial._slot_nodes["front-main"].root.size == Vector2(442, 374) and secondary_nodes.root.size == Vector2(442, 342))
	_check("secondary_head_uses_generated_same_paper_shell", secondary_nodes.base_texture != null and (secondary_nodes.base_texture as TextureRect).texture != null)
	_check("secondary_head_uses_area51_story", secondary_nodes.story_texture != null and (secondary_nodes.story_texture as TextureRect).texture != null and (secondary_nodes.story_texture as TextureRect).visible)
	_check("secondary_story_fallback_is_mutually_exclusive", secondary_nodes.story_fallback != null and not (secondary_nodes.story_fallback as ColorRect).visible)
	_check("secondary_headline_contract_rect", (secondary_nodes.title_carrier as Control).position.round() == Vector2(16, 14) and (secondary_nodes.title_carrier as Control).size.round() == Vector2(410, 54))
	_check("secondary_meta_contract_rect", (secondary_nodes.meta_carrier as Control).position.round() == Vector2(16, 300) and (secondary_nodes.meta_carrier as Control).size.round() == Vector2(360, 30))
	_check("secondary_story_contract_rect", (secondary_nodes.story_texture as TextureRect).position.round() == Vector2(16, 78) and (secondary_nodes.story_texture as TextureRect).size.round() == Vector2(410, 210))
	_check("persistent_status_badges_removed", editorial.find_child("StatusBadge", true, false) == null)
	_check("persistent_return_buttons_removed", editorial.find_child("ReturnToCandidates", true, false) == null)
	_check("persistent_instruction_removed", not _contains_label_text(editorial._candidate_panel, "点击候选拿稿"))
	_check("placed_articles_not_duplicated_in_candidate_pool", editorial._article_buttons.size() == 1)
	_check("idle_has_zero_replace_buttons", not editorial._context_replace_button.visible)

	editorial._on_slot_pressed("front-side")
	await _frames(2)
	var first_replace_position: Vector2 = editorial._context_replace_button.position
	_check("click_occupied_shows_one_local_replace", editorial._context_replace_button.visible and editorial._focused_slot_id == "front-side" and _visible_context_replace_count(editorial) == 1)
	_check("local_replace_uses_frozen_action_rect", editorial._context_replace_button.size == Vector2(44, 44) and first_replace_position.round() == Vector2(949, 470))
	editorial._on_slot_pressed("front-main")
	await _frames(2)
	_check("click_other_slot_moves_single_replace", editorial._context_replace_button.visible and editorial._focused_slot_id == "front-main" and _visible_context_replace_count(editorial) == 1 and editorial._context_replace_button.position != first_replace_position)
	editorial._cancel_transients()
	await _frames(2)
	_check("cancel_clears_local_replace", not editorial._context_replace_button.visible and editorial._focused_slot_id == "")

	var before_armed: Dictionary = scene.run_state.slot_assignment.duplicate(true)
	editorial._on_slot_pressed("front-side")
	editorial._on_context_replace_pressed()
	await _frames(2)
	_check("replace_armed_hides_button_without_writing", editorial._replace_target_slot_id == "front-side" and not editorial._context_replace_button.visible and scene.run_state.slot_assignment == before_armed)
	editorial._on_candidate_pressed(1006)
	await _frames(3)
	_check("armed_replace_commits_candidate_and_returns_old", int(scene.run_state.slot_assignment["front-side"]) == 1006 and not scene._is_article_placed(1002))
	_check("replace_completion_clears_transients", editorial._replace_target_slot_id == "" and editorial._focused_slot_id == "" and not editorial._context_replace_button.visible)

	_set_fixture(scene)
	scene._refresh_all()
	await _frames(3)
	scene._on_article_selected(1006)
	await _frames(2)
	editorial._on_slot_pressed("front-side")
	await _frames(2)
	_check("candidate_first_replace_pending_has_one_button", scene.selected_article_id == 1006 and editorial._context_replace_button.visible and _visible_context_replace_count(editorial) == 1)
	editorial._on_context_replace_pressed()
	await _frames(3)
	_check("candidate_first_confirm_replaces_atomically", int(scene.run_state.slot_assignment["front-side"]) == 1006 and not scene._is_article_placed(1002) and scene.selected_article_id == -1)

	_set_fixture(scene)
	scene._refresh_all()
	await _frames(3)
	scene._on_article_selected(1006)
	editorial._on_slot_pressed("inner-2")
	await _frames(3)
	_check("candidate_click_to_empty_slot_is_direct", int(scene.run_state.slot_assignment["inner-2"]) == 1006 and scene.selected_article_id == -1)

	_set_fixture(scene)
	scene._refresh_all()
	await _frames(3)
	var candidate_drag := {"source_kind": "candidate", "article_id": 1006, "source_slot_id": ""}
	editorial._on_slot_pressed("front-side")
	editorial._on_drag_started(candidate_drag)
	editorial._on_drag_hovered("slot", "front-side")
	await _frames(2)
	_check("dragging_hides_replace_button", editorial._drag_active and not editorial._context_replace_button.visible and _visible_context_replace_count(editorial) == 0)
	_check("drag_hover_is_local_and_text_free", editorial._drag_hover_slot_id == "front-side" and editorial.find_child("StatusBadge", true, false) == null)
	editorial._on_article_dropped(candidate_drag, "slot", "front-side")
	await _frames(3)
	_check("candidate_drag_replaces_and_returns_old", int(scene.run_state.slot_assignment["front-side"]) == 1006 and not scene._is_article_placed(1002))

	_set_fixture(scene)
	scene._refresh_all()
	await _frames(3)
	var slot_drag := {"source_kind": "slot", "article_id": 1001, "source_slot_id": "front-main"}
	editorial._on_drag_started(slot_drag)
	editorial._on_article_dropped(slot_drag, "slot", "front-side")
	await _frames(3)
	_check("occupied_to_occupied_is_atomic_swap", int(scene.run_state.slot_assignment["front-main"]) == 1002 and int(scene.run_state.slot_assignment["front-side"]) == 1001)
	_check("swap_keeps_filled_count", _filled_count(scene.run_state.slot_assignment) == 5)

	_set_fixture(scene)
	scene._refresh_all()
	await _frames(2)
	editorial._on_drag_started(slot_drag)
	editorial._on_article_dropped(slot_drag, "slot", "inner-2")
	await _frames(3)
	_check("occupied_to_empty_moves_article", int(scene.run_state.slot_assignment["front-main"]) == -1 and int(scene.run_state.slot_assignment["inner-2"]) == 1001)

	_set_fixture(scene)
	scene._refresh_all()
	await _frames(2)
	editorial._on_drag_started(slot_drag)
	editorial._on_drag_hovered("candidate_pool", "")
	await _frames(2)
	_check("candidate_pool_becomes_drop_target_only_during_drag", editorial._candidate_panel.drop_enabled and editorial._drag_hover_kind == "candidate_pool")
	editorial._on_article_dropped(slot_drag, "candidate_pool", "")
	await _frames(3)
	_check("slot_drag_to_candidate_pool_removes_from_page", int(scene.run_state.slot_assignment["front-main"]) == -1 and not scene._is_article_placed(1001))
	_check("removed_article_reappears_once_in_candidates", editorial._article_buttons.size() == 2)

	_set_fixture(scene)
	scene._refresh_all()
	await _frames(2)
	var same_slot_before: Dictionary = scene.run_state.slot_assignment.duplicate(true)
	scene._apply_editorial_transfer("slot", 1001, "front-main", "slot", "front-main")
	_check("same_slot_drop_is_noop", scene.run_state.slot_assignment == same_slot_before)
	scene._apply_editorial_transfer("candidate", 1006, "", "candidate_pool", "")
	_check("candidate_to_candidate_pool_is_illegal_noop", scene.run_state.slot_assignment == same_slot_before)
	_check("assignment_invariant_is_unique", scene._editorial_assignment_is_unique(scene.run_state.slot_assignment))

	editorial._on_slot_pressed("front-side")
	var snapshot: Dictionary = scene.run_state.slot_assignment.duplicate(true)
	editorial.show_confirmation()
	await _frames(3)
	_check("confirmation_clears_all_transients", editorial._confirmation_open and not editorial._context_replace_button.visible and not editorial._drag_active and editorial._focused_slot_id == "")
	_check("confirmation_freezes_drag_and_click", secondary_nodes.target.disabled and not editorial._candidate_panel.drop_enabled)
	_check("confirmation_reads_unchanged_snapshot", scene.run_state.slot_assignment == snapshot)
	_check("both_pages_remain_visible_in_confirmation", editorial._page_nodes.left.visible and editorial._page_nodes.right.visible)

	var passed := true
	for check in _checks:
		if not bool(check.get("pass", false)):
			passed = false
	var result := {
		"passed": passed,
		"checks": _checks,
		"check_count": _checks.size(),
		"final_assignments": scene.run_state.slot_assignment,
		"final_layout_mode": "dual_page",
		"replace_button_contract": {"idle": 0, "focused": 1, "dragging": 0, "confirmation": 0, "maximum": 1},
	}
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_PATH).get_base_dir())
	var file := FileAccess.open(ProjectSettings.globalize_path(OUT_PATH), FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "  ") + "\n")
	file.close()
	if not passed:
		push_error("weekly editorial same-paper local-replace audit failed")
	quit(0 if passed else 1)


func _check(id: String, condition: bool) -> void:
	_checks.append({"id": id, "pass": condition})


func _contains_label_text(node: Node, text_value: String) -> bool:
	if node is Label and str((node as Label).text).contains(text_value):
		return true
	for child in node.get_children():
		if _contains_label_text(child, text_value):
			return true
	return false


func _visible_context_replace_count(node: Node) -> int:
	var count := 0
	if node is Button and node.name == "ContextReplaceButton" and (node as Button).visible:
		count += 1
	for child in node.get_children():
		count += _visible_context_replace_count(child)
	return count


func _filled_count(assignments: Dictionary) -> int:
	var count := 0
	for article_id in assignments.values():
		if int(article_id) != -1:
			count += 1
	return count


func _set_fixture(scene: Control) -> void:
	scene.run_state.article_candidates.assign([
		{"id": 1001, "title": "M330 末班车在不存在的站台停了三秒", "tags": ["Gossip", "Humor"], "quality": "Gold", "base_value": 540, "negatives": [], "source": "material_inventory"},
		{"id": 1002, "title": "51 区夜班货车携带会呼吸的路牌", "tags": ["Military", "Economy"], "quality": "Gold", "base_value": 500, "negatives": [], "source": "material_inventory"},
		{"id": 1003, "title": "港口广播连续七晚播报明天的潮汐", "tags": ["Gossip", "Shopping"], "quality": "Silver", "base_value": 340, "negatives": [], "source": "material_inventory"},
		{"id": 1004, "title": "罗斯威尔档案第十四页拒绝被复印", "tags": ["Politics", "Military"], "quality": "Silver", "base_value": 320, "negatives": ["thin_source"], "source": "material_inventory"},
		{"id": 1005, "title": "市政厅新增了一个不存在的影子部门", "tags": ["Politics", "Humor"], "quality": "Bronze", "base_value": 220, "negatives": [], "source": "filler"},
		{"id": 1006, "title": "街区猫群一致拒绝经过蓝色电话亭", "tags": ["Pets", "Gossip"], "quality": "Bronze", "base_value": 190, "negatives": [], "source": "filler"},
	])
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
