from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from assets.polygon import Polygon
from assets.mouse import handle_modeling_mouse

class PolygonEditor:
    """Editor 2D minimalista: captura vértices, aplica scanline e desenha UI."""
    
    def __init__(self):
        self.current_polygon = None
        self.completion_callback = None
        self.is_active = False
    
    def start_modeling(self, completion_callback=None):
        """Inicia sessão: cria `Polygon`, define callback e ativa editor."""
        self.current_polygon = Polygon()
        self.completion_callback = completion_callback
        self.is_active = True
        print("Modelagem iniciada - Clique esquerdo: adicionar ponto | Clique direito: finalizar")
    
    def stop_modeling(self):
        """Finaliza sessão e limpa polígono atual."""
        self.is_active = False
        self.current_polygon = None
        print("Modelagem finalizada")
    
    def handle_mouse(self, button, state, x, y):
        """Encaminha cliques ao handler; finaliza com clique direito."""
        if not self.is_active:
            return False
        
        result = handle_modeling_mouse(button, state, x, y, self.current_polygon, self._on_polygon_complete)
        
        # Se foi clique direito e polígono foi finalizado, parar modelagem
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            if self.current_polygon and len(self.current_polygon.vertices) >= 3:
                self.stop_modeling()
        
        return result
    
    def _on_polygon_complete(self, polygon):
        """Preenche (se preciso), reporta segmentos e dispara callback externo."""
        if self.completion_callback:
            # Garantir que o polígono está preenchido antes de finalizar
            if hasattr(polygon, 'filled_segments') and not polygon.filled_segments:
                polygon.fill()
            
            print(f"Polígono finalizado com {len(polygon.filled_segments) if polygon.filled_segments else 0} segmentos preenchidos")
            self.completion_callback(polygon)
    
    def render(self):
        """Desenha preenchimento (scanline), bordas e vértices enquanto ativo."""
        if not self.is_active or not self.current_polygon:
            return
        
        # Limpar fundo com cor diferente para indicar modo de modelagem
        glClearColor(0.05, 0.05, 0.15, 1.0)
        
        # Com ≥3 vértices, aplica preenchimento automaticamente
        if len(self.current_polygon.vertices) >= 3:
            try:
                # Preencher o polígono automaticamente
                self.current_polygon.fill((0.3, 0.7, 0.3))  # Verde claro
                # Desenhar o preenchimento
                self.current_polygon.draw_fill()
            except Exception as e:
                print(f"Erro no preenchimento: {e}")
        
        # Desenhar bordas por cima do preenchimento
        if len(self.current_polygon.vertices) >= 2:
            self.current_polygon.draw_edges(2.0)
        
        # Desenhar pontos nos vértices por cima de tudo
        self._draw_vertex_points()
    
    def _draw_vertex_points(self):
        """Pontos nos vértices para feedback visual durante edição."""
        if not self.current_polygon or not self.current_polygon.vertices:
            return
        
        glColor3f(1.0, 1.0, 0.0)  # Amarelo
        glPointSize(6.0)
        glBegin(GL_POINTS)
        
        for vertex in self.current_polygon.vertices:
            glVertex2f(vertex[0], vertex[1])
        
        glEnd()
    
    def get_current_polygon_vertices(self):
        """Retorna cópia dos vértices atuais (para consumo externo)."""
        if self.current_polygon:
            return self.current_polygon.vertices.copy()
        return []
    
    def setup_2d_projection(self, width, height):
        """Configura ortho 2D e desabilita recursos 3D (depth/lighting)."""
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