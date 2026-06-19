extends Control

const OUT_DIR := "res://../docs/screenshots/2026-06-08-world-map-action-log-safe-pass-godot"
const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

var scene: Control

func _ready() -> void:
	get_tree().root.size = Vector2i(1920, 1080)
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))

	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	scene = packed.instantiate() as Control
	add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	scene.offset_left = 0.0
	scene.offset_top = 0.0
	scene.offset_right = 0.0
	scene.offset_bottom = 0.0

	await _settle_frames(8)
	scene._on_advance_phase_pressed()
	await _settle_frames(8)
	_save_png("01-world-map-region-select.png")

	scene._on_enter_region_requested()
	await _settle_frames(8)
	scene._on_node_pressed("m330")
	await _settle_frames(8)
	_save_png("02-region-task-board.png")

	scene._on_open_dispatch_requested()
	await _settle_frames(8)
	_save_png("03-dispatch-no-staff.png")
	scene._toggle_staff("ivy")
	scene._toggle_staff("mora")
	await _settle_frames(8)
	_save_png("03-dispatch-desk-chain.png")

	scene._on_back_to_region_requested()
	await _settle_frames(8)
	scene._on_node_pressed("n51")
	await _settle_frames(8)
	scene._on_open_dispatch_requested()
	await _settle_frames(8)
	scene._toggle_staff("ivy")
	scene._toggle_staff("reed")
	scene.run_state.remaining_days = 1
	scene._refresh_all()
	await _settle_frames(8)
	_save_png("04-dispatch-days-insufficient.png")

	scene.run_state.remaining_days = 7
	scene.selected_staff_ids.clear()
	scene.dispatch_notice_text = ""
	scene.dispatch_signoff_state = "idle"
	scene.run_state.macro_stats.mania = 35
	scene.run_state.macro_stats.weirdness = 40
	scene._refresh_all()
	await _settle_frames(8)
	scene._on_back_to_region_requested()
	await _settle_frames(8)
	scene._on_node_pressed("hidden_gate")
	await _settle_frames(8)
	scene._on_open_dispatch_requested()
	await _settle_frames(8)
	scene._toggle_staff("qiao")
	await _settle_frames(8)
	_save_png("04b-dispatch-potential-insufficient.png")

	scene._on_back_to_region_requested()
	await _settle_frames(8)
	scene._on_node_pressed("temp_ufo")
	await _settle_frames(8)
	scene._on_open_dispatch_requested()
	await _settle_frames(8)
	scene._toggle_staff("ivy")
	scene._toggle_staff("qiao")
	scene._toggle_staff("reed")
	await _settle_frames(8)
	_save_png("04-dispatch-desk-deadline.png")
	scene._on_execute_pressed()
	await get_tree().create_timer(0.08).timeout
	await _settle_frames(2)
	_save_png("05-dispatch-cta-loading.png")
	await get_tree().create_timer(0.16).timeout
	await _settle_frames(2)
	_save_png("06-dispatch-cta-stamped.png")
	await get_tree().create_timer(0.22).timeout
	await _settle_frames(8)
	_save_png("07-region-return-after-signoff.png")
	get_tree().quit(0)

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await get_tree().process_frame

func _save_png(file_name: String) -> void:
	var image := get_viewport().get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path("%s/%s" % [OUT_DIR, file_name]))
