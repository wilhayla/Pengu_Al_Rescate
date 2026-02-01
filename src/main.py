# Punto de entrada donde corre el juego
import arcade
import sys
import os

# 1. Obtenemos la ruta absoluta de la carpeta 'src'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. La añadimos al buscador de Python
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


# Importamos nuestras constantes
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from views.menu_view import MenuView

class PenguGame(arcade.Window):
    """
    Esta es la clase principal que controla el juego. 
    Hereda de arcade.Window para gestionar la ventana y los eventos.
    """

    def __init__(self):
        # Llamamos al constructor de la clase padre (ventana)
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Aquí declararemos nuestras listas de Sprites (Capas)
        self.scene = None
        self.player_sprite = None
        
        # Cámara para el sistema de niveles escalables
        self.camera = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Configuración inicial del juego. Llama a esto para reiniciar el nivel. """
        
        # 1. Inicializar la cámara
        self.camera = arcade.camera.Camera2D()

        # 2. Inicializar la escena (Aquí irán el suelo y obstáculos)
        self.scene = arcade.Scene()

        # 3. Crear al jugador (Pengu)
        # Mañana cambiaremos esto por la clase Player() en un archivo separado
        img_placeholder = ":resources:images/animated_characters/robot/robot_idle.png" 
        self.player_sprite = arcade.Sprite(img_placeholder, 0.5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 150
        self.scene.add_sprite("Player", self.player_sprite)

    def on_draw(self):
        """ Renderizar la pantalla """
        self.clear()
        
        # Usar la cámara antes de dibujar la escena
        self.camera.use()
        
        # Dibujar todos los objetos del juego
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        """ Gestión de controles (Teclado) """
        if key == arcade.key.SPACE or key == arcade.key.UP:
            # Aquí irá la lógica de salto
            print("¡Pengu intenta saltar!")

    def on_update(self, delta_time):
        """ Lógica de movimiento y colisiones (60 veces por segundo) """
        # Mover los sprites
        self.scene.update(delta_time=delta_time)

def main():
    """ Función de entrada al programa """
    # 1. Creamos la ventana básica (sin lógica interna)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # 2. Creamos la instancia del Menú
    menu = MenuView()
    
    # 3. Le decimos a la ventana: "Muestra el menú"
    window.show_view(menu)
    
    # 4. Arrancamos el motor
    arcade.run()

if __name__ == "__main__":
    main()