import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from models.enemy import EnemigoSeguidor  #importar la clase EnemigoSeguidor

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Aquí es donde mañana guardaremos al pingüino
        self.player = None 
        self.lista_enemigos = None

    def setup(self):
        """ Configuración inicial del nivel (se llama al empezar o reiniciar) """
        # Creamos la lista de sprites
        self.lista_enemigos = arcade.SpriteList()

        # IMPORTANTE: Mañana el encargado del jugador debe darte la clase
        # Por ahora, creamos un sprite temporal para que el enemigo no falle
        self.player = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", 0.5)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2

        # 2. Creamos al enemigo y lo añadimos a su lista

        # Le pasamos self.player para que sepa a quién seguir
        malo = EnemigoSeguidor(600, 300, self.player, velocidad=2)
        self.lista_enemigos.append(malo)

    def on_show_view(self):
        """ Se ejecuta al empezar el juego """
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.setup() # <--- ¡Indispensable llamar al setup aquí!

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

        # 2. Revisar si ALGÚN enemigo de la lista tocó al pingüino
        enemigos_que_me_tocaron = arcade.check_for_collision_with_list(self.player, self.lista_enemigos)

        # 3. Si la lista no está vacía, hubo contacto
        if len(enemigos_que_me_tocaron) > 0:
            print("¡Ouch! Un enemigo te alcanzó.")
            self.perder_vida() # Función que podrías crear para manejar la muerte

    def on_key_press(self, key, modifiers):
        """ Control del pingüino """
        if key == arcade.key.ESCAPE:
            # Si se cansan, vuelven al menú
            from views.menu_view import MenuView
            self.window.show_view(MenuView())