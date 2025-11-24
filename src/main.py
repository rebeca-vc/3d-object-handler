from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import imgui
from imgui.integrations.opengl import FixedPipelineRenderer as GlutRenderer
from camera import Camera
from control_panel import ControlPanelState, draw_control_panel 

# Variáveis globais
renderer = None
camera = Camera()
ui_state = ControlPanelState() 


## -------- MOUSE CONTROLS -------- ##

def mouse(button, state, x, y):
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


def draw_grid(size=10, step=1):
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


## -------- GLUT BASIC -------- ##

def display():
    global renderer, ui_state # Usamos o ui_state global

    # Início do frame do ImGui
    imgui.new_frame()

    # NOVO: Chamada para a função de desenho do painel de controle
    draw_control_panel(ui_state) 
    
    # --- Desenho da Cena OpenGL ---

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera update
    camera.update()
    gluLookAt(camera.camera_position_x, camera.camera_position_y, camera.camera_position_z,
              camera.focal_point_x, camera.focal_point_y, camera.focal_point_z,
              0, 1, 0)

    # Drawing Grid and Axes
    draw_axes()
    draw_grid()  

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
    renderer = GlutRenderer() 

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

    glutMainLoop()

if __name__ == "__main__":
    main()