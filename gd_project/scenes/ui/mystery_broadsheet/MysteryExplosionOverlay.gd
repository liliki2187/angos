extends Control

@export var progress: float = 0.0:
	set(value):
		progress = clampf(value, 0.0, 1.0)
		queue_redraw()


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _draw() -> void:
	if progress <= 0.0:
		return

	var center := size * 0.5
	var max_radius := minf(size.x, size.y) * 0.44
	var burst := max_radius * minf(progress / 0.78, 1.0)
	var flash := maxf(0.0, 1.0 - progress * 2.8)
	var ember_alpha := maxf(0.0, 1.0 - progress * 1.15)

	draw_circle(center, burst * 0.3 + 28.0, Color(1.0, 0.95, 0.88, 0.44 * flash))
	draw_circle(center, burst * 0.18 + 12.0, Color(1.0, 0.72, 0.24, 0.76 * flash))

	for index in range(18):
		var angle := (TAU / 18.0) * index + progress * 2.3
		var inner := center + Vector2.RIGHT.rotated(angle) * burst * 0.16
		var outer := center + Vector2.RIGHT.rotated(angle) * (burst + 46.0 + 12.0 * sin(progress * 10.0 + float(index)))
		var width := 2.0 + 7.0 * (1.0 - progress)
		draw_line(inner, outer, Color(1.0, 0.78, 0.24, 0.72 * ember_alpha), width, true)

	for index in range(11):
		var orbit := center + Vector2.RIGHT.rotated(progress * 5.6 + index * 0.58) * (burst * 0.56 + 18.0 * index)
		var radius := 5.0 + 10.0 * (1.0 - progress) * (1.0 - float(index) / 11.0)
		draw_circle(orbit, radius, Color(0.82, 0.23, 0.16, 0.54 * ember_alpha))

	var ring_alpha := maxf(0.0, 1.0 - progress * 1.65)
	draw_arc(center, burst + 18.0, 0.0, TAU, 72, Color(1.0, 0.88, 0.68, 0.42 * ring_alpha), 4.0, true)
