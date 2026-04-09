extends Control
# ============================================================
# 事件检定系统场景
# 复刻《苏丹的游戏》掷骰检定机制
# ============================================================
# 三种检定类型 single/combined/split、对手对抗、双模式、
# 骰子飞入旋转动画、成功烟花/失败特效、DEBUG 实时日志
# ============================================================

# ── 常量 ──────────────────────────────────────────────────
const DIE_SIZE := 38
const DIE_GAP := 5
const ANIM_DUR := 1.0
const NEGATE_DUR := 0.1

const DIFF_P := [0.60, 0.50, 1.0 / 3.0]
const DIFF_LABEL := ["easy", "normal", "hard"]
const TYPE_LABEL := ["single", "combined", "split"]
const MODE_LABEL := ["numeric", "dice"]
const ATTR_KEYS := ["wisdom","social","combat","conceal","imagination","rationality","writing","courage","insight","perception"]
const ATTR_CN := {"wisdom":"智慧","social":"社交","combat":"战斗","conceal":"隐匿","imagination":"想象","rationality":"理性","writing":"笔力","courage":"胆识","insight":"灵视","perception":"洞察"}

# ── 配色 ──────────────────────────────────────────────────
const C := {
	bg = Color(0.08, 0.06, 0.10), bg2 = Color(0.067, 0.098, 0.133),
	bg3 = Color(0.102, 0.141, 0.188), panel = Color(0.055, 0.075, 0.11),
	gold = Color(0.831, 0.525, 0.306), gold_dim = Color(0.54, 0.33, 0.19),
	red = Color(0.75, 0.19, 0.19), green = Color(0.18, 0.55, 0.31),
	purple = Color(0.48, 0.31, 0.69), cyan = Color(0.23, 0.54, 0.62),
	neon = Color(0.22, 1.0, 0.52),
	text = Color(0.85, 0.86, 0.89), dim = Color(0.42, 0.48, 0.54),
	bright = Color(0.94, 0.95, 0.96),
	border = Color(0.165, 0.204, 0.267), hit = Color(0.18, 0.55, 0.31),
	miss = Color(0.75, 0.19, 0.19), negate = Color(0.33, 0.33, 0.33),
}

# ── 状态 ──────────────────────────────────────────────────
var _type: int = 0
var _diff: int = 1
var _mode: int = 1  # 默认骰子模式
var _busy := false

# ── UI 控件引用 ───────────────────────────────────────────
@onready var left_vbox: VBoxContainer = $LeftPanel/LeftMargin/Scroll/LeftVBox
@onready var dice_area: Control = $CenterPanel/DiceArea
@onready var type_badge: Label = $CenterPanel/TypeBadge
@onready var result_label: Label = $CenterPanel/ResultLabel
@onready var threshold_info: Label = $CenterPanel/ThresholdInfo
@onready var debug_log: RichTextLabel = $RightPanel/RightVBox/DebugLog
@onready var roll_timer: Timer = $DiceRollTimer

var _type_btns: Array = []
var _diff_btns: Array = []
var _mode_btns: Array = []
var _attr_a_opt: OptionButton
var _attr_a_spin: SpinBox
var _attr_b_opt: OptionButton
var _attr_b_spin: SpinBox
var _attr_b_box: VBoxContainer
var _k_row: HBoxContainer
var _k_split_row: HBoxContainer
var _k_spin: SpinBox
var _k_a_spin: SpinBox
var _k_b_spin: SpinBox
var _dp_spin: SpinBox
var _opp_chk: CheckButton
var _opp_spin: SpinBox
var _exec_btn: Button
var _prob_val: Label
var _prob_bars: VBoxContainer
var _dice_nodes: Array = []
var _fireworks: Node2D
var _fail_fx: Node2D

# ============================================================
# 工具
# ============================================================
static func _clampf(v: float, lo: float, hi: float) -> float:
	return maxf(lo, minf(hi, v))

static func _binom_coeff(n: int, k: int) -> int:
	if k < 0 or k > n: return 0
	if k == 0 or k == n: return 1
	var r := 1
	var mn := mini(k, n - k)
	for i in range(mn): r = r * (n - i) / (i + 1)
	return r

static func _binom_pmf(n: int, k: int, p: float) -> float:
	return _binom_coeff(n, k) * pow(p, k) * pow(1.0 - p, n - k)

static func _binom_cdf_ge(n: int, k: int, p: float) -> float:
	var s := 0.0
	for i in range(k, n + 1): s += _binom_pmf(n, i, p)
	return _clampf(s, 0.0, 1.0)

static func _roll_dice(n: int, p: float) -> Array:
	var out := []
	for i in range(n):
		out.append(randf() < p)
	return out

static func _rand_negate(total: int, count: int) -> Array:
	var idx := range(total)
	for i in range(count - 1, 0, -1):
		var j := randi() % (i + 1)
		var tmp = idx[i]; idx[i] = idx[j]; idx[j] = tmp
	return idx.slice(0, mini(count, total))

# ============================================================
# UI 辅助
# ============================================================
func _make_section(text: String) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", 11)
	l.add_theme_color_override("font_color", C.dim)
	left_vbox.add_child(l)
	return l

func _make_hbox() -> HBoxContainer:
	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 4)
	h.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_vbox.add_child(h)
	return h

func _make_btn(text: String, parent: Container) -> Button:
	var b := Button.new()
	b.text = text
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.add_theme_font_size_override("font_size", 11)
	_style_toggle(b, false)
	parent.add_child(b)
	return b

func _style_toggle(b: Button, active: bool) -> void:
	var col = C.gold if active else C.border
	var bg = Color(C.gold.r, C.gold.g, C.gold.b, 0.1) if active else Color(0,0,0,0)
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.set_border_width_all(1)
	s.border_color = col
	s.corner_radius_top_left = 3; s.corner_radius_top_right = 3
	s.corner_radius_bottom_left = 3; s.corner_radius_bottom_right = 3
	s.content_margin_left = 6; s.content_margin_right = 6
	s.content_margin_top = 3; s.content_margin_bottom = 3
	b.add_theme_stylebox_override("normal", s)
	var sh := StyleBoxFlat.new()
	sh.bg_color = bg; sh.border_color = Color(col.r, col.g, col.b, 0.6)
	sh.set_border_width_all(1)
	sh.corner_radius_top_left = 3; sh.corner_radius_top_right = 3
	sh.corner_radius_bottom_left = 3; sh.corner_radius_bottom_right = 3
	sh.content_margin_left = 6; sh.content_margin_right = 6
	sh.content_margin_top = 3; sh.content_margin_bottom = 3
	b.add_theme_stylebox_override("hover", sh)
	var tc := C.gold if active else C.dim
	b.add_theme_color_override("font_color", tc)

func _make_label(text: String, size: int = 12) -> Label:
	var l := Label.new(); l.text = text
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", C.text)
	return l

func _make_spin(min_v: float, max_v: float, step: float, val: float) -> SpinBox:
	var s := SpinBox.new()
	s.min_value = min_v; s.max_value = max_v; s.step = step; s.value = val
	s.add_theme_font_size_override("font_size", 12)
	var le := s.get_line_edit()
	le.add_theme_color_override("font_color", C.text)
	le.add_theme_font_size_override("font_size", 12)
	s.custom_minimum_size.x = 70
	return s

func _make_opt() -> OptionButton:
	var o := OptionButton.new()
	o.add_theme_font_size_override("font_size", 12)
	for i in range(ATTR_KEYS.size()):
		o.add_item(ATTR_CN[ATTR_KEYS[i]], i)
	o.custom_minimum_size.x = 80
	return o

# ============================================================
# 构建左侧面板
# ============================================================
func _build_left() -> void:
	# 事件预设
	_make_section("事件预设")
	var h0 := _make_hbox()
	var presets := [["封面临时改题", 0], ["拿下广告主", 1], ["暗访偷拍+圆谎", 2]]
	for p in presets:
		var b := _make_btn(p[0], h0)
		b.pressed.connect(_load_preset.bind(p[1]))

	# 检定类型
	_make_section("检定配置")
	var h1 := _make_hbox()
	for i in range(3):
		var b := _make_btn(TYPE_LABEL[i], h1)
		_type_btns.append(b)
		b.pressed.connect(set_type.bind(i))
		_style_toggle(b, i == 0)

	# 难度
	_make_section("难度")
	var h2 := _make_hbox()
	for i in range(3):
		var b := _make_btn("%s(%.2f)" % [DIFF_LABEL[i], DIFF_P[i]], h2)
		_diff_btns.append(b)
		b.pressed.connect(set_diff.bind(i))
		_style_toggle(b, i == 1)

	# 属性 A
	_make_section("属性 A")
	var h3 := _make_hbox()
	h3.add_child(_make_label("属性", 12)); _attr_a_opt = _make_opt(); h3.add_child(_attr_a_opt)
	h3.add_child(_make_label("值", 12)); _attr_a_spin = _make_spin(0, 30, 1, 7); h3.add_child(_attr_a_spin)

	# 属性 B
	_attr_b_box = VBoxContainer.new(); _attr_b_box.add_theme_constant_override("separation", 4)
	var _lbl_b := Label.new(); _lbl_b.text = "属性 B"
	_lbl_b.add_theme_font_size_override("font_size", 11); _lbl_b.add_theme_color_override("font_color", C.dim)
	_attr_b_box.add_child(_lbl_b)
	var h4 := HBoxContainer.new(); h4.add_theme_constant_override("separation", 4)
	h4.add_child(_make_label("属性", 12)); _attr_b_opt = _make_opt(); h4.add_child(_attr_b_opt)
	_attr_b_opt.selected = 1  # 默认社交
	h4.add_child(_make_label("值", 12)); _attr_b_spin = _make_spin(0, 30, 1, 5); h4.add_child(_attr_b_spin)
	_attr_b_box.add_child(h4)
	_attr_b_box.visible = (_type != 0)
	left_vbox.add_child(_attr_b_box)

	# 阈值
	_make_section("阈值")
	_k_row = _make_hbox()
	_k_row.add_child(_make_label("k", 12)); _k_spin = _make_spin(0, 30, 1, 3); _k_row.add_child(_k_spin)
	_k_split_row = HBoxContainer.new(); _k_split_row.add_theme_constant_override("separation", 4)
	_k_split_row.add_child(_make_label("kA", 12)); _k_a_spin = _make_spin(0, 30, 1, 3); _k_split_row.add_child(_k_a_spin)
	_k_split_row.add_child(_make_label("kB", 12)); _k_b_spin = _make_spin(0, 30, 1, 2); _k_split_row.add_child(_k_b_spin)
	left_vbox.add_child(_k_split_row)
	_k_split_row.visible = (_type == 2)

	# Δp
	_make_section("修正")
	var h5 := _make_hbox()
	h5.add_child(_make_label("Δp", 12)); _dp_spin = _make_spin(-0.5, 0.5, 0.01, 0.0); h5.add_child(_dp_spin)

	# 对抗
	_make_section("对抗")
	var h6 := _make_hbox()
	h6.add_child(_make_label("启用", 12)); _opp_chk = CheckButton.new(); _opp_chk.button_pressed = true; h6.add_child(_opp_chk)
	h6.add_child(_make_label("对手值", 12)); _opp_spin = _make_spin(0, 30, 1, 3); h6.add_child(_opp_spin)

	# 显示模式
	_make_section("显示模式")
	var h7 := _make_hbox()
	for i in range(2):
		var b := _make_btn(MODE_LABEL[i], h7)
		_mode_btns.append(b)
		b.pressed.connect(set_mode.bind(i))
		_style_toggle(b, i == 1)

	# 执行按钮
	_exec_btn = Button.new()
	_exec_btn.text = "🎲 执行检定"
	_exec_btn.add_theme_font_size_override("font_size", 14)
	var es := StyleBoxFlat.new()
	es.bg_color = C.gold; es.set_border_width_all(0)
	es.corner_radius_top_left = 4; es.corner_radius_top_right = 4
	es.corner_radius_bottom_left = 4; es.corner_radius_bottom_right = 4
	es.content_margin_top = 8; es.content_margin_bottom = 8
	_exec_btn.add_theme_stylebox_override("normal", es)
	_exec_btn.add_theme_color_override("font_color", Color.WHITE)
	left_vbox.add_child(_exec_btn)
	_exec_btn.pressed.connect(_on_execute)

	# 概率显示
	_make_section("理论成功率")
	_prob_val = Label.new(); _prob_val.text = "—"
	_prob_val.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_prob_val.add_theme_font_size_override("font_size", 28)
	_prob_val.add_theme_color_override("font_color", C.neon)
	left_vbox.add_child(_prob_val)
	_prob_bars = VBoxContainer.new(); _prob_bars.add_theme_constant_override("separation", 4)
	left_vbox.add_child(_prob_bars)

	# 值变化监听
	for sig in [_attr_a_spin.value_changed, _attr_b_spin.value_changed, _k_spin.value_changed,
				_k_a_spin.value_changed, _k_b_spin.value_changed, _dp_spin.value_changed, _opp_spin.value_changed]:
		sig.connect(_on_param_changed)
	_opp_chk.toggled.connect(func(_v): _update_prob())

# ============================================================
# Setters
# ============================================================
func set_type(v: int) -> void:
	_type = v
	for i in range(3):
		_style_toggle(_type_btns[i], i == v)
	_attr_b_box.visible = (v != 0)
	_k_row.visible = (v != 2)
	_k_split_row.visible = (v == 2)
	_update_badge(); _update_prob()

func set_diff(v: int) -> void:
	_diff = v
	for i in range(3):
		_style_toggle(_diff_btns[i], i == v)
	_update_badge(); _update_prob()

func set_mode(v: int) -> void:
	_mode = v
	for i in range(2):
		_style_toggle(_mode_btns[i], i == v)

func _update_badge() -> void:
	type_badge.text = "%s · %s" % [TYPE_LABEL[_type], DIFF_LABEL[_diff].to_upper()]

# ============================================================
# 概率计算
# ============================================================
func _get_config() -> Dictionary:
	var p_base = DIFF_P[_diff]
	var dp = _dp_spin.value
	var p = _clampf(p_base + dp, 0.0, 1.0)
	return {
		type = _type, diff = _diff, mode = _mode,
		p_base = p_base, delta_p = dp, p = p,
		attr_a = int(_attr_a_spin.value), attr_b = int(_attr_b_spin.value),
		k = int(_k_spin.value), k_a = int(_k_a_spin.value), k_b = int(_k_b_spin.value),
		has_opp = _opp_chk.button_pressed, enemy = int(_opp_spin.value),
	}

func _update_prob() -> void:
	if _busy: return
	var c := _get_config()
	for ch in _prob_bars.get_children(): ch.queue_free()

	if c.type <= 1:  # single / combined
		var n = c.attr_a if c.type == 0 else c.attr_a + c.attr_b
		var ne = max(0, n - c.enemy) if c.has_opp else n
		var kc = clamp(c.k, 0, ne)
		var prob = _binom_cdf_ge(ne, kc, c.p) if ne > 0 else 0.0
		_prob_val.text = "%.1f%%" % (prob * 100)
		_prob_val.add_theme_color_override("font_color", C.neon)
		_add_bar("成功", prob, C.green)
	else:  # split
		var eA = 0; var eB = 0
		if c.has_opp and c.enemy > 0 and (c.attr_a + c.attr_b) > 0:
			eA = floori(float(c.enemy) * c.attr_a / (c.attr_a + c.attr_b))
			eB = c.enemy - eA
		var nAe = max(0, c.attr_a - eA); var nBe = max(0, c.attr_b - eB)
		var kAc = clamp(c.k_a, 0, nAe); var kBc = clamp(c.k_b, 0, nBe)
		var pA = _binom_cdf_ge(nAe, kAc, c.p) if nAe > 0 else 0.0
		var pB = _binom_cdf_ge(nBe, kBc, c.p) if nBe > 0 else 0.0
		var pM = pA * pB; var pm = pA*(1-pB)+(1-pA)*pB; var pf = (1-pA)*(1-pB)
		_prob_val.text = "%.1f%%" % (pM * 100)
		_prob_val.add_theme_color_override("font_color", C.gold)
		_add_bar("大成功", pM, C.gold)
		_add_bar("小成功", pm, C.cyan)
		_add_bar("失败", pf, C.red)

func _on_param_changed(_v = null) -> void:
	_update_prob()

func _add_bar(label: String, pct: float, col: Color) -> void:
	var h := HBoxContainer.new(); h.add_theme_constant_override("separation", 4)
	var l := Label.new(); l.text = label; l.custom_minimum_size.x = 50
	l.add_theme_font_size_override("font_size", 10); l.add_theme_color_override("font_color", C.dim)
	h.add_child(l)
	var pb := ProgressBar.new(); pb.min_value = 0; pb.max_value = 1; pb.value = pct
	pb.custom_minimum_size.x = 60; pb.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	pb.show_percentage = false
	var s := StyleBoxFlat.new(); s.bg_color = Color(0.1, 0.1, 0.1)
	s.set_border_width_all(0); s.corner_radius_top_left = 2; s.corner_radius_top_right = 2
	s.corner_radius_bottom_left = 2; s.corner_radius_bottom_right = 2
	pb.add_theme_stylebox_override("background", s)
	var sf := StyleBoxFlat.new(); sf.bg_color = col
	sf.corner_radius_top_left = 2; sf.corner_radius_top_right = 2
	sf.corner_radius_bottom_left = 2; sf.corner_radius_bottom_right = 2
	pb.add_theme_stylebox_override("fill", sf)
	h.add_child(pb)
	var v := Label.new(); v.text = "%.1f%%" % (pct * 100); v.custom_minimum_size.x = 45
	v.add_theme_font_size_override("font_size", 10); v.add_theme_color_override("font_color", C.dim)
	h.add_child(v)
	_prob_bars.add_child(h)

# ============================================================
# 预设
# ============================================================
func _load_preset(idx: int) -> void:
	_clear_dice(); _clear_debug()
	if idx == 0:
		set_type(0); set_diff(1); _attr_a_opt.selected = 1; _attr_a_spin.value = 7
		_dp_spin.value = -0.05; _opp_chk.button_pressed = true; _opp_spin.value = 3; _k_spin.value = 4
	elif idx == 1:
		set_type(1); set_diff(2); _attr_a_opt.selected = 0; _attr_a_spin.value = 6
		_attr_b_opt.selected = 1; _attr_b_spin.value = 5
		_dp_spin.value = 0; _opp_chk.button_pressed = true; _opp_spin.value = 3; _k_spin.value = 6
	else:
		set_type(2); set_diff(1); _attr_a_opt.selected = 3; _attr_a_spin.value = 8
		_attr_b_opt.selected = 1; _attr_b_spin.value = 4
		_dp_spin.value = 0; _opp_chk.button_pressed = true; _opp_spin.value = 2
		_k_a_spin.value = 3; _k_b_spin.value = 2
	_update_prob()
	_debug("config", "加载预设: %s" % ["封面临时改题", "拿下广告主", "暗访偷拍+圆谎"][idx])

# ============================================================
# DEBUG
# ============================================================
func _debug(tag: String, msg: String) -> void:
	var tc := {config=C.cyan, calc=C.gold, roll=C.green, opponent=C.red, result=C.purple, prob=C.neon}
	var c = tc.get(tag, C.dim)
	var ts = Time.get_time_string_from_system()
	debug_log.append_text("[color=%s]%s[/color] [color=%s]%-8s[/color] %s\n" % [C.dim, ts, c, tag.to_upper(), msg])

func _clear_debug() -> void:
	debug_log.clear()

# ============================================================
# 骰子 UI
# ============================================================
func _make_die() -> PanelContainer:
	var p := PanelContainer.new()
	p.custom_minimum_size = Vector2(DIE_SIZE, DIE_SIZE)
	var s := StyleBoxFlat.new()
	s.bg_color = C.bg3; s.set_border_width_all(2); s.border_color = C.border
	s.corner_radius_top_left = 6; s.corner_radius_top_right = 6
	s.corner_radius_bottom_left = 6; s.corner_radius_bottom_right = 6
	p.add_theme_stylebox_override("panel", s)
	var l := Label.new(); l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size", 18)
	p.add_child(l)
	return p

func _set_die_state(die: PanelContainer, state: String) -> void:
	var l := die.get_child(0)
	var s := StyleBoxFlat.new()
	s.corner_radius_top_left = 6; s.corner_radius_top_right = 6
	s.corner_radius_bottom_left = 6; s.corner_radius_bottom_right = 6
	s.set_border_width_all(2); s.content_margin_left = 2; s.content_margin_right = 2
	s.content_margin_top = 2; s.content_margin_bottom = 2
	match state:
		"hit":
			s.bg_color = Color(C.hit.r, C.hit.g, C.hit.b, 0.15); s.border_color = C.hit
			l.text = "✓"; l.add_theme_color_override("font_color", C.hit)
		"miss":
			s.bg_color = Color(C.miss.r, C.miss.g, C.miss.b, 0.1); s.border_color = C.miss
			l.text = "✗"; l.add_theme_color_override("font_color", C.miss)
		"negate":
			s.bg_color = Color(C.negate.r, C.negate.g, C.negate.b, 0.15); s.border_color = C.negate
			l.text = "—"; l.add_theme_color_override("font_color", C.negate)
		"random":
			s.bg_color = C.bg3; s.border_color = C.border
			l.text = "✓" if randf() > 0.5 else "✗"
			l.add_theme_color_override("font_color", C.dim)
		_:
			s.bg_color = C.bg3; s.border_color = C.border
			l.text = "?"; l.add_theme_color_override("font_color", C.dim)
	die.add_theme_stylebox_override("panel", s)

func _calc_die_positions(count: int, area: Rect2, rows: int = 1) -> Array:
	if count <= 0: return []
	var per_row := ceili(float(count) / rows)
	var row_w := per_row * DIE_SIZE + (per_row - 1) * DIE_GAP
	var total_h := rows * DIE_SIZE + (rows - 1) * DIE_GAP
	var start_x := area.position.x + (area.size.x - row_w) / 2.0
	var start_y := area.position.y + (area.size.y - total_h) / 2.0
	var positions := []
	for i in range(count):
		var row := i / per_row
		var col := i % per_row
		var x := start_x + col * (DIE_SIZE + DIE_GAP)
		var y := start_y + row * (DIE_SIZE + DIE_GAP)
		positions.append(Vector2(x, y))
	return positions

func _random_edge_pos(viewport: Vector2) -> Vector2:
	var side := randi() % 4
	var pad := 50.0
	match side:
		0: return Vector2(randf() * viewport.x, -pad - randf() * 100)
		1: return Vector2(viewport.x + pad + randf() * 100, randf() * viewport.y)
		2: return Vector2(randf() * viewport.x, viewport.y + pad + randf() * 100)
		_: return Vector2(-pad - randf() * 100, randf() * viewport.y)

func _clear_dice() -> void:
	for d in _dice_nodes: d.queue_free()
	_dice_nodes.clear()

# ============================================================
# 特效
# ============================================================
func _make_leaf() -> Polygon2D:
	var leaf := Polygon2D.new()
	leaf.polygon = PackedVector2Array([
		Vector2(0, -8),
		Vector2(5, -2),
		Vector2(3, 7),
		Vector2(-4, 6),
		Vector2(-6, -2),
	])
	return leaf

func _make_spark(size: float) -> Polygon2D:
	var spark := Polygon2D.new()
	spark.polygon = PackedVector2Array([
		Vector2(0, -size),
		Vector2(size, 0),
		Vector2(0, size),
		Vector2(-size, 0),
	])
	return spark

func _play_fireworks(center: Vector2) -> void:
	if is_instance_valid(_fireworks):
		_fireworks.queue_free()
	var root := Node2D.new()
	add_child(root)
	root.global_position = center
	_fireworks = root

	var palette := [C.gold, C.neon, C.bright]
	for i in range(72):
		var spark := _make_spark(randf_range(2.0, 4.0))
		spark.color = palette[randi() % palette.size()]
		spark.modulate.a = randf_range(0.7, 1.0)
		root.add_child(spark)

		var dir := Vector2.RIGHT.rotated(randf() * TAU)
		var dist := randf_range(120.0, 280.0)
		var duration := randf_range(0.55, 1.1)
		var tw := create_tween().set_parallel(true)
		tw.tween_property(spark, "position", dir * dist, duration).set_trans(Tween.TRANS_QUART).set_ease(Tween.EASE_OUT)
		tw.tween_property(spark, "scale", Vector2(randf_range(0.3, 0.8), randf_range(0.3, 0.8)), duration)
		tw.tween_property(spark, "rotation", randf_range(-3.5, 3.5), duration)
		tw.tween_property(spark, "modulate:a", 0.0, duration)

	await get_tree().create_timer(1.2).timeout
	if is_instance_valid(root):
		root.queue_free()
	if _fireworks == root:
		_fireworks = null

func _play_fail_fx(_center: Vector2) -> void:
	if is_instance_valid(_fail_fx):
		_fail_fx.queue_free()
	var root := Node2D.new()
	add_child(root)
	_fail_fx = root

	var view := get_viewport_rect().size
	for i in range(28):
		var leaf := _make_leaf()
		var gray := randf_range(0.45, 0.72)
		leaf.color = Color(gray, gray, gray, randf_range(0.65, 0.95))
		leaf.global_position = Vector2(randf_range(20.0, view.x - 20.0), randf_range(-180.0, -20.0))
		leaf.scale = Vector2(randf_range(0.8, 1.25), randf_range(0.8, 1.25))
		leaf.rotation = randf_range(-1.2, 1.2)
		root.add_child(leaf)

		var target := Vector2(leaf.global_position.x + randf_range(-160.0, 160.0), view.y + randf_range(30.0, 130.0))
		var duration := randf_range(1.3, 2.3)
		var tw := create_tween().set_parallel(true)
		tw.tween_property(leaf, "global_position", target, duration).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)
		tw.tween_property(leaf, "rotation", leaf.rotation + randf_range(-3.8, 3.8), duration)
		tw.tween_property(leaf, "modulate:a", 0.0, duration * 0.5).set_delay(duration * 0.5)

	await get_tree().create_timer(2.4).timeout
	if is_instance_valid(root):
		root.queue_free()
	if _fail_fx == root:
		_fail_fx = null

# ============================================================
# 执行检定
# ============================================================
func _on_execute() -> void:
	if _busy: return
	_busy = true
	_exec_btn.disabled = true
	_clear_dice(); _clear_debug()
	var c := _get_config()
	_debug("config", "检定: %s | 难度: %s | 模式: %s" % [TYPE_LABEL[c.type], DIFF_LABEL[c.diff], MODE_LABEL[c.mode]])
	_debug("config", "p_base=%.4f Δp=%.4f → p=%.4f" % [c.p_base, c.delta_p, c.p])

	if c.type <= 1:
		await _exec_single_combined(c)
	else:
		await _exec_split(c)

	_busy = false; _exec_btn.disabled = false

func _exec_single_combined(c: Dictionary) -> void:
	var is_combined = c.type == 1
	var n = c.attr_a if not is_combined else c.attr_a + c.attr_b
	_debug("calc", "骰子 n = %s = %d" % [("attrA(%d)" % c.attr_a) if not is_combined else "attrA(%d)+attrB(%d)" % [c.attr_a, c.attr_b], n])

	var enemy = c.enemy if c.has_opp else 0
	var ne = max(0, n - enemy)
	var k = clamp(c.k, 0, ne)

	if c.has_opp:
		_debug("opponent", "enemy=%d → n_eff=max(0,%d-%d)=%d" % [enemy, n, enemy, ne])
	_debug("opponent", "k=clamp(%d, 0, %d)=%d" % [c.k, ne, k])

	if ne == 0 and k > 0:
		_debug("calc", "[color=red]⚠ n_eff=0 → 必失败[/color]")
	elif ne == 0 and k == 0:
		_debug("calc", "[color=red]⚠ n_eff=0, k=0 → 必成功[/color]")

	var prob = _binom_cdf_ge(ne, k, c.p) if ne > 0 else (0.0 if k > 0 else 1.0)
	_debug("prob", "P(X≥%d) where X~Bin(%d,%.4f) = %.2f%%" % [k, ne, c.p, prob * 100])

	# 掷骰
	var dice := _roll_dice(n, c.p)
	_debug("roll", "投出 %d 颗: [%s]" % [n, _fmt_dice(dice)])
	var hits = dice.count(true)
	_debug("roll", "原始命中: %d/%d" % [hits, n])

	# 骰子动画
	var area_rect := dice_area.get_global_rect()
	var positions := _calc_die_positions(n, area_rect)
	await _animate_dice_flyin(dice, positions, area_rect)

	# 对抗抵消
	if c.has_opp and enemy > 0 and c.mode == 1:
		var neg_count := mini(enemy, n)
		var neg_idx := _rand_negate(n, neg_count)
		_debug("opponent", "对手作废 %d 颗: [%s]" % [neg_count, ", ".join(neg_idx.map(func(x): return str(x)))])
		for idx in neg_idx:
			_set_die_state(_dice_nodes[idx], "negate")
			_debug("opponent", "die[%d] → —" % idx)
			await get_tree().create_timer(NEGATE_DUR).timeout

		var alive := range(n).filter(func(x): return not neg_idx.has(x))
		hits = alive.filter(func(x): return dice[x]).size()
		_debug("calc", "有效命中=%d/%d" % [hits, alive.size()])
	elif c.has_opp:
		var neg_idx := _rand_negate(n, mini(enemy, n))
		var alive := range(n).filter(func(x): return not neg_idx.has(x))
		hits = alive.filter(func(x): return dice[x]).size()
		_debug("opponent", "[数值模式] 作废%d 颗, 有效命中=%d" % [mini(enemy, n), hits])

	var is_pass = hits >= k
	_debug("result", "%d ≥ %d → %s" % [hits, k, "成功 ✓" if is_pass else "失败 ✗"])
	var tier := "pass" if is_pass else "fail"
	var msg := "成功！命中 %d ≥ %d" % [hits, k] if is_pass else "失败！命中 %d < %d" % [hits, k]
	_show_result(tier, msg)
	threshold_info.text = "命中 %d / 阈值 %d | 有效骰子 %d / 原始 %d" % [hits, k, ne, n]
	if is_pass: await _play_fireworks(center_panel_center())
	else: await _play_fail_fx(center_panel_center())

func _exec_split(c: Dictionary) -> void:
	_debug("calc", "A: attr=%d kA=%d | B: attr=%d kB=%d" % [c.attr_a, c.k_a, c.attr_b, c.k_b])

	var eA := 0; var eB := 0
	if c.has_opp and c.enemy > 0 and (c.attr_a + c.attr_b) > 0:
		eA = floori(float(c.enemy) * c.attr_a / (c.attr_a + c.attr_b))
		eB = c.enemy - eA
		_debug("opponent", "分摊: eA=floor(%d×%d/%d)=%d, eB=%d-%d=%d (sum=%d%s)" %
			[c.enemy, c.attr_a, c.attr_a+c.attr_b, eA, c.enemy, eA, eB, eA+eB, " ✓" if eA+eB==c.enemy else " ✗"])

	var nAe = max(0, c.attr_a - eA); var nBe = max(0, c.attr_b - eB)
	var kAc = clamp(c.k_a, 0, nAe); var kBc = clamp(c.k_b, 0, nBe)
	_debug("calc", "nAe=%d kA=%d | nBe=%d kB=%d" % [nAe, kAc, nBe, kBc])

	var pA = _binom_cdf_ge(nAe, kAc, c.p) if nAe > 0 else 0.0
	var pB = _binom_cdf_ge(nBe, kBc, c.p) if nBe > 0 else 0.0
	_debug("prob", "P_A=%.2f%% P_B=%.2f%% | 大=%.2f%% 小=%.2f%% 败=%.2f%%" %
		[pA*100, pB*100, pA*pB*100, (pA*(1-pB)+(1-pA)*pB)*100, (1-pA)*(1-pB)*100])

	var diceA := _roll_dice(c.attr_a, c.p)
	var diceB := _roll_dice(c.attr_b, c.p)
	_debug("roll", "A组: [%s]" % _fmt_dice(diceA))
	_debug("roll", "B组: [%s]" % _fmt_dice(diceB))

	# 骰子动画：A 组上方，B 组下方
	var area := dice_area.get_global_rect()
	var half_h := area.size.y / 2.0 - 20
	var area_a := Rect2(area.position.x, area.position.y + 20, area.size.x, half_h)
	var area_b := Rect2(area.position.x, area.position.y + half_h + 30, area.size.x, half_h)
	var posA := _calc_die_positions(c.attr_a, area_a)
	var posB := _calc_die_positions(c.attr_b, area_b)
	var all_dice := diceA + diceB
	var all_pos := posA + posB

	# 添加分组标签
	var lbl_a := Label.new(); lbl_a.text = "A组 — " + ATTR_CN.get(ATTR_KEYS[_attr_a_opt.selected], "A")
	lbl_a.position = Vector2(area_a.position.x, area_a.position.y - 18)
	lbl_a.add_theme_font_size_override("font_size", 11); lbl_a.add_theme_color_override("font_color", C.dim)
	dice_area.add_child(lbl_a)
	var lbl_b := Label.new(); lbl_b.text = "B组 — " + ATTR_CN.get(ATTR_KEYS[_attr_b_opt.selected], "B")
	lbl_b.position = Vector2(area_b.position.x, area_b.position.y - 18)
	lbl_b.add_theme_font_size_override("font_size", 11); lbl_b.add_theme_color_override("font_color", C.dim)
	dice_area.add_child(lbl_b)

	await _animate_dice_flyin(all_dice, all_pos, area)

	# 对抗
	if c.has_opp and (eA > 0 or eB > 0):
		if c.mode == 1:
			_debug("opponent", "对手回合...")
			var negA := _rand_negate(c.attr_a, mini(eA, c.attr_a))
			var negB := _rand_negate(c.attr_b, mini(eB, c.attr_b))
			for idx in negA:
				_set_die_state(_dice_nodes[idx], "negate"); await get_tree().create_timer(NEGATE_DUR).timeout
			for idx in negB:
				_set_die_state(_dice_nodes[c.attr_a + idx], "negate"); await get_tree().create_timer(NEGATE_DUR).timeout
			var aliveA := range(c.attr_a).filter(func(x): return not negA.has(x))
			var aliveB := range(c.attr_b).filter(func(x): return not negB.has(x))
			var hitA = aliveA.filter(func(x): return diceA[x]).size()
			var hitB = aliveB.filter(func(x): return diceB[x]).size()
			_debug("calc", "A有效命中=%d B有效命中=%d" % [hitA, hitB])
		else:
			var negA := _rand_negate(c.attr_a, mini(eA, c.attr_a))
			var negB := _rand_negate(c.attr_b, mini(eB, c.attr_b))
			for idx in negA: _set_die_state(_dice_nodes[idx], "negate")
			for idx in negB: _set_die_state(_dice_nodes[c.attr_a + idx], "negate")
			var aliveA := range(c.attr_a).filter(func(x): return not negA.has(x))
			var aliveB := range(c.attr_b).filter(func(x): return not negB.has(x))
			var hitA = aliveA.filter(func(x): return diceA[x]).size()
			var hitB = aliveB.filter(func(x): return diceB[x]).size()
			_debug("opponent", "[数值模式] A命中=%d B命中=%d" % [hitA, hitB])

	# 统计结果（重新从 dice_nodes 读取状态）
	var hitA2 := 0; var hitB2 := 0
	for i in range(c.attr_a):
		if _dice_nodes[i].get_child(0).text == "✓": hitA2 += 1
	for i in range(c.attr_b):
		if _dice_nodes[c.attr_a + i].get_child(0).text == "✓": hitB2 += 1

	var passA = hitA2 >= kAc; var passB = hitB2 >= kBc
	_debug("result", "A: %d≥%d %s | B: %d≥%d %s" % [hitA2, kAc, "✓" if passA else "✗", hitB2, kBc, "✓" if passB else "✗"])

	var tier: String; var txt: String
	if passA and passB: tier = "major"; txt = "🎉 大成功！A(%d≥%d) B(%d≥%d)" % [hitA2, kAc, hitB2, kBc]
	elif passA or passB: tier = "minor"; txt = "👍 小成功 — %s %s" % [("A✓" if passA else "A✗"), ("B✓" if passB else "B✗")]
	else: tier = "fail"; txt = "💀 失败 — A(%d<%d) B(%d<%d)" % [hitA2, kAc, hitB2, kBc]
	_debug("result", "BANDS → %s" % tier.to_upper())

	_show_result(tier, txt)
	threshold_info.text = "A: %d / %d %s | B: %d / %d %s" % [hitA2, kAc, "✓" if passA else "✗", hitB2, kBc, "✓" if passB else "✗"]
	if tier == "major": await _play_fireworks(center_panel_center())
	elif tier == "minor": await _play_fireworks(center_panel_center())
	else: await _play_fail_fx(center_panel_center())

# ============================================================
# 骰子飞入动画
# ============================================================
func _animate_dice_flyin(dice: Array, final_positions: Array, area: Rect2) -> void:
	var viewport := get_viewport().get_visible_rect().size
	_dice_nodes.clear()

	# 创建骰子并设置初始位置
	for i in range(dice.size()):
		var die := _make_die()
		_set_die_state(die, "random")
		die.position = _random_edge_pos(viewport)
		die.rotation = randf_range(-3.0, 3.0)
		dice_area.add_child(die)
		_dice_nodes.append(die)

	# 启动随机值变化定时器
	roll_timer.start(0.06)

	# 动画
	var tween := create_tween().set_parallel(true)
	for i in range(dice.size()):
		var die: PanelContainer = _dice_nodes[i]
		var dur := ANIM_DUR + randf_range(-0.2, 0.2)
		tween.tween_property(die, "position", final_positions[i], dur).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BOUNCE)
		tween.tween_property(die, "rotation", 0.0, dur).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_ELASTIC)

	await tween.finished
	roll_timer.stop()

	# 设置最终状态
	for i in range(dice.size()):
		_set_die_state(_dice_nodes[i], "hit" if dice[i] else "miss")

func _on_roll_timer() -> void:
	for die in _dice_nodes:
		_set_die_state(die, "random")

# ============================================================
# 结果显示
# ============================================================
func _show_result(tier: String, text: String) -> void:
	match tier:
		"pass", "minor":
			result_label.add_theme_color_override("font_color", C.neon)
		"major":
			result_label.add_theme_color_override("font_color", C.gold)
		"fail":
			result_label.add_theme_color_override("font_color", C.red)
	result_label.text = text

func _fmt_dice(dice: Array) -> String:
	return " ".join(dice.map(func(d): return "✓" if d else "✗"))

func center_panel_center() -> Vector2:
	return $CenterPanel.get_global_rect().get_center()

# ============================================================
# 生命周期
# ============================================================
func _ready() -> void:
	_build_left()
	_update_badge()
	_update_prob()
	_debug("system", "事件检定系统就绪")

func _on_back() -> void:
	var path := str(Globals.scene_paths.get("main_menu", "res://scenes/ui/main_menu/MainMenu.tscn"))
	Globals.log("EventCheck", "返回主菜单 → %s" % path)
	var err = get_tree().change_scene_to_file(path)
	if err != OK: Globals.log_error("EventCheck", "场景切换失败: %d" % err)
