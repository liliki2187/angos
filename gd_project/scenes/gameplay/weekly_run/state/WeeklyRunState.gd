extends RefCounted
class_name WeeklyRunState

const WEEK_DAYS := 7
const INITIAL_SUBSCRIBERS := 1200
const INITIAL_EDITORIAL_PROFILE := 0.0
const INITIAL_MACRO_STATS := {
	"credibility": 42,
	"weirdness": 38,
	"reputation": 45,
	"order": 48,
	"mania": 22,
}

var week := 1
var remaining_days := WEEK_DAYS
var current_phase := "briefing"
var briefing_event_id := ""
var active_tasks: Array[Dictionary] = []
var opportunity_ids: Array[String] = []
var dispatch_results: Array[Dictionary] = []
var material_inventory: Array[Dictionary] = []
var new_material_ids: Array[String] = []
var cognition_entries: Array[Dictionary] = []
var article_candidates: Array[Dictionary] = []
var slot_assignment := {}
var published_issue: Dictionary = {}
var settlement_preview: Dictionary = {}
var settlement_result: Dictionary = {}
var next_week_hooks: Dictionary = {}
var macro_stats := INITIAL_MACRO_STATS.duplicate(true)
var subscribers := INITIAL_SUBSCRIBERS
var editorial_profile := INITIAL_EDITORIAL_PROFILE
var flags := {}
var resolved_nodes := {}
var log_entries: Array[String] = []
var last_dispatch_roll: Dictionary = {}
var next_material_serial := 1
var next_article_id := 1

func reset_for_new_run(briefing_event_id_input: String, active_tasks_input: Array[Dictionary], opportunity_ids_input: Array[String]) -> void:
	week = 1
	subscribers = INITIAL_SUBSCRIBERS
	editorial_profile = INITIAL_EDITORIAL_PROFILE
	macro_stats = INITIAL_MACRO_STATS.duplicate(true)
	flags.clear()
	resolved_nodes.clear()
	log_entries.clear()
	material_inventory.clear()
	next_week_hooks.clear()
	next_material_serial = 1
	_reset_week_state(briefing_event_id_input, active_tasks_input, opportunity_ids_input)

func begin_next_week(briefing_event_id_input: String, active_tasks_input: Array[Dictionary], opportunity_ids_input: Array[String]) -> void:
	week += 1
	_reset_week_state(briefing_event_id_input, active_tasks_input, opportunity_ids_input)

func append_log(text: String) -> void:
	log_entries.append(text)
	if log_entries.size() > 12:
		log_entries = log_entries.slice(log_entries.size() - 12, log_entries.size())

func sync_slot_assignment(slot_data: Array) -> void:
	for slot in slot_data:
		var slot_id := str(slot.id)
		if not slot_assignment.has(slot_id):
			slot_assignment[slot_id] = -1

func get_new_materials() -> Array[Dictionary]:
	var materials: Array[Dictionary] = []
	var expected_ids := {}
	for material_id in new_material_ids:
		expected_ids[str(material_id)] = true
	for material in material_inventory:
		if bool(expected_ids.get(str(material.id), false)):
			materials.append(material)
	return materials

func _reset_week_state(briefing_event_id_input: String, active_tasks_input: Array[Dictionary], opportunity_ids_input: Array[String]) -> void:
	remaining_days = WEEK_DAYS
	current_phase = "briefing"
	briefing_event_id = briefing_event_id_input
	active_tasks = active_tasks_input.duplicate(true)
	opportunity_ids = opportunity_ids_input.duplicate()
	dispatch_results.clear()
	new_material_ids.clear()
	cognition_entries.clear()
	article_candidates.clear()
	slot_assignment.clear()
	published_issue.clear()
	settlement_preview.clear()
	settlement_result.clear()
	resolved_nodes.clear()
	last_dispatch_roll.clear()
	next_article_id = 1
