import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from models.enemy import EnemigoSeguidor  #importar la clase EnemigoSeguidor

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Aquí es donde mañana guardaremos al pingüino
        self.player = None 
        self.lista_enemigos = None

        # 1. Declaramos la cámara
        self.camera = None

    def setup(self):
        """ Configuración inicial del nivel (se llama al empezar o reiniciar) """
        # 2. Inicializamos la cámara (Camera2D es la versión moderna en Arcade)
        self.camera = arcade.camera.Camera2D()

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

        # 3. ACTIVAR LA CÁMARA
        # Todo lo que se dibuje después de esta línea seguirá a la cámara
        self.camera.use()

        # Dibujamos los elementos del juego
        if self.player:
            self.player.draw()
        
        self.lista_enemigos.draw() # <--- ¡Faltaba esto para ver a los malos!
        
        self.clear()
        arcade.draw_text(
            "ZONA DE JUEGO", 
            SCREEN_WIDTH / 2, 
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK, 
            font_size=30, 
            anchor_x="center"
        )

    def on_update(self, delta_time):
        """ Aquí se mueve todo (gravedad, enemigos, etc.) """
        """ Lógica de movimiento y colisiones """
        # 3. Esto hace que TODOS los enemigos en la lista ejecuten su método update()
        # 1. Actualizar enemigos
        if self.lista_enemigos:
            self.lista_enemigos.update()

        # 2. Revisar si ALGÚN enemigo de la lista tocó al pingüino
        if self.player and self.lista_enemigos:
            enemigos_que_me_tocaron = arcade.check_for_collision_with_list(self.player, self.lista_enemigos)

            # 3. Si la lista no está vacía, hubo contacto
            if len(enemigos_que_me_tocaron) > 0:
                print("¡Ouch! Un enemigo te alcanzó.")
                self.perder_vida() # Función que podrías crear para manejar la muerte
                
    def perder_vida(self):
        """ Lógica para cuando el pingüino es alcanzado """
        print("Reiniciando nivel...")
        self.setup()

    def on_key_press(self, key, modifiers):
        """ Control del pingüino """
        if key == arcade.key.ESCAPE:
            # Si se cansan, vuelven al menú
            from views.menu_view import MenuView
            self.window.show_view(MenuView())