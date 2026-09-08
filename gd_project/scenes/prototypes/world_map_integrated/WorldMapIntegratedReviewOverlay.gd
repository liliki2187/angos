extends Control

var _font: Font


func configure(font: Font) -> void:
	_font = font
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_build_labels()


func _draw() -> void:
	var hit := Color(0.30, 0.86, 0.88, 0.82)
	var primary := Color(0.96, 0.60, 0.20, 0.92)
	var no_hit := Color(0.72, 0.76, 0.42, 0.78)
	draw_rect(Rect2(432, 154, 960, 902), Color(0.28, 0.63, 0.72, 0.52), false, 2.0)
	for rect in [
		Rect2(52, 226, 340, 170), Rect2(52, 408, 340, 170), Rect2(52, 590, 340, 170),
		Rect2(662, 318, 212, 76), Rect2(1000, 336, 216, 76), Rect2(1054, 666, 244, 84),
		Rect2(1443, 596, 414, 56),
	]:
		draw_rect(rect, hit, false, 2.0)
	draw_rect(Rect2(1443, 956, 414, 76), primary, false, 3.0)
	draw_rect(Rect2(52, 882, 340, 94), no_hit, false, 2.0)
	for x in [36.0, 408.0, 432.0, 1392.0, 1416.0, 1884.0]:
		draw_line(Vector2(x, 0), Vector2(x, 1080), Color(0.55, 0.78, 0.82, 0.11), 1.0)


func _build_labels() -> void:
	_add_label("CARD HIT 340×170", Rect2(58, 250, 220, 24), Color("54dde0"))
	_add_label("MAP SAFE 960×902", Rect2(440, 158, 250, 24), Color("54a9c8"))
	_add_label("BEACON HIT", Rect2(662, 292, 180, 24), Color("54dde0"))
	_add_label("DISCLOSURE HIT 414×56", Rect2(1447, 568, 300, 24), Color("54dde0"))
	_add_label("PRIMARY HIT 414×76", Rect2(1508, 928, 300, 24), Color("ff9a36"))
	_add_label("DISABLED · NO ACTION", Rect2(58, 850, 270, 24), Color("b9c66c"))


func _add_label(text_value: String, rect: Rect2, color: Color) -> void:
	var label := Label.new()
	label.text = text_value
	label.position = rect.position
	label.size = rect.size
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("font", _font)
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", color)
	add_child(label)
