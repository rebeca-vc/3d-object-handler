from OpenGL.GL import *

"""
Gerencia a seleção e aplicação dos modelos de sombreamento (Flat, Gouraud, Phong).
"""
class ShadingController:
   
    """
    Aplica o modelo de sombreamento desejado.
    """
    def apply_shading(self, selected_shading_mode):
        
        if selected_shading_mode == 'Flat':
            glShadeModel(GL_FLAT)
            
        elif selected_shading_mode == 'Gouraud':
            glShadeModel(GL_SMOOTH)
            
        elif selected_shading_mode == 'Phong':
            # Aviso: Para Phong real, você precisará de Shaders (GLSL).
            # Como fallback, usamos Gouraud.
            glShadeModel(GL_SMOOTH) 
        else:
            glShadeModel(GL_SMOOTH)
            print(f"Modo de sombreamento '{selected_shading_mode}' desconhecido. Usando Gouraud.")