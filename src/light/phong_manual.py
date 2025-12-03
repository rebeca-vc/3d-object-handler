from OpenGL.GL import *
from OpenGL.GLU import *
import math
from light.math_utils import *

class PhongManual:
    def __init__(self):
        self.width = 800
        self.height = 600

    def update_size(self, width, height):
        self.width = int(width)
        self.height = int(height)

    """
    Rasterização manual (Scanline) com iluminação Phong por pixel.
    Usa GL_POINTS para aproveitar o Z-Buffer do OpenGL.
    """
    def render_object(self, obj, camera_pos, light_pos, light_colors):

        # Captura as matrizes DO CENÁRIO 3D ATUAL (para projetar os vértices corretamente)
        model_view = glGetDoublev(GL_MODELVIEW_MATRIX) 
        projection = glGetDoublev(GL_PROJECTION_MATRIX) 
        viewport = glGetIntegerv(GL_VIEWPORT) 
        
        
        vertices = obj.vertices_3d
        faces = obj.faces

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity() 

        glPointSize(1.7)
        glDisable(GL_LIGHTING) 

        glEnable(GL_DEPTH_TEST) 

        glBegin(GL_POINTS)

        
        # Triangulação: Vamos usar apenas os triângulos dos objetos
        for face in faces:
            pivot = face[0] # Pivo: é o vértice principal para fazer a triangulação por leque
            for i in range(1, len(face) - 1): # Iteramos sobre todos os vértices para tansformar a face em triângulos
                indice_vertice1 = face[i] 
                indice_vertice2 = face[i+1]
                
                triangle_vertex0 = vertices[pivot]
                triangle_vertex1 = vertices[indice_vertice1]
                triangle_vertex2 = vertices[indice_vertice2]
                
                # print(triangle_vertex0, triangle_vertex1, triangle_vertex2)
                # Rasteriza cada triângulo da face
                self._rasterize_triangle(triangle_vertex0, triangle_vertex1, triangle_vertex2, model_view, projection, viewport, camera_pos, light_pos, light_colors, obj.material)
        
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_LIGHTING)

    # Auxiliar para interpolação linear entre dois dicionários de atributos
    def interp(self, d1, d2, factor):
        res = {}
        for k in d1:
            res[k] = d1[k] + (d2[k] - d1[k]) * factor
        return res

    # Função que desenha uma linha horizontal (Span)
    def draw_scanline(self, y, pa, pb, cam_pos, light_pos, light_colors, material, viewport):

        # Ordenar da esquerda (pa) para direita (pb)
        if pa['x'] > pb['x']: pa, pb = pb, pa

        # Pegando valores para passar na linha do Y
        x_start = int(math.floor(pa['x']))
        x_end = int(math.floor(pb['x']))
        
        dx = pb['x'] - pa['x']
        if dx <= 0: 
            return

        # Loop X (Span)
        for x in range(x_start, x_end):
            # Fator de interpolação horizontal 
            # x - x0 / x1 - x0 
            factor = (x - pa['x']) / dx
            
            # --- PHONG SHADING MANUAL  --- #
            
            # Interpolando posição no espaço (para a luz e para o glVertex3f)
            # y0 + (y1 - y0) * (x - x0 / x1 - x0 ) --> interpolação linear
            pos_eye = (
                pa['wx'] + (pb['wx'] - pa['wx']) * factor,
                pa['wy'] + (pb['wy'] - pa['wy']) * factor,
                pa['wz'] + (pb['wz'] - pa['wz']) * factor
            )

            # Interpolando Normal
            norm_eye = (
                pa['nx'] + (pb['nx'] - pa['nx']) * factor,
                pa['ny'] + (pb['ny'] - pa['ny']) * factor,
                pa['nz'] + (pb['nz'] - pa['nz']) * factor
            )

            norm_eye = normalize(norm_eye) # Renormalizar após interpolação

            # Vetores de Iluminação
            # V (View) = vetor da posição para a câmera (0,0,0 no eye space)
            V = normalize((-pos_eye[0], -pos_eye[1], -pos_eye[2]))
            
            # L (Light) = vetor da posição para a luz
            # Assumindo l_pos posicional
            L = normalize(sub(light_pos, pos_eye))
            
            # Cálculo da Cor (Phong)
            
            # Componente Ambiente
            # Componente_Ambiente = Ia . Ka

            # material.ambient = Ka 
            # light_colors['amb'] = Ia 
            amb = [material.ambient[i] * light_colors['amb'][i] for i in range(3)]
            
            # Componente Difusa (Lambert)
            # Componente_Difusa = I1 . Kd * cos(theta)
            
            # cos(theta) = Normal . Luz
            # material.diffuse = Kd
            # light_colors['dif'] = I1
            NdotL = max(dot(norm_eye, L), 0.0)
            diff = [material.diffuse[i] * light_colors['dif'][i] * NdotL for i in range(3)]
            
            # Componente Especular (Phong)
            # I1 . Ks . cos^n(alpha)

            # cos(alpha) = Reflection * Vetor para o olho/camera
            # material.shininess = n
            # material.specular = Ks  
            # light_colors['spec'] = I1
            spec = [0, 0, 0]
            if NdotL > 0.0:
                # R = reflect(-L, N)
                R = reflect(sub((0,0,0), L), norm_eye)
                spec_val = pow(max(dot(R, V), 0.0), material.shininess) # Definindo intensidade de brilho
                spec = [material.specular[i] * light_colors['spec'][i] * spec_val for i in range(3)]
            
            # Cor final: I = ambiente + difusa + especular
            final_color = (
                min(1.0, amb[0] + diff[0] + spec[0]),
                min(1.0, amb[1] + diff[1] + spec[1]),
                min(1.0, amb[2] + diff[2] + spec[2])
            )
            
            # DESENHO E Z-BUFFER
            glColor3f(*final_color)

            # Posição 3D interpolada.
            # O OpenGL projeta ela novamente, calcula o Z e compara com o Depth Buffer existente.
            glVertex3f(pos_eye[0], pos_eye[1], pos_eye[2])

    def project(self, v_obj, mv, normal, proj, vp):
        """Projeta vértice para Tela (X,Y) e Espaço do Olho (3D)"""
        x, y, z = v_obj
        
        # A função gluProject mapeia coordenadas de objeto para coordenadas de janela.
        win_x, win_y, win_z = gluProject(x, y, z, mv, proj, vp)
        
        # Coordenadas do vértice vista pela câmera
        # P_eye = ModelView * P_obj
        camera_view_x = mv[0][0]*x + mv[1][0]*y + mv[2][0]*z + mv[3][0]
        camera_view_y = mv[0][1]*x + mv[1][1]*y + mv[2][1]*z + mv[3][1]
        camera_view_z = mv[0][2]*x + mv[1][2]*y + mv[2][2]*z + mv[3][2]

        # Rotacionar normal - O Model View determina para onde estou "olhando"
        ne_x = mv[0][0]*normal[0] + mv[1][0]*normal[1] + mv[2][0]*normal[2]
        ne_y = mv[0][1]*normal[0] + mv[1][1]*normal[1] + mv[2][1]*normal[2]
        ne_z = mv[0][2]*normal[0] + mv[1][2]*normal[1] + mv[2][2]*normal[2]
        
        return {
            'x': win_x, 
            'y': win_y,       
            'win_z': win_z,       
            'wx': camera_view_x, 
            'wy': camera_view_y, 
            'wz': camera_view_z, 
            'nx': ne_x, 
            'ny': ne_y, 
            'nz': ne_z  
        }

    def _rasterize_triangle(self, v0, v1, v2, mv, proj, vp, cam_pos, l_pos, l_cols, material):

        # ---- PROJETAR ---- #
        tri_normal = normalize(cross(sub(v1, v0), sub(v2, v0))) 
        p0 = self.project(v0, mv, tri_normal, proj, vp)
        p1 = self.project(v1, mv, tri_normal, proj, vp)
        p2 = self.project(v2, mv, tri_normal, proj, vp)

        # ordenar por y
        pts = sorted([p0, p1, p2], key=lambda p: p['y'])

        # criar ET (Edge Table) para o triângulo
        ET = {}

        # Função colocada dentro de rasterize para facilitar o uso do ET como var global dentro do contexto da func
        def add_edge(pa, pb):
            if pa['y'] == pb['y']:
                return 

            # assegurar que pa é o menor y
            if pa['y'] > pb['y']:
                pa, pb = pb, pa

            dy = pb['y'] - pa['y']
            if dy == 0:
                return

            edge = {
                'ymax': pb['y'],
                'x': pa['x'],
                'dx': (pb['x'] - pa['x']) / dy,

                'wx': pa['wx'],
                'd_wx': (pb['wx'] - pa['wx']) / dy,

                'wy': pa['wy'],
                'd_wy': (pb['wy'] - pa['wy']) / dy,

                'wz': pa['wz'],
                'd_wz': (pb['wz'] - pa['wz']) / dy,

                'win_z': pa['win_z'],
                'd_win_z': (pb['win_z'] - pa['win_z']) / dy,

                'nx': pa['nx'],
                'd_nx': (pb['nx'] - pa['nx']) / dy,

                'ny': pa['ny'],
                'd_ny': (pb['ny'] - pa['ny']) / dy,

                'nz': pa['nz'],
                'd_nz': (pb['nz'] - pa['nz']) / dy,
            }

            y0 = int(pa['y'])
            if y0 not in ET:
                ET[y0] = []
            ET[y0].append(edge)

        # criar arestas do triângulo
        add_edge(pts[0], pts[1])
        add_edge(pts[1], pts[2])
        add_edge(pts[0], pts[2])

        if not ET:
            return

        # ---- AET - Active Edge Table ---- #
        AET = []

        y = min(ET.keys())
        y_max_global = int(max(p['y'] for p in pts))

        # ---- LOOP DE SCANLINE ---- #
        while y <= y_max_global:

            # ativar arestas que começam neste y
            if y in ET:
                AET.extend(ET[y])

            # remover arestas que terminam neste y
            AET = [e for e in AET if e['ymax'] > y]

            if len(AET) < 2:
                # sem dois lados para formar um span
                y += 1
                # atualizar arestas
                for e in AET:
                    e['x'] += e['dx']
                    e['wx'] += e['d_wx']
                    e['wy'] += e['d_wy']
                    e['wz'] += e['d_wz']
                    e['win_z'] += e['d_win_z']
                    e['nx'] += e['d_nx']
                    e['ny'] += e['d_ny']
                    e['nz'] += e['d_nz']
                continue

            # ordenar por X
            AET.sort(key=lambda e: e['x'])

            e1 = AET[0]
            e2 = AET[-1]

            # construir PA e PB (classe draw_scanline irá interpolar)
            PA = {
                'x': e1['x'],
                'wx': e1['wx'],
                'wy': e1['wy'],
                'wz': e1['wz'],
                'win_z': e1['win_z'],
                'nx': e1['nx'],
                'ny': e1['ny'],
                'nz': e1['nz'],
            }

            PB = {
                'x': e2['x'],
                'wx': e2['wx'],
                'wy': e2['wy'],
                'wz': e2['wz'],
                'win_z': e2['win_z'],
                'nx': e2['nx'],
                'ny': e2['ny'],
                'nz': e2['nz'],
            }

            # print(y, PA, PB, cam_pos, l_pos, l_cols, material)
            self.draw_scanline(y, PA, PB, cam_pos, l_pos, l_cols, material, vp)

            # incrementar Y e atualizar atributos das arestas
            y += 1

            for e in AET:
                e['x'] += e['dx']
                e['wx'] += e['d_wx']
                e['wy'] += e['d_wy']
                e['wz'] += e['d_wz']
                e['win_z'] += e['d_win_z']
                e['nx'] += e['d_nx']
                e['ny'] += e['d_ny']
                e['nz'] += e['d_nz']