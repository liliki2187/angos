extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-07-21-region-task-pin-runtime-preflight"
const PIN_SHELL_PATH := "res://Assets/ui/angus_packaging/region_task/v2/pin_slice/rt-task-pin-shell-c-hybrid-v3-3x.png"
const LABEL_BASE_PATH := "res://Assets/ui/angus_packaging/region_task/v2/pin_slice/rt-task-pin-label-c-hybrid-v3-2x.png"
const ICON_ATLAS_PATH := "res://Assets/ui/angus_packaging/region_task/v2/pin_slice/rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png"

const PAPER := Color("e8dfc8")
const INK := Color("17252a")
const MUTED_INK := Color("52636a")
const BOARD := Color("071d2e")

var _pin_shell: Texture2D
var _label_base: Texture2D
var _icon_atlas: Texture2D
var _backplate_atlas: Texture2D
var _pin_accent_atlas: Texture2D
var _label_accent_atlas: Texture2D

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	_pin_shell = load(PIN_SHELL_PATH)
	_label_base = load(LABEL_BASE_PATH)
	_icon_atlas = load(ICON_ATLAS_PATH)
	_backplate_atlas = _load_external_texture("design/art-direction/region-task-board/runtime-preflight-v1/rt-task-pin-selected-backplates-v1-atlas-3x.png")
	_pin_accent_atlas = _load_external_texture("design/art-direction/region-task-board/runtime-preflight-v1/rt-task-pin-type-accents-v1-atlas-3x.png")
	_label_accent_atlas = _load_external_texture("design/art-direction/region-task-board/runtime-preflight-v1/rt-task-label-type-accents-v1-atlas-2x.png")
	if [_pin_shell, _label_base, _icon_atlas, _backplate_atlas, _pin_accent_atlas, _label_accent_atlas].any(func(texture: Texture2D) -> bool: return texture == null):
		push_error("区域任务背板预检资源加载失败。")
		quit(1)
		return
	await _capture_contract_board()
	await _capture_native_readback()
	print("capture_region_task_selected_backplate_preflight.gd OK")
	quit(0)

func _capture_contract_board() -> void:
	var viewport := _make_viewport(Vector2i(2560, 1440))
	var stage := Control.new()
	stage.size = Vector2(2560, 1440)
	viewport.add_child(stage)
	_add_background(stage)
	_add_label(stage, "区域任务短签｜精确运行比例与真实中文回填", Rect2(80, 34, 2400, 58), 34, PAPER, HORIZONTAL_ALIGNMENT_CENTER)
	_add_label(stage, "所有组件先按 1× 合同组合，再以整数 2× 展示；左：默认　中：选中　右：边缘左置", Rect2(80, 92, 2400, 34), 18, Color("aebc9a"), HORIZONTAL_ALIGNMENT_CENTER)
	_add_label(stage, "默认", Rect2(400, 150, 556, 40), 24, PAPER, HORIZONTAL_ALIGNMENT_CENTER)
	_add_label(stage, "选中", Rect2(1120, 150, 556, 40), 24, PAPER, HORIZONTAL_ALIGNMENT_CENTER)
	_add_label(stage, "右边缘左置验证", Rect2(1884, 150, 564, 40), 24, PAPER, HORIZONTAL_ALIGNMENT_CENTER)

	var specs := [
		{"kind": "permanent", "row": "常驻任务", "title": "罗斯威尔档案残页", "meta": "常驻调查 · 1天"},
		{"kind": "temp", "row": "限时任务", "title": "突发：雷达异常光点", "meta": "限时截稿 · 2天"},
		{"kind": "chain", "row": "连续任务", "title": "M330 末班车空白段", "meta": "连续追踪 · 2天"},
		{"kind": "hidden", "row": "隐藏任务", "title": "灵视：黑色方尖碑的回声", "meta": "灵视异常 · 3天"},
	]
	var row_y := [220.0, 450.0, 680.0, 910.0]
	for index in range(specs.size()):
		var spec: Dictionary = specs[index]
		var y: float = row_y[index]
		_add_label(stage, str(spec.row), Rect2(90, y + 48, 250, 52), 25, PAPER, HORIZONTAL_ALIGNMENT_CENTER)
		_add_sample(stage, Vector2(400, y), 2.0, str(spec.kind), str(spec.title), str(spec.meta), false, false)
		_add_sample(stage, Vector2(1120, y), 2.0, str(spec.kind), str(spec.title), str(spec.meta), true, false)
		if index == 3:
			_add_sample(stage, Vector2(2300, y), 2.0, str(spec.kind), str(spec.title), str(spec.meta), true, true)

	var boundary := ColorRect.new()
	boundary.position = Vector2(2480, 196)
	boundary.size = Vector2(2, 920)
	boundary.color = Color("886a40")
	stage.add_child(boundary)
	_add_label(stage, "地图安全边界", Rect2(2380, 1118, 180, 30), 15, Color("cbbf9f"), HORIZONTAL_ALIGNMENT_CENTER)

	_add_label(stage, "1× 原生读回（不放大）", Rect2(90, 1190, 340, 34), 20, PAPER)
	_add_sample(stage, Vector2(470, 1170), 1.0, "hidden", "灵视：黑色方尖碑的回声", "灵视异常 · 3天", true, false)
	_add_label(stage, "合同：pin 64×80｜hit 72×80｜anchor [36,76]｜label 200×72｜content [14,8,166,56]", Rect2(850, 1188, 1500, 34), 17, Color("aebc9a"))
	_add_label(stage, "本图只验证缩小可读性、独立图层与左右挂签；不是生产 atlas，也不是 Godot 正式替换。", Rect2(850, 1234, 1500, 34), 17, Color("cbbf9f"))

	await _settle_frames(8)
	await _save_png(viewport, "%s/01-contract-scale-content-fill.png" % OUT_DIR)
	await _dispose_viewport(viewport)

func _capture_native_readback() -> void:
	var viewport := _make_viewport(Vector2i(1280, 720))
	var stage := Control.new()
	stage.size = Vector2(1280, 720)
	viewport.add_child(stage)
	_add_background(stage)
	_add_label(stage, "1× 原生尺寸读回｜四类选中背板", Rect2(48, 28, 1184, 46), 28, PAPER, HORIZONTAL_ALIGNMENT_CENTER)
	var specs := [
		{"kind": "permanent", "title": "罗斯威尔档案残页", "meta": "常驻调查 · 1天"},
		{"kind": "temp", "title": "突发：雷达异常光点", "meta": "限时截稿 · 2天"},
		{"kind": "chain", "title": "M330 末班车空白段", "meta": "连续追踪 · 2天"},
		{"kind": "hidden", "title": "灵视：黑色方尖碑的回声", "meta": "灵视异常 · 3天"},
	]
	var origins := [Vector2(120, 126), Vector2(700, 126), Vector2(120, 382), Vector2(700, 382)]
	for index in range(specs.size()):
		var spec: Dictionary = specs[index]
		_add_sample(stage, origins[index], 1.0, str(spec.kind), str(spec.title), str(spec.meta), true, false)
	await _settle_frames(8)
	await _save_png(viewport, "%s/02-native-1x-selected-readback.png" % OUT_DIR)
	await _dispose_viewport(viewport)

func _add_sample(parent: Control, origin: Vector2, scale_factor: float, kind: String, title: String, meta: String, selected: bool, label_left: bool) -> void:
	var host := Control.new()
	host.position = origin
	host.size = Vector2(72, 80)
	host.scale = Vector2(scale_factor, scale_factor)
	host.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(host)
	var type_index := _type_index(kind)
	if selected:
		_add_texture(host, _atlas_frame(_backplate_atlas, type_index, Vector2i(216, 240)), Vector2.ZERO, Vector2(72, 80), 10)
	var label_origin := Vector2(-208, 4) if label_left else Vector2(78, 4)
	var label_host := Control.new()
	label_host.position = label_origin
	label_host.size = Vector2(200, 72)
	label_host.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label_host.z_index = 20
	host.add_child(label_host)
	var label_texture := _add_texture(label_host, _label_base, Vector2.ZERO, Vector2(200, 72), 0)
	var label_accent := _add_texture(label_host, _atlas_frame(_label_accent_atlas, type_index, Vector2i(400, 144)), Vector2.ZERO, Vector2(200, 72), 1)
	if label_left:
		_flip_control_h(label_texture, 200.0)
		_flip_control_h(label_accent, 200.0)
	var title_label := _add_label(label_host, title, Rect2(14, 8, 166, 28), 15, INK)
	title_label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	var meta_label := _add_label(label_host, meta, Rect2(14, 36, 166, 22), 12, MUTED_INK)
	meta_label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	_add_texture(host, _pin_shell, Vector2(4, 0), Vector2(64, 80), 21)
	_add_texture(host, _atlas_frame(_pin_accent_atlas, type_index, Vector2i(192, 240)), Vector2(4, 0), Vector2(64, 80), 30)
	_add_texture(host, _atlas_frame(_icon_atlas, _icon_index(kind), Vector2i(84, 84)), Vector2(22, 14), Vector2(28, 28), 40)

func _add_background(parent: Control) -> void:
	var background := ColorRect.new()
	background.size = parent.size
	background.color = BOARD
	parent.add_child(background)

func _add_texture(parent: Control, texture: Texture2D, position: Vector2, size: Vector2, layer: int) -> TextureRect:
	var rect := TextureRect.new()
	rect.position = position
	rect.size = size
	rect.texture = texture
	rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rect.z_index = layer
	parent.add_child(rect)
	return rect

func _flip_control_h(control: Control, width: float) -> void:
	control.position.x = width
	control.scale = Vector2(-1, 1)

func _add_label(parent: Control, text_value: String, rect: Rect2, font_size: int, color: Color, alignment: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT) -> Label:
	var label := Label.new()
	label.position = rect.position
	label.size = rect.size
	label.text = text_value
	label.horizontal_alignment = alignment
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	parent.add_child(label)
	return label

func _atlas_frame(texture: Texture2D, index: int, frame_size: Vector2i) -> AtlasTexture:
	var atlas := AtlasTexture.new()
	atlas.atlas = texture
	atlas.region = Rect2(index * frame_size.x, 0, frame_size.x, frame_size.y)
	return atlas

func _type_index(kind: String) -> int:
	match kind:
		"temp": return 1
		"chain": return 2
		"hidden": return 3
		_: return 0

func _icon_index(kind: String) -> int:
	match kind:
		"chain": return 1
		"hidden": return 2
		"temp": return 3
		_: return 0

func _load_external_texture(relative_path: String) -> Texture2D:
	var root_path := ProjectSettings.globalize_path("res://..").path_join(relative_path)
	var image := Image.load_from_file(root_path)
	if image.is_empty():
		push_error("无法加载预检纹理：%s" % root_path)
		return null
	return ImageTexture.create_from_image(image)

func _make_viewport(viewport_size: Vector2i) -> SubViewport:
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = viewport_size
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

func _save_png(viewport: SubViewport, path: String) -> void:
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path(path))
