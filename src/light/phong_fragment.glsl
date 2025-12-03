#version 120 // Versão GLSL compatível com OpenGL 2.1

varying vec3 Normal;
varying vec3 Position;

uniform vec4 uAmbient;
uniform vec4 uDiffuse;
uniform vec4 uSpecular;
uniform float uShininess;

void main()
{
    vec4 light_ambient  = gl_LightSource[1].ambient;
    vec4 light_diffuse  = gl_LightSource[1].diffuse;
    vec4 light_specular = gl_LightSource[1].specular;
    vec4 light_position = gl_LightSource[1].position; 

    vec3 N = normalize(Normal);
    vec3 L;
    
    // Verifica se é luz direcional ou posicional
    if (light_position.w == 0.0) {
        L = normalize(vec3(light_position));
    } else {
        L = normalize(vec3(light_position) - Position); 
    }
    
    vec3 V = normalize(-Position);
    vec3 R = reflect(-L, N);

    // --- Phong Lighting Model ---
    
    // 1. Ambiente (Global + Luz)
    vec4 global_ambient = gl_LightModel.ambient * 2.0;
    vec4 ambient = (gl_LightModel.ambient + light_ambient) * uAmbient;

    // 2. Difusa
    float diff_factor = max(dot(N, L), 0.0);
    vec4 diffuse = light_diffuse * uDiffuse * diff_factor;

    // 3. Especular
    float spec_factor = 0.0;
    if (diff_factor > 0.0) {
        spec_factor = pow(max(dot(V, R), 0.0), uShininess);
    }
    vec4 specular = light_specular * uSpecular * spec_factor;

    gl_FragColor = ambient + diffuse + specular;
}