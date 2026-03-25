shader_type canvas_item;

uniform float gray_amount : hint_range(0.0, 1.0) = 0.0;
uniform float ghost_strength : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec2 shift = vec2(0.0025 * sin(TIME * 12.0), 0.0);
	vec4 base = texture(TEXTURE, UV);
	vec4 ghost = texture(TEXTURE, clamp(UV + shift, vec2(0.0), vec2(1.0)));

	float luma = dot(base.rgb, vec3(0.299, 0.587, 0.114));
	vec3 gray = vec3(luma);
	vec3 color = mix(base.rgb, gray, gray_amount);
	color = mix(color, ghost.rgb, ghost_strength * 0.22);

	float scan = sin((UV.y + TIME * 0.32) * 168.0) * 0.5 + 0.5;
	color *= 1.0 - ghost_strength * 0.12 * scan;
	COLOR = vec4(color, base.a);
}
