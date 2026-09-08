shader_type canvas_item;
render_mode unshaded;

// 修复旧透明提取产生的二值边缘；只混合轮廓覆盖率，完整纸面不模糊。
uniform bool smooth_edges = true;
uniform bool front_only = false;
uniform bool smooth_quad = false;
uniform bool contour_enabled = false;
uniform sampler2D contour_rows : filter_linear, repeat_disable;
varying vec4 paper_tint;

void vertex() {
	paper_tint = COLOR;
}

vec4 paper_sample(sampler2D tex, vec2 at) {
	vec4 value = texture(tex, at);
	if (front_only) {
		// 现有母件的暖白纸与青色衬纸分离，保留原纸轮廓，不绘制新形状。
		value.a *= smoothstep(0.025, 0.09, value.r - value.b);
	}
	return value;
}

void fragment() {
	vec4 center = paper_sample(TEXTURE, UV);
	vec4 result = center;
	if (smooth_edges) {
		vec2 step_uv = TEXTURE_PIXEL_SIZE * 0.75;
		vec4 total = vec4(0.0);
		for (int y = -1; y <= 1; y++) {
			for (int x = -1; x <= 1; x++) {
				float weight = (x == 0 ? 2.0 : 1.0) * (y == 0 ? 2.0 : 1.0) / 16.0;
				vec4 sample_color = paper_sample(TEXTURE, UV + vec2(float(x), float(y)) * step_uv);
				total += vec4(sample_color.rgb * sample_color.a, sample_color.a) * weight;
			}
		}
		// 预乘后混合，避免透明像素内遗留的棋盘底污染纸边颜色。
		result = vec4(total.rgb / max(total.a, 0.0001), total.a);
		if (center.a > 0.999 && total.a > 0.999) {
			result.rgb = center.rgb;
		}
	}
	if (contour_enabled) {
		vec2 source_at = UV / TEXTURE_PIXEL_SIZE;
		vec4 edges = texture(contour_rows, vec2(0.5, UV.y));
		// 只修右侧底纸的两条左长边；顶部夹具与底角保留原资产。
		float extent = smoothstep(100.0, 140.0, source_at.y) * (1.0 - smoothstep(994.0, 1020.0, source_at.y));
		float outer_distance = source_at.x - edges.r;
		float outer_aa = max(fwidth(outer_distance) * 0.65, 0.001);
		float outer_band = 1.0 - smoothstep(edges.r + 2.5, edges.r + 4.0, source_at.x);
		vec4 backing = texture(TEXTURE, vec2(max(source_at.x, edges.b + 1.5) * TEXTURE_PIXEL_SIZE.x, UV.y));
		backing.a = smoothstep(-outer_aa, outer_aa, outer_distance);
		result = mix(result, backing, extent * outer_band);
		// 白纸/蓝衬纸的内部色界也按连续曲线重建，不能只改透明外缘。
		float inner_distance = source_at.x - edges.g;
		float inner_aa = max(fwidth(inner_distance) * 0.65, 0.001);
		float inner_band = 1.0 - smoothstep(2.5, 4.0, abs(inner_distance));
		// 从两侧干净纸纹取色，避开旧轮廓的深色描边；采样点也沿连续曲线移动。
		vec3 blue = texture(TEXTURE, vec2((edges.g - 6.0) * TEXTURE_PIXEL_SIZE.x, UV.y)).rgb;
		vec3 paper = texture(TEXTURE, vec2((edges.g + 4.0) * TEXTURE_PIXEL_SIZE.x, UV.y)).rgb;
		vec3 seam = mix(blue, paper, smoothstep(-inner_aa, inner_aa, inner_distance));
		result.rgb = mix(result.rgb, seam, extent * inner_band);
	}
	COLOR = result * paper_tint;
	if (smooth_quad) {
		// 倾斜照片的矩形边界没有透明留边，需在四边补一像素几何覆盖率。
		vec2 footprint = max(fwidth(UV), vec2(0.00001));
		vec2 coverage = smoothstep(vec2(0.0), footprint, UV) * smoothstep(vec2(0.0), footprint, vec2(1.0) - UV);
		COLOR.a *= coverage.x * coverage.y;
	}
}
