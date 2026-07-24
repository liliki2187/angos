extends SceneTree

const BoardV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd")
const ManifestV2 := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd")

const OUT_DIR := "res://../docs/screenshots/2026-07-21-region-task-single-compound-probe-v4"
const PROBE_TEXTURE := "res://tests/fixtures/region_task_compound_probe_v4/rt-task-compound-permanent-selected-right-v4-3x.png"
const OUTPUT_PATH := OUT_DIR + "/02-godot-1x-map-placement-v4.png"

const INK := Color("17252a")
const META_INK := Color("405157")


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
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
	board.render(_fixture_payload())
	await _settle_frames(6)

	var original_pin := board.find_child("EventPin_roswell_archive", true, false) as Control
	if original_pin == null:
		push_error("Single compound probe could not find the selected runtime pin.")
		quit(1)
		return
	var pin_parent := original_pin.get_parent() as Control
	var pin_position := original_pin.position
	original_pin.visible = false
	_add_compound_probe(pin_parent, pin_position)
	await _settle_frames(8)

	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	if image == null or image.is_empty():
		push_error("Single compound probe capture returned an empty image.")
		quit(1)
		return
	var error := image.save_png(ProjectSettings.globalize_path(OUTPUT_PATH))
	if error != OK:
		push_error("Single compound probe capture failed to save: %s" % error_string(error))
		quit(1)
		return
	print("capture_region_task_single_compound_probe_v4.gd OK")
	quit(0)


func _fixture_payload() -> Dictionary:
	return {
		"region_title": "西南荒漠",
		"week": 2,
		"remaining_days": 5,
		"selected_node_id": "roswell_archive",
		"nodes": [
			{
				"id": "roswell_archive",
				"name": "罗斯威尔档案残页",
				"kind": "permanent",
				"days": 1,
				"type": "sci",
				"tone": "normal",
				"state": "available",
				"enabled": true,
				"map_pos": {"x": 0.31, "y": 0.43},
			},
		],
		"node_title": "罗斯威尔档案残页",
		"region_node_summary": "当地旧报社留下了一页被反复涂改的目击档案，记录的时间与空军基地日志并不一致。",
		"region_node_meta": "地点 / 新墨西哥荒漠  ·  需求 / 洞察与调查  ·  1天",
		"region_node_deadline": "",
		"region_node_chain": "风险等级：低 · 情报来源稳定",
		"region_action_hint": "建议：优先派遣洞察较高的记者；当前选择不会消耗天数。",
		"dispatch_open_enabled": true,
		"dispatch_open_text": "送至签批台",
	}


func _add_compound_probe(parent: Control, at_position: Vector2) -> void:
	var probe := Control.new()
	probe.name = "SingleCompoundArtProbeV4"
	probe.position = at_position
	probe.size = Vector2(278, 80)
	probe.mouse_filter = Control.MOUSE_FILTER_IGNORE
	probe.z_index = 20
	parent.add_child(probe)

	var source_image := Image.load_from_file(ProjectSettings.globalize_path(PROBE_TEXTURE))
	if source_image == null or source_image.is_empty():
		push_error("Single compound probe texture failed to load: %s" % PROBE_TEXTURE)
		return
	var compound_texture := ImageTexture.create_from_image(source_image)
	var compound := TextureRect.new()
	compound.name = "GeneratedCompoundArt"
	compound.size = Vector2(278, 80)
	compound.texture = compound_texture
	compound.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	compound.stretch_mode = TextureRect.STRETCH_SCALE
	compound.mouse_filter = Control.MOUSE_FILTER_IGNORE
	probe.add_child(compound)

	var icon_atlas := ManifestV2.load_asset_texture("rt2_task_pin_kind_icons_v3")
	if icon_atlas != null:
		var icon_texture := AtlasTexture.new()
		icon_texture.atlas = icon_atlas
		icon_texture.region = Rect2(0, 0, 84, 84)
		var icon := TextureRect.new()
		icon.name = "RuntimeKindIcon"
		icon.position = Vector2(22, 14)
		icon.size = Vector2(28, 28)
		icon.texture = icon_texture
		icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
		probe.add_child(icon)

	var title := Label.new()
	title.name = "RuntimeTitle"
	title.position = Vector2(92, 12)
	title.size = Vector2(166, 28)
	title.text = "罗斯威尔档案残页"
	title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	title.add_theme_font_size_override("font_size", 15)
	title.add_theme_color_override("font_color", INK)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	probe.add_child(title)

	var meta := Label.new()
	meta.name = "RuntimeMeta"
	meta.position = Vector2(92, 40)
	meta.size = Vector2(166, 22)
	meta.text = "常驻调查 · 1天"
	meta.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	meta.add_theme_font_size_override("font_size", 12)
	meta.add_theme_color_override("font_color", META_INK)
	meta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	probe.add_child(meta)


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
