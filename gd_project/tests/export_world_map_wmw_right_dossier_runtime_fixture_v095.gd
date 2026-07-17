extends SceneTree

const Systems = preload("res://scenes/gameplay/weekly_run/systems/WeeklyRunSystems.gd")
const OUT_PATH := "res://Assets/ui/angus_packaging/world_map/wmw_v095_right_dossier_candidate_a5/right_dossier_candidate_a5_runtime_fixture.json"


func _init() -> void:
	call_deferred("_export_fixture")


func _export_fixture() -> void:
	var state = Systems.WeeklyRunState.new()
	state.current_phase = "explore"
	var region: Dictionary = Systems.Content.REGION_DATA[0]
	var counts := {
		"visible": 0,
		"deadline": 0,
		"chain": 0,
		"clue": 0,
	}
	var mission_preview: Array[Dictionary] = []
	for node in region.get("nodes", []):
		if not Systems.is_node_visible(state, node):
			continue
		counts["visible"] = int(counts["visible"]) + 1
		match str(node.get("kind", "permanent")):
			"temp":
				counts["deadline"] = int(counts["deadline"]) + 1
			"chain":
				counts["chain"] = int(counts["chain"]) + 1
			_:
				counts["clue"] = int(counts["clue"]) + 1
		if mission_preview.size() < 3:
			var kind := str(node.get("kind", "permanent"))
			var kind_label := "线索"
			if kind == "temp":
				kind_label = "限时"
			elif kind == "chain":
				kind_label = "深链"
			mission_preview.append({
				"id": str(node.get("id", "")),
				"name": str(node.get("name", "")),
				"kind": kind,
				"kind_label": kind_label,
				"days": int(node.get("days", 0)),
			})

	var unlocked := Systems.is_region_unlocked(state, region)
	var status_primary := "锁定"
	if unlocked:
		if int(counts["deadline"]) > 0:
			status_primary = "红线升温"
		elif int(counts["chain"]) > 0:
			status_primary = "青线追踪"
		else:
			status_primary = "可进入"
	var status_display_text := status_primary

	var region_brief := str(region.get("hint", "")).replace("初始解锁。", "").strip_edges()
	if region_brief == "":
		region_brief = "本周取材区已打开，可进入后选择具体线报。"
	var warning_text := "暂无额外惩罚。"
	if not unlocked:
		warning_text = str(region.get("unlock_gap", "缺少线索许可"))
	elif int(counts["deadline"]) > 0:
		warning_text = "本周剩余 %d 天，红线稿应优先处理。" % int(state.remaining_days)
	elif int(counts["chain"]) > 0:
		warning_text = "青线追踪会推进后续地区。"

	var fixture := {
		"schema_version": 1,
		"candidate": "right_dossier_candidate_a5_v0.9.5",
		"provenance": "production_runtime_export",
		"generated_from_production_data": true,
		"source_files": [
			"gd_project/scenes/gameplay/weekly_run/content/WeeklyRunContent.gd",
			"gd_project/scenes/gameplay/weekly_run/systems/WeeklyRunSystems.gd",
			"gd_project/scenes/gameplay/weekly_run/state/WeeklyRunState.gd",
		],
		"region_id": str(region.get("id", "")),
		"region_title": str(region.get("name", "")),
		"region_unlocked": unlocked,
		"remaining_days": int(state.remaining_days),
		"counts": counts,
		"status_primary": status_primary,
		"status_display_text": status_display_text,
		"region_body_text": "%s\n%s" % [region_brief, warning_text],
		"mission_intel_title": str(Systems.Content.WORLD_MAP_UI_COPY["mission_intel_collapsed"]),
		"mission_intel_facts": "限时 %d · 线索 %d · 深链 %d" % [
			int(counts["deadline"]),
			int(counts["clue"]),
			int(counts["chain"]),
		],
		"mission_preview": mission_preview,
		"mission_preview_total": int(counts["visible"]),
		"primary_enter_label": str(Systems.Content.WORLD_MAP_UI_COPY["region_enter_enabled"] if unlocked else Systems.Content.WORLD_MAP_UI_COPY["region_enter_disabled"]),
	}

	var absolute_path := ProjectSettings.globalize_path(OUT_PATH)
	DirAccess.make_dir_recursive_absolute(absolute_path.get_base_dir())
	var file := FileAccess.open(absolute_path, FileAccess.WRITE)
	if file == null:
		push_error("Cannot open runtime fixture output: %s" % absolute_path)
		quit(1)
		return
	file.store_string(JSON.stringify(fixture, "  ", false) + "\n")
	file.close()
	print("Wrote production runtime fixture: %s" % absolute_path)
	quit(0)
