def get_edges(vertex, adjacent):
    
    if vertex[1] >= adjacent[1]:
        return None   
    
    xmax = adjacent[0]
    ymax = adjacent[1]
    xmin = vertex[0]
    ymin = vertex[1]

    inclination = 0 
    if (xmax - xmin) != 0 and (ymax - ymin) != 0:
        m = (ymax - ymin) / (xmax - xmin)
        inclination = 1/m

    return [ymax, xmin, inclination]
    
    

def get_edges_list(polygon, index):

    vertex = polygon[index]

    # ultimo ponto
    if index == len(polygon) - 1:
        next = polygon[0]
    else:
        next = polygon[index + 1]

    # primeiro ponto
    if index == 0:
        previous = polygon[len(polygon) - 1]
    else:
        previous = polygon[index - 1]

    edges_list = []
    if get_edges(vertex, next) != None:
        edges_list.append(get_edges(vertex, next))
    if get_edges(vertex, previous) != None:
        edges_list.append(get_edges(vertex, previous))

    return edges_list

def polygon_filling(polygon):

    if len(polygon) < 3:
        return

    ET = dict()
    for i in range(len(polygon)):

        edges = get_edges_list(polygon, i)
        
        if len(edges) != 0:
            if polygon[i][1] in ET:
                ET[polygon[i][1]] += edges
            else:
                ET[polygon[i][1]] = edges

    if not ET:
        return

    filled_segments = []
    y = min(ET.keys())      
    AET = []               

    while ET or AET:

        # remove arestas de ET e adiciona em AET 
        if y in ET:
            AET.extend(ET.pop(y))

        # mantém AET ordenada por x
        AET.sort(key=lambda e: e[1])

        # remore arestas já concluidas de AET quando o ymax passou
        AET = [edge for edge in AET if edge[0] > y]

        # desenhar linha de varredura
        for i in range(0, len(AET), 2):
            if i + 1 < len(AET):
                x1 = round(AET[i][1])
                x2 = round(AET[i + 1][1])
                
                # desenha linha
                filled_segments.append((y, x1, x2))

        # incrementa y
        y += 1

        # atualiza x das arestas remanescentes
        for edge in AET:
            edge[1] += edge[2]  # x = x + 1/m

        # reordena AET por x
        AET.sort(key=lambda e: e[1])
    
    return filled_segments
