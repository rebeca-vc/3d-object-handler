import math

class Camera:
    def __init__(self, sensibility=0.5):
        self.focal_point_x = 0.0
        self.focal_point_y = 0.0
        self.focal_point_z = 0.0
        self.focal_point_distance = 8.0

        self.yaw = 45.0
        self.pitch = 30.0

        self.sensibility = sensibility

        self.mouse_button = None
        self.mouse_last_x = 0
        self.mouse_last_y = 0

        self.camera_position_x = 0
        self.camera_position_y = 0
        self.camera_position_z = 0

    # Atualiza as coordenadas da câmera com base nos parâmetros de Yaw e Pitch
    def update(self):
        # Convertendo para radianos para usar no sen/cos
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)

        # Conversão coordenadas esféricas para cartesinas
        self.camera_position_x = self.focal_point_x + self.focal_point_distance * math.cos(rad_pitch) * math.sin(rad_yaw)
        self.camera_position_y = self.focal_point_y + self.focal_point_distance * math.sin(rad_pitch)
        self.camera_position_z = self.focal_point_z + self.focal_point_distance * math.cos(rad_pitch) * math.cos(rad_yaw)

    # Define a posição inicial do mouse para futuras comparações
    def start_mouse(self, button, x, y):
        self.mouse_button = button
        self.mouse_last_x = x
        self.mouse_last_y = y

    # Define o que será feito a depender do movimento do mouse
    def move_mouse(self, x, y):
        # Calcula deltas
        dx = x - self.mouse_last_x
        dy = y - self.mouse_last_y

        # Atualiza posição atual do mouse
        self.mouse_last_x = x
        self.mouse_last_y = y

        # Faz o movimento de órbita - rotação em torno do ponto focal
        if self.mouse_button == 2:
            self.yaw += dx * self.sensibility 
            self.pitch -= dy * self.sensibility
            # Evitamos pontos de +-90° que podem causar singularidade
            self.pitch = max(-89, min(89, self.pitch))
        
        # Pan
        elif self.mouse_button == 0:
            self.pan(dx, dy)
            
    def pan(self, dx, dy):
        # Fator para correção de sensibilidade a depender da distância do ponto focal
        factor = self.focal_point_distance * 0.002

        rad_yaw = math.radians(self.yaw + 90)

        right_x = math.sin(rad_yaw)
        right_z = math.cos(rad_yaw)

        up_x = 0
        up_y = 1
        up_z = 0

        self.focal_point_x -= right_x * dx * factor
        self.focal_point_z -= right_z * dx * factor

        self.focal_point_x += up_x * dy * factor
        self.focal_point_y += up_y * dy * factor
        self.focal_point_z += up_z * dy * factor

    def dolly(self, direction):
        # Aproxima ou afasta do ponto focal
        self.focal_point_distance += direction * 0.3
        # Delimita um limite mínimo de distância
        self.focal_point_distance = max(1.0, self.focal_point_distance)