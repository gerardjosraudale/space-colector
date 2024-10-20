import arcade
import random

# Constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Collector"

PLAYER_SPEED = 5
STAR_SPEED = 2
ASTEROID_SPEED = 3

class SpaceCollector(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Player properties
        self.player_sprite = None
        self.player_speed = PLAYER_SPEED

        # Star and Asteroid lists
        self.star_list = None
        self.asteroid_list = None

        # Player score
        self.score = 0

        # Sound effects
        self.star_collect_sound = arcade.load_sound("assets/star_collect.wav")
        self.hit_sound = arcade.load_sound("assets/hit.wav")

        # Background music
        self.background_music = arcade.load_sound("assets/background_music.wav")  # Assuming MP3 format

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        # Initialize the player sprite
        self.player_sprite = arcade.Sprite("assets/spaceship.png", scale=0.5)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 50

        # Initialize movement
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Initialize star and asteroid lists
        self.star_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()

        # Start the score at zero
        self.score = 0

        # Add more initial stars
        for i in range(10):  # Increased number of stars
            star = arcade.Sprite("assets/star.png", scale=0.5)
            star.center_x = random.randint(20, SCREEN_WIDTH - 20)
            star.center_y = random.randint(200, SCREEN_HEIGHT - 20)
            self.star_list.append(star)

        # Play background music
        arcade.play_sound(self.background_music, volume=0.5, looping=True)

    def on_draw(self):
        arcade.start_render()
        # Draw the player, stars, and asteroids
        self.player_sprite.draw()
        self.star_list.draw()
        self.asteroid_list.draw()

        # Draw the score on the screen
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        # Apply the movement
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y

        # Boundaries check
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

        # Move stars and respawn when they move off the screen
        for star in self.star_list:
            star.center_y -= STAR_SPEED
            if star.center_y < 0:
                star.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
                star.center_x = random.randint(20, SCREEN_WIDTH - 20)

        # Check for star collection and respawn new stars after collection
        star_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.star_list)
        for star in star_hit_list:
            star.kill()
            arcade.play_sound(self.star_collect_sound)
            self.score += 1

            # Add a new star after one is collected
            new_star = arcade.Sprite("assets/star.png", scale=0.5)
            new_star.center_x = random.randint(20, SCREEN_WIDTH - 20)
            new_star.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
            self.star_list.append(new_star)

        # Add new stars randomly over time
        if random.random() < 0.01:  # 1% chance to add a new star every frame
            new_star = arcade.Sprite("assets/star.png", scale=0.5)
            new_star.center_x = random.randint(20, SCREEN_WIDTH - 20)
            new_star.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
            self.star_list.append(new_star)

    def on_key_press(self, key, modifiers):
        # Update player speed based on key press
        if key == arcade.key.UP:
            self.player_sprite.change_y = self.player_speed
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -self.player_speed
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -self.player_speed
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = self.player_speed

    def on_key_release(self, key, modifiers):
        # Stop moving the player when key is released
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player_sprite.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0

def main():
    print("Starting the game...")
    game = SpaceCollector()
    game.setup()
    arcade.run()
    print("Game loop is running.")

if __name__ == "__main__":
    main()
