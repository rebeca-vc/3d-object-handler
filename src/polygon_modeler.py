from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import os
from object.extruded_object import ExtrudedObject
from polygon_filling.polygon_modeling import PolygonEditor


class AppState:
    """Estados da aplicação: alterna entre modo 3D e modelagem 2D."""
    NORMAL_3D = "3d_mode"
    POLYGON_MODELING = "polygon_mode"


class PolygonModeler:
    """Gerencia modelagem 2D (scanline) e cria extrusão 3D correspondente."""
    
    def __init__(self):
        self.state = AppState.NORMAL_3D
        self.modeling_data = {
            'depth': 3.0,
            'completion_callback': None
        }
        # Usar editor de polígonos
        self.polygon_editor = PolygonEditor()
        
    def is_modeling_active(self):
        """Indica se editor está ativo para captura de pontos 2D."""
        return self.polygon_editor.is_active
    
    def start_modeling(self, depth, completion_callback):
        """Inicia modelagem 2D com profundidade alvo e callback de conclusão."""
        print(f"Iniciando modelagem poligonal com profundidade {depth}")
        
        self.state = AppState.POLYGON_MODELING
        self.modeling_data['depth'] = depth
        self.modeling_data['completion_callback'] = completion_callback
        
        # Configurar callback de finalização
        def on_polygon_complete(polygon):
            self._finalize_polygon(polygon)
        
        # Iniciar edição no polygon-filling (entrada de vértices)
        self.polygon_editor.start_modeling(on_polygon_complete)
        
        # Configurar projeção 2D para desenhar HUD e polígono
        self._setup_2d_projection()
        
    def stop_modeling(self):
        """Finaliza modelagem 2D e restaura contexto 3D."""
        print("Finalizando modelagem poligonal")
        
        self.state = AppState.NORMAL_3D
        self.polygon_editor.stop_modeling()
        
        # Restaurar configuração 3D
        self._restore_3d_projection()
    
    def handle_mouse(self, button, state, x, y):
        """Encaminha eventos de mouse ao editor enquanto ativo (True/False)."""
        if not self.is_modeling_active():
            return False
        
        # Delegar para o editor de polígonos
        return self.polygon_editor.handle_mouse(button, state, x, y)
    
    def render_modeling_interface(self):
        """Renderiza preenchimento (scanline), bordas e vértices em 2D."""
        if not self.is_modeling_active():
            return
        
        # Delegar para o editor de polígonos
        self.polygon_editor.render()
    
    def _finalize_polygon(self, polygon):
        """Valida polígono, obtém `filled_segments` e instancia `ExtrudedObject`."""
        if polygon and len(polygon.vertices) >= 3:
            # Verificar se polígono é válido para extrusão
            if not polygon.is_valid_for_extrusion():
                print("Erro: polígono inválido - contém pontos colineares")
                self.stop_modeling()
                return
            
            # Garantir que temos os dados de preenchimento
            filled_segments = getattr(polygon, 'filled_segments', None)
            
            if filled_segments:
                print(f"Criando objeto 3D com {len(filled_segments)} segmentos de preenchimento")
                
                # Analisar se há buracos para feedback
                y_lines = {}
                for y, x1, x2 in filled_segments:
                    if y not in y_lines:
                        y_lines[y] = 0
                    y_lines[y] += 1
                
                holes = sum(1 for count in y_lines.values() if count > 1)
                if holes > 0:
                    print(f"  → Polígono com buracos detectados em {holes} linhas")
                else:
                    print("  → Polígono sólido (sem buracos)")
            else:
                print("Aviso: Criando objeto 3D sem dados de preenchimento")
            
            # Converter para objeto 3D com dados de preenchimento
            extruded_obj = self._create_extruded_object(
                polygon.vertices, 
                self.modeling_data['depth'],
                filled_segments
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
    
    def _create_extruded_object(self, vertices_2d, depth, filled_segments=None):
        """Normaliza pontos 2D → mundo e cria `ExtrudedObject` com fill opcional."""
        # Normalizar coordenadas 2D para espaço 3D
        normalized_vertices = self._normalize_2d_to_3d(vertices_2d)
        
        # Criar objeto extrudado com dados de preenchimento
        extruded_obj = ExtrudedObject(
            base_vertices=normalized_vertices,
            depth=depth,
            material='white_plastic',
            filled_segments=filled_segments
        )
        
        return extruded_obj
    
    def _normalize_2d_to_3d(self, vertices_2d):
        """Tela (pixels) → mundo ([-5,5] em XY), Z=0 para extrusão posterior."""
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
        """Projeção ortográfica 2D para edição e visualização do polígono."""
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)
        
        # Delegar para o editor de polígonos
        self.polygon_editor.setup_2d_projection(w, h)
    
    def _restore_3d_projection(self):
        """Reabilita 3D (depth + lighting) e limpa matriz de projeção."""
        # Reabilitar funcionalidades 3D
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # A projeção será reconfigurada no próximo frame via projection_setup()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()