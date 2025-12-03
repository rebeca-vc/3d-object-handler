from OpenGL.GL import *
from OpenGL.GLUT import *


def pick_object(mouse_x, mouse_y, scene_objects):
    """Color picking: renderiza com IDs em RGB e lê o pixel do mouse."""
    
    if not scene_objects:
        return -1
    
    # Altura da janela para converter coordenada Y de leitura
    height = glutGet(GLUT_WINDOW_HEIGHT)
    
    # Salvar estados atuais para restaurar depois
    lighting_enabled = glIsEnabled(GL_LIGHTING)
    texture_2d_enabled = glIsEnabled(GL_TEXTURE_2D)
    blend_enabled = glIsEnabled(GL_BLEND)
    
    # Salvar cor de fundo atual
    clear_color = glGetFloatv(GL_COLOR_CLEAR_VALUE)
    
    try:
        # Configurar para color picking (fundo preto, sem luz/texture/blend)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desabilitar recursos visuais temporariamente
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D) 
        glDisable(GL_BLEND)
        
        # Renderizar objetos com cores codificadas (ID → RGB)
        for i, obj in enumerate(scene_objects):
            oid = i + 1  # índice → ID
            r = oid & 0xFF
            g = (oid >> 8) & 0xFF
            b = (oid >> 16) & 0xFF
            glColor3ub(r, g, b)
            obj.draw()
        
        glFlush()
        
        # Ler pixel na posição do mouse (origem no canto inferior)
        read_x = int(mouse_x)
        read_y = int(height - mouse_y)
        pixel_data = glReadPixels(read_x, read_y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        
        # Decodificar ID
        if isinstance(pixel_data, bytes) and len(pixel_data) >= 3:
            r, g, b = pixel_data[0], pixel_data[1], pixel_data[2]
        else:
            r, g, b = pixel_data[0][0], pixel_data[0][1], pixel_data[0][2]
        detected_id = r + (g << 8) + (b << 16)
        
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
        glClearColor(clear_color[0], clear_color[1], clear_color[2], clear_color[3])
