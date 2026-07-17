from pathlib import Path
import json

from PIL import ImageDraw

import render_functional_closure_v3 as base


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "black-white-full-map-v4-default.png"
EVENT_OUTPUT = ROOT / "black-white-full-map-v4-world-change.png"
AUDIT = ROOT / "black-white-full-map-v4-audit.json"

W, H = 1920, 1080
INK = base.INK
DARK = base.DARK
MID = base.MID
SOFT = base.SOFT
PALE = base.PALE
PAPER = base.PAPER
WHITE = base.WHITE


def line(draw, points, fill=INK, width=2):
    draw.line(points, fill=fill, width=width, joint="curve")


def txt(draw, text, x, y, font=base.F16, fill=INK, anchor="la"):
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)


def center(draw, text, rect, font=base.F16, fill=INK):
    x, y, w, h = rect
    txt(draw, text, x + w / 2, y + h / 2, font=font, fill=fill, anchor="mm")


def box(draw, x, y, w, h, fill=WHITE, outline=INK, width=2, radius=0):
    bounds = (x, y, x + w, y + h)
    if radius:
        draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)
    else:
        draw.rectangle(bounds, fill=fill, outline=outline, width=width)


def dashed_rect(draw, x, y, w, h, fill="#b0b0ac", dash=10, gap=8, width=1):
    for sx in range(x, x + w, dash + gap):
        line(draw, [(sx, y), (min(sx + dash, x + w), y)], fill=fill, width=width)
        line(draw, [(sx, y + h), (min(sx + dash, x + w), y + h)], fill=fill, width=width)
    for sy in range(y, y + h, dash + gap):
        line(draw, [(x, sy), (x, min(sy + dash, y + h))], fill=fill, width=width)
        line(draw, [(x + w, sy), (x + w, min(sy + dash, y + h))], fill=fill, width=width)


def build_default():
    image = base.img.copy()
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, 401, 23), fill=PAPER)
    txt(draw, "LOW-FIDELITY V4 · FULL MAP / CONDITIONAL FEEDBACK · 1920×1080", 16, 8, font=base.F11, fill=MID)

    # Remove the old v3 receipt band and its diagnostic labels.
    draw.rectangle((402, 916, 1374, 1057), fill=PAPER)

    # Remove the old map-size label before moving it to the new bottom edge.
    draw.rectangle((438, 882, 700, 914), fill=WHITE)
    for gx in (518, 610):
        line(draw, [(gx, 882), (gx, 914)], fill="#e0e0dc", width=1)

    # Extend the same map board to y=1032 without moving any existing pins.
    draw.rectangle((426, 916, 1350, 1032), fill=WHITE)
    for gx in range(518, 1350, 92):
        line(draw, [(gx, 916), (gx, 1032)], fill="#e0e0dc", width=1)
    for gy in (916, 1007):
        line(draw, [(426, gy), (1350, gy)], fill="#e0e0dc", width=1)

    # Non-interactive southern world silhouette: geography only, never a fourth region.
    antarctica = [
        (496, 968),
        (570, 948),
        (650, 956),
        (735, 938),
        (820, 950),
        (910, 936),
        (1004, 949),
        (1090, 940),
        (1180, 955),
        (1270, 946),
        (1310, 980),
        (1220, 1008),
        (1108, 998),
        (1010, 1014),
        (910, 1002),
        (812, 1016),
        (710, 1000),
        (604, 1012),
        (520, 996),
    ]
    draw.polygon(antarctica, fill="#e1e1dd", outline=INK)

    box(draw, 426, 96, 924, 936, fill=None, outline=INK, width=3)
    txt(draw, "地图主舞台 924×936 · DEFAULT 无常驻底带", 888, 1042, font=base.F10, fill=MID, anchor="ma")

    # Restore the logical center-column guides removed by the clear pass.
    dashed_rect(draw, 402, 24, 972, 1032)
    return image


def build_event(default_image):
    image = default_image.copy()
    draw = ImageDraw.Draw(image)

    draw.rectangle((404, 1033, 1372, 1055), fill=PAPER)

    # Conditional overlay. It does not alter the map rect or add an interaction.
    box(draw, 450, 942, 876, 90, fill=WHITE, outline=INK, width=3)
    box(draw, 462, 956, 40, 40, fill=SOFT, outline=INK, width=2, radius=4)
    center(draw, "Δ", (462, 956, 40, 40), font=base.F20)
    txt(draw, "最近世界变化", 518, 950, font=base.F18, fill=INK)
    txt(draw, "红线窗口已推进", 518, 997, font=base.F20, fill=INK, anchor="ls")
    txt(draw, "北美禁区带", 1056, 950, font=base.F14, fill=MID)
    txt(draw, "剩余 7 天 → 6 天", 1056, 997, font=base.F18, fill=INK, anchor="ls")
    txt(draw, "条件态：仅真实 before / after 差量出现 · 无命中", 888, 1039, font=base.F10, fill=MID, anchor="ma")
    return image


default_image = build_default()
event_image = build_event(default_image)
default_image.save(DEFAULT_OUTPUT, format="PNG", optimize=True)
event_image.save(EVENT_OUTPUT, format="PNG", optimize=True)

audit = {
    "artifact_type": "structure_wireframe_state_pair",
    "version": "full_map_feedback_v4",
    "viewport": [W, H],
    "default": {
        "map_stage": [426, 96, 924, 936],
        "bottom_receipt_strips": [],
        "bottom_safe_margin": [402, 1032, 972, 24],
        "event_overlay_present": False,
    },
    "conditional_world_change": {
        "map_stage": [426, 96, 924, 936],
        "overlay": [450, 942, 876, 90],
        "icon": [462, 956, 40, 40],
        "title": [518, 950, 180, 24],
        "main_delta": [518, 978, 518, 30],
        "affected_object": [1056, 950, 246, 24],
        "value_delta": [1056, 978, 246, 30],
        "interactive": False,
        "requires_event_id": True,
        "requires_cause": True,
        "requires_before_after": True,
        "current_runtime_support": False,
    },
    "map_interaction_safe_zone": [450, 120, 876, 798],
    "assertions": {
        "default_receipts_absent": True,
        "default_map_reaches_y1032": True,
        "map_rect_stable_across_states": True,
        "overlay_inside_map": True,
        "overlay_is_conditional": True,
        "overlay_has_no_hit_rect": True,
        "current_world_receipts_not_promoted_to_event_delta": True,
        "legend_absent": True,
        "fourth_region_absent": True,
        "v3_left_and_right_columns_unchanged": True,
        "runtime_contract_changed": False,
    },
}
AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(DEFAULT_OUTPUT)
print(EVENT_OUTPUT)
print(AUDIT)
