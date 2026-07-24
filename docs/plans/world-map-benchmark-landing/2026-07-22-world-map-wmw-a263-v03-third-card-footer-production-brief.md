# WMW A263 v0.3 第三卡 footer 修复制作说明

## 目标与范围

只关闭 v0.2 第三卡灰靛“锁定”状态签右端帽被裁掉的问题。冻结第三卡 footer `[49,744,367,52]`、其它两张地区卡、日程、中央地图、右栏、图片、配色与全部功能语义；不改 Godot、runtime、atlas、正式合同、frozen compact A5.1、B2.12 或 GDD。

## 制作方式

- **美术职责**：built-in imagegen 对 v0.2 第三卡 ingredient 做定向编辑，只把过长灰靛签体改为紧凑闭合双端帽，保留无涂布象牙纸、浅暮靛、低多边形照片、边框和阴影。
- **程序职责**：从新 ingredient 裁取 `848×120` source crop，通过 `direct_resize` 映入 `367×52`；恢复真实中文，生成默认 / 确认双态、流程板、100%/200%/400% QA 与 audit。程序不重绘状态签材质。
- **禁止方式**：不右移旧 v0.2 crop，不继续使用 `ImageOps.fit(center, cover)`，不扩大卡片或日程，不用纯色矩形补端帽。

## 最终 imagegen prompt

```text
Use case: precise-object-edit
Asset type: localized no-text WMW desktop game UI ingredient for the third region-card footer
Input image: the provided image is the edit target and style/material reference.
Primary request: preserve the complete image, photography, frame, navy board, warm uncoated ivory paper, shadows, low-poly editorial texture, and all existing geometry. Change only the blank slate-indigo status tag on the bottom-right of the ivory footer.
Required edit: replace the overly long tag with a compact, fully closed status tag approximately 2.4:1 to 2.7:1 width-to-height. Keep both clipped-corner endcaps fully visible. Place it completely inside the ivory footer, with generous clean ivory margin on its right side and above/below. It must look like a deliberate small read-only status label, not a long button and not a cropped strip. Leave a large empty ivory title area to its left.
Text: no text, no glyphs, no symbols, no watermark.
Constraints: change only the bottom-right blank status tag; preserve every other visual feature as closely as possible. The tag must not touch any image boundary, footer boundary, or frame boundary. No new UI elements, no extra labels, no stretching, no perspective change, no color regrade.
```

## 通过条件

- protected object 保留率至少 `99%`，实际为 `100%`；
- 四向 crop loss 均为 `0`；
- 最终右 / 上 / 下边距至少 `8 / 4 / 4px`，实际为 `8.22 / 8.67 / 5.2px`；
- 左右端帽完整、轮廓闭合；
- 标题到签体至少 `16px`，实际 `99.25px`；
- 文字相对实际可见色域中心每轴误差不超过 `4px`，实际 `(0.49,2.77px)`；
- v0.3 相对 v0.2 只改变第三卡 footer；默认 / 确认差分仍只在日程允许区。

