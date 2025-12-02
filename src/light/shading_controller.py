from OpenGL.GL import *

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if status == GL_FALSE:
        raise RuntimeError(f"Erro de compilação do shader {shader_type}:\n{glGetShaderInfoLog(shader)}")
        
    return shader

def create_shader_program(vertex_source, fragment_source):
    vert_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
    frag_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
    
    program = glCreateProgram()
    glAttachShader(program, vert_shader)
    glAttachShader(program, frag_shader)
    
    glLinkProgram(program)
    
    status = glGetProgramiv(program, GL_LINK_STATUS)
    if status == GL_FALSE:
        raise RuntimeError(f"Erro de linkagem do programa shader:\n{glGetProgramInfoLog(program)}")
    
    # Após a linkagem, os shaders individuais podem ser deletados (opcional, mas boa prática)
    glDeleteShader(vert_shader)
    glDeleteShader(frag_shader)
    
    return program

# --- CÓDIGO DA CLASSE ShadingController (Com alterações) ---

class ShadingController:
   
    def __init__(self):
        self.phong_program = None
        self._load_phong_shader()
    
    def _load_phong_shader(self):
        # Em um projeto real, você leria os arquivos .glsl
        # Aqui, usamos as strings definidas anteriormente.
        try:
            vertex = ""
            with open('light/phong_vertex.glsl', 'r', encoding='utf-8') as arquivo:
                vertex = arquivo.read() # Lê todo o conteúdo do arquivo
                print(vertex)

            PHONG_VERTEX_SOURCE = vertex

            fragment = ""
            with open('light/phong_fragment.glsl', 'r', encoding='utf-8') as arquivo:
                fragment = arquivo.read() # Lê todo o conteúdo do arquivo
                print(fragment)

            PHONG_FRAGMENT_SOURCE = fragment
            self.phong_program = create_shader_program(PHONG_VERTEX_SOURCE, PHONG_FRAGMENT_SOURCE)
            print("Programa Phong Shader carregado com sucesso.")

        except RuntimeError as e:
            print(f"Falha ao carregar o Phong Shader: {e}")
            self.phong_program = None


    def apply_shading(self, selected_shading_mode):
        
        if selected_shading_mode == 'Flat':
            glUseProgram(0) # Desativa shaders GLSL
            glShadeModel(GL_FLAT)
            
        elif selected_shading_mode == 'Gouraud':
            glUseProgram(0) # Desativa shaders GLSL
            glShadeModel(GL_SMOOTH)
            
        elif selected_shading_mode == 'Phong':
            if self.phong_program:
                # Ativa o programa shader para todos os desenhos subsequentes
                glUseProgram(self.phong_program) 
            else:
                # Fallback se o shader falhou ao carregar
                glUseProgram(0)
                glShadeModel(GL_SMOOTH) 
                print("Atenção: Phong Shading não disponível, usando Gouraud como fallback.")
        else:
            glUseProgram(0)
            glShadeModel(GL_SMOOTH)
            print(f"Modo de sombreamento '{selected_shading_mode}' desconhecido. Usando Gouraud.")