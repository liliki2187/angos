extends SceneTree

const BoardV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd")
const ManifestV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd")

var out_dir := "res://../docs/screenshots/2026-07-21-region-task-single-compound-probe-v4"
var frame_dir := out_dir + "/frames-state-chain-v4"
var static_output := out_dir + "/06-godot-three-state-1x-v4.png"

var pin_texture := "res://tests/fixtures/region_task_compound_probe_v4/rt-task-pin-permanent-default-v4-3x.png"
var default_texture := "res://tests/fixtures/region_task_compound_probe_v4/rt-task-compound-permanent-default-right-v4-3x.png"
var selected_texture := "res://tests/fixtures/region_task_compound_probe_v4/rt-task-compound-permanent-selected-right-v4-3x.png"

const INK := Color("17252a")
const META_INK := Color("405157")
const STATE_INK := Color("d9dfb5")


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	_configure_variant()
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(out_dir))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(frame_dir))
	await _capture_static_three_state()
	await _capture_dynamic_state_chain()
	print("capture_region_task_compound_state_chain_v4.gd OK: %s" % static_output)
	quit(0)


func _configure_variant() -> void:
	var args := OS.get_cmdline_user_args()
	if "--variant=v5b" in args:
		out_dir = "res://../docs/screenshots/2026-07-21-region-task-state-chain-v5b"
		frame_dir = out_dir + "/frames-state-chain-v5b"
		static_output = out_dir + "/02-godot-three-state-1x-v5b.png"
		pin_texture = "res://tests/fixtures/region_task_compound_probe_v5b/rt-task-pin-permanent-default-v5b-3x.png"
		default_texture = "res://tests/fixtures/region_task_compound_probe_v5b/rt-task-compound-permanent-default-right-v5b-3x.png"
		selected_texture = "res://tests/fixtures/region_task_compound_probe_v5b/rt-task-compound-permanent-selected-underlay-right-v5b-3x.png"
	elif "--variant=v4b" in args:
		out_dir = "res://../docs/screenshots/2026-07-21-region-task-state-chain-v4b"
		frame_dir = out_dir + "/frames-state-chain-v4b"
		static_output = out_dir + "/02-godot-three-state-1x-v4b.png"
		pin_texture = "res://tests/fixtures/region_task_compound_probe_v4b/rt-task-pin-permanent-default-v4b-3x.png"
		default_texture = "res://tests/fixtures/region_task_compound_probe_v4b/rt-task-compound-permanent-default-right-v4b-3x.png"
		selected_texture = "res://tests/fixtures/region_task_compound_probe_v4b/rt-task-compound-permanent-selected-right-v4b-3x.png"


func _capture_static_three_state() -> void:
	var viewport := _make_viewport()
	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1920, 1080)
	await _settle_frames(4)
	board.render(_three_state_payload())
	await _settle_frames(6)

	for spec in [
		{"id": "state_idle", "state": "idle", "label": "DEFAULT / 未选中"},
		{"id": "state_hover", "state": "hover", "label": "HOVER / 临时展开"},
		{"id": "state_selected", "state": "selected", "label": "SELECTED / 持续显示"},
	]:
		var original := board.find_child("EventPin_%s" % spec.id, true, false) as Control
		if original == null:
			push_error("Missing runtime pin for static state: %s" % spec.id)
			continue
		var parent := original.get_parent() as Control
		var at_position := original.position
		original.visible = false
		var rig := _add_state_rig(parent, at_position, str(spec.label))
		_apply_stable_state(rig, str(spec.state))

	await _settle_frames(8)
	await _save_full_png(viewport, static_output)
	await _dispose_viewport(viewport)


func _capture_dynamic_state_chain() -> void:
	var viewport := _make_viewport()
	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1920, 1080)
	await _settle_frames(4)
	board.render(_dynamic_payload())
	await _settle_frames(6)
	var original := board.find_child("EventPin_state_demo", true, false) as Control
	if original == null:
		push_error("Missing runtime pin for dynamic state chain.")
		await _dispose_viewport(viewport)
		return
	var parent := original.get_parent() as Control
	var at_position := original.position
	original.visible = false
	var rig := _add_state_rig(parent, at_position, "IDLE / DEFAULT")
	_apply_stable_state(rig, "idle")
	await _settle_frames(4)

	var frame_index := 0
	frame_index = await _hold_frames(viewport, rig, frame_index, 8, "IDLE / DEFAULT")
	frame_index = await _transition_idle_to_hover(viewport, rig, frame_index, 3)
	frame_index = await _hold_frames(viewport, rig, frame_index, 10, "HOVER / 临时展开")
	frame_index = await _transition_hover_to_selected(viewport, rig, frame_index, 3)
	frame_index = await _hold_frames(viewport, rig, frame_index, 10, "SELECTED / 已选中")
	frame_index = await _hold_frames(viewport, rig, frame_index, 10, "SELECTED / 指针移出仍保持")
	frame_index = await _transition_selected_to_hover(viewport, rig, frame_index, 3)
	frame_index = await _transition_hover_to_idle(viewport, rig, frame_index, 3)
	await _hold_frames(viewport, rig, frame_index, 8, "IDLE / 取消选中")
	await _dispose_viewport(viewport)


func _add_state_rig(parent: Control, at_position: Vector2, state_label: String) -> Dictionary:
	var rig := Control.new()
	rig.name = "CompoundStateRigV4"
	rig.position = at_position
	rig.size = Vector2(278, 80)
	rig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rig.z_index = 20
	parent.add_child(rig)

	var selected := _make_texture_rect(rig, selected_texture, Vector2.ZERO, Vector2(278, 80), 0)
	var default_compound := _make_texture_rect(rig, default_texture, Vector2.ZERO, Vector2(278, 80), 1)
	var pin_only := _make_texture_rect(rig, pin_texture, Vector2(4, 0), Vector2(64, 80), 2)

	var icon_atlas := ManifestV2.load_asset_texture("rt2_task_pin_kind_icons_v3")
	var icon := TextureRect.new()
	icon.name = "RuntimeKindIcon"
	icon.position = Vector2(22, 14)
	icon.size = Vector2(28, 28)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	icon.z_index = 4
	if icon_atlas != null:
		var icon_texture := AtlasTexture.new()
		icon_texture.atlas = icon_atlas
		icon_texture.region = Rect2(0, 0, 84, 84)
		icon.texture = icon_texture
	rig.add_child(icon)

	var title := _make_label(rig, "罗斯威尔档案残页", Rect2(92, 12, 166, 28), 15, INK, 4)
	title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	var meta := _make_label(rig, "常驻调查 · 1天", Rect2(92, 40, 166, 22), 12, META_INK, 4)
	meta.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	var audit_label := _make_label(rig, state_label, Rect2(0, -30, 278, 24), 14, STATE_INK, 5)
	audit_label.add_theme_constant_override("outline_size", 4)
	audit_label.add_theme_color_override("font_outline_color", Color("071d2e"))

	return {
		"root": rig,
		"pin": pin_only,
		"default": default_compound,
		"selected": selected,
		"title": title,
		"meta": meta,
		"audit": audit_label,
	}


func _apply_stable_state(rig: Dictionary, state: String) -> void:
	match state:
		"idle":
			_set_alpha(rig.pin, 1.0)
			_set_alpha(rig.default, 0.0)
			_set_alpha(rig.selected, 0.0)
			_set_alpha(rig.title, 0.0)
			_set_alpha(rig.meta, 0.0)
		"hover":
			_set_alpha(rig.pin, 0.0)
			_set_alpha(rig.default, 1.0)
			_set_alpha(rig.selected, 0.0)
			_set_alpha(rig.title, 1.0)
			_set_alpha(rig.meta, 1.0)
		"selected":
			_set_alpha(rig.pin, 0.0)
			_set_alpha(rig.default, 1.0)
			_set_alpha(rig.selected, 1.0)
			_set_alpha(rig.title, 1.0)
			_set_alpha(rig.meta, 1.0)


func _hold_frames(viewport: SubViewport, rig: Dictionary, frame_index: int, count: int, label_text: String) -> int:
	rig.audit.text = label_text
	for _index in range(count):
		await _save_dynamic_frame(viewport, rig.root, frame_index)
		frame_index += 1
	return frame_index


func _transition_idle_to_hover(viewport: SubViewport, rig: Dictionary, frame_index: int, count: int) -> int:
	rig.audit.text = "IDLE → HOVER"
	for index in range(count):
		var amount := float(index + 1) / float(count)
		_set_alpha(rig.pin, 1.0 - amount)
		_set_alpha(rig.default, amount)
		_set_alpha(rig.selected, 0.0)
		_set_alpha(rig.title, amount)
		_set_alpha(rig.meta, amount)
		await _save_dynamic_frame(viewport, rig.root, frame_index)
		frame_index += 1
	return frame_index


func _transition_hover_to_selected(viewport: SubViewport, rig: Dictionary, frame_index: int, count: int) -> int:
	rig.audit.text = "HOVER → SELECTED"
	for index in range(count):
		var amount := float(index + 1) / float(count)
		_set_alpha(rig.pin, 0.0)
		_set_alpha(rig.default, 1.0)
		_set_alpha(rig.selected, amount)
		_set_alpha(rig.title, 1.0)
		_set_alpha(rig.meta, 1.0)
		await _save_dynamic_frame(viewport, rig.root, frame_index)
		frame_index += 1
	return frame_index


func _transition_selected_to_hover(viewport: SubViewport, rig: Dictionary, frame_index: int, count: int) -> int:
	rig.audit.text = "取消选中 → HOVER"
	for index in range(count):
		var amount := float(index + 1) / float(count)
		_set_alpha(rig.selected, 1.0 - amount)
		await _save_dynamic_frame(viewport, rig.root, frame_index)
		frame_index += 1
	return frame_index


func _transition_hover_to_idle(viewport: SubViewport, rig: Dictionary, frame_index: int, count: int) -> int:
	rig.audit.text = "HOVER → IDLE"
	for index in range(count):
		var amount := float(index + 1) / float(count)
		_set_alpha(rig.pin, amount)
		_set_alpha(rig.default, 1.0 - amount)
		_set_alpha(rig.title, 1.0 - amount)
		_set_alpha(rig.meta, 1.0 - amount)
		await _save_dynamic_frame(viewport, rig.root, frame_index)
		frame_index += 1
	return frame_index


func _set_alpha(item: CanvasItem, alpha: float) -> void:
	var color := item.modulate
	color.a = clampf(alpha, 0.0, 1.0)
	item.modulate = color


func _make_texture_rect(parent: Control, path: String, position_value: Vector2, size_value: Vector2, z: int) -> TextureRect:
	var source_image := Image.load_from_file(ProjectSettings.globalize_path(path))
	if source_image == null or source_image.is_empty():
		push_error("State-chain texture failed to load: %s" % path)
	var texture := ImageTexture.create_from_image(source_image)
	var rect := TextureRect.new()
	rect.position = position_value
	rect.size = size_value
	rect.texture = texture
	rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rect.stretch_mode = TextureRect.STRETCH_SCALE
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rect.z_index = z
	parent.add_child(rect)
	return rect


func _make_label(parent: Control, text_value: String, rect: Rect2, font_size: int, color: Color, z: int) -> Label:
	var label := Label.new()
	label.position = rect.position
	label.size = rect.size
	label.text = text_value
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.z_index = z
	parent.add_child(label)
	return label


func _three_state_payload() -> Dictionary:
	return {
		"region_title": "西南荒漠",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": "state_selected",
		"nodes": [
			_task_node("state_idle", 0.18, 0.24),
			_task_node("state_hover", 0.31, 0.49),
			_task_node("state_selected", 0.48, 0.72),
		],
		"node_title": "罗斯威尔档案残页",
		"region_node_summary": "同一任务在地图上的三种交互状态：未选中只保留图钉，悬停临时展开，选中后持续显示并增加类型色后衬。",
		"region_node_meta": "地点 / 新墨西哥荒漠  ·  需求 / 洞察与调查  ·  1天",
		"region_node_deadline": "",
		"region_node_chain": "风险等级：低 · 情报来源稳定",
		"region_action_hint": "建议：优先派遣洞察较高的记者；当前选择不会消耗天数。",
		"dispatch_open_enabled": true,
		"dispatch_open_text": "送至签批台",
	}


func _dynamic_payload() -> Dictionary:
	return {
		"region_title": "西南荒漠",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": "",
		"nodes": [_task_node("state_demo", 0.31, 0.48)],
		"node_title": "选择一份事件档案",
		"dispatch_open_enabled": false,
		"dispatch_open_text": "先选择任务",
	}


func _task_node(task_id: String, x: float, y: float) -> Dictionary:
	return {
		"id": task_id,
		"name": "罗斯威尔档案残页",
		"kind": "permanent",
		"days": 1,
		"type": "sci",
		"tone": "normal",
		"state": "available",
		"enabled": true,
		"map_pos": {"x": x, "y": y},
	}


func _make_viewport() -> SubViewport:
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(1920, 1080)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
	root.add_child(viewport)
	return viewport


func _dispose_viewport(viewport: SubViewport) -> void:
	root.remove_child(viewport)
	viewport.queue_free()
	await process_frame


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _save_full_png(viewport: SubViewport, path: String) -> void:
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	var error := image.save_png(ProjectSettings.globalize_path(path))
	if error != OK:
		push_error("Failed to save static state-chain capture: %s" % error_string(error))


func _save_dynamic_frame(viewport: SubViewport, rig: Control, frame_index: int) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	var origin := Vector2i(roundi(rig.global_position.x - 38.0), roundi(rig.global_position.y - 46.0))
	var crop_rect := Rect2i(origin, Vector2i(370, 172))
	var cropped := image.get_region(crop_rect)
	var path := "%s/frame_%03d.png" % [frame_dir, frame_index]
	var error := cropped.save_png(ProjectSettings.globalize_path(path))
	if error != OK:
		push_error("Failed to save dynamic state-chain frame: %s" % error_string(error))
