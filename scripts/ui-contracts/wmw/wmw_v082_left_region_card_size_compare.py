from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"
MODULE_PATH = ROOT / "tmp/wmw_v082_left_region_card_reinsert.py"

OUT_PROOF_160 = BASE / "355-world-map-wmw-v0-8-2-left-card-uniform-160-reinsert-proof.png"
OUT_QA_160 = BASE / "356-world-map-wmw-v0-8-2-left-card-uniform-160-reinsert-qa.png"
OUT_COMPARE = BASE / "357-world-map-wmw-v0-8-2-left-card-150-vs-160-comparison.png"
OUT_MANIFEST = BASE / "358-world-map-wmw-v0-8-2-left-card-size-comparison-manifest.json"


def load_module():
    spec = importlib.util.spec_from_file_location("wmw_v082_reinsert", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load module")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def set_contract_160(mod) -> None:
    mod.CARD.update(
        {
            "export_size": [204, 160],
            "positions": [[44, 24], [44, 196], [44, 368], [44, 540]],
            "photo_slot": [21, 24, 174, 64],
            "label_plate": [22, 104, 114, 32],
            "meta_line": [22, 138, 104, 10],
            "action_badge": [158, 106, 38, 38],
            "stack_gap": 12,
        }
    )


def save_160_outputs(mod):
    proof, rects = mod.create_full(qa=False)
    proof.save(OUT_PROOF_160)
    qa, _ = mod.create_full(qa=True)
    qa.save(OUT_QA_160)
    return proof, qa, rects


def create_comparison(mod, proof_160: Image.Image) -> None:
    proof_150 = Image.open(BASE / "351-world-map-wmw-v0-8-2-left-card-uniform-reinsert-proof.png").convert("RGB")
    left_150 = proof_150.crop((20, 0, 280, 720))
    left_160 = proof_160.crop((20, 0, 280, 720))
    canvas = Image.new("RGB", (900, 920), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((32, 24), "v0.8.2 Left Card Size Comparison", font=mod.FB, fill=(244, 240, 212))
    draw.text((32, 58), "A: 204x150 fits, but feels shorter / looser.  B: 204x160 keeps a stronger card rhythm and more photo height.", font=mod.F_SMALL, fill=(222, 230, 204))
    draw.text((70, 96), "A 204x150", font=mod.FB, fill=(228, 226, 190))
    draw.text((455, 96), "B 204x160 recommended", font=mod.FB, fill=(180, 246, 190))
    canvas.paste(left_150, (50, 130))
    canvas.paste(left_160, (435, 130))
    draw.rectangle([50, 130, 310, 850], outline=(230, 194, 84), width=2)
    draw.rectangle([435, 130, 695, 850], outline=(102, 246, 142), width=2)
    notes = [
        "Recommendation: use 204x160 as the next contract candidate before clean-sprite brief.",
        "Reason: four cards still fit inside the left column; stack bottom is y=700 at 1280x720.",
        "The photo slot becomes 174x64 instead of 174x58, reducing the source-image crop pressure.",
        "This is still a geometry / fit proof, not final art quality.",
    ]
    for i, line in enumerate(notes):
        draw.text((32, 864 + i * 14), line, font=mod.F_SMALL, fill=(232, 232, 210))
    canvas.save(OUT_COMPARE)


def write_manifest(rects) -> None:
    data = {
        "artifact": "WMW v0.8.2 left_region_card size comparison",
        "date": "2026-07-07",
        "artifact_type": "contract_fit_comparison / not final art / not atlas",
        "outputs": {
            "proof_150": str(BASE / "351-world-map-wmw-v0-8-2-left-card-uniform-reinsert-proof.png"),
            "proof_160": str(OUT_PROOF_160),
            "qa_160": str(OUT_QA_160),
            "comparison": str(OUT_COMPARE),
            "manifest": str(OUT_MANIFEST),
        },
        "candidate_a": {
            "export_size": [204, 150],
            "photo_slot": [174, 58],
            "positions": [[44, 24], [44, 197], [44, 370], [44, 543]],
            "assessment": "passes fit, but left cards read shorter / looser and first two photos have more crop pressure",
        },
        "candidate_b": {
            "export_size": [204, 160],
            "photo_slot": [174, 64],
            "positions": [[44, 24], [44, 196], [44, 368], [44, 540]],
            "assessment": "recommended next contract candidate; four cards still fit, photo slot is less shallow",
        },
        "rects_160": rects,
        "decision_needed": "User review whether to revise left_region_card contract from 204x150 to 204x160 before v0.8.2 clean sprite brief.",
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    mod = load_module()
    set_contract_160(mod)
    proof_160, _, rects = save_160_outputs(mod)
    create_comparison(mod, proof_160)
    write_manifest(rects)
    print(OUT_PROOF_160)
    print(OUT_QA_160)
    print(OUT_COMPARE)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
