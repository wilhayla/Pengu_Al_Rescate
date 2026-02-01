import arcade
import random
from constants import *

class Obstacle(arcade.Sprite):
    def __init__(self, speed):
        # Por ahora usamos un recurso predeterminado de arcade (una roca)
        super().__init__(":resources:images/items/rock.png", CHARACTER_SCALING)
        
        # Posición inicial: justo fuera de la pantalla a la derecha
        self.center_x = SCREEN_WIDTH + 100
        self.center_y = 110 # Un poco arriba del suelo
        
        self.speed = speed
    
    def update(self):
        # Mover a la izquierda
        self.center_x -= self.speed
        
        # Si sale de la pantalla, eliminarse
        if self.right < 0:
            self.remove_from_sprite_lists()