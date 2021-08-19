import arcade
import random

SPRITE_SCALING_PLAYER = 0.4
SPRITE_SCALING_ENEMY = 0.4
SPRITE_SCALING_COIN = 0.5
COIN_COUNT = 0
MOVEMENT_SPEED = 4
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRAVITY = 0.5
SPRITE_SCALING_BOX = 0.3
PLAYER_JUMP_SPEED = 9
RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):


     return [
         arcade.load_texture(filename),
         arcade.load_texture(filename, flipped_horizontally=True)]

class PlayerCharacter(arcade.Sprite):
    """ Player Sprite"""
    def __init__(self):
        # Set up parent class
        super().__init__()
        self.center_x = 300
        self.center_y = 300

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = SPRITE_SCALING_PLAYER

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False


        self.jump_texture_pair = load_texture_pair("SnekJump.png")
        self.fall_texture_pair = load_texture_pair("SnekFall.png")

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
            if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
                self.character_face_direction = LEFT_FACING
            elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
                self.character_face_direction = RIGHT_FACING


               

            
            if self.change_y != 0 and not self.is_on_ladder:
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
                self.center_x = 300
                self.center_y = 300

            self.update_animation()

class Grunt(arcade.Sprite):

    def __init__(self,x,y):
        super().__init__("enemy cutout.png")
        self.center_x = x
        self.center_y = y
        self.cur_texture = 0
        self.character_face_direction = LEFT_FACING
        self.scale = SPRITE_SCALING_ENEMY





class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        

        self.player_list = None
        self.wall_list = None
        self.physics_engine = None
        self.player_sprite = None


        self.set_mouse_visible(True)

    def setup(self):
        
        self.player_list = arcade.SpriteList()
        self.player_sprite = PlayerCharacter()
        self.player_list.append(self.player_sprite)
        self.enemy_list = arcade.SpriteList()

        
        enemy = Grunt(700, 288)
        self.enemy_list.append(enemy)
    

        self.wall_list = arcade.SpriteList()
        wall = arcade.Sprite("dev tex 1.png", SPRITE_SCALING_BOX)
        wall.center_x = 300
        wall.center_y = 200
        self.wall_list.append(wall)


        wall = arcade.Sprite("dev tex 1.png", SPRITE_SCALING_BOX)
        wall.center_x = 348
        wall.center_y = 200
        self.wall_list.append(wall)

        wall = arcade.Sprite("dev tex 1.png", SPRITE_SCALING_BOX)
        wall.center_x = 396
        wall.center_y = 200
        self.wall_list.append(wall)

        wall = arcade.Sprite("dev tex 1.png", SPRITE_SCALING_BOX)
        wall.center_x = 700
        wall.center_y = 200
        self.wall_list.append(wall)


        self.background = arcade.load_texture("background.png")


        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                        self.wall_list,
                                                        GRAVITY)

            
    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(self.get_viewport()[0], self.get_viewport()[2], SCREEN_WIDTH, SCREEN_HEIGHT, self.background)




        self.wall_list.draw()
        # self.coin_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        arcade.draw_text("Test area", 550, 600, arcade.color.BLACK, 50)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED 
        elif symbol == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED 
        elif symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif symbol == arcade.key.O:
            self.player_sprite.center_x = 300
            self.player_sprite.center_y = 300

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.A or symbol == arcade.key.D:
            self.player_sprite.change_x = 0


    def update(self, delta_time):
        self.set_viewport(self.player_sprite.center_x - SCREEN_WIDTH/2, self.player_sprite.center_x + SCREEN_WIDTH/2, self.player_sprite.center_y - SCREEN_HEIGHT/2, self.player_sprite.center_y + SCREEN_HEIGHT/2)
        self.player_sprite.update(delta_time)
        self.physics_engine.update()
        self.enemy_list.update()

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()