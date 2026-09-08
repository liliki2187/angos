extends SceneTree
## 运行正式周循环并通过真实输入事件检查新地图，额外地区只存在于容量测试中。
const OUT := "res://../docs/screenshots/2026-09-07-world-map-soft-columns"
const GameScene = preload("res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn")
var game: Control
var page: Control
var results: Array = []
var frames := 0
var capture_enabled := true
var output_dir := OUT
var selection_review := false
var motion_frames := 0
var motion_clips := 0
var stills_only := false
var scroll_review := false
var scroll_frames := 0
var task_review := false
var polish_review := false

func _init() -> void:
	call_deferred("_run")

func _check(value: bool, message: String) -> void:
	print("CHECK ", value, " ", message)
	results.append({"通过": value, "检查": message})
	if not value:
		push_error(message)

func _settle(count: int = 5) -> void:
	for i in range(count):
		await process_frame

func _run() -> void:
	capture_enabled = DisplayServer.get_name() != "headless"
	# 自动输入逐条分发，避免真实图形窗口将采集期间的输入合并到另一帧。
	Input.use_accumulated_input = false
	selection_review = OS.get_cmdline_user_args().has("--selection-review")
	stills_only = OS.get_cmdline_user_args().has("--stills-only")
	scroll_review = OS.get_cmdline_user_args().has("--scroll-review")
	task_review = OS.get_cmdline_user_args().has("--task-review")
	polish_review = OS.get_cmdline_user_args().has("--polish-review")
	if selection_review:
		output_dir = "res://../docs/screenshots/2026-09-07-world-map-selection"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture-out="):
			output_dir = argument.trim_prefix("--capture-out=")
	root.size = Vector2i(1920, 1080)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir + "/frames"))
	if selection_review:
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir + "/motion"))
	if scroll_review:
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir + "/scroll"))
	game = GameScene.instantiate()
	root.add_child(game)
	await _settle(8)
	game.call("_on_advance_phase_pressed")
	await _settle(8)
	page = game.explore_phase.call("get_world_map_assembly")
	_check(page.visible, "正式周循环已挂载并显示新地图")
	_check(not game.header_panel.visible, "旧世界地图标题栏未叠加")
	var baseline_days: int = game.run_state.remaining_days
	var initial: Dictionary = page.call("get_state_snapshot")
	_check(initial.region_count == 3 and initial.shared_texture_identity, "初始三地区及三处共用 Texture2D")
	_check(initial.task_total == 4, "北美预览使用当前真实 4 个可见任务")
	if task_review:
		_check(page._task_counts.text == "限时 1   ·   线索 2   ·   深链 1", "初始真实任务分类为限时1、线索2、深链1，与4项总数一致")
		_check(page._task_warning.text.contains("截止条件") and page._risk.get_theme_color("font_color") == page.RUST, "限时提醒说明截止条件并使用风险色")
		_check(page._remaining_days.text == "本周剩余 %d 天" % baseline_days, "左侧日程明确显示真实周剩余天数")
		_check(is_equal_approx(page._photo.size.x / page._photo.size.y, page.PHOTO_RATIO) and initial.shared_texture_identity, "右图缩小后仍完整等比且三处共用同一Texture2D")
		var node_before: String = game.selected_node_id
		await _click(page._task_labels[0])
		_check(game.explore_view_mode == "world" and game.selected_node_id == node_before and game.run_state.remaining_days == baseline_days, "点击任务预览文字不会选任务、进入派遣或扣天数")
	if scroll_review:
		_check(not page._scroll.get_v_scroll_bar().visible and not page._list_hint.visible, "三地区完整放下时不显示滚动条和更多提示")
	if selection_review:
		await _neutral_pointer()
		_check(_highlight_count() == 1 and page._cards["us"].title_paper.visible, "移开鼠标且释放焦点后，仍恰有一个地区保留蜜黄选中层")
		_check(page._pins["us"].gold.visible and page._kicker.text == "当前查看 · 01 北美", "地图与右侧栏目头指向同一选中地区")
	if polish_review:
		_check(page._task_labels[0].get_line_count() == 1 and page._task_meta[0].position.y - page._task_labels[0].size.y <= 6, "常态短任务名与耗时紧密成组，不预留空白标题行")
		_check(page._task_rows[1].position.y - page._task_meta[0].get_global_rect().end.y >= 10, "任务组间留白大于组内距离")
		_check(page._task_header.size.x < page._task_paper.size.x * 0.5, "任务标题使用局部页签而非通栏深色横杠")
		_check(is_equal_approx(page._photo.position.x, page._headline.position.x) and is_equal_approx(page._headline.position.x, page._deck.position.x) and is_equal_approx(page._deck.position.x, page._task_rows[0].position.x), "图片、新闻与任务文字使用共同阅读边线")
		page._paper_material.set_shader_parameter("smooth_edges", false)
		page._front_material.set_shader_parameter("smooth_edges", false)
		page._photo_edge_material.set_shader_parameter("smooth_quad", false)
		var dossier_material := page._canvas.get_node("DossierPaper").material as ShaderMaterial
		dossier_material.set_shader_parameter("smooth_edges", false)
		dossier_material.set_shader_parameter("contour_enabled", false)
		await _settle(3)
		await _capture("14-edge-sampling-before.png")
		page._paper_material.set_shader_parameter("smooth_edges", true)
		page._front_material.set_shader_parameter("smooth_edges", true)
		page._photo_edge_material.set_shader_parameter("smooth_quad", true)
		dossier_material.set_shader_parameter("smooth_edges", true)
		dossier_material.set_shader_parameter("contour_enabled", true)
		await _settle(3)
	await _capture("01-live-default.png")
	await _film(5)
	await _click(page._cards["east_asia"].hit)
	var east: Dictionary = page.call("get_state_snapshot")
	_check(east.selected_region_id == "east_asia" and east.primary_disabled and east.shared_texture_identity, "锁定左卡可选，三图同步且 CTA 禁用")
	_check(east.photo_path.ends_with("east_asia.png"), "东亚没有误用北美图片")
	if task_review:
		_check(page._task_counts.text == "解锁后显示任务分布" and not page._task_rows[0].is_visible_in_tree() and page._empty_tasks.text.contains("声望"), "锁定地区不泄露任务分类和任务行，真实声望缺口保留")
		if polish_review:
			_check(not page._summary.visible and page._summary.tooltip_text.is_empty(), "锁定状态隐藏无效折叠热区并清空提示")
	if selection_review:
		await _neutral_pointer()
		_check(_highlight_count() == 1 and page._cards["east_asia"].backing.visible and page._pins["east_asia"].gold.visible, "锁定地区保留完整选中强度，原选区高亮已清除")
		_check(page._cards["east_asia"].face.position == page.SELECTED_PAPER_OFFSET, "纸张落定后停在预期位置")
		_check(page._cards["east_asia"].photo.size == page._cards["us"].photo.size, "选中不改变图片规格")
	await _capture("02-live-locked.png")
	if selection_review:
		var hover := InputEventMouseMotion.new()
		hover.position = page._cards["us"].hit.get_global_rect().get_center()
		Input.parse_input_event(hover)
		page._cards["us"].hit.grab_focus()
		await _settle(3)
		_check(game.selected_region_id == "east_asia" and _highlight_count() == 1 and not page._cards["us"].title_paper.visible, "悬停与键盘焦点不冒充选中，也不转移当前地区")
		await _capture("07-hover-focus-not-selection.png")
	await _film(5)
	page._cards["us"].hit.grab_focus()
	await _keyboard_enter()
	_check(game.selected_region_id == "us", "键盘 Enter 可选择地区")
	page._cards["east_asia"].hit.grab_focus()
	await _keyboard_enter()
	await _click(page._pins["us"].hit)
	_check(game.selected_region_id == "us", "地图标签真实鼠标输入回传正式地区 ID")
	var primary_before: Array = page.call("get_state_snapshot").primary_rect
	var expanded_paper_height: float = page._task_paper.size.y
	var expanded_photo_rect: Rect2 = page._photo.get_global_rect()
	await _click(page._summary)
	_check(not page.call("get_state_snapshot").expanded, "任务折叠按钮真实可操作")
	_check(page.call("get_state_snapshot").primary_rect == primary_before, "任务折叠不移动 CTA")
	if polish_review:
		_check(page._task_paper.size.y < expanded_paper_height - 80, "折叠时任务附页随内容收短，不保留整块空底")
		_check(page._photo.get_global_rect() == expanded_photo_rect, "折叠收纸不移动或缩放上方图片")
	if task_review:
		_check(page._task_counts.is_visible_in_tree() and page._task_warning.is_visible_in_tree() and not page._task_rows[0].is_visible_in_tree(), "折叠只收起任务行，分类与提醒继续可见")
		await _capture("10-task-collapsed.png")
	await _film(3)
	await _click(page._summary)
	if task_review:
		await _capture("11-task-reopened.png")
	await _click(page._primary)
	_check(game.explore_view_mode == "region", "主 CTA 进入正式地区任务台")
	_check(game.run_state.remaining_days == baseline_days, "浏览和进入不扣天数")
	game.call("_on_back_to_world_requested")
	await _settle()
	_check(game.explore_view_mode == "world" and game.selected_region_id == "us", "从地区任务台返回同一世界地图选区")
	await _film(4)
	# 已开放但零任务，与锁定状态分开。
	game.run_state.flags["m330_chain_step_2"] = true
	game.call("_on_region_pressed", "pacific")
	await _settle()
	var empty: Dictionary = page.call("get_state_snapshot")
	_check(not empty.primary_disabled and empty.task_total == 0 and empty.empty_text.contains("暂无"), "已开放空地区显示暂无任务，允许进入")
	if task_review:
		_check(page._task_counts.text == "限时 0   ·   线索 0   ·   深链 0" and not page._task_rows[0].is_visible_in_tree(), "已开放空区显示真实零分类，不保留上一地区的任务行")
		if polish_review:
			_check(not page._summary.visible and page._summary.tooltip_text.is_empty(), "开放空态不残留折叠手形或无效提示")
	await _capture("03-live-open-empty.png")
	game.run_state.flags.erase("m330_chain_step_2")
	game.run_state.remaining_days = 3
	game.call("_on_region_pressed", "us")
	await _settle()
	_check(page.call("get_state_snapshot").task_total == 3, "到期任务消失后预览总数实时刷新")
	if task_review:
		_check(page._task_counts.text == "限时 0   ·   线索 2   ·   深链 1" and page._task_warning.text.contains("推进后续地区"), "限时任务到期后分类、追踪说明同步更新，无残留截止警告")
		_check(page._risk.get_theme_color("font_color") != page.RUST and page._cards["us"].risk.text == "青线追踪", "青线状态和左卡同步显示推进机会，颜色不沿用危险红")
		_check(page._remaining_days.text == "本周剩余 3 天", "剩余天数刷新独立于任务耗时和限时截止信息")
		await _capture("12-live-chain-after-expiry.png")
	game.run_state.remaining_days = baseline_days
	game.call("_refresh_all")
	await _settle()
	if task_review:
		await _review_long_task_content()
	# 容量数据只向表现层注入，不新增任何正式地区或任务。
	var payload: Dictionary = game.call("_build_explore_payload")
	var regions: Array = payload.regions.duplicate(true)
	for i in range(3, 10):
		regions.append({"id": "capacity_%d" % i, "name": "第%02d号远洋地区新闻联络处" % (i + 1), "hint": "容量检查数据，不是正式新增地区", "unlocked": false, "enabled": false, "tone": "locked"})
	payload.regions = regions
	if scroll_review:
		payload.regions = regions.slice(0, 4)
		page.call("render", payload)
		await _settle(8)
		_scroll_debug("four")
		var fourth_title: Rect2 = page._cards["capacity_3"].title.get_global_rect()
		_check(page._scroll.get_global_rect().encloses(fourth_title), "四地区时初始视口露出第四张完整标题，提示下方还有内容")
		_check(page._scroll.get_v_scroll_bar().visible and page._list_hint.visible, "最小溢出时纸尺滚动条与更多地区提示可见")
		await _capture("08-capacity-four-top.png")
		payload.regions = regions
	page.call("render", payload)
	await _settle()
	_check(page.call("get_state_snapshot").region_count == 10, "10 地区全部创建，没有 mini 截断")
	_check(page.call("get_state_snapshot").map_region_count == 10, "列表与地图地区数量一致")
	_scroll_debug("ten")
	await _capture("04-capacity-ten-top.png")
	if scroll_review:
		var schedule: Control = page._canvas.get_node("SchedulePaper")
		var schedule_rect := schedule.get_global_rect()
		var selected_before: String = page.call("get_state_snapshot").selected_region_id
		await _drag_scroll_to_bottom()
		_scroll_debug("drag_end")
		_check(_at_scroll_bottom() and not page._list_hint.visible, "真实拖动纸签到末尾后列表抵底且更多提示消失")
		_check(schedule.get_global_rect() == schedule_rect and page.call("get_state_snapshot").selected_region_id == selected_before, "拖动列表不移动只读日程，也不改变选中地区")
		await _capture("09-drag-ten-bottom.png")
		var up := InputEventMouseButton.new()
		up.position = page._scroll.get_global_rect().get_center()
		up.button_index = MOUSE_BUTTON_WHEEL_UP
		up.factor = 6.0
		up.pressed = true
		Input.parse_input_event(up)
		await _settle(3)
		_check(not _at_scroll_bottom() and page._list_hint.visible, "从末尾向上滚动后更多提示恢复")
	for i in range(12):
		var wheel := InputEventMouseButton.new()
		wheel.position = page._scroll.get_global_rect().get_center()
		wheel.button_index = MOUSE_BUTTON_WHEEL_DOWN
		wheel.factor = 6.0
		wheel.pressed = true
		Input.parse_input_event(wheel)
		await _settle(2)
		await _film(1)
	await _capture("05-capacity-ten-bottom.png")
	_check(_at_scroll_bottom(), "真实鼠标滚轮能浏览至第十地区末尾")
	_check(page._cards["capacity_9"].photo.texture == null, "未知地区缺图不冒用其他地区资源")
	var bottom: int = page._scroll.scroll_vertical
	page.call("render", payload)
	await _settle()
	_check(page._scroll.scroll_vertical == bottom, "同选区数据刷新保留滚动位置")
	page._cards["capacity_9"].hit.grab_focus()
	await _settle()
	_check(root.gui_get_focus_owner() == page._cards["capacity_9"].hit, "末尾地区有真实键盘焦点")
	payload.selected_region_id = "capacity_9"
	payload.region_enter_enabled = false
	payload.region_status_primary = "地区锁定"
	payload.region_unlock_gap = "容量样本 · 等待地区准入条件"
	page.call("render", payload)
	await _settle()
	await _capture("06-capacity-long-name-missing-art.png")
	if selection_review:
		_check(_highlight_count() == 1 and page._cards["capacity_9"].title_paper.visible and page._pins["capacity_9"].gold.visible, "第十地区缺图与锁定时仍独立显示选中状态")
	_check(page.call("get_state_snapshot").shared_texture_identity, "缺图状态三处仍保持同一身份")
	payload.selected_region_id = "us"
	payload.region_enter_enabled = true
	payload.region_status_primary = "红线升温"
	page.call("render", payload)
	await _settle(8)
	_check(page._scroll.scroll_vertical == 0, "选回首地区时对应卡自动滚回可见范围")
	# 恢复真实数据，确保本地启动后不带测试内容。
	game.call("_refresh_all")
	await _settle()
	if scroll_review:
		_scroll_debug("restored")
		_check(not page._scroll.get_v_scroll_bar().visible and not page._list_hint.visible and page._scroll.scroll_vertical == 0, "恢复真实三地区后滚动条、提示和滚动偏移均清除")
	if polish_review and capture_enabled:
		root.size = Vector2i(1280, 720)
		await _settle(8)
		# Window.size 是物理像素；get_global_rect 与 Viewport 可见矩形同属拉伸前逻辑坐标。
		_check(root.get_visible_rect().encloses(page._primary.get_global_rect()), "1280×720桌面等比缩放后进入按钮仍在视口内")
		await _capture("15-desktop-1280x720.png")
		root.size = Vector2i(1920, 1080)
		await _settle(5)
	var final_result := true
	for result in results:
		final_result = final_result and bool(result["通过"])
	var report := FileAccess.open(output_dir + "/checks.json", FileAccess.WRITE)
	report.store_string(JSON.stringify({"全部通过": final_result, "运行环境": DisplayServer.get_name(), "检查": results, "选中态专项": selection_review, "动效帧数": motion_frames, "动效帧率": 60, "选中动效帧已保存": capture_enabled and not stills_only, "滚动专项": scroll_review, "滚动输入步数": scroll_frames, "滚动抽帧数": scroll_frames if capture_enabled and not (task_review and stills_only) else 0, "任务专项": task_review}, "\t"))
	report.close()
	print("SOFT_COLUMNS_RESULT ", final_result, " checks=", results.size())
	game.queue_free()
	await _settle(3)
	quit(0 if final_result else 1)

func _click(control: Control) -> void:
	var at := control.get_global_rect().get_center()
	var motion := InputEventMouseMotion.new()
	motion.position = at
	motion.global_position = at
	Input.parse_input_event(motion)
	Input.flush_buffered_events()
	for pressed in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = at
		event.global_position = at
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		Input.parse_input_event(event)
		Input.flush_buffered_events()
		if not pressed and selection_review and (control == page._cards["east_asia"].hit or control == page._pins["us"].hit) and motion_clips < 2:
			await _record_selection_motion(control)
	await _settle(4)

func _keyboard_enter() -> void:
	for pressed in [true, false]:
		var event := InputEventKey.new()
		event.keycode = KEY_ENTER
		event.pressed = pressed
		Input.parse_input_event(event)
		await _settle(3)

func _capture(filename: String) -> void:
	print("CAPTURE ", filename)
	if not capture_enabled:
		return
	await _settle(2)
	# 隐藏运行窗口不一定连续发出 frame_post_draw，显式刷新真实渲染后读取 viewport。
	RenderingServer.force_draw(false)
	var image := root.get_texture().get_image()
	image.save_png(ProjectSettings.globalize_path(output_dir + "/" + filename))

func _film(count: int) -> void:
	if not capture_enabled or selection_review:
		return
	for i in range(count):
		await _capture("frames/%04d.png" % frames)
		frames += 1
		await create_timer(0.10).timeout

func _highlight_count() -> int:
	var count := 0
	for card in page._cards.values():
		if card.title_paper.visible and card.backing.visible:
			count += 1
	return count

func _at_scroll_bottom() -> bool:
	var bar: VScrollBar = page._scroll.get_v_scroll_bar()
	return bar.max_value > bar.page and absf(bar.value - (bar.max_value - bar.page)) <= 1.0

func _review_long_task_content() -> void:
	# 仅注入表现层压力样本；完成后还原真实数据。
	var payload: Dictionary = game.call("_build_explore_payload").duplicate(true)
	payload.region_mission_preview[0].name = "跨海电台连续收到来自失联渔船的同一组午夜呼号与无人应答的求救信号"
	payload.region_mission_preview[1].name = "沿着地下铁末班车留下的空白车票追查最后一站与突然消失的乘客"
	var index: int = 0
	for i in range(payload.regions.size()):
		if payload.regions[i].id == "us":
			index = i
	var news: Dictionary = page.Catalog.get_news(payload.regions[index])
	news.headline = "失联渔船的午夜呼号又从一间无人洗衣店传来"
	news.deck = "值班记录中的潮汐时间与街区停电同时发生。\n第二份来稿确认了同一段电波，但来源仍待核实。"
	payload.regions[index].world_map_news = news
	payload.region_warning_text = "存在限时任务，请进入地区查看具体截止条件。连续追踪还会影响后续地区开放。"
	page.call("render", payload)
	await _settle(8)
	for label in [page._headline, page._deck, page._task_warning, page._task_labels[0]]:
		print("TEXT_METRICS ", label.name, " size=", label.size, " font_height=", label.get_theme_font("font").get_height(label.get_theme_font_size("font_size")), " lines=", label.get_line_count(), " visible=", label.get_visible_line_count())
		_check(label.get_visible_line_count() >= mini(2, label.get_line_count()), "长文实际可见行数充足：" + label.name)
	_check(page._task_labels[0].get_line_count() == 2 and page._task_labels[1].get_line_count() == 2, "两条长任务名均获得两行承载")
	_check(page._headline.get_global_rect().end.y <= page._deck.get_global_rect().position.y and page._deck.get_global_rect().end.y <= page._task_paper.get_global_rect().position.y, "两行新闻标题与摘要不侵入任务纸面")
	var text_clear: bool = page._task_warning.get_global_rect().end.y <= page._task_rows[0].get_global_rect().position.y
	for i in range(2):
		text_clear = text_clear and page._task_labels[i].get_global_rect().end.y <= page._task_meta[i].get_global_rect().position.y
	text_clear = text_clear and page._task_meta[1].get_global_rect().end.y < page._primary.get_global_rect().position.y
	_check(text_clear, "两行提醒、长任务名、耗时与主CTA保持各自可读空间")
	if polish_review:
		_check(page._task_paper.get_global_rect().end.y <= page._primary.get_global_rect().position.y - 12, "最长内容的任务纸面与进入按钮仍有独立段距")
		_check(page._task_meta[1].get_global_rect().end.y <= page._task_paper.get_global_rect().end.y - 14, "末条耗时留在纸内并保留底部余量")
	await _capture("13-long-content-layout-fixture.png")
	game.call("_refresh_all")
	await _settle(8)

func _scroll_debug(context: String) -> void:
	var bar: VScrollBar = page._scroll.get_v_scroll_bar()
	print("SCROLL ", context, " ", {"visible": bar.visible, "hint": page._list_hint.visible, "max": bar.max_value, "page": bar.page, "value": bar.value, "rect": bar.get_global_rect(), "container": page._scroll.get_global_rect(), "list_min": page._list.get_combined_minimum_size(), "list_size": page._list.size})

func _drag_scroll_to_bottom() -> void:
	var bar: VScrollBar = page._scroll.get_v_scroll_bar()
	var rect := bar.get_global_rect()
	var start := Vector2(rect.get_center().x, rect.position.y + 48)
	var finish := Vector2(start.x, rect.end.y - 8)
	var hover := InputEventMouseMotion.new()
	hover.position = start
	Input.parse_input_event(hover)
	await _settle(2)
	var down := InputEventMouseButton.new()
	down.position = start
	down.button_index = MOUSE_BUTTON_LEFT
	down.pressed = true
	Input.parse_input_event(down)
	await _settle(2)
	var previous := start
	for i in range(25):
		var at := start.lerp(finish, float(i) / 24.0)
		var move := InputEventMouseMotion.new()
		move.position = at
		move.relative = at - previous
		move.button_mask = MOUSE_BUTTON_MASK_LEFT
		Input.parse_input_event(move)
		await _settle(2)
		if not (task_review and stills_only):
			await _capture("scroll/%04d.png" % scroll_frames)
		scroll_frames += 1
		previous = at
	var up := InputEventMouseButton.new()
	up.position = finish
	up.button_index = MOUSE_BUTTON_LEFT
	up.pressed = false
	Input.parse_input_event(up)
	await _settle(3)

func _neutral_pointer() -> void:
	var event := InputEventMouseMotion.new()
	event.position = Vector2(1150, 950)
	Input.parse_input_event(event)
	var owner := root.gui_get_focus_owner()
	if is_instance_valid(owner):
		owner.release_focus()
	await _settle(16)

func _record_selection_motion(control: Control) -> void:
	var stable_rect := control.get_global_rect()
	# 先让真实 mouse-up 完成分发，再移开指针和释放焦点，避免取消尚未处理的按压。
	await process_frame
	var at := InputEventMouseMotion.new()
	at.position = Vector2(1150, 950)
	Input.parse_input_event(at)
	var owner := root.gui_get_focus_owner()
	if is_instance_valid(owner):
		owner.release_focus()
	# --fixed-fps 60 使每帧对应 1/60 秒模拟时间，PNG 编码开销不会跳过补间帧。
	for i in range(16):
		await process_frame
		if capture_enabled and not stills_only:
			RenderingServer.force_draw(false)
			root.get_texture().get_image().save_png(ProjectSettings.globalize_path(output_dir + "/motion/%04d.png" % motion_frames))
		motion_frames += 1
	_check(control.get_global_rect() == stable_rect, "纸张补间期间点击热区保持稳定")
	motion_clips += 1
