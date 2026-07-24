from __future__ import annotations

import os
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parent
os.environ["WMW_A263_VARIANT"] = "v0.3"
runpy.run_path(str(ROOT / "render_wmw_a263_uncoated_fullscreen_text_landing_v0_2.py"), run_name="__main__")
