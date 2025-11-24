import imgui

"""
    Gerencia o estado de todas as variáveis controladas pelo Painel ImGui.
"""
class ControlPanelState:
 
    def __init__(self):
        # Seleção de Objeto 3D
        self.object_options = ["Cubo", "Esfera", "Teapot", "Pirâmide"]
        self.object_selected_index = 0

        # Cores 
        self.object_color = (1.0, 1.0, 1.0) 

        # Material do Objeto
        self.object_material_options = ["Plástico", "Borracha", "Metal", "Ouro"]
        self.object_material_selected_index = 0
        
        # Profundidade do Polígono Arbitrário 
        self.polygon_depth_options = [str(i) for i in range(3, 11)] 
        self.polygon_depth_index = 0
        
        # Opções de Iluminação (Lightning)
        self.lightning_options = ["Flat", "Gouraud", "Phong"]
        self.lightning_selected_index = 0
        
        # Opções de Projeção
        self.projection_options = ["Paralelo", "Perspectiva"]
        self.projection_selected_index = 1 

        # Componentes de Luz
        self.ambient_light = True
        self.difuse_light = True
        self.specular_light = True

"""
    Desenha a janela e todos os widgets do Painel de Controle usando ImGui.
    Recebe um objeto ControlPanelState para ler/modificar o estado.
"""
def draw_control_panel(state: ControlPanelState):
    # Flags para travar a janela
    window_flags = imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE
    imgui.set_next_window_size(400, 500)
    
    # Aplica as flags
    is_open, _ = imgui.begin("Painel de Controle", flags=window_flags)
    
    if is_open:

        # OBJETOS

        imgui.text("Adição de Objetos Primitivos")
        
        changed, state.object_selected_index = imgui.combo(
            "Objeto 3D", 
            state.object_selected_index, 
            state.object_options
        )
        
        # Cor do Material (Exemplo)
        changed_color, state.object_color = imgui.color_edit3("Cor do Material", *state.object_color)
        if changed_color:
            print(f"Cor alterada para: {state.object_color}")

        changed, state.object_material_selected_index = imgui.combo(
            "Material", 
            state.object_material_selected_index, 
            state.object_material_options
        )
        
        imgui.text("")

        if imgui.button("Adicionar Objeto"):
            print(f"Adicionando objeto!")
            print(f"Objeto: {state.object_options[state.object_selected_index]}")
            print(f"Cor: {state.object_color}")
            print(f"Material: {state.object_material_options[state.object_material_selected_index]}")

        imgui.text("")
        # --- Seção de Objeto Arbitrário --- #

        imgui.separator()

        imgui.text("Objeto Poligonal Arbitrário")
        
        changed_depth, state.polygon_depth_index = imgui.combo(
            "Profundidade", 
            state.polygon_depth_index, 
            state.polygon_depth_options
        )

        imgui.text(f"Profunidade: {state.polygon_depth_options[state.polygon_depth_index]}")

        
        imgui.text("")
        if imgui.button("Iniciar Modelagem"):
            print(f"Abrindo modelagem com {state.polygon_depth_options[state.polygon_depth_index]} de profundidade!")
        imgui.text("")

        imgui.separator()

        # --- Seção de Configuração Gráfica --- #
        imgui.text("Configurações de Renderização")

        # Projeção
        changed_proj, state.projection_selected_index = imgui.combo(
            "Projeção", 
            state.projection_selected_index, 
            state.projection_options
        )
        if changed_proj:
            print(f"Projeção alterada para: {state.projection_options[state.projection_selected_index]}")

        # Iluminação
        changed_light, state.lightning_selected_index = imgui.combo(
            "Modelo de Shading", 
            state.lightning_selected_index, 
            state.lightning_options
        )
        if changed_light:
            print(f"Shading alterado para: {state.lightning_options[state.lightning_selected_index]}")

        # Componentes de Luz
        imgui.text("Componentes da Luz:")
        _, state.ambient_light = imgui.checkbox("Ambiente", state.ambient_light)
        _, state.difuse_light = imgui.checkbox("Difusa", state.difuse_light)
        _, state.specular_light = imgui.checkbox("Especular", state.specular_light)

        imgui.text("")
        if imgui.button("Adicionar fonte de luz"):
            print(f"Adicionando fonte de luz")
        imgui.text("")

    imgui.end()
