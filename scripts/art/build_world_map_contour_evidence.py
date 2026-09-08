"""整理真实Godot长边对照；只裁切、排版和核验截图，不绘制游戏美术。"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    root = parser.parse_args().root
    out = root / 'docs/screenshots/2026-09-08-world-map-contour-v2'
    focused = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
    regression = json.loads((out / 'regression/checks.json').read_text(encoding='utf-8'))
    assert focused['全部通过'] and len(focused['检查']) == 11
    assert regression['全部通过'] and len(regression['检查']) == 68
    report = []
    for w, h in [(1920, 1080), (1600, 900), (1280, 720)]:
        before = np.array(Image.open(out / f'{w}x{h}-before.png').convert('RGB'))
        after = np.array(Image.open(out / f'{w}x{h}-after.png').convert('RGB'))
        assert before.shape == after.shape == (h, w, 3)
        changed = np.any(before != after, axis=2)
        yy, xx = np.nonzero(changed)
        assert len(xx) > 0
        scale = w / 1920
        assert xx.min() >= int(1210 * scale) and xx.max() <= int(1270 * scale)
        assert yy.min() >= int(99 * scale) and yy.max() <= int(1020 * scale)
        report.append({'显示尺寸': [w, h], '变化像素数': len(xx), '变化包围盒': [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)], '两条左边缘以外逐像素一致': True})
    asset_dir = root / 'gd_project/Assets/ui/angus_packaging/world_map/soft_columns_v1'
    source_records = json.loads((asset_dir / 'asset-sources.json').read_text(encoding='utf-8'))['纸件']
    for record in source_records:
        assert hashlib.sha256((asset_dir / record['文件']).read_bytes()).hexdigest() == record['sha256']
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 21)
    board = Image.new('RGB', (1020, 750), '#142c30')
    draw = ImageDraw.Draw(board)
    for col, state in enumerate(['before', 'after']):
        im = Image.open(out / f'1920x1080-{state}.png')
        label = ['修改前：上轮局部柔化', '修改后：连续轮廓'][col]
        draw.text((col * 510 + 12, 10), label + ' · 3倍像素放大', font=font, fill='#eee4d3')
        for row, y in enumerate([220, 720]):
            crop = im.crop((1210, y, 1380, y + 110))
            board.paste(crop.resize((510, 330), Image.Resampling.NEAREST), (col * 510, 45 + row * 345))
    board.save(out / 'left-edge-comparison.png')
    (out / 'pixel-checks.json').write_text(json.dumps({'实图像素核对': report, '原纸件SHA全部保留': True, '范围': '只针对右侧底纸左长边；不能外推为整页所有纸件零锯齿。'}, ensure_ascii=False, indent=2), encoding='utf-8')
    for source, target in [('contour-v2.log', 'runtime.log'), ('contour-regression.log', 'regression/runtime.log')]:
        shutil.copyfile(root / 'tmp' / source, out / target)
        log = (out / target).read_text(encoding='utf-8')
        assert not any(error in log for error in ['SCRIPT ERROR', 'ERROR:', 'WARNING:'])
    gallery = '\n\n'.join(f'## {w}×{h} 实际运行\n\n![{w}×{h}](./{w}x{h}-after.png)\n\n[同尺寸修改前](./{w}x{h}-before.png)' for w, h in [(1920,1080),(1600,900),(1280,720)])
    (out / 'index.md').write_text('''# 右侧底纸左长边修正 · 真实运行证据

用户指出箭头处仍有锯齿后，按其“继续”授权实施。当前为已接入Godot、待用户审阅实际观感。

这次将蓝衬纸外缘和白纸内缘重建为连续轮廓，边缘覆盖率按屏幕像素控制。原PNG、纸纹主体、三处新闻图、文字和交互布局保留；局部交界的取色绕过旧描边，避免留下深色短线。曲线数据由Godot读取原图后计算并缓存，不生成替代美术图。

两条左长边以外，三种尺寸的修改前后截图逐像素一致。原纸件SHA全部一致。11项针对性运行检查、68项原功能回归通过；这不等于用户已确认美术，也不代表所有纸件轮廓均已修正。

![箭头附近上、下两段真实对照，3倍最近邻放大用于看像素](./left-edge-comparison.png)

本轮只修这张代表件的左长边，顶部夹具、角部和其他纸件沿用既有处理。没有新增动效；下列图是三个真实窗口尺寸，未将1080p截图缩小冒充900p或720p运行。

'''+gallery+'''

## 检查与过程身份

- [11项针对性检查](./checks.json)、[68项功能回归](./regression/checks.json)、[实图像素范围](./pixel-checks.json)。
- v1为过程样本：边缘取色曾带出旧描边；截图尺寸断言误用了逻辑纹理尺寸。v2修正取色，并以GPU读回图的实际像素检查尺寸。
- 修改前是同一场景关闭连续轮廓、保留上轮局部柔化的状态；不是关闭所有抗锯齿的更差基线。
''', encoding='utf-8')
    hashes = {str(p.relative_to(out)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.name != 'evidence-manifest.json'}
    (out / 'evidence-manifest.json').write_text(json.dumps({'状态': '已实施，待用户视觉审阅', '针对性检查': 11, '回归检查': 68, 'sha256': hashes}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'focused': 11, 'regression': 68, 'pixel_checks': report}, ensure_ascii=False))


if __name__ == '__main__':
    main()
