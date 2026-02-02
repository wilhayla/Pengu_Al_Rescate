import arcade
from src.views.game_over_view import GameOverView

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # Vidas y Puntaje (Score) 
        self.score = 0
        self.vidas = 3
        
        # Mapa / Suelo / Paredes (Referencia a Tiled) 
        self.tile_map = None
        self.scene = None

    def setup(self):
        """ Configuración inicial del nivel """
        # Ruta al archivo Tiled 
        map_name = "assets/mapas/nivel1.tmx"
        
        # Opciones de capas para el mapa
        layer_options = {
            "Suelo": {"use_spatial_hash": True},
            "Paredes": {"use_spatial_hash": True},
        }
        
        # Cargar el mapa
        self.tile_map = arcade.load_tilemap(map_name, scaling=1, layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_draw(self):
        """ Renderizar todo """
        self.clear()
        
        # Dibujar el mapa y personajes
        self.scene.draw()
        
        # Dibujar Puntaje (Score) y Vidas en pantalla 
        arcade.draw_text(f"Score: {self.score}", 20, self.window.height - 40, arcade.color.WHITE, 14)
        arcade.draw_text(f"Vidas: {self.vidas}", 20, self.window.height - 70, arcade.color.RED, 14)

    def update(self, delta_time):
        """ Lógica de juego y colisiones """
        # Ejemplo: Si el jugador cae al vacío o toca un enemigo
        # self.vidas - = 1 
        
        # Verificación de Game Over
        if self.vidas <= 0:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        """ Ejemplo para probar: Si pulsas 'X' pierdes una vida """
        if key == arcade.key.X:
            self.vidas -= 1