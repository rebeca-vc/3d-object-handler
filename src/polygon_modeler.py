from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import os
from object.extruded_object import ExtrudedObject
# Importação direta do polygon-filling modificado
sys.path.append(os.path.join(os.path.dirname(__file__), 'polygon-filling'))

from polygon_modeling import PolygonEditor


class AppState:
    """Estados da aplicação para controlar modo de renderização"""
    NORMAL_3D = "3d_mode"
    POLYGON_MODELING = "polygon_mode"


class PolygonModeler:
    """
    Gerenciador de modelagem poligonal com integração direta
    ao polygon-filling modificado.
    """
    
    def __init__(self):
        self.state = AppState.NORMAL_3D
        self.modeling_data = {
            'depth': 3.0,
            'completion_callback': None
        }
        # Usar editor de polígonos
        self.polygon_editor = PolygonEditor()
        
    def is_modeling_active(self):
        """Verifica se está no modo de modelagem"""
        return self.polygon_editor.is_active
    
    def start_modeling(self, depth, completion_callback):
        """Inicia modo de modelagem poligonal"""
        print(f"Iniciando modelagem poligonal com profundidade {depth}")
        
        self.state = AppState.POLYGON_MODELING
        self.modeling_data['depth'] = depth
        self.modeling_data['completion_callback'] = completion_callback
        
        # Configurar callback de finalização
        def on_polygon_complete(polygon):
            self._finalize_polygon(polygon)
        
        # Iniciar edição no polygon-filling
        self.polygon_editor.start_modeling(on_polygon_complete)
        
        # Configurar projeção 2D
        self._setup_2d_projection()
        
    def stop_modeling(self):
        """Finaliza modo de modelagem e volta ao 3D"""
        print("Finalizando modelagem poligonal")
        
        self.state = AppState.NORMAL_3D
        self.polygon_editor.stop_modeling()
        
        # Restaurar configuração 3D
        self._restore_3d_projection()
    
    def handle_mouse(self, button, state, x, y):
        """
        Processa eventos de mouse durante modelagem
        
        Returns:
            bool: True se evento foi processado, False caso contrário
        """
        if not self.is_modeling_active():
            return False
        
        # Delegar para o editor de polígonos
        return self.polygon_editor.handle_mouse(button, state, x, y)
    
    def render_modeling_interface(self):
        """Renderiza interface 2D para modelagem"""
        if not self.is_modeling_active():
            return
        
        # Delegar para o editor de polígonos
        self.polygon_editor.render()
    
    def _finalize_polygon(self, polygon):
        """Finaliza polígono e cria objeto 3D extrudado"""
        if polygon and len(polygon.vertices) >= 3:
            # Verificar se polígono é válido para extrusão
            if not polygon.is_valid_for_extrusion():
                print("Erro: polígono inválido - contém pontos colineares")
                self.stop_modeling()
                return
            
            # Converter para objeto 3D
            extruded_obj = self._create_extruded_object(
                polygon.vertices, 
                self.modeling_data['depth']
            )
            
            # Chamar callback para adicionar à cena
            callback = self.modeling_data['completion_callback']
            if callback:
                callback(extruded_obj)
                print(f"Objeto extrudado criado e adicionado à cena")
            else:
                print("Erro: callback de conclusão não definido")
        else:
            print("Erro: polígono precisa de pelo menos 3 pontos")
        
        # Voltar para modo 3D
        self.stop_modeling()
    
    def _create_extruded_object(self, vertices_2d, depth):
        """Cria objeto 3D por extrusão"""
        # Normalizar coordenadas 2D para espaço 3D
        normalized_vertices = self._normalize_2d_to_3d(vertices_2d)
        
        # Criar objeto extrudado
        extruded_obj = ExtrudedObject(
            base_vertices=normalized_vertices,
            depth=depth,
            material='white_plastic'
        )
        
        return extruded_obj
    
    def _normalize_2d_to_3d(self, vertices_2d):
        """Converte coordenadas de tela para mundo 3D"""
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)
        
        world_vertices = []
        for x, y in vertices_2d:
            # Converter tela → [-5, 5] no plano XY (Z=0)
            world_x = ((x / w) - 0.5) * 10.0
            world_y = ((y / h) - 0.5) * 10.0
            world_vertices.append([world_x, world_y, 0.0])
        
        return world_vertices
    
    def _setup_2d_projection(self):
        """Configura projeção ortográfica 2D para modelagem"""
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)
        
        # Delegar para o editor de polígonos
        self.polygon_editor.setup_2d_projection(w, h)
    
    def _restore_3d_projection(self):
        """Restaura projeção 3D original"""
        # Reabilitar funcionalidades 3D
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # A projeção será reconfigurada no próximo frame via projection_setup()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()