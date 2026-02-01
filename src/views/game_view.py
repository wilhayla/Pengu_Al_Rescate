import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Aquí es donde mañana guardaremos al pingüino
        self.player_sprite = None 

    def on_show_view(self):
        """ Se ejecuta al empezar el juego """
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        """ Aquí se dibuja el juego 60 veces por segundo """
        self.clear()
        
        self.clear()
        arcade.draw_text(
            "ZONA DE JUEGO", 
            SCREEN_WIDTH / 2, 
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK, 
            font_size=30, 
            anchor_x="center"
        )
        arcade.draw_text(
            "Mañana aquí pondremos al pingüino", 
            SCREEN_WIDTH / 2, 
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.DARK_BLUE, 
            font_size=15, 
            anchor_x="center"
        )

    def on_update(self, delta_time):
        """ Aquí se mueve todo (gravedad, enemigos, etc.) """
        pass

    def on_key_press(self, key, modifiers):
        """ Control del pingüino """
        if key == arcade.key.ESCAPE:
            # Si se cansan, vuelven al menú
            from views.menu_view import MenuView
            self.window.show_view(MenuView())