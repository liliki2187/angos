extends SceneTree

const OUT_DIR := "res://../docs/screenshots/2026-06-16-world-map-v6g-single-state-mock"
const PreviewControl := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapV6gPreview.gd")

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	root.size = Vector2i(1920, 1080)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))

	await _capture_preview(false, "01-v6g-single-state-mock-clean.png")
	await _capture_preview(true, "02-v6g-single-state-mock-safe-zones.png")
	quit(0)

func _capture_preview(show_debug_zones: bool, file_name: String) -> void:
	for child in root.get_children():
		root.remove_child(child)
		child.queue_free()

	var preview := PreviewControl.new()
	preview.configure(show_debug_zones)
	root.add_child(preview)
	preview.set_anchors_preset(Control.PRESET_FULL_RECT)
	preview.offset_left = 0.0
	preview.offset_top = 0.0
	preview.offset_right = 0.0
	preview.offset_bottom = 0.0

	await _settle_frames(8)
	var image := root.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame
