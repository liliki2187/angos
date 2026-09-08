"""整理真实 ImageGen 素材；程序只负责裁切、透明背景提取与来源清单。"""
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'image_gen/2026-09-07/world-map-soft-columns-runtime-v1'
DEST = ROOT / 'gd_project/Assets/ui/angus_packaging/world_map/soft_columns_v1'

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    sheet = Image.open(SOURCE / 'paper-sheet.png').convert('RGBA')
    # 模型输出 RGB 棋盘底，实际透明通道由中性色背景提取，不能声称原图自带 alpha。
    arr = np.array(sheet)
    rgb = arr[:, :, :3].astype(np.int16)
    neutral = (rgb.max(axis=2) - rgb.min(axis=2) < 24) & (rgb.min(axis=2) > 105)
    arr[neutral, 3] = 0
    sheet = Image.fromarray(arr)
    boxes = {
        'region-paper': (28, 104, 661, 492),
        'dossier-paper': (676, 72, 1254, 1150),
        'schedule-paper': (26, 529, 669, 729),
        'action-paper': (30, 782, 653, 923),
        'region-tag': (28, 984, 404, 1157),
        'note-paper': (426, 950, 661, 1196),
    }
    records = []
    for name, box in boxes.items():
        img = sheet.crop(box)
        pixels = np.array(img)
        # 衬纸/胶带内部的灰色不是背景；补回封闭的小孔，保持材质连续。
        # fromarray 的共享内存图像必须复制为可写图像，否则 floodfill 会静默失效。
        mask = Image.fromarray(np.pad(pixels[:, :, 3], 1)).copy()
        ImageDraw.floodfill(mask, (0, 0), 128, thresh=0)
        assert mask.getpixel((0, 0)) == 128, f'{name}：外部背景标记失败'
        opaque = np.array(mask)[1:-1, 1:-1] != 128
        pixels[:, :, 3] = opaque.astype(np.uint8) * 255
        transparent_count = int(np.count_nonzero(~opaque))
        assert transparent_count > opaque.size * 0.02, f'{name}：透明背景丢失'
        assert int(np.count_nonzero(opaque)) > opaque.size * 0.35, f'{name}：纸张主体丢失'
        assert not opaque[0, 0], f'{name}：左上角棋盘底残留'
        img = Image.fromarray(pixels)
        img.save(DEST / f'{name}.png')
        records.append({'文件': f'{name}.png', '来源矩形': box, '尺寸': img.size,
                        '透明像素数': transparent_count, '透明通道检查': '通过'})
    for name in ['background', 'us', 'east_asia', 'pacific']:
        shutil.copyfile(SOURCE / f'{name}.png', DEST / f'{name}.png')
    # 从已批准视觉依据提取现有品牌图形，不重新绘制地球标记。
    brand = np.array(Image.open(SOURCE / 'style-reference.png').convert('RGBA').crop((12, 17, 115, 109)))
    rgb_brand = brand[:, :, :3].astype(np.float32)
    brand[:, :, 3] = np.clip((rgb_brand[:, :, 0] - 95) * 255 / 60, 0, 255).astype(np.uint8)
    Image.fromarray(brand).save(DEST / 'wmw-brand.png')
    records.append({'文件': 'wmw-brand.png', '来源矩形': [12, 17, 115, 109], '尺寸': [103, 92]})
    for entry in records:
        entry['sha256'] = hashlib.sha256((DEST / entry['文件']).read_bytes()).hexdigest()
    (DEST / 'asset-sources.json').write_text(json.dumps({
        '版本': 1, '说明': '底图、纸材和新闻图均由真实 ImageGen 生成。裁切和去棋盘底是后处理，不承担美术重绘。',
        '来源目录': str(SOURCE.relative_to(ROOT)).replace('\\', '/'),
        '共享图片': {key: f'{key}.png' for key in ['us', 'east_asia', 'pacific']},
        '纸件': records,
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'已整理 {len(records) + 4} 个运行资产：{DEST}')

if __name__ == '__main__':
    main()
