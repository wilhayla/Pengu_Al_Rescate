import arcade
import random
from constants import *

class Obstacle(arcade.Sprite):
    def __init__(self, speed):
        # Por ahora usamos un recurso predeterminado de arcade (una roca)
        # super().__init__(":resources:images/items/rock.png", CHARACTER_SCALING)
        super().__init__()
        self.texture = arcade.make_soft_circle_texture(50, arcade.color.RED)
        
        # Posición inicial: justo fuera de la pantalla a la derecha
        self.center_x = SCREEN_WIDTH + 100
        self.center_y = 110 # Un poco arriba del suelo
        
        # self.speed = speed
        # En lugar de una variable 'speed' custom, usamos la de Arcade
        self.change_x = -speed
    
    def update(self, delta_time: float = 1 / 60):
        # Mover a la izquierda
        # self.center_x -= self.speed
        
        # 1. Dejamos que Arcade mueva el sprite automáticamente 
        # (Esto usa el valor de self.change_x que definiste en el __init__)
        super().update()
        
        # Si sale de la pantalla, eliminarse
        # if self.right < 0:
            # self.remove_from_sprite_lists()
        
        # if self.right < -1000: # <--- Opcional: Borrar solo si está MUY a la izquierda
        #     self.remove_from_sprite_lists()