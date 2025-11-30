from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from assets.polygon import Polygon
from assets.mouse import handle_modeling_mouse

class PolygonEditor:
    """
    Editor simplificado de polígonos para integração direta com aplicação 3D.
    Remove botões e foca na criação de polígonos para extrusão.
    """
    
    def __init__(self):
        self.current_polygon = None
        self.completion_callback = None
        self.is_active = False
    
    def start_modeling(self, completion_callback=None):
        """Inicia sessão de modelagem"""
        self.current_polygon = Polygon()
        self.completion_callback = completion_callback
        self.is_active = True
        print("Modelagem iniciada - Clique esquerdo: adicionar ponto | Clique direito: finalizar")
    
    def stop_modeling(self):
        """Para sessão de modelagem"""
        self.is_active = False
        self.current_polygon = None
        print("Modelagem finalizada")
    
    def handle_mouse(self, button, state, x, y):
        """Processa eventos de mouse durante modelagem"""
        if not self.is_active:
            return False
        
        result = handle_modeling_mouse(button, state, x, y, self.current_polygon, self._on_polygon_complete)
        
        # Se foi clique direito e polígono foi finalizado, parar modelagem
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            if self.current_polygon and len(self.current_polygon.vertices) >= 3:
                self.stop_modeling()
        
        return result
    
    def _on_polygon_complete(self, polygon):
        """Callback chamado quando polígono é finalizado"""
        if self.completion_callback:
            self.completion_callback(polygon)
    
    def render(self):
        """Renderiza polígono em construção"""
        if not self.is_active or not self.current_polygon:
            return
        
        # Limpar fundo com cor diferente para indicar modo de modelagem
        glClearColor(0.05, 0.05, 0.15, 1.0)
        
        # Desenhar apenas bordas (não preencher)
        self.current_polygon.draw_edges(2.0)
        
        # Desenhar pontos nos vértices
        self._draw_vertex_points()
    
    def _draw_vertex_points(self):
        """Desenha pontos nos vértices para melhor visualização"""
        if not self.current_polygon or not self.current_polygon.vertices:
            return
        
        glColor3f(1.0, 1.0, 0.0)  # Amarelo
        glPointSize(6.0)
        glBegin(GL_POINTS)
        
        for vertex in self.current_polygon.vertices:
            glVertex2f(vertex[0], vertex[1])
        
        glEnd()
    
    def get_current_polygon_vertices(self):
        """Retorna vértices do polígono atual"""
        if self.current_polygon:
            return self.current_polygon.vertices.copy()
        return []
    
    def setup_2d_projection(self, width, height):
        """Configura projeção 2D para modelagem"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Desabilitar funcionalidades 3D
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)


# Instância global para uso externo
editor_instance = PolygonEditor()