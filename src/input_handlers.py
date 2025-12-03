from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import imgui
from object.object_selection import pick_object


def keyboard(key, x, y, polygon_modeler, selected_objects, camera, light_enabled, light):
    if polygon_modeler.is_modeling_active():
        return
    
    step = 0.5 
    # Movimentação da luz móvel
    if light_enabled:
        if key == GLUT_KEY_LEFT:
            light.update_light_position('LEFT', step)
        elif key == GLUT_KEY_RIGHT:
            light.update_light_position('RIGHT', step)
        elif key == GLUT_KEY_UP:
            light.update_light_position('UP', step)
        elif key == GLUT_KEY_DOWN:
            light.update_light_position('DOWN', step)

        elif key == b'r': 
            light.update_light_position('ELEVATE', step)
        elif key == b'f':
            light.update_light_position('LOWER', step)

        glutPostRedisplay()


    """Controle de teclado para WASD (movimento XY), Q/E (movimento Z) e Ctrl+WASD/Q/E (rotação)."""
    if not selected_objects:
        return
    
    # Verificar se Ctrl está pressionado
    modifiers = glutGetModifiers()
    is_ctrl_pressed = modifiers & GLUT_ACTIVE_CTRL
    
    move_step = 0.1
    rotate_step = 5.0  # graus
    movement_applied = False
    
    if is_ctrl_pressed:
        # Ctrl + WASD = Rotação nos eixos X e Y
        # Verificar códigos de controle
        if key == b'\x17':  # \x17 é Ctrl+W
            for obj in selected_objects:
                obj.set_rotation(obj.rotation[0] + rotate_step, obj.rotation[1], obj.rotation[2])
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) rotacionado(s) no eixo X")
            
        elif key == b'\x13':  # \x13 é Ctrl+S
            for obj in selected_objects:
                obj.set_rotation(obj.rotation[0] - rotate_step, obj.rotation[1], obj.rotation[2])
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) rotacionado(s) no eixo X")
            
        elif key == b'\x01':  # \x01 é Ctrl+A
            for obj in selected_objects:
                obj.set_rotation(obj.rotation[0], obj.rotation[1] - rotate_step, obj.rotation[2])
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) rotacionado(s) no eixo Y")
            
        elif key == b'\x04':  # \x04 é Ctrl+D
            for obj in selected_objects:
                obj.set_rotation(obj.rotation[0], obj.rotation[1] + rotate_step, obj.rotation[2])
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) rotacionado(s) no eixo Y")
        
        # Ctrl + Q/E = Rotação no eixo Z
        elif key == b'\x11':  # \x11 é Ctrl+Q
            for obj in selected_objects:
                obj.set_rotation(obj.rotation[0], obj.rotation[1], obj.rotation[2] - rotate_step)
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) rotacionado(s) no eixo Z")
            
        elif key == b'\x05':  # \x05 é Ctrl+E
            for obj in selected_objects:
                obj.set_rotation(obj.rotation[0], obj.rotation[1], obj.rotation[2] + rotate_step)
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) rotacionado(s) no eixo Z")
    
    else:
        # WASD para movimento no plano XY
        if key == b'w' or key == b'W':  # W = Movimento Y positivo (frente)
            for obj in selected_objects:
                obj.set_position(obj.position[0], obj.position[1] + move_step, obj.position[2])
            movement_applied = True
            
        elif key == b's' or key == b'S':  # S = Movimento Y negativo (trás)
            for obj in selected_objects:
                obj.set_position(obj.position[0], obj.position[1] - move_step, obj.position[2])
            movement_applied = True
            
        elif key == b'a' or key == b'A':  # A = Movimento X negativo (esquerda)
            for obj in selected_objects:
                obj.set_position(obj.position[0] - move_step, obj.position[1], obj.position[2])
            movement_applied = True
            
        elif key == b'd' or key == b'D':  # D = Movimento X positivo (direita)
            for obj in selected_objects:
                obj.set_position(obj.position[0] + move_step, obj.position[1], obj.position[2])
            movement_applied = True
        
        # Q/E para movimento no eixo Z
        elif key == b'q' or key == b'Q':  # Q = Movimento Z negativo (para frente)
            for obj in selected_objects:
                obj.set_position(obj.position[0], obj.position[1], obj.position[2] - move_step)
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) movido(s) no eixo Z - Posição: {selected_objects[0].position}")
            
        elif key == b'e' or key == b'E':  # E = Movimento Z positivo (para trás)
            for obj in selected_objects:
                obj.set_position(obj.position[0], obj.position[1], obj.position[2] + move_step)
            movement_applied = True
            print(f"{len(selected_objects)} objeto(s) movido(s) no eixo Z - Posição: {selected_objects[0].position}")
        
        if movement_applied and not (key in [b'q', b'Q', b'e', b'E']):
            print(f"{len(selected_objects)} objeto(s) movido(s) - Posição: {selected_objects[0].position}")
    
    if movement_applied:
        glutPostRedisplay()


def handle_object_selection(x, y, modifiers, objects, selected_objects):
    """Detecta Clique em objetos usando color picking"""

    if not (modifiers & GLUT_ACTIVE_CTRL):
        return False
    
    # Debug: adicionar prints para verificar se está sendo chamada
    print(f"handle_object_selection chamada: pos=({x}, {y}), objetos={len(objects)}")
    
    # Usar função otimizada de color picking
    object_id = pick_object(x, y, objects)
    print(f"pick_object retornou: {object_id}")

    if object_id >= 0 and object_id < len(objects):
        selected_obj = objects[object_id]
        if selected_obj in selected_objects: # Se já estava selecionado, desseleciona
            selected_objects.remove(selected_obj)
            print(f"Objeto {object_id} desselecionado")
        else:  # Adiciona à seleção
            selected_objects.append(selected_obj)
            print(f"Objeto {object_id} selecionado")
    else: # Ctrl+Clique no vazio limpa toda seleção
        if selected_objects:
            selected_objects.clear()
            print("Toda seleção limpa")
    return True


def mouse(button, state, x, y, polygon_modeler, objects, selected_objects, camera):
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
    
    # 3. SELEÇÃO DE OBJETOS (Ctrl+Clique)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        modifiers = glutGetModifiers()  # AQUI é onde o GLUT detecta as teclas
        
        # Se Ctrl está pressionado, processar seleção
        if modifiers & GLUT_ACTIVE_CTRL:
            handle_object_selection(x, y, modifiers, objects, selected_objects)
            return  # Não processar câmera se foi seleção
    
    # 4. CONTROLE DA CÂMERA E ESCALA (scroll)
    if state == GLUT_DOWN:
        # Alteração de escala com Ctrl+scroll (se objetos estão selecionados)
        if button == 3 or button == 4:  # Scroll wheel
            modifiers = glutGetModifiers()
            if selected_objects and (modifiers & GLUT_ACTIVE_CTRL):
                scale_step = 0.1
                if button == 3:  # Ctrl+Scroll up - aumentar escala
                    for obj in selected_objects:
                        new_scale = (obj.scale[0] + scale_step, obj.scale[1] + scale_step, obj.scale[2] + scale_step)
                        obj.set_scale(new_scale[0], new_scale[1], new_scale[2])
                    print(f"{len(selected_objects)} objeto(s) escala aumentada - Escala: {selected_objects[0].scale}")
                    glutPostRedisplay()
                    return
                elif button == 4:  # Ctrl+Scroll down - diminuir escala (mínimo 0.1)
                    for obj in selected_objects:
                        new_scale = (max(0.1, obj.scale[0] - scale_step), max(0.1, obj.scale[1] - scale_step), max(0.1, obj.scale[2] - scale_step))
                        obj.set_scale(new_scale[0], new_scale[1], new_scale[2])
                    print(f"{len(selected_objects)} objeto(s) escala diminuída - Escala: {selected_objects[0].scale}")
                    glutPostRedisplay()
                    return
            
            # Zoom da câmera (scroll normal sem Ctrl)
            if button == 3:
                camera.dolly(-1)
            elif button == 4:
                camera.dolly(1)
            return
        
        # Controle normal da câmera (se não é scroll)
        camera.start_mouse(button, x, y)


def motion(x, y, polygon_modeler, camera):
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