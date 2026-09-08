"""整理任务附页及纸边修正的真实 Godot 证据；仅裁切、排版和编码媒体。"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    root = parser.parse_args().root.resolve()
    out = root / 'docs/screenshots/2026-09-08-world-map-task-polish-v5'
    checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
    assert checks['全部通过'] and checks['运行环境'] == 'Windows'
    assert len(checks['检查']) == 68 and all(item['通过'] for item in checks['检查'])
    names = [
        ('01-live-default.png', '正式三地区默认状态：任务附页与紧凑任务组'),
        ('10-task-collapsed.png', '真实点击收起：纸面减高，照片与进入按钮固定'),
        ('11-task-reopened.png', '真实点击重新展开'),
        ('02-live-locked.png', '正式锁定状态：条件完整，无无效折叠热区'),
        ('03-live-open-empty.png', '开放空态：可进入，但没有任务与折叠入口'),
        ('12-live-chain-after-expiry.png', '按现有规则构造的限时到期与追踪状态'),
        ('13-long-content-layout-fixture.png', '极端长内容压力样本：完整两行文本，图片缩为容量兜底'),
        ('04-capacity-ten-top.png', '十地区容量样本：顶部'),
        ('05-capacity-ten-bottom.png', '十地区容量样本：滚轮到底'),
        ('06-capacity-long-name-missing-art.png', '长地区名、锁定与缺图容量样本'),
        ('07-hover-focus-not-selection.png', '焦点与当前选中分离'),
        ('08-capacity-four-top.png', '四地区最小溢出'),
        ('09-drag-ten-bottom.png', '真实滚动条拖动到底'),
        ('15-desktop-1280x720.png', '1280×720 桌面窗口等比显示，非移动版'),
    ]
    images = {name: Image.open(out / name).convert('RGB') for name, _ in names}
    for name, im in images.items():
        assert im.size == ((1280, 720) if name.startswith('15-') else (1920, 1080))
    sequence = [images[name] for name in ('01-live-default.png', '10-task-collapsed.png', '11-task-reopened.png')]
    for frame in sequence[1:]:
        for box in [(1296, 210, 1746, 463), (1278, 914, 1828, 990), (0, 932, 590, 1080)]:
            assert ImageChops.difference(sequence[0].crop(box), frame.crop(box)).getbbox() is None
    frames = [im.crop((1220, 592, 1890, 1038)) for im in sequence]
    palette_board = Image.new('RGB', (670, 446 * 3))
    for i, frame in enumerate(frames):
        palette_board.paste(frame, (0, 446 * i))
    palette = palette_board.quantize(colors=256)
    encoded = [im.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for im in frames]
    encoded[0].save(out / 'task-disclosure.gif', save_all=True, append_images=encoded[1:], duration=[1800]*3, loop=0, disposal=1, optimize=True)
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 23)
    old = Image.open(root / 'docs/screenshots/2026-09-08-world-map-task-readability/01-live-default.png').convert('RGB')
    comparison = Image.new('RGB', (1380, 1040), '#122a2e')
    draw = ImageDraw.Draw(comparison)
    for col, (im, label) in enumerate([(old, '修改前 · A362 实际运行'), (sequence[0], '修改后 · 任务附页与纸边修正')]):
        draw.text((col * 690 + 18, 15), label, font=font, fill='#eee4d3')
        comparison.paste(im.crop((1220, 60, 1910, 1040)), (col * 690, 60))
    comparison.save(out / 'task-comparison.png')

    before = Image.open(out / '14-edge-sampling-before.png').convert('RGB')
    after = sequence[0]
    edges = Image.new('RGB', (1320, 720), '#122a2e')
    draw = ImageDraw.Draw(edges)
    for col, im in enumerate([before, after]):
        draw.text((col * 660 + 16, 12), ['原采样 · 3 倍像素放大', '修正后 · 3 倍像素放大'][col], font=font, fill='#eee4d3')
        for row, box in enumerate([(35,165,255,235),(652,541,872,611),(1230,60,1450,130)]):
            edges.paste(im.crop(box).resize((660,210), Image.Resampling.NEAREST), (col * 660, 50 + row * 220))
            assert ImageChops.difference(before.crop(box), after.crop(box)).getbbox() is not None
    edges.save(out / 'paper-edge-comparison.png')
    for box in [(1360,235,1660,420),(1665,485,1800,535),(120,250,280,330)]:
        assert ImageChops.difference(before.crop(box), after.crop(box)).getbbox() is None, '主体或完整纸面不应被边缘修正模糊'
    asset_dir = root / 'gd_project/Assets/ui/angus_packaging/world_map/soft_columns_v1'
    source_manifest = json.loads((asset_dir / 'asset-sources.json').read_text(encoding='utf-8'))
    alpha_report = []
    for record in source_manifest['纸件']:
        if record['文件'] == 'wmw-brand.png':
            continue
        path = asset_dir / record['文件']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], '原始纸件发生了未登记修改'
        alpha = np.array(Image.open(path).convert('RGBA'))[:, :, 3]
        assert list(np.unique(alpha)) == [0, 255]
        alpha_report.append({'文件': path.name, '透明度级数': 2, '半透明边缘像素': 0, '原PNG摘要与原来源记录一致': True})
    (out / 'paper-edge-diagnosis.json').write_text(json.dumps({
        '原纸件': alpha_report,
        '原因': ['旧透明背景提取把轮廓变成0/255二值透明度', '倾斜照片是无透明留边矩形，其几何边界没有覆盖率过渡'],
        '修复': 'Godot 局部纸件材质混合边缘覆盖率；透明颜色按预乘方式加权避免底色污染。倾斜照片仅在四边约一像素补几何覆盖率。',
        '范围': '原PNG、文字、插画主体及全局渲染设置未改。完整纸面与插画内部抽样块在同场景前后逐像素一致。',
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    shutil.copyfile(root / 'tmp/task-polish-runtime.log', out / 'runtime.log')
    assert 'SOFT_COLUMNS_RESULT true checks=68' in (out / 'runtime.log').read_text(encoding='utf-8')
    gallery = '\n\n'.join(f'## {title}\n\n![{title}](./{name})' for name, title in names)
    (out / 'index.md').write_text('''# 任务附页与纸边修正 · 正式 Godot 实际运行

A364：用户授权按父级方案实施，并检查纸边锯齿。68/68 图形运行检查通过，退出码 0。当前结果待用户审阅观感。

任务名、类型与耗时按实际行数成组；单张浅矿物青附页与小标题签保留任务识别；折叠收短纸面，照片及进入按钮固定。锁定／空态移除无效折叠入口。正常右图为450宽，仍与左卡、地图证据共用同一个 Texture2D。

![同尺度前后对照](./task-comparison.png)

## 展开与收起

![真实点击后的运行画面](./task-disclosure.gif)

三帧来自真实鼠标点击后的 Godot 渲染，折叠为即时变化。程序仅裁切与延长每态停留至1.8秒，没有生成补帧，不声称原速录屏。照片、进入按钮和日程在三帧逐像素不变，分类和提醒保留。

## 纸边与倾斜照片边缘

![同场景开关抗锯齿的对照](./paper-edge-comparison.png)

同一场景只切换边缘修正后抓取，三倍最近邻放大以展示原始像素，不是正常观看比例。六类纸件原PNG均只有0/255透明度，旧提取缺少过渡；中央倾斜照片另有矩形几何边界锯齿。修正仅作用于Godot局部材质，原PNG与插画主体未修改；大尺度手绘纸形仍保留。详见 [边缘诊断](./paper-edge-diagnosis.json)。

## 验证边界

- 正式内容仍为三个地区。四／十地区、长名称和缺图是容量样本。
- 最长新闻、提醒和两条长任务名同时出现时，右图会完整等比缩至约266宽。它是极端容量兜底，文字完整但构图弱于常态；不记作与常态同等美术通过。正式内容若常触发该尺寸，应继续调整内容容量。
- 本次执行既有32步选中补间与25步滚动输入回归，未重新保存这两类动画。1280×720 为桌面16:9缩放检查，不是移动版。
- UI Designer 与 UX 老哥确认正常任务分组、识别及纸件关系改善，并指出内边距及空态入口问题；本版已增加纸面内边距、隐藏空态折叠热区。内部复核不替代用户视觉认可。
- v1 至 v4 为过程样本：v1 纸件留边不合适；v2/v3 仍有收尾项；v4 的缩放断言误把物理窗口像素与逻辑坐标比较。当前以 v5 为最终证据，未覆盖旧图。

''' + gallery + '\n\n[68 项检查](./checks.json) · [运行日志](./runtime.log)\n', encoding='utf-8')
    artifacts = [name for name, _ in names] + ['14-edge-sampling-before.png', 'task-disclosure.gif', 'task-comparison.png', 'paper-edge-comparison.png', 'paper-edge-diagnosis.json', 'checks.json', 'runtime.log']
    (out / 'evidence-manifest.json').write_text(json.dumps({
        '状态': '已实施并完成运行验证，待用户审阅', '检查数': 68, '真实展开收起帧数': 3,
        'sha256': {name: hashlib.sha256((out / name).read_bytes()).hexdigest() for name in artifacts},
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'runtime_checks':68,'screenshots':15,'gif_frames':Image.open(out/'task-disclosure.gif').n_frames,'binary_alpha_assets':len(alpha_report)}))


if __name__ == '__main__':
    main()
