extends Control

const BG := Color("061923")
const GRID := Color(0.36, 0.52, 0.56, 0.09)
const COAST := Color(0.56, 0.69, 0.67, 0.34)
const MAP_RECT := Rect2(432, 154, 960, 902)
const MAP_TEXTURE := preload("res://Assets/prototypes/world_map_integrated/a_style_v2_runtime/world_map_board_960x902.png")


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	queue_redraw()


func get_asset_contract() -> Dictionary:
	return {
		"resource_path": MAP_TEXTURE.resource_path,
		"source_size": [int(MAP_TEXTURE.get_width()), int(MAP_TEXTURE.get_height())],
		"display_rect": [int(MAP_RECT.position.x), int(MAP_RECT.position.y), int(MAP_RECT.size.x), int(MAP_RECT.size.y)],
		"runtime_overlay_owns_beacons": true,
	}


func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), BG, true)
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(size.x, 0), Vector2(size.x, 172), Vector2(0, 326)]), [Color("0b2530")])
	draw_rect(Rect2(MAP_RECT.position + Vector2(10, 12), MAP_RECT.size), Color(0.0, 0.02, 0.03, 0.42), true)
	draw_texture_rect(MAP_TEXTURE, MAP_RECT, false)
	draw_polyline(PackedVector2Array([
		Vector2(724, 356), Vector2(918, 356), Vector2(940, 338), Vector2(1392, 338), Vector2(1416, 350),
	]), Color(0.25, 0.50, 0.65, 0.58), 2.0, false)


func _draw_grid() -> void:
	for x in range(int(MAP_RECT.position.x), int(MAP_RECT.end.x) + 1, 80):
		draw_line(Vector2(x, MAP_RECT.position.y), Vector2(x, MAP_RECT.end.y), GRID, 1.0)
	for y in range(int(MAP_RECT.position.y), int(MAP_RECT.end.y) + 1, 78):
		draw_line(Vector2(MAP_RECT.position.x, y), Vector2(MAP_RECT.end.x, y), GRID, 1.0)
	draw_line(Vector2(MAP_RECT.position.x, MAP_RECT.end.y), Vector2(MAP_RECT.end.x, MAP_RECT.end.y), Color(0.72, 0.77, 0.68, 0.12), 1.0)


func _draw_world() -> void:
	var north := PackedVector2Array([
		Vector2(458, 250), Vector2(558, 190), Vector2(742, 206), Vector2(874, 298),
		Vector2(842, 430), Vector2(714, 494), Vector2(568, 454), Vector2(486, 356),
	])
	_draw_land(north, [Color("2a6470"), Color("3b7580"), Color("426a71"), Color("214b5b")])

	var south := PackedVector2Array([
		Vector2(704, 494), Vector2(820, 548), Vector2(818, 704), Vector2(752, 900), Vector2(668, 650),
	])
	_draw_land(south, [Color("285360"), Color("35646a"), Color("53685a")])

	var eurasia := PackedVector2Array([
		Vector2(830, 238), Vector2(932, 178), Vector2(1112, 188), Vector2(1236, 228),
		Vector2(1362, 336), Vector2(1320, 452), Vector2(1166, 494), Vector2(1014, 464), Vector2(892, 382),
	])
	_draw_land(eurasia, [Color("2d5966"), Color("3c6e72"), Color("65705a"), Color("234958")])

	var africa := PackedVector2Array([
		Vector2(930, 464), Vector2(1054, 480), Vector2(1110, 602), Vector2(1048, 842),
		Vector2(948, 776), Vector2(896, 568),
	])
	_draw_land(africa, [Color("8c7c4d"), Color("756f50"), Color("596853")])

	var australia := PackedVector2Array([
		Vector2(1132, 724), Vector2(1264, 704), Vector2(1364, 786), Vector2(1322, 914), Vector2(1176, 930),
	])
	_draw_land(australia, [Color("315663"), Color("456b6d"), Color("746d4d")])

	var evidence := Color(0.72, 0.78, 0.68, 0.20)
	draw_dashed_line(Vector2(690, 352), Vector2(1188, 372), evidence, 2.0, 9.0)
	draw_dashed_line(Vector2(1188, 372), Vector2(1270, 710), evidence, 2.0, 9.0)
	draw_circle(Vector2(950, 362), 4.0, Color("9a4a36"))

	var antarctica := PackedVector2Array([
		Vector2(486, 1006), Vector2(566, 986), Vector2(646, 996), Vector2(726, 981),
		Vector2(814, 993), Vector2(900, 985), Vector2(982, 999), Vector2(1060, 987),
		Vector2(1140, 998), Vector2(1228, 989), Vector2(1290, 1003), Vector2(1348, 1024),
		Vector2(1274, 1036), Vector2(1176, 1029), Vector2(1090, 1039), Vector2(1008, 1030),
		Vector2(920, 1041), Vector2(834, 1033), Vector2(748, 1044), Vector2(660, 1031),
		Vector2(570, 1040), Vector2(510, 1025),
	])
	_draw_land(antarctica, [Color("193742"), Color("24464a"), Color("324a43")])


func _draw_land(points: PackedVector2Array, colors: Array[Color]) -> void:
	var center := Vector2.ZERO
	for point in points:
		center += point
	center /= float(points.size())
	for index in range(points.size()):
		var next_index := (index + 1) % points.size()
		draw_polygon(PackedVector2Array([center, points[index], points[next_index]]), [colors[index % colors.size()]])
	draw_polyline(points, COAST, 2.0, true)
