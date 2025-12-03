#version 120 // Versão GLSL compatível com OpenGL 2.1 (padrão antigo)

varying vec3 Normal;
varying vec3 Position;

void main()
{
    // Transforma a posição do vértice (espaço do objeto -> espaço de visualização/câmera)
    Position = vec3(gl_ModelViewMatrix * gl_Vertex);

    // Transforma a normal (apenas a parte 3x3 da matriz ModelView para evitar translações)
    Normal = normalize(gl_NormalMatrix * gl_Normal);

    // Posição final do vértice (projeção)
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}