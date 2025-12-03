from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import imgui
from imgui.integrations.opengl import ProgrammablePipelineRenderer 

from ui_controls.camera import Camera
from ui_controls.control_panel import ControlPanelState, draw_control_panel 
from object.object import Object
from polygon_modeler import PolygonModeler
from input_handlers import keyboard, mouse, motion
from light.lighting_models import LightingController
from light.shading_controller import ShadingController
from light.phong_manual import PhongManual

renderer = None
camera = Camera()
ui_state = ControlPanelState() 
objects: list[Object] = []
selected_objects: list[Object] = []  
polygon_modeler = PolygonModeler()
lighting_controller = LightingController()
phong_manual = PhongManual()
shading_controller = None

## -------- OBJECT CONTROLS ------- ##

def add_object_to_scene(obj: Object):
    """Adiciona um objeto à lista global de objetos da cena."""
    # Aplicar a cor selecionada no painel ao objeto adicionado
    try:
        r, g, b = ui_state.object_color
        obj.set_color(r, g, b)
    except Exception:
        pass
    objects.append(obj)
    print(f"Objeto adicionado à cena. Total de objetos: {len(objects)}")

def start_polygon_modeling(depth, completion_callback):
    """Inicia modo de modelagem poligonal."""
    polygon_modeler.start_modeling(depth, completion_callback)

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

# ----- OTHER FUNCTIONS ----- #

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    imgui.get_io().display_size = w, h

def clear_scene():
    """Remove todos os objetos da lista global de objetos da cena."""
    global objects
    print(f"Limpando a cena. Total de objetos removidos:")
    objects.clear()

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

## -------- GLUT BASIC -------- ##

def display():
    global renderer, ui_state 

    # Início do frame do ImGui
    imgui.new_frame()

    # Chamada para a função de desenho do painel de controle com modelagem
    draw_control_panel(ui_state, add_object_to_scene, start_polygon_modeling, lighting_controller.enable_movable_light, clear_scene, lighting_controller.light_enabled)
    
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
        
        # Desenha Grid e Eixos 
        draw_axes()
        draw_grid()

        # Configura a iluminação 
        lighting_controller.light_setup(ui_state.ambient_light, ui_state.difuse_light, ui_state.specular_light)        
        lighting_controller.apply_light_position()

        # Aplica o shader escolhido 
        shading_controller.apply_shading(ui_state.lightning_options[ui_state.lightning_selected_index], ui_state.phong_manual)

        # Desenha cada objeto
        for obj in objects:
            glPushMatrix()
            glMultMatrixf(obj._matrix)

            is_cube = (obj.shape == 'cube')

            if ui_state.phong_manual and is_cube:
                # Guarda o programa atual para restaurar depois (opcional, mas seguro)
                glUseProgram(0) 
                glDisable(GL_LIGHTING)
                
                # Coleta dados de luz atuais
                camera_pos = (camera.camera_position_x, camera.camera_position_y, camera.camera_position_z)
                light_pos = lighting_controller.light_position
                light_colors = {
                    'amb': lighting_controller.light_ambient if ui_state.ambient_light else [0,0,0,1],
                    'dif': lighting_controller.light_diffuse if ui_state.difuse_light else [0,0,0,1],
                    'spec': lighting_controller.light_specular if ui_state.specular_light else [0,0,0,1]
                }

                # Renderiza Manualmente
                phong_manual.render_object(obj, camera_pos, light_pos, light_colors)
                
               
                glEnable(GL_LIGHTING) 
                shading_controller.apply_shading(ui_state.lightning_options[ui_state.lightning_selected_index], False) 

            else:
                glEnable(GL_LIGHTING) 
                obj.draw()

            glPopMatrix()


    # --- Renderização do ImGui ---
    imgui.render()
    renderer.render(imgui.get_draw_data())

    glutSwapBuffers()

def init():
    global shading_controller
    
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    lighting_controller.initialize_global_lighting()
    shading_controller = ShadingController()    

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
    phong_manual.update_size(current_width, current_height)
    reshape(current_width, current_height) 

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMouseFunc(lambda b, s, x, y: mouse(b, s, x, y, polygon_modeler, objects, selected_objects, camera))
    glutMotionFunc(lambda x, y: motion(x, y, polygon_modeler, camera))
    glutKeyboardFunc(lambda k, x, y: keyboard(k, x, y, polygon_modeler, selected_objects, camera, lighting_controller.light_enabled, lighting_controller))
    glutReshapeFunc(reshape) 
    glutSpecialFunc(lambda k, x, y: keyboard(k, x, y, polygon_modeler, selected_objects, camera, lighting_controller.light_enabled, lighting_controller)) 

    glutMainLoop()

if __name__ == "__main__":
    main()
