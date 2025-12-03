from OpenGL.GL import *
try:
    from .filling import polygon_filling
except ImportError:
    from filling import polygon_filling
import math


class Polygon():
    """Polígono 2D com vértices, cor e segmentos de preenchimento (scanline)."""

    def __init__(self, color=(1.0, 1.0, 1.0)):
        self.vertices = []
        self.color = color
        self.filled_segments = []
    
    def fill(self, color=(0.5, 0.5, 1.0)):
        """Calcula segmentos de preenchimento via scanline e define cor."""
        if len(self.vertices) < 3:
            self.filled_segments = []
            return
            
        try:
            self.filled_segments = polygon_filling(self.vertices)
            self.color = color
            
            if self.filled_segments:
                print(f"Polígono preenchido: {len(self.filled_segments)} segmentos")
                
                # Buracos: múltiplos segmentos na mesma linha Y
                y_lines = {}
                for y, x1, x2 in self.filled_segments:
                    if y not in y_lines:
                        y_lines[y] = 0
                    y_lines[y] += 1
                
                holes = sum(1 for count in y_lines.values() if count > 1)
                if holes > 0:
                    print(f"  → Detectados buracos em {holes} linhas")
                else:
                    print("  → Polígono sólido (sem buracos)")
            else:
                print("Aviso: Nenhum segmento gerado pelo algoritmo de preenchimento")
                
        except Exception as e:
            print(f"Erro no preenchimento: {e}")
            self.filled_segments = []

    def add_vertex(self, x, y):
        """Adiciona vértice (x,y) à lista de vértices na ordem atual."""
        self.vertices.append([x, y])

    def clear(self):
        self.vertices.clear()
    
    def _are_collinear(self, p1, p2, p3):
        """Testa colinearidade via produto vetorial ≈ 0 (tolerância)."""
        # Produto vetorial: (p2 - p1) x (p3 - p1)
        # Se for 0 (ou muito próximo de 0), os pontos são colineares
        cross_product = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
        return abs(cross_product) < 1e-10  # Tolerância para erros de ponto flutuante
    
    def _has_collinear_points(self):
        """Verifica se há vértices consecutivos colineares (inválido para extrusão)."""
        if len(self.vertices) < 3:
            return False
        
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            p3 = self.vertices[(i + 2) % len(self.vertices)]
            
            if self._are_collinear(p1, p2, p3):
                return True
        return False
    
    def is_valid_for_extrusion(self):
        """Valida extrusão: ≥3 vértices e sem colinearidade consecutiva."""
        if len(self.vertices) < 3:
            return False
        
        # Verifica se há pontos colineares
        if self._has_collinear_points():
            return False
            
        return True

    def draw_edges(self, current_line_thickness):
        """Desenha arestas como retângulos de espessura `current_line_thickness`."""
        if len(self.vertices) < 2:
            return
        
        glColor3f(1.0, 1.0, 1.0)

        half_w = current_line_thickness / 2.0

        glBegin(GL_QUADS)
        for i in range(len(self.vertices)):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)]

            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx * dx + dy * dy)
            if length == 0:
                continue

            # Vetor perpendicular normalizado para espessura
            nx = -dy / length
            ny = dx / length

            # deslocamento para dar espessura
            offset_x = nx * half_w
            offset_y = ny * half_w

            # 4 vértices do retângulo
            glVertex2f(x1 + offset_x, y1 + offset_y)
            glVertex2f(x1 - offset_x, y1 - offset_y)
            glVertex2f(x2 - offset_x, y2 - offset_y)
            glVertex2f(x2 + offset_x, y2 + offset_y)
        glEnd()

    def draw_fill(self):
        """Desenha preenchimento: linhas e pontos conforme `filled_segments`."""
        if not self.filled_segments:
            return
            
        glColor3f(*self.color)
        
        # Segmentos como linhas horizontais
        glBegin(GL_LINES)
        for y, x1, x2 in self.filled_segments:
            glVertex2f(x1, y)
            glVertex2f(x2, y)
        glEnd()
        
        # Alternativa: pontos para maior visibilidade
        glPointSize(1.0)
        glBegin(GL_POINTS)
        for y, x1, x2 in self.filled_segments:
            for x in range(int(x1), int(x2) + 1):
                glVertex2f(x, y)
        glEnd()
