# Colores, tamaños de pantalla, gravedades,  etc

# --- Configuración de Pantalla ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pengu al Rescate: Misión Ambiental"

# --- Físicas y Movimiento ---
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 12
PLAYER_START_X = 100
PLAYER_START_Y = 150

# --- Capas del Mapa (Para Tiled) ---
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_OBSTACLES = "Obstacles"
LAYER_NAME_ITEMS = "Items"

# --- Lógica de Progresión ---
POINTS_TO_LEVEL_UP = 500      # Cada cuántos puntos sube la dificultad
LEVELS_TO_NEXT_WORLD = 3      # Cada cuántos niveles de dificultad cambiamos de bioma (Hielo -> Ciudad)
INITIAL_GAME_SPEED = 5        # Velocidad inicial del suelo y obstáculos
SPEED_INCREMENT = 0.5         # Cuánto aumenta la velocidad al subir de nivel

# --- Identificadores de Mundos ---
WORLD_ARCTIC = "Arctic"
WORLD_CITY = "City"
WORLD_OCEAN = "Ocean"