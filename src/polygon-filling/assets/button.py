from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class Button:
    def __init__(self, shape, color, x = None, y = None, text = None, choice = False):
        self.shape = shape
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        if(self.shape == 'square'):
            self.width = 50
            self.height = 30
        else:
            self.radius = 15
        self.choice = choice
    
    def is_inside(self, x, y):
        if(self.shape == 'square'):
            return (abs(self.x - x) < self.width/2 and (abs(self.y - y) < self.height/2))
        else:
            return (self.x - x)**2 + (self.y - y)**2 <= self.radius**2

# cores dos botões de cor
colors = {
    'white': (1.0, 1.0, 1.0),
    'red': (1.0, 0.0, 0.0),
    'green': (0.0, 1.0, 0.0),
    'gray': (0.5, 0.5, 0.5),
    'blue': (0.0, 0.0, 1.0),
    'yellow': (1.0, 1.0, 0.0),
}

def set_buttons(buttons):
    x_max = glutGet(GLUT_WINDOW_WIDTH)
    y_max = glutGet(GLUT_WINDOW_HEIGHT)

    # adiciona botões de cor à lista
    circles_offset = 40
    grid_initial_x = x_max - 50
    grid_initial_y = y_max - 80

    for i in range(len(colors)):
        column = i % 3
        line = int(i / 3)
        colors_list = list(colors.values())
        buttons.append(Button('circle', colors_list[i], 
                              grid_initial_x - circles_offset * column, 
                              grid_initial_y + circles_offset * line))

    # adiciona botão de limpar tela à lista
    square_offset = 20
    x_square = grid_initial_x - 3 * circles_offset - square_offset
    y_square = grid_initial_y + circles_offset/2

    buttons.append(Button('square', colors['gray'], x_square, y_square, "CLEAR"))

    # botão aumentar espessura
    buttons.append(Button('square', colors['gray'], x_square + 70, y_square - 60, "+"))

    # botão diminuir espessura
    buttons.append(Button('square', colors['gray'], x_square + 130, y_square - 60, "-"))


def draw_centered_text(center_x, center_y, text, font=GLUT_BITMAP_HELVETICA_12):
    # calcula comprimento e altura aprox do texto
    char_width = 7
    text_width = len(text) * char_width
    font_height = 12
    
    # calcula posicao centralizada do texto
    text_x = center_x - text_width // 2
    text_y = center_y - font_height // 4 
    
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(text_x - 3, text_y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

def draw_button(button, buttons = None):
    # desenha botões de cor
    if button.shape == 'circle':
        # configura o desenho de circulo para o circulo de escolha
        if(button.choice == True):
            chosen_button = find_chosen_button(button, buttons)
            if chosen_button == None:
                return
            button.x = chosen_button.x
            button.y = chosen_button.y
            button.radius = chosen_button.radius + 3

        segments = 16
        glBegin(GL_TRIANGLE_FAN)

        if(button.choice == True):
            glColor3f(0.75, 0.75, 0.75)
        else:
            glColor(*button.color)

        # centro
        glVertex2f(button.x, button.y)
        
        for i in range(segments+1):
            angle = 2*math.pi*i/segments
            x = button.x  
            x = button.x + button.radius * math.cos(angle)
            y = button.y + button.radius * math.sin(angle)
            glVertex2f(x, y)

        glEnd()

    # desenha botão de limpar
    elif button.shape == 'square':
        glBegin(GL_QUADS)
        glColor(*button.color)
        glVertex2f(button.x - button.width/2, button.y - button.height/2)
        glVertex2f(button.x + button.width/2, button.y - button.height/2)
        glVertex2f(button.x + button.width/2, button.y + button.height/2)
        glVertex2f(button.x - button.width/2, button.y + button.height/2)
        glEnd()
        
        # desenha texto centralizado
        draw_centered_text(button.x, button.y, button.text)

def get_clicked_button(x, y, buttons):
    for button in buttons:
        if(button.is_inside(x, y)):
            return button
    return None

# pode ser usado para botões quadrados de cores diferentes também
def find_chosen_button(choice_button, buttons):
    if(buttons == None):
        return None
        
    for button in buttons:
        if button.shape != choice_button.shape:
            continue
    
        if(choice_button.color == button.color):
            return button
    
    return None