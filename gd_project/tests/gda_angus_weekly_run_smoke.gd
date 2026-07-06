extends SceneTree

const WEEKLY_RUN_SCENE := "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn"

var _failures: Array[String] = []

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	root.size = Vector2i(1920, 1080)

	var packed := load(WEEKLY_RUN_SCENE) as PackedScene
	if packed == null:
		_fail("cannot load WeeklyRunGame.tscn")
		_finish()
		return

	var scene := packed.instantiate() as Control
	if scene == null:
		_fail("cannot instantiate WeeklyRunGame as Control")
		_finish()
		return

	root.add_child(scene)
	scene.set_anchors_preset(Control.PRESET_FULL_RECT)
	scene.offset_left = 0.0
	scene.offset_top = 0.0
	scene.offset_right = 0.0
	scene.offset_bottom = 0.0

	await _settle_frames(8)

	_expect_node(scene, "RootMargin/RootVBox/HeaderPanel/HeaderHBox/TitleBox/Title")
	_expect_node(scene, "RootMargin/RootVBox/PhaseHost")
	_expect_node(scene, "RootMargin/RootVBox/PhaseHost/BriefingPhase")
	_expect_node(scene, "RootMargin/RootVBox/PhaseHost/ExplorePhase")
	_expect_initialized(scene, "briefing_phase")
	_expect_initialized(scene, "explore_phase")

	_call_or_fail(scene, "_on_advance_phase_pressed")
	await _settle_frames(8)
	_expect_node(scene, "RootMargin/RootVBox/PhaseHost/ExplorePhase/RootVBox/WorldView")

	_call_or_fail(scene, "_on_region_pressed", ["us"])
	await _settle_frames(4)
	_call_or_fail(scene, "_on_enter_region_requested")
	await _settle_frames(4)
	_call_or_fail(scene, "_on_node_pressed", ["m330"])
	await _settle_frames(4)
	_call_or_fail(scene, "_on_open_dispatch_requested")
	await _settle_frames(4)
	_call_or_fail(scene, "_toggle_staff", ["ivy"])
	await _settle_frames(4)

	_expect_node(scene, "RootMargin/RootVBox/PhaseHost/ExplorePhase/RootVBox/DispatchView")
	_finish()

func _settle_frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _expect_node(scene: Node, path: String) -> void:
	if scene.get_node_or_null(path) == null:
		_fail("missing node: %s" % path)

func _expect_initialized(scene: Object, property_name: String) -> void:
	if scene.get(property_name) == null:
		_fail("not initialized: %s" % property_name)

func _call_or_fail(scene: Object, method_name: String, args: Array = []) -> void:
	if not scene.has_method(method_name):
		_fail("missing method: %s" % method_name)
		return
	scene.callv(method_name, args)

func _fail(message: String) -> void:
	_failures.append(message)
	push_error(message)

func _finish() -> void:
	if _failures.is_empty():
		print("gda_angus_weekly_run_smoke.gd OK")
		quit(0)
		return
	print("gda_angus_weekly_run_smoke.gd FAILURES=%d" % _failures.size())
	quit(1)
