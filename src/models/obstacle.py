import arcade
import os
from pathlib import Path
import random
from constants import *

class Obstacle(arcade.Sprite):
    def __init__(self, speed):
        # 1. Ruta segura
        file_path = Path(__file__).resolve()
        project_root = file_path.parent.parent.parent
        
        # 2. NOMBRE DEL ARCHIVO (¡VERIFICA ESTO!)
        # Si en tu carpeta el archivo se llama 'lata.png', cámbialo aquí.
        # Si se llama 'lata_basura.png', cámbialo aquí.
        nombre_archivo = "basurero.png" 
        
        image_path = str(project_root / "assets" / "images" / "obstacles" / nombre_archivo)
        
        # 3. Inicializar
        super().__init__(image_path, CHARACTER_SCALING)
        
        # Posición inicial: justo fuera de la pantalla a la derecha
        self.center_x = SCREEN_WIDTH + 100
        self.center_y = 130 # Un poco arriba del suelo
        
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