from pathlib import Path
import json

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "black-white-full-map-v4-default.png"
OUTPUT_A = ROOT / "black-white-redline-status-v5-a-earliest-deadline.png"
OUTPUT_B = ROOT / "black-white-redline-status-v5-b-remove-stamp.png"
DEFAULT_OUTPUT = ROOT / "black-white-full-map-v5-default.png"
AUDIT = ROOT / "black-white-redline-status-v5-audit.json"

W, H = 1920, 1080
INK = "#171717"
MID = "#777777"
SOFT = "#d6d6d2"
WHITE = "#ffffff"

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


F16 = font(16)
F16B = font(16, True)
F20 = font(20)
F22B = font(22, True)


def box(draw, rect, fill=WHITE, outline=INK, width=2):
    x, y, w, h = rect
    draw.rectangle((x, y, x + w, y + h), fill=fill, outline=outline, width=width)


def center(draw, text, rect, used_font, fill=INK):
    x, y, w, h = rect
    draw.text((x + w / 2, y + h / 2), text, font=used_font, fill=fill, anchor="mm")


def redraw_region_body(draw):
    body = [1431, 456, 414, 135]
    box(draw, body, fill=WHITE, outline=INK, width=2)
    draw.text((1450, 495), "都市传说与军事封锁交叉。", font=F20, fill=INK, anchor="la")
    draw.text((1450, 542), "地区说明只回答为什么去。", font=F16, fill=MID, anchor="la")


def build_candidate_a(source):
    image = source.copy()
    draw = ImageDraw.Draw(image)
    stamp = [1767, 75, 87, 87]
    box(draw, stamp, fill=SOFT, outline=INK, width=2)
    center(draw, "最早截止", [1773, 91, 75, 20], F16B)
    center(draw, "第4天", [1773, 118, 75, 28], F22B)
    redraw_region_body(draw)
    return image


def build_candidate_b(source):
    image = source.copy()
    draw = ImageDraw.Draw(image)

    # 只清理 A5.1-H warning 派生态的标题 / 状态章区域。
    draw.rectangle((1519, 72, 1856, 164), fill=WHITE)
    title = [1521, 87, 333, 51]
    box(draw, title, fill=SOFT, outline=INK, width=2)
    center(draw, "北美禁区带", title, F22B)
    redraw_region_body(draw)
    return image


def rect_contains(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def diff_audit(source, candidate, allowed_rects):
    diff = ImageChops.difference(source, candidate)
    bbox = diff.getbbox()
    changed_pixels = 0
    outside_allowed = 0
    if bbox is not None:
        pixels = diff.load()
        for y in range(bbox[1], bbox[3]):
            for x in range(bbox[0], bbox[2]):
                if pixels[x, y] != (0, 0, 0):
                    changed_pixels += 1
                    if not any(rect_contains(x, y, rect) for rect in allowed_rects):
                        outside_allowed += 1
    return {
        "difference_bbox_xyxy": list(bbox) if bbox else None,
        "changed_pixels": changed_pixels,
        "outside_allowed_pixels": outside_allowed,
        "allowed_rects_xywh": allowed_rects,
        "passed": outside_allowed == 0,
    }


source = Image.open(SOURCE).convert("RGB")
assert source.size == (W, H)

candidate_a = build_candidate_a(source)
candidate_b = build_candidate_b(source)
assert candidate_a.size == (W, H)
assert candidate_b.size == (W, H)

candidate_a.save(OUTPUT_A, format="PNG", optimize=True)
candidate_b.save(OUTPUT_B, format="PNG", optimize=True)
candidate_b.save(DEFAULT_OUTPUT, format="PNG", optimize=True)

a_diff = diff_audit(
    source,
    candidate_a,
    [[1767, 75, 87, 87], [1431, 456, 414, 135]],
)
b_diff = diff_audit(
    source,
    candidate_b,
    [[1519, 72, 337, 92], [1431, 456, 414, 135]],
)

assert a_diff["passed"]
assert b_diff["passed"]

audit = {
    "artifact_type": "structure_wireframe_variant_pair",
    "version": "redline_status_decision_v5",
    "viewport": [W, H],
    "source": str(SOURCE),
    "shared_invariants": {
        "left_column_unchanged": True,
        "center_map_unchanged": True,
        "right_photo_unchanged": True,
        "mission_intel_summary_unchanged": True,
        "four_mission_rows_unchanged": True,
        "task_03_deadline_label_unchanged": True,
        "cta_unchanged": True,
        "region_body_rect": [1431, 456, 414, 135],
        "incorrect_remaining_days_sentence_removed": True,
        "compact_a51_frozen_contract_changed": False,
        "godot_runtime_changed": False,
        "colored_art_generated": False,
    },
    "candidate_a": {
        "role": "CONDITIONAL",
        "output": str(OUTPUT_A),
        "region_title": [1521, 87, 240, 51],
        "status_stamp": [1767, 75, 87, 87],
        "label_safe_zone": [1773, 91, 75, 20],
        "value_safe_zone": [1773, 118, 75, 28],
        "copy": ["最早截止", "第4天"],
        "interactive": False,
        "requires_earliest_deadline_day": True,
        "requires_same_source_as_visible_mission_rows": True,
        "current_runtime_support": False,
        "diff": a_diff,
    },
    "candidate_b": {
        "role": "SELECTED_DEFAULT",
        "output": str(OUTPUT_B),
        "promoted_default_output": str(DEFAULT_OUTPUT),
        "warning_title_override": [1521, 87, 333, 51],
        "warning_status_stamp_visible": False,
        "locked_chain_status_stamp_capability_retained": True,
        "compact_a51_base_slot_retained": True,
        "interactive": False,
        "requires_new_runtime_aggregate": False,
        "diff": b_diff,
    },
    "decision": {
        "selected": "B",
        "selected_at": "2026-07-20",
        "reason": "当前状态章不独占回答玩家问题；剩余天数已由左下日程器承载，限时数量与具体截止分别由任务摘要和任务行承载。",
        "candidate_a_retained_as_conditional_reference": True,
        "user_ruling_required_before_runtime_or_contract_change": False,
        "runtime_or_contract_change_authorized": False,
    },
}

AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(OUTPUT_A)
print(OUTPUT_B)
print(DEFAULT_OUTPUT)
print(AUDIT)
