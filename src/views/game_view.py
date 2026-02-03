import arcade
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MOVEMENT_SPEED
from models.enemy import EnemigoSeguidor  #importar la clase EnemigoSeguidor
from models.obstacle import Obstacle
from models.player import Player

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Aquí es donde mañana guardaremos al pingüino
        self.player = None 
        self.player_list = None # <--- Nueva lista para el jugador
        self.lista_enemigos = None
        
        # 1. Declaramos la cámara
        self.camera = None

        # --- NUEVO: Lista de obstáculos y temporizador ---
        self.lista_obstaculos = None
        self.tiempo_proximo_obstaculo = 0.0

    def setup(self):
        """ Configuración inicial del nivel (se llama al empezar o reiniciar) """
        
        # IMPORTANTE: Mañana el encargado del jugador debe darte la clase
        # Por ahora, creamos un sprite temporal para que el enemigo no falle
        # Creamos la lista y añadimos al jugador dentro
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player = Player()
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player) # <--- Lo metemos en la lista

        for x in range(0, SCREEN_WIDTH * 2, 64): # Suelo largo para poder caminar
            suelo = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
            suelo.center_x = x
            suelo.center_y = 32
            self.wall_list.append(suelo)

        # IMPORTANTE: Para que el pingüino no atraviese el suelo, 
        # necesitamos el motor de físicas en la vista principal
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, 
            self.wall_list, # Asegúrate de tener una lista de suelos/muros
            gravity_constant=0.5
        )

        # Creamos la lista de sprites
        self.lista_enemigos = arcade.SpriteList()

        # 2. Creamos al enemigo y lo añadimos a su lista
        # Le pasamos self.player para que sepa a quién seguir
        malo = EnemigoSeguidor(600, 300, self.player, velocidad=2)
        self.lista_enemigos.append(malo)

        # --- NUEVO: Inicializar lista de obstáculos ---
        self.lista_obstaculos = arcade.SpriteList()
        self.tiempo_proximo_obstaculo = 0.5  # El primer obstáculo sale a los 2 segundos

        # 2. Inicializamos la cámara (Camera2D es la versión moderna en Arcade)
        self.camera = arcade.camera.Camera2D()
        self.camera.center = self.player.position

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

        # 2. DIBUJAR EL SUELO (Debe ir primero para que esté al fondo)
        if self.wall_list:
            self.wall_list.draw()

        # Dibujamos los elementos del juego
        '''
        if self.player_list:
            self.player_list.draw()
        
        if self.lista_enemigos:
            self.lista_enemigos.draw() # <--- ¡Faltaba esto para ver a los malos!

        if self.lista_obstaculos:
            self.lista_obstaculos.draw()'''
        self.lista_obstaculos.draw() 
        self.lista_enemigos.draw()
        self.player_list.draw()
        
        arcade.draw_text(
            "ZONA DE JUEGO", 
            self.player.center_x, # <-- CAMBIO: Dibujamos el texto sobre el robot para debug
            self.player.center_y + 100,
            arcade.color.BLACK, 
            font_size=20, 
            anchor_x="center"
        )

    def on_update(self, delta_time):
        """ Aquí se mueve todo (gravedad, enemigos, etc.) """
        """ Lógica de movimiento y colisiones """

        # 1. Actualizar físicas (esto mueve al pingüino y aplica gravedad)
        self.physics_engine.update()

        # 2. Actualizar la animación del pingüino
        self.player.update_animation(delta_time)
        
        # 3. Esto hace que TODOS los enemigos en la lista ejecuten su método update()
        # 1. Actualizar enemigos
        if self.lista_enemigos:
            self.lista_enemigos.update()

        # 2. # 2. Colisión con enemigos
        if self.player and self.lista_enemigos:
            enemigos_que_me_tocaron = arcade.check_for_collision_with_list(self.player, self.lista_enemigos)

            # 3. Si la lista no está vacía, hubo contacto
            if len(enemigos_que_me_tocaron) > 0:
                print("¡Ouch! Un enemigo te alcanzó.")
                self.perder_vida() # Función que podrías crear para manejar la muerte
        
        # 3. Lógica de generación de obstáculos
        self.tiempo_proximo_obstaculo -= delta_time
        # Este print te dirá cuánto tiempo falta en cada segundo
        # (Solo imprimimos cuando sea entero para no inundar la consola)
        if int(self.tiempo_proximo_obstaculo * 10) % 10 == 0:
            print(f"Reloj piedras: {self.tiempo_proximo_obstaculo:.1f}")

        if self.tiempo_proximo_obstaculo <= 0:
            print("¡EL RELOJ LLEGÓ A CERO! Creando piedra...")
            # Creamos la roca con una velocidad de 5
            nueva_roca = Obstacle(speed=5)

            nueva_roca.center_x = self.player.center_x + 400
            nueva_roca.center_y = 64
            # RECUERDA: Si el robot se mueve, ajusta la X aquí:
            # nueva_roca.center_x = self.player.center_x + 500
            self.lista_obstaculos.append(nueva_roca)
            print(f"¡PIEDRA CREADA! Total en lista: {len(self.lista_obstaculos)}")
            
            # Reiniciamos el tiempo (sale uno nuevo cada 1.5 a 3 segundos)
            # self.tiempo_proximo_obstaculo = random.uniform(1.5, 3.0)
            self.tiempo_proximo_obstaculo = 1.0

        # 4. Actualizar movimiento de las rocas
        self.lista_obstaculos.update()

        # 5. Colisión con obstáculos
        if arcade.check_for_collision_with_list(self.player, self.lista_obstaculos):
            print("¡AUCH! El robot chocó con una piedra.")
            # Aquí podrías restar vidas o ir a Game Over
            self.perder_vida()

        # 6. ACTUALIZAR CÁMARA (Forma correcta para tu versión)
        # Esto mantiene al robot en el centro siempre
        self.camera.center = self.player.position

        for roca in self.lista_obstaculos:
            if roca.right < self.player.left - 200: # Si la roca ya pasó al pingüino por mucho
                roca.remove_from_sprite_lists()
       
    def perder_vida(self):
        """ Esta función se ejecuta cuando chocas """
        print("¡El pingüino ha sido golpeado!")
        self.player.die()  # Esto usa el método die() que creamos en player.py
        
        # Opcional: Si quieres que el enemigo también vuelva a su sitio
        self.setup() # Esto reiniciaría todo el nivel

    def on_key_press(self, key, modifiers):
        """ Control del pingüino y navegación """
        
        # 1. SALTO: Usamos la lógica de tu clase Player
        # Solo saltamos si el motor de físicas confirma que tocamos suelo
        if key == arcade.key.SPACE or key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.jump()

        # 2. MOVIMIENTO LATERAL: (Opcional, según tu diseño)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

        # 3. NAVEGACIÓN: Salir al menú
        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)