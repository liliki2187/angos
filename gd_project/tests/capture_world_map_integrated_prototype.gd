extends SceneTree

const PrototypeScene := preload("res://scenes/prototypes/world_map_integrated/WorldMapIntegratedPrototype.tscn")
const OUT_DIR := "res://../docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton"
const FRAME_DIR := OUT_DIR + "/frames-v5-vertical-closure"
const RUNTIME_SIZE := Vector2i(1920, 1080)

var _viewport: SubViewport
var _prototype: Control


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(FRAME_DIR))
	_setup_viewport()
	await _settle_frames(8)

	var ok := true
	ok = await _capture("31-vertical-closure-shared-image-v5.png") and ok
	ok = await _capture_frame(0) and ok

	_prototype.set_review_overlay(true)
	ok = await _capture("32-hit-rect-review-v5.png") and ok
	_prototype.set_review_overlay(false)

	_prototype.activate_region_for_test("east_asia", "地图节点")
	ok = await _capture("33-locked-feedback-v5.png") and ok
	ok = await _capture_frame(1) and ok

	_prototype.activate_region_for_test("north_america", "地区卡")
	ok = await _capture_frame(2) and ok

	_prototype.set_mission_expanded(true)
	ok = await _capture("34-mission-expanded-v5.png") and ok
	ok = await _capture_frame(3) and ok

	_prototype.activate_primary_for_test()
	ok = await _capture_frame(4) and ok

	if not ok:
		push_error("world map integrated prototype capture failed")
		quit(1)
		return
	print("capture_world_map_integrated_prototype.gd OK")
	quit(0)


func _setup_viewport() -> void:
	_viewport = SubViewport.new()
	_viewport.disable_3d = true
	_viewport.size = RUNTIME_SIZE
	_viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	_viewport.transparent_bg = false
	root.add_child(_viewport)
	_prototype = PrototypeScene.instantiate()
	_prototype.position = Vector2.ZERO
	_prototype.size = Vector2(RUNTIME_SIZE)
	_viewport.add_child(_prototype)


func _capture(file_name: String) -> bool:
	await _settle_frames(5)
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	return _save_png("%s/%s" % [OUT_DIR, file_name])


func _capture_frame(index: int) -> bool:
	await _settle_frames(3)
	await RenderingServer.frame_post_draw
	return _save_png("%s/frame_%03d.png" % [FRAME_DIR, index])


func _save_png(resource_path: String) -> bool:
	var texture := _viewport.get_texture()
	if texture == null:
		push_error("SubViewport texture is null for %s" % resource_path)
		return false
	var image := texture.get_image()
	if image == null or image.is_empty():
		push_error("SubViewport image is empty for %s" % resource_path)
		return false
	if _sampled_color_count(image) < 24:
		push_error("Captured image has too few sampled colors: %s" % resource_path)
		return false
	var error := image.save_png(ProjectSettings.globalize_path(resource_path))
	if error != OK:
		push_error("save_png failed for %s: %s" % [resource_path, error])
		return false
	print("saved %s" % resource_path)
	return true


func _sampled_color_count(image: Image) -> int:
	var colors := {}
	for y in range(0, image.get_height(), 20):
		for x in range(0, image.get_width(), 20):
			colors[image.get_pixel(x, y).to_rgba32()] = true
	return colors.size()


func _settle_frames(count: int) -> void:
	for _index in range(count):
		await process_frame
