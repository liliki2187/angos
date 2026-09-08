"""整理 Godot 选中态实图、真实补间帧和前后对照，不修改界面美术。"""
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
    out = root / 'docs/screenshots/2026-09-07-world-map-selection'
    before = root / 'docs/screenshots/2026-09-07-world-map-soft-columns/01-live-default.png'
    checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
    assert checks['全部通过'] and len(checks['检查']) == 32 and checks['动效帧数'] == 32
    names = [
        ('01-live-default.png', '北美选中：鼠标移开且没有键盘焦点'),
        ('02-live-locked.png', '东亚选中但锁定：选中层完整，进入仍禁用'),
        ('03-live-open-empty.png', '已开放的太平洋：选中与空任务分开表达'),
        ('04-capacity-ten-top.png', '10 地区容量样本：列表顶部'),
        ('05-capacity-ten-bottom.png', '10 地区容量样本：列表底部'),
        ('06-capacity-long-name-missing-art.png', '第十地区选中：长名称、缺图和锁定同时成立'),
        ('07-hover-focus-not-selection.png', '焦点与悬停位于北美，当前选中仍是东亚'),
    ]
    for filename, _ in names:
        assert Image.open(out / filename).size == (1920, 1080)
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 24)
    board = Image.new('RGB', (1920, 596), '#142b30')
    draw = ImageDraw.Draw(board)
    for x, path, title in [(0, before, '修改前 · 细侧线'), (960, out / names[0][0], 'Godot 实际运行 · 蜜黄纸签与衬纸')]:
        draw.text((x + 18, 12), title, font=font, fill='#efe6d1')
        board.paste(Image.open(path).convert('RGB').resize((960, 540), Image.Resampling.LANCZOS), (x, 56))
    board.save(out / 'comparison.png')
    recorded = [Image.open(out / ('motion/%04d.png' % i)).convert('RGB') for i in range(32)]
    # 实帧应存在纸张位移，并在补间结束后稳定；这不代替人对动画的判断。
    movement = []
    for start in [0, 16]:
        bbox = ImageChops.difference(recorded[start], recorded[start + 15]).getbbox()
        assert bbox is not None, '补间帧没有可见变化'
        assert ImageChops.difference(recorded[start + 13], recorded[start + 15]).getbbox() is None, '补间没有在预期时间内落定'
        movement.append(bbox)
    first = Image.open(out / names[0][0]).convert('RGB')
    locked = Image.open(out / names[1][0]).convert('RGB')
    # 从 60fps 固定模拟步长中每两帧取一张，以 30fps 播放。仅静态停留延长。
    sequence = [first] + recorded[0:16:2] + [locked] + recorded[16:32:2] + [first]
    duration = [1100] + [33, 33, 34, 33, 33, 34, 33, 33] + [1300] + [33, 33, 34, 33, 33, 34, 33, 33] + [700]
    palette_board = Image.new('RGB', (640, 720))
    palette_board.paste(first.resize((640, 360)), (0, 0))
    palette_board.paste(locked.resize((640, 360)), (0, 360))
    palette = palette_board.quantize(colors=256)
    encoded = [im.resize((1280, 720), Image.Resampling.LANCZOS).quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for im in sequence]
    encoded[0].save(out / 'selection.gif', save_all=True, append_images=encoded[1:], duration=duration, loop=0, disposal=1, optimize=True)
    assert Image.open(out / 'selection.gif').is_animated
    shutil.copyfile(root / 'tmp/selection-runtime.log', out / 'runtime.log')
    gallery = '\n\n'.join(f'### {title}\n\n![{title}](./{filename})' for filename, title in names)
    (out / 'index.md').write_text('''# 世界地图选中态 · Godot 真实运行

本轮按用户“可以试试”将蜜黄标题纸签、外露衬纸、地图标签和右侧“当前查看”接入正式游戏。图片继续共用原 Texture2D，未重新生成或改变新闻图。

32/32 运行检查通过。测试覆盖鼠标移开与焦点释放、悬停不转移选区、锁定选中、稳定热区、10 地区与图片复用。用户最终视觉评价待定。

## 前后对照

![修改前与实际运行](./comparison.png)

## 切换演示

![真实 Godot 补间帧](./selection.gif)

从 Godot 60fps 固定模拟步长取得真实渲染帧，以 30fps 抽样播放。纸张补间为 160ms，静态停留延长以便观察。初始画面和两次切换均来自真实运行，程序只组装媒体。

''' + gallery + '\n\n[32 项检查](./checks.json) · [证据清单](./evidence-manifest.json)\n', encoding='utf-8')
    artifacts = [file for file, _ in names] + ['comparison.png', 'selection.gif', 'checks.json', 'runtime.log']
    manifest = {
        '状态': '选中态试做完成，运行检查通过，待用户视觉确认',
        '检查数': 32, '补间时长毫秒': 160, '真实帧数': 32, '模拟帧率': 60, '演示帧率': 30,
        '动效变化矩形': movement,
        '说明': '原始截图与补间帧均来自正式 WeeklyRunGame。静态停留延长，补间按模拟时间抽样播放。',
        'sha256': {file: hashlib.sha256((out / file).read_bytes()).hexdigest() for file in artifacts},
    }
    (out / 'evidence-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'gif_frames': Image.open(out / 'selection.gif').n_frames, 'motion_bounds': movement, 'screenshots': len(names), 'checks': 32}, ensure_ascii=True))

if __name__ == '__main__':
    main()
