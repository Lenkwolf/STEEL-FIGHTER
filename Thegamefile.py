
import arcade
import random


from arcade.application import MOUSE_BUTTON_LEFT

SPRITE_SCALING_PLAYER = 0.4
TILE_SCALING = 0.4
SPRITE_SCALING_ENEMY = 0.4
SPRITE_SCALING_COIN = 0.5
COIN_COUNT = 0
MOVEMENT_SPEED = 4
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024
GRAVITY = 0.4
SPRITE_SCALING_BOX = 0.3
PLAYER_JUMP_SPEED = 9
RIGHT_FACING = 0
LEFT_FACING = 1
ENEMY_SPEED = 3

def load_texture_pair(filename):
     return [
         arcade.load_texture(filename),
         arcade.load_texture(filename, flipped_horizontally=True)]

class PlayerCharacter(arcade.Sprite):
    
    """ Player Sprite"""
    def __init__(self):
        # Set up parent class
        super().__init__()
        self.center_x = 735
        self.center_y = 384

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
            
            #falling 
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
                if self.cur_texture >  len(self.walk_textures)-1:
                    self.cur_texture = 0
                self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
            return
            
    def update(self, dt):
            self.center_x += self.change_x
            self.center_y += self.change_y

            if self.bottom < -400:
                self.center_x = 735
                self.center_y = 384

            self.update_animation()

class Enemy(arcade.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.cur_texture = 0
        self.change_x = ENEMY_SPEED
        self.character_face_direction = RIGHT_FACING
        self.scale = SPRITE_SCALING_ENEMY
        self.patrol = 100
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
        self.steps -= -1
        if self.steps >= 0:
            if self.center_x > self.start_x + self.patrol:
                self.change_x = -ENEMY_SPEED
                self.character_face_direction = RIGHT_FACING
            elif self.center_x < self.start_x - self.patrol:
                self.change_x = ENEMY_SPEED
                self.character_face_direction = LEFT_FACING
        else:
            if self.steps <- 60:
                self.steps = random.randint(30, 90)
    def update_animation(self, delta_time: float = 1/60):
        if self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture > len(self.idle_textures)-1:
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]

        elif self.change_x != 0:
            self.cur_texture += 1
            if self.cur_texture >  len(self.walk_textures)-1:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
    def update(self):
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.update_animation()

class MyGame(arcade.Window):

    def __init__(self):

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

        self.set_mouse_visible(True)

    def setup(self):

        map_name = ":resources:tmx_maps/map.tmx"

        platforms_layer_name = 'Tile Layer 1'

        my_map = arcade.tilemap.read_tmx("1st map.tmx")

        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                     layer_name=platforms_layer_name,
                                                     scaling=TILE_SCALING,
                                                     use_spatial_hash=True)

        self.player_list = arcade.SpriteList()
        self.player_sprite = PlayerCharacter()
        self.player_list.append(self.player_sprite)
        self.enemy_list = arcade.SpriteList()

        enemy = Enemy(3075, 448)
        self.enemy_list.append(enemy)

        self.background = arcade.load_texture("background.png")

        self.Foreground = arcade.load_texture("Foreground.png")
        
        self.logo = arcade.load_texture("assets/LOGO.png")

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                        self.wall_list,
                                                        GRAVITY)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(self.get_viewport()[0], self.get_viewport()[2], SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_lrwh_rectangle_textured(543, 270, 400, 500, self.logo)
        self.wall_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        
        arcade.draw_lrwh_rectangle_textured(self.get_viewport()[0], self.get_viewport()[2] ,1280, 1024
    , self.Foreground)

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
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        self.process_keychange()


    def on_mouse_press(self, x,y,button, modifiers):
        if button == MOUSE_BUTTON_LEFT:
            print(self.get_viewport()[0]+x , self.get_viewport()[2]+y)



    def update(self, delta_time):
        self.set_viewport(self.player_sprite.center_x - SCREEN_WIDTH/2, self.player_sprite.center_x + SCREEN_WIDTH/2, self.player_sprite.center_y - SCREEN_HEIGHT/2, self.player_sprite.center_y + SCREEN_HEIGHT/2)
        self.player_sprite.update(delta_time)
        self.physics_engine.update()
        self.enemy_list.on_update()

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()