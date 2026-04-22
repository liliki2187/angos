extends RefCounted
class_name WeeklyMaterialInventory

var _materials_by_id := {}
var _material_ids: Array[String] = []

func clear() -> void:
	_materials_by_id.clear()
	_material_ids.clear()

func ingest_material(material: Dictionary) -> void:
	var material_id := str(material.get("id", ""))
	if material_id == "":
		return
	_materials_by_id[material_id] = material.duplicate(true)
	if not _material_ids.has(material_id):
		_material_ids.append(material_id)

func get_material(material_id: String) -> Dictionary:
	if not _materials_by_id.has(material_id):
		return {}
	return (_materials_by_id[material_id] as Dictionary).duplicate(true)

func get_materials_by_ids(material_ids: Array[String]) -> Array[Dictionary]:
	var expected_ids := {}
	for material_id in material_ids:
		expected_ids[str(material_id)] = true

	var materials: Array[Dictionary] = []
	for stored_id in _material_ids:
		if bool(expected_ids.get(stored_id, false)):
			materials.append(get_material(stored_id))
	return materials

func get_all_materials() -> Array[Dictionary]:
	return get_materials_by_ids(_material_ids)
