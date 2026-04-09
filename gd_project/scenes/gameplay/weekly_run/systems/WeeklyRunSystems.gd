extends RefCounted
class_name WeeklyRunSystems

const Content = preload("res://scenes/gameplay/weekly_run/content/WeeklyRunContent.gd")
const WeeklyRunState = preload("res://scenes/gameplay/weekly_run/state/WeeklyRunState.gd")

static func initialize_new_run(state: WeeklyRunState) -> void:
	var briefing_event_id := _roll_briefing_event_id()
	var active_tasks := _roll_active_tasks()
	state.reset_for_new_run(briefing_event_id, active_tasks, [])
	state.opportunity_ids = collect_opportunity_ids(state)
	state.append_log("[color=#f0d8a0]第 1 周开始[/color]：新的周简报已经送达。")

static func begin_next_week(state: WeeklyRunState) -> void:
	var briefing_event_id := _roll_briefing_event_id()
	var active_tasks := _roll_active_tasks()
	state.begin_next_week(briefing_event_id, active_tasks, [])
	state.opportunity_ids = collect_opportunity_ids(state)
	state.append_log("[color=#f0d8a0]进入第 %d 周[/color]：新的简报、任务与机会池已经刷新。" % state.week)

static func start_explore(state: WeeklyRunState) -> void:
	state.current_phase = "explore"

static func enter_editorial(state: WeeklyRunState) -> void:
	state.current_phase = "editorial"
	_rebuild_editorial_pipeline(state)

static func build_briefing_lines(state: WeeklyRunState) -> Array[String]:
	var lines: Array[String] = [Content.get_briefing_text(state.briefing_event_id)]
	if not state.active_tasks.is_empty():
		lines.append("")
		lines.append("[color=#d8c8a2]本周任务[/color]")
		for task in state.active_tasks:
			lines.append("- %s" % str(task.summary))
	if not state.next_week_hooks.is_empty():
		lines.append("")
		lines.append("[color=#9fb3c7]上期余波[/color]")
		lines.append("利润档：%s" % str(state.next_week_hooks.get("profit_band", "neutral")))
		if state.next_week_hooks.has("dominant_axis"):
			lines.append("本期倾向：%s" % str(state.next_week_hooks.get("dominant_axis", "mixed")))
	return lines

static func collect_opportunity_ids(state: WeeklyRunState) -> Array[String]:
	var ids: Array[String] = []
	for region in Content.REGION_DATA:
		if not is_region_unlocked(state, region):
			continue
		for node in region.nodes:
			if is_node_visible(state, node):
				ids.append(str(node.id))
	return ids

static func get_region_by_id(region_id: String) -> Dictionary:
	for region in Content.REGION_DATA:
		if str(region.id) == region_id:
			return region
	return {}

static func get_node_by_id(region_id: String, node_id: String) -> Dictionary:
	var region := get_region_by_id(region_id)
	for node in region.get("nodes", []):
		if str(node.id) == node_id:
			return node
	return {}

static func get_node_availability(state: WeeklyRunState, node: Dictionary, selected_staff_ids: Array[String], totals: Dictionary) -> Dictionary:
	if state.current_phase != "explore":
		return {"enabled": false, "reason": "先确认本周简报，再进入探索"}
	if state.remaining_days < int(node.days):
		return {"enabled": false, "reason": "剩余天数不足"}
	if selected_staff_ids.is_empty():
		return {"enabled": false, "reason": "先选择 1-3 名职员"}
	if str(node.kind) == "temp" and bool(state.resolved_nodes.get(str(node.id), false)):
		return {"enabled": false, "reason": "这个临时节点本周已处理"}
	if node.has("deadline_day") and state.remaining_days < int(node.deadline_day):
		return {"enabled": false, "reason": "这个突发节点已经过期"}
	for key in node.need.keys():
		if int(totals.get(str(key), 0)) < int(node.need[key]):
			return {"enabled": false, "reason": "派遣属性未满足需求"}
	return {"enabled": true, "reason": "可执行"}

static func has_legal_dispatches(state: WeeklyRunState) -> bool:
	var staff_ids: Array[String] = []
	for staff in Content.STAFF_POOL:
		staff_ids.append(str(staff.id))
	for region in Content.REGION_DATA:
		if not is_region_unlocked(state, region):
			continue
		for node in region.nodes:
			if not is_node_visible(state, node):
				continue
			for combo in _enumerate_staff_combinations(staff_ids, 3):
				var totals := _build_staff_totals(combo)
				if bool(get_node_availability(state, node, combo, totals).enabled):
					return true
	return false

static func is_region_unlocked(state: WeeklyRunState, region: Dictionary) -> bool:
	match str(region.unlock_rule):
		"always":
			return true
		"east_asia":
			return state.macro_stats.reputation >= 55 or bool(state.flags.get("roswell_dossier", false))
		_:
			return false

static func is_node_visible(state: WeeklyRunState, node: Dictionary) -> bool:
	if str(node.kind) != "hidden":
		return true
	return _hidden_node_unlocked(state, node)

static func perform_split_check(node: Dictionary, totals: Dictionary) -> Dictionary:
	var p := float(Content.DIFFICULTY_P.get(str(node.difficulty), 0.50))
	var attr_a := int(totals.explore) + int(totals.insight) + int(totals.occult)
	var attr_b := int(totals.survival) + int(totals.reason)
	var total_pool: int = maxi(1, attr_a + attr_b)
	var enemy_a := floori(float(int(node.enemy)) * attr_a / total_pool)
	var enemy_b := int(node.enemy) - enemy_a
	var k_a := clampi(int(node.k_a), 0, max(0, attr_a - enemy_a))
	var k_b := clampi(int(node.k_b), 0, max(0, attr_b - enemy_b))
	var dice_a := _roll_dice(attr_a, p)
	var dice_b := _roll_dice(attr_b, p)
	var negated_a := _random_negate_indices(attr_a, mini(enemy_a, attr_a))
	var negated_b := _random_negate_indices(attr_b, mini(enemy_b, attr_b))
	var hit_a := 0
	for index in range(attr_a):
		if not negated_a.has(index) and dice_a[index]:
			hit_a += 1
	var hit_b := 0
	for index in range(attr_b):
		if not negated_b.has(index) and dice_b[index]:
			hit_b += 1
	var tier := "fail"
	if hit_a >= k_a and hit_b >= k_b:
		tier = "major"
	elif hit_a >= k_a or hit_b >= k_b:
		tier = "minor"
	return {
		"node_id": str(node.id),
		"dice_a": dice_a,
		"dice_b": dice_b,
		"negated_a": negated_a,
		"negated_b": negated_b,
		"hit_a": hit_a,
		"hit_b": hit_b,
		"k_a": k_a,
		"k_b": k_b,
		"tier": tier,
	}

static func calculate_node_probabilities(node: Dictionary, totals: Dictionary) -> Dictionary:
	var attr_a := int(totals.explore) + int(totals.insight) + int(totals.occult)
	var attr_b := int(totals.survival) + int(totals.reason)
	var p := float(Content.DIFFICULTY_P.get(str(node.difficulty), 0.50))
	var total_pool: int = maxi(1, attr_a + attr_b)
	var enemy_a := floori(float(int(node.enemy)) * attr_a / total_pool)
	var enemy_b := int(node.enemy) - enemy_a
	var k_a := clampi(int(node.k_a), 0, max(0, attr_a - enemy_a))
	var k_b := clampi(int(node.k_b), 0, max(0, attr_b - enemy_b))
	var p_a := _binomial_cdf_ge(attr_a - enemy_a, k_a, p)
	var p_b := _binomial_cdf_ge(attr_b - enemy_b, k_b, p)
	return {
		"major": p_a * p_b,
		"minor": p_a * (1.0 - p_b) + (1.0 - p_a) * p_b,
		"fail": (1.0 - p_a) * (1.0 - p_b),
	}

static func apply_dispatch_resolution(state: WeeklyRunState, node: Dictionary, roll: Dictionary, region_name: String) -> Dictionary:
	state.remaining_days = max(0, state.remaining_days - int(node.days))
	state.resolved_nodes[str(node.id)] = true
	state.last_dispatch_roll = roll.duplicate(true)

	var dispatch_result := {
		"node_id": str(node.id),
		"node_name": str(node.name),
		"source_region": region_name,
		"tier": str(roll.tier),
		"days_cost": int(node.days),
	}
	state.dispatch_results.append(dispatch_result)

	var material := _generate_material(state, node, roll, region_name)
	state.material_inventory.append(material)
	state.new_material_ids.append(str(material.id))

	var phase_message := ""
	match str(roll.tier):
		"major":
			state.macro_stats.reputation += 3
			state.macro_stats.credibility += 2 if node.type == "sci" else 1
			state.macro_stats.weirdness += 2 if node.type == "occult" else 0
			state.macro_stats.order += 1
			phase_message = "这次外采拿到了能直接进入编辑部的高质量素材。"
		"minor":
			state.macro_stats.reputation += 1
			state.macro_stats.credibility += 1 if node.type == "sci" else 0
			state.macro_stats.weirdness += 1 if node.type == "occult" else 0
			phase_message = "这条素材可用，但还缺少最后一击。"
		_:
			state.macro_stats.order -= 2
			state.macro_stats.mania += 2
			phase_message = "外采失手，只带回一条残缺素材。"

	if str(node.id) == "skin" and str(roll.tier) != "fail":
		state.flags["roswell_dossier"] = true

	state.opportunity_ids = collect_opportunity_ids(state)
	return {
		"message": phase_message,
		"material": material,
		"dispatch_result": dispatch_result,
	}

static func build_settlement_preview(state: WeeklyRunState, slot_assignment: Dictionary) -> Dictionary:
	return calculate_editorial_stats(state, slot_assignment)

static func publish_issue(state: WeeklyRunState, slot_assignment: Dictionary) -> Dictionary:
	state.slot_assignment = slot_assignment.duplicate(true)
	state.settlement_preview = calculate_editorial_stats(state, state.slot_assignment)
	state.published_issue = {
		"week": state.week,
		"articles": _collect_placed_articles(state, state.slot_assignment),
		"stats": state.settlement_preview.duplicate(true),
	}
	return state.settlement_preview

static func settle_published_issue(state: WeeklyRunState) -> Dictionary:
	var stats: Dictionary = state.settlement_preview.duplicate(true)
	if stats.is_empty():
		stats = calculate_editorial_stats(state, state.slot_assignment)
		state.settlement_preview = stats.duplicate(true)

	var result := stats.duplicate(true)
	result.week = state.week
	result.editorial_profile_before = state.editorial_profile
	state.subscribers = int(stats.next_subscribers)
	state.editorial_profile = float(stats.next_editorial_profile)
	result.editorial_profile_after = state.editorial_profile
	state.macro_stats.reputation += int(clamp(roundi(stats.profit / 700.0), -2, 3))
	state.macro_stats.credibility += 1 if stats.axis_p >= stats.axis_m and stats.axis_p >= stats.axis_l else 0
	state.macro_stats.weirdness += 1 if count_occult_new_materials(state) >= 2 else 0
	state.macro_stats.order += 1 if stats.empty_slots == 0 else -1
	state.macro_stats.mania = max(0, state.macro_stats.mania - 1 if stats.m_balance >= 1.0 else state.macro_stats.mania + 1)
	result.commentary = _settlement_commentary(stats)
	state.settlement_result = result
	state.next_week_hooks = _build_next_week_hooks(stats)
	state.current_phase = "summary"
	return result

static func calculate_editorial_stats(state: WeeklyRunState, slot_assignment: Dictionary) -> Dictionary:
	var placed := []
	for slot in Content.SLOT_DATA:
		var article := get_article_by_id(state, int(slot_assignment.get(str(slot.id), -1)))
		if not article.is_empty():
			placed.append({"slot": slot, "article": article})
	var filled_slots := placed.size()
	var empty_slots := Content.SLOT_DATA.size() - filled_slots
	var total_base_value := 0.0
	var tag_counts := {}
	var neg_penalty := 0
	var axis_p := 0
	var axis_m := 0
	var axis_l := 0
	for item in placed:
		var slot: Dictionary = item.slot
		var article: Dictionary = item.article
		total_base_value += float(article.base_value) * float(slot.weight)
		neg_penalty += article.negatives.size()
		for tag in article.tags:
			tag_counts[str(tag)] = int(tag_counts.get(str(tag), 0)) + 1
			if tag in ["Politics", "Military", "Economy"]:
				axis_p += 1
			elif tag in ["Sport", "Shopping"]:
				axis_m += 1
			else:
				axis_l += 1
	var unique_tags := tag_counts.size()
	var combo_raw := 0
	var linked_tags := 0
	for count in tag_counts.values():
		if int(count) > 1:
			combo_raw += int(count) - 1
			linked_tags += 1
	var total_axes: int = maxi(1, axis_p + axis_m + axis_l)
	var avg_axis := float(total_axes) / 3.0
	var deviation := absf(axis_p - avg_axis) + absf(axis_m - avg_axis) + absf(axis_l - avg_axis)
	var m_quality := clampf(0.88 + total_base_value / 2100.0, 0.88, 1.55)
	var m_combo := clampf(1.00 + combo_raw * 0.04, 1.00, 1.32)
	var m_diversity := clampf(0.92 + unique_tags * 0.035, 0.92, 1.24)
	var m_layout := 0.88 + filled_slots * 0.07
	var m_empty := clampf(1.00 - empty_slots * 0.12, 0.35, 1.00)
	var m_penalty := clampf(1.00 - neg_penalty * 0.05, 0.70, 1.00)
	var m_link := clampf(1.00 + linked_tags * 0.03, 1.00, 1.18)
	var m_balance := clampf(1.14 - deviation * 0.06, 0.82, 1.14)
	var m_bias := clampf(1.00 + _dominant_axis_shift(axis_p, axis_m, axis_l) * state.editorial_profile * 0.06, 0.92, 1.08)
	var demand := int(round((3200.0 + state.subscribers * 0.45 + total_base_value * 1.45) * m_quality * m_combo * m_diversity * m_layout * m_empty * m_penalty * m_link * m_balance * m_bias))
	var print_capacity := 4200
	var sold := clampi(demand, 0, print_capacity)
	var news_revenue := sold * 0.30
	var sub_revenue := state.subscribers * 0.18
	var ad_revenue := 2.0 * 180.0 * clampf(0.70 + linked_tags * 0.05 + (m_bias - 1.0), 0.45, 1.20)
	var total_revenue := news_revenue + sub_revenue + ad_revenue
	var total_cost := 210.0 + 980.0 + 260.0 + filled_slots * 28.0
	var profit := total_revenue - total_cost
	return {
		"filled_slots": filled_slots,
		"empty_slots": empty_slots,
		"total_base_value": int(round(total_base_value)),
		"unique_tags": unique_tags,
		"combo_raw": combo_raw,
		"linked_tags": linked_tags,
		"neg_penalty": neg_penalty,
		"axis_p": axis_p,
		"axis_m": axis_m,
		"axis_l": axis_l,
		"m_quality": m_quality,
		"m_combo": m_combo,
		"m_diversity": m_diversity,
		"m_layout": m_layout,
		"m_empty": m_empty,
		"m_penalty": m_penalty,
		"m_link": m_link,
		"m_balance": m_balance,
		"m_bias": m_bias,
		"demand": demand,
		"sold": sold,
		"print_capacity": print_capacity,
		"news_revenue": news_revenue,
		"sub_revenue": sub_revenue,
		"ad_revenue": ad_revenue,
		"total_revenue": total_revenue,
		"total_cost": total_cost,
		"profit": profit,
		"next_subscribers": max(600, int(round(state.subscribers + profit / 130.0 + (m_balance - 1.0) * 180.0 + (m_quality - 1.0) * 220.0 - empty_slots * 45.0))),
		"next_editorial_profile": clampf(state.editorial_profile + _dominant_axis_shift(axis_p, axis_m, axis_l) * 0.12, -1.0, 1.0),
	}

static func get_article_by_id(state: WeeklyRunState, article_id: int) -> Dictionary:
	for article in state.article_candidates:
		if int(article.id) == article_id:
			return article
	return {}

static func count_occult_new_materials(state: WeeklyRunState) -> int:
	var count := 0
	for material in state.get_new_materials():
		if str(material.type) == "occult":
			count += 1
	return count

static func _rebuild_editorial_pipeline(state: WeeklyRunState) -> void:
	state.cognition_entries.clear()
	for material in state.material_inventory:
		state.cognition_entries.append(_cognition_from_material(material))
	state.article_candidates.clear()
	state.next_article_id = 1
	for cognition in state.cognition_entries:
		state.article_candidates.append(_article_from_cognition(state, cognition))
	while state.article_candidates.size() < 10:
		state.article_candidates.append(_generate_filler_article(state))
	state.sync_slot_assignment(Content.SLOT_DATA)

static func _cognition_from_material(material: Dictionary) -> Dictionary:
	var tag_pool: Array = Content.STORY_TAG_MAP.get(str(material.type), ["Shopping"])
	var primary := str(tag_pool[0])
	var secondary := str(tag_pool[(material.id.length() + 1) % tag_pool.size()])
	var quality_data: Dictionary = Content.QUALITY_MAP.get(int(material.tier), Content.QUALITY_MAP[1])
	return {
		"material_id": str(material.id),
		"title": str(material.title),
		"tags": [primary] if primary == secondary else [primary, secondary],
		"quality": str(quality_data.quality),
		"base_value": int(quality_data.base_value),
		"negatives": material.risk_flags.duplicate(),
		"source": "material_inventory",
	}

static func _article_from_cognition(state: WeeklyRunState, cognition: Dictionary) -> Dictionary:
	var article := {
		"id": state.next_article_id,
		"title": str(cognition.title),
		"tags": cognition.tags.duplicate(),
		"quality": str(cognition.quality),
		"base_value": int(cognition.base_value),
		"negatives": cognition.negatives.duplicate(),
		"source": str(cognition.source),
		"material_id": str(cognition.material_id),
	}
	state.next_article_id += 1
	return article

static func _generate_filler_article(state: WeeklyRunState) -> Dictionary:
	var all_tags := Content.FILLER_SUBJECTS.keys()
	var primary := str(all_tags[randi() % all_tags.size()])
	var subject_list: Array = Content.FILLER_SUBJECTS[primary]
	var quality_roll: int = [1, 1, 2, 2, 3][randi() % 5]
	var quality_data: Dictionary = Content.QUALITY_MAP[quality_roll]
	var article := {
		"id": state.next_article_id,
		"title": str(subject_list[randi() % subject_list.size()]),
		"tags": [primary],
		"quality": str(quality_data.quality),
		"base_value": int(quality_data.base_value * 0.85),
		"negatives": ["thin_source"] if quality_roll == 1 and randf() < 0.45 else [],
		"source": "filler",
	}
	state.next_article_id += 1
	return article

static func _generate_material(state: WeeklyRunState, node: Dictionary, roll: Dictionary, region_name: String) -> Dictionary:
	var tier := 1
	if roll.tier == "major":
		tier = 3
	elif roll.tier == "minor":
		tier = 2
	var suffixes := {
		"sci": ["军方备忘录", "照片底片", "雷达转录", "船运清单"],
		"occult": ["低语片段", "异象素描", "供述抄本", "祭仪录音"],
		"pop": ["目击者热帖", "城市速报", "流言剪报", "街头口供"],
	}
	var suffix_list: Array = suffixes.get(str(node.type), ["现场摘要"])
	var material_id := "%s_%d_%d" % [str(node.id), state.week, state.next_material_serial]
	state.next_material_serial += 1
	return {
		"id": material_id,
		"title": "%s · %s" % [str(node.name), str(suffix_list[randi() % suffix_list.size()])],
		"type": str(node.type),
		"tier": tier,
		"source_region": region_name,
		"source_node": str(node.name),
		"risk_flags": ["fragmented"] if roll.tier == "fail" else [],
	}

static func _collect_placed_articles(state: WeeklyRunState, slot_assignment: Dictionary) -> Array[Dictionary]:
	var placed: Array[Dictionary] = []
	for slot in Content.SLOT_DATA:
		var article := get_article_by_id(state, int(slot_assignment.get(str(slot.id), -1)))
		if not article.is_empty():
			placed.append({"slot_id": str(slot.id), "article": article.duplicate(true)})
	return placed

static func _build_next_week_hooks(stats: Dictionary) -> Dictionary:
	var dominant_axis := "mixed"
	if int(stats.axis_p) >= int(stats.axis_m) and int(stats.axis_p) >= int(stats.axis_l):
		dominant_axis = "public_affairs"
	elif int(stats.axis_m) >= int(stats.axis_l):
		dominant_axis = "mass_attention"
	else:
		dominant_axis = "light_features"
	return {
		"profit_band": "positive" if float(stats.profit) >= 0.0 else "negative",
		"dominant_axis": dominant_axis,
		"empty_slots": int(stats.empty_slots),
	}

static func _roll_briefing_event_id() -> String:
	return str(Content.BRIEFING_EVENT_IDS[randi() % Content.BRIEFING_EVENT_IDS.size()])

static func _roll_active_tasks() -> Array[Dictionary]:
	var candidates: Array = Content.BRIEFING_TASK_TEMPLATES.duplicate(true)
	candidates.shuffle()
	var count := mini(3, candidates.size())
	var tasks: Array[Dictionary] = []
	for index in range(count):
		tasks.append(candidates[index])
	return tasks

static func _build_staff_totals(selected_staff_ids: Array[String]) -> Dictionary:
	var totals := {"explore": 0, "insight": 0, "occult": 0, "survival": 0, "reason": 0, "social": 0}
	for staff in Content.STAFF_POOL:
		if selected_staff_ids.has(str(staff.id)):
			for key in totals.keys():
				totals[key] += int(staff.attrs[key])
	return totals

# Stable GDScript still does not support nested typed collections such as Array[Array[String]].
static func _enumerate_staff_combinations(staff_ids: Array[String], max_size: int) -> Array:
	var output: Array = []
	for size in range(1, mini(max_size, staff_ids.size()) + 1):
		_collect_staff_combinations(staff_ids, size, 0, [], output)
	return output

static func _collect_staff_combinations(staff_ids: Array[String], target_size: int, start_index: int, current: Array[String], output: Array) -> void:
	if current.size() == target_size:
		output.append(current.duplicate())
		return
	for index in range(start_index, staff_ids.size()):
		current.append(staff_ids[index])
		_collect_staff_combinations(staff_ids, target_size, index + 1, current, output)
		current.pop_back()

static func _hidden_node_unlocked(state: WeeklyRunState, node: Dictionary) -> bool:
	match str(node.get("unlock_rule", "")):
		"hidden_monolith":
			return state.macro_stats.mania >= 35 and state.macro_stats.weirdness >= 40
		_:
			return true

static func _dominant_axis_shift(axis_p: int, axis_m: int, axis_l: int) -> float:
	if axis_p >= axis_m and axis_p >= axis_l:
		return -1.0
	if axis_m >= axis_l:
		return 1.0
	return 0.6

static func _settlement_commentary(stats: Dictionary) -> String:
	if float(stats.profit) >= 700.0:
		return "这一期既卖得动，也让编辑部的定位更清晰，正式周循环链路已经开始成形。"
	if float(stats.profit) >= 0.0:
		return "这一期勉强盈利，版面结构已经可用，但仍要继续压空版和偏科。"
	return "这一期亏损，主要问题通常是空版过多、题材失衡或高价值稿件不足。"

static func _roll_dice(n: int, p: float) -> Array:
	var results := []
	for _i in range(max(0, n)):
		results.append(randf() < p)
	return results

static func _random_negate_indices(total: int, count: int) -> Array:
	var indices := []
	for index in range(total):
		indices.append(index)
	indices.shuffle()
	return indices.slice(0, mini(count, total))

static func _binomial_coeff(n: int, k: int) -> int:
	if k < 0 or k > n:
		return 0
	if k == 0 or k == n:
		return 1
	var result := 1
	var limit := mini(k, n - k)
	for i in range(limit):
		result = result * (n - i) / (i + 1)
	return result

static func _binomial_pmf(n: int, k: int, p: float) -> float:
	return _binomial_coeff(n, k) * pow(p, k) * pow(1.0 - p, n - k)

static func _binomial_cdf_ge(n: int, k: int, p: float) -> float:
	var total := 0.0
	for value in range(k, n + 1):
		total += _binomial_pmf(n, value, p)
	return total
