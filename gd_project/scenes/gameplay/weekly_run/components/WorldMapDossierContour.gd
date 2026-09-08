extends RefCounted
## 从现有纸件读取轮廓坐标，纸纹与新闻图仍使用原Texture2D。
## 浮点表是着色器的曲线数据，不是重绘或放大后的美术图片。

static var _rows: Texture2D

static func rows(source: Texture2D) -> Texture2D:
	if _rows != null:
		return _rows
	var image := source.get_image()
	if image.is_compressed():
		image.decompress()
	if image.get_size() != Vector2i(578, 1078):
		push_warning("底纸尺寸已变，需重新核对长边范围；暂保留原纸材质")
		return null
	var outer := PackedFloat32Array()
	var inner := PackedFloat32Array()
	for y in range(image.get_height()):
		var row := clampi(y, 100, 1020)
		var outer_x := 0.0
		var inner_x := 40.0
		for x in range(80):
			if image.get_pixel(x, row).a > 0.5:
				outer_x = float(x)
				break
		for x in range(int(outer_x) + 2, 90):
			var color := image.get_pixel(x, row)
			if color.r > 0.75 and color.r - color.b > 0.08:
				inner_x = float(x)
				break
		outer.append(outer_x)
		inner.append(inner_x)
	# 消除细碎台阶，保留几十像素以上的偏斜与起伏；只改变轮廓坐标。
	var table := Image.create(1, image.get_height(), false, Image.FORMAT_RGBAF)
	for y in range(image.get_height()):
		var weight_sum := 0.0
		var smooth_outer := 0.0
		var smooth_inner := 0.0
		for offset in range(-24, 25):
			var weight := exp(-float(offset * offset) / 128.0)
			var row := clampi(y + offset, 100, 1020)
			smooth_outer += outer[row] * weight
			smooth_inner += inner[row] * weight
			weight_sum += weight
		table.set_pixel(0, y, Color(smooth_outer / weight_sum, smooth_inner / weight_sum, outer[y], inner[y]))
	_rows = ImageTexture.create_from_image(table)
	return _rows
