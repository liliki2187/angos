extends SceneTree

const BoardV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd")
const ManifestV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd")

const OUTPUT := "res://../docs/screenshots/2026-07-21-region-task-icon-seat-options-v5/02-godot-icon-seat-options-1x.png"
const OPTIONS := [
	{
		"id": "option_a",
		"label": "A / 下开口切角框（推荐）",
		"texture": "res://tests/fixtures/region_task_icon_seat_options_v5/rt-task-pin-permanent-icon-seat-a-open-bottom-v5-3x.png",
	},
	{
		"id": "option_b",
		"label": "B / 闭合八边纸槽",
		"texture": "res://tests/fixtures/region_task_icon_seat_options_v5/rt-task-pin-permanent-icon-seat-b-closed-v5-3x.png",
	},
	{
		"id": "option_c",
		"label": "C / 微差色切角纸窗",
		"texture": "res://tests/fixtures/region_task_icon_seat_options_v5/rt-task-pin-permanent-icon-seat-c-window-v5-3x.png",
	},
]

const STATE_INK := Color("f4e8c8")


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUTPUT.get_base_dir()))
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(1920, 1080)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
	root.add_child(viewport)

	var board := BoardV2.new()
	viewport.add_child(board)
	board.size = Vector2(1920, 1080)
	await _settle_frames(4)
	board.render(_payload())
	await _settle_frames(6)

	for option in OPTIONS:
		var original := board.find_child("EventPin_%s" % option.id, true, false) as Control
		if original == null:
			push_error("Missing option pin: %s" % option.id)
			continue
		var parent := original.get_parent() as Control
		var at_position := original.position
		original.visible = false
		_add_option_rig(parent, at_position, option)

	await _settle_frames(8)
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	var error := image.save_png(ProjectSettings.globalize_path(OUTPUT))
	if error != OK:
		push_error("Failed to save icon-seat options screenshot: %s" % error_string(error))
	else:
		print("capture_region_task_icon_seat_options_v5.gd OK: %s" % OUTPUT)
	quit(0)


func _add_option_rig(parent: Control, at_position: Vector2, option: Dictionary) -> void:
	var rig := Control.new()
	rig.position = at_position
	rig.size = Vector2(72, 80)
	rig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rig.z_index = 20
	parent.add_child(rig)

	var source_image := Image.load_from_file(ProjectSettings.globalize_path(str(option.texture)))
	var pin := TextureRect.new()
	pin.position = Vector2(4, 0)
	pin.size = Vector2(64, 80)
	pin.texture = ImageTexture.create_from_image(source_image)
	pin.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	pin.stretch_mode = TextureRect.STRETCH_SCALE
	pin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rig.add_child(pin)

	var icon_atlas := ManifestV2.load_asset_texture("rt2_task_pin_kind_icons_v3")
	var icon := TextureRect.new()
	icon.position = Vector2(22, 14)
	icon.size = Vector2(28, 28)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	icon.z_index = 2
	if icon_atlas != null:
		var icon_texture := AtlasTexture.new()
		icon_texture.atlas = icon_atlas
		icon_texture.region = Rect2(0, 0, 84, 84)
		icon.texture = icon_texture
	rig.add_child(icon)

	var label := Label.new()
	label.position = Vector2(-40, -34)
	label.size = Vector2(260, 26)
	label.text = str(option.label)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", STATE_INK)
	label.add_theme_constant_override("outline_size", 4)
	label.add_theme_color_override("font_outline_color", Color("071d2e"))
	label.z_index = 3
	rig.add_child(label)


func _payload() -> Dictionary:
	return {
		"region_title": "西南荒漠",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": "",
		"nodes": [
			_task_node("option_a", 0.18, 0.28),
			_task_node("option_b", 0.43, 0.50),
			_task_node("option_c", 0.67, 0.70),
		],
		"node_title": "图标座方案复核",
		"region_node_summary": "三枚图钉使用同一外轮廓、同一图标尺寸和同一锚点；这里只比较图标周围的承托方式。",
		"region_node_meta": "范围 / 常驻任务右挂 · 只读美术候选",
		"region_node_deadline": "",
		"region_node_chain": "A 下开口框 · B 闭合纸槽 · C 微差色纸窗",
		"region_action_hint": "请选择一项进入三态同步；本页未修改生产资源。",
		"dispatch_open_enabled": false,
		"dispatch_open_text": "等待方案确认",
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


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
