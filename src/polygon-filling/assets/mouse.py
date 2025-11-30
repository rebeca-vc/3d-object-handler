from OpenGL.GLUT import *
from .polygon import Polygon

def handle_modeling_mouse(button, state, x, y, current_polygon, completion_callback=None):
    """
    Processa eventos de mouse durante modelagem de polígonos para extrusão 3D.
    
    Args:
        button: Botão do mouse pressionado
        state: Estado do botão (GLUT_DOWN/GLUT_UP)
        x, y: Coordenadas do mouse
        current_polygon: Polígono atual sendo modelado
        completion_callback: Função chamada quando polígono é finalizado
    
    Returns:
        bool: True se evento foi processado, False caso contrário
    """
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        height = glutGet(GLUT_WINDOW_HEIGHT)
        point = [x, height - y]
        
        # Adiciona ponto ao polígono atual
        if current_polygon:
            current_polygon.add_vertex(*point)
            print(f"Ponto {len(current_polygon.vertices)}: {point}")
            glutPostRedisplay()
        return True
    
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Finalizar polígono
        if current_polygon and len(current_polygon.vertices) >= 3:
            print(f"Polígono finalizado com {len(current_polygon.vertices)} vértices")
            
            # Chamar callback se fornecido
            if completion_callback:
                completion_callback(current_polygon)
        else:
            print("Erro: polígono precisa de pelo menos 3 pontos")
        
        glutPostRedisplay()
        return True
    
    return False
