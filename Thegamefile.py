
import arcade
import random
import math

from arcade.application import MOUSE_BUTTON_LEFT
from arcade.draw_commands import draw_lrwh_rectangle_textured
from arcade.key import ESCAPE
SPRITE_SCALING_BULLET = 0.4
SPRITE_SCALING_PLAYER = 0.4
TILE_SCALING = 0.4
SPRITE_SCALING_ENEMY = 0.4
SPRITE_SCALING_COIN = 0.5
COIN_COUNT = 0
MOVEMENT_SPEED = 4
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
GRAVITY = 0.4
SPRITE_SCALING_BOX = 0.3
PLAYER_JUMP_SPEED = 9
RIGHT_FACING = 0
LEFT_FACING = 1
ENEMY_SPEED = 3
BULLET_SPEED = 45
PARTICLE_GRAVITY = 0.2
PARTICLE_FADE_RATE = 1
PARTICLE_MIN_SPEED = 0
PARTICLE_SPEED_RANGE = 2.5
PARTICLE_COUNT = 550
PARTICLE_RADIUS = 3
PARTICLE_COLORS = [arcade.color.ALIZARIN_CRIMSON,
                   arcade.color.RED,
                   arcade.color.RED_BROWN,
                   arcade.color.KU_CRIMSON,
                   arcade.color.RED_DEVIL]


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)]


class PlayerCharacter(arcade.Sprite):

    """ Player Sprite"""

    def __init__(self):
        # Set up parent class
        super().__init__()
        # Default to face-right
        self.character_face_direction = RIGHT_FACING
        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = SPRITE_SCALING_PLAYER
        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.fall_texture_pair = load_texture_pair("RexFall.png")
        # Load textures for idling
        self.idle_textures = []
        for i in range(8):
            for j in range(10):
                texture = load_texture_pair(f"./idle/Idle_{i}.png")
                self.idle_textures.append(texture)

        # load textures for walking
        self.walk_textures = []
        for i in range(6):
            for j in range(4):
                texture = load_texture_pair(f"./Run/Run_{i}.png")
                self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_textures[0][0]

    def update_animation(self, delta_time: float = 1/60):

        #left and right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # falling
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]

        # Idle animation
        elif self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture > len(self.idle_textures)-1:
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]

        # walking animation
        elif self.change_x != 0:
            self.cur_texture += 1
            if self.cur_texture > len(self.walk_textures)-1:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
        return

    def update(self, dt):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.update_animation()


class Particle(arcade.SpriteCircle):
    """ Explosion particle """

    def __init__(self, my_list):
        color = random.choice(PARTICLE_COLORS)
        super().__init__(PARTICLE_RADIUS, color)
        self.normal_texture = self.texture
        self.my_list = my_list
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed
        self.my_alpha = 255

    def update(self):
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY


class Enemy(arcade.Sprite):
    '''sets up enemies'''

    def __init__(self, x, y, patrol):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.cur_texture = 0
        self.change_x = ENEMY_SPEED
        self.character_face_direction = LEFT_FACING
        self.scale = SPRITE_SCALING_ENEMY
        self.patrol = patrol
        self.start_x = x
        self.steps = random.randint(30, 90)
        self.idle_textures = []
        for i in range(8):
            for j in range(10):
                texture = load_texture_pair(f"./enemyidle/enemy_{i}.png")
                self.idle_textures.append(texture)

        self.walk_textures = []
        for i in range(2):
            for j in range(4):
                texture = load_texture_pair(f"./enemywalk/enemyrun_{i}.png")
                self.walk_textures.append(texture)

        self.texture = self.idle_textures[0][0]

    def on_update(self, delta_time):
        self.update()
        self.steps -= 1

        if self.steps < - 60:
            self.steps = random.randint(10, 20)
        elif self.steps <= 0:
            if self.center_x > self.start_x + self.patrol:
                self.change_x = -ENEMY_SPEED
                self.character_face_direction = RIGHT_FACING
            elif self.center_x < self.start_x - self.patrol:
                self.change_x = ENEMY_SPEED
                self.character_face_direction = LEFT_FACING

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture > len(self.idle_textures)-1:
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]

        elif self.change_x != 0:
            self.cur_texture += 1
            if self.cur_texture > len(self.walk_textures)-1:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.update_animation()


class Win(arcade.Sprite):
    '''allows player to progress through levels'''

    def __init__(self, x, y):

        super().__init__("dev tex 1.png", 0.2)
        self.center_x = x
        self.center_y = y


class MyGame(arcade.Window):
    '''sets up the game function'''

    def __init__(self):
        '''sets up assets'''
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "STEEL FIGHTER")

        self.player_list = None
        self.wall_list = None
        self.physics_engine = None
        self.player_sprite = None
        self.enemy_sprite = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.bullet_list = None
        self.explosions_list = None
        self.level = 1
        self.set_mouse_visible(True)
        self.win_list = None

    def setup(self, level):
        '''sets up map and enemies'''
        map_name = ":resources:tmx_maps/map.tmx"

        platforms_layer_name = 'Tile Layer 1'

        my_map = arcade.tilemap.read_tmx(f"{level} map.tmx")

        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)
        self.win_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 1376
        self.player_sprite.center_y = 1200
        self.player_list.append(self.player_sprite)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        if level == 1:
            enemy = Enemy(3714, 1280, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(4667, 1406, 70)
            self.enemy_list.append(enemy)

            enemy = Enemy(4250, 1727, 40)
            self.enemy_list.append(enemy)

            enemy = Enemy(7230, 2045, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(7230, 1790, 150)
            self.enemy_list.append(enemy)

            win = Win(8926, 2151)
            self.win_list.append(win)
            self.background = arcade.load_texture("background.png")

        if level == 2:
            enemy = Enemy(2624, 1408, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(2111, 1282, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(3262, 1664, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(4251, 1664, 30)
            self.enemy_list.append(enemy)

            enemy = Enemy(4918, 1539, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(5912, 1539, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(6746, 1664, 100)
            self.enemy_list.append(enemy)

            enemy = Enemy(7583, 1728, 100)
            self.enemy_list.append(enemy)

            self.background = arcade.load_texture("level 2 background.png")
            self.player_sprite.center_x = 930
            self.player_sprite.center_y = 1200

        self.Foreground = arcade.load_texture("Foreground.png")

        self.logo = arcade.load_texture("assets/LOGO.png")

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        '''draws the map and entities'''
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(self.get_viewport()[0], self.get_viewport()[
                                            2], SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_lrwh_rectangle_textured(1181, 1077, 400, 500, self.logo)

        self.wall_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.explosions_list.draw()
        self.win_list.draw()
        arcade.draw_lrwh_rectangle_textured(self.get_viewport()[0], self.get_viewport()[
                                            2], 1280, 960, self.Foreground)

    def process_keychange(self):

        if self.up_pressed and not self.down_pressed:
            if (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True

            # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.ENTER:
            bullet = arcade.Sprite("Bullet.png", SPRITE_SCALING_BULLET)
            # Give the bullet a speed
            if self.player_sprite.character_face_direction == RIGHT_FACING:
                bullet.change_x = BULLET_SPEED
                bullet.angle = 0
                bullet.center_x = self.player_sprite.center_x+30
                bullet.bottom = self.player_sprite.center_y-15
            if self.player_sprite.character_face_direction == LEFT_FACING:
                bullet.change_x = -BULLET_SPEED
                bullet.angle = 180
                bullet.center_x = self.player_sprite.center_x-30
                bullet.bottom = self.player_sprite.center_y-15
            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.ESCAPE:
            ESCAPE = True
        self.process_keychange()

    def on_mouse_press(self, x, y, button, modifiers):
        map_mouse_x = self.get_viewport()[0] + x
        map_mouse_y = self.get_viewport()[2] + y
        print(f'{map_mouse_x = } {map_mouse_y = } ')

    def update(self, delta_time):
        '''updates time and checks for collisions'''
        self.set_viewport(self.player_sprite.center_x - SCREEN_WIDTH/2, self.player_sprite.center_x + SCREEN_WIDTH/2,
                          self.player_sprite.center_y - SCREEN_HEIGHT/2, self.player_sprite.center_y + SCREEN_HEIGHT/2)
        self.player_sprite.update(delta_time)
        self.bullet_list.update()
        self.physics_engine.update()
        self.enemy_list.on_update()
        self.explosions_list.update()
        if self.player_sprite.center_y <= 400:
            self.setup(self.level)

        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list)
        for enemy in enemy_hit_list:
            if enemy_hit_list:
                self.setup(self.level)

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.enemy_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            for enemy in hit_list:
                for i in range(PARTICLE_COUNT):
                    particle = Particle(self.explosions_list)
                    particle.position = enemy.position
                    self.explosions_list.append(particle)
                enemy.remove_from_sprite_lists()
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.wall_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            if bullet.center_x > self.get_viewport()[0] + SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        win_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.win_list)
        for win in win_hit_list:

            if win_hit_list:
                self.level += 1
                self.setup(self.level)


def main():
    window = MyGame()
    window.setup(1)
    arcade.run()


if __name__ == "__main__":
    main()
