from OpenGL.GL import *

class LightingController:
    """
    Gerencia a inicialização, a configuração e a posição das fontes de luz.
    GL_LIGHT0 é usada como luz padrão (fixa).
    GL_LIGHT1 é usada como luz móvel.
    """
    def __init__(self):
        # Estado e Posição da luz móvel (LIGHT1)
        self.light_enabled = False
        # Posição inicial (ponto de luz: w=1.0)
        self.light_position = [2.0, 5.0, 2.0, 1.0] 
        self.light_id = GL_LIGHT1 # ID da luz móvel

        # Configurações de cores para a luz (pode ser ajustado)
        self.light_ambient  = [0.2, 0.2, 0.2, 1.0]
        self.light_diffuse  = [0.8, 0.8, 0.8, 1.0]
        self.light_specular = [1.0, 1.0, 1.0, 1.0]

    def initialize_global_lighting(self):
        """
        Configura o ambiente global de iluminação (GL_LIGHTING, GL_LIGHT0).
        Deve ser chamado uma vez na inicialização (main.py/init).
        """
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE) # Garante que as normais sejam unitárias
        
        # Configuração da Luz Padrão (LIGHT0)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0]) # Posição padrão fixa
        
        # Se você quiser que a luz ambiente afete o objeto mesmo sem a luz móvel:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0]) 

    def enable_movable_light(self):
        """Ativa e configura a luz móvel (LIGHT1)."""
        if not self.light_enabled:
            glEnable(self.light_id)
            
            # Aplica as cores definidas
            glLightfv(self.light_id, GL_AMBIENT,  self.light_ambient)
            glLightfv(self.light_id, GL_DIFFUSE,  self.light_diffuse)
            glLightfv(self.light_id, GL_SPECULAR, self.light_specular)
            
            # Aplica a posição inicial (será atualizada em 'update')
            glLightfv(self.light_id, GL_POSITION, self.light_position)
            
            self.light_enabled = True
            print("Fonte de luz LIGHT1 móvel adicionada e ativada.")
        else:
            print("A fonte de luz LIGHT1 já está ativa.")

    def update_light_position(self, key_direction: str, step: float = 0.5):
        """Move a luz (LIGHT1) com base na direção do teclado."""
        if not self.light_enabled:
            return
            
        # O self.light_position tem o formato [x, y, z, w]
        if key_direction == 'LEFT':
            self.light_position[0] -= step
        elif key_direction == 'RIGHT':
            self.light_position[0] += step
        elif key_direction == 'UP':
            self.light_position[2] -= step # Move -Z (para frente)
        elif key_direction == 'DOWN':
            self.light_position[2] += step # Move +Z (para trás)
        elif key_direction == 'ELEVATE': # Ex: tecla 'a'
            self.light_position[1] += step
        elif key_direction == 'LOWER': # Ex: tecla 'z'
            self.light_position[1] -= step

    def apply_light_position(self):
        """
        Aplica a posição atualizada da luz no pipeline OpenGL.
        Deve ser chamada a cada frame (display).
        """
        if self.light_enabled:
            # Aplica a posição da luz em coordenadas de mundo (após a transformação da câmera)
            glLightfv(self.light_id, GL_POSITION, self.light_position)
            
            # Opcional: Desenha um marcador para a luz
            self._draw_light_marker()
            
    def _draw_light_marker(self):
        """Desenha uma esfera para visualizar a posição da luz."""
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glTranslatef(self.light_position[0], self.light_position[1], self.light_position[2])
        glColor3f(1.0, 1.0, 0.0) # Amarelo para indicar a luz
        glutWireSphere(0.2, 8, 8) 
        glPopMatrix()
        glEnable(GL_LIGHTING)