'''
''''''''''''' keyboard control'''''''
--> right key: right movement
<-- left key : left movement
 -- space key : for jumping
'''''''''''''''''''''''''''''''
'''
# -------------------- Import Libraries ----------------------
import pygame
from pygame.locals import *
from pygame import mixer
import globals
import importlib

# -------------------- Initialization ----------------------
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# -------------------- Import Custom Classes ----------------------
from player import Player
from enemy import Enemy
from button import Button

# -------------------- Game Variables ----------------------
screen_width = 960
screen_height = 640
clock = pygame.time.Clock()
main_menu = True
fps = 60
tile_size = 50
level = 1
score = 0

# -------------------- Define Colors ----------------------
white = (255, 255, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Royal Remedy Run')

# -------------------- Define fonts ----------------------
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# -------------------- Load Images ----------------------
bg_menu_img = pygame.image.load('assets/images/backgroundstart.png')
bg_img_level1 = pygame.image.load('assets/images/background1.png')
bg_img_level2 = pygame.image.load('assets/images/background2.png')
bg_img_level3 = pygame.image.load('assets/images/background3.png')
bg_img_level4 = pygame.image.load('assets/images/background4.png')
restart_img = pygame.image.load('assets/images/reset.png')
restart_img = pygame.transform.scale(restart_img, (300,100))
start_img = pygame.image.load('assets/images/start.png')
start_img = pygame.transform.scale(start_img, (300,100))
exit_img = pygame.image.load('assets/images/exit.png')
exit_img = pygame.transform.scale(exit_img, (300,100))
gate_img = pygame.image.load('assets/images/gate.png')
gate_img = pygame.transform.scale(gate_img, (300,100))
remedy_img = pygame.image.load('assets/images/remedy.png')
remedy_img = pygame.transform.scale(remedy_img, (300,100))
heart_full_img = pygame.image.load('assets/images/h1.png')
heart_half_img = pygame.image.load('assets/images/h2.png')
heart_quarter_img = pygame.image.load('assets/images/h3.png')
heart_full_img = pygame.transform.scale(heart_full_img, (40, 40))
heart_half_img = pygame.transform.scale(heart_half_img, (40, 40))
heart_quarter_img = pygame.transform.scale(heart_quarter_img, (40, 40))

# -------------------- Load Sounds ----------------------
pygame.mixer.music.load('assets/sounds/🎵 RPG Combat Music _ Hour of the Witch.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_sound = pygame.mixer.Sound('assets/sounds/coin.wav')
coin_sound.set_volume(0.3)
jump_sound = pygame.mixer.Sound('assets/sounds/Jump Sound Effect (High Quality).mp3')
jump_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('assets/sounds/Game Over sound effect.mp3')
game_over_sound.set_volume(0.7)

# -------------------- Functions ----------------------
# Function to draw text into the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# Function to display lives
def draw_lives(health):
    for i in range(3):  # Max 3 hearts
        x_pos = 10 + i * 50
        if health > i:
            if health - i >= 1:
                screen.blit(heart_full_img, (x_pos, 10))
            elif health - i == 0.5:
                screen.blit(heart_half_img, (x_pos, 10))
            else:
                screen.blit(heart_quarter_img, (x_pos, 10))
        else:
            pygame.draw.rect(screen, (0, 0, 0), (x_pos, 10, 40, 40))  # Black out empty hearts

# Function to load levels
def load_level(level):
    try:
        # Dynamically import the level module
        level_module = importlib.import_module(f'levels.level{level}')
        importlib.reload(level_module)
        return level_module.level_data  # Return the data structure
    except ModuleNotFoundError:
        print(f"Level {level} not found!") # for debugging
        return None
    except AttributeError:
        print(f"Level {level} is missing its data structure!") #for debugging
        return None

# Function to reset level
def reset_level(level):
    player.reset(100, screen_height - 130, enemy_group, lava_group, exit_group, remedy_group, jump_sound, game_over_sound)
    enemy_group.empty()
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()

# -------------------- Classes ----------------------
# World class responsible of designing the world game
class World():
    def __init__(self, data):
        self.tile_list = []
        land_img = pygame.image.load('assets/images/land.png')
        row_count = 0

        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: # if level data is 1 display land
                    img = pygame.transform.scale(land_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2: # if level data is 2 display enemy
                    enemy = Enemy(col_count * tile_size - 15, row_count * tile_size)
                    enemy_group.add(enemy)
                if tile == 3: # if level data is 3 display lava
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                if tile == 4: # if level data is 4 display coin
                    coin = Coin(col_count * tile_size +15, row_count * tile_size)
                    coin_group.add(coin)
                if tile == 5: # if level data is 5 display gate or remedy
                    # Use remedy image instead of door in the last level
                    if level == globals.max_level:  # Check if it’s the last level
                        exit_img = remedy_img  # Use the remedy image
                    else:
                        exit_img = gate_img  # Default door image
                    exit = Exit(col_count * tile_size, row_count * tile_size - 15, exit_img)
                    exit_group.add(exit)
                if tile ==6:
                    remedy = Remedy(col_count * tile_size, row_count * tile_size)
                    remedy_group.add(remedy)
                col_count += 1
            row_count += 1

    # Function to draw the world
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# class responsible of lava
class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/images/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# class responsible of remedy
class Remedy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/images/Remedy.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# class responsible of coin
class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/images/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size//2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


# class responsible of exit
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (tile_size, tile_size * 1.5))  # Use the passed image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

enemy_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
remedy_group = pygame.sprite.Group()

# -------------------- Objects initialization ----------------------
# Initializing the player from Player class
player = Player(10, 500, enemy_group, lava_group, exit_group, remedy_group, jump_sound, game_over_sound)  #player initialization
world_data = load_level(level)
world = World(world_data) #world initialization from Word class

# -------------------- Buttons ----------------------
restart_button = Button(300, 250 // 2, restart_img)
start_button = Button(screen_width // 2 - 275, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 -275, screen_height // 2 +100, exit_img)

# -------------------- Game Loop ----------------------
run = True
while run:
    clock.tick(fps)

    # start menu
    if main_menu == True:
        screen.blit(bg_menu_img, (0, 0))
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    # To control background per level
    else:
        if level == 1:
            screen.blit(bg_img_level1, (0, 0))
        if level == 2:
            screen.blit(bg_img_level2, (0, 0))
        if level == 3:
            screen.blit(bg_img_level3, (0, 0))
        if level == 4:
            screen.blit(bg_img_level4, (0, 0))

        # drawing
        world.draw()
        enemy_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        # 0 mean game is running
        if globals.game_over == 0:
            enemy_group.update()
            # Update score and add sound effects
            if pygame.sprite.spritecollide(player, coin_group, True):
               score += 1
               coin_sound.play()

            # Display the score
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 50)
            # Update Game status
            game_status = player.update(world)

            if game_status == -1:  # Player touched enemy or lava
                if globals.player_lives > 0:
                    pass
                else:
                    globals.game_over = -1  # Trigger game over

        draw_lives(globals.player_lives)  # Draw player's lives
        globals.game_over = player.update(world)  # Update the player

        # -1 means the game has stopped
        if globals.game_over == -1:
            screen.blit(bg_img_level3, (0, 0))  # Display background 3 for game over
            draw_text('GAME OVER', font, red, (screen_width // 2) - 200, screen_height // 2 - 50)
            if globals.player_lives <= 0:  # Reset only if lives are 0
                if restart_button.draw():
                    player.reset(100, screen_height - 130, enemy_group, lava_group, exit_group, remedy_group, jump_sound, game_over_sound)
                    world = World(world_data)
                    globals.player_lives = 3  # Reset lives
                    globals.game_over = 0  # Reset game state
                    score = 0


		#if player completed the level
        if globals.game_over == 1:  # Player completed the level
            # Reset game and go to the next level
            print(f"Level {level} completed! Advancing to level {level + 1}")
            level += 1
            if level <= globals.max_level:
                world_data = load_level(level)
                if world_data:
                    # Reset player and game objects
                    enemy_group.empty()
                    lava_group.empty()
                    exit_group.empty()
                    player.reset(100, screen_height - 130, enemy_group, lava_group, exit_group, remedy_group, jump_sound, game_over_sound)
                    world = World(world_data)
                    player_lives = 3  # Reset lives
                    globals.game_over = 0  # Reset the game state
                else:
                    print(f"Level {level} data is missing!")
            else:
                screen.blit(bg_img_level1, (0, 0))
                draw_text('YOU WIN!', font, white, (screen_width // 2) - 140, screen_height // 2)
            # No more levels left; allow restart to go back to level 1
                if restart_button.draw():
                    print("Restarting game. Resetting to level 1.")
                    level = 1  # Reset to level 1
                    world_data = load_level(level)
                    if world_data:
                        # Clear all groups
                        reset_level(level)
                        player.reset(100, screen_height - 130, enemy_group, lava_group, exit_group, remedy_group, jump_sound, game_over_sound)
                        world = World(world_data)
                        globals.player_lives = 3  # Reset lives
                        globals.game_over = 0  # Reset game state
                        score = 0
                    else:
                        print("Failed to load Level 1 data!")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Exit condition
            run = False

    pygame.display.update()  # For refreshing the screen

pygame.quit()
