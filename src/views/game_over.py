import arcade

class GameOverView(arcade.View):
    def __init__(self, final_score):
        super().__init__()
        self.final_score = final_score

    def on_show_view(self):
        """ Se ejecuta una vez cuando cambiamos a esta vista """
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        
        arcade.draw_text(
            "¡GAME OVER!",
            self.window.width / 2, self.window.height / 2 + 100,
            arcade.color.RED, font_size=50, anchor_x="center", font_name="Kenney Future"
        )

        arcade.draw_text(
            f"Puntaje Final: {self.final_score}",
            self.window.width / 2, self.window.height / 2,
            arcade.color.WHITE, font_size=30, anchor_x="center", font_name="Kenney Future"
        )

        arcade.draw_text(
            "Presiona 'R' para REINTENTAR o 'S' para SALIR",
            self.window.width / 2, self.window.height / 2 - 100,
            arcade.color.YELLOW, font_size=20, anchor_x="center", font_name="Kenney Future"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            # Sustituye 'GameView' por el nombre real de tu clase en game_view.py
            from .game_view import GameView 
            nuevo_juego = GameView()
            nuevo_juego.setup()
            self.window.show_view(nuevo_juego)
            
        elif key == arcade.key.S:
            arcade.exit() # Una forma más limpia de cerrar arcade