extends Control
class_name WeeklyRunWorldMapStructureLayer

@export_enum("base", "routes", "selected") var layer_mode := "base"

const SEA := Color("0b2227")
const FACETS := [
	Color("14383c"), Color("184247"), Color("1b4a4d"), Color("205156"),
	Color("173f43"), Color("23575a"), Color("1c484b"), Color("285e5d"),
]

var _regions: Array = []
var _selected_region_id := ""


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_meta("artifact_type", "structure_only")
	set_meta("production_asset", false)
	queue_redraw()


func render(regions: Array, selected_region_id: String) -> void:
	_regions = regions.duplicate(true)
	_selected_region_id = selected_region_id
	queue_redraw()


func _draw() -> void:
	match layer_mode:
		"routes":
			_draw_routes()
		"selected":
			_draw_selected()
		_:
			_draw_base()


func _draw_base() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), SEA)
	var sx := size.x / 616.0
	var sy := size.y / 464.0
	var polygons := [
		PackedVector2Array([Vector2(42, 132), Vector2(93, 76), Vector2(172, 67), Vector2(206, 118), Vector2(164, 170), Vector2(78, 175)]),
		PackedVector2Array([Vector2(75, 175), Vector2(166, 171), Vector2(198, 226), Vector2(153, 312), Vector2(96, 273)]),
		PackedVector2Array([Vector2(232, 95), Vector2(308, 58), Vector2(391, 84), Vector2(409, 134), Vector2(346, 160), Vector2(274, 146)]),
		PackedVector2Array([Vector2(272, 146), Vector2(348, 159), Vector2(382, 231), Vector2(319, 277), Vector2(250, 226)]),
		PackedVector2Array([Vector2(410, 135), Vector2(487, 101), Vector2(566, 128), Vector2(555, 195), Vector2(479, 211), Vector2(382, 180)]),
		PackedVector2Array([Vector2(384, 231), Vector2(476, 211), Vector2(534, 270), Vector2(478, 316), Vector2(400, 290)]),
		PackedVector2Array([Vector2(452, 333), Vector2(510, 315), Vector2(562, 349), Vector2(538, 391), Vector2(475, 388)]),
		PackedVector2Array([Vector2(179, 324), Vector2(232, 296), Vector2(278, 326), Vector2(247, 376), Vector2(190, 371)]),
	]
	for index in range(polygons.size()):
		var scaled := PackedVector2Array()
		for point in polygons[index]:
			scaled.append(Vector2(point.x * sx, point.y * sy))
		draw_colored_polygon(scaled, FACETS[index % FACETS.size()])
		for edge_index in range(scaled.size()):
			draw_line(scaled[edge_index], scaled[(edge_index + 1) % scaled.size()], Color(0.47, 0.69, 0.66, 0.12), 1.0)
	for x in range(0, int(size.x), 77):
		draw_line(Vector2(float(x), 0.0), Vector2(float(x), size.y), Color(0.55, 0.76, 0.72, 0.035), 1.0)
	for y in range(0, int(size.y), 58):
		draw_line(Vector2(0.0, float(y)), Vector2(size.x, float(y)), Color(0.55, 0.76, 0.72, 0.035), 1.0)


func _draw_routes() -> void:
	if _regions.size() < 2:
		return
	var points: Array[Vector2] = []
	for region in _regions:
		points.append(_region_point(region))
	for index in range(points.size() - 1):
		draw_dashed_line(points[index], points[index + 1], Color(0.87, 0.76, 0.36, 0.56), 2.0, 8.0)
	if points.size() > 2:
		draw_dashed_line(points[points.size() - 1], points[0], Color(0.87, 0.76, 0.36, 0.34), 1.5, 8.0)


func _draw_selected() -> void:
	for region in _regions:
		if str(region.get("id", "")) != _selected_region_id:
			continue
		var point := _region_point(region)
		draw_circle(point, 21.0, Color(0.79, 0.86, 0.37, 0.12))
		draw_arc(point, 21.0, 0.0, TAU, 48, Color("c9db5f"), 2.0)
		draw_arc(point, 29.0, -0.45, 1.85, 32, Color(0.79, 0.86, 0.37, 0.48), 1.0)


func _region_point(region: Dictionary) -> Vector2:
	var map_pos: Dictionary = region.get("map_pos", {"x": 0.5, "y": 0.5})
	return Vector2(float(map_pos.get("x", 0.5)) * size.x, float(map_pos.get("y", 0.5)) * size.y)
