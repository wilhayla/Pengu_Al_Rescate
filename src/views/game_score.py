import arcade

class Score_Manager:
    def __init__(self, window):
        self.window = window
        self.score = 0
        self.vidas = 3
        # Cámara exclusiva para la interfaz (fija en pantalla)
        self.gui_camera = arcade.camera.Camera2D()

    def add_score(self, points):
        """Suma puntos al marcador"""
        self.score += points

    def perder_vida(self):
        self.vidas -= 1
        return self.vidas  # Devolvemos cuántas quedan para saber si es Game Over
    
    def reset_score(self):
        """Reinicia el marcador a cero"""
        self.score = 0

    def draw(self):
        """Dibuja el puntaje en la pantalla usando la cámara de UI"""
        # Activamos la cámara de interfaz antes de dibujar
        self.gui_camera.use()
        
        # Dibujamos el texto en coordenadas de pantalla
        arcade.draw_text(
            f"PUNTOS: {self.score}",
            30,                          # Margen izquierdo
            self.window.height - 50,     # Margen superior
            arcade.color.WHITE,
            font_size=22,
            bold=True,
            font_name="Kenney Future"    
        )

        # 2. LÓGICA DE VIDAS AGREGADA
        # Dibujamos las vidas un poco más abajo (ajusté el margen a -90)
        arcade.draw_text(
            f"VIDAS: {self.vidas}",
            30,                          # Mismo margen izquierdo
            self.window.height - 90,     # Un poco más abajo que los puntos
            arcade.color.RED_DEVIL,      # Color rojo para resaltar que son vidas
            font_size=22,
            bold=True,
            font_name="Kenney Future"
        )