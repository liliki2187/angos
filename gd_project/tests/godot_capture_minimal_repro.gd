extends SceneTree

## Minimal repro: Godot 4.6 UI screenshot capture on Windows.
##
## Headless (--headless): root.get_texture() and SubViewport both return null (dummy renderer).
## Windowed (--rendering-driver opengl3): both paths work.
##
## Run:
##   tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe --headless --path gd_project -s res://tests/godot_capture_minimal_repro.gd
##   tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe --path gd_project --resolution 640x360 --windowed --audio-driver Dummy --rendering-driver opengl3 -s res://tests/godot_capture_minimal_repro.gd

const OUT_DIR := "res://../docs/screenshots/godot-capture-minimal-repro"
const OUT_ROOT := "01-root-get-texture.png"
const OUT_SUBVIEWPORT := "02-subviewport.png"

var _headless_mode := false

func _init() -> void:
	_headless_mode = DisplayServer.get_name() == "headless"
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	var root_ok := await _try_root_capture()
	var sub_ok := await _try_subviewport_capture()

	print("godot_capture_minimal_repro display_driver=%s" % DisplayServer.get_name())
	print("godot_capture_minimal_repro root.get_texture(): %s" % ("PASS" if root_ok else "FAIL"))
	print("godot_capture_minimal_repro SubViewport capture: %s" % ("PASS" if sub_ok else "FAIL"))

	if _headless_mode:
		if root_ok or sub_ok:
			push_error("Unexpected pass in headless mode.")
			quit(1)
			return
		print("godot_capture_minimal_repro VERDICT: headless cannot capture UI textures on Godot 4.6; use windowed + opengl3 for screenshot scripts.")
		quit(0)
		return

	if not sub_ok:
		push_error("SubViewport capture failed in windowed mode; screenshot pipeline is blocked.")
		quit(1)
		return

	print("godot_capture_minimal_repro VERDICT: windowed capture OK.")
	quit(0)

func _try_root_capture() -> bool:
	for child in root.get_children():
		root.remove_child(child)
		child.queue_free()
	root.size = Vector2i(640, 360)
	var panel := ColorRect.new()
	panel.color = Color("#ff3366")
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(panel)
	await _settle_frames(4)
	var texture := root.get_texture()
	if texture == null:
		return false
	var image := texture.get_image()
	if image == null:
		return false
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, OUT_ROOT]))
	return true

func _try_subviewport_capture() -> bool:
	for child in root.get_children():
		root.remove_child(child)
		child.queue_free()
	var viewport := SubViewport.new()
	viewport.disable_3d = true
	viewport.size = Vector2i(640, 360)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
	root.add_child(viewport)
	var panel := ColorRect.new()
	panel.color = Color("#33cc66")
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	viewport.add_child(panel)
	await _settle_frames(4)
	var texture := viewport.get_texture()
	if texture == null:
		return false
	var image := texture.get_image()
	if image == null:
		return false
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, OUT_SUBVIEWPORT]))
	return true

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame
