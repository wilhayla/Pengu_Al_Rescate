import arcade
import sys
import os

# 1. Configuración de rutas (Mantenemos esto porque es muy útil)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 2. Importamos lo necesario
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from views.menu_view import MenuView

def main():
    """ Función de entrada única al programa """
    # 1. Creamos la ventana física (el contenedor)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # 2. Creamos la vista inicial
    menu = MenuView()
    
    # 3. Mostramos el menú
    window.show_view(menu)
    
    # 4. ¡A jugar!
    arcade.run()

if __name__ == "__main__":
    main()