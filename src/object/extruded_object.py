from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import copy
import math
from object.objects import Object
from object.material import MATERIALS


class ExtrudedObject(Object):
    
    # Objeto 3D criado por extrusão de um polígono 2D.
    
    
    def __init__(self, base_vertices, depth, material='white_plastic'):
        """
        Cria objeto 3D por extrusão
        
        Args:
            base_vertices: Lista de vértices 2D [[x,y,z], ...] que formam a base
            depth: Profundidade da extrusão (valor Z)
            material: Nome do material a ser aplicado
        """
        # Inicializar classe pai
        super().__init__(shape='custom', material=material)
        
        self.base_vertices = base_vertices
        self.depth = depth
        self.vertices_3d = []
        self.faces = []
        
        # Gerar geometria 3D
        self._generate_3d_geometry()
    
    def _generate_3d_geometry(self):
        """Gera vértices e faces 3D por extrusão"""
        base_count = len(self.base_vertices)
        
        if base_count < 3:
            print("Erro: Polígono base deve ter pelo menos 3 vértices")
            return
        
        # Criar vértices 3D
        self.vertices_3d = []
        
        # Face frontal (z=0)
        for vertex in self.base_vertices:
            self.vertices_3d.append([vertex[0], vertex[1], 0.0])
        
        # Face traseira (z=depth)
        for vertex in self.base_vertices:
            self.vertices_3d.append([vertex[0], vertex[1], self.depth])
        
        # Gerar faces
        self.faces = []
        
        # Face frontal (polígono base)
        front_face = list(range(base_count))
        self.faces.append(front_face)
        
        # Face traseira (polígono base invertido)
        back_face = list(range(base_count, 2 * base_count))
        back_face.reverse()  # Inverter para normal apontar para fora
        self.faces.append(back_face)
        
        # Faces laterais (conectando frente e trás)
        for i in range(base_count):
            next_i = (i + 1) % base_count
            
            # Criar quad para cada aresta
            face = [
                i,                          # vértice atual (frente)
                next_i,                     # próximo vértice (frente)
                next_i + base_count,        # próximo vértice (trás)
                i + base_count              # vértice atual (trás)
            ]
            self.faces.append(face)
    
    def draw(self):
        """Renderiza o objeto usando OpenGL"""
        glPushMatrix()
        try:
            # Aplicar transformações do objeto pai
            glShadeModel(self.shading_model)
            glMultMatrixf(self._matrix)
            self._apply_material()
            
            # Renderizar faces
            self._render_faces()
            
        finally:
            glPopMatrix()
    
    def _render_faces(self):
        """Renderiza todas as faces do objeto"""
        for face_indices in self.faces:
            face_size = len(face_indices)
            
            if face_size == 3:
                glBegin(GL_TRIANGLES)
            elif face_size == 4:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_POLYGON)
            
            # Calcular normal da face para iluminação
            if face_size >= 3:
                normal = self._calculate_face_normal(face_indices)
                glNormal3f(*normal)
            
            # Desenhar vértices da face
            for vertex_index in face_indices:
                vertex = self.vertices_3d[vertex_index]
                glVertex3f(*vertex)
            
            glEnd()
    
    def _calculate_face_normal(self, face_indices):
        """Calcula normal de uma face para iluminação"""
        if len(face_indices) < 3:
            return [0.0, 0.0, 1.0]  # Normal padrão
        
        # Pegar três primeiros vértices
        v1 = self.vertices_3d[face_indices[0]]
        v2 = self.vertices_3d[face_indices[1]]
        v3 = self.vertices_3d[face_indices[2]]
        
        # Calcular vetores da face
        edge1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
        edge2 = [v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]]
        
        # Produto vetorial para normal
        normal = [
            edge1[1] * edge2[2] - edge1[2] * edge2[1],
            edge1[2] * edge2[0] - edge1[0] * edge2[2],
            edge1[0] * edge2[1] - edge1[1] * edge2[0]
        ]
        
        # Normalizar
        length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if length > 0:
            normal = [normal[0]/length, normal[1]/length, normal[2]/length]
        else:
            normal = [0.0, 0.0, 1.0]
        
        return normal
    
    def set_depth(self, new_depth):
        """Altera a profundidade da extrusão"""
        self.depth = new_depth
        self._generate_3d_geometry()
    
    def get_vertex_count(self):
        """Retorna número total de vértices"""
        return len(self.vertices_3d)
    
    def get_face_count(self):
        """Retorna número total de faces"""
        return len(self.faces)
    
    def get_info(self):
        """Retorna informações sobre o objeto"""
        return {
            'type': 'ExtrudedObject',
            'base_vertices': len(self.base_vertices),
            'depth': self.depth,
            'total_vertices': self.get_vertex_count(),
            'total_faces': self.get_face_count()
        }