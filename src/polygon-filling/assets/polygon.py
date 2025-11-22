from OpenGL.GL import *
import math
from .filling import polygon_filling


class Polygon():

    def __init__(self, color=(1.0, 1.0, 1.0)):
        self.vertices = []
        self.filled_segments = []
        self.color = color
        self.filled = False
    
    def add_vertex(self, x, y):
        self.vertices.append([x, y])

    def clear(self):
        self.vertices.clear()
        self.filled_segments.clear()

    def fill(self, color=(1.0, 1.0, 1.0)):
        self.filled_segments = polygon_filling(self.vertices)
        self.color = color

    def draw_edges(self, current_line_thickness):
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
    
    def draw_fill(self):
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        for y, x1, x2 in self.filled_segments:
            for x in range(x1, x2 + 1):
                glVertex2f(x, y)
        glEnd()

    
    def check_inside_polygon(self, x, y):
        if not self.vertices or len(self.vertices) < 3:
            return False
        
        intersections = 0
        n = len(self.vertices)
        
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            
            if y1 == y2:
                continue
            # para estar no meio é um xor (sp 1 é maior)
            if (y1 > y) != (y2 > y):
                #  x em que a reta horizontal mouse intercepta a aresta
                x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                
                # valida se a interseção foi à direita
                if x_intersect > x:
                    intersections += 1
        
        return intersections % 2 == 1