extends SceneTree
## 同一真实场景切换长边曲线，三种桌面尺寸分别采集，避免截图缩放冒充运行验证。
const GameScene = preload("res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn")
var out := "res://../docs/screenshots/2026-09-08-world-map-contour-v1"
var checks: Array = []

func _init() -> void:
	call_deferred("_run")

func _settle(count: int = 8) -> void:
	for i in range(count):
		await process_frame

func _check(ok: bool, description: String) -> void:
	checks.append({"通过": ok, "检查": description})
	print("CHECK ", ok, " ", description)

func _capture(name: String) -> void:
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(ProjectSettings.globalize_path(out + "/" + name))

func _run() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture-out="):
			out = argument.trim_prefix("--capture-out=")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(out))
	root.size = Vector2i(1920, 1080)
	var game := GameScene.instantiate()
	root.add_child(game)
	await _settle()
	game.call("_on_advance_phase_pressed")
	await _settle(30)
	var page: Control = game.explore_phase.call("get_world_map_assembly")
	var dossier: NinePatchRect = page._canvas.get_node("DossierPaper")
	var material := dossier.material as ShaderMaterial
	_check(page.visible and bool(material.get_shader_parameter("contour_enabled")), "正式地图已启用独立底纸曲线材质")
	_check(dossier.texture == page.Catalog.texture(page.Catalog.ASSET_DIR + "dossier-paper.png"), "底纸仍使用原Texture2D")
	var original_state: Dictionary = page.call("get_state_snapshot")
	for viewport_size in [Vector2i(1920, 1080), Vector2i(1600, 900), Vector2i(1280, 720)]:
		root.size = viewport_size
		await _settle(12)
		var label := "%dx%d" % [viewport_size.x, viewport_size.y]
		material.set_shader_parameter("contour_enabled", false)
		await _settle()
		_capture(label + "-before.png")
		material.set_shader_parameter("contour_enabled", true)
		await _settle()
		_capture(label + "-after.png")
		# ViewportTexture.get_size()可报告拉伸前逻辑尺寸；实际像素以GPU读回图为准。
		_check(root.get_texture().get_image().get_size() == viewport_size, label + "实际渲染尺寸一致")
		_check(root.get_visible_rect().encloses(page._primary.get_global_rect()), label + "进入按钮和底部说明完整可见")
		_check(page.call("get_state_snapshot").shared_texture_identity and page.call("get_state_snapshot").task_total == original_state.task_total, label + "三图共用及真实任务数保持")
	var ok := true
	for check in checks:
		ok = ok and check["通过"]
	var report := FileAccess.open(out + "/checks.json", FileAccess.WRITE)
	report.store_string(JSON.stringify({"全部通过": ok, "运行环境": DisplayServer.get_name(), "检查": checks}, "\t"))
	report.close()
	print("CONTOUR_RESULT ", ok, " checks=", checks.size())
	game.queue_free()
	await _settle(3)
	quit(0 if ok else 1)
