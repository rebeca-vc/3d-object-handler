# lighting_models.py
from OpenGL.GL import *

def enable_lighting(ambient=True, diffuse=True, specular=True):
    """Ativa a iluminação global e os componentes de luz."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) 

    # Define as propriedades da luz (pode ser ajustado)
    light_ambient = [0.2, 0.2, 0.2, 1.0] if ambient else [0.0, 0.0, 0.0, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0] if diffuse else [0.0, 0.0, 0.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0] if specular else [0.0, 0.0, 0.0, 1.0]
    light_position = [5.0, 5.0, 5.0, 1.0] # Posição da luz 

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # Ativa o cálculo automático de normais (útil se você não gerar as normais explicitamente)
    glEnable(GL_NORMALIZE)
    
    # Define as propriedades padrão do material
    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = 50.0 # Brilho

    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)
    
    # Faz a cor definida por glColor3f afetar a componente ambiente e difusa do material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


def set_flat_shading():
    """Configura o modelo de sombreamento Flat (Constante)."""
    # A cor é calculada APENAS uma vez para cada face (face vertex)
    glShadeModel(GL_FLAT)
    print("Shading: Flat")

def set_gouraud_shading():
    """Configura o modelo de sombreamento Gouraud (Suave)."""
    # A cor é calculada para cada VÉRTICE e interpolada através da face
    glShadeModel(GL_SMOOTH)
    print("Shading: Gouraud")

