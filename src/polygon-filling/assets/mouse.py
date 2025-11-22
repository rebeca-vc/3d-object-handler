from OpenGL.GLUT import *
from .polygon import Polygon
from .button import get_clicked_button

def mouse(button, state, x, y, polygons, buttons, chosen_color_ref, current_line_thickness_ref):
    global chosen_color
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        height = glutGet(GLUT_WINDOW_HEIGHT)
        clicked_button = get_clicked_button(x,height - y, buttons)

        # verifica se clicou em um botao
        if clicked_button != None:
            if clicked_button.text == "CLEAR":
                    # limpar tela
                    for poly in polygons:
                        poly.clear()
            elif clicked_button.text == "+":
                # aumentar espessura
                current_line_thickness_ref[0] = min(10.0, current_line_thickness_ref[0] + 0.5)
            elif clicked_button.text == "-":
                # diminuir espessura
                current_line_thickness_ref[0] = max(0.5, current_line_thickness_ref[0] - 0.5)
                    
            elif clicked_button.shape == 'circle':
                # Troca cor polígono
                chosen_color_ref[0] = clicked_button.color
        else:
            # Cria o polígono
            point = [x, height - y]

            if not polygons:
                polygons.append(Polygon(chosen_color_ref[0]))
            # Adiciona o ponto no último polígono criado
            polygons[-1].add_vertex(*point)

        glutPostRedisplay()

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

        # Descobre qual polígono o clique está dentro
        height = glutGet(GLUT_WINDOW_HEIGHT)
        click_point = [x, height - y]

        first_fill = False
        for poly in reversed(polygons):
            if poly.check_inside_polygon(*click_point):
                if not poly.filled:
                    first_fill = True
                poly.fill(chosen_color_ref[0])
                poly.filled = True
                break
        
        # Cria novo polígono
        if first_fill:
            polygons.append(Polygon(chosen_color_ref[0]))
        
        glutPostRedisplay()
