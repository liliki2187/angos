extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-22-weekly-editorial-main-head-cobalt-assetization-v1"
const ASSET_ROOT := "res://Assets/ui/angus_packaging/weekly_editorial/assetization_preflight/main_head_cobalt_v1"
const STORY_PATH := "res://Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-story-m330-last-train-v1.png"
const LOGICAL_SIZE := Vector2(442, 374)
const STATES := [
	{"id": "idle", "label": "普通态", "file": "01-main-head-idle.png"},
	{"id": "legal", "label": "合法目标", "file": "02-main-head-legal.png"},
	{"id": "hover", "label": "唯一悬停", "file": "03-main-head-hover.png"},
	{"id": "focused", "label": "聚焦＋换稿", "file": "04-main-head-focused.png"},
]

var _audit_states: Array[Dictionary] = []


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	print("main_head_capture: start")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	for state in STATES:
		print("main_head_capture: state %s" % String(state.id))
		await _capture_component(String(state.id), String(state.file))
	print("main_head_capture: review board")
	await _capture_review_board()
	print("main_head_capture: audit")
	_write_audit()
	print("capture_weekly_editorial_main_head_cobalt_assetization_v1.gd OK")
	quit(0)


func _capture_component(state_id: String, file_name: String) -> void:
	var viewport := _make_viewport(Vector2i(442, 374), true)
	print("main_head_capture: viewport %s" % state_id)
	var component := _build_component(state_id)
	print("main_head_capture: component %s" % state_id)
	viewport.add_child(component)
	print("main_head_capture: settle %s" % state_id)
	await _settle(4)
	print("main_head_capture: save %s" % state_id)
	_save_png(viewport, file_name)
	_audit_states.append(_state_audit(state_id, component))
	root.remove_child(viewport)
	viewport.queue_free()
	await process_frame


func _capture_review_board() -> void:
	var viewport := _make_viewport(Vector2i(1920, 1080), false)
	var board := Control.new()
	board.size = Vector2(1920, 1080)
	viewport.add_child(board)

	var background := ColorRect.new()
	background.color = Color("06131f")
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	board.add_child(background)

	var title := _label("主头版 exact-size 资产化预演 v1", 30, Color("eee7d8"))
	title.position = Vector2(64, 38)
	title.size = Vector2(1200, 46)
	board.add_child(title)
	var subtitle := _label("方案 1 钴蓝配色 · 442×374 正交根节点 · 动态内容未烘焙", 16, Color("9fb2be"))
	subtitle.position = Vector2(66, 88)
	subtitle.size = Vector2(1100, 28)
	board.add_child(subtitle)

	var main_panel := Panel.new()
	main_panel.position = Vector2(64, 142)
	main_panel.size = Vector2(522, 454)
	main_panel.add_theme_stylebox_override("panel", _panel_style(Color("0b2230"), Color("31506b"), 2, 10))
	board.add_child(main_panel)
	var main_component := _build_component("focused")
	main_component.position = Vector2(40, 40)
	main_panel.add_child(main_component)

	var main_tag := _label("实际运行尺寸 442×374", 15, Color("d9c87a"))
	main_tag.position = Vector2(64, 610)
	main_tag.size = Vector2(522, 26)
	board.add_child(main_tag)

	var layers_title := _label("Godot 拼装层", 22, Color("eee7d8"))
	layers_title.position = Vector2(650, 142)
	layers_title.size = Vector2(400, 32)
	board.add_child(layers_title)
	var layer_names := [
		["Z50", "无输入装饰 / 固定印务角标", Color("d3b355")],
		["Z40", "真实 44×44 Button / 命中区", Color("d6c47a")],
		["Z30", "合法、悬停、聚焦透明状态层", Color("4d87b5")],
		["Z20", "动态标题、报道图、meta", Color("eee7d8")],
		["Z10", "2× 暖纸与深蓝照片凹槽", Color("71804c")],
	]
	for index in range(layer_names.size()):
		var row := Panel.new()
		row.position = Vector2(650 + index * 20, 194 + index * 72)
		row.size = Vector2(540, 56)
		row.add_theme_stylebox_override("panel", _panel_style(Color("102835"), layer_names[index][2], 2, 7))
		board.add_child(row)
		var text := _label("%s　%s" % [layer_names[index][0], layer_names[index][1]], 16, Color("e7e1d5"))
		text.position = Vector2(14, 10)
		text.size = Vector2(510, 34)
		row.add_child(text)

	var rule := _label("斜边只存在于透明图层；Root、图片、文字与按钮始终保持 0°。", 17, Color("a9bac2"))
	rule.position = Vector2(650, 586)
	rule.size = Vector2(620, 32)
	board.add_child(rule)

	var states_title := _label("同一合同坐标下的四个关键状态", 22, Color("eee7d8"))
	states_title.position = Vector2(64, 682)
	states_title.size = Vector2(700, 34)
	board.add_child(states_title)
	for index in range(STATES.size()):
		var state: Dictionary = STATES[index]
		var card := Panel.new()
		card.position = Vector2(64 + index * 455, 732)
		card.size = Vector2(418, 300)
		card.add_theme_stylebox_override("panel", _panel_style(Color("0a1d29"), Color("294457"), 1, 8))
		board.add_child(card)
		var preview := _build_component(String(state.id))
		preview.scale = Vector2(0.62, 0.62)
		preview.position = Vector2(72, 16)
		card.add_child(preview)
		var state_label := _label(String(state.label), 16, Color("e9e2d5"))
		state_label.position = Vector2(18, 258)
		state_label.size = Vector2(380, 24)
		state_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		card.add_child(state_label)

	await _settle(5)
	await RenderingServer.frame_post_draw
	_save_png(viewport, "05-main-head-assetization-review-board.png")
	root.remove_child(viewport)
	viewport.queue_free()
	await process_frame


func _build_component(state_id: String) -> Control:
	var root_control := Control.new()
	root_control.name = "MainHeadRoot_%s" % state_id
	root_control.size = LOGICAL_SIZE
	root_control.mouse_filter = Control.MOUSE_FILTER_STOP
	root_control.set_meta("hit_rect", Rect2(Vector2.ZERO, LOGICAL_SIZE))

	var page_paper_carrier := ColorRect.new()
	page_paper_carrier.name = "PreviewPagePaperCarrier"
	page_paper_carrier.size = LOGICAL_SIZE
	page_paper_carrier.color = Color("b9ad8f")
	page_paper_carrier.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root_control.add_child(page_paper_carrier)

	root_control.add_child(_texture_layer("BasePaper", "%s/base-paper.png" % ASSET_ROOT, Vector2.ZERO, LOGICAL_SIZE))

	var story := TextureRect.new()
	story.name = "DynamicStoryImage"
	story.position = Vector2(16, 92)
	story.size = Vector2(410, 218)
	story.texture = load(STORY_PATH)
	story.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	story.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	story.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root_control.add_child(story)

	root_control.add_child(_texture_layer("FixedDecoration", "%s/fixed-decoration.png" % ASSET_ROOT, Vector2.ZERO, LOGICAL_SIZE))
	if state_id == "legal":
		root_control.add_child(_texture_layer("LegalOverlay", "%s/state-legal.png" % ASSET_ROOT, Vector2.ZERO, LOGICAL_SIZE))
	elif state_id == "hover":
		root_control.add_child(_texture_layer("HoverOverlay", "%s/state-hover.png" % ASSET_ROOT, Vector2.ZERO, LOGICAL_SIZE))
	elif state_id == "focused":
		root_control.add_child(_texture_layer("FocusedOverlay", "%s/state-focused.png" % ASSET_ROOT, Vector2.ZERO, LOGICAL_SIZE))

	var headline_slot := Control.new()
	headline_slot.name = "DynamicHeadlineSlot"
	headline_slot.position = Vector2(16, 14)
	headline_slot.size = Vector2(410, 68)
	headline_slot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root_control.add_child(headline_slot)

	var eyebrow := _label("头版主稿 · A01", 11, Color("596259"))
	eyebrow.name = "DynamicEyebrow"
	eyebrow.position = Vector2(0, 0)
	eyebrow.size = Vector2(190, 23)
	headline_slot.add_child(eyebrow)

	var headline := _label("M330末班车在不存在的站台停了三秒", 24, Color("26363d"))
	headline.name = "DynamicHeadline"
	headline.position = Vector2(0, 23)
	headline.size = Vector2(410, 45)
	headline.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	headline.clip_text = true
	headline.add_theme_font_size_override("font_size", 24)
	headline_slot.add_child(headline)

	var meta := _label("深度 · 金级 · 620", 12, Color("647064"))
	meta.name = "DynamicMeta"
	meta.position = Vector2(16, 318)
	meta.size = Vector2(360, 42)
	meta.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	root_control.add_child(meta)

	if state_id == "focused":
		var button := Button.new()
		button.name = "LocalReplaceAction"
		button.position = Vector2(390, 322)
		button.size = Vector2(44, 44)
		button.text = "换稿"
		button.add_theme_font_size_override("font_size", 12)
		button.add_theme_color_override("font_color", Color("f5eddd"))
		button.add_theme_stylebox_override("normal", _texture_style("%s/replace-action-skin.png" % ASSET_ROOT))
		button.add_theme_stylebox_override("hover", _texture_style("%s/replace-action-skin.png" % ASSET_ROOT))
		button.add_theme_stylebox_override("pressed", _texture_style("%s/replace-action-skin.png" % ASSET_ROOT))
		root_control.add_child(button)
	return root_control


func _texture_layer(node_name: String, path: String, position: Vector2, size: Vector2) -> TextureRect:
	var texture_rect := TextureRect.new()
	texture_rect.name = node_name
	texture_rect.position = position
	texture_rect.size = size
	texture_rect.texture = load(path)
	texture_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	texture_rect.stretch_mode = TextureRect.STRETCH_SCALE
	texture_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return texture_rect


func _texture_style(path: String) -> StyleBoxTexture:
	var style := StyleBoxTexture.new()
	style.texture = load(path)
	return style


func _label(text_value: String, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return label


func _panel_style(background: Color, border: Color, border_width: int, radius: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = background
	style.border_color = border
	style.set_border_width_all(border_width)
	style.set_corner_radius_all(radius)
	return style


func _make_viewport(size: Vector2i, transparent: bool) -> SubViewport:
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = size
	viewport.transparent_bg = transparent
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	return viewport


func _settle(count: int) -> void:
	for _index in range(count):
		await process_frame


func _save_png(viewport: SubViewport, file_name: String) -> void:
	var image := viewport.get_texture().get_image()
	if image == null:
		push_error("Unable to capture %s" % file_name)
		return
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))


func _state_audit(state_id: String, component: Control) -> Dictionary:
	var result := {
		"state": state_id,
		"root_position": [component.position.x, component.position.y],
		"root_size": [component.size.x, component.size.y],
		"root_rotation": component.rotation,
		"story_rect": [],
		"headline_slot_rect": [],
		"eyebrow_rect": [],
		"headline_rect": [],
		"meta_rect": [],
		"replace_rect": null,
		"visual_input_nodes": [],
	}
	for child in component.get_children():
		if child is TextureRect and child.mouse_filter != Control.MOUSE_FILTER_IGNORE:
			result.visual_input_nodes.append(child.name)
		if child.name == "DynamicStoryImage":
			result.story_rect = _rect_array(child)
		elif child.name == "DynamicHeadlineSlot":
			result.headline_slot_rect = _rect_array(child)
			var eyebrow := child.get_node("DynamicEyebrow") as Control
			var headline := child.get_node("DynamicHeadline") as Control
			result.eyebrow_rect = [child.position.x + eyebrow.position.x, child.position.y + eyebrow.position.y, eyebrow.size.x, eyebrow.size.y]
			result.headline_rect = [child.position.x + headline.position.x, child.position.y + headline.position.y, headline.size.x, headline.size.y]
		elif child.name == "DynamicMeta":
			result.meta_rect = _rect_array(child)
		elif child.name == "LocalReplaceAction":
			result.replace_rect = _rect_array(child)
	return result


func _rect_array(control: Control) -> Array:
	return [control.position.x, control.position.y, control.size.x, control.size.y]


func _write_audit() -> void:
	var expected := {
		"root": [0, 0, 442, 374],
		"headline_slot": [16, 14, 410, 68],
		"eyebrow": [16, 14, 190, 23],
		"headline": [16, 37, 410, 45],
		"story": [16, 92, 410, 218],
		"meta": [16, 318, 360, 42],
		"replace": [390, 322, 44, 44],
	}
	var state_geometry_identity := true
	var root_rotation_zero := true
	var visual_layers_ignore_input := true
	var action_visibility_and_geometry := true
	for state in _audit_states:
		state_geometry_identity = state_geometry_identity and state.root_size == [442.0, 374.0]
		state_geometry_identity = state_geometry_identity and state.story_rect == [16.0, 92.0, 410.0, 218.0]
		state_geometry_identity = state_geometry_identity and state.headline_slot_rect == [16.0, 14.0, 410.0, 68.0]
		state_geometry_identity = state_geometry_identity and state.eyebrow_rect == [16.0, 14.0, 190.0, 23.0]
		state_geometry_identity = state_geometry_identity and state.headline_rect == [16.0, 37.0, 410.0, 45.0]
		state_geometry_identity = state_geometry_identity and state.meta_rect == [16.0, 318.0, 360.0, 42.0]
		root_rotation_zero = root_rotation_zero and is_zero_approx(float(state.root_rotation))
		visual_layers_ignore_input = visual_layers_ignore_input and state.visual_input_nodes.is_empty()
		if state.state == "focused":
			action_visibility_and_geometry = action_visibility_and_geometry and state.replace_rect == [390.0, 322.0, 44.0, 44.0]
		else:
			action_visibility_and_geometry = action_visibility_and_geometry and state.replace_rect == null
	var passed := state_geometry_identity and root_rotation_zero and visual_layers_ignore_input and action_visibility_and_geometry
	var audit := {
		"artifact": "weekly_editorial_main_head_cobalt_assetization_preflight_v1",
		"viewport": [1920, 1080],
		"expected": expected,
		"states": _audit_states,
		"checks": {
			"state_geometry_identity": state_geometry_identity,
			"root_rotation_zero": root_rotation_zero,
			"visual_layers_ignore_input": visual_layers_ignore_input,
			"action_visibility_and_geometry": action_visibility_and_geometry,
			"dynamic_content_not_baked": true,
			"production_scene_modified": false,
		},
		"passed": passed,
	}
	var file := FileAccess.open("%s/audit.json" % OUT_DIR, FileAccess.WRITE)
	file.store_string(JSON.stringify(audit, "  ") + "\n")
	file.close()
