extends Control
class_name WeeklyRunShellBackdrop

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED:
		queue_redraw()

func _draw() -> void:
	var line_color := Color(0.12, 0.36, 0.38, 0.11)
	var scan_color := Color(0.70, 0.15, 0.11, 0.06)
	for y in range(0, int(size.y), 18):
		draw_line(Vector2(0, y), Vector2(size.x, y), line_color, 1.0)
	for x in range(0, int(size.x), 64):
		draw_line(Vector2(x, 0), Vector2(x, size.y), Color(0.10, 0.24, 0.26, 0.08), 1.0)
	var seam_x := size.x * 0.515
	draw_line(Vector2(seam_x, 0), Vector2(seam_x, size.y), scan_color, 2.0)
	draw_rect(Rect2(Vector2.ZERO, Vector2(size.x, 96)), Color(0.02, 0.04, 0.05, 0.20))
