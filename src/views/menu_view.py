import arcade

# Importamos las vistas necesarias y constantes
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuView(arcade.View):
    """ Pantalla principal que aparece al iniciar el juego """

    def on_show_view(self):
        """ Se ejecuta cuando cambiamos a esta vista """
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        """ Dibujar el menú """
        
        self.clear()  # Esto limpia la pantalla con el color de fondo

       # Título principal
        arcade.draw_text(
            "PENGU AL RESCATE", 
            SCREEN_WIDTH / 2, 
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE, 
            font_size=40, 
            anchor_x="center",
            anchor_y="center"

        )
        
        # Instrucción para el jugador
        arcade.draw_text(
            "Presiona ENTER para comenzar", 
            SCREEN_WIDTH / 2, 
            SCREEN_HEIGHT * 0.4,
            arcade.color.AQUAMARINE, 
            font_size=20, 
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """ Si presiona Enter, pasamos a la vista del juego """
        if key == arcade.key.ENTER:
            from views.game_view import GameView

            game_view = GameView()

            self.window.show_view(game_view)

            # Aquí es donde mañana llamaremos a la GameView
            print("Cambiando a la vista del juego...")
            # game_view = GameView()
            # self.window.show_view(game_view)