extends SceneTree

const RegionTaskManifest := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskAssetManifest.gd")
const UiStyle := preload("res://scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd")

func _init() -> void:
	var manifest := RegionTaskManifest.load_manifest(true)
	_assert(not manifest.is_empty(), "region task manifest should load through runtime file access")
	_assert(str(manifest.get("id", "")) == "region_task_board_assetized_v1", "manifest id should match region task assetized v1")
	_assert(UiStyle.has_region_task_assetized_contract(), "UiStyle should recognize the complete region task asset contract")

	var visual_lock: Dictionary = manifest.get("visual_lock", {})
	_assert(str(visual_lock.get("source_asset", "")).ends_with("region-task-board-clean-pixel-v2.png"), "visual lock should anchor to approved region task board art")
	_assert(_contains(visual_lock.get("must_keep", []), "central map low-poly paper material"), "visual lock should preserve the approved central map material")
	_assert(_contains(visual_lock.get("must_avoid", []), "new visual direction"), "visual lock should reject a new visual direction")
	_assert(_contains(visual_lock.get("must_avoid", []), "yellowed archive paper"), "visual lock should reject yellowed archive paper")
	_assert(_contains(visual_lock.get("must_avoid", []), "baked fake pins"), "visual lock should reject baked fake pins")

	_assert(_has_asset("rt_map_base_clean", manifest), "clean map base asset should exist")
	_assert(_has_asset("rt_pin_atlas", manifest), "pin atlas should exist")
	_assert(_has_asset("rt_task_card_atlas", manifest), "task card atlas should exist")
	_assert(_has_asset("rt_cta_dispatch_atlas", manifest), "dispatch CTA atlas should exist")
	_assert(_has_asset("rt_advance_day_atlas", manifest), "advance day atlas should exist")
	_assert(_has_asset("rt_hud_strip", manifest), "HUD strip should exist")

	for frame_id in ["normal", "hover", "selected", "locked", "completed", "urgent"]:
		_assert(RegionTaskManifest.has_frame("rt_pin_atlas", frame_id, manifest), "pin atlas frame should exist: %s" % frame_id)
	for frame_id in ["default", "hover", "pressed", "disabled", "focus", "loading"]:
		_assert(RegionTaskManifest.has_frame("rt_cta_dispatch_atlas", frame_id, manifest), "CTA atlas frame should exist: %s" % frame_id)
	for frame_id in ["default", "hover", "pressed", "disabled", "focus", "confirming"]:
		_assert(RegionTaskManifest.has_frame("rt_advance_day_atlas", frame_id, manifest), "advance day atlas frame should exist: %s" % frame_id)

	_assert(not RegionTaskManifest.text_safe_rects("rt_task_card_atlas").is_empty(), "task card atlas should declare text safe rects")
	_assert(not RegionTaskManifest.forbidden_rects("rt_task_card_atlas").is_empty(), "task card atlas should declare no-text rects")
	_assert(not RegionTaskManifest.hit_rect("rt_task_card_atlas").size.is_zero_approx(), "task card atlas should declare hit rect")
	_assert(not RegionTaskManifest.hover_rect("rt_task_card_atlas").size.is_zero_approx(), "task card atlas should declare hover rect")
	_assert(not RegionTaskManifest.hit_rect("rt_cta_dispatch_atlas").size.is_zero_approx(), "CTA atlas should declare hit rect")
	_assert(not RegionTaskManifest.hover_rect("rt_cta_dispatch_atlas").size.is_zero_approx(), "CTA atlas should declare hover rect")
	_assert(not RegionTaskManifest.text_safe_rects("rt_advance_day_atlas").is_empty(), "advance day atlas should declare text safe rects")
	_assert(not RegionTaskManifest.forbidden_rects("rt_advance_day_atlas").is_empty(), "advance day atlas should declare no-text rects")
	_assert(not RegionTaskManifest.hit_rect("rt_advance_day_atlas").size.is_zero_approx(), "advance day atlas should declare hit rect")
	_assert(not RegionTaskManifest.hover_rect("rt_advance_day_atlas").size.is_zero_approx(), "advance day atlas should declare hover rect")
	var advance_asset := RegionTaskManifest.get_asset("rt_advance_day_atlas", manifest)
	_assert(str(advance_asset.get("action_scope", "")) == "global_region_day_advance", "advance day should be scoped as a global day advance action")
	var separation_policy: Dictionary = advance_asset.get("separation_policy", {})
	_assert(_contains(separation_policy.get("must_not_share_visual_group_with", []), "rt_cta_dispatch_atlas"), "advance day should not share the task CTA visual group")
	_assert(int(separation_policy.get("minimum_screen_gap_from_task_cta", 0)) >= 160, "advance day should enforce a minimum screen gap from task CTA")

	var pin_asset := RegionTaskManifest.get_asset("rt_pin_atlas", manifest)
	_assert(pin_asset.has("anchor_point"), "pin atlas should declare anchor point")
	_assert(pin_asset.has("label_anchor"), "pin atlas should declare label anchor")
	_assert(int(pin_asset.get("collision_radius", 0)) > 0, "pin atlas should declare collision radius")

	var map_asset := RegionTaskManifest.get_asset("rt_map_base_clean", manifest)
	var no_text_rects: Array = map_asset.get("no_text_rects", [])
	_assert(not no_text_rects.is_empty(), "clean map base should declare no-text/no-baked-object rules")
	var map_rules: Array = no_text_rects[0].get("rules", []) if typeof(no_text_rects[0]) == TYPE_DICTIONARY else []
	_assert(_contains(map_rules, "no baked pins"), "clean map base should forbid baked pins")
	_assert(_contains(map_rules, "no baked labels"), "clean map base should forbid baked labels")
	_assert(not map_asset.get("hotspots", []).is_empty(), "clean map base should provide runtime hotspot anchors")

	var detail_asset := RegionTaskManifest.get_asset("rt_detail_sheet_base", manifest)
	var detail_content_rects: Array = detail_asset.get("content_rects", [])
	_assert(not _has_rect_id(detail_content_rects, "cta_label"), "detail sheet should not own CTA label text")
	_assert(_has_rect_id(detail_content_rects, "blocking_reason"), "detail sheet should own CTA disabled/blocking reason")
	_assert(_has_rect_id(detail_asset.get("no_text_rects", []), "cta_mount"), "detail sheet should declare CTA mount as no-text slot")
	_assert(str(detail_asset.get("cta_policy", "")).contains("rt_cta_dispatch_atlas"), "detail sheet should point CTA ownership to CTA atlas")

	var qa_cases: Array = manifest.get("qa_cases", [])
	_assert(not qa_cases.is_empty(), "manifest should declare QA cases")
	_assert(_has_case_id(qa_cases, "long_title"), "manifest should cover long title QA")
	_assert(_has_case_id(qa_cases, "disabled_cta"), "manifest should cover disabled CTA QA")
	_assert(_has_case_id(qa_cases, "hover_and_pressed"), "manifest should cover hover and pressed QA")
	_assert(_has_case_id(qa_cases, "advance_day_misclick_guard"), "manifest should cover advance day misclick guard QA")

	print("test_region_task_asset_manifest.gd OK")
	quit(0)

func _has_asset(asset_id: String, manifest: Dictionary) -> bool:
	var asset := RegionTaskManifest.get_asset(asset_id, manifest)
	return not asset.is_empty()

func _contains(values: Array, needle: String) -> bool:
	for value in values:
		if str(value) == needle:
			return true
	return false

func _has_rect_id(values: Array, rect_id: String) -> bool:
	for value in values:
		if typeof(value) == TYPE_DICTIONARY and str(value.get("id", "")) == rect_id:
			return true
	return false

func _has_case_id(values: Array, case_id: String) -> bool:
	for value in values:
		if typeof(value) == TYPE_DICTIONARY and str(value.get("id", "")) == case_id:
			return true
	return false

func _assert(condition: bool, message: String) -> void:
	if condition:
		print("PASS: %s" % message)
		return
	push_error("FAIL: %s" % message)
	quit(1)
