from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)


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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)

    draw_axes()
    draw_grid()   # plano cartesiano com malha
    # draw_cube()   # seu cubo estático

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / float(h or 1), 0.1, 100)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    screen_width = glutGet(GLUT_SCREEN_WIDTH)
    screen_height = glutGet(GLUT_SCREEN_HEIGHT)

    window_width = screen_width - 100  
    window_height = screen_height - 100
    
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(50, 50)  
    glutCreateWindow(b"Trabalho 2")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()

if __name__ == "__main__":
    main()
