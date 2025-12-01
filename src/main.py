from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import imgui
from imgui.integrations.opengl import ProgrammablePipelineRenderer # troquei pra resolver a hud
from camera import Camera
from control_panel import ControlPanelState, draw_control_panel 
from object.objects import Object
from polygon_modeler import PolygonModeler

# Variáveis globais
renderer = None
camera = Camera()
ui_state = ControlPanelState() 
objects: list[Object] = []
polygon_modeler = PolygonModeler()
light_enabled = False
light_position = [2.0, 5.0, 2.0, 1.0] 

def add_object_to_scene(obj: Object):
    """Adiciona um objeto à lista global de objetos da cena."""
    objects.append(obj)
    print(f"Objeto adicionado à cena. Total de objetos: {len(objects)}")

def start_polygon_modeling(depth, completion_callback):
    """Inicia modo de modelagem poligonal."""
    polygon_modeler.start_modeling(depth, completion_callback)


## -------- MOUSE CONTROLS -------- ##

def mouse(button, state, x, y):
    # Primeiro verificar se está em modo de modelagem
    if polygon_modeler.handle_mouse(button, state, x, y):
        return  # Evento processado pela modelagem
    
    # Processamento normal do mouse para modo 3D
    io = imgui.get_io()
    
    # 1. ATUALIZAÇÃO IMGUI
    io.mouse_pos = x, y 
    if button >= 0 and button < 3: 
        io.mouse_down[button] = (state == GLUT_DOWN)

    # 2. VERIFICAÇÃO DE INTERAÇÃO IMGUI
    if io.want_capture_mouse:
        return
    
    # 3. CONTROLE DA CÂMERA 
    if state == GLUT_DOWN:
        camera.start_mouse(button, x, y) 

    if button == 3:
        camera.dolly(-1)
    elif button == 4:
        camera.dolly(1)


def motion(x, y):
    # Se está em modelagem, não processar movimento da câmera
    if polygon_modeler.is_modeling_active():
        return
    
    io = imgui.get_io()
    
    # 1. ATUALIZAÇÃO IMGUI 
    io.mouse_pos = x, y
    
    # 2. VERIFICAÇÃO DE INTERAÇÃO IMGUI
    if io.want_capture_mouse:
        return
    
    # 3. CONTROLE DA CÂMERA 
    # Move a câmera com as novas coordenadas.
    camera.move_mouse(x, y)


## -------- GRID AND AXES -------- ##

def draw_axes():
    # Desabilita iluminação para que as cores apareçam direto
    glDisable(GL_LIGHTING)
    
    glBegin(GL_LINES)

    # Eixo X em vermelho
    glColor3f(1, 0, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f( 10, 0, 0)

    # Eixo Y em verde
    glColor3f(0, 1, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(0,  10, 0)

    # Eixo Z em azul
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -10)
    glVertex3f(0, 0,  10)

    glEnd()
    
    # Reabilita iluminação para os objetos
    glEnable(GL_LIGHTING)


def draw_grid(size=10, step=1):
    # Desabilita iluminação para que a cor da grid apareça
    glDisable(GL_LIGHTING)
    
    glColor3f(0.4, 0.4, 0.4)  # cor da malha

    glBegin(GL_LINES)
    for i in range(-size, size + 1, step):
        # Linhas paralelas ao eixo X (varrendo Z)
        glVertex3f(-size, 0, i)
        glVertex3f( size, 0, i)

        # Linhas paralelas ao eixo Z (varrendo X)
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0,  size)
    glEnd()
    
    # Reabilita iluminação
    glEnable(GL_LIGHTING)

## -------- KEYBOARD CONTROLS -------- ##

def keyboard(key, x, y):
    global light_position, light_enabled
    step = 0.5 # Velocidade de movimento da luz

    if light_enabled:
        if key == GLUT_KEY_LEFT:
            light_position[0] -= step # Move -X
        elif key == GLUT_KEY_RIGHT:
            light_position[0] += step # Move +X
        elif key == GLUT_KEY_UP:
            light_position[2] -= step # Move -Z
        elif key == GLUT_KEY_DOWN:
            light_position[2] += step # Move +Z

        # Movimentação no eixo Y
        elif key == b'w': 
            light_position[1] += step
        elif key == b's':
            light_position[1] -= step

        glutPostRedisplay() # Redesenha a cena para ver a luz se mover

## -------- GLUT BASIC -------- ##

def display():
    global renderer, ui_state 

    # Início do frame do ImGui
    imgui.new_frame()

    # Chamada para a função de desenho do painel de controle com modelagem
    draw_control_panel(ui_state, add_object_to_scene, start_polygon_modeling, add_light_source, clear_scene, light_enabled)
    
    # Verificar se está em modo de modelagem
    if polygon_modeler.is_modeling_active():
        # Renderização 2D para modelagem
        glClear(GL_COLOR_BUFFER_BIT)
        polygon_modeler.render_modeling_interface()
    else:
        # Renderização 3D normal
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)
        projection_setup(w, h, ui_state)


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Camera update
        camera.update()
        gluLookAt(camera.camera_position_x, camera.camera_position_y, camera.camera_position_z,
                  camera.focal_point_x, camera.focal_point_y, camera.focal_point_z,
                  0, 1, 0)
        
        shading_setup(ui_state)
        light_setup(ui_state, GL_LIGHT0)

        if light_enabled:
            glLightfv(GL_LIGHT1, GL_POSITION, light_position)

            # Desenha um marcador para a luz (opcional)
            glDisable(GL_LIGHTING)
            glPushMatrix()
            glTranslatef(light_position[0], light_position[1], light_position[2])
            glColor3f(1.0, 1.0, 0.0) # Luz amarela
            glutWireSphere(0.2, 8, 8) # Desenha uma esfera
            glPopMatrix()
            glEnable(GL_LIGHTING)


        # Drawing Grid and Axes
        draw_axes()
        draw_grid()

        # Desenha cada objeto
        for obj in objects:
            obj.draw()

    # --- Renderização do ImGui ---
    imgui.render()
    renderer.render(imgui.get_draw_data())

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # A projeção deve ser ajustada com base no ui_state se quisermos alternar entre paralela/perspectiva
    # Por agora, mantemos a perspectiva, mas a lógica de escolha pode vir do ui_state.projection_selected_index
    gluPerspective(60.0, w / float(h), 0.1, 100.0)
    
    imgui.get_io().display_size = w, h

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

def projection_setup(width, height, ui_state):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect_ratio = width / height if height > 0 else 1.0
    projection_mode = ui_state.projection_options[ui_state.projection_selected_index]

    if projection_mode == 'Perspectiva':
        gluPerspective(60.0, aspect_ratio, 0.1, 100.0) 

    elif projection_mode == 'Paralelo':
        view_radius = 5.0 
        
        if aspect_ratio >= 1:
            glOrtho(-view_radius * aspect_ratio, view_radius * aspect_ratio, 
                    -view_radius, view_radius, 
                    0.1, 100.0)
        else:
            glOrtho(-view_radius, view_radius, 
                    -view_radius / aspect_ratio, view_radius / aspect_ratio, 
                    0.1, 100.0)
            
    glMatrixMode(GL_MODELVIEW)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)  # se escalas variadas forem usadas

def clear_scene():
    """Remove todos os objetos da lista global de objetos da cena."""
    global objects
    print(f"Limpando a cena. Total de objetos removidos:")
    objects.clear()


def shading_setup(ui_state):
    shading_mode = ui_state.lightning_options[ui_state.lightning_selected_index]

    if shading_mode == 'Flat':
        glShadeModel(GL_FLAT)
        # O Flat shading usa a cor e a normal do primeiro vértice do polígono.
        # Todos os pixels do polígono terão a mesma cor.
        
    elif shading_mode == 'Gouraud':
        glShadeModel(GL_SMOOTH)
        # O Smooth shading (Gouraud no OpenGL) interpola as cores
        # calculadas nos vértices pelos pixels do polígono.
        
    elif shading_mode == 'Phong':
        # Para Phong, que exige shaders, você fará:
        # 1. Ativar o programa shader (se implementado)
        # 2. Passar as variáveis uniformes (luz, material, câmera) para o shader.
        # Por enquanto, vamos manter o Gouraud (Smooth) como fallback visual:
        glShadeModel(GL_SMOOTH) 
        print("Atenção: Phong shading requer shaders GLSL, usando Gouraud como fallback.")

def light_setup(ui_state, light_id):
    # Valores base
    ambience_base = [0.1, 0.1, 0.1, 1.0]
    difuse_base = [0.8, 0.8, 0.8, 1.0]
    specular_base = [1.0, 1.0, 1.0, 1.0]
    
    # Aplicar 0.0 se o componente não estiver ativo no painel
    ambient = ambience_base if ui_state.ambient_light else [0.0, 0.0, 0.0, 1.0]
    difuse = difuse_base if ui_state.difuse_light else [0.0, 0.0, 0.0, 1.0]
    specular = specular_base if ui_state.specular_light else [0.0, 0.0, 0.0, 1.0]
    
    # Aplica os vetores de cor na fonte de luz (LIGHT0, por exemplo)
    glLightfv(light_id, GL_AMBIENT, ambient)
    glLightfv(light_id, GL_DIFFUSE, difuse)
    glLightfv(light_id, GL_SPECULAR, specular)
    
    # Se todos os componentes estiverem desligados, desligamos a luz.
    if not ui_state.ambient_light and not ui_state.difuse_light and not ui_state.specular_light:
        glDisable(light_id)
    else:
        glEnable(light_id)

def add_light_source():
    """Ativa a fonte de luz e a configura na cena."""
    global light_enabled

    if not light_enabled:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT1) # Usar LIGHT1 para nossa luz móvel (LIGHT0 é para a luz padrão)

        # Cor da luz (ex: branca)
        light_ambient  = [0.2, 0.2, 0.2, 1.0]
        light_diffuse  = [0.8, 0.8, 0.8, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]

        glLightfv(GL_LIGHT1, GL_AMBIENT,  light_ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE,  light_diffuse)
        glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)

        # Configura a posição inicial (será feita no `display` também)
        glLightfv(GL_LIGHT1, GL_POSITION, light_position)

        light_enabled = True
        print("Fonte de luz LIGHT1 adicionada e ativada.")
    else:
        print("A fonte de luz LIGHT1 já está ativa.")


def main():
    global renderer

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    screen_width = glutGet(GLUT_SCREEN_WIDTH)
    screen_height = glutGet(GLUT_SCREEN_HEIGHT)
    
    window_width = screen_width - 100  
    window_height = screen_height - 100
    
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(50, 50)  
    glutCreateWindow(b"Trabalho 2")

    # Inicialização do ImGui
    imgui.create_context()
    renderer = ProgrammablePipelineRenderer() 

    init()
    
    # Forçar a chamada de reshape para configurar o tamanho inicial (DisplaySize)
    current_width = glutGet(GLUT_WINDOW_WIDTH)
    current_height = glutGet(GLUT_WINDOW_HEIGHT)
    reshape(current_width, current_height) 

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutReshapeFunc(reshape) 
    glutSpecialFunc(keyboard) 
    glutKeyboardFunc(keyboard) 

    glutMainLoop()

if __name__ == "__main__":
    main()