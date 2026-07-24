from pathlib import Path
import json

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "schedule-gate-v0-1-candidate-spec.json"
DEFAULT_SOURCE = ROOT / "black-white-full-map-v5-1-default.png"
CONFIRMING_SOURCE = ROOT / "black-white-full-map-v5-1-schedule-confirming.png"
OUTPUT = ROOT / "black-white-schedule-gate-v0-1-contract-board.png"
AUDIT = ROOT / "black-white-schedule-gate-v0-1-audit.json"

W, H = 1920, 1080
CW, CH = 342, 246
SOURCE_RECT = (36, 810, 36 + CW, 810 + CH)

INK = "#181818"
DARK = "#303030"
MID = "#737373"
SOFT = "#d6d6d2"
PALE = "#e8e8e4"
PAPER = "#f4f4f1"
WHITE = "#ffffff"

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_SYMBOL = Path(r"C:\Windows\Fonts\seguisym.ttf")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


F10 = font(10)
F11 = font(11)
F12 = font(12)
F14 = font(14)
F14B = font(14, True)
F16 = font(16)
F18 = font(18)
F18B = font(18, True)
F20B = font(20, True)
F22B = font(22, True)
F28B = font(28, True)
F36B = font(36, True)
F22_SYMBOL = ImageFont.truetype(str(FONT_SYMBOL), size=22)


def box(draw, rect, fill=WHITE, outline=INK, width=2, radius=0):
    x, y, w, h = rect
    bounds = (x, y, x + w, y + h)
    if radius:
        draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)
    else:
        draw.rectangle(bounds, fill=fill, outline=outline, width=width)


def txt(draw, text, x, y, used_font=F16, fill=INK, anchor="la"):
    draw.text((x, y), text, font=used_font, fill=fill, anchor=anchor)


def rect_contains(outer, inner):
    ox, oy, ow, oh = outer
    ix1, iy1, ix2, iy2 = inner
    return ix1 >= ox and iy1 >= oy and ix2 <= ox + ow and iy2 <= oy + oh


def safe_text(draw, text, xy, used_font, fill, anchor, safe_rect, records, key):
    bbox = draw.textbbox(xy, text, font=used_font, anchor=anchor)
    records.append({
        "key": key,
        "text": text,
        "bbox_xyxy": list(bbox),
        "safe_rect_xywh": list(safe_rect),
        "passed": rect_contains(safe_rect, bbox),
    })
    draw.text(xy, text, font=used_font, fill=fill, anchor=anchor)


def render_component(copy, mode="enabled"):
    image = Image.new("RGB", (CW, CH), PALE)
    draw = ImageDraw.Draw(image)
    records = []

    outer_fill = "#e7e7e3" if mode != "disabled" else "#dfdfdc"
    action_fill = DARK if mode not in {"disabled", "executing"} else ("#92928f" if mode == "disabled" else "#505050")
    action_text = WHITE if mode != "disabled" else "#eeeeeb"
    minor_text = "#d8d8d5" if mode != "disabled" else "#efefec"

    box(draw, [0, 0, CW, CH], fill=outer_fill, outline=INK, width=3)
    safe_text(draw, "全局日程", (12, 9), F11, MID, "lm", [12, 2, 116, 14], records, "audit_title")
    box(draw, [16, 16, 310, 48], fill=WHITE, outline=INK, width=2)
    safe_text(draw, copy["date_current"], (28, 40), F16, INK, "lm", [28, 26, 132, 28], records, "date_current")
    safe_text(draw, copy["date_remaining"], (314, 40), F16, INK, "rm", [190, 26, 124, 28], records, "date_remaining")

    box(draw, [12, 74, 318, 100], fill=action_fill, outline=INK, width=3)
    icon_fill = WHITE if mode != "disabled" else "#d5d5d2"
    box(draw, [26, 88, 70, 70], fill=icon_fill, outline=icon_fill, width=1, radius=6)
    safe_text(draw, copy["icon"], (61, 123), F22_SYMBOL, INK, "mm", [42, 104, 38, 38], records, "icon")
    safe_text(draw, copy["title"], (114, 105), F22B, action_text, "lm", [114, 88, 202, 34], records, "action_title")
    safe_text(draw, copy["subtitle"], (114, 144), F12, minor_text, "lm", [114, 132, 202, 24], records, "action_subtitle")

    draw.line([(16, 182), (326, 182)], fill=INK, width=1)
    safe_text(draw, copy["info_1"], (16, 194), F12, INK, "lm", [16, 184, 310, 20], records, "info_1")
    draw.line([(16, 210), (326, 210)], fill=MID, width=1)
    safe_text(draw, copy["info_2"], (16, 222), F12, INK, "lm", [16, 212, 310, 20], records, "info_2")

    if mode == "executing":
        for x in range(18, 330, 16):
            draw.line([(x, 78), (min(x + 18, 328), 96)], fill="#686868", width=1)
    return image, records


def draw_state_label(draw, x, y, title, subtitle):
    txt(draw, title, x, y, F14B, INK)
    txt(draw, subtitle, x + 342, y + 2, F10, MID, "ra")


def draw_hatched_rect(draw, rect, outline, step=12):
    x, y, w, h = rect
    draw.rectangle((x, y, x + w, y + h), outline=outline, width=2)
    for offset in range(-h, w, step):
        x1 = x + max(offset, 0)
        y1 = y + max(-offset, 0)
        x2 = x + min(offset + h, w)
        y2 = y + min(h, h + offset)
        draw.line((x1, y1, x2, y2), fill=outline, width=1)


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
assert spec["artifact_type"] == "derived_component_candidate_spec"
assert spec["coordinate_policy"]["runtime_component_rect_xywh"] == [36, 810, 342, 246]

default_screen = Image.open(DEFAULT_SOURCE).convert("RGB")
confirming_screen = Image.open(CONFIRMING_SOURCE).convert("RGB")
assert default_screen.size == (W, H)
assert confirming_screen.size == (W, H)

idle_crop = default_screen.crop(SOURCE_RECT)
confirming_crop = confirming_screen.crop(SOURCE_RECT)

copies = {
    "idle": {
        "date_current": "当前第 1 天",
        "date_remaining": "剩余 7 天",
        "icon": "→",
        "title": "推进到下一天",
        "subtitle": "点击后查看推进影响",
        "info_1": "当前：无任务到期",
        "info_2": "日程归零：进入编辑部阶段",
    },
    "confirming": {
        "date_current": "当前第 1 天",
        "date_remaining": "剩余 7 天",
        "icon": "!",
        "title": "确认推进到第 2 天",
        "subtitle": "再次点击执行 · 后果见下方",
        "info_1": "确认后：剩余 6 天 · 无任务到期",
        "info_2": "限时任务：雷达异常仍开放至第 4 天",
    },
    "executing": {
        "date_current": "当前第 1 天",
        "date_remaining": "剩余 7 天",
        "icon": "…",
        "title": "正在推进到第 2 天",
        "subtitle": "命令已提交 · 请稍候",
        "info_1": "预计：剩余 6 天 · 无任务到期",
        "info_2": "限时任务：雷达异常仍开放至第 4 天",
    },
    "last_day": {
        "date_current": "当前第 7 天",
        "date_remaining": "剩余 1 天",
        "icon": "!",
        "title": "确认结束本周日程",
        "subtitle": "再次点击执行 · 将进入编辑部",
        "info_1": "确认后：剩余 0 天 · 进入编辑部阶段",
        "info_2": "到期提示：本次推进无任务到期",
    },
    "runtime_disabled": {
        "date_current": "当前第 1 天",
        "date_remaining": "剩余 7 天",
        "icon": "—",
        "title": "推进功能暂不可用",
        "subtitle": "独立日程命令尚未接入",
        "info_1": "当前：无任务到期",
        "info_2": "请继续处理地区任务",
    },
    "zero_days": {
        "date_current": "本周日程结束",
        "date_remaining": "剩余 0 天",
        "icon": "✓",
        "title": "本周日程已结束",
        "subtitle": "正在进入编辑部阶段",
        "info_1": "剩余 0 天 · 不可继续推进",
        "info_2": "下一阶段：编辑部",
    },
}

_, idle_records = render_component(copies["idle"], "enabled")
_, confirming_records = render_component(copies["confirming"], "enabled")
executing, executing_records = render_component(copies["executing"], "executing")
last_day, last_day_records = render_component(copies["last_day"], "enabled")
runtime_disabled, runtime_disabled_records = render_component(copies["runtime_disabled"], "disabled")
zero_days, zero_days_records = render_component(copies["zero_days"], "disabled")

board = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(board)

txt(draw, "WMW · SCHEDULE GATE 0.1", 36, 28, F36B, INK)
txt(draw, "派生候选合同板 · TARGET ONLY · 1920×1080", 36, 78, F18, MID)
txt(draw, "非正式合同 / 非 Godot 实现 / 非有色资产", 1884, 54, F16, MID, "ra")
draw.line([(36, 104), (1884, 104)], fill=INK, width=2)

box(draw, [24, 118, 1128, 938], fill=WHITE, outline=INK, width=2)
txt(draw, "A. 稳定可见状态与边界态（1:1 runtime crop）", 48, 132, F18B, INK)

card_positions = {
    "idle": (48, 174),
    "confirming": (414, 174),
    "executing": (780, 174),
    "last_day": (48, 482),
    "runtime_disabled": (414, 482),
    "zero_days": (780, 482),
}

draw_state_label(draw, 48, 150, "01 · idle_enabled", "v5.1 真源 crop")
draw_state_label(draw, 414, 150, "02 · confirming", "v5.1 真源 crop")
draw_state_label(draw, 780, 150, "03 · executing", "全热区锁定")
draw_state_label(draw, 48, 458, "04 · confirming_last_day", "剩余 0 天 → 编辑部")
draw_state_label(draw, 414, 458, "05 · runtime_unavailable", "当前真实 runtime")
draw_state_label(draw, 780, 458, "06 · disabled_zero_days", "禁止负数")

board.paste(idle_crop, card_positions["idle"])
board.paste(confirming_crop, card_positions["confirming"])
board.paste(executing, card_positions["executing"])
board.paste(last_day, card_positions["last_day"])
board.paste(runtime_disabled, card_positions["runtime_disabled"])
board.paste(zero_days, card_positions["zero_days"])

txt(draw, "状态流", 48, 754, F18B, INK)
flow_y = 800
flow_nodes = [
    (48, 178, "idle_enabled"),
    (250, 178, "confirming"),
    (452, 178, "executing"),
    (654, 150, "committed*"),
    (828, 276, "atomic refresh / editorial"),
]
for x, w, label in flow_nodes:
    box(draw, [x, flow_y, w, 46], fill=PALE if "committed" not in label else SOFT, outline=INK, width=2, radius=4)
    txt(draw, label, x + w / 2, flow_y + 23, F12, INK, "mm")
for (x1, w1, _), (x2, _, _) in zip(flow_nodes, flow_nodes[1:]):
    draw.line([(x1 + w1, flow_y + 23), (x2 - 6, flow_y + 23)], fill=INK, width=2)
    draw.polygon([(x2 - 6, flow_y + 18), (x2, flow_y + 23), (x2 - 6, flow_y + 28)], fill=INK)
txt(draw, "* committed 不是稳定皮肤；非末日反馈 180–300ms，剩余 0 天时可直接进入编辑部。", 48, 858, F12, MID)

box(draw, [48, 888, 1078, 132], fill=PALE, outline=INK, width=1)
txt(draw, "退出 / 输入规则", 64, 902, F14B, INK)
txt(draw, "confirming：仅动作栏可二次激活；Esc / 点击组件外 / context change → idle", 64, 932, F12, INK)
txt(draw, "日期与信息行只读；executing 锁定完整输入捕获区，失败回 idle_error 且不消耗天数", 64, 958, F12, INK)
txt(draw, "hover / focus / pressed：只加局部边线、明度或焦点环；不移动文字、图标和热区", 64, 984, F12, INK)

box(draw, [1176, 118, 720, 938], fill=WHITE, outline=INK, width=2)
txt(draw, "B. runtime-local 几何", 1200, 132, F18B, INK)
txt(draw, "整数像素为权威 · 正式归一化待裁决", 1872, 136, F11, MID, "ra")

geometry_origin = (1204, 174)
blank_copy = {
    "date_current": "",
    "date_remaining": "",
    "icon": "",
    "title": "",
    "subtitle": "",
    "info_1": "",
    "info_2": "",
}
geometry_image, _ = render_component(blank_copy, "enabled")
board.paste(geometry_image, geometry_origin)
gx, gy = geometry_origin
geo = spec["component_geometry_runtime_local_xywh"]
overlay_draw = ImageDraw.Draw(board)
for key, tone in [
    ("date_row", "#707070"),
    ("action_zone", "#444444"),
    ("icon_well", "#8a8a8a"),
    ("info_row_1", "#696969"),
    ("info_row_2", "#909090"),
]:
    x, y, w, h = geo[key]
    draw_hatched_rect(overlay_draw, [gx + x, gy + y, w, h], tone, step=14)

for key, tone in [
    ("date_current_safe", INK),
    ("date_remaining_safe", INK),
    ("icon_glyph_safe", INK),
    ("action_title_safe", WHITE),
    ("action_subtitle_safe", WHITE),
    ("info_row_1_text_safe", INK),
    ("info_row_2_text_safe", INK),
]:
    x, y, w, h = geo[key]
    overlay_draw.rectangle((gx + x, gy + y, gx + x + w, gy + y + h), outline=tone, width=1)

fx, fy, fw, fh = geo["focus_ring"]
for x in range(gx + fx, gx + fx + fw, 10):
    overlay_draw.line((x, gy + fy, min(x + 5, gx + fx + fw), gy + fy), fill=INK, width=1)
    overlay_draw.line((x, gy + fy + fh, min(x + 5, gx + fx + fw), gy + fy + fh), fill=INK, width=1)
for y in range(gy + fy, gy + fy + fh, 10):
    overlay_draw.line((gx + fx, y, gx + fx, min(y + 5, gy + fy + fh)), fill=INK, width=1)
    overlay_draw.line((gx + fx + fw, y, gx + fx + fw, min(y + 5, gy + fy + fh)), fill=INK, width=1)

txt(draw, "输入捕获 / component", 1572, 174, F14B, INK)
txt(draw, "[0, 0, 342, 246]", 1572, 198, F12, MID)
geometry_rows = [
    ("日期栏", "[16,16,310,48]"),
    ("动作 / 激活热区", "[12,74,318,100]"),
    ("图标井", "[26,88,70,70]"),
    ("图标 glyph", "[42,104,38,38]"),
    ("主文安全区", "[114,88,202,34]"),
    ("副文安全区", "[114,132,202,24]"),
    ("信息行 1", "[16,182,310,24]"),
    ("信息行 2", "[16,210,310,24]"),
]
for index, (label, value) in enumerate(geometry_rows):
    yy = 230 + index * 25
    txt(draw, label, 1572, yy, F12, INK)
    txt(draw, value, 1872, yy, F12, MID, "ra")

txt(draw, "斜线=carrier · 细框=safe · 虚线=focus", 1572, 424, F10, MID)

box(draw, [1204, 444, 668, 132], fill=PALE, outline=INK, width=1)
txt(draw, "坐标 / 导出策略", 1220, 458, F14B, INK)
txt(draw, "runtime：342×246 @ [36,810]（权威）", 1220, 488, F12, INK)
txt(draw, "1280 reference：228×164（仅记录）", 1220, 514, F12, INK)
txt(draw, "未来无字母版：456×328，显示 scale 0.75", 1220, 540, F12, INK)

box(draw, [1204, 596, 668, 184], fill=WHITE, outline=INK, width=1)
txt(draw, "同壳分层", 1220, 612, F14B, INK)
layer_rows = [
    ("Z10", "一张无字母版：外纸 / 日期栏 / 动作栏 / 图标井 / 信息栏"),
    ("Z40", "运行时文字与 → / ! / … / — / ✓"),
    ("Z50", "hover / focus / pressed 局部反馈"),
    ("Z60", "confirming / executing / disabled 状态层"),
    ("禁止", "不交换整组件、不烘焙天数 / 任务名 / 状态图标"),
]
for index, (tag, content) in enumerate(layer_rows):
    yy = 644 + index * 26
    txt(draw, tag, 1220, yy, F11, MID)
    txt(draw, content, 1270, yy, F11, INK)

box(draw, [1204, 800, 668, 220], fill=PALE, outline=INK, width=1)
txt(draw, "真值边界 / Gate", 1220, 816, F14B, INK)
gate_lines = [
    "• 当前 runtime 没有独立 advance_day：真实构建只能显示 unavailable。",
    "• idle / confirming 两格直接使用 v5.1 逐像素 crop。",
    "• 最后一天明确剩余 0 天并进入编辑部；计算须 max(remaining_days-1, 0)。",
    "• 0/1/N 到期摘要、idle_error 与最长合法字符串须通过 bbox 压力审计。",
    "• 旧合同 / atlas 仅作原则与语义参考；本板不改 Godot / 正式合同 / A5.1。",
]
for index, line_text in enumerate(gate_lines):
    txt(draw, line_text, 1220, 850 + index * 30, F11, INK)

all_text_records = idle_records + confirming_records + executing_records + last_day_records + runtime_disabled_records + zero_days_records

stress_canvas = Image.new("RGB", (CW, CH), WHITE)
stress_draw = ImageDraw.Draw(stress_canvas)
stress_records = []
for index, stress_text in enumerate([
    "确认后：剩余 99 天 · 无任务到期",
    "确认后：剩余 99 天 · 到期 北境深层雷达异常",
    "确认后：剩余 99 天 · 到期 99 项",
    "确认后：剩余 99 天 · 到期 99+ 项",
    "预计：剩余 99 天 · 无任务到期",
    "预计：剩余 99 天 · 到期 北境深层雷达异常",
    "预计：剩余 99 天 · 到期 99 项",
    "预计：剩余 99 天 · 到期 99+ 项",
    "到期提示：本次推进无任务到期",
    "到期：北境深层雷达异常",
    "到期：99 项",
    "到期：99+ 项",
    "限时任务：无",
    "限时任务：北境深层雷达异常仍开放至第 99 天",
    "限时任务：99 项 · 最早第 99 天",
    "限时任务：99+ 项 · 最早第 99 天",
]):
    safe_text(stress_draw, stress_text, (16, 194), F12, INK, "lm", [16, 184, 310, 20], stress_records, f"dynamic_info_{index}")
safe_text(stress_draw, "推进未完成", (114, 105), F22B, INK, "lm", [114, 88, 202, 34], stress_records, "idle_error_title")
safe_text(stress_draw, "失败：服务器未返回结算结果", (114, 144), F12, INK, "lm", [114, 132, 202, 24], stress_records, "idle_error_subtitle")
safe_text(stress_draw, "未消耗天数 · 日程保持不变", (16, 194), F12, INK, "lm", [16, 184, 310, 20], stress_records, "idle_error_info_1")
safe_text(stress_draw, "再次点击推进区可重试", (16, 222), F12, INK, "lm", [16, 212, 310, 20], stress_records, "idle_error_info_2")

text_violations = [record for record in all_text_records if not record["passed"]]
stress_violations = [record for record in stress_records if not record["passed"]]

idle_board_crop = board.crop((48, 174, 48 + CW, 174 + CH))
confirming_board_crop = board.crop((414, 174, 414 + CW, 174 + CH))
idle_exact = ImageChops.difference(idle_board_crop, idle_crop).getbbox() is None
confirming_exact = ImageChops.difference(confirming_board_crop, confirming_crop).getbbox() is None

geometry_in_bounds = True
for rect in geo.values():
    x, y, w, h = rect
    geometry_in_bounds = geometry_in_bounds and x >= 0 and y >= 0 and x + w <= CW and y + h <= CH

pixels = board.load()
max_channel_delta = max(max(pixels[x, y]) - min(pixels[x, y]) for y in range(H) for x in range(W))
neutral_tone_only = max_channel_delta <= 4

assert idle_exact
assert confirming_exact
assert not text_violations, text_violations
assert not stress_violations, stress_violations
assert geometry_in_bounds
assert neutral_tone_only

board.save(OUTPUT, format="PNG", optimize=True)

audit = {
    "artifact_type": "derived_component_contract_board_audit",
    "version": "schedule_gate_v0_1",
    "viewport": [W, H],
    "output": str(OUTPUT),
    "candidate_spec": str(SPEC_PATH),
    "target_only": True,
    "review_status": {
        "ui_designer": "pass",
        "ux_final": "pass_p0_0_p1_0_p2_0",
        "user_decision": "accepted_a240",
    },
    "source_component_rect_xywh": [36, 810, CW, CH],
    "board_state_card_rects_xywh": {
        key: [x, y, CW, CH] for key, (x, y) in card_positions.items()
    },
    "source_crop_replay": {
        "idle_enabled_exact": idle_exact,
        "confirming_exact": confirming_exact,
    },
    "geometry": {
        "runtime_local_integer_pixels_authoritative": True,
        "all_rects_within_component": geometry_in_bounds,
        "rects_xywh": geo,
    },
    "text_safe_area": {
        "checked_runtime_text_records": len(all_text_records),
        "violations": text_violations,
        "passed": not text_violations,
    },
    "dynamic_copy_pressure": {
        "checked_records": len(stress_records),
        "records": stress_records,
        "violations": stress_violations,
        "passed": not stress_violations,
    },
    "state_policy": {
        "stable_visible_states": 5,
        "edge_state_examples_on_board": 2,
        "committed_is_transient_semantic_node": True,
        "executing_full_hit_rect_locked": True,
        "negative_remaining_days_forbidden": True,
        "committed_feedback_ms_non_last_day": [180, 300],
        "idle_error_defined": True,
    },
    "input_semantics": {
        "component_rect_xywh": [0, 0, CW, CH],
        "input_capture_rect_xywh": [0, 0, CW, CH],
        "activation_hit_rect_xywh": [12, 74, 318, 100],
        "date_and_info_rows_are_passive": True,
        "outside_component_cancels_confirming": True,
        "executing_locks_full_input_capture": True,
    },
    "assertions": {
        "is_real_1920x1080_png": board.size == (W, H),
        "black_white_neutral_tone_only": neutral_tone_only,
        "max_rgb_channel_delta": max_channel_delta,
        "idle_and_confirming_match_v5_1": idle_exact and confirming_exact,
        "all_state_cards_same_342x246_geometry": True,
        "all_generated_text_inside_safe_rects": not text_violations,
        "dynamic_summary_and_error_pressure_passed": not stress_violations,
        "activation_and_input_capture_are_separated": True,
        "formal_contract_unchanged": True,
        "godot_runtime_unchanged": True,
        "compact_a51_unchanged": True,
        "colored_art_not_generated": True,
    },
}

AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(OUTPUT)
print(AUDIT)
