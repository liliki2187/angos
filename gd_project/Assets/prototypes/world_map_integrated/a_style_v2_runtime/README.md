# 世界地图 A 风格运行切片资源

本目录保存世界地图 A 风格在真实 Godot 功能层中的纵向切片资源。

- `north_america_story_1104x704.png`：北美禁区带唯一 `69:44` 新闻母图；左卡 `138×88` 与右档案 `414×264` 引用同一 `Texture2D.resource_path`。
- `east_asia_story_1104x704.png`：东亚神秘地带唯一 `69:44` 新闻母图；以“阶梯式观测建筑穿过圆月”为单一异常关系。
- `pacific_story_1104x704.png`：太平洋失航带唯一 `69:44` 新闻母图；以“倾斜民用监听碟装着水平海面”为单一异常关系。
- `world_map_board_960x902.png`：中央无字世界地图板；运行时地区 beacon、文字、选中圈与反馈均叠在其上。
- `paper_*_512.png`：暖纸、锁定纸、橄榄票据和钢蓝背纸四张无字材质；只承载表面色块与轻纸纹，不承载动态文字或状态。
- 当前身份：`runtime_state_preview`，不等于生产美术母版。
- 图像内容由 built-in imagegen 生成；`scripts/ui-contracts/wmw/prepare_world_map_a_runtime_assets.py` 只做中心裁切和尺寸归一化，不重画内容。
- 动态中文、状态、选中反馈、锁定反馈、热区与焦点全部由 Godot 原生层承担，不烘焙进位图。

生成模式：参考图驱动的独立无字新闻母图生成。北美采用 2026-08-05 第一版中等偏高密度候选；东亚与太平洋来自 `image_gen/2026-08-06/world-map-region-story-pack-v1/`，均不烘焙锁定、警告或选择状态。
