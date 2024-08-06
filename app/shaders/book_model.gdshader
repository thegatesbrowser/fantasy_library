shader_type spatial;

uniform vec4 color: source_color;

void vertex() {
	VERTEX.x += 0.5;
	
	float pivot_angle = cos(TIME * 0.2) * float(INSTANCE_ID) * 0.1;
	pivot_angle = clamp(pivot_angle, -PI, 0.0);
	mat2 rotation_matrix = mat2(vec2(cos(pivot_angle), -sin(pivot_angle)), vec2(sin(pivot_angle), cos(pivot_angle)));
	
	VERTEX.xy = rotation_matrix * VERTEX.xy;
	NORMAL.xy = rotation_matrix * NORMAL.xy;
}

void fragment() {
	ALBEDO = color.rgb;
}

//void light() {
	//
//}
