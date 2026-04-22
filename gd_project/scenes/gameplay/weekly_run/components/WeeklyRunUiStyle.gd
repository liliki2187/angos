extends RefCounted
class_name WeeklyRunUiStyle

static func apply_panel_style(panel: Control, bg: Color = Color(0.08, 0.11, 0.16, 0.97), border: Color = Color(0.20, 0.25, 0.31, 1.0), radius: int = 14) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	style.content_margin_left = 12
	style.content_margin_top = 12
	style.content_margin_right = 12
	style.content_margin_bottom = 12
	panel.add_theme_stylebox_override("panel", style)

static func apply_button_style(button: Button, emphasis: bool, enabled: bool = true) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.09, 0.12, 0.18, 1.0)
	normal.border_color = Color(0.28, 0.34, 0.42, 1.0)
	if emphasis:
		normal.bg_color = Color(0.22, 0.18, 0.08, 1.0)
		normal.border_color = Color(0.80, 0.64, 0.33, 1.0)
	normal.set_border_width_all(1)
	normal.corner_radius_top_left = 10
	normal.corner_radius_top_right = 10
	normal.corner_radius_bottom_left = 10
	normal.corner_radius_bottom_right = 10
	normal.content_margin_left = 10
	normal.content_margin_right = 10
	normal.content_margin_top = 8
	normal.content_margin_bottom = 8
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", normal.duplicate())
	button.add_theme_stylebox_override("pressed", normal.duplicate())
	button.add_theme_stylebox_override("disabled", normal.duplicate())
	var font_color := Color(0.95, 0.96, 0.98, 1.0)
	if emphasis:
		font_color = Color(0.95, 0.88, 0.72, 1.0)
	button.add_theme_color_override("font_color", font_color)
	button.add_theme_color_override("font_hover_color", font_color)
	button.add_theme_color_override("font_pressed_color", font_color)
	button.add_theme_color_override("font_disabled_color", Color(0.57, 0.61, 0.67, 1.0))
	button.disabled = not enabled
