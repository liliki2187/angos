shader_type canvas_item;

uniform float weirdness : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec2 uv = UV;
	float wave = sin(uv.y * 122.0 + TIME * 18.0) * 0.008 * weirdness;
	float wobble = sin(uv.y * 28.0 + TIME * 2.7) * 0.004 * weirdness;
	uv.x += wave + wobble;

	vec2 shift = vec2(0.007 * weirdness * sin(TIME * 22.0), 0.0);
	vec2 uv_r = clamp(uv + shift, vec2(0.0), vec2(1.0));
	vec2 uv_b = clamp(uv - shift, vec2(0.0), vec2(1.0));

	vec4 r = texture(TEXTURE, uv_r);
	vec4 g = texture(TEXTURE, clamp(uv, vec2(0.0), vec2(1.0)));
	vec4 b = texture(TEXTURE, uv_b);
	vec4 color = vec4(r.r, g.g, b.b, g.a);

	float line = step(0.56, fract((UV.y + TIME * 0.9) * 96.0));
	color.rgb *= 1.0 - weirdness * 0.18 * line;

	float vignette = smoothstep(0.92, 0.24, distance(UV, vec2(0.5)));
	color.rgb = mix(color.rgb, color.rgb * vignette, weirdness * 0.42);

	float dim = dot(color.rgb, vec3(0.299, 0.587, 0.114));
	color.rgb = mix(color.rgb, vec3(dim), weirdness * 0.14);
	COLOR = color;
}
