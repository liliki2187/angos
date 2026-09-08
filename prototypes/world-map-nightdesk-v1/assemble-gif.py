"""把真实录屏解码出的画面组装为便于聊天预览的动图。"""
from pathlib import Path
from PIL import Image

evidence = Path(__file__).parent / "evidence" / "v2"
paths = sorted((evidence / "decoded-frames").glob("*.png"))
if not paths:
    raise RuntimeError("请先运行 decode-video.cjs 解码真实录像")
frames = [Image.open(p).convert("RGB") for p in paths]
palette = frames[0].quantize(colors=256)
indexed = [f.quantize(palette=palette) for f in frames]
target = evidence / "06-interaction-demo.gif"
indexed[0].save(target, save_all=True, append_images=indexed[1:], duration=125, loop=0, optimize=True, disposal=1)
print(f"{len(frames)} 帧，{target.stat().st_size} 字节，{target}")
