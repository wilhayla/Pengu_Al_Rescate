import arcade
import math

class EnemigoSeguidor(arcade.Sprite):
    def __init__(self, x, y, sprite_objetivo, velocidad):
        """
        :param x: Posición X inicial
        :param y: Posición Y inicial
        :param sprite_objetivo: El pingüino al que debe seguir
        :param velocidad: Qué tan rápido se mueve (ej. 2 o 3)
        """
        # Cambia la ruta por tu imagen de enemigo (gaviota, robot, etc.)
        super().__init__(":resources:images/enemies/fly.png", 0.6)
        self.center_x = x
        self.center_y = y
        self.objetivo = sprite_objetivo
        self.velocidad = velocidad

    def update(self):
        # 1. Obtener la posición del pingüino
        destino_x = self.objetivo.center_x
        destino_y = self.objetivo.center_y

        # 2. Calcular el ángulo hacia el pingüino
        distancia_x = destino_x - self.center_x
        distancia_y = destino_y - self.center_y
        angulo = math.atan2(distancia_y, distancia_x)

        # 3. Aplicar movimiento basado en el ángulo
        self.change_x = math.cos(angulo) * self.velocidad
        self.change_y = math.sin(angulo) * self.velocidad

        # 4. Actualizar posición física
        self.center_x += self.change_x
        self.center_y += self.change_y