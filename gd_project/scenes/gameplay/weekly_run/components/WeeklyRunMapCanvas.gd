extends Control
class_name WeeklyRunMapCanvas

var mode := "world"
var selected_id := ""

func configure(next_mode: String, next_selected_id: String = "") -> void:
	mode = next_mode
	selected_id = next_selected_id
	queue_redraw()

func _draw() -> void:
	var rect := Rect2(Vector2.ZERO, size)
	if mode == "region":
		_draw_grid(rect)
		_draw_region_map(rect)
		_draw_halftone(rect)
	else:
		_draw_world_selection(rect)

func _draw_grid(rect: Rect2) -> void:
	draw_rect(rect, Color(0.035, 0.055, 0.070, 1.0), true)
	var grid_color := Color(0.12, 0.20, 0.22, 0.34)
	for x in range(0, int(rect.size.x), 34):
		draw_line(Vector2(x, 0), Vector2(x, rect.size.y), grid_color, 1.0)
	for y in range(0, int(rect.size.y), 34):
		draw_line(Vector2(0, y), Vector2(rect.size.x, y), grid_color, 1.0)
	draw_rect(rect.grow(-2.0), Color(0.20, 0.74, 0.78, 0.28), false, 2.0)

func _draw_world_map(rect: Rect2) -> void:
	var land := Color(0.14, 0.19, 0.20, 0.92)
	var land_dim := Color(0.09, 0.12, 0.13, 0.86)
	var north_america := PackedVector2Array([
		_point(rect, 0.17, 0.24), _point(rect, 0.31, 0.20), _point(rect, 0.42, 0.31),
		_point(rect, 0.39, 0.48), _point(rect, 0.28, 0.58), _point(rect, 0.18, 0.48)
	])
	var south_america := PackedVector2Array([
		_point(rect, 0.35, 0.58), _point(rect, 0.43, 0.66), _point(rect, 0.39, 0.86),
		_point(rect, 0.30, 0.78)
	])
	var eurasia := PackedVector2Array([
		_point(rect, 0.52, 0.27), _point(rect, 0.78, 0.22), _point(rect, 0.90, 0.39),
		_point(rect, 0.79, 0.52), _point(rect, 0.59, 0.48)
	])
	var africa := PackedVector2Array([
		_point(rect, 0.55, 0.48), _point(rect, 0.68, 0.50), _point(rect, 0.67, 0.74),
		_point(rect, 0.56, 0.72), _point(rect, 0.50, 0.59)
	])
	var australia := PackedVector2Array([
		_point(rect, 0.76, 0.70), _point(rect, 0.88, 0.72), _point(rect, 0.86, 0.82),
		_point(rect, 0.75, 0.82)
	])
	draw_polygon(north_america, [Color(0.12, 0.34, 0.36, 0.98)])
	draw_polyline(north_america, Color(0.22, 0.84, 0.88, 0.52), 3.0, true)
	for shape in [south_america, eurasia, africa, australia]:
		draw_polygon(shape, [land_dim])
		draw_polyline(shape, Color(0.24, 0.29, 0.31, 0.84), 2.0, true)
	_draw_fax_edges(rect)

func _draw_world_channel_overlay(rect: Rect2) -> void:
	draw_rect(rect, Color(0.92, 0.88, 0.74, 0.055), true)
	_draw_world_modern_overprint(rect)
	_draw_world_selection(rect)

func _draw_world_modern_overprint(rect: Rect2) -> void:
	var cyan := Color(0.02, 0.54, 0.62, 0.08)
	var cyan_line := Color(0.02, 0.48, 0.54, 0.13)
	var red := Color(0.78, 0.12, 0.08, 0.08)
	var red_line := Color(0.70, 0.10, 0.08, 0.13)

	var left_shard := PackedVector2Array([
		_point(rect, 0.075, 0.20), _point(rect, 0.205, 0.13),
		_point(rect, 0.150, 0.28), _point(rect, 0.070, 0.34),
	])
	var right_shard := PackedVector2Array([
		_point(rect, 0.835, 0.14), _point(rect, 0.955, 0.18),
		_point(rect, 0.925, 0.26), _point(rect, 0.805, 0.23),
	])
	var lower_red := PackedVector2Array([
		_point(rect, 0.735, 0.78), _point(rect, 0.970, 0.69),
		_point(rect, 0.935, 0.81), _point(rect, 0.760, 0.88),
	])
	draw_polygon(left_shard, [cyan])
	draw_polygon(right_shard, [cyan])
	draw_polygon(lower_red, [red])

	_draw_registration_mark(rect, Vector2(0.165, 0.755), red_line)
	_draw_registration_mark(rect, Vector2(0.830, 0.225), cyan_line)
	_draw_registration_mark(rect, Vector2(0.690, 0.825), red_line)

	for index in range(4):
		var y := 0.22 + float(index) * 0.16
		draw_line(_point(rect, 0.085, y), _point(rect, 0.185, y + 0.018), Color(0.03, 0.40, 0.44, 0.07), 1.0)
		draw_line(_point(rect, 0.790, y + 0.045), _point(rect, 0.925, y + 0.030), Color(0.55, 0.08, 0.06, 0.06), 1.0)

func _draw_registration_mark(rect: Rect2, normalized_pos: Vector2, color: Color) -> void:
	var center := _point(rect, normalized_pos.x, normalized_pos.y)
	draw_line(center + Vector2(-18, 0), center + Vector2(18, 0), color, 1.0)
	draw_line(center + Vector2(0, -18), center + Vector2(0, 18), color, 1.0)
	draw_arc(center, 10.0, 0.0, TAU, 36, color, 1.0)

func _draw_world_selection(rect: Rect2) -> void:
	if selected_id == "":
		return
	var points := {
		"us": Vector2(0.24, 0.39),
		"east_asia": Vector2(0.74, 0.44),
		"pacific": Vector2(0.56, 0.60),
	}
	if not points.has(selected_id):
		return
	var center: Vector2 = _point(rect, points[selected_id].x, points[selected_id].y)
	draw_circle(center, 7.0, Color(0.92, 0.18, 0.12, 0.62))
	draw_circle(center, 3.0, Color(0.98, 0.86, 0.55, 0.70))

func _draw_region_map(rect: Rect2) -> void:
	var land := PackedVector2Array([
		_point(rect, 0.18, 0.24), _point(rect, 0.48, 0.19), _point(rect, 0.76, 0.28),
		_point(rect, 0.83, 0.56), _point(rect, 0.63, 0.76), _point(rect, 0.31, 0.72),
		_point(rect, 0.16, 0.50)
	])
	draw_polygon(land, [Color(0.12, 0.24, 0.25, 0.94)])
	draw_polyline(land, Color(0.25, 0.82, 0.86, 0.52), 3.0, true)
	for i in range(5):
		var y := rect.size.y * (0.25 + i * 0.13)
		draw_line(Vector2(rect.size.x * 0.20, y), Vector2(rect.size.x * 0.80, y + sin(float(i)) * 18.0), Color(0.20, 0.37, 0.38, 0.40), 2.0)
	draw_line(_point(rect, 0.28, 0.54), _point(rect, 0.44, 0.42), Color(0.93, 0.20, 0.16, 0.64), 3.0)
	draw_line(_point(rect, 0.44, 0.42), _point(rect, 0.66, 0.32), Color(0.93, 0.20, 0.16, 0.52), 3.0)
	draw_line(_point(rect, 0.44, 0.42), _point(rect, 0.58, 0.66), Color(0.93, 0.20, 0.16, 0.45), 2.0)
	_draw_fax_edges(rect)

func _draw_fax_edges(rect: Rect2) -> void:
	var paper := Color(0.86, 0.78, 0.58, 0.13)
	draw_rect(Rect2(Vector2(rect.size.x * 0.06, rect.size.y * 0.08), Vector2(rect.size.x * 0.18, 18)), paper, true)
	draw_rect(Rect2(Vector2(rect.size.x * 0.70, rect.size.y * 0.12), Vector2(rect.size.x * 0.20, 18)), paper, true)
	draw_rect(Rect2(Vector2(rect.size.x * 0.08, rect.size.y * 0.82), Vector2(rect.size.x * 0.26, 18)), paper, true)

func _draw_halftone(rect: Rect2) -> void:
	var dot_color := Color(0.0, 0.0, 0.0, 0.18)
	for y in range(8, int(rect.size.y), 20):
		for x in range(8, int(rect.size.x), 20):
			var edge: float = float(x) / maxf(1.0, rect.size.x)
			var r: float = 1.1 + edge * 1.4
			draw_circle(Vector2(x, y), r, dot_color)

func _point(rect: Rect2, x: float, y: float) -> Vector2:
	return Vector2(rect.size.x * x, rect.size.y * y)
