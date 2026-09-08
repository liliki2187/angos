"""整理真实 Godot 滚动截图与输入抽帧；只裁图、排版和编码媒体。"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
from PIL import Image, ImageChops, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    root = parser.parse_args().root.resolve()
    out = root / 'docs/screenshots/2026-09-08-world-map-scroll-affordance'
    checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
    assert checks['全部通过'] and checks['运行环境'] != 'headless'
    assert checks['滚动专项'] and checks['滚动抽帧数'] == 25
    names = [
        ('01-live-default.png', '真实三地区：完整放下，不显示滚动提示'),
        ('08-capacity-four-top.png', '四地区容量样本：露出下一张标题，纸尺和更多提示可见'),
        ('04-capacity-ten-top.png', '十地区容量样本：列表顶部'),
        ('09-drag-ten-bottom.png', '真实拖动到列表底部：更多提示消失，日程保持固定'),
        ('05-capacity-ten-bottom.png', '真实滚轮到列表底部'),
        ('06-capacity-long-name-missing-art.png', '第十地区长名称、缺图与锁定选中'),
        ('02-live-locked.png', '真实东亚锁定选中'),
        ('03-live-open-empty.png', '真实太平洋开放但暂无任务'),
        ('07-hover-focus-not-selection.png', '悬停与焦点不替代当前选中地区'),
    ]
    for name, _ in names:
        assert Image.open(out / name).size == (1920, 1080)
    recorded = [Image.open(out / f'scroll/{i:04d}.png').convert('RGB') for i in range(25)]
    assert ImageChops.difference(recorded[0], recorded[-1]).getbbox() is not None
    for frame in recorded:
        assert ImageChops.difference(recorded[0].crop((0, 932, 590, 1080)), frame.crop((0, 932, 590, 1080))).getbbox() is None, '滚动时日程画面发生变化'
        assert ImageChops.difference(recorded[0].crop((600, 0, 1920, 1080)), frame.crop((600, 0, 1920, 1080))).getbbox() is None, '拖动改变了地图或右侧内容'
    crop = (0, 110, 600, 1080)
    sequence = [Image.open(out / '04-capacity-ten-top.png').convert('RGB')] + recorded + [Image.open(out / '09-drag-ten-bottom.png').convert('RGB')]
    sequence = [frame.crop(crop) for frame in sequence]
    palette_board = Image.new('RGB', (600, 1940))
    palette_board.paste(sequence[0], (0, 0))
    palette_board.paste(sequence[-1], (0, 970))
    palette = palette_board.quantize(colors=256)
    encoded = [frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for frame in sequence]
    encoded[0].save(out / 'scroll.gif', save_all=True, append_images=encoded[1:], duration=[900] + [80] * 25 + [1200], loop=0, disposal=1, optimize=True)
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 22)
    board = Image.new('RGB', (1800, 1020), '#10292e')
    draw = ImageDraw.Draw(board)
    for i, (name, title) in enumerate([
        ('01-live-default.png', '真实三地区 · 无溢出提示'),
        ('08-capacity-four-top.png', '四地区样本 · 下一张标题露出'),
        ('09-drag-ten-bottom.png', '十地区样本 · 拖到底后提示消失'),
    ]):
        draw.text((i * 600 + 16, 12), title, font=font, fill='#efe6d1')
        board.paste(Image.open(out / name).convert('RGB').crop(crop), (i * 600, 50))
    board.save(out / 'scroll-states.png')
    shutil.copyfile(root / 'tmp/scroll-affordance-runtime.log', out / 'runtime.log')
    count = len(checks['检查'])
    gallery = '\n\n'.join(f'## {title}\n\n![{title}](./{name})' for name, title in names)
    (out / 'index.md').write_text(f'''# 世界地图左栏滚动提示 · Godot 实际运行

A361：用户同意用下一张卡片露头、纸尺滚动条及条件式“更多地区”提示增强可滚动感。日程固定，图片规格和三处 Texture2D 复用保留。当前结果待用户审阅。

{count}/{count} 运行检查通过。正式游戏仍有三个地区；第 4—10 地区只为容量测试，缺图与长名称是测试状态，不是新增正式内容。

![三种实际运行状态](./scroll-states.png)

## 真实拖动演示

![原生滚动条拖动抽帧](./scroll.gif)

25 张帧来自正式 WeeklyRunGame 对真实鼠标输入事件的渲染结果。媒体仅裁切左栏并延长停留，拖动抽帧统一以 80ms 展示，不声称原速录屏。日程及中央、右侧在所有拖动帧中逐像素保持不变。

''' + gallery + f'\n\n[{count} 项检查](./checks.json) · [运行日志](./runtime.log)\n', encoding='utf-8')
    artifacts = [name for name, _ in names] + ['scroll.gif', 'scroll-states.png', 'checks.json', 'runtime.log']
    manifest = {
        '状态': '已落地并完成运行验证，待用户观感确认',
        '检查数': count, '真实滚动帧数': 25,
        '日程及地图右侧逐帧保持不变': True,
        '媒体说明': '真实渲染抽帧，程序仅裁切、排版和编码；播放时间经过调整。',
        'sha256': {name: hashlib.sha256((out / name).read_bytes()).hexdigest() for name in artifacts},
    }
    (out / 'evidence-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'checks': count, 'gif_frames': Image.open(out / 'scroll.gif').n_frames, 'screenshots': len(names)}))


if __name__ == '__main__':
    main()
