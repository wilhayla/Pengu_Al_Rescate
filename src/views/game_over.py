import arcade

# Clase para la pantalla de Fin de Juego 
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        # Cargamos la imagen d
        self.texture = arcade.load_texture("assets/images/game_over.png")

    def on_draw(self):
        self.clear()
        # Dibujamos la imagen centrada en la pantalla
        self.texture.draw_sized(
            self.window.width / 2, 
            self.window.height / 2,
            self.window.width * 0.8, # Ajusta el tamaño si es necesario
            self.window.height * 0.4
        )
        arcade.draw_text("Presiona ESPACIO para reiniciar", self.window.width/2, 100, 
                         arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

# Clase de juego principal  
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.vidas = 3
        self.tile_map = None
        self.scene = None

    def setup(self):
        """ Configuración inicial del nivel """
        map_name = "assets/mapas/nivel1.tmx"
        layer_options = {
            "Suelo": {"use_spatial_hash": True},
            "Paredes": {"use_spatial_hash": True},
        }
        
        try:
            self.tile_map = arcade.load_tilemap(map_name, scaling=1, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
        except Exception as e:
            print(f"Error cargando mapa: {e}")
            self.scene = arcade.Scene()

    def on_draw(self):
        self.clear()
        self.scene.draw()
        arcade.draw_text(f"Score: {self.score}", 20, self.window.height - 40, arcade.color.WHITE, 14)
        arcade.draw_text(f"Vidas: {self.vidas}", 20, self.window.height - 70, arcade.color.RED, 14)

    def update(self, delta_time):
        # Verificación de Game Over
        if self.vidas <= 0:
            # Ahora llamamos a la vista que muestra la imagen
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.X:
            self.vidas -= 1