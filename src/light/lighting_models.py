from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class LightingController:
    """
    Gerencia a inicialização, a configuração e a posição das fontes de luz.
    GL_LIGHT0 é usada como luz padrão (fixa).
    GL_LIGHT1 é usada como luz móvel.
    """
    def __init__(self):
        # Estado e Posição da luz móvel (LIGHT1)
        self.light_enabled = False

        # Posição inicial 
        self.light_position = [2.0, 5.0, 2.0, 1.0] 
        self.light_id = GL_LIGHT1 

        # Configurações de cores para a luz 
        self.light_ambient  = [0.2, 0.2, 0.2, 1.0]
        self.light_diffuse  = [0.8, 0.8, 0.8, 1.0]
        self.light_specular = [1.0, 1.0, 1.0, 1.0]

    """
    Configura o ambiente global de iluminação (GL_LIGHTING, GL_LIGHT0).
    Deve ser chamado uma vez na inicialização (main.py/init).
    """
    def initialize_global_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE) 
        
        # Configuração da Luz Padrão (LIGHT0)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0]) 
        
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0]) 

    """Ativa e configura a luz móvel (LIGHT1)."""
    def enable_movable_light(self):
        if not self.light_enabled:
            glEnable(GL_LIGHTING)
            glEnable(self.light_id)
            
            # Aplica as cores
            glLightfv(self.light_id, GL_AMBIENT,  self.light_ambient)
            glLightfv(self.light_id, GL_DIFFUSE,  self.light_diffuse)
            glLightfv(self.light_id, GL_SPECULAR, self.light_specular)
            
            # Aplica a posição inicial 
            glLightfv(self.light_id, GL_POSITION, self.light_position)
            
            self.light_enabled = True
            print("Fonte de luz LIGHT1 móvel adicionada e ativada.")            

    """Move a luz (LIGHT1) com base na direção do teclado."""
    def update_light_position(self, key_direction: str, step: float = 0.5):
        if not self.light_enabled:
            return
            
        # O self.light_position = [x, y, z, w]
        if key_direction == 'LEFT':
            self.light_position[0] -= step
        elif key_direction == 'RIGHT':
            self.light_position[0] += step
        elif key_direction == 'UP':
            self.light_position[2] -= step 
        elif key_direction == 'DOWN':
            self.light_position[2] += step 
        elif key_direction == 'ELEVATE': 
            self.light_position[1] += step
        elif key_direction == 'LOWER':
            self.light_position[1] -= step

    """
    Aplica a posição atualizada da luz no pipeline OpenGL.
    Deve ser chamada a cada frame (display).
    """
    def apply_light_position(self):
        if self.light_enabled:
            # Aplica a posição da luz em coordenadas de mundo 
            glLightfv(self.light_id, GL_POSITION, self.light_position)
            glDisable(GL_LIGHTING)
            glPushMatrix()
            glTranslatef(self.light_position[0], self.light_position[1], self.light_position[2])
            glColor3f(1.0, 1.0, 0.0) 
            glutWireSphere(0.2, 8, 8) 
            glPopMatrix()
            glEnable(GL_LIGHTING)

    def light_setup(self, ambient_light, difuse_light, specular_light):
        # Valores base
        ambience_base = [0.1, 0.1, 0.1, 1.0]
        difuse_base = [0.8, 0.8, 0.8, 1.0]
        specular_base = [1.0, 1.0, 1.0, 1.0]
        
        # Aplicar 0.0 se o componente não estiver ativo no painel
        ambient = ambience_base if ambient_light else [0.0, 0.0, 0.0, 1.0]
        difuse = difuse_base if difuse_light else [0.0, 0.0, 0.0, 1.0]
        specular = specular_base if specular_light else [0.0, 0.0, 0.0, 1.0]
        
        # Aplica os vetores de cor na fonte de luz 
        glLightfv(self.light_id, GL_AMBIENT, ambient)
        glLightfv(self.light_id, GL_DIFFUSE, difuse)
        glLightfv(self.light_id, GL_SPECULAR, specular)
        
        # Se todos os componentes estiverem desligados, desligamos a luz.
        if not ambient_light and not difuse_light and not specular_light:
            glDisable(self.light_id)
        else:
            glEnable(self.light_id)
