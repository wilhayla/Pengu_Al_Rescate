import arcade
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MOVEMENT_SPEED, PLAYER_START_X, PLAYER_START_Y, CHARACTER_SCALING, TILE_SCALING, PUNTAJE_VICTORIA
from models.enemy import EnemigoSeguidor  #importar la clase EnemigoSeguidor
from models.obstacle import Obstacle
from models.player import Player
from pathlib import Path
from views.game_score import Score_Manager
from views.game_over import GameOverView

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

        self.physics_engine = None

        self.collect_item_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.golpe = arcade.load_sound(":resources:sounds/hurt1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

    def setup(self):
        """ Configuración inicial del nivel usando mapa Tiled (.tmx) """

        # 1. LÓGICA DE PERSISTENCIA
        # Esto evita que el puntaje y las vidas vuelvan a cero al morir
        if not hasattr(self, "score_manager"):
            self.score_manager = Score_Manager(self.window)

        # 1. Inicialización del Jugador
        # Nota: Asegúrate de que la clase Player herede de arcade.Sprite correctamente
        self.player = Player()
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y
        self.ganaste = False
        self.meta_puntos = PUNTAJE_VICTORIA

        file_path = Path(__file__).resolve()
        project_root = file_path.parent.parent.parent
        # Ruta a tu imagen personalizada
        coin_path = str(project_root / "assets" / "images" / "obstacles" / "banana_basura.png")

        # ==========================================================
        # IMPORTACIÓN TMX
        # ==========================================================
        map_name = "Nivel01v4.tmx" 

        layer_options = {
            "Plataforma": {
                "use_spatial_hash": True,
            },
            "Fondo": {
                "use_spatial_hash": False,
            },
        }

        try:
            # Cargamos el mapa desde la raíz
            self.tile_map = arcade.load_tilemap(
                map_name, 
                scaling=TILE_SCALING, 
                layer_options=layer_options
            )
        except Exception as e:
            print(f"Error fatal cargando el mapa: {e}")
            return

        # Inicializamos la Escena desde el mapa cargado
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Añadir al jugador a una capa específica de la escena
        self.scene.add_sprite_list("Jugador")
        self.scene.add_sprite("Jugador", self.player)

        # 1. Crear la lista en la escena
        self.scene.add_sprite_list("Coleccionables")

        # 2. Configuración de la generación aleatoria
        NUMERO_DE_ITEMS = 10
        ANCHO_MAPA = 1500 # Ajusta según el tamaño de tu nivel
        ALTO_MINIMO = 200
        ALTO_MAXIMO = 500

        for i in range(NUMERO_DE_ITEMS):
            item = arcade.Sprite(coin_path, 0.5)
            
            # Generar coordenadas aleatorias
            item.center_x = random.randrange(0, ANCHO_MAPA)
            item.center_y = random.randrange(ALTO_MINIMO, ALTO_MAXIMO)
            
            # 3. Añadir a la escena
            self.scene.add_sprite("Coleccionables", item)
        # --------------------------------------------------

        for i in range(NUMERO_DE_ITEMS):
            item = arcade.Sprite(coin_path, 0.5)
            
            colocacion_exitosa = False
            while not colocacion_exitosa:
                # Intentar una posición
                item.center_x = random.randrange(0, ANCHO_MAPA)
                item.center_y = random.randrange(ALTO_MINIMO, ALTO_MAXIMO)

                # Verificar si choca con una plataforma
                paredes_cercanas = arcade.check_for_collision_with_list(
                    item, 
                    self.scene.get_sprite_list("Plataforma")
                )

                # Si no choca con nada, lo dejamos ahí
                if len(paredes_cercanas) == 0:
                    colocacion_exitosa = True
            
            self.scene.add_sprite("Coleccionables", item)

        # Límite del mapa basado en los tiles
        self.limite_mapa_derecho = self.tile_map.width * self.tile_map.tile_width * CHARACTER_SCALING

        # ==========================================================
        # MOTOR DE FÍSICAS (CORREGIDO PARA EVITAR ATTRIBUTEERROR)
        # ==========================================================
        
        # Intentamos obtener la capa de colisiones de forma segura
        try:
            muros = self.scene.get_sprite_list("Plataforma")
        except (KeyError, AttributeError):
            print("AVISO: La capa 'Plataforma' no existe. Creando lista vacía.")
            muros = arcade.SpriteList()

        # Inicializamos el motor con la lista de muros obtenida
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, 
            walls=muros, 
            gravity_constant=0.5
        )

        # 3. Elementos dinámicos
        self.lista_enemigos = arcade.SpriteList()
        self.tiempo_proximo_enemigo = 5
        self.lista_obstaculos = arcade.SpriteList()
        self.tiempo_proximo_obstaculo = 0.5

        # 4. Cámara para el mundo
        self.camera = arcade.camera.Camera2D()
        # 5. Camara para la interfaz (queda quieta en la pantalla)
        self.gui_camera = arcade.camera.Camera2D()

    def on_show_view(self):
        """ Se ejecuta al empezar el juego """
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.setup() # <--- ¡Indispensable llamar al setup aquí!

    def on_draw(self):
        """ Aquí se dibuja el juego 60 veces por segundo """
        self.clear()

        # 1. ACTIVAR LA CÁMARA
        # Todo lo que se dibuje después de esta línea seguirá a la cámara
        self.camera.use()

        # 2. DIBUJAR LA ESCENA COMPLETA
        # Esto ya dibuja el Fondo, las Plataformas y al Jugador en el orden correcto
        self.scene.draw()

        # 3. ELEMENTOS DINÁMICOS (Si no los añadiste a la escena en el setup)
        # Solo dibujamos lo que NO esté ya dentro de self.scene
        self.lista_obstaculos.draw() 
        self.lista_enemigos.draw()

        self.score_manager.draw()

        self.gui_camera.use()

        # Dibujamos el nivel en la esquina superior izquierda
        # (Ajusta 10, 550 según el tamaño de tu ventana para que no tape los puntos)
        posicion_superior = SCREEN_HEIGHT -130

        arcade.draw_text(
            f"DIFICULTAD: {self.nivel_interfaz}",
            20,                         # Posición X
            posicion_superior,                        # Posición Y (ajustar si es necesario)
            arcade.color.ORANGE_PEEL,          
            font_size=25,
            bold=True
        )
        # ==========================================================

        if self.ganaste:
            self.gui_camera.use()
            
            # Fondo oscuro
            arcade.draw_rect_filled(
                arcade.XYWH(
                    SCREEN_WIDTH / 2, 
                    SCREEN_HEIGHT / 2, 
                    SCREEN_WIDTH, 
                    SCREEN_HEIGHT
                ),
                (0, 0, 0, 180)
            )

            # Título principal (Cambiamos start_x/y por x/y)
            arcade.draw_text(
                text="¡GANASTE!",
                x=SCREEN_WIDTH / 2,
                y=SCREEN_HEIGHT / 2 + 50,
                color=arcade.color.GOLD,
                font_size=50,
                anchor_x="center",
                bold=True
            )

            # Subtexto explicativo
            arcade.draw_text(
                text="Pasas al siguiente mundo.\nPresiona 'R' para reiniciar",
                x=SCREEN_WIDTH / 2,
                y=SCREEN_HEIGHT / 2 - 50,
                color=arcade.color.WHITE,
                font_size=20,
                anchor_x="center",
                multiline=True,
                width=SCREEN_WIDTH,
                align="center"
            )

    def on_update(self, delta_time):
        """ Aquí se mueve todo (gravedad, enemigos, etc.) """

        # <<<<<< GANAR: Si ya ganó, detenemos toda la actualización
        if self.ganaste:
            return

        # --- LÓGICA DE DIFICULTAD ---
        # Calculamos el multiplicador: aumenta 0.2 (20%) cada 100 puntos
        self.base_nivel = self.score_manager.score // 100

        # <<<<<< FUCSIA: Esta variable la usaremos para el texto en pantalla
        # Sumamos 1 para que el jugador vea "Dificultad: 1" al empezar
        self.nivel_interfaz = self.base_nivel + 1

        dificultad = 1.0 + (self.base_nivel * 0.5)

        # <<<<<< GANAR: Verificar si alcanzó la meta definida en constants
        # Importante hacerlo después de actualizar el nivel pero antes de mover todo
        if self.score_manager.score >= PUNTAJE_VICTORIA:
            self.ganaste = True
            return

        # ** Mensaje en consola para confirmar que el nivel subió **
        if self.score_manager.score > 0 and self.score_manager.score % 100 == 0:
            print(f"¡DIFICULTAD AUMENTADA! Nivel: {self.base_nivel} | Multiplicador: {dificultad}")

        # 1. Actualizar físicas (esto mueve al pingüino y aplica gravedad)
        self.physics_engine.update()
        # 2. SEGUNDO: Chequeamos si en esa nueva posición el pingüino está tocando algo
        # Obtenemos los items de la escena
        lista_recolectables = self.scene.get_sprite_list("Coleccionables")
        
        # Buscamos colisiones
        items_tocados = arcade.check_for_collision_with_list(self.player, lista_recolectables)

        # 3. TERCERO: Procesamos los resultados
        for item in items_tocados:
            item.remove_from_sprite_lists()
            self.score_manager.add_score(10)
            arcade.play_sound(self.collect_item_sound)
            # Tip: Puedes imprimirlo para estar seguro de que funciona
            print(f"¡Basura atrapada! Puntos: {self.score_manager.score}")

        # --- LÓGICA DE ENEMIGOS ---
        self.tiempo_proximo_enemigo -= delta_time

        velocidad_malo = 4 * dificultad

        if self.tiempo_proximo_enemigo <= 0:
            nuevo_malo = EnemigoSeguidor(
                self.player.center_x + 600, 
                random.randint(200, 500),   
                self.player, 
                velocidad=velocidad_malo
            )
            nuevo_malo.tiempo_de_vida = 5.0
            self.lista_enemigos.append(nuevo_malo)

            # Los enemigos aparecen más seguido a mayor dificultad
            self.tiempo_proximo_enemigo = 7 / dificultad
        
        if self.lista_enemigos:
            self.lista_enemigos.update()
            for enemigo in self.lista_enemigos:
                quedo_atras = enemigo.right < self.player.left - 200
                tiempo_agotado = False
                if hasattr(enemigo, 'tiempo_de_vida'):
                    enemigo.tiempo_de_vida -= delta_time
                    if enemigo.tiempo_de_vida <= 0:
                        tiempo_agotado = True

                if quedo_atras or tiempo_agotado:
                    enemigo.remove_from_sprite_lists()

        # --- LÓGICA DE OBSTÁCULOS (PIEDRAS) ---
        self.tiempo_proximo_obstaculo -= delta_time
        if self.tiempo_proximo_obstaculo <= 0:

            velocidad_roca = 6 * dificultad

            # Multiplicamos la velocidad base (5) por la dificultad
            nueva_roca = Obstacle(velocidad_roca)
            nueva_roca.center_x = self.player.center_x + 600 # Un poco más lejos para que de tiempo a saltar
            nueva_roca.center_y = 64
            self.lista_obstaculos.append(nueva_roca)

            # Las rocas aparecen más seguido a mayor dificultad
            self.tiempo_proximo_obstaculo = 1.2 / dificultad

        self.lista_obstaculos.update()

        # Limpieza de rocas viejas
        for roca in self.lista_obstaculos:
            if roca.right < self.player.left - 200:
                roca.remove_from_sprite_lists()

        # --- COLISIONES ---
        if self.player and self.lista_enemigos:
            if len(arcade.check_for_collision_with_list(self.player, self.lista_enemigos)) > 0:
                self.perder_vida()
                arcade.play_sound(self.golpe)

        if arcade.check_for_collision_with_list(self.player, self.lista_obstaculos):
            self.perder_vida()
            arcade.play_sound(self.golpe)

        # --- ANIMACIÓN ---
        self.player.update_animation(delta_time)

        # ==========================================================
        # 2. CORRECCIÓN DE LÍMITES (COLOCAR AL FINAL)
        # ==========================================================
        limite_final = SCREEN_WIDTH * 2

        # Límite izquierdo
        if self.player.left < 0:
            self.player.left = 0
            self.player.change_x = 0

        # Límite derecho
        # Usamos un pequeño margen de 2 píxeles para evitar que el motor lo empuje fuera
        if self.player.right > limite_final:
            self.player.right = limite_final
            self.player.change_x = 0
            self.player.center_x = limite_final - (self.player.width / 2)

        # ==========================================================
        # 3. ACTUALIZAR CÁMARA
        # ==========================================================
        cam_x = self.player.center_x
        cam_y = self.player.center_y

        # Bloqueo Izquierdo
        if cam_x < SCREEN_WIDTH / 2:
            cam_x = SCREEN_WIDTH / 2
        
        # Bloqueo Derecho 
        if cam_x > limite_final - (SCREEN_WIDTH / 2):
            cam_x = limite_final - (SCREEN_WIDTH / 2)

        self.camera.center = (cam_x, cam_y)
       
    def perder_vida(self):
        """ Esta función se ejecuta cuando chocas """
        print("¡El pingüino ha sido golpeado!")

        # 1. Restar la vida en el Score_Manager
        self.score_manager.vidas -= 1

        self.player.die()  # Esto usa el método die() que creamos en player.py
        
        # 3. Lógica de decisión: ¿Reiniciar o Game Over?
        if self.score_manager.vidas > 0:
            # Si aún tiene vidas, reiniciamos el nivel para continuar
            print(f"Vidas restantes: {self.score_manager.vidas}")
            self.setup() 
        else:
            arcade.play_sound(self.game_over)
            # Si las vidas llegan a 0
            print("GAME OVER - Sin vidas restantes")
            
            # 1. Creamos la vista de Game Over y le pasamos el score actual
            view = GameOverView(self.score_manager.score)

            # 2. Cambiamos la vista actual por la de Game Over
            self.window.show_view(view)

    def on_key_press(self, key, modifiers):
        """ Control del pingüino y navegación """
        
        # 1. SALTO: Usamos la lógica de tu clase Player
        # Solo saltamos si el motor de físicas confirma que tocamos suelo
        if key == arcade.key.SPACE or key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.jump()
                arcade.play_sound(self.jump_sound)

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