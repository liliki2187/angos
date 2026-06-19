extends PanelContainer
class_name WeeklyRunMetricCard

const METRIC_META := {
	"credibility": {"color": Color(0.27, 0.86, 0.88, 1.0), "symbol": "◆", "state": "核验章"},
	"weirdness": {"color": Color(0.86, 0.22, 0.20, 1.0), "symbol": "▲", "state": "传闻热"},
	"reputation": {"color": Color(0.95, 0.70, 0.28, 1.0), "symbol": "★", "state": "发行波"},
	"order": {"color": Color(0.45, 0.64, 0.96, 1.0), "symbol": "□", "state": "封条线"},
	"mania": {"color": Color(1.00, 0.20, 0.30, 1.0), "symbol": "●", "state": "低频异响"},
}

@onready var accent_rect: ColorRect = $HBox/Accent
@onready var symbol_label: Label = $HBox/Symbol
@onready var title_label: Label = $HBox/VBox/TopRow/Title
@onready var value_label: Label = $HBox/VBox/TopRow/Value
@onready var state_label: Label = $HBox/VBox/State
@onready var meter_bar: ProgressBar = $HBox/VBox/Meter

var _accent_color := Color(0.27, 0.86, 0.88, 1.0)
var _metric_value := 0.0
var _is_pressure := false
var _is_focus := false

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_apply_metric_style(_accent_color)

func bind(label: String, value: String, key: String = "", state_override: String = "", focus: bool = false) -> void:
	var meta: Dictionary = METRIC_META.get(key, {
		"color": Color(0.75, 0.78, 0.70, 1.0),
		"symbol": "◆",
		"state": "观测中",
	})
	_accent_color = meta.get("color", Color(0.75, 0.78, 0.70, 1.0))
	_metric_value = clampf(value.to_float(), 0.0, 100.0)
	_is_focus = focus
	_is_pressure = key in ["weirdness", "mania"] and _metric_value >= 50.0
	title_label.text = label
	value_label.text = "%02d" % int(round(_metric_value))
	state_label.text = state_override if state_override != "" else _state_text(str(meta.get("state", "观测中")), _metric_value, _is_pressure)
	symbol_label.text = str(meta.get("symbol", "◆"))
	accent_rect.color = _accent_color
	symbol_label.add_theme_color_override("font_color", _accent_color)
	value_label.add_theme_color_override("font_color", Color(0.98, 0.93, 0.74, 1.0))
	state_label.add_theme_color_override("font_color", _state_color())
	meter_bar.value = _metric_value
	_apply_metric_style(_accent_color)
	queue_redraw()

func _state_text(base_text: String, metric_value: float, pressure: bool) -> String:
	if pressure:
		return "%s / 升温" % base_text
	if metric_value >= 65.0:
		return "%s / 强" % base_text
	if metric_value <= 25.0:
		return "%s / 弱" % base_text
	return "%s / 稳" % base_text

func _apply_metric_style(color: Color) -> void:
	var panel_style := StyleBoxFlat.new()
	panel_style.bg_color = Color(0.038, 0.047, 0.050, 0.96)
	panel_style.border_color = Color(0.70, 0.62, 0.42, 0.58)
	if _is_pressure:
		panel_style.border_color = color
	if _is_focus:
		panel_style.border_color = Color(0.96, 0.76, 0.32, 1.0)
	panel_style.set_border_width_all(1)
	panel_style.corner_radius_top_left = 3
	panel_style.corner_radius_top_right = 3
	panel_style.corner_radius_bottom_left = 3
	panel_style.corner_radius_bottom_right = 3
	panel_style.content_margin_left = 6
	panel_style.content_margin_top = 4
	panel_style.content_margin_right = 6
	panel_style.content_margin_bottom = 4
	add_theme_stylebox_override("panel", panel_style)

	var meter_bg := StyleBoxFlat.new()
	meter_bg.bg_color = Color(0.015, 0.018, 0.020, 1.0)
	meter_bg.corner_radius_top_left = 1
	meter_bg.corner_radius_top_right = 1
	meter_bg.corner_radius_bottom_left = 1
	meter_bg.corner_radius_bottom_right = 1
	meter_bar.add_theme_stylebox_override("background", meter_bg)

	var meter_fill := StyleBoxFlat.new()
	meter_fill.bg_color = color
	meter_fill.corner_radius_top_left = 1
	meter_fill.corner_radius_top_right = 1
	meter_fill.corner_radius_bottom_left = 1
	meter_fill.corner_radius_bottom_right = 1
	meter_bar.add_theme_stylebox_override("fill", meter_fill)

func _draw() -> void:
	var ink := Color(_accent_color.r, _accent_color.g, _accent_color.b, 0.26)
	var hot_ink := Color(_accent_color.r, _accent_color.g, _accent_color.b, 0.52)
	draw_line(Vector2(8.0, size.y - 5.0), Vector2(size.x - 8.0, size.y - 5.0), ink, 1.0)
	draw_line(Vector2(size.x - 30.0, 5.0), Vector2(size.x - 9.0, 5.0), ink, 1.0)
	draw_circle(Vector2(size.x - 13.0, 11.0), 2.4, hot_ink if _is_pressure else ink)
	if _is_pressure or _is_focus:
		draw_line(Vector2(size.x - 20.0, 15.0), Vector2(size.x - 8.0, 23.0), hot_ink, 1.0)
		draw_line(Vector2(size.x - 18.0, 24.0), Vector2(size.x - 9.0, 30.0), hot_ink, 1.0)

func _state_color() -> Color:
	if _is_focus:
		return Color(1.0, 0.76, 0.36, 1.0)
	if _is_pressure:
		return Color(1.0, 0.58, 0.48, 1.0)
	return Color(0.76, 0.73, 0.58, 1.0)
