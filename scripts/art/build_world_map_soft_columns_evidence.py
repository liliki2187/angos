"""整理真实 Godot 截图和抽帧演示；不绘制或替代游戏界面。"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()
    out = root / 'docs/screenshots/2026-09-07-world-map-soft-columns'
    checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
    assert checks['全部通过'] and len(checks['检查']) == 23
    reference = root / 'image_gen/2026-09-07/world-map-a-soft-three-columns-v1/02-filled-soft-three-column-candidate.png'
    shutil.copyfile(reference, out / 'style-reference.png')
    names = [
        ('01-live-default.png', '正式游戏 · 北美默认态'),
        ('02-live-locked.png', '正式游戏 · 锁定地区仍可预览'),
        ('03-live-open-empty.png', '已开放但暂无任务'),
        ('04-capacity-ten-top.png', '10 地区容量样本 · 列表顶部'),
        ('05-capacity-ten-bottom.png', '10 地区容量样本 · 列表底部'),
        ('06-capacity-long-name-missing-art.png', '长名称、缺图与锁定状态'),
    ]
    for filename, _ in names:
        assert Image.open(out / filename).size == (1920, 1080), filename
    # 仅拼接和缩放真实截图，标签在画面之外。
    board = Image.new('RGB', (1920, 600), '#142b30')
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 22)
    draw = ImageDraw.Draw(board)
    for x, filename, title in [(0, 'style-reference.png', 'A357 风格候选'), (960, names[0][0], 'A359 Godot 实际运行')]:
        draw.text((x + 20, 14), title, font=font, fill='#f4eddc')
        im = Image.open(out / filename).convert('RGB').resize((960, 540), Image.Resampling.LANCZOS)
        board.paste(im, (x, 60))
    board.save(out / 'comparison.png')
    # 静态状态抽帧停留略延长，滚轮保持帧序；不宣称是原速录屏。
    frame_paths = sorted((out / 'frames').glob('*.png'))
    assert len(frame_paths) == 29
    frames = [Image.open(p).convert('RGB').resize((1280, 720), Image.Resampling.LANCZOS) for p in frame_paths]
    palette_board = Image.new('RGB', (640, 360 * 3))
    for i, index in enumerate([0, 5, 28]):
        palette_board.paste(frames[index].resize((640, 360)), (0, i * 360))
    palette = palette_board.quantize(colors=256)
    gif = [frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for frame in frames]
    durations = [400] * 10 + [330] * 3 + [350] * 4 + [180] * 11 + [1200]
    gif[0].save(out / 'interaction.gif', save_all=True, append_images=gif[1:], duration=durations, loop=0, optimize=True, disposal=1)
    assert Image.open(out / 'interaction.gif').is_animated
    gallery = ''.join(f'<figure><a href="{file}"><img src="{file}" loading="lazy" alt="{label}"></a><figcaption>{label} · 点击查看 1920×1080 原图</figcaption></figure>' for file, label in names)
    check_rows = ''.join(f'<li>✓ {item["检查"]}</li>' for item in checks['检查'])
    html = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Angus 世界地图 · Godot 落地对照</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#11272d;color:#f4eddf;font:17px/1.7 "Microsoft YaHei",sans-serif;min-width:1100px}main{max-width:1700px;margin:0 auto;padding:36px 42px 80px}h1{font-size:32px;margin:0 0 12px}h2{font-size:24px;margin:36px 0 12px}p{max-width:1100px;color:#cad5cf}a{color:#efd17b}button{font:inherit;background:#dec060;border:0;padding:8px 18px;cursor:pointer;color:#11272d}button[aria-pressed="false"]{background:#55777a;color:white}nav{display:flex;gap:10px;margin:18px 0}.compare{position:relative;aspect-ratio:16/9;overflow:hidden}.compare img{position:absolute;width:100%;height:100%;inset:0}.compare #reference{clip-path:inset(0 50% 0 0)}.compare #divider{position:absolute;left:50%;height:100%;border-left:2px solid #f4cf60}label{display:flex;gap:16px;align-items:center;margin:10px 0}input{flex:1}figure{margin:0 0 20px}img{display:block;width:100%;height:auto}figcaption{padding:9px 0;color:#d5dfd5}.gallery{display:grid;grid-template-columns:1fr 1fr;gap:22px}details{border-top:1px solid #55777a;padding-top:15px}li{margin-bottom:4px}.tag{color:#f4cf60}.demo{max-width:1280px}small{color:#aebeb7}
</style><main><h1>世界地图已接入正式 Godot 周循环</h1><p>墨青地图、宽块面插画、暖白纸件、蜜黄入口与手写批注按 A357 三栏候选转译。下方运行画面均从真实 Godot 场景获取；功能检查通过，最终美术观感待用户确认。</p>
<p class="tag">23 / 23 运行检查通过 · 三处共用同一纹理 · 10 地区容量验证 · 1920×1080 桌面</p>
<h2>风格候选与实际运行</h2><p>拖动分界线：左侧为候选、右侧为运行截图；也可单独切换。两图统一显示尺度，候选本身并非运行证据。</p>
<nav><button id="split" aria-pressed="true">并置对照</button><button id="target" aria-pressed="false">仅看风格候选</button><button id="live" aria-pressed="false">仅看实际运行</button><a href="comparison.png">打开左右并排图</a></nav>
<div class="compare"><img src="01-live-default.png" alt="真实 Godot 默认态"><img id="reference" src="style-reference.png" alt="A357 风格候选"><div id="divider"></div></div><label>风格候选<input id="slider" type="range" min="0" max="100" value="50" aria-label="候选图显示比例">实际运行</label>
<h2>真实运行交互抽帧</h2><p>演示地区切换、任务折叠与 10 地区滚轮浏览。来自真实输入后的 viewport 帧，停留时间经过调整，便于查看，并非原速录屏。第 4—10 地区仅为容量样本，不是新增游戏内容。</p><img class="demo" src="interaction.gif" alt="Godot 真实交互抽帧演示">
<h2>各状态完整截图</h2><div class="gallery">GALLERY</div>
<h2>实现与验证记录</h2><p>左卡、右栏和地图附图使用同一 Texture2D，完整等比显示。任务读取正式节点；地区锁定、已开放空态和缺图分别处理。列表滚动不带走日程，任务折叠不移动进入按钮。</p>
<p>未来新增正式地区仍需配置新闻、母图和地图位置；目前有正式内容的地区为三处。当前截图已验证 Windows 中文字体，其他平台字体显示尚未复测。</p>
<p><a href="../../plans/world-map-benchmark-landing/2026-09-07-soft-columns-landing.md">完整排查与落地说明</a> · <a href="checks.json">23 项检查原始记录</a> · <a href="evidence-manifest.json">证据清单</a></p>
<details><summary>展开 23 项运行检查</summary><ul>CHECKS</ul></details><p><small>Godot 4.6.2 · Windows / OpenGL 3.3 · 运行检查退出码 0。导入器最终退出码 0，但仍报告退出时 8 个资源占用；来源未定位，单独记录，不混入“全项目无告警”的说法。</small></p></main>
<script>
const slider=document.getElementById('slider'),ref=document.getElementById('reference'),line=document.getElementById('divider');function show(p,active){ref.style.clipPath=`inset(0 ${100-p}% 0 0)`;line.style.left=p+'%';line.style.display=(p>0&&p<100)?'block':'none';slider.value=p;for(const id of ['split','target','live'])document.getElementById(id).setAttribute('aria-pressed',id===active)}slider.addEventListener('input',()=>show(Number(slider.value),'split'));document.getElementById('split').onclick=()=>show(50,'split');document.getElementById('target').onclick=()=>show(100,'target');document.getElementById('live').onclick=()=>show(0,'live');
</script></html>'''.replace('GALLERY', gallery).replace('CHECKS', check_rows)
    (out / 'index.html').write_text(html, encoding='utf-8')
    for source, filename in [(root / 'tmp/soft-columns-runtime.log', 'runtime.log'), (root / 'tmp/soft-columns-import-final.log', 'import.log')]:
        shutil.copyfile(source, out / filename)
    relevant = [file for file, _ in names] + ['comparison.png', 'interaction.gif', 'checks.json', 'runtime.log', 'import.log', 'style-reference.png']
    manifest = {
        '状态': '正式接入与运行验证完成，待用户视觉确认',
        '截图来源': 'capture_world_map_soft_columns.gd：正式 WeeklyRunGame 场景、真实输入事件、RenderingServer viewport',
        '动图说明': '真实运行抽帧，调整停留时长，不是原速录屏',
        '检查通过': len(checks['检查']),
        '文件': {file: hashlib.sha256((out / file).read_bytes()).hexdigest() for file in relevant},
    }
    (out / 'evidence-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'截图': len(names), '原始帧': len(frames), 'GIF字节数': (out/'interaction.gif').stat().st_size, '输出': str(out)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
