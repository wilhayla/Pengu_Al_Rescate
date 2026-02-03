import arcade
from constants import PLAYER_START_X, PLAYER_START_Y, PLAYER_JUMP_SPEED, CHARACTER_SCALING

class Player(arcade.Sprite):
# Sprite del jugador (Pengu). Carga las texturas de los diferentes estados en __init__ para no recargarlas cada frame. 
# update_animation elige la textura en base a la velocidad vertical/horizontal.
# jump aplica la velocidad vertical; die reinicia posición y velocidades.

    def __init__(self):
# Inicialización del sprite: Llamamos al constructor de arcade.Sprite indicando una imagen inicial y la escala. 
# (Si quieres usar otra imagen, aqui podemos cambiarlo). Posicionamos al personaje y cargamos texturas usadas.
# Pasamos una textura por defecto y la escala al constructor padre
        super().__init__(":resources:images/animated_characters/penguin/penguin_idle.png", CHARACTER_SCALING)

        # Establecer posición inicial (centro del sprite)
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y

        # Cargar texturas UNA SOLA VEZ en el constructor:
        # - arcade.load_texture carga la imagen y devuelve un objeto Texture.
        self.texture_idle = arcade.load_texture(":resources:images/animated_characters/penguin/penguin_idle.png")
        self.texture_jump = arcade.load_texture(":resources:images/animated_characters/penguin/penguin_jump.png")
        self.texture_fall = arcade.load_texture(":resources:images/animated_characters/penguin/penguin_walk01.png")

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
