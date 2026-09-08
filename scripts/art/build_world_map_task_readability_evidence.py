"""整理 A362 的真实 Godot 截图；程序仅裁切、排版与编码媒体。"""
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
    out = root / 'docs/screenshots/2026-09-08-world-map-task-readability'
    checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
    assert checks['全部通过'] and checks['运行环境'] == 'Windows'
    assert checks['任务专项'] and len(checks['检查']) == 57
    assert all(item['通过'] for item in checks['检查'])
    assert checks['滚动输入步数'] == 25 and checks['滚动抽帧数'] == 0
    names = [
        ('01-live-default.png', '真实初始状态：任务分类、限时提醒及本周剩余天数'),
        ('10-task-collapsed.png', '真实点击收起：分类与提醒保留，进入按钮固定'),
        ('11-task-reopened.png', '真实点击重新展开：两条只读预览'),
        ('02-live-locked.png', '真实锁定地区：不泄露任务，保留解锁缺口'),
        ('03-live-open-empty.png', '真实开放空态：任务为零，但地区仍可进入'),
        ('12-live-chain-after-expiry.png', '真实规则的到期刷新：限时归零，青线追踪与剩余三天'),
        ('13-long-content-layout-fixture.png', '长内容布局样本：两行新闻、提醒和任务名，非新增正式剧情'),
        ('04-capacity-ten-top.png', '十地区容量样本：列表顶部'),
        ('05-capacity-ten-bottom.png', '十地区容量样本：滚轮到底'),
        ('06-capacity-long-name-missing-art.png', '长地区名与缺图容量样本'),
        ('07-hover-focus-not-selection.png', '悬停与焦点不替代当前选中'),
        ('08-capacity-four-top.png', '四地区最小溢出容量样本'),
        ('09-drag-ten-bottom.png', '十地区容量样本：真实拖动到底'),
    ]
    images = {name: Image.open(out / name).convert('RGB') for name, _ in names}
    assert all(im.size == (1920, 1080) for im in images.values())
    sequence = [images[name] for name in ('01-live-default.png', '10-task-collapsed.png', '11-task-reopened.png')]
    for frame in sequence[1:]:
        for box in [(1285, 679, 1813, 749), (1270, 926, 1830, 1007), (0, 932, 590, 1080)]:
            assert ImageChops.difference(sequence[0].crop(box), frame.crop(box)).getbbox() is None, '折叠改变了分类、提醒、CTA 或日程'
    assert ImageChops.difference(sequence[0].crop((1280, 750, 1828, 923)), sequence[1].crop((1280, 750, 1828, 923))).getbbox()
    crop = (1230, 610, 1880, 1040)
    frames = [im.crop(crop) for im in sequence]
    palette_board = Image.new('RGB', (650, 430 * 3))
    for i, frame in enumerate(frames):
        palette_board.paste(frame, (0, 430 * i))
    palette = palette_board.quantize(colors=256)
    encoded = [im.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for im in frames]
    encoded[0].save(out / 'task-disclosure.gif', save_all=True, append_images=encoded[1:], duration=[1800, 1800, 1800], loop=0, disposal=1, optimize=True)

    old = Image.open(root / 'docs/screenshots/2026-09-08-world-map-scroll-affordance/01-live-default.png').convert('RGB')
    comparison_crop = (1220, 65, 1910, 1045)
    board = Image.new('RGB', (1380, 1040), '#10292e')
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 25)
    for i, (im, title) in enumerate([(old, '补齐前 · A361 实际运行'), (sequence[0], '补齐后 · A362 实际运行')]):
        draw.text((i * 690 + 18, 15), title, font=font, fill='#efe6d1')
        board.paste(im.crop(comparison_crop), (i * 690, 60))
    board.save(out / 'task-comparison.png')
    shutil.copyfile(root / 'tmp/task-readability-runtime.log', out / 'runtime.log')
    count = len(checks['检查'])
    gallery = '\n\n'.join(f'## {title}\n\n![{title}](./{name})' for name, title in names)
    (out / 'index.md').write_text(f'''# 世界地图任务识别与信息补齐 · Godot 实际运行

A362：用户授权补齐分类、风险说明与剩余天数，允许适当缩小右图，并要求任务与新闻明显区分。已接入正式游戏，{count}/{count} 运行检查通过，退出码 0；本轮任务区的新观感待用户审阅。

右图完整等比缩小，三处仍为同一 Texture2D。任务放在一张浅矿物青纸面上，以深色标题签、类型墨条和耗时区分新闻；任务行只读，进入地区后选择具体任务。

![同尺度前后对照](./task-comparison.png)

## 真实展开与收起

![任务区展开与收起](./task-disclosure.gif)

三帧来自正式 WeeklyRunGame 接收真实鼠标点击后保存的运行画面。折叠为即时切换，没有新增补间；GIF 仅裁切右下并把每个状态停留延长为 1.8 秒，不声称原速录屏。分类、风险提醒、进入按钮和日程在三帧中逐像素一致。

本次也执行了 32 步选中补间和 25 步滚动输入回归，但未保存这两类动画帧；已有 [选中动效](../2026-09-07-world-map-selection/selection.gif) 与 [滚动演示](../2026-09-08-world-map-scroll-affordance/scroll.gif) 保留其原版本身份。

## 内容与验证边界

- 正式内容仍为三个地区；四／十地区、长名称、缺图均为容量测试。
- 开放空态和到期状态由现有游戏数据与规则构造；长新闻和长任务名只注入展示 payload，不写入正式任务库。
- 新闻仍为固定地区来稿；独立推进日、动态新闻及新增正式地区内容不在此次收尾范围。
- UI Designer 与 UX 老哥已看实际截图，未发现阻止交付的问题；内部复核不等于用户最终视觉批准。

''' + gallery + f'\n\n[{count} 项运行检查](./checks.json) · [运行日志](./runtime.log)\n', encoding='utf-8')
    artifacts = [name for name, _ in names] + ['task-disclosure.gif', 'task-comparison.png', 'checks.json', 'runtime.log']
    manifest = {
        '状态': '已落地并完成运行验证，任务区新观感待用户审阅',
        '检查数': count, '展开收起真实状态帧数': 3,
        '分类提醒进入按钮及日程逐帧一致': True,
        '媒体说明': '真实点击后的 Godot 运行画面，程序仅裁切、排版和编码；停留时间延长，无生成补帧。',
        'sha256': {name: hashlib.sha256((out / name).read_bytes()).hexdigest() for name in artifacts},
    }
    (out / 'evidence-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'checks': count, 'disclosure_frames': Image.open(out / 'task-disclosure.gif').n_frames, 'screenshots': len(names)}))


if __name__ == '__main__':
    main()
