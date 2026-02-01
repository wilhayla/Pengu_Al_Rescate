"""
Platformer Game

python -m arcade.examples.platform_tutorial.14_multiple_levels
"""
import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 2
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        # Variable to hold our texture for our player
        self.player_texture = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Variable to hold our Tiled Map
        self.tile_map = None

        # Replacing all of our SpriteLists with a Scene variable
        self.scene = None

        # A variable to store our camera object
        self.camera = None

        # A variable to store our gui camera object
        self.gui_camera = None

        # This variable will store our score as an integer.
        self.score = 0

        # This variable will store the text for score that we will draw to the screen.
        self.score_text = None

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level number to load
        self.level = 1

        # Should we reset the score?
        self.reset_score = True

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        layer_options = {
            "BloquesLadrillos": {
                "use_spatial_hash": True
            },
            "FondoEdificio": {
                "use_spatial_hash": False
            }
        }

        # Load our TileMap
        self.tile_map = arcade.load_tilemap(
            "nivel01v1.json",
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        # Create our Scene Based on the TileMap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Load player texture
        self.player_texture = arcade.load_texture(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        )

        # Add Player Spritelist before "Foreground"
        self.scene.add_sprite_list_after("Player", "FondoEdificio")

        # Create player sprite with same scale as tiles
        self.player_sprite = arcade.Sprite(self.player_texture, scale=TILE_SCALING * 0.5)

        # --- Posición inicial sobre un bloque sólido ---
        platforms = self.scene["BloquesLadrillos"]
        if platforms:
            first_platform = platforms[0]
            self.player_sprite.center_x = first_platform.center_x
            self.player_sprite.center_y = first_platform.center_y + \
                first_platform.height / 2 + self.player_sprite.height / 2
        else:
            # fallback si no hay bloques
            self.player_sprite.center_x = 128
            self.player_sprite.center_y = 128

        self.scene.add_sprite("Player", self.player_sprite)

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.scene["BloquesLadrillos"],
            gravity_constant=GRAVITY
        )

        # Initialize cameras
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # Reset score if needed
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Initialize score text
        self.score_text = arcade.Text(f"Score: {self.score}", x=0, y=5)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Calculate the right edge of the map in pixels
        self.end_of_map = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
        print("Ancho del mapa en pixeles:", self.end_of_map)


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate our camera before drawing
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate our GUI camera
        self.gui_camera.use()

        # Draw our Score
        self.score_text.draw()

    def on_update(self, delta_time):
        """Movement and Game Logic"""

        # Move the player using our physics engine
        self.physics_engine.update()

        # Check if the player got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1

            # Turn off score reset when advancing level
            self.reset_score = False

            # Reload game with new level
            self.setup()

        # Center our camera on the player
        self.camera.position = self.player_sprite.position


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()