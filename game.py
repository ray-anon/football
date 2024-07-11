import pygame
import random

vector = pygame.math.Vector2

#init the pygame
pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("FootBall")
 

#set fonts and clock
FPS = 60
clock = pygame.time.Clock()

#create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group  = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()
football_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()

class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/target.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (WINDOW_WIDTH , random.randint(0 , WINDOW_HEIGHT - 100))
    
    def update(self):
        pass


#class Game
class Game():
    def __init__(self , player , football_group , football , target):
        self.score = 0
        self.lives = 10
        
        self.player = player
        self.football_group = football_group
        self.target = target
        self.is_kicked = False
        
        self.football = football
        self.player = player
    def update(self):
        self.check_collisions()
        if self.is_kicked == True:
            self.kicked()
            
        if self.football.rect.left > WINDOW_WIDTH:
            self.football.rect.topleft = (self.football.STARTING_X , self.football.STARTING_Y)
            self.is_kicked = False
    
    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player , self.football_group , False):
            self.velocity_y = self.player.velocity.x
            self.is_kicked = True
            self.player.rect.x = 0
            
        if pygame.sprite.spritecollide(self.target , self.football_group , False):
            self.target.rect.bottomright = (WINDOW_WIDTH , random.randint(0 , WINDOW_HEIGHT - 100))
    
    def kicked(self):
        self.football.rect.x += self.football.velocity_x
        self.football.rect.y -= abs(self.velocity_y * 2.26)
    

#class football
class Football(pygame.sprite.Sprite):
    def __init__(self , x , y):
        super().__init__()
        self.image = pygame.image.load("images/football.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)
        
        self.velocity_x = 10
        
        self.STARTING_X = x
        self.STARTING_Y = y
        

#class Tile
class Tile(pygame.sprite.Sprite):
    def __init__(self , x , y , image_int , main_group , sub_group=""):
        super().__init__()
        if image_int == 1:
            self.image = pygame.image.load('images/tiles/dirt.png')
        if image_int == 2:
            self.image = pygame.image.load('images/tiles/grass.png')
            self.mask = pygame.mask.from_surface(self.image)
            sub_group.add(self)
        if image_int == 3:
            self.image = pygame.image.load('images/tiles/water.png')
            sub_group.add(self)
        main_group.add(self)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)
    
    def update(self):
        pygame.draw.rect(display_surface , (255 , 0, 0 ) , self.rect , 1)
    
class Player(pygame.sprite.Sprite):
    def __init__(self , x , y , grass_tiles , water_tiles):
        super().__init__()
        
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        
        
        
        for i in range(1 , 11):
            self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/player/Idle ({i}).png") , (64 , 64)))
            self.idle_left_sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"images/player/Idle ({i}).png") , True, False) , (64 , 64)))
            if i <= 8:
                self.move_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/player/Run ({i}).png") , (64 , 64)))
            if i <= 5:
                self.move_left_sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"images/player/Slide ({i}).png") , True , False ), (64 , 64)))
        self.current_spite = 0
          
        self.image = self.idle_left_sprites[self.current_spite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x , y)
        
        
        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles
        
        #kinematics constansts
        self.HORIZONTAL_ACCELERATION = 0.44
        self.HORIZONTAL_FRICITION = 0.15
        self.VERTICAL_ACCELERATION = 0.5
        self.VERTICAL_JUMP_SPEED = 7
        
        #kinematics
        self.velocity = vector(0 , 0)
        self.acceleration = vector(0, 0)
        self.position = vector(x , y)
        
        self.STARTING_X = x
        self.STARTING_Y = y
        
    def update(self):
        pygame.draw.rect(display_surface , (0, 255 , 0) , self.rect , 1)
        
        #create a mask
        self.mask = pygame.mask.from_surface(self.image)
        
        #draw the mask
        mask_outline = self.mask.outline()
        pygame.draw.lines(self.image , (0 , 0 , 255) , True , mask_outline)
        
        self.move()
        self.check_collisions()
    
    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
        keys = pygame.key.get_pressed()
        #fuck make sure to add if and elif and else 
        #else you will fuck up very bad
        if keys[pygame.K_RIGHT] and self.rect.x < 200:
            self.acceleration.x =  self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites)
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.acceleration.x = -self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites)
            else:
                self.animate(self.idle_left_sprites)
        
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICITION
        self.velocity += self.acceleration 
        self.position += self.velocity + 0.5*self.acceleration
        
        self.rect.bottomleft = self.position
        
    def check_collisions(self):
        collided_platforms = pygame.sprite.spritecollide(self , self.grass_tiles , False , pygame.sprite.collide_mask)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 8
            self.velocity.y = 0
        if pygame.sprite.spritecollide(self , self.water_tiles , False):
            print("dead")
    
    def jump(self):
        if pygame.sprite.spritecollide(self , self.grass_tiles , False):
            self.velocity.y = -self.VERTICAL_JUMP_SPEED
    
    def animate(self , sprite_list):
        if self.current_spite < len(sprite_list) - 1:
            self.current_spite += 1
        else:
            self.current_spite = 0
        self.image = sprite_list[self.current_spite]
    
tile_map = [
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 4,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,2, 2,2,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,1, 1,1,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,0,0,0, 0,0,0,0,0, 2,2,2,2,2],
    [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,3,3,3, 3,3,3,3,3, 1,1,1,1,1],
    [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,3,3,3, 3,3,3,3,3, 1,1,1,1,1],
]

for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j * 32 , i * 32 , 1 , main_tile_group)
        if tile_map[i][j] == 2:
            Tile(j * 32 , i * 32 , 2 , main_tile_group , grass_tile_group)
        if tile_map[i][j] == 3:
            Tile(j * 32 , i * 32 , 3 , main_tile_group ,water_tile_group)
        if tile_map[i][j] == 4:
            player = Player(j * 32 , i * 32 + 32 , grass_tile_group , water_tile_group)
            my_player_group.add(player)

#football object
football = Football(8 * 32 , 16 * 32)
football_group.add(football)


#target object
target = Target()
target_group.add(target)

#game object
my_game = Game(player , football_group , football , target)

#load bg image
bg_image = pygame.image.load('images/background.png')
bg_rect = bg_image.get_rect()
bg_rect.topleft = (0 , 0)

#game loop
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            
    #blit the background
    display_surface.blit(bg_image , bg_rect)
    
    #blit the player
    my_player_group.update()
    my_player_group.draw(display_surface)
    
    #blitting the images
    main_tile_group.draw(display_surface)
    main_tile_group.update()
    
    #football group
    football_group.draw(display_surface)
    
    #game object
    my_game.update() 
    
    #target object
    target_group.update()
    target_group.draw(display_surface)
    
    
    pygame.display.update()

#quit pygame
pygame.quit()