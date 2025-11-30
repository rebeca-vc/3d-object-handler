from OpenGL.GL import *
import math


class Polygon():

    def __init__(self, color=(1.0, 1.0, 1.0)):
        self.vertices = []
        self.color = color
    
    def add_vertex(self, x, y):
        self.vertices.append([x, y])

    def clear(self):
        self.vertices.clear()
    
    def _are_collinear(self, p1, p2, p3):
        """Verifica se três pontos são colineares usando produto vetorial"""
        # Produto vetorial: (p2 - p1) x (p3 - p1)
        # Se for 0 (ou muito próximo de 0), os pontos são colineares
        cross_product = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
        return abs(cross_product) < 1e-10  # Tolerância para erros de ponto flutuante
    
    def _has_collinear_points(self):
        """Verifica se o polígono tem pontos colineares consecutivos"""
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
        """Verifica se polígono é válido para extrusão"""
        if len(self.vertices) < 3:
            return False
        
        # Verifica se há pontos colineares
        if self._has_collinear_points():
            return False
            
        return True

    def draw_edges(self, current_line_thickness):
        """Desenha bordas do polígono com espessura"""
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

            # Vetor perpendicular normalizado
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