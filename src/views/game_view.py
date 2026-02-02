import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from models.enemy import EnemigoSeguidor  #importar la clase EnemigoSeguidor

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Aquí es donde mañana guardaremos al pingüino
        self.player_sprite = None 
        self.lista_enemigos = None

    def setup(self):
        """ Configuración inicial del nivel (se llama al empezar o reiniciar) """
        # Creamos la lista de sprites
        self.lista_enemigos = arcade.SpriteList()

        # Supongamos que ya creaste a tu pingüino
        # self.player = Player(...) 

        # 2. Creamos al enemigo y lo añadimos a su lista

        # Le pasamos self.player para que sepa a quién seguir
        malo = EnemigoSeguidor(600, 300, self.player_sprite, velocidad=2)
        self.lista_enemigos.append(malo)

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
        """ Lógica de movimiento y colisiones """
        # 3. Esto hace que TODOS los enemigos en la lista ejecuten su método update()
        self.lista_enemigos.update()

    def on_key_press(self, key, modifiers):
        """ Control del pingüino """
        if key == arcade.key.ESCAPE:
            # Si se cansan, vuelven al menú
            from views.menu_view import MenuView
            self.window.show_view(MenuView())