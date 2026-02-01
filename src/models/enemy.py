import arcade
import math

class EnemigoSeguidor(arcade.Sprite):
    def __init__(self, x, y, sprite_objetivo, velocidad):
        super().__init__(":resources:images/enemies/fly.png", 0.6)
        self.center_x = x
        self.center_y = y
        self.objetivo = sprite_objetivo
        self.velocidad = velocidad

    def update(self):
        # Calcular distancia
        distancia_x = self.objetivo.center_x - self.center_x
        distancia_y = self.objetivo.center_y - self.center_y
        distancia = math.sqrt(distancia_x**2 + distancia_y**2)

        # Solo moverse si está lejos (evita vibración)
        if distancia > 3:
            angulo = math.atan2(distancia_y, distancia_x)
            self.change_x = math.cos(angulo) * self.velocidad
            self.change_y = math.sin(angulo) * self.velocidad
            
            # El sprite mire hacia donde va
            if self.change_x > 0:
                self.texture = self.textures[0] # Necesitarían cargar texturas espejo
        else:
            self.change_x = 0
            self.change_y = 0

        # Llamar al update del padre para que arcade procese el movimiento
        super().update()