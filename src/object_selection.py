from OpenGL.GL import *
from OpenGL.GLUT import *

def pick_object(mouse_x, mouse_y, scene_objects):
    """
    Executa a passagem de seleção baseada em cor.
    Returns:
        int: Índice do objeto selecionado ou -1 se nenhum.
    """
    
    if not scene_objects:
        return -1
    
    # Obter altura da janela usando GLUT
    height = glutGet(GLUT_WINDOW_HEIGHT)
    
    # Salvar estados atuais para restaurar depois
    lighting_enabled = glIsEnabled(GL_LIGHTING)
    texture_2d_enabled = glIsEnabled(GL_TEXTURE_2D)
    blend_enabled = glIsEnabled(GL_BLEND)
    
    # Salvar cor de fundo atual
    clear_color = glGetFloatv(GL_COLOR_CLEAR_VALUE)
    
    try:
        # Configurar para color picking
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desabilitar recursos visuais temporariamente
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D) 
        glDisable(GL_BLEND)
        
        # Renderizar objetos com cores codificadas
        for i, obj in enumerate(scene_objects):
            # ID baseado no índice (começando de 1)
            oid = i + 1
            
            # Decomposição RGB
            r = oid & 0xFF
            g = (oid >> 8) & 0xFF
            b = (oid >> 16) & 0xFF
            
            # Definir cor e desenhar
            glColor3ub(r, g, b)
            obj.draw()
        
        # Forçar renderização
        glFlush()
        
        # Ler pixel na posição do mouse
        read_x = int(mouse_x)
        read_y = int(height - mouse_y)
        
        pixel_data = glReadPixels(read_x, read_y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        
        # Decodificar ID
        if isinstance(pixel_data, bytes) and len(pixel_data) >= 3:
            r, g, b = pixel_data[0], pixel_data[1], pixel_data[2]
        else:
            # Array format
            r, g, b = pixel_data[0][0], pixel_data[0][1], pixel_data[0][2]
        
        detected_id = r + (g << 8) + (b << 16)
        
        # Converter para índice (-1 se fundo)
        return (detected_id - 1) if detected_id > 0 else -1
        
    except Exception as e:
        print(f"Erro no color picking: {e}")
        return -1
        
    finally:
        # Restaurar estados originais
        if lighting_enabled:
            glEnable(GL_LIGHTING)
        if texture_2d_enabled:
            glEnable(GL_TEXTURE_2D)
        if blend_enabled:
            glEnable(GL_BLEND)
        
        # Restaurar cor de fundo original
        glClearColor(clear_color[0], clear_color[1], clear_color[2], clear_color[3])