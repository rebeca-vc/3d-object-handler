from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from object.object import Object
from object.material import MATERIALS


class ExtrudedObject(Object):
    
    # Objeto 3D criado por extrusão de um polígono 2D.
    
    
    def __init__(self, base_vertices, depth, material='white_plastic', filled_segments=None):
        """
        Cria objeto 3D por extrusão
        
        Args:
            base_vertices: Lista de vértices 2D [[x,y,z], ...] que formam a base
            depth: Profundidade da extrusão (valor Z)
            material: Nome do material a ser aplicado
            filled_segments: Lista de segmentos preenchidos [(y, x1, x2), ...] do algoritmo de filling
        """
        # Inicializar classe pai
        super().__init__(shape='custom', material=material)
        
        self.base_vertices = base_vertices
        self.depth = depth
        self.filled_segments = filled_segments
        self.vertices_3d = []
        self.faces = []
        
        # Gerar geometria 3D 
        self._generate_geometry()
    
    def _generate_3d_geometry(self):
        """Extrusão simples do polígono base (fallback quando não há filling)."""
        base_count = len(self.base_vertices)
        if base_count < 3:
            print("Erro: Polígono base deve ter pelo menos 3 vértices")
            return

        # Vértices frente e trás a partir da base (já no espaço do mundo)
        self.vertices_3d = []
        front_indices = []
        back_indices = []
        for vx, vy, *_ in self.base_vertices:
            front_indices.append(len(self.vertices_3d))
            self.vertices_3d.append([vx, vy, 0.0])
        for vx, vy, *_ in self.base_vertices:
            back_indices.append(len(self.vertices_3d))
            self.vertices_3d.append([vx, vy, self.depth])

        # Faces
        self.faces = []
        self.faces.append(front_indices)
        back_face = back_indices[::-1]
        self.faces.append(back_face)
        for i in range(base_count):
            j = (i + 1) % base_count
            self.faces.append([front_indices[i], front_indices[j], back_indices[j], back_indices[i]])
    
    def _generate_geometry(self):
        """
        Geração unificada de geometria:
        - Se houver filled_segments, gera faces frontal e traseira com base no filling
        - Caso contrário, usa a extrusão simples com polígono base
        """
        if self.filled_segments:
            print(f"Gerando extrusão com dados de preenchimento ({len(self.filled_segments)} segmentos)")
            # Faces frontal e traseira guiadas por scanline
            self._build_front_back_from_fill()
            # Faces laterais: retângulos por aresta da base, com comprimento = profundidade
            self._build_laterals_from_base()
            # Não adicionar geometria interna: apenas planos que delimitam o objeto
            print(f"Geometria com preenchimento (apenas planos) gerada: {len(self.vertices_3d)} vértices, {len(self.faces)} faces")
        else:
            print("Gerando extrusão simples sem dados de preenchimento")
            self._generate_3d_geometry()

    def _build_front_back_from_fill(self):
        """
        Gera as faces frontal (z=0) e traseira (z=depth) usando os segmentos
        retornados por polygon_filling, construindo quads entre linhas y e y+1.
        """
        self.vertices_3d = []
        self.faces = []

        if not self.filled_segments:
            return

        # Obter dimensão da janela atual para converter tela -> mundo
        # Preferir tamanho do ImGui (setado em reshape); evitar chamar glutGet sem GLUT
        try:
            import imgui
            io = imgui.get_io()
            w, h = io.display_size
            if not w or not h:
                raise ValueError('imgui display_size not ready')
        except Exception:
            # Como fallback, tentar GLUT; se não estiver inicializado, usar defaults
            try:
                w = glutGet(GLUT_WINDOW_WIDTH)
                h = glutGet(GLUT_WINDOW_HEIGHT)
            except Exception:
                w, h = 800, 600
        # Usar mesma conversão de polygon_modeler._normalize_2d_to_3d para garantir alinhamento
        def screen_to_world(x, y):
            wx = ((x / w) - 0.5) * 10.0
            wy = ((y / h) - 0.5) * 10.0
            return wx, wy

        # Agrupar por y e também preparar pares y -> y+1
        by_y = {}
        for y, x1, x2 in self.filled_segments:
            by_y.setdefault(y, []).append((x1, x2))

        sorted_ys = sorted(by_y.keys())

        # Para cada par de linhas consecutivas, formar retângulos preenchidos
        for i in range(len(sorted_ys) - 1):
            y_curr = sorted_ys[i]
            y_next = sorted_ys[i + 1]

            # Converter Y de tela para mundo
            _, world_y_curr = screen_to_world(0, y_curr)
            _, world_y_next = screen_to_world(0, y_next)

            # segmentos atuais e próximos (assumindo mesma estrutura de preenchimento)
            segs_curr = sorted(by_y[y_curr], key=lambda s: s[0])
            segs_next = sorted(by_y[y_next], key=lambda s: s[0])

            # Estratégia simples: para cada segmento na linha atual, criar um quad "alto" de 1 linha
            # Isso aproxima a área preenchida entre y e y+1.
            for x1, x2 in segs_curr:
                # Converter X de tela para mundo
                world_x1, _ = screen_to_world(x1, 0)
                world_x2, _ = screen_to_world(x2, 0)

                # Vértices frente (z=0)
                v0 = [world_x1, world_y_curr, 0.0]
                v1 = [world_x2, world_y_curr, 0.0]
                v2 = [world_x2, world_y_next, 0.0]
                v3 = [world_x1, world_y_next, 0.0]

                base_idx = len(self.vertices_3d)
                self.vertices_3d.extend([v0, v1, v2, v3])
                self.faces.append([base_idx, base_idx + 1, base_idx + 2, base_idx + 3])

                # Vértices trás (z=depth)
                b0 = [world_x1, world_y_curr, self.depth]
                b1 = [world_x2, world_y_curr, self.depth]
                b2 = [world_x2, world_y_next, self.depth]
                b3 = [world_x1, world_y_next, self.depth]

                back_idx = len(self.vertices_3d)
                self.vertices_3d.extend([b0, b1, b2, b3])
                # Inverter ordem para normal apontar para fora
                self.faces.append([back_idx + 3, back_idx + 2, back_idx + 1, back_idx])

    def _build_laterals_from_base(self):
        """
        Cria faces laterais como retângulos por aresta do polígono base,
        com lado igual à aresta e comprimento igual à profundidade de extrusão.
        Usa os vértices da base no mesmo espaço do objeto.
        """
        if not self.base_vertices or len(self.base_vertices) < 2:
            return

        # Construir vértices frente/trás a partir da base (já em espaço do mundo)
        front_indices = []
        back_indices = []

        for vx, vy, *_ in self.base_vertices:
            front_indices.append(len(self.vertices_3d))
            self.vertices_3d.append([vx, vy, 0.0])
        for vx, vy, *_ in self.base_vertices:
            back_indices.append(len(self.vertices_3d))
            self.vertices_3d.append([vx, vy, self.depth])

        base_count = len(front_indices)
        # Para cada aresta do polígono base, criar retângulo lateral
        for i in range(base_count):
            j = (i + 1) % base_count
            self.faces.append([
                front_indices[i],
                front_indices[j],
                back_indices[j],
                back_indices[i]
            ])
    
    def _add_filled_internal_geometry(self):
        """
        Adiciona geometria interna baseada nos segmentos preenchidos.
        Preserva buracos em polígonos com auto-interseção.
        """
        if not self.filled_segments:
            return
        
        # Agrupar segmentos por linha Y
        y_lines = {}
        for y, x1, x2 in self.filled_segments:
            # Usar coordenadas diretamente
            world_y = y
            world_x1 = x1
            world_x2 = x2
            
            if world_y not in y_lines:
                y_lines[world_y] = []
            y_lines[world_y].append((world_x1, world_x2))
        
        # Criar faces internas apenas para segmentos preenchidos
        internal_vertices_start = len(self.vertices_3d)
        
        for world_y in sorted(y_lines.keys())[::5]:  # Usar apenas algumas linhas para performance
            x_segments = y_lines[world_y]
            
            for x1, x2 in x_segments:
                if abs(x2 - x1) < 0.1:  # Pular segmentos muito pequenos
                    continue
                
                # Criar vértices para este segmento horizontal
                # Face frontal (z=0)
                front_left = [x1, world_y, 0.0]
                front_right = [x2, world_y, 0.0]
                # Face traseira (z=depth)
                back_left = [x1, world_y, self.depth]
                back_right = [x2, world_y, self.depth]
                
                # Adicionar vértices
                v_idx = len(self.vertices_3d)
                self.vertices_3d.extend([front_left, front_right, back_left, back_right])
                
                # Criar face conectando frente e trás (quad interno)
                internal_face = [
                    v_idx,     # front_left
                    v_idx + 1, # front_right  
                    v_idx + 3, # back_right
                    v_idx + 2  # back_left
                ]
                self.faces.append(internal_face)
        
        added_vertices = len(self.vertices_3d) - internal_vertices_start
        print(f"Adicionadas {added_vertices} vértices internos baseados no preenchimento")

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
        # Regenerar usando caminho unificado para manter faces pelo filling quando existir
        self._generate_geometry()
    
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
