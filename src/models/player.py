import arcade

# DATOS GLOBALES DEL JUEGO

SCREEN_WIDTH = 800                       # Ancho de la ventana en píxeles
SCREEN_HEIGHT = 600                      # Alto de la ventana en píxeles
SCREEN_TITLE = "PENGU AL RESCATE: MISION AMBIENTAL"

CHARACTER_SCALING = 0.8                  # Factor que escala el sprite respecto a su tamaño original
TILE_SCALING = 0.5                       # Factor que escala los tiles del suelo

# FÍSICAS Y MOVIMIENTO

GRAVITY = 0.5                            # Gravedad aplicada por el motor
PLAYER_JUMP_SPEED = 12                   # Velocidad vertical que se aplica al saltar
PLAYER_START_X = 100                     # Posición X inicial del jugador
PLAYER_START_Y = 150                     # Posición Y inicial del jugador
PLAYER_MOVEMENT_SPEED = 5                # Velocidad horizontal del jugador

# CLASE DEL PERSONAJE (PENGU)

class Player(arcade.Sprite):
# Sprite del jugador (Pengu). Carga las texturas de los diferentes estados en __init__ para no recargarlas cada frame. 
# update_animation elige la textura en base a la velocidad vertical/horizontal.
# jump aplica la velocidad vertical; die reinicia posición y velocidades.

    def __init__(self):
# Inicialización del sprite: Llamamos al constructor de arcade.Sprite indicando una imagen inicial y la escala. 
# (Si quieres usar otra imagen, aqui podemos cambiarlo). Posicionamos al personaje y cargamos texturas usadas.
# Pasamos una textura por defecto y la escala al constructor padre
        super().__init__(":resources:images/animated_characters/male_person/malePerson_idle.png", CHARACTER_SCALING)

        # Establecer posición inicial (centro del sprite)
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y

        # Cargar texturas UNA SOLA VEZ en el constructor:
        # - arcade.load_texture carga la imagen y devuelve un objeto Texture.
        self.texture_idle = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_idle.png")
        self.texture_jump = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_jump.png")
        self.texture_fall = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_fall.png")

        # La propiedad self.texture es la que se dibuja; inicializamos con idle
        self.texture = self.texture_idle

    def update_animation(self, delta_time: float = 1/60):
        # Elegir la textura a mostrar según la velocidad vertical:- self.change_y > 0 -> salto (subiendo)- self.change_y < 0 -> caída - else -> idle
        # change_y es administrado por PhysicsEnginePlatformer
        if self.change_y > 0:
            # El personaje está subiendo: mostrar textura de salto
            self.texture = self.texture_jump
        elif self.change_y < 0:
            # El personaje está bajando: textura de caída
            self.texture = self.texture_fall
        else:
            # Personaje en suelo o sin velocidad vertical importante: idle
            self.texture = self.texture_idle

    def jump(self):
# Aplica la velocidad vertical para saltar. La comprobación de si puede saltar (si está tocando suelo) se hace normalmente en on_key_press con physics_engine.can_jump().

        self.change_y = PLAYER_JUMP_SPEED

    def die(self):
# Reinicia la posición y las velocidades del jugador. Aquí también podrías decrementar vidas o reubicar objetos.
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y
        self.change_x = 0
        self.change_y = 0

# CLASE PRINCIPAL DEL JUEGO

class MyGame(arcade.Window):
# Ventana principal del juego: maneja la inicialización, el dibujo, los inputs y la lógica. Separar setup() de __init__ permite reiniciar niveles sin recrear la ventana.

    def __init__(self):
# Inicializa la ventana y variables del estado del juego (listas/objetos creados en setup).
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables que serán inicializadas en setup()
        self.player_list = None       # SpriteList para el jugador
        self.wall_list = None         # SpriteList para muros/platforms
        self.player_sprite = None     # Referencia al objeto Player
        self.physics_engine = None    # PhysicsEnginePlatformer que gestiona gravedad/colisiones

        # Color de fondo (solo estética)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
# Crea y configura los elementos del juego: SpriteLists (eficientes para dibujar/actualizar) - Player y muros del suelo - PhysicsEnginePlatformer con gravedad
# Crear listas de sprites
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Crear e insertar el jugador en la lista
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # Crear el suelo con tiles repetidos para cubrir la pantalla
        # Nota: tile_width es un "magic number" que depende del tamaño real del tile
        tile_width = 64  # px (ajusta si cambias el recurso del tile)
        for x in range(0, SCREEN_WIDTH + tile_width, tile_width):
            # Creamos cada tile usando un recurso incluido en arcade
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x + tile_width // 2  # Centrar el tile en el segmento
            wall.center_y = 32                    # Altura fija del suelo
            self.wall_list.append(wall)

        # Crear motor de físicas: se encarga de aplicar gravedad y resolver colisiones
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def on_draw(self):
# Dibujar la escena cada frame: primero fondo y muros, luego sprites del jugador.
        self.clear()            # Limpia la pantalla (rellena con background color)
        self.wall_list.draw()   # Dibujar muros/tiles (deben ir detrás normalmente)
        self.player_list.draw() # Dibujar jugador y otros sprites por encima

    def on_key_press(self, key, modifiers):
# Maneja teclas presionadas: SPACE: salta si el physics engine reporta que puede saltar (on ground) - LEFT/A, RIGHT/D: cambia la velocidad horizontal del jugador
    
        if key == arcade.key.SPACE and self.physics_engine and self.physics_engine.can_jump():
            self.player_sprite.jump()
        elif key in (arcade.key.LEFT, arcade.key.A):
            # Mover izquierda: velocidad horizontal negativa
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            # Mover derecha: velocidad horizontal positiva
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
# Al soltar teclas de movimiento horizontal, detener el movimiento poniendo change_x a 0.
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
#          1) physics_engine.update()  -> resolver colisiones / aplicar gravedad
#          2) sprite lists update()    -> permite que sprites actualicen su estado si implementan update()
#          3) update_animation(...)    -> usar delta_time para animaciones dependientes del tiempo

        # Actualizar físicas (mueve y resuelve colisiones)
        if self.physics_engine:
            self.physics_engine.update()

        # Actualizar listas de sprites (llama a update() de cada sprite si existe)
        if self.player_list:
            self.player_list.update()

        # Actualizar animación del jugador (pasamos delta_time en caso de usarlo)
        if self.player_sprite:
            self.player_sprite.update_animation(delta_time)

        # Reiniciar si cae fuera de la pantalla (y aquí podrías restar vidas/puntuación)
        if self.player_sprite and self.player_sprite.center_y < 0:
            self.player_sprite.die()

# EJECUCIÓN DEL JUEGO
if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
    