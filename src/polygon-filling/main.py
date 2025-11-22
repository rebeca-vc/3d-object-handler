from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from assets.polygon import Polygon
from assets import mouse
from assets.button import *

polygons = []
buttons = []
chosen_color = [colors['white']]
current_line_thickness = [1.0]

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for poly in polygons:
        poly.draw_edges(current_line_thickness[0])
        poly.draw_fill()

    draw_button(Button('circle', chosen_color[0], choice=True), buttons)
    for button_element in buttons:
        draw_button(button_element)
        
    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    screen_width = glutGet(GLUT_SCREEN_WIDTH)
    screen_height = glutGet(GLUT_SCREEN_HEIGHT)

    window_width = screen_width - 100  
    window_height = screen_height - 100
    
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(50, 50)  
    glutCreateWindow(b"Trabalho 1")
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(display)
    glutMouseFunc(lambda b, s, x, y: mouse.mouse(b, s, x, y, polygons, buttons, chosen_color, current_line_thickness))
    glutMouseWheelFunc(lambda wheel, direction, x, y: mouse.scroll(wheel, direction, x, y, polygons))

    set_buttons(buttons)
    glutMainLoop()

if __name__ == "__main__":
    main()